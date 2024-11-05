import torch
import json
from tqdm import tqdm
import torch
from torch.utils.data import  DataLoader
import random

MAX_SPAN_SIZE_RATIO = 20 # max_span_size += (max_span_size * MAX_SPAN_SIZE_RATIO) // 100
def read_data(data_path):
    data_file = open(data_path, 'r', encoding='utf-8')
    data = json.load(data_file)
    #data = data[:2000]
    data_file.close()
    return data

class DataProcessor:
    def __init__(self,tokenizer, data_path,
                input_max_length,
                batch_size=None,
                shuffle=False,
                entity_types={},
                mode='train' ):
        
        self.data_path = data_path
        self.mode = mode

        self.input_max_length = input_max_length
        self.max_potenial_length = 0

        self.batch_size = batch_size
        self.shuffle = shuffle
            
        # tokenizer information
        self.tokenizer = tokenizer
        self.start_token = tokenizer.cls_token
        self.end_token = tokenizer.sep_token
        self.pad_token = tokenizer.pad_token
        self.unk_token = tokenizer.unk_token

        # data loss
        self.deleted_data = 0
        self.total_tokens, self.total_unk_tokens = 0, 0

        # entity and relation types
        self.entity_types = { k : {'id' : v, 'count' : 0} for k,v in entity_types.items()} 
      

    
    def tokenize(self, pre_tokens):
        # encoding
        tokens = []
        input_tokens = [-1]
        tokens_by_id = {}
        start = 0
        for i, pre_token in enumerate(pre_tokens):
            current_tokens = self.tokenizer.tokenize(pre_token)
            if len(current_tokens) == 0:
                current_tokens = [self.unk_token]
                self.total_unk_tokens += 1

            tokens_by_id[i] = {'tokens': current_tokens, 'start': start, 'end': start + len(current_tokens)}
            start += len(current_tokens)
            tokens = tokens + current_tokens
            input_tokens += [i] * len(current_tokens)
            self.total_tokens += len(current_tokens)
        
        tokens = [self.start_token] + tokens + [self.end_token]
        if self.input_max_length and len(tokens) > self.input_max_length:
            print('Max length exceeded : ', len(tokens))
            self.deleted_data += 1
            return None
        
        self.max_potenial_length = max(self.max_potenial_length, len(tokens))
        return {
            'tokens': tokens,
            'tokens_by_id': tokens_by_id,
            'input_tokens': input_tokens
        }


    def preCreateItem_(self,sequence):
        pre_tokens = sequence['tokens']
        entities = sequence['entities'] if 'entities' in sequence else []
        output = self.tokenize(sequence['tokens'])
        if not output:
            return None
        tokens, tokens_by_id = output['tokens'], output['tokens_by_id']
        # create encoding
        context_size = len(tokens)
        encoding_ = self.tokenizer.convert_tokens_to_ids(tokens)
        
        if self.mode == 'predict':
            doc_ = dict({
                'pre_tokens': pre_tokens,
                'tokens_by_id': tokens_by_id,
                'input_tokens': output['input_tokens'],
                'entities': entities,
                'encoding': encoding_,
            })
            return doc_
        
        
        # entities only positive at this stage
        entity_labels = [0]*context_size
        for entity in entities:
            start, end = tokens_by_id[entity['start']]['start'] + 1, tokens_by_id[entity['end']-1]['end'] + 1
            # for entity classification
            # mask
            if f"B-{entity['type']}" not in self.entity_types:
                if self.mode != 'train':
                    print('Entity type not found')
                    self.deleted_data += 1
                    return None
                self.entity_types[f"B-{entity['type']}"] = {'id' : self.id_ent, 'count' : 0}
                self.id_ent += 1
                self.entity_types[f"I-{entity['type']}"] = {'id' : self.id_ent, 'count' : 0}
                self.id_ent += 1

            # count, don't manage overlapping entities 
            self.entity_types[f"B-{entity['type']}"]['count'] += 1
            self.entity_types[f"I-{entity['type']}"]['count'] += end - start - 1

            # manage overlapping entities
            if sum(entity_labels[start:end]) > 0:
                # delete data
                print('Overlapping entities')
                self.deleted_data += 1
                return None
            # labels 
            entity_labels[start] = self.entity_types[f"B-{entity['type']}"]['id']
            entity_labels[start+1:end] = [self.entity_types[f"I-{entity['type']}"]['id'] for i in range(start+1,end)]
           

        doc_ = dict({
            'entities': entities,
            # encoding
            'encoding': encoding_,
            # entities
            'entity_labels': entity_labels
        })
       
        return doc_
        
    def createItem_(self,doc):  
        encoding_ = doc['encoding'].copy()
        # padding encoding
        prev_context_size = len(encoding_) 
        missing_tokens = self.max_length - prev_context_size
        pad_id = self.tokenizer.convert_tokens_to_ids(self.pad_token)
        encoding_ += [pad_id] * missing_tokens
        context_size = len(encoding_)
        
        encoding = torch.tensor(encoding_, dtype=torch.long)
        context_masks = torch.zeros(context_size, dtype=torch.bool)
        context_masks[:prev_context_size] = 1

        if self.mode == 'predict':
            return dict(encodings=encoding, context_masks=context_masks)

        # entities items
        entity_labels = doc['entity_labels'].copy()
        entity_labels += [0] * missing_tokens
        entity_labels = torch.tensor(entity_labels, dtype=torch.long)
        

        doc_ = dict(
                encodings=encoding, context_masks=context_masks,
                #entities
                entity_labels=entity_labels
            )

        return  doc_ 
    

    def getBatchDataset(self, batch_doc):
        self.max_length = max([len(doc['encoding']) for doc in batch_doc])
        current_doc = []
        for doc in batch_doc:
            current_doc.append(self.createItem_(doc))  
        dataloader = DataLoader(current_doc, batch_size=self.batch_size, shuffle=False) 
        return next(iter(dataloader))
    
   
    def preload_data(self):
        data = read_data(self.data_path)
        self.init_len = len(data)
        if self.mode == 'train':
            # init
            self.id_ent = 1

        self.data= []
        for i, obj in tqdm(enumerate(data), desc='Tokenizing data', total=len(data)):
            # tokenize
            doc_ = self.preCreateItem_(obj)
            if not doc_:
                continue
            self.data.append(doc_)

        # batch data
        self.total_data = len(self.data)
        if self.shuffle:
            random.shuffle(self.data)   
        self.dataset = []
        for i in range(0, len(self.data), self.batch_size):
            self.dataset.append(self.data[i:i+self.batch_size])

        # print
        if self.mode != 'predict':            
            print(f"{self.data_path} :")
            print('-'*200)
            print('Entities :')
            print('-'*100)
            for k,v in self.entity_types.items():
                print(f"{k} : id={v['id']}, count={v['count']}")
            print('-'*100)
            print('Total tokens :', self.total_tokens)
            print('Total unknown tokens : {} ({} %)'.format(self.total_unk_tokens, round((self.total_unk_tokens/self.total_tokens)*100,2)))
            print('Total data :', len(self.data))
            print('Deleted data : {} ({} %)'.format(self.deleted_data, round((self.deleted_data/self.init_len)*100,2)))
            print('Max length :', self.max_potenial_length)
            print('-'*200)

  