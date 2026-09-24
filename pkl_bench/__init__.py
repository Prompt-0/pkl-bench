"""
PKL-Bench: The Pro Kabaddi League Research Benchmark Dataset & Analytics Suite
Covering 10 seasons (2014-2024), 1,060 matches, and 103,176 play-by-play raid events.
"""

__version__ = "1.0.0"
__author__ = "Ritesh Dobhal"
__affiliation__ = "University of Delhi"

from .loader import (
    load_seasons,
    load_teams,
    load_venues,
    load_rulesets,
    load_matches,
    load_players,
    load_player_matches,
    load_raids,
    get_benchmark_split,
    get_splits_info,
)

from .metrics import (
    brier_score,
    expected_calibration_error,
    multiclass_log_loss,
    classification_report_dict,
    expected_points_added,
)

from .validator import (
    validate_dataset_integrity,
    audit_score_conservation,
)

from .baselines import (
    calculate_player_impact_metrics,
    calculate_expected_points_added,
)

__all__ = [
    "load_seasons",
    "load_teams",
    "load_venues",
    "load_rulesets",
    "load_matches",
    "load_players",
    "load_player_matches",
    "load_raids",
    "get_benchmark_split",
    "get_splits_info",
    "brier_score",
    "expected_calibration_error",
    "multiclass_log_loss",
    "classification_report_dict",
    "expected_points_added",
    "calculate_player_impact_metrics",
    "calculate_expected_points_added",
    "validate_dataset_integrity",
    "audit_score_conservation",
]
