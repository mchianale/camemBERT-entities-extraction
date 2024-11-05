import pandas as pd


def calculate_iou(span1, span2):
    """
        Calcule le score d'intersection sur union (IoU) entre deux intervalles.

        :param span1: Tuple contenant les positions de début et de fin du premier intervalle (start1, end1).
        :param span2: Tuple contenant les positions de début et de fin du deuxième intervalle (start2, end2).
        :return: Le score IoU entre les deux intervalles.
    """
    start1, end1 = span1
    start2, end2 = span2
    
    intersection = max(0, min(end1, end2) - max(start1, start2))
    union = max(end1, end2) - min(start1, start2)
    
    iou = intersection / union
    return iou

def computeAllIou(true_span, pred_span):
    """
        Calcule les scores IoU pour toutes les combinaisons possibles entre les entités vraies et prédites.

        :param true_span: Liste de tuples représentant les entités vraies, chaque tuple contient un identifiant et un intervalle.
        :param pred_span: Liste de tuples représentant les entités prédites, chaque tuple contient un identifiant et un intervalle.
        :return: Liste triée des scores IoU avec les paires d'identifiants correspondants.
    """
    iou_scores = []
    for span1 in true_span:
        for span2 in pred_span:
            if span1[0] == -1 or span2[0] == -1:
                iou = 0
            else:
                iou = calculate_iou(span1[1], span2[1])
            iou_scores.append([span1[0], span2[0], iou])
    sorted_iou_scores = sorted(iou_scores, key=lambda x: x[2], reverse=True)

    already_matched_true = []
    already_matched_pred = []
    iou_scores = []
    for score in sorted_iou_scores:
        if score[0] not in already_matched_true and score[1] not in already_matched_pred:
            iou_scores.append(score)
            if score[0] != -1:
                already_matched_true.append(score[0])
            if score[1] != -1:
                already_matched_pred.append(score[1])
    
    return iou_scores

def mapEntities(objs):

    doc_ids = []
    true_ents = []
    pred_ents = []
    true_type = []
    pred_type = []
    true_id = []
    pred_id = []
    scores = []

    for i,obj in enumerate(objs):
        id = i
        pred_span = []
        true_span = []
        for j,entity in enumerate(obj['true_entities']):
            true_span.append((j,[entity['start'], entity['end']]))
        for k,entity in enumerate(obj['predicted_entities']):
                pred_span.append((k,[entity['start'], entity['end']]))
         
        true_span += [(-1,[-1,-1]) for k in range(max(0, len(pred_span) - len(true_span)))]
        pred_span += [(-1,[-1,-1]) for k in range(max(0, len(true_span) - len(pred_span)))]
        iou_scores = computeAllIou(true_span, pred_span)
        for score in iou_scores:
            doc_ids.append(id)
            if score[0] == -1:
                true_ents.append(None)
                true_type.append(None)
                true_id.append(None)
            else:
                entity = obj['true_entities'][score[0]]
                true_ents.append(' '.join(obj['tokens'][entity['start']:entity['end']]))
                true_type.append(entity['type'])
                true_id.append(score[0])
            if score[1] == -1:
                pred_ents.append(None)
                pred_type.append(None)
                pred_id.append(None)
            else:
                entity = obj['predicted_entities'][score[1]]
                pred_ents.append(' '.join(obj['tokens'][entity['start']:entity['end']]))
                pred_type.append(entity['type'])
                pred_id.append(score[1])
            scores.append(score[2])
    df = pd.DataFrame({'doc_id': doc_ids,'true_id' : true_id, 'pred_id' : pred_id, 'true': true_ents, 'pred': pred_ents, 'true_type': true_type, 'pred_type': pred_type, 'iou': scores})
    return df


