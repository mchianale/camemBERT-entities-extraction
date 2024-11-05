import numpy as np
import pandas as pd
import json
from .map_predictions import mapPredictions, mapEntities

'''
computeMetricsEntitybyTypeSpan() : Calcule les métriques pour les entités par type et par intervalle (span).
computeMetricsRelationBySpan() : Calcule les métriques pour les relations sans tenir compte de la classification des entités (considère que les spans prédits).
computeMetricsRelationByTypeSpan() : Calcule les métriques pour les relations en tenant compte de la classification des entités (span + type prédits).
evaluate() : Calcule les métriques sur les entités et les métriques de relation (si disponibles) et sauvegarde les résultats si un output_path est spécifié.
'''

class ComputeMetrics:
    '''
        Classe pour calculer les métriques.

        Arguments :
        - ent_types (list of str) : Liste des types d'entités à évaluer. Chaque type d'entité est représenté par une chaîne de caractères.
        - df_ents (pandas.DataFrame) : DataFrame contenant les données des entités avec les colonnes suivantes :
        - 'true_type' : Type véritable de l'entité
        - 'pred_type' : Type prédit de l'entité
        - 'iou' : Intersection sur l'union (IoU) entre les entités prédites et véritables
        - rel_types (list of str, optionnel) : Liste des types de relations à évaluer. Si `None`, les métriques de relation ne seront pas calculées.
        - df_rels (pandas.DataFrame, optionnel) : DataFrame contenant les données des relations avec les colonnes suivantes :
        - 'true_relation_type' : Type véritable de la relation
        - 'pred_relation_type' : Type prédit de la relation
        - 'iou_head' : Intersection sur l'union pour le début de la relation
        - 'iou_tail' : Intersection sur l'union pour la fin de la relation
        - 'true_entity_head' : Entité véritable pour le début de la relation
        - 'pred_entity_head' : Entité prédite pour le début de la relation
        - 'true_entity_tail' : Entité véritable pour la fin de la relation
        - 'pred_entity_tail' : Entité prédite pour la fin de la relation
        - threshold (float) : Seuil pour la mesure de l'IoU. La valeur par défaut est 0.8. Les prédictions avec une IoU inférieure à ce seuil seront considérées comme des faux positifs ou des faux négatifs.
        - output_path (str, optionnel) : Chemin du répertoire où les résultats seront sauvegardés sous forme de fichiers CSV. Si `None`, les résultats ne seront pas sauvegardés.
        - printer (bool) : Si `True`, affiche les résultats des métriques dans la console. La valeur par défaut est `True`.
    '''
    def __init__(self, ent_types,df_ents,
                 rel_types=None, df_rels=None, threshold=0.8, output_path=None, printer=True):
        
        self.ent_types = sorted(ent_types)
        self.df_ents = df_ents
        self.rel_types = rel_types
        if self.rel_types:
            self.rel_types = sorted(self.rel_types)
        self.df_rels = df_rels
        self.threshold = threshold
        self.output_path = output_path
        self.printer = printer
        self.metrics = {}


    def computeMetricsEntitybyTypeSpan(self):

        metrics = {}
        total_tp = 0
        total_fp = 0
        total_fn = 0
        
        for t in self.ent_types:
            df_t = self.df_ents[(self.df_ents['true_type'] == t) | (self.df_ents['pred_type'].isin([t]))]
            #An entity is considered correct if the entity type and span is predicted correctly
            tp = len(self.df_ents[(self.df_ents['true_type'] == t) & (self.df_ents['pred_type'] == t) & (self.df_ents['iou'] >= self.threshold)])
            total_tp += tp
            #false positive  
            df_fp = df_t[df_t['pred_type'] == t]
            fp = len(df_fp[(df_fp['iou'] < self.threshold) | (df_fp['true_type'] != t)])  
            total_fp += fp
            #false negative
            df_fn = df_t[df_t['true_type'] == t]
            fn = len(df_fn[(df_fn['iou'] < self.threshold) | (df_fn['pred_type'] != t)])
            total_fn += fn

            precision = (tp / (tp + fp))*100  
            recall = (tp / (tp + fn))*100 
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

            
            total = self.df_ents[self.df_ents['true_type'] == t].shape[0]
            metrics[t] = {'precision': precision, 'recall': recall, 'f1': f1, 'total' : total}

        metrics['Average'] = {'precision': np.mean([metrics[t]['precision'] for t in self.ent_types]), 
                                'recall': np.mean([metrics[t]['recall'] for t in self.ent_types]), 
                                'f1': np.mean([metrics[t]['f1'] for t in self.ent_types]), 
                                'total': self.df_ents[self.df_ents['true_id'].notnull()].shape[0]}
        
        precision_micro = (total_tp / (total_tp + total_fp))*100
        recall_micro = (total_tp / (total_tp + total_fn))*100
        f1_micro = (2*precision_micro*recall_micro) / (precision_micro + recall_micro)
        
        metrics['micro'] = {
            'precision': precision_micro,
            'recall': recall_micro,
            'f1': f1_micro,
            'total': self.df_ents[self.df_ents['true_id'].notnull()].shape[0]
        }

        if self.printer:
            print('--- Entities ---\nAn entity is considered correct if the entity type and span is predicted correctly')
            for t in metrics.keys():
                print(t,' :')
                for k in metrics[t].keys():
                    print(f'{k}: {metrics[t][k]:.2f}')
                print()
            print('-'*50)

        self.metrics['entity'] = metrics

    # NEC
    # Without entity classification (NEC)
    def computeMetricsRelationBySpan(self):
        metrics = {}
        # true positve
        total_tp = 0
        total_fp = 0
        total_fn = 0
        for t in self.rel_types:
            df_t = self.df_rels[(self.df_rels['true_relation_type'] == t) | (self.df_rels['pred_relation_type'] == t)]
            # true positive
            tp = len(df_t[(df_t['iou_head'] >= self.threshold) & (df_t['iou_tail'] >= self.threshold) & (df_t['true_relation_type'] == df_t['pred_relation_type'])])
            total_tp += tp
            #false positive  
            df_fp = df_t[df_t['pred_relation_type'] == t]
            fp = len(df_fp[(df_fp['iou_head'] < self.threshold) |  (df_fp['iou_tail'] < self.threshold) | (df_fp['true_relation_type'] != t)])  
            total_fp += fp
            #false negative
            df_fn = df_t[df_t['true_relation_type'] == t]
            fn = len(df_fn[(df_fn['iou_head'] < self.threshold) |  (df_fn['iou_tail'] < self.threshold) | (df_fn['pred_relation_type'] != t)]) 
            total_fn += fn

            precision = (tp / (tp + fp))*100
            recall = (tp / (tp + fn))*100
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            total = self.df_rels[self.df_rels['true_relation_type'] == t].shape[0]
            metrics[t] = {'precision': precision, 'recall': recall, 'f1': f1, 'total' : total}
                

        metrics['Average'] = {'precision': np.mean([metrics[t]['precision'] for t in self.rel_types]), 'recall': np.mean([metrics[t]['recall'] for t in self.rel_types]), 'f1': np.mean([metrics[t]['f1'] for t in self.rel_types]), 
                            'total': self.df_rels[self.df_rels['true_relation_type'].notnull()].shape[0]}
        
        precision_micro = (total_tp / (total_tp + total_fp))*100
        recall_micro = (total_tp / (total_tp + total_fn))*100
        f1_micro = (2*precision_micro*recall_micro) / (precision_micro + recall_micro)
        
        metrics['micro'] = {
            'precision': precision_micro,
            'recall': recall_micro,
            'f1': f1_micro,
            'total': self.df_rels[self.df_rels['true_relation_type'].notnull()].shape[0]
        }
        if self.printer:
            print('Without entity classification (NEC)\nA relation is considered correct if the relation type and the spans of the two related entities are predicted correctly (entity type is not considered)')
            for t in metrics.keys():
                print(t,' :')
                for k in metrics[t].keys():
                    print(f'{k}: {metrics[t][k]:.2f}')
                print()
            print('-'*50)
                
        self.metrics['relation_by_span'] = metrics


    # With entity classification (NEC)
    def computeMetricsRelationByTypeSpan(self):
        metrics = {}
        # true positv
        total_tp = 0
        total_fp = 0
        total_fn = 0
        for t in self.rel_types:
            df_t = self.df_rels[(self.df_rels['true_relation_type'] == t) | (self.df_rels['pred_relation_type'] == t)]
            # true positive
            tp = len(df_t[(df_t['iou_head'] >= self.threshold) & (df_t['iou_tail'] >= self.threshold) & (df_t['true_relation_type'] == df_t['pred_relation_type']) 
                    & (df_t['true_entity_head'] == df_t['pred_entity_head']) & (df_t['true_entity_tail'] == df_t['pred_entity_tail'])])
            total_tp += tp
            #false positive  
            df_fp = df_t[df_t['pred_relation_type'] == t]
            fp = len(df_fp[(df_fp['iou_head'] < self.threshold) |  (df_fp['iou_tail'] < self.threshold) | (df_fp['true_relation_type'] != t) | 
                (df_fp['true_entity_head'] != df_fp['pred_entity_head']) | (df_fp['true_entity_tail'] != df_fp['pred_entity_tail'])])  
            total_fp += fp
            #false negative
            df_fn = df_t[df_t['true_relation_type'] == t]
            fn = len(df_fn[(df_fn['iou_head'] < self.threshold) |  (df_fn['iou_tail'] < self.threshold) | (df_fn['pred_relation_type'] != t) | 
                (df_fn['true_entity_head'] != df_fn['pred_entity_head']) | (df_fn['true_entity_tail'] != df_fn['pred_entity_tail'])]) 
            total_fn += fn

            precision = (tp / (tp + fp))*100
            recall = (tp / (tp + fn))*100
            f1 = 2 * precision * recall / (precision + recall)  if (precision + recall) > 0 else 0
            total = self.df_rels[self.df_rels['true_relation_type'] == t].shape[0]
            metrics[t] = {'precision': precision, 'recall': recall, 'f1': f1, 'total' : total}
          

        metrics['Average'] = {'precision': np.mean([metrics[t]['precision'] for t in self.rel_types]), 'recall': np.mean([metrics[t]['recall'] for t in self.rel_types]), 'f1': np.mean([metrics[t]['f1'] for t in self.rel_types]), 
                            'total': self.df_rels[self.df_rels['true_relation_type'].notnull()].shape[0]}
       
        precision_micro = (total_tp / (total_tp + total_fp))*100
        recall_micro = (total_tp / (total_tp + total_fn))*100
        f1_micro = (2*precision_micro*recall_micro) / (precision_micro + recall_micro)
        
        metrics['micro'] = {
            'precision': precision_micro,
            'recall': recall_micro,
            'f1': f1_micro,
            'total': self.df_rels[self.df_rels['true_relation_type'].notnull()].shape[0]
        }
        
        if self.printer:
            print('With entity classification (NEC)\nA relation is considered correct if the relation type and the two related entities are predicted correctly (in span and entity type)')
            for t in metrics.keys():
                print(t,' :')
                for k in metrics[t].keys():
                    print(f'{k}: {metrics[t][k]:.2f}')
                print()
            print('-'*50)

        self.metrics['relation_by_span_type'] = metrics

    def evaluate(self):
        #self.computeMetricsEntitybySpan()
        self.computeMetricsEntitybyTypeSpan()
        if self.rel_types:
            self.computeMetricsRelationBySpan()
            self.computeMetricsRelationByTypeSpan()
        if self.output_path is not None:
            for k,v in self.metrics.items():
                df_metric= pd.DataFrame(v).T
                df_metric.to_csv(f'{self.output_path}/{k}.csv')
                if self.printer:
                    print(f'{k} metrics saved in {self.output_path}/{k}.csv')

