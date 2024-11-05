from datetime import datetime
import pandas as pd
import random
class DataVariants:
    def __init__(self):
        self.situation_professionnelle_options = [
            "CDI",                          # Contrat à Durée Indéterminée
            "CDD",                          # Contrat à Durée Déterminée
            "sans emploi",                  # Sans emploi
            "chômage",                      # En chômage
            "travailleur indépendant",      # Travailleur indépendant
            "entrepreneur",                 # Entrepreneur
            "freelance",                    # Freelance
            "étudiant",                     # Étudiant
            "retraité",                     # Retraité
            "fonctionnaire",                # Fonctionnaire
            "auto-entrepreneur",            # Auto-entrepreneur
            "stagiaire",                    # Stagiaire
            "intérimaire",                  # Intérimaire
            "contrat d'apprentissage",      # Contrat d'apprentissage
            "bénévole",                     # Bénévole
            "congé parental",               # Congé parental
            "à temps partiel",              # À temps partiel
            "vacataire",                    # Vacataire
            "travail temporaire",           # Travail temporaire
            "saisonnier",                   # Saisonnier
            "mission de service civique",   # Service civique
            "emploi précaire",              # Emploi précaire
            "recherche d'emploi"            # En recherche d'emploi
        ]

        self.synonymes_montant = [
            "Ma demande de prêt s'élève à", 
            "Le montant de mon emprunt est de", 
            "Je sollicite un prêt de", 
            "Je fais une demande de prêt d'un montant de", 
            "La somme que je souhaite emprunter est de", 
            "Je souhaite emprunter", 
            "Je demande un crédit de", 
            "Je demande un prêt de", 
            "Le montant que je demande est de", 
            "Mon emprunt est de", 
            "Mon prêt est de", 
            "J'ai besoin d'un financement de", 
            "J'aimerais emprunter",
            "Je souhaite obtenir", 
            "Je voudrais obtenir", 
            "Je demande", 
            "Je sollicite un prêt de", 
            "Je souhaite un financement de", 
            "Je demande un emprunt de", 
            "Je fais une demande de prêt de", 
            "Mon objectif est de recevoir", 
            "Je prévois de contracter un emprunt de", 
            "Je vise un prêt de", 
            "Je compte demander", 
            "Je souhaite souscrire un prêt de",
            "Je fais une demande pour obtenir un prêt de", 
            "Le prêt dont j'ai besoin est de", 
            "Je fais une requête pour un emprunt de", 
            "Je voudrais bénéficier d'un prêt de", 
            "J'ai l'intention d'emprunter", 
            "Je me tourne vers vous pour un crédit de", 
            "Le crédit souhaité est de", 
            "Mon projet nécessite un prêt de", 
            "Je prévois de demander un crédit de", 
            "Je sollicite un montant de", 
            "La somme que je désire emprunter est de", 
            "Je vise à obtenir un emprunt de", 
            "Je formule une demande pour un prêt de", 
            "J'ai besoin d'un montant de", 
            "Je formule une requête pour un crédit de", 
            "Je cherche à obtenir un financement de", 
            "Je souhaite demander un emprunt de", 
            "Je désire obtenir un crédit de"
        ]

        self.synonymes_duree = [
            "que je souhaite rembourser sur", 
            "que je prévois de rembourser sur", 
            "que je voudrais rembourser sur", 
            "remboursable en", 
            "sur une période de", 
            "étalé sur", 
            "que je rembourserai sur", 
            "remboursable sur", 
            "que je compte rembourser en", 
            "sur une durée de", 
            "remboursable sur une durée de", 
            "étalé sur une période de", 
            "réparti sur",
            "que je pense rembourser sur", 
            "étalé sur une période de", 
            "que je rembourserai en", 
            "réglé sur", 
            "à rembourser sur", 
            "que je vais rembourser sur", 
            "que je compte étaler sur", 
            "avec un remboursement prévu sur", 
            "étalé dans le temps sur", 
            "prévu pour être remboursé en", 
            "que je vais étaler sur", 
            "planifié sur une période de", 
            "remboursable dans un délai de", 
            "sur une durée totale de", 
            "réparti dans le temps sur", 
            "sur une durée étalée de", 
            "à rembourser en", 
            "remboursable sur une période de", 
            "distribué sur", 
            "que je compte rembourser d'ici", 
            "que je souhaite régler sur", 
            "prévu sur", 
            "que j'envisage de rembourser en", 
            "étalé sur une durée de", 
            "distribué sur une période de", 
            "à étaler sur", 
            "que je vais rembourser d'ici"
        ]

        self.intro_situation = [
            "Concernant ma situation professionnelle,", 
            "Sur le plan professionnel,", 
            "Du point de vue de ma situation actuelle,", 
            "En ce qui concerne ma profession,", 
            "Professionnellement,", 
            "Pour ma part,",
            "Actuellement,",
            "À l'heure actuelle,",
            "En ce qui concerne mon emploi,", 
            "Au niveau professionnel,", 
            "Par rapport à ma situation actuelle,", 
            "En ce moment,", 
            "Quant à ma profession,", 
            "À propos de ma situation professionnelle,", 
            "Pour ce qui est de mon emploi,", 
            "Du point de vue professionnel,", 
            "Du côté de ma profession,", 
            "Quant à ma situation au travail,", 
            "Concernant mon emploi actuel,", 
            "En ce qui a trait à ma situation professionnelle,", 
            "Du côté de mon activité professionnelle,", 
            "Sur le plan de mon emploi,", 
            "En ce qui concerne mon travail,", 
            "Quant à ma situation professionnelle actuelle,", 
            "En termes d'emploi,", 
            "Du point de vue de mon emploi actuel,", 
            "Pour ce qui concerne ma profession,", 
            "Pour ce qui est de ma situation actuelle,", 
            "Du côté de mon travail,", 
            "À propos de ma profession actuelle,", 
            "Quant à mon activité professionnelle,", 
            "Au sujet de ma profession actuelle,", 
            "En ce qui me concerne au niveau professionnel,", 
            "Par rapport à mon emploi actuel,", 
            "Du côté de mon emploi actuel,", 
            "Du point de vue de mon activité professionnelle,", 
            "Quant à mon statut professionnel,", 
            "En ce qui me concerne professionnellement,"
        ]

        self.synonymes_revenu = [
            "mon salaire mensuel est de", 
            "mon revenu mensuel est de", 
            "je perçois un revenu de", 
            "je touche un salaire de", 
            "je gagne un salaire de", 
            "mes revenus s'élèvent à", 
            "je reçois un revenu mensuel de", 
            "mon salaire est de", 
            "je perçois un salaire de",
            "mon revenu est de", 
            "je gagne chaque mois", 
            "mes revenus mensuels sont de", 
            "je reçois mensuellement", 
            "mes gains mensuels sont de", 
            "je touche un revenu mensuel de", 
            "je bénéficie d'un revenu de", 
            "mon salaire brut est de", 
            "mes ressources mensuelles s'élèvent à", 
            "je touche chaque mois un salaire de", 
            "je reçois mensuellement un salaire de", 
            "je perçois mensuellement", 
            "je touche une rémunération mensuelle de", 
            "ma rémunération mensuelle est de", 
            "je gagne un montant mensuel de", 
            "mes entrées d'argent mensuelles s'élèvent à", 
            "mes revenus perçus sont de", 
            "mes entrées financières mensuelles sont de", 
            "je gagne par mois", 
            "je touche chaque mois une somme de", 
            "mes ressources financières s'élèvent à", 
            "mon revenu net mensuel est de", 
            "mes rentrées mensuelles sont de", 
            "je dispose chaque mois d'un revenu de", 
            "mon revenu brut mensuel s'élève à", 
            "je dispose de", 
            "mon revenu total mensuel est de", 
            "je perçois un montant mensuel de", 
            "mes gains mensuels s'élèvent à", 
            "je touche un montant de"
        ]

        self.synonymes_depense = [
            "mes dépenses mensuelles s'élèvent à", 
            "je dépense en moyenne", 
            "mes charges mensuelles sont de", 
            "mes dépenses sont de", 
            "mes frais mensuels sont de", 
            "je consacre environ", 
            "mes dépenses totalisent", 
            "j'ai des dépenses mensuelles de",
            "mes coûts mensuels sont de", 
            "je dépense chaque mois", 
            "je dois payer mensuellement", 
            "mes frais chaque mois sont de", 
            "je dépense chaque mois environ", 
            "mes charges s'élèvent à", 
            "mes frais s'élèvent à", 
            "les dépenses mensuelles que j'ai sont de", 
            "mon budget mensuel est de", 
            "mes coûts sont de", 
            "je paie chaque mois", 
            "je dois payer chaque mois environ", 
            "les frais que j'ai chaque mois sont de", 
            "les charges que j'ai mensuellement sont de", 
            "mes dépenses se chiffrent à", 
            "je débourse chaque mois", 
            "je verse chaque mois", 
            "mes sorties d'argent sont de", 
            "mes paiements mensuels sont de", 
            "je consacre chaque mois", 
            "les frais que je paie mensuellement sont de", 
            "les dépenses que je fais chaque mois sont de", 
            "les charges mensuelles que je paie sont de", 
            "les frais que j'ai chaque mois sont de", 
            "les dépenses mensuelles que je dois payer sont de", 
            "je débourse mensuellement", 
            "je dépense environ", 
            "les charges mensuelles que j'ai à payer sont de", 
            "je paie chaque mois une somme de", 
            "je paie environ chaque mois"
        ]

        self.intro_property = [
            "Je souhaite acquérir", 
            "Je prévois d'acheter", 
            "Mon objectif est d'acquérir", 
            "Je suis intéressé(e) par l'achat", 
            "Mon projet concerne l'achat", 
            "Je désire devenir propriétaire de", 
            "Je cherche à acheter", 
            "Je souhaiterais devenir propriétaire de",
            "Je souhaite devenir propriétaire de", 
            "Je projette d'acquérir", 
            "Je veux acheter", 
            "Je vise l'achat de", 
            "Mon intention est d'acquérir", 
            "Mon projet est d'acheter", 
            "Je planifie l'achat de", 
            "Je compte acheter", 
            "Je souhaite investir dans", 
            "Je me projette dans l'achat de", 
            "Je cherche à devenir propriétaire de", 
            "Je prévois un investissement pour acheter", 
            "Je souhaite réaliser l'acquisition de", 
            "Je suis sur le point d'acheter", 
            "Je souhaite finaliser l'achat de", 
            "Mon ambition est de devenir propriétaire de", 
            "Mon objectif est d'investir dans", 
            "Mon intention est d'acheter", 
            "Je voudrais acheter", 
            "Je suis intéressé(e) par l'acquisition de", 
            "Je projette de devenir propriétaire de", 
            "Mon projet est d'acquérir", 
            "Je désire acquérir", 
            "Mon but est de devenir propriétaire de", 
            "Je suis à la recherche de", 
            "Je suis en train de planifier l'achat de", 
            "Mon plan est d'acheter", 
            "Mon objectif est de finaliser l'acquisition de", 
            "Je cherche à investir dans l'achat de", 
            "Je suis en train d'acquérir", 
            "Je souhaite faire l'acquisition de", 
            "Je désire acheter", 
            "Je voudrais investir dans"
        ]

        self.adresse_variants = [
            "situé à", 
            "qui se trouve à", 
            "localisé à", 
            "dans la commune de", 
            "à l'adresse suivante", 
            "au sein de", 
            "dans le quartier de", 
            "en plein cœur de", 
            "proche de", 
            "dans la ville de", 
            "dans la région de",
            "situé dans", 
            "établi à", 
            "implanté à", 
            "au cœur de", 
            "dans le secteur de", 
            "au centre de", 
            "dans les environs de", 
            "non loin de", 
            "à proximité de", 
            "en banlieue de", 
            "dans la zone de", 
            "au nord de", 
            "au sud de", 
            "dans le centre de", 
            "proche du centre-ville de", 
            "dans les alentours de", 
            "à quelques minutes de", 
            "à distance de marche de", 
            "à côté de", 
            "non loin des commodités de", 
            "dans la localité de", 
            "à proximité immédiate de", 
            "en bordure de", 
            "dans les abords de", 
            "dans un secteur calme de", 
            "en périphérie de", 
            "non loin du centre-ville de", 
            "à quelques kilomètres de", 
            "à quelques pas de", 
            "à proximité des commerces de", 
            "près de", 
            "non loin des écoles de", 
            "dans un quartier résidentiel de", 
            "au sud-ouest de", 
            "dans les environs immédiats de", 
            "dans un secteur recherché de", 
            "dans une zone privilégiée de", 
            "à la limite de", 
            "dans le voisinage de"
        ]


        self.description_variants = [
            "spacieux", 
            "lumineux", 
            "avec jardin", 
            "avec terrasse", 
            "situé dans un quartier résidentiel calme", 
            "idéalement situé", 
            "rénové récemment", 
            "dans un environnement paisible", 
            "avec une belle vue", 
            "proche des commodités", 
            "à proximité des écoles", 
            "avec un garage", 
            "avec des finitions modernes",
            "avec un balcon", 
            "doté d'une grande pièce de vie", 
            "avec de beaux volumes", 
            "proche des transports", 
            "avec un parking privé", 
            "avec une piscine", 
            "proche des commerces", 
            "avec de vastes espaces", 
            "récemment rénové", 
            "dans un cadre verdoyant", 
            "avec un espace extérieur", 
            "entièrement refait à neuf", 
            "dans un secteur prisé", 
            "au calme", 
            "offrant une vue dégagée", 
            "avec une cuisine moderne", 
            "à deux pas des commodités", 
            "avec un double séjour", 
            "avec une grande terrasse", 
            "avec une orientation sud", 
            "avec des espaces lumineux", 
            "proche des écoles et commerces", 
            "avec un grand jardin", 
            "proche du centre-ville", 
            "avec des équipements de qualité", 
            "avec une grande salle de bains", 
            "avec des prestations haut de gamme", 
            "avec un chauffage moderne", 
            "dans un secteur résidentiel", 
            "dans un immeuble sécurisé", 
            "à proximité immédiate des transports", 
            "avec un accès facile aux autoroutes", 
            "avec des matériaux de qualité", 
            "avec un toit-terrasse", 
            "avec de larges baies vitrées", 
            "avec une cave", 
            "avec des chambres spacieuses"
        ]

        self.variantes_dict = {
            'user_name': [
                'nom du client', 'nom client', 'nom complet', 'nom', 'client', 'nom prénom', 'prénom et nom', 'identité'
            ],
            'user_mail': [
                "mail du client", 'email client', 'adresse email', 'courriel', 'mail', 'email personnel', 'adresse électronique'
            ],
            'user_num': [
                "Numéro de Téléphone", 'téléphone', 'numéro de tel', 'tel', 'numéro', 'contact téléphonique', 'téléphone portable', 'mobile', 'fixe'
            ],
            'user_address': [
                'adresse du client', 'adresse complète', 'adresse client', 'rue', 'lieu de résidence', 'domicile', 'adresse postale'
            ],
            'user_situation': [
                'situation', 'statut professionnel', 'emploi', 'situation actuelle', 'travail', 'contrat de travail', 'situation pro', 'profession', 'statut emploi', 'situation d\'emploi', 'poste actuel', 'type de contrat', 'activité professionnelle'
            ],
            'revenu_mensuel': [
                'Revenu Mensuel', 'salaire', 'revenus', 'revenus mensuels', 'revenu net', 'salaire mensuel', 'revenu', 'gains mensuels', 'revenus actuels'
            ],
            'depense_mensuel': [
                'Dépense Mensuelle', 'charges mensuelles', 'dépenses', 'dépenses actuelles', 'coût mensuel', 'frais mensuels', 'sorties mensuelles'
            ],
            'apport': [
                'apport personnel', 'apport financier', 'contribution personnelle', 'fonds propres', 'somme apportée', 'investissement personnel', 'apport pour achat immobilier'
            ],
            'montant_pret': [
                'Montant du Prêt', 'prêt demandé', 'montant du prêt', 'somme demandée', 'total du prêt', 'montant de l\'emprunt', 'valeur du prêt'
            ],
            'duree_pret': [
                'Durée du Prêt', 'durée de l\'emprunt', 'période du prêt', 'temps du prêt', 'délai du prêt', 'durée totale du prêt'
            ],
            'duree_pret_year': [
                'Durée du Prêt', 'durée de l\'emprunt', 'période du prêt', 'temps du prêt', 'délai du prêt', 'durée totale du prêt'
            ],
            'logement_address': [
                'Adresse du Logement', 'adresse de la propriété', 'adresse bien immobilier', 'adresse de la maison', 'lieu de la propriété', 'adresse logement', 'lieu du bien'
            ],
            'type_logement': [
                'Type de Logement', 'type de bien', 'nature de la propriété', 'catégorie de bien', 'genre de logement', 'propriété'
            ]
        }


        self.euros = [
            '',
            ' Eur',
            'Eur',
            ' euros', 
            ' Euros', 
            ' EUROS', 
            ' eur', 
            ' EUR', 
            ' euro',
            ' EURO', 
            ' Euro',
            ' €',
            'euros', 
            'Euros', 
            'EUROS', 
            'eur', 
            'EUR', 
            'euro',
            'EURO', 
            'Euro',
            '€'
        ]

        self.type_logements = ['villa', 'résidence', 'pavillon', 'duplex', 'terrain'
                        'studio', 'appartement', 'propriété', 
                        'maison', 'hôtel', 'hôtel particulier', 'auberge',
                        'caravane', 'studio', 'loft', 'manoir', 'logement']+[ 'T' + str(i) for i in range(0, 20)]

        self.current_year =  datetime.now().date().year
        self.months = {
            1: 'Janvier',
            2: 'Fevrier',
            3: 'Mars',
            4: 'Avril',
            5: 'Mai',
            6: 'Juin',
            7: 'Juillet',
            8: 'Août',
            9: 'Septembre',
            10: 'Octobre',
            11: 'Novembre',
            12: 'Decembre'
        }

        self.starts = list(pd.read_csv('generator/data/start.csv')['0'])
        self.salutations = [
                '', 
                "Monsieur, Madame ",
                "Monsieur, Madame ",
                "Monsieur ",
                "Bonjour, monsieur ",
                "Madame ",
                "Bonjour Madame ",
                "Chère Madame ",
                "Chère Monsieur ",
                "Cher ",
                "Bonjour ",
                "Salut ",
                "Cher Monsieur, Madame ",
                "Cher Monsieur ",
                "Salutations ",
                "Mes salutations ",
                "Bonjour Monsieur, Madame ",
                "Bonjour cher(e) ",
                "Bonsoir ",
                "Bonsoir Monsieur ",
                "Bonsoir Madame ",
                "Salut Monsieur ",
                "Salut Madame ",
                "Hey ",
                "Hello ",
                "Bonjour à vous ",
                "Chers amis ",
                "Cher(e) ",
                "Salut à toi ",
                "À l'attention de Monsieur, Madame ",
                "À l'attention de ",
                "Respecté(e) ",
                "Cordialement ",
                "En réponse à votre demande, ",
                "Bonjour cher ",
                "Bonjour chère ",
                "À vous, ",
                "Chère Madame, Cher Monsieur ",
                "Très cher ",
                "Bonjour à tous ",
                "Mes salutations distinguées "
        ]


        self.prets = [
            "Ma demande de prêt s'élève à [montant_pret][montant_pret] que je souhaiterais payer sur [duree_pret][duree_pret]",
            "Je souhaiterais obtenir au minimum [montant_pret][montant_pret] sur [duree_pret][duree_pret]",
            "Je peux rembourser ma demande sur [duree_pret][duree_pret]. Le montant demandé étant de [montant_pret][montant_pret]"
        ]

        # Générer 150 variantes en combinant les synonymes
        for _ in range(150):
            montant = random.choice(self.synonymes_montant)
            duree = random.choice(self.synonymes_duree)
            
            phrase = f"{montant} [montant_pret][montant_pret] {duree} [duree_pret][duree_pret]."
            self.prets.append(phrase)

        # Ajout de quelques exemples supplémentaires pour enrichir
        self.prets += [
            "Je sollicite un crédit de [montant_pret][montant_pret] avec une durée de remboursement de [duree_pret][duree_pret].",
            "Le montant de mon emprunt est de [montant_pret][montant_pret], remboursable sur [duree_pret][duree_pret].",
            "Je souhaite emprunter [montant_pret][montant_pret] que je rembourserai sur une période de [duree_pret][duree_pret].",
            "Je souhaite obtenir un crédit de [montant_pret][montant_pret], à rembourser sur une durée de [duree_pret][duree_pret].",
            "Le prêt que je sollicite est de [montant_pret][montant_pret] et sera remboursé sur [duree_pret][duree_pret].",
            "Je souhaite souscrire à un prêt de [montant_pret][montant_pret] remboursable sur [duree_pret][duree_pret].",
            "Je demande un crédit de [montant_pret][montant_pret] que je compte rembourser sur [duree_pret][duree_pret].",
            "Le financement demandé est de [montant_pret][montant_pret] avec une période de remboursement de [duree_pret][duree_pret].",
            "Je vise un prêt de [montant_pret][montant_pret] remboursable en [duree_pret][duree_pret].",
            "Mon objectif est d'obtenir un crédit de [montant_pret][montant_pret] que je rembourserai sur [duree_pret][duree_pret]."
        ]

        self.synonymes_duree_year = [
            "que je souhaite rembourser d'ici", 
            "que je prévois de rembourser avant", 
            "remboursable jusqu'à", 
            "que je rembourserai d'ici", 
            "à rembourser avant", 
            "dont le remboursement est prévu jusqu'à", 
            "que je compte régler avant", 
            "que je vais rembourser avant", 
            "remboursable d'ici", 
            "à solder avant", 
            "avec une date de remboursement prévue pour", 
            "dont le dernier paiement sera avant", 
            "réglable jusqu'à", 
            "à finaliser avant", 
            "que je souhaite solder d'ici", 
            "dont l'échéance est prévue pour", 
            "remboursable jusqu'à la date de", 
            "à régler avant la fin de", 
            "dont le solde est prévu pour", 
            "que je compte solder d'ici", 
            "dont la fin de remboursement est prévue pour", 
            "à rembourser jusqu'à la date de", 
            "remboursable jusqu'en", 
            "dont le remboursement se termine en", 
            "à régler d'ici", 
            "planifié pour être remboursé avant", 
            "à solder d'ici", 
            "dont la dernière échéance est prévue pour", 
            "qui doit être remboursé avant", 
            "que je vais solder avant", 
            "qui sera soldé d'ici", 
            "avec une fin de remboursement en", 
            "réglé au plus tard en", 
            "dont l'échéance finale est en", 
            "dont je prévois de finir le remboursement en", 
            "prévu pour être soldé d'ici", 
            "que je vais rembourser d'ici la fin de", 
            "avec une échéance finale avant", 
            "dont le paiement final est prévu pour"
        ]
        self.pretsv2 = [
            "Ma demande de prêt s'élève à [montant_pret][montant_pret], que je souhaite rembourser d'ici [duree_pret_year][duree_pret_year].",
            "Je souhaiterais obtenir un prêt de [montant_pret][montant_pret] à rembourser jusqu'à [duree_pret_year][duree_pret_year].",
            "Je peux rembourser ma demande d'ici [duree_pret_year][duree_pret_year]. Le montant demandé est de [montant_pret][montant_pret]."
        ]

        # Générer 150 variantes en combinant les synonymes pour montant et duree_pret_year
        for _ in range(150):
            montant = random.choice(self.synonymes_montant)
            duree_year = random.choice(self.synonymes_duree_year)
            
            # Phrase combinant montant et la date de fin de prêt
            phrase = f"{montant} [montant_pret][montant_pret] {duree_year} [duree_pret_year][duree_pret_year]."
            self.pretsv2.append(phrase)

        # Ajout de quelques exemples supplémentaires pour enrichir
        self.pretsv2 += [
            "Je sollicite un crédit de [montant_pret][montant_pret] à rembourser d'ici [duree_pret_year][duree_pret_year].",
            "Le montant de mon emprunt est de [montant_pret][montant_pret], et je le rembourserai jusqu'à [duree_pret_year][duree_pret_year].",
            "Je souhaite emprunter [montant_pret][montant_pret], remboursable jusqu'en [duree_pret_year][duree_pret_year].",
            "Je demande un crédit de [montant_pret][montant_pret], à rembourser avant [duree_pret_year][duree_pret_year].",
            "Le prêt demandé s'élève à [montant_pret][montant_pret], que je rembourserai jusqu'en [duree_pret_year][duree_pret_year].",
            "Je compte obtenir un prêt de [montant_pret][montant_pret], à rembourser avant [duree_pret_year][duree_pret_year].",
            "Le montant du crédit que je demande est de [montant_pret][montant_pret], et je le rembourserai d'ici [duree_pret_year][duree_pret_year].",
            "Mon objectif est de souscrire un crédit de [montant_pret][montant_pret], remboursable avant [duree_pret_year][duree_pret_year]."
        ]


        self.situations_emplois = [
            "je suis actuellement en [user_situation][user_situation]",
            "je travaille en tant que [user_situation][user_situation]",
            "je suis employé(e) en [user_situation][user_situation]",
            "j'ai un [user_situation][user_situation] actuellement",
            "je suis actuellement [user_situation][user_situation]",
            "je travaille comme [user_situation][user_situation]",
            "mon statut est [user_situation][user_situation]",
            "j'occupe la fonction de [user_situation][user_situation]",
            "je suis engagé(e) en tant que [user_situation][user_situation]",
            "j'exerce actuellement comme [user_situation][user_situation]",
            "ma situation actuelle est [user_situation][user_situation]",
            "mon emploi actuel est [user_situation][user_situation]",
            "je suis en poste comme [user_situation][user_situation]",
            "mon activité professionnelle est [user_situation][user_situation]",
            "je travaille actuellement sous un contrat de [user_situation][user_situation]",
            "je suis titulaire d'un poste de [user_situation][user_situation]",
            "j'occupe actuellement un emploi en tant que [user_situation][user_situation]"
        ]

        self.variants_s1 = []
        for intro in self.intro_situation:
            for emploi in self.situations_emplois:
                # Ajouter la situation, revenu et dépenses dans la même phrase
                self.variants_s1.append(f"{intro} {emploi}, et {random.choice(self.synonymes_revenu)} [revenu_mensuel][revenu_mensuel]. {random.choice(self.synonymes_depense)} [depense_mensuel][depense_mensuel].")
                self.variants_s1.append(f"{intro} {emploi}, {random.choice(self.synonymes_depense)} [depense_mensuel][depense_mensuel]. {random.choice(self.synonymes_revenu)} [revenu_mensuel][revenu_mensuel].")
        self.variants_s2 = []
        for revenu_intro in self.synonymes_revenu:
            for depense_intro in self.synonymes_depense:
                self.variants_s2.append(f"{revenu_intro} [revenu_mensuel][revenu_mensuel]. {depense_intro} [depense_mensuel][depense_mensuel].")
                self.variants_s2.append(f"{depense_intro} [depense_mensuel][depense_mensuel]. {revenu_intro} [revenu_mensuel][revenu_mensuel].")


        self.variants_p1 = [] #logement_address" & "type_logement"
        for intro in self.intro_property:
            for adresse in self.adresse_variants:
                for desc in self.description_variants:
                    self.variants_p1.append(f"{intro} [type_logement][type_logement] {desc} {adresse} [logement_address][logement_address].")
                    self.variants_p1.append(f"{intro} [type_logement][type_logement] {adresse} [logement_address][logement_address].")
        
        self.variants_p2 = [] # "type_logement"
        for intro in self.intro_property:
            for desc in self.description_variants:
                self.variants_p2.append(f"{intro} [type_logement][type_logement] {desc}.")
                self.variants_p2.append(f"{intro} [type_logement][type_logement].")

        self.variants_p3 = [] #logement_address
        for intro in self.intro_property:
            for adresse in self.adresse_variants:
                self.variants_p3.append(f"{intro} une propriété {adresse} [logement_address][logement_address].")
                self.variants_p3.append(f"{intro} un bien immobilier {adresse} [logement_address][logement_address].")

        self.variants_p4 = [] # None
        for intro in self.intro_property:
            self.variants_p4.append(f"{intro} une propriété.")
            self.variants_p4.append(f"{intro} un bien immobilier.")

        self.remerciements = list(pd.read_csv('generator/data/remerciements.csv')['0'])