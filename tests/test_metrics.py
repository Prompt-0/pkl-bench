"""
Tests for mathematical evaluation metrics in sports analytics.
"""

import numpy as np

from pkl_bench.metrics import (
    brier_score,
    classification_report_dict,
    expected_calibration_error,
    expected_points_added,
    multiclass_log_loss,
)


def test_brier_score_perfect():
    y_true = [1, 0, 1, 1]
    y_prob = [1.0, 0.0, 1.0, 1.0]
    assert brier_score(y_true, y_prob) == 0.0


def test_brier_score_random():
    y_true = [1, 0, 1, 0]
    y_prob = [0.5, 0.5, 0.5, 0.5]
    assert brier_score(y_true, y_prob) == 0.25


def test_ece_perfect():
    y_true = [1, 1, 0, 0]
    y_prob = [1.0, 1.0, 0.0, 0.0]
    ece = expected_calibration_error(y_true, y_prob, n_bins=10)
    assert ece == 0.0


def test_expected_points_added():
    actual = np.array([2.0, 0.0, 1.0])
    expected = np.array([0.8, 0.8, 0.5])
    epa = expected_points_added(actual, expected)
    np.testing.assert_allclose(epa, [1.2, -0.8, 0.5])


def test_multiclass_log_loss():
    y_true = [0, 1, 2]
    y_prob = np.array([
        [0.9, 0.05, 0.05],
        [0.1, 0.8, 0.1],
        [0.05, 0.15, 0.8]
    ])
    loss = multiclass_log_loss(y_true, y_prob, labels=[0, 1, 2])
    assert isinstance(loss, float)
    assert loss > 0.0 and loss < 0.5


def test_classification_report_dict():
    y_true = [0, 1, 0, 1, 1]
    y_pred = [0, 1, 0, 1, 0]
    report = classification_report_dict(y_true, y_pred)
    assert "accuracy" in report
    assert "macro_f1" in report
    assert "weighted_f1" in report
    assert "details" in report
    assert report["accuracy"] == 0.8

