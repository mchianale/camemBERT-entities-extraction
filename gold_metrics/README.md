# Evaluation Methods

## `computeMetricsEntitybyTypeSpan()`
This method calculates the metrics for entities by type and span. It evaluates the performance of entity extraction by comparing the predicted entity spans with the true entity spans for each type. The metrics returned are Precision, Recall, and F1 for each entity type, along with the total count of each entity type in the real data.

## `computeMetricsRelationBySpan()`
This method calculates the metrics for relations, without considering the classification of the entities. It evaluates the relations based solely on the predicted spans, ignoring the entity types. The metrics returned are Precision, Recall, and F1 for each relation, along with the total count of each relation type in the real data.

## `computeMetricsRelationByTypeSpan()`
This method calculates the metrics for relations while considering both the predicted spans and the entity types. It evaluates the relations by comparing the predicted spans and types with the true spans and types of the entities involved. The metrics returned are Precision, Recall, and F1 for each relation type, along with the total count of each relation type in the real data.

## Metrics Calculation
For each evaluation method, the following metrics are calculated:
- **Precision**: Measures the accuracy of the predicted entities or relations.
- **Recall**: Measures how well the model captures the true entities or relations.
- **F1 Score**: Harmonic mean of Precision and Recall, providing a single measure of the model's performance.

Additionally, the following values are returned globally:
- **Average**: The average of the Precision, Recall, and F1 scores across all types.
- **Micro**: A micro-average of Precision, Recall, and F1 scores, which aggregates the true positives, false positives, and false negatives across all types before calculating the metrics.

