# Evalution 
Principalement repris les idées de [**Spert**](https://arxiv.org/abs/1909.07755) pour les 3 méthodes d'évaluation.
## Méthode d'évaluation
- **computeMetricsEntitybyTypeSpan()** : Calcule les métriques pour les entités par type et par intervalle (span).
- **computeMetricsRelationBySpan()** : Calcule les métriques pour les relations sans tenir compte de la classification des entités (considère que les spans prédits).
- **computeMetricsRelationByTypeSpan()** : Calcule les métriques pour les relations en tenant compte de la classification des entités (span + type prédits).

Pour chaque méthode d'évaluation, renvoie les metrics **(Precision, Recall, F1)** de chaque type **(entité ou relation)**, avec le nombre **Total** (Il s'agit du nombre d'éléments du type évalué présents dans les données réelles.). De manière globale, renvoie la moyenne et la valeur micro pour chaque metric **(Precision, Recall, F1)**.

## Utilisation
```python
from gold_metrics import evaluation_metrics
# Exemple de données
ent_types = ['Agent', 'Speaker']
rel_types = ['Granted']
# Évaluation des métriques avec des données fournies directement
evaluation_metrics(ent_types, rel_types, threshold=0.8, data=data, output_path='resultats/', printer=True)
# Évaluation des métriques avec un fichier de données
evaluation_metrics(ent_types, rel_types, threshold=0.8, data_path='data_path/data.json', output_path='resultats/', printer=True)
```
**Paramètres :**
- **ent_types** (liste de `str`) : Une liste des types d'entités à évaluer.
- **rel_types** (liste de `str`, optionnel) : Une liste des types de relations à évaluer. Si ce paramètre est `None`, les métriques de relation ne seront pas calculées.
- **threshold** (`float`) : Seuil pour la mesure de l'intersection sur l'union (IoU). Les valeurs d'IoU inférieures à ce seuil seront considérées comme des faux positifs ou des faux négatifs. La valeur par défaut est `0.8`.
- **data** (liste de dictionnaires, optionnel) : Liste de Dictionnaires contenant les données à évaluer. Si ce paramètre est `None`, vous devez fournir `data_path`.
- **data_path** (chaîne de caractères, optionnel) : Chemin du fichier JSON contenant les données à évaluer. Si ce paramètre est `None`, vous devez fournir `data`.
- **output_path** (chaîne de caractères, optionnel) : Chemin du répertoire où les résultats seront sauvegardés sous forme de fichiers CSV. Si ce paramètre est `None`, les résultats ne seront pas sauvegardés.
- **printer** (`bool`) : Si `True`, affiche les résultats des métriques dans la console. La valeur par défaut est `True`.

**Format d'entrée attendu :**
```json
{
        "tokens": [
            "PARIS",
            ",",
            "7",
            "mai",
            ",",
            "Reuter",
            "-",
            "La",
            "France",
            ",",
            "la",
            "Grande",
            "-",
            "Bretagne",
            "et",
            "l",
            "'",
            "Allemagne",
            "ont",
            "annoncé",
            "mercredi",
            "qu",
            "'",
            "elles",
            "joindraient",
            "leurs",
            "efforts",
            "pour",
            "interdire",
            "les",
            "mines",
            "terrestres",
            "antipersonnel",
            ",",
            "dans",
            "le",
            "cadre",
            "de",
            "toutes",
            "les",
            "négociations",
            "en",
            "cours",
            "."
        ],
        "true_entities": [
            {
                "start": 7,
                "end": 18, 
                "type": "Org"
            },
            {
                "start": 19,
                "end": 20,
                "type": "Cue"
            },
            {
                "start": 23,
                "end": 33,
                "type": "IndirectQ"
            }
        ],
        "true_relations": [
            {
                "head": 1,
                "tail": 2,
                "type": "Indicates"
            },
            {
                "head": 0,
                "tail": 2,
                "type": "Quoted_in"
            },
            {
                "head": 0,
                "tail": 1,
                "type": "Granted"
            }
        ],
        "predicted_entities": [
            {
                "start": 7,
                "end": 18,
                "type": "Org"
            },
            {
                "start": 19,
                "end": 20,
                "type": "Cue"
            },
            {
                "start": 23,
                "end": 43,
                "type": "IndirectQ"
            }
        ],
        "predicted_relations": [
            {
                "head": 0,
                "tail": 1,
                "type": "Granted"
            },
            {
                "head": 0,
                "tail": 2,
                "type": "Quoted_in"
            },
            {
                "head": 1,
                "tail": 2,
                "type": "Indicates"
            }
        ]
    }
```
 
