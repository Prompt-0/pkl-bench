"""
Benchmark Task 4: Player Valuation & Impact Rating
Computes context-adjusted True Raider Impact (TRI), Expected Points Added (EPA),
and Defender Impact metrics.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from ..loader import load_player_matches, load_raids, load_players


def calculate_player_impact_metrics(season: Optional[int] = None) -> pd.DataFrame:
    """
    Computes True Raider Impact (TRI) and True Defender Impact (TDI).
    Formula:
      TRI = (Raid Points - 1.25 * Unsuccessful Raids + 0.5 * Super Raids) / Total Raids
      TDI = (Tackle Points - 1.0 * Unsuccessful Tackles + 1.0 * Super Tackles) / Total Tackles
    """
    df_pm = load_player_matches(season=season)

    # Group by player
    grouped = df_pm.groupby(["player_id", "player_name", "role"]).agg({
        "played": "sum",
        "total_points": "sum",
        "raid_points_total": "sum",
        "raids_total": "sum",
        "raids_successful": "sum",
        "raids_unsuccessful": "sum",
        "super_raids": "sum",
        "tackle_points_total": "sum",
        "tackles_total": "sum",
        "tackles_successful": "sum",
        "tackles_unsuccessful": "sum",
        "super_tackles": "sum",
        "super_10": "sum",
        "high_5": "sum"
    }).reset_index()

    # Filter out players with minimal attempts for statistical stability
    grouped["matches_played"] = grouped["played"]

    # True Raider Impact
    min_raids = 20
    tri = np.where(
        grouped["raids_total"] >= min_raids,
        (grouped["raid_points_total"] - 1.25 * grouped["raids_unsuccessful"] + 0.5 * grouped["super_raids"]) / grouped["raids_total"],
        np.nan
    )
    grouped["true_raider_impact"] = np.round(tri, 3)

    # True Defender Impact
    min_tackles = 15
    tdi = np.where(
        grouped["tackles_total"] >= min_tackles,
        (grouped["tackle_points_total"] - 1.0 * grouped["tackles_unsuccessful"] + 1.0 * grouped["super_tackles"]) / grouped["tackles_total"],
        np.nan
    )
    grouped["true_defender_impact"] = np.round(tdi, 3)

    return grouped.sort_values("total_points", ascending=False).reset_index(drop=True)


def calculate_expected_points_added(df_raids: Optional[pd.DataFrame] = None, min_raids: int = 50) -> pd.DataFrame:
    """
    Computes context-conditioned Expected Points Added (EPA) for every raider:
    EPA_t = Actual Raid Points_t - E[Points | Do-or-Die, Half]
    Aggregates Cumulative EPA and EPA per Raid.
    """
    if df_raids is None:
        df_raids = load_raids()

    # Calculate baseline expectation across state partitions
    state_means = df_raids.groupby(["is_do_or_die", "half"])["raid_points"].mean().to_dict()

    df = df_raids.copy()
    df["expected_points"] = df.apply(
        lambda r: state_means.get((r["is_do_or_die"], r["half"]), 0.5), axis=1
    )
    df["epa"] = df["raid_points"] - df["expected_points"]

    raider_epa = df.groupby(["raider_id", "raider_name"]).agg(
        total_raids=("raid_sequence_no", "count"),
        total_raid_points=("raid_points", "sum"),
        cumulative_epa=("epa", "sum"),
        epa_per_raid=("epa", "mean")
    ).reset_index()

    raider_epa = raider_epa[raider_epa["total_raids"] >= min_raids]
    raider_epa["cumulative_epa"] = np.round(raider_epa["cumulative_epa"], 2)
    raider_epa["epa_per_raid"] = np.round(raider_epa["epa_per_raid"], 4)

    return raider_epa.sort_values("cumulative_epa", ascending=False).reset_index(drop=True)

