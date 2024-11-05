from abc import ABC
from transformers import AdamW
import torch


def get_optimizer_params(model,learning_rate,new_learning_rate, weight_decay):
        param_optimizer = list(model.named_parameters())
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        new_params = ['entity_classifier', 'crf']
        optimizer_grouped_parameters = [
            # Parameters with weight decay from BERT
            {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay) and not any(np in n for np in new_params)], 
             'weight_decay': weight_decay, 'lr': learning_rate},
            # Parameters without weight decay from BERT
            {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay) and not any(np in n for np in new_params)], 
             'weight_decay': 0.0, 'lr': learning_rate},
            # New layers with weight decay
            {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay) and any(np in n for np in new_params)], 
             'weight_decay': weight_decay, 'lr': new_learning_rate},
            # New layers without weight decay
            {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay) and any(np in n for np in new_params)], 
             'weight_decay': 0.0, 'lr':new_learning_rate}
        ]
        return AdamW(optimizer_grouped_parameters)


class Loss(ABC):
    def compute(self, *args, **kwargs):
        pass


class TokenClassifierLoss(Loss):
    def __init__(self, entity_criterion, 
                 model, optimizer, scheduler, max_grad_norm):
        self._entity_criterion = entity_criterion
        self._model = model
        self._optimizer = optimizer
        self._scheduler = scheduler
        self._max_grad_norm = max_grad_norm

    def compute(self,entity_logits, entity_types, entity_masks,backward=True):
        entity_masks = entity_masks.to(entity_logits.device)
        entity_types = entity_types.to(entity_logits.device)
        
        # entity loss  
        entity_masks = entity_masks.view(-1).float()
        entity_logits = entity_logits.view(-1, entity_logits.shape[-1])
        entity_types = entity_types.view(-1)
        entity_loss = self._entity_criterion(entity_logits, entity_types)
        entity_loss = (entity_loss * entity_masks).sum() / entity_masks.sum()

        if backward:
            self._model.zero_grad()
            entity_loss.backward()
            torch.nn.utils.clip_grad_norm_(self._model.parameters(), self._max_grad_norm)
            self._optimizer.step()
            self._scheduler.step()

        return {'loss': entity_loss.item()}
    


   

 