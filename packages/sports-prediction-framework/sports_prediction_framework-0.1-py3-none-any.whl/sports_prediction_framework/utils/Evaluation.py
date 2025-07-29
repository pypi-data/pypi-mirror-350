from typing import Tuple

import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from enum import Enum


class Metric(Enum):
    ACCURACY = "Accuracy"
    PRECISION = "Precision"
    RECALL = "Recall"
    F1_SCORE = "F1 Score"
    BRIER_SCORE = "Brier Score"
    RPS = "RPS"


def evaluate_metrics(df: pd.DataFrame, average: str = None) -> tuple[DataFrame, ndarray]:
    """
    Evaluates classification metrics and returns a DataFrame summary, including Brier and RPS.

    Parameters:
    - df: DataFrame with columns [0, 1, 2] (predicted probabilities) and 'WDL' (true label)
    - average: Averaging method for multi-class metrics.
               Options: None (per class), 'macro', 'micro', 'weighted'

    Returns:
    - DataFrame summarizing accuracy, precision, recall, F1 score, confusion matrix,
      Brier Score, and RPS.
    """
    preds, labels = get_valid_predictions(df)

    accuracy = compute_accuracy(preds, labels)
    precision = precision_score(labels, preds, average=average, zero_division=0)
    recall = recall_score(labels, preds, average=average, zero_division=0)
    f1 = f1_score(labels, preds, average=average, zero_division=0)
    cm = compute_confusion_matrix(preds, labels)
    brier = compute_multiclass_brier_score(df)
    rps = compute_rps(df)

    if average is None:
        # Return per-class metrics in DataFrame format
        metrics_df = pd.DataFrame({
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1
        }, index=[f'Class {i}' for i in range(len(precision))])
        metrics_df.loc['Overall Accuracy'] = [accuracy, None, None]
    else:
        # Return overall metrics in a single-row DataFrame
        metrics_df = pd.DataFrame([{
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1,
            'Brier Score': brier,
            'RPS': rps
        }])

    return metrics_df, cm


def get_valid_predictions(df: pd.DataFrame):
    """
    Filters out rows with NaNs in prediction columns (0, 1, 2),
    then returns predicted classes and true labels.

    Parameters:
    - df: DataFrame with columns [0, 1, 2] (predicted probabilities) and 'WDL' (true label)

    Returns:
    - preds: ndarray of predicted outcomes (int 0, 1, 2)
    - labels: ndarray of true labels
    """
    valid_rows = df[[0, 1, 2]].notna().all(axis=1)
    preds = df.loc[valid_rows, [0, 1, 2]].values.argmax(axis=1)
    labels = df.loc[valid_rows, 'WDL'].values
    return preds, labels


def compute_accuracy(preds: np.ndarray, labels: np.ndarray) -> float:
    """
    Computes the accuracy of predictions.

    Parameters:
    - preds: predicted outcomes
    - labels: true outcomes

    Returns:
    - accuracy as a float (0.0 to 1.0)
    """
    return accuracy_score(labels, preds)


def compute_precision(preds: np.ndarray, labels: np.ndarray) -> dict:
    """
    Computes precision score per class.

    Parameters:
    - preds: predicted outcomes
    - labels: true outcomes

    Returns:
    - dict of precision scores for each class
    """
    return precision_score(labels, preds, average=None, zero_division=0)


def compute_recall(preds: np.ndarray, labels: np.ndarray) -> dict:
    """
    Computes recall score per class.

    Parameters:
    - preds: predicted class labels
    - labels: true class labels

    Returns:
    - dict of recall scores for each class
    """
    return recall_score(labels, preds, average=None, zero_division=0)


def compute_f1(preds: np.ndarray, labels: np.ndarray) -> dict:
    """
    Computes F1 score per class.

    Parameters:
    - preds: predicted class labels
    - labels: true class labels

    Returns:
    - dict of F1 scores for each class
    """
    return f1_score(labels, preds, average=None, zero_division=0)


def compute_confusion_matrix(preds: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """
    Computes the confusion matrix.

    Parameters:
    - preds: predicted class labels
    - labels: true class labels

    Returns:
    - 2D numpy array (confusion matrix)
    """
    return confusion_matrix(labels, preds)


def compute_multiclass_brier_score(df: pd.DataFrame) -> float:
    """
    Computes the multiclass Brier Score.

    Parameters:
    - df: DataFrame with columns [0, 1, 2] (predicted probabilities) and 'WDL' (true label)

    Returns:
    - Brier Score: a float representing the mean squared error across all classes
    """
    # Filter valid rows
    valid_rows = ~df[[0, 1, 2]].isnull().any(axis=1)
    df_valid = df.loc[valid_rows]

    # True labels (as integers)
    true_labels = df_valid['WDL'].astype(int).values

    # One-hot encode true labels
    one_hot = np.zeros_like(df_valid[[0, 1, 2]].values)
    one_hot[np.arange(len(true_labels)), true_labels] = 1

    # Predicted probabilities
    probs = df_valid[[0, 1, 2]].values

    # Multiclass Brier Score: mean squared error over all classes
    brier = np.mean(np.sum((probs - one_hot) ** 2, axis=1))
    return brier


def compute_rps(df: pd.DataFrame) -> float:
    """
    Computes the Ranked Probability Score (RPS) for multi-class probabilistic predictions.

    Parameters:
    - df: DataFrame with columns [0, 1, 2] (predicted probabilities) and 'WDL' (true label)

    Returns:
    - RPS: a float representing the mean RPS score
    """
    # Filter out rows with NaNs in any of the prediction columns
    valid_mask = ~df[[0, 1, 2]].isnull().any(axis=1)
    df_valid = df[valid_mask].copy()

    # True labels as 1D array
    true_labels = df_valid["WDL"].astype(int).values

    # One-hot encode the true labels
    one_hot = np.zeros_like(df_valid[[0, 1, 2]].values)
    one_hot[np.arange(len(true_labels)), true_labels] = 1

    # Cumulative sums for predicted and actual distributions
    cum_preds = np.cumsum(df_valid[[0, 1, 2]].values, axis=1)
    cum_true = np.cumsum(one_hot, axis=1)

    # Compute RPS per sample
    rps_per_sample = np.sum((cum_preds - cum_true) ** 2, axis=1) / (df_valid.shape[1] - 1)
    return np.mean(rps_per_sample)