def mapRelation(obj, df_, id):
    true_relations = obj['true_relations']
    pred_relations = obj['predicted_relations']
    doc_ids = []
    true_types = []
    pred_types = []
    true_head_ids = []
    pred_head_ids = []
    true_tail_ids = []
    pred_tail_ids = []
    true_head_types = []
    pred_head_types = []
    iou_heads = []
    true_tail_types = []
    pred_tail_types = []
    iou_tails = []

    already_seen = []
    for true_rel in true_relations:
        pred_type  = None
        true_type = true_rel['type']
        true_head = true_rel['head']
        true_tail = true_rel['tail']

        df_head = df_[df_['true_id'] == true_head]
        true_head_type = df_head['true_type'].values[0]
        pred_head = df_head['pred_id'].values[0]
        pred_head_type = df_head['pred_type'].values[0]
        iou_head = df_head['iou'].values[0]

        df_tail = df_[df_['true_id'] == true_tail]
        true_tail_type = df_tail['true_type'].values[0]
        pred_tail = df_tail['pred_id'].values[0]
        pred_tail_type = df_tail['pred_type'].values[0]
        iou_tail = df_tail['iou'].values[0]

        for pred_rel in pred_relations:
            if pred_rel['head'] == pred_head and pred_rel['tail'] == pred_tail:
                pred_type = pred_rel['type']
                already_seen.append(pred_rel)
                break
            if pred_rel['head'] == pred_tail and pred_rel['tail'] == pred_head:
                pred_type = pred_rel['type']
                already_seen.append(pred_rel)
                break
       
        doc_ids.append(id)
        true_types.append(true_type)
        pred_types.append(pred_type)
        true_head_ids.append(true_head)
        pred_head_ids.append(pred_head)
        true_tail_ids.append(true_tail)
        pred_tail_ids.append(pred_tail)
        true_head_types.append(true_head_type)
        pred_head_types.append(pred_head_type)
        iou_heads.append(iou_head)
        true_tail_types.append(true_tail_type)
        pred_tail_types.append(pred_tail_type)
        iou_tails.append(iou_tail)

    for pred_rel in pred_relations:
        if pred_rel in already_seen:
            continue
        true_type = None
        pred_type = pred_rel['type']
        pred_head = pred_rel['head']
        pred_tail = pred_rel['tail']

        df_head = df_[df_['pred_id'] == pred_head]
        true_head = df_head['true_id'].values[0]
        true_head_type = df_head['true_type'].values[0]
        pred_head_type = df_head['pred_type'].values[0]
        iou_head = df_head['iou'].values[0]

        df_tail = df_[df_['pred_id'] == pred_tail]
        true_tail = df_tail['true_id'].values[0]
        true_tail_type = df_tail['true_type'].values[0]
        pred_tail_type = df_tail['pred_type'].values[0]
        iou_tail = df_tail['iou'].values[0]

        doc_ids.append(id)
        true_types.append(true_type)
        pred_types.append(pred_type)
        true_head_ids.append(true_head)
        pred_head_ids.append(pred_head)
        true_tail_ids.append(true_tail)
        pred_tail_ids.append(pred_tail)
        true_head_types.append(true_head_type)
        pred_head_types.append(pred_head_type)
        iou_heads.append(iou_head)
        true_tail_types.append(true_tail_type)
        pred_tail_types.append(pred_tail_type)
        iou_tails.append(iou_tail)
    
    return dict({'doc_ids' : doc_ids, 'true_head_id': true_head_ids, 'pred_head_id': pred_head_ids, 'true_tail_id': true_tail_ids, 'pred_tail_id': pred_tail_ids, 
                 'true_entity_head': true_head_types, 'pred_entity_head': pred_head_types, 'iou_head': iou_heads, 
                 'true_entity_tail': true_tail_types, 'pred_entity_tail': pred_tail_types, 'iou_tail': iou_tails, 
                 'true_relation_type': true_types, 'pred_relation_type': pred_types})

def mapRelations(objs, df_ents):
    res = {}
    for i,obj in enumerate(objs):
        df_ = df_ents[df_ents['doc_id'] == i]
        output = mapRelation(obj, df_, i)
        for k, v in output.items():
            if k not in res:
                res[k] = []
            res[k] += v

    return pd.DataFrame(res)

def mapPredictions(data):
    df_ents = mapEntities(data)
    df_rels = mapRelations(data, df_ents)
    return df_ents, df_rels