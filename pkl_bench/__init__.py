"""
PKL-Bench: The Pro Kabaddi League Research Benchmark Dataset & Analytics Suite
Covering 10 seasons (2014-2024), 1,060 matches, and 90,644 play-by-play raid events.
"""

__version__ = "1.0.0"
__author__ = "Ritesh Dobhal"
__affiliation__ = "University of Delhi"

from .baselines import (
    calculate_expected_points_added,
    calculate_player_impact_metrics,
)
from .loader import (
    get_benchmark_split,
    get_splits_info,
    load_matches,
    load_player_matches,
    load_players,
    load_raids,
    load_rulesets,
    load_seasons,
    load_teams,
    load_venues,
)
from .metrics import (
    brier_score,
    classification_report_dict,
    expected_calibration_error,
    expected_points_added,
    multiclass_log_loss,
)
from .validator import (
    audit_score_conservation,
    validate_dataset_integrity,
)

__all__ = [
    "audit_score_conservation",
    "brier_score",
    "calculate_expected_points_added",
    "calculate_player_impact_metrics",
    "classification_report_dict",
    "expected_calibration_error",
    "expected_points_added",
    "get_benchmark_split",
    "get_splits_info",
    "load_matches",
    "load_player_matches",
    "load_players",
    "load_raids",
    "load_rulesets",
    "load_seasons",
    "load_teams",
    "load_venues",
    "multiclass_log_loss",
    "validate_dataset_integrity",
]
