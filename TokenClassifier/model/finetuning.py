from transformers import CamembertTokenizer, CamembertConfig, CamembertModel
from tqdm import tqdm 
import torch
import transformers
import os

from model.data_processing import DataProcessor
from model.CamForTokenClassification import CamembertForTokenClassification
from model.loss import TokenClassifierLoss, get_optimizer_params
from model.manager import update_config, plot_loss, read_config, getResultPaths, save_predictions, getPredictionPath
from model.predictions import getPredictions_batch

from gold_metrics import evaluation_metrics


class TokenClassifier:
    def __init__(self, config, mode):
        self.mode = mode
        self.model_name = config['model']
        # common information
        self.input_max_length = config['max_length']
        self.batch_size = config['batch_size']
        if mode == 'train':
            self.config = config
            # informations
            self.train_path = config['train_path']
            self.save_path = config['save_path']
            self.shuffle = config['shuffle']
            
            # encoding information
            tokenizer_path = self.model_name
            self.lowercase = config['lowercase']
           
            # training information
            self.epochs = config['epochs']

            # model information
            self.prop_drop = config['prop_drop']
            self.freeze_transformer = config['freeze_transformer']

            # optimizer information
            self.weight_decay = config['weight_decay']
            self.lr = config['learning_rate']
            self.new_lr = config['new_learning_rate']
            self.lr_warmup = config['lr_warmup']
            self.max_grad_norm = config['max_grad_norm']
 
            # validation information
            self.valid_path = None
            if 'valid_path' in config:
                self.valid_path = config['valid_path']
                self.valid_batch_size = config['valid_batch_size']
        else:
            self.save_path = self.model_name
            self.predict_path = config['predict_path']
            # retrieve informations from the model
            train_config = read_config(os.path.join(self.model_name, 'config.json'))
            # encoding information
            tokenizer_path = train_config['_name_or_path']
            self.lowercase = train_config['lowercase']   
            # model information
            self.freeze_transformer = train_config['freeze_transformer']
            self.prop_drop = train_config['prop_drop']

            self.entity_types = train_config['entity_types']
            self.reverse_entity_types = {value: key for key, value in self.entity_types.items()} 

            # eval information
            if self.mode == 'eval':
                self.threshold = config['threshold']
            else:
                self.results_path = config['results_path']

        self.tokenizer = CamembertTokenizer.from_pretrained(tokenizer_path, do_lower_case=self.lowercase) 
        # device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_data(self):
        if self.mode == 'train':
            # train dataset
            self.data_train_processor = DataProcessor(
                tokenizer=self.tokenizer,
                data_path=self.train_path,
                input_max_length=self.input_max_length,
                batch_size=self.batch_size,
                shuffle=self.shuffle,
                mode=self.mode
            )
             
            self.data_train_processor.preload_data()
            self.train_data = self.data_train_processor.dataset

            # retrieve information
            self.entity_types = self.data_train_processor.entity_types
            self.entity_types = {key: value['id'] for key, value in self.entity_types.items()}
            total_data = self.data_train_processor.total_data  
            updates_epoch = total_data // self.batch_size
            self.updates_total = updates_epoch * self.epochs

            # validation dataset
            if self.valid_path:
                self.data_valid_processor = DataProcessor(
                    tokenizer=self.tokenizer,
                    data_path=self.valid_path,
                    input_max_length=self.input_max_length,
                    batch_size=self.valid_batch_size,
                    entity_types=self.entity_types,
                    mode='valid'
                )
                self.data_valid_processor.preload_data()
                self.valid_data = self.data_valid_processor.dataset
        else:
            self.data_predict_processor = DataProcessor(
                tokenizer=self.tokenizer,
                data_path=self.predict_path,     
                input_max_length=self.input_max_length,
                batch_size=self.batch_size,
                entity_types=self.entity_types,
                mode='predict'
            )
            self.data_predict_processor.preload_data()
            self.predict_data = self.data_predict_processor.dataset
  
    def load_model(self):
        config = CamembertConfig.from_pretrained(self.model_name)
        

        self.model = CamembertForTokenClassification.from_pretrained(
                self.model_name,
                config=config,
                prop_drop=self.prop_drop,
                freeze_transformer=self.freeze_transformer,
                # entity information
                entity_types=len(self.entity_types)+1
            )
        
        if self.mode == 'train':
            state_dict = CamembertModel.from_pretrained(self.model_name).state_dict()
            self.model.bert.load_state_dict(state_dict)
    
        self.model.to(self.device)
        if self.mode == 'train':
            print('-' * 50)
            print('Model :')
            print(self.model)
            print('-' * 50)

            # create optimizer
            self.optimizer = get_optimizer_params(self.model,self.lr,self.new_lr, self.weight_decay)
            # create scheduler
            scheduler = transformers.get_linear_schedule_with_warmup(self.optimizer,
                                                                    num_warmup_steps=self.lr_warmup * self.updates_total,
                                                                    num_training_steps=self.updates_total)
            entity_criterion = torch.nn.CrossEntropyLoss(reduction='none')
            self.compute_loss = TokenClassifierLoss(entity_criterion=entity_criterion, 
                                                    model=self.model, optimizer=self.optimizer, 
                                                    scheduler=scheduler, max_grad_norm=self.max_grad_norm)
            

    def train(self):
        tr_loss = [0] * self.epochs
        if self.valid_path:
            val_loss = [0] * self.epochs
        
        for epoch in range(self.epochs):
            self.model.zero_grad()
            for batch_ in tqdm(self.train_data, desc="Training"):       
                self.model.train()    
                batch_loss = self.compute_batch(batch_)  
                tr_loss[epoch] += batch_loss['loss']
             
            # validation
            if self.valid_path:
                self.model.eval()
                with torch.no_grad():
                    for batch_ in tqdm(self.valid_data, desc="Validation"):
                        batch_loss = self.compute_batch(batch_, backward=False)
                        val_loss[epoch] += batch_loss['loss']

            print(f"Epoch {epoch + 1}/{self.epochs} - Loss: {tr_loss[epoch]}")
            if self.valid_path:
                print(f"Validation Loss: {val_loss[epoch]}")
        
        # save model
        self.save_model()   
        # loss
        plot_loss({'loss': tr_loss}, self.save_path, 'train')
        if self.valid_path:
            plot_loss({'loss': val_loss}, self.save_path, 'valid')

    def compute_batch(self, batch_, backward=True):
        batch = self.data_train_processor.getBatchDataset(batch_)
        entity_logits = self.model(encodings=batch['encodings'],context_masks=batch['context_masks'])
        # compute loss and optimize parameters
        batch_loss = self.compute_loss.compute(
                                        entity_logits=entity_logits,
                                        entity_masks=batch['context_masks'],
                                        entity_types=batch['entity_labels'],
                                        backward=backward
        )
        return batch_loss
    


    def predict(self):
        self.predictions = []
        with torch.no_grad():
            self.model.eval()
            for batch_ in tqdm(self.predict_data, desc='Predictions'):
                batch = self.data_predict_processor.getBatchDataset(batch_)
                input_tokens = [batch_[i]['input_tokens'] for i in range(len(batch_))]
                
                pred_entities =  self.model(
                    encodings=batch['encodings'], 
                    context_masks=batch['context_masks'],
                    input_tokens=input_tokens,
                    entity_types=self.reverse_entity_types,
                    inference=True
                )
                self.predictions += getPredictions_batch(batch_, pred_entities)
                
        if self.mode == 'eval': # save pred in the model folder
            self.results_path, self.prediction_path = getResultPaths(self.save_path, self.predict_path, self.threshold)  
        else:
            self.prediction_path = getPredictionPath(self.results_path, self.predict_path)

        save_predictions(self.predictions, self.prediction_path)
        print('Predictions saved in ', self.prediction_path)
     
    def eval(self):
        self.predict()
        ent_types = [ent_type[2:] for ent_type in self.entity_types]
        print('Evaluation :')
        evaluation_metrics(data=self.predictions, ent_types=ent_types, 
                           threshold=self.threshold, output_path=self.results_path)
        print('Metrics saved in ', self.results_path)
   

    def save_model(self):
        self.model.save_pretrained(self.save_path)
        self.config['entity_types'] = self.entity_types
        update_config(self.save_path, self.config)
        print('Model saved in ', self.save_path)