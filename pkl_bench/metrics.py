"""
Standardized evaluation metrics for sports analytics and ML benchmarking.
"""

from typing import Dict, Any, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.metrics import log_loss, brier_score_loss, classification_report, accuracy_score, f1_score


def brier_score(y_true: Union[np.ndarray, List[int]], y_prob: Union[np.ndarray, List[float]]) -> float:
    """
    Computes the Brier score for probabilistic binary classification.
    BS = (1/N) * sum((y_prob_i - y_true_i)^2)
    Lower is better. Perfect score is 0.0.
    """
    y_t = np.asarray(y_true).astype(float)
    y_p = np.asarray(y_prob).astype(float)
    return float(np.mean((y_p - y_t) ** 2))


def multiclass_log_loss(
    y_true: Union[np.ndarray, List[Any]],
    y_prob: np.ndarray,
    labels: Optional[List[Any]] = None
) -> float:
    """
    Computes multi-class logarithmic loss.
    Cross-entropy loss over categorical probability distribution.
    """
    return float(log_loss(y_true, y_prob, labels=labels))


def expected_calibration_error(
    y_true: Union[np.ndarray, List[int]],
    y_prob: Union[np.ndarray, List[float]],
    n_bins: int = 10
) -> float:
    """
    Computes the Expected Calibration Error (ECE) for predicted probabilities.
    ECE = sum_{b=1}^B (|B_b| / N) * |acc(B_b) - conf(B_b)|
    """
    y_t = np.asarray(y_true)
    y_p = np.asarray(y_prob)

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    total_samples = len(y_t)

    for i in range(n_bins):
        bin_lower = bins[i]
        bin_upper = bins[i + 1]
        mask = (y_p >= bin_lower) & (y_p < bin_upper) if i < n_bins - 1 else (y_p >= bin_lower) & (y_p <= bin_upper)
        bin_size = np.sum(mask)

        if bin_size > 0:
            bin_acc = np.mean(y_t[mask])
            bin_conf = np.mean(y_p[mask])
            ece += (bin_size / total_samples) * np.abs(bin_acc - bin_conf)

    return float(ece)


def classification_report_dict(
    y_true: Union[np.ndarray, List[Any]],
    y_pred: Union[np.ndarray, List[Any]]
) -> Dict[str, Any]:
    """
    Returns full accuracy, macro-F1, weighted-F1, and per-class precision/recall metrics.
    """
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    weighted_f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    return {
        "accuracy": float(acc),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "details": report
    }


def expected_points_added(
    actual_points: Union[np.ndarray, List[float]],
    expected_points: Union[np.ndarray, List[float]]
) -> np.ndarray:
    """
    Calculates Expected Points Added (EPA) for an event:
    EPA = Actual Points - Expected Points
    """
    return np.asarray(actual_points) - np.asarray(expected_points)
