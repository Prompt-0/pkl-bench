"""
PKL-Bench: The Pro Kabaddi League Research Benchmark Dataset & Analytics Suite
Covering 10 seasons (2014-2024), 1,060 matches, and 103,176 play-by-play raid events.
"""

__version__ = "1.0.0"
__author__ = "Antigravity Research Group"

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
    "validate_dataset_integrity",
    "audit_score_conservation",
]
