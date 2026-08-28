# Machine Learning Evaluation

## Overview

Model evaluation measures how well a machine learning model performs on data that it has not seen during training.

Evaluation helps determine whether the model generalizes to real-world data.

## Dataset Splitting

A dataset is commonly divided into:

- Training set
- Validation set
- Test set

The training set is used to learn model parameters.

The validation set is used to tune hyperparameters and compare approaches.

The test set is used for final evaluation.

## Classification Metrics

### Accuracy

Accuracy represents the proportion of predictions that are correct.

Accuracy can be misleading when classes are highly imbalanced.

### Precision

Precision measures how many predicted positive examples are actually positive.

Precision is important when false positives are costly.

### Recall

Recall measures how many actual positive examples were successfully identified.

Recall is important when missing positive cases is costly.

### F1 Score

F1 score combines precision and recall.

It is useful when both precision and recall are important.

## Computer Vision Metrics

Object detection commonly uses:

- IoU
- Precision
- Recall
- mAP

IoU, or Intersection over Union, measures the overlap between the predicted bounding box and the ground-truth bounding box.

## Retrieval Evaluation

RAG systems can be evaluated using retrieval metrics such as:

- Precision@K
- Recall@K
- Hit Rate
- Mean Reciprocal Rank

These metrics measure whether relevant documents are successfully retrieved.

## RAG Evaluation

A RAG application should evaluate both retrieval and generation.

Important dimensions include:

- Retrieval relevance
- Answer relevance
- Faithfulness
- Context utilization
- Citation accuracy

A system should not only produce fluent answers; its answers should be supported by the retrieved information.