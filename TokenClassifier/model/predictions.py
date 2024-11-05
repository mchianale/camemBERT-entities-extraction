def getPredictions_batch(true_docs, entities):
    # final format
    predictions = []
    for batch_index in range(len(entities)):
        predictions.append({
            'tokens': true_docs[batch_index]['pre_tokens'],
            'true_entities': true_docs[batch_index]['entities'],
            'predicted_entities': entities[batch_index],
        })
    return predictions

   


