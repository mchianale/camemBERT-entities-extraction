# Fine-Tuning Camembert for Real Estate Loan Entity Extraction

## Overview
This repository focuses on fine-tuning the Camembert language model for extracting specific entities related to real estate loan requests from French texts. The task involves identifying various entities from loan applications, such as user personal details, financial information, and property-related data. These entities are extracted from the text and classified into corresponding labels.

## Task Description
The goal is to extract the following entities from a given French text related to real estate loan applications. The task is formulated as a token classification problem, where each token in the text is classified into one of the predefined categories.

## Entities to Extract

| Entity Name               | Description                      |
|---------------------------|----------------------------------|
| user_mail                 | User's email                     |
| user_num                  | User's phone number              |
| user_address              | User's address                   |
| user_name                 | User's name                      |
| montant_pret              | Loan amount                      |
| duree_pret                | Loan duration                    |
| user_situation            | User's financial situation       |
| depense_mensuel           | Monthly expenses                 |
| revenu_mensuel            | Monthly income                   |
| type_logement             | Type of housing                  |
| apport                    | Down payment                     |
| duree_pret_year           | Loan duration in years           |
| logement_address          | Property address                 |

## Methodology

To achieve the goal of extracting these entities, the following steps were taken:

1. **Data Generation**: 
   - A synthetic data generator was created to generate artificial loan application texts. This data was used to train the model before applying it to real-world data. **[see folder](https://github.com/mchianale/camemBERT-entities-extraction/tree/main/generator)**
   
2. **Fine-Tuning Camembert**: 
   - The Camembert model, which is a pre-trained French language model, was fine-tuned to classify tokens into the above entities. A token classification architecture was used, with a fully connected layer (FC1) and a dropout layer to reduce overfitting. **[see folder](https://github.com/mchianale/camemBERT-entities-extraction/tree/main/TokenClassifier)**
   - **Model Architecture**:
     - `self.fc1 = nn.Linear(input_dim, hidden_dim)`: The first fully connected layer.
     - `self.fc2 = nn.Linear(hidden_dim, output_dim)`: The second fully connected layer that outputs the predicted class for each token.
     - `self.dropout = nn.Dropout(dropout_prob)`: A dropout layer to avoid overfitting during training.

![Token Classification](https://github.com/mchianale/camemBERT-entities-extraction/blob/main/image/token_classification.png)   
    **Token Labeling Convention**
    - **0**: Represents negative cases (i.e., tokens that are not part of any entity).
    - **B-**: A token marking the beginning of an entity (e.g., the first token of the entity "user_mail").
    - **I-**: A token that comes after the beginning token of an entity (e.g., subsequent tokens of the entity "user_mail").
    For example:
    - **B-user_mail**: Marks the beginning of a user's email address.
    - **I-user_mail**: Marks the continuation of the user's email address.
   
3. **Model Evaluation**:
   - Evaluation of the fine-tuned model was performed using precision, recall, and F1 score to ensure the model's effectiveness in extracting entities accurately from loan application texts.
   - Various evaluation metrics were employed, including:
     - **Precision**: Measures the proportion of relevant instances among the retrieved instances.
     - **Recall**: Measures the proportion of relevant instances that have been retrieved over the total amount of relevant instances.
     - **F1 Score**: A balanced measure that combines both precision and recall into one number.
   - **[see package gold_metrics](https://github.com/mchianale/camemBERT-entities-extraction/blob/main/gold_metrics/README.md)**

## Requirement
**Dependencies :**
```bash
pip install -r requirements.txt
```

**Evaluation package set :**
```bash
cd gold_metrics
pip install -e .
```

## Create Data

To generate fake data :
```bash
cd generator
python createData.py
```

To specify the output path and dataset size, edit generator/createData.py:
```python
train_size = 10000
test_size = 5000
train_path = 'data/train.json'
test_path = 'data/test.json'  
```

## Train
```bash
cd TokenClassifier
python run.py --train configs/train_cam.json
```
Train config example :
```json
{
    "model" : "camembert-base",
    "train_path" : "../data/train.json",
    "save_path" : "models",
    "batch_size" : 8,
    "epochs" : 100,
    "shuffle" : true,
    "max_length" : 300,
    "lowercase" : false,
    "prop_drop" : 0.1,
    "freeze_transformer" : false,
    "learning_rate" : 5e-5,
    "new_learning_rate" : 2e-5,
    "lr_warmup" : 0.1,
    "weight_decay" : 0.01,
    "max_grad_norm" : 1.0,

    "valid_path" : "../data/dev.json",
    "valid_batch_size" : 8
}
```
- *valid_path* (option)

**Tokenizer Parameters:**
- **Path**: Use the same path as the `model` argument for the tokenizer.
- **do_lowercase**: `lowercase` — This ensures that all tokens are lowercased.
- **max_length**: Defines the maximum document length after tokenization. Padding is applied during training for each batch.

**Optimizer Parameters:**
- **learning_rate**: This parameter sets the learning rate for the Camembert model during fine-tuning.
- **new_learning_rate**: This parameter sets the learning rate for the Feedforward Neural Network (FFN) used for token classification.

## Evaluation
```bash
cd TokenClassifier
python run.py --eval configs/eval.json
```
Eval config example :
```json
{
    "model" : "models/3_camembert-base",
    "predict_path" : "../data/test.json",
    "batch_size" : 8,
    "max_length" : 300,
    "threshold" : 0.8
}
```

- threshold : minimum threshold of IoU computation to consider if a prediction is correct.

## Prediction
```bash
cd TokenClassifier
python run.py --predict configs/predict.json
```

Prediction config example :
```json
{
    "model" : "models/3_camembert-base",
    "predict_path" : "../data/test.json",
    "results_path" : "predictions",
    "batch_size" : 8,
    "max_length" : 300
}
```

## Result
**train config :**
```json
{
    "model" : "camembert-base",
    "train_path" : "../data/train.json",
    "save_path" : "models",
    "batch_size" : 16,
    "epochs" : 40,

    "shuffle" : true,
    "max_length" : 300,
    "lowercase" : false,

    "prop_drop" : 0.1,
    "freeze_transformer" : false,

    "learning_rate" : 5e-5,
    "new_learning_rate" : 2e-5,
    "lr_warmup" : 0.2,
    "weight_decay" : 0.01,
    "max_grad_norm" : 1.0
}
```

---

**Train data size :** 2000

---

**Result :**

| Micro-Precision | Micro-Recall | Micro-F1 | Total Entities |
|:---------------:|:------------:|:---------:|:-------------:|
|      99.65       |     99.54    |   99.59   |     50014      |

*An entity is considered correct if both the type and the position of the entity are correctly predicted (based on a threshold for the position).*

- Threshold : **80%**
 
