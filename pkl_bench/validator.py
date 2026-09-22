"""
Comprehensive dataset integrity, constraint validation, and score conservation auditing.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from pathlib import Path
from .loader import (
    load_seasons,
    load_teams,
    load_venues,
    load_matches,
    load_players,
    load_player_matches,
    load_raids,
    get_splits_info,
)


def audit_score_conservation(df_matches: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Verifies the fundamental mathematical conservation law of Kabaddi scoring:
    Team Score = Raid Points + Tackle Points + All-Out Bonus + Technical/Extra Points.
    Returns audit statistics and any discrepancies.
    """
    if df_matches is None:
        df_matches = load_matches()

    total_checked = len(df_matches)
    perfect_t1 = 0
    perfect_t2 = 0
    discrepancies = []

    for idx, row in df_matches.iterrows():
        mid = row["match_id"]
        # Team 1 audit
        calc_t1 = row["team1_raid_points"] + row["team1_tackle_points"] + row["team1_all_out_points"] + row["team1_extra_points"]
        diff_t1 = abs(calc_t1 - row["team1_score"])
        if diff_t1 == 0:
            perfect_t1 += 1
        elif diff_t1 > 0 and calc_t1 > 0:
            discrepancies.append({
                "match_id": mid,
                "team": "team1",
                "actual_score": row["team1_score"],
                "sum_breakdown": calc_t1,
                "delta": diff_t1
            })

        # Team 2 audit
        calc_t2 = row["team2_raid_points"] + row["team2_tackle_points"] + row["team2_all_out_points"] + row["team2_extra_points"]
        diff_t2 = abs(calc_t2 - row["team2_score"])
        if diff_t2 == 0:
            perfect_t2 += 1
        elif diff_t2 > 0 and calc_t2 > 0:
            discrepancies.append({
                "match_id": mid,
                "team": "team2",
                "actual_score": row["team2_score"],
                "sum_breakdown": calc_t2,
                "delta": diff_t2
            })

    pct_t1 = (perfect_t1 / total_checked) * 100
    pct_t2 = (perfect_t2 / total_checked) * 100

    return {
        "matches_evaluated": total_checked,
        "team1_conservation_pass_rate_pct": round(pct_t1, 2),
        "team2_conservation_pass_rate_pct": round(pct_t2, 2),
        "total_discrepancies_flagged": len(discrepancies),
        "sample_discrepancies": discrepancies[:5]
    }


def validate_dataset_integrity(data_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Executes a complete validation battery across all dataset tiers:
    1. Schema consistency and shape verification
    2. Primary key uniqueness
    3. Foreign key integrity
    4. Benchmark split disjointness and completeness
    """
    results = {}

    # Load tiers
    df_seasons = load_seasons(data_dir=data_dir)
    df_teams = load_teams(data_dir=data_dir)
    df_venues = load_venues(data_dir=data_dir)
    df_matches = load_matches(data_dir=data_dir)
    df_players = load_players(data_dir=data_dir)
    df_pm = load_player_matches(data_dir=data_dir)
    df_raids = load_raids(data_dir=data_dir)
    splits = get_splits_info(data_dir=data_dir)

    results["counts"] = {
        "seasons": len(df_seasons),
        "teams": len(df_teams),
        "venues": len(df_venues),
        "matches": len(df_matches),
        "players": len(df_players),
        "player_match_stats": len(df_pm),
        "raids_pbp": len(df_raids)
    }

    # Check 1: Primary Key Uniqueness
    pk_checks = {
        "seasons.season_id": df_seasons["season_id"].is_unique,
        "teams.team_id": df_teams["team_id"].is_unique,
        "venues.venue_id": df_venues["venue_id"].is_unique,
        "matches.match_id": df_matches["match_id"].is_unique,
        "players.player_id": df_players["player_id"].is_unique,
    }
    results["primary_key_uniqueness"] = pk_checks

    # Check 2: Foreign Key Integrity
    valid_team_ids = set(df_teams["team_id"])
    match_teams_valid = (
        df_matches["team1_id"].isin(valid_team_ids).all() and
        df_matches["team2_id"].isin(valid_team_ids).all()
    )
    pm_teams_valid = df_pm["team_id"].isin(valid_team_ids).all()

    valid_match_ids = set(df_matches["match_id"])
    pm_matches_valid = df_pm["match_id"].isin(valid_match_ids).all()
    raids_matches_valid = df_raids["match_id"].isin(valid_match_ids).all()

    results["foreign_key_integrity"] = {
        "matches_team_ids_valid": bool(match_teams_valid),
        "player_matches_team_ids_valid": bool(pm_teams_valid),
        "player_matches_match_ids_valid": bool(pm_matches_valid),
        "raids_match_ids_valid": bool(raids_matches_valid)
    }

    # Check 3: Benchmark Split Disjointness
    train_ids = set(splits["train"]["match_ids"])
    val_ids = set(splits["validation"]["match_ids"])
    test_ids = set(splits["test"]["match_ids"])

    train_val_intersect = len(train_ids.intersection(val_ids))
    train_test_intersect = len(train_ids.intersection(test_ids))
    val_test_intersect = len(val_ids.intersection(test_ids))
    total_split_ids = len(train_ids) + len(val_ids) + len(test_ids)

    results["benchmark_splits"] = {
        "train_matches": len(train_ids),
        "validation_matches": len(val_ids),
        "test_matches": len(test_ids),
        "total_matches_in_splits": total_split_ids,
        "is_strictly_disjoint": (train_val_intersect == 0 and train_test_intersect == 0 and val_test_intersect == 0),
        "covers_all_matches": (total_split_ids == len(df_matches))
    }

    # Check 4: Score Conservation Law
    results["score_conservation"] = audit_score_conservation(df_matches)

    all_passed = (
        all(pk_checks.values()) and
        all(results["foreign_key_integrity"].values()) and
        results["benchmark_splits"]["is_strictly_disjoint"] and
        results["benchmark_splits"]["covers_all_matches"]
    )
    results["overall_validation_passed"] = bool(all_passed)
    return results
