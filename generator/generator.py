import random
from faker import Faker
import string
from dataVariants import DataVariants
import pandas as pd
from geopy.geocoders import Nominatim

class Generator:
    # format
    def __init__(self):
        self.ent_types = {
            "user_name" : {'canBeNull' : False},
            "user_mail" : {'canBeNull' : False},
            "user_num" :  {'canBeNull' : False},
            "user_address" : {'canBeNull' : False},
            "user_situation" : {'canBeNull' : True},
            "revenu_mensuel" : {'canBeNull' : False},
            "depense_mensuel" : {'canBeNull' : False}, 
            "apport" : {'canBeNull' : True},
            "montant_pret" : {'canBeNull' : False}, 
            "duree_pret": {'canBeNull' : False},
            "duree_pret_year": {'canBeNull' : False},
            "logement_address" : {'canBeNull' : True}, 
            "type_logement" : {'canBeNull' : True},
          
        }
        self.fake = Faker()
        self.dataVariants = DataVariants()
        self.geolocator = Nominatim(user_agent="adresse_fr")
        self.addresses = list(pd.read_csv('generator/data/address.csv')['address'])
        
    def addBruit(self, text : str):
        for i in range(len(text)):
            text[i] = random.choice(text[i].upper(), text[i].lower())

    def getNewFormat(self, x : str):
        return random.choice([
            f"{x}",
            f"{x.upper()}",
            f"{x[0].upper()+x[1:].lower()}"
        ])

    # name
    def generateFakeName(self):
        name = self.fake.name()
        first_name, last_name = name.split(' ')[0], name.split(' ')[-1]
        first_name = self.getNewFormat(first_name)
        last_name = self.getNewFormat(last_name)
        return random.choice([
            f"{last_name} {first_name}",
            f"{first_name} {last_name}"
        ])
    
    def generate_random_sequence(self, n, spec_char=""):
        # Create a pool of characters: digits, letters (both upper and lower case), and the special character '_'
        pool = string.ascii_letters + string.digits + spec_char
        
        # Use random.choices to select n random characters from the pool
        return ''.join(random.choices(pool, k=n))
    
    # mail
    def generateFakeMail(self):
        # name
        name = self.fake.name()
        first_name, last_name = name.split(' ')[0], name.split(' ')[-1]
        first_name = random.choice([self.getNewFormat(first_name), first_name[0]])
        last_name = self.getNewFormat(last_name)
        # start
        mail = random.choice([
            f"{last_name}{first_name}",
            f"{first_name}{last_name}",
            f"{last_name}.{first_name}",
            f"{first_name}.{last_name}",
            f"{last_name}_{first_name}",
            f"{first_name}_{last_name}",
            f"{last_name}",
            f"{first_name}",         
        ])
        bruit = random.choice([True, False])
        if bruit:
            mail += self.generate_random_sequence(random.randint(1, 10), "_")
        # provider
        mail += '@'
        well_known_provider = random.choice([True, True, False])
        if well_known_provider:
            mail += random.choice([
                "gmail", "yahoo", "laposte", "outlook", "hotmail", 
                "icloud", "protonmail", "orange", "sfr", "zoho", 
                "aol", "gmx"
            ])
        else:
            mail += self.generate_random_sequence(random.randint(3, 10), ".")
        # domain
        mail += random.choice([".com", ".fr", ".net", ".org", ".co.uk", ".de", ".es"])
        return self.getNewFormat(mail)

    def generateFakePrice(self, min, max):
        n = random.randint(min, max)
        sep = random.choice([' ', '', ',', ';', '.', 'k'])
        if sep == 'k':
            milliers = n // 1000
            reste = n % 1000
            reste = str(reste) if reste != 0 else ""
            n = str(milliers) + random.choice(['k', 'K']) + reste
        elif sep != '':
            all = random.choice([True, False])
            n = f"{n:,}".replace(",", sep)
            if not all:
                index = n.find(sep)
                if n[index+1:].find(sep) != -1:
                    n = n[:index+1] + n[index+1:].replace(sep, "")
        else:
            n = str(n)
        n += random.choice(self.dataVariants.euros)
        return n
    
    # duree
    def generateFakeDuree_v0(self, max_year):
        year = str(random.randint(self.dataVariants.current_year, self.dataVariants.current_year + max_year))
        MonthF = random.choice([0, 1, 2])
        if MonthF == 0:
            bruit = random.choice(['fin ', 'début ',  "l'année ", "l'an ", '', ''])
            return self.getNewFormat(bruit + year)
        month = random.randint(1, 12)
        if MonthF == 1:
            month = str( month)
            date_ = [year, month]
            random.shuffle(date_)
            sep = random.choice([' ', ':', ' : ', ' :', ': ', '/', ' /', '/ ', ' / ', '-', '- ', ' -', ' - '])
            return date_[0] + sep + date_[1]   
        MonthF = random.choice([0, 1])
        if month == 1:
                term = 'er'
        else:
            term = 'ème'
        sep = random.choice(['', ' '])
        month2 = self.dataVariants.months[month]
        month = str(month)
        if MonthF == 0:
            month = random.choice([month + sep + term + " mois de",month + sep + term + " mois de l'année", month2])
            return self.getNewFormat(month + ' ' + year)

        month = random.choice([month + sep + term + " mois de l'année", month + sep + term + " mois", month2])  
        sep1 = random.choice(['', ' '])
        sep2 = random.choice(['', ' '])
        return self.getNewFormat(year + ' (' + sep1 + month + sep2 + ')')
      
    def generateFakeDuree_v1(self):
        a = random.randint(0, 30)
        if a == 0:
            m = random.randint(1, 11)
            year = ""
        else:
            m = random.randint(0, 11)
            year = random.choice(['ans', 'ANS', 'Années', 'année', 'Année', 'an', 'AN', 'ANNEES', 'ANNEE'])
            sep = random.choice([',', ' , ', ' ; ', ' ,', ';', ' : ', ';', ' ', ':', ' :', ': ', ' ', '', ' ', ''])
            a = str(a)
            year = random.choice([
                f"{a}{sep}{year}",
                f"{year}{sep}{a}"
            ])

        if m != 0:
            month = random.choice(['MOIS', 'mois', 'Mois'])
            sep = random.choice([',', ' , ', ' ; ', ' ,', ';', ' : ', ';', ' ', ':', ' :', ': ', ' ', '', ' ', ''])
            m = str(m) 
            month = random.choice([
                f"{m}{sep}{month}",
                f"{month}{sep}{m}"
            ])
        else:
            month = ""
        sep = random.choice([',', ' , ', ' ; ', ' ,', ';', ' et ', ';', ' ']) if year != "" and month != "" else ""
        date = [year, month]
        random.shuffle(date)
        date = date[0] + sep + date[1]
        return ''.join(date)


    # generate a fake type of job
    def generateFakeJob(self):
        job = random.choice(self.dataVariants.situation_professionnelle_options)  
        job = self.getNewFormat(job)
        return job

    # type of logement
    def generateFakeTypeLog(self):
        tlog = random.choice(self.dataVariants.type_logements)
        tlog = self.getNewFormat(tlog)
        return tlog

    # phone french one
    def generateFakeNumber(self):
        phone_number = random.choice([
            f'+33{random.randint(1,9)}',
            f'0{random.randint(1,9)}',
            f'{random.randint(1,9)}'
        ])
        for _ in range(4):
            phone_number += random.choice([' ', '']) + str(random.randint(0,9)) + str(random.randint(0,9))
        return phone_number

    def get_random_address(self):
        # Choisir une adresse au hasard parmi celles trouvées
        location = random.choice(self.addresses)
        location = location.split(',')
        location.reverse()
        keep_all = random.choice([True, False])
        if not keep_all:
            location = location[:5]
        #[...,departement, region, France métropolitaine, zipcode, France]
        can_be_null = [i for i in range(5)]
        zip_or_dep = random.choice([[1], [4], [1,4]])
        for zd in zip_or_dep:
            can_be_null.remove(zd)
        for i in range(len(location)):
            if i in can_be_null:
                location[i] = random.choice(['','', location[i]])
                if location[i] != '':
                    location[i] = self.getNewFormat(location[i])
                location[i] += random.choice([' ', ',', ';', ';', '.', '-'])
        random.shuffle(location)
        if location[0] in [' ', ',', ';', ';', '.', '-']:
            location = location[1:]
        if location[0] in [' ', ',', ';', ';', '.', '-']:
            location = location[1:]
        if location[-1] in [' ', ',', ';', ';', '.', '-']:
            location = location[:-1]
        return ''.join(location)
    
    def generate(self, ent_type):
        if self.ent_types[ent_type]['canBeNull']:
            nullOrNot = random.choice([True, False])
            if nullOrNot:
                return None
        if ent_type in ["revenu_mensuel","depense_mensuel"]:
            return self.generateFakePrice(300, 30000)
        if ent_type in  ["montant_pret", "apport"]:
            return self.generateFakePrice(15000, 3000000)
        if ent_type == "user_name":
            return self.generateFakeName()
        if ent_type == "user_mail":
            return self.generateFakeMail()
        if ent_type == "user_num":
            return self.generateFakeNumber()
        if ent_type == "user_situation":
            return self.generateFakeJob()
        if ent_type == "duree_pret_year":
            return self.generateFakeDuree_v0(max_year=30)
        if ent_type == "duree_pret":
            return self.generateFakeDuree_v1()
        if ent_type in ["user_address", "logement_address"]:
            return self.get_random_address()
        if ent_type == "type_logement":
            return self.generateFakeTypeLog()
     

    # get one object 
    def getRandomObj(self):
        types = list(self.ent_types.keys())
        types.remove(random.choice(["duree_pret","duree_pret_year"]))
        res = {}
        for k in types:
            output = self.generate(k)
            res[k] = None
            if output:
                bound = f'[{k}]'
                res[k] = bound + output + bound
            
        return res
        
