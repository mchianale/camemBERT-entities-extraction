from generator import Generator
import random
from tqdm import tqdm
import json
train_size = 10000
test_size = 5000
train_path = 'data/train.json'
test_path = 'data/test.json'   

ent_types = [
        '[user_name]',
        '[user_address]',
        '[user_mail]',
        '[user_num]',
        '[revenu_mensuel]',
        '[depense_mensuel]',
        '[montant_pret]',
        '[apport]',
        '[duree_pret]',
        '[duree_pret_year]'
        '[type_logement]',
        '[logement_address]',
        '[user_situation]',    
    ]
puncts = [',', '.', ';', ':', '%', '?', '!', '-', '$', '€', '(', ')', '"']


def update(k, v, text):
    bound = f'[{k}][{k}]'
    text = text.replace(bound, v)
    return text
class LoanRequestGenerator:
    def __init__(self):
        self.generator = Generator()


    def create_v0(self):
        obj = self.generator.getRandomObj()
        lines = []
        for k,v in obj.items():
            if v != None:
                if k not in ['revenu_mensuel', 'depense_mensuel', 'montant_pret', 'apport', 'logement_address']:
                    line = random.choice(self.generator.dataVariants.variantes_dict[k] + [''])
                else:
                    line = random.choice(self.generator.dataVariants.variantes_dict[k])
                if line != '':
                    line += random.choice([' , ', ' ; ', ' : ', ' ,' ' ;', ' :', ',', ';', ';', ' '])
                    line = self.generator.getNewFormat(line)
                line += v 
            else:
                line = ''
            lines.append(line)
        random.shuffle(lines)
        return ' '.join(lines)
    
    def create_v1(self):
        obj = self.generator.getRandomObj()

        # introduction
        person_input = []
        for k in ['user_name', 'user_mail', 'user_address', 'user_num']:
            if obj[k] != None:
                line = random.choice(self.generator.dataVariants.variantes_dict[k] + [''])
                if line != '':
                    line += random.choice([' , ', ' ; ', ' : ', ' ,' ' ;', ' :', ',', ';', ';', ' '])
                    line = self.generator.getNewFormat(line)
                line += obj[k] 
            else:
                line = ''
            person_input.append(line)
        random.shuffle(person_input)

        input = ' '.join(person_input) + ' '

        # intro salutation
        input += random.choice(self.generator.dataVariants.starts) + ' '
        start2 = random.choice(self.generator.dataVariants.salutations)
        if start2 != '':
            notUserName = self.generator.generateFakeName()
            start2 += notUserName + random.choice([' ', '', ',', ';', ':', ' : ', ': ', ' :', ' ; ']) + ' '
        input += start2 

        # pret
        if 'duree_pret' in obj:
            pret = random.choice(self.generator.dataVariants.prets)
            pret = update('duree_pret', obj['duree_pret'], pret)
        else:
            pret = random.choice(self.generator.dataVariants.pretsv2)
            pret = update('duree_pret_year', obj['duree_pret_year'], pret)
        pret = update('montant_pret', obj['montant_pret'], pret)
        pret = random.choice(['', ' ', '.', '...'])  + pret

        #  situation
        if obj['user_situation'] is not None:
            situation = random.choice(self.generator.dataVariants.variants_s1)
            situation = update('user_situation', obj['user_situation'], situation)
        else:
            situation = random.choice(self.generator.dataVariants.variants_s2)
        situation = update('revenu_mensuel', obj['revenu_mensuel'], situation)
        situation = update('depense_mensuel', obj['depense_mensuel'], situation)

        # property info
        if obj["logement_address"] is not None and obj["type_logement"] is not None:
            property_info = random.choice(self.generator.dataVariants.variants_p1)
            property_info = update("logement_address", obj["logement_address"], property_info)
            property_info = update("type_logement", obj["type_logement"], property_info)
        elif obj["type_logement"] is not None:
            property_info = random.choice(self.generator.dataVariants.variants_p2)
            property_info = update("type_logement", obj["type_logement"], property_info)
        elif obj["logement_address"] is not None:
            property_info = random.choice(self.generator.dataVariants.variants_p3)
            property_info = update("logement_address", obj["logement_address"], property_info)
        else:
            property_info = random.choice(self.generator.dataVariants.variants_p4)
        property_info = random.choice(['', ' ', '.', '...']) + property_info

        # end
        end = random.choice(['', ' ', '.', '...']) + random.choice(self.generator.dataVariants.remerciements) + random.choice(['', obj['user_name']])
        l =  [pret, situation, property_info]
        random.shuffle(l)
        input += ''.join(l) + end
        return input




def cleanEnt(text):
    tokens = []
    current_words = ''
    for i in range(len(text)):
        if text[i] == ' ':
            if current_words:
                tokens.append(current_words)
            current_words = ''
        elif text[i] in puncts:
            if current_words:
                tokens.append(current_words)
            tokens.append(text[i])
            current_words = ''
        else:
            current_words += text[i]
    if current_words != '':
        tokens.append(current_words)
    return tokens

def preTokenize(text):
    tokens = []
    entities = []
    current_words = ''
    i = 0
    
    while i < len(text):
        if text[i] == '[':  # Detect start of entity
            # Add the current word to tokens
            if current_words:
                tokens.append(current_words)
                current_words = ''
            
            # Extract the entity type
            end_idx = text.find(']', i)
            if end_idx == -1:
                raise ValueError("Entity tag not closed")
            entity_type = text[i:end_idx + 1]  # [entity_name]
            entity_name = entity_type.replace('[', '').replace(']', '')
            
            # Look for the end of the entity in text
            entity_end_idx = text.find(entity_type, end_idx + 1)
            if entity_end_idx == -1:
                raise ValueError(f"Entity {entity_type} not closed")
            
            # Extract the entity's text content
            entity_text = text[end_idx + 1:entity_end_idx].strip()
            entity_tokens = cleanEnt(entity_text)
            
            # Add entity metadata
            entities.append({
                'id': len(entities),
                'start': len(tokens),
                'end': len(tokens) + len(entity_tokens),
                'type': entity_name,
                'tokens': entity_tokens
            })
            
            # Add tokens and update index
            tokens += entity_tokens
            i = entity_end_idx + len(entity_type)  # Skip past the closing entity marker
            continue
        elif text[i] == ' ':
            if current_words:
                tokens.append(current_words)
            current_words = ''
        elif text[i] in puncts:
            if current_words:
                tokens.append(current_words)
            tokens.append(text[i])
            current_words = ''
        else:
            current_words += text[i]
        i += 1

    # Append the last word if exists
    if current_words:
        tokens.append(current_words)
    
    for ent in entities:
        assert(tokens[ent['start']:ent['end']] == ent['tokens'])
    return {
        'tokens': tokens,
        'entities': entities
    }

def generateData(data_size, path, dataCreator):
    print(f'generate data {path}...')
    with open(path, 'w', encoding='utf-8') as json_file:
        json_file.write('[\n')
        id = 0
        for i in tqdm(range(data_size)):
            case_ = random.choice([0, 1, 1, 1])
            if case_ == 0:
                txt = dataCreator.create_v0()
            else:
                txt = dataCreator.create_v1()
            
            output = preTokenize(txt)
            output['id'] = id
            output['text'] = txt
            json.dump(output, json_file)
            # Write a newline after each JSON object
            if i == data_size-1:
                json_file.write('\n')
            else:
                json_file.write(',\n')    
            id += 1
        json_file.write(']')


if __name__ == '__main__':
    dataCreator = LoanRequestGenerator()
    generateData(train_size, train_path, dataCreator)
    generateData(test_size, test_path, dataCreator)
  