def evaluation_metrics(ent_types, rel_types=None,   
                    threshold=0.8,
                    data=None, data_path=None, output_path=None, printer=True):
    '''
        Fonction pour évaluer les métriques d'extraction d'entités  et de relations.

        Arguments :
        - ent_types (list of str) : Liste des types d'entités à évaluer.
        - rel_types (list of str, optionnel) : Liste des types de relations à évaluer. Si `None`, les métriques de relation ne seront pas calculées.
        - threshold (float) : Seuil pour la mesure de l'IoU. La valeur par défaut est 0.8.
        - data (list de dict, optionnel) : Dictionnaire contenant les données à évaluer. Si `None`, `data_path` doit être spécifié.
        - data_path (str, optionnel) : Chemin du fichier JSON contenant les données à évaluer. Si `None`, `data` doit être spécifié.
        - output_path (str, optionnel) : Chemin du répertoire où les résultats seront sauvegardés sous forme de fichiers CSV.
        - printer (bool) : Si `True`, affiche les résultats des métriques dans la console. La valeur par défaut est `True`.

        Exemple d'utilisation :
        ent_types = ['Agent', 'Speaker']
        rel_types = ['Granted']
        # Évaluation des métriques avec des données fournies directement
        evaluation_metrics(ent_types, rel_types, threshold=0.8, data=data, output_path='resultats/', printer=True)
        # Évaluation des métriques avec un fichier de données
        evaluation_metrics(ent_types, rel_types, threshold=0.8, data_path='data_path/data.json', output_path='resultats/', printer=True)
    '''
    assert data or data_path, 'data or data_path must be provided'
    if data_path and not data:
        f = open(data_path)
        data = json.load(f)
        f.close()

    if not rel_types:
        df_ents, df_rels = mapEntities(data), None
    else:
        df_ents, df_rels = mapPredictions(data)
       
    cm = ComputeMetrics(ent_types, df_ents, rel_types, df_rels, threshold, output_path, printer)
    cm.evaluate()
    