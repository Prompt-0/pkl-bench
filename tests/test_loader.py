"""
Tests for PKL-Bench data loading functionality.
"""

import pytest
import pandas as pd
from pkl_bench.loader import (
    load_seasons,
    load_teams,
    load_venues,
    load_matches,
    load_players,
    load_player_matches,
    load_raids,
    get_benchmark_split,
    get_splits_info,
)


def test_load_seasons():
    df = load_seasons()
    assert len(df) == 10
    assert set(df["season_id"]) == set(range(1, 11))
    assert "champion_team_name" in df.columns


def test_load_teams():
    df = load_teams()
    assert len(df) == 12
    assert "Bengaluru Bulls" in df["team_name"].values
    assert "Puneri Paltan" in df["team_name"].values


def test_load_venues():
    df = load_venues()
    assert len(df) >= 20
    assert "matches_hosted" in df.columns
    assert df["matches_hosted"].sum() >= 1000


def test_load_matches():
    df_all = load_matches()
    assert len(df_all) == 1060
    assert "score_margin" in df_all.columns

    # Test filtering by season
    df_s10 = load_matches(season=10)
    assert len(df_s10) == 136
    assert (df_s10["season_id"] == 10).all()


def test_load_players():
    df = load_players()
    assert len(df) >= 800
    assert "career_total_points" in df.columns
    assert df["career_total_points"].max() > 1000  # Top raiders have >1000 points


def test_load_raids():
    df_raids = load_raids(season=1)
    assert len(df_raids) > 4000
    assert "outcome_category" in df_raids.columns
    assert "clock_seconds_remaining" in df_raids.columns


def test_benchmark_splits():
    train_m, val_m, test_m = get_benchmark_split(task="matches")
    assert len(train_m) == 787
    assert len(val_m) == 137
    assert len(test_m) == 136
    assert len(train_m) + len(val_m) + len(test_m) == 1060

    # Ensure zero overlap
    train_ids = set(train_m["match_id"])
    val_ids = set(val_m["match_id"])
    test_ids = set(test_m["match_id"])
    assert len(train_ids.intersection(val_ids)) == 0
    assert len(train_ids.intersection(test_ids)) == 0
    assert len(val_ids.intersection(test_ids)) == 0
