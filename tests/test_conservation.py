"""
Tests for score conservation law and dataset validation battery.
"""

import pytest
from pkl_bench.validator import audit_score_conservation, validate_dataset_integrity


def test_score_conservation():
    res = audit_score_conservation()
    assert res["matches_evaluated"] == 1060
    assert res["team1_conservation_pass_rate_pct"] == 100.0
    assert res["team2_conservation_pass_rate_pct"] == 100.0
    assert res["total_discrepancies_flagged"] == 0


def test_full_dataset_integrity():
    res = validate_dataset_integrity()
    assert res["overall_validation_passed"] is True
    assert all(res["primary_key_uniqueness"].values())
    assert all(res["foreign_key_integrity"].values())
    assert res["benchmark_splits"]["is_strictly_disjoint"] is True
    assert res["benchmark_splits"]["covers_all_matches"] is True
