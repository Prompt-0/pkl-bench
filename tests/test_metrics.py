"""
Tests for mathematical evaluation metrics in sports analytics.
"""

import pytest
import numpy as np
from pkl_bench.metrics import (
    brier_score,
    expected_calibration_error,
    multiclass_log_loss,
    classification_report_dict,
    expected_points_added
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
