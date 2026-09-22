"""
Data loader module for PKL-Bench.
Provides fast typed access to Parquet and CSV dataset tiers and official benchmark splits.
"""

import json
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List, Union
import pandas as pd

# Default data location relative to this file or standard installation path
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = PACKAGE_ROOT / "data"


def _resolve_file(rel_path: str, format_pref: str = "parquet", data_dir: Optional[Path] = None) -> Path:
    base = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    target = base / f"{rel_path}.{format_pref}"
    if not target.exists():
        fallback_fmt = "csv" if format_pref == "parquet" else "parquet"
        target_fallback = base / f"{rel_path}.{fallback_fmt}"
        if target_fallback.exists():
            return target_fallback
        raise FileNotFoundError(f"Neither {target} nor {target_fallback} found in data directory: {base}")
    return target


def _load_df(rel_path: str, format_pref: str = "parquet", data_dir: Optional[Path] = None) -> pd.DataFrame:
    file_path = _resolve_file(rel_path, format_pref, data_dir)
    if file_path.suffix == ".parquet":
        return pd.read_parquet(file_path)
    return pd.read_csv(file_path)


def load_seasons(format_pref: str = "parquet", data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load PKL seasons metadata (Seasons 1-10)."""
    return _load_df("metadata/seasons", format_pref, data_dir)


def load_teams(format_pref: str = "parquet", data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load all 12 PKL franchise registry entries."""
    return _load_df("metadata/teams", format_pref, data_dir)


def load_venues(format_pref: str = "parquet", data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load all 28 PKL stadium venue records."""
    return _load_df("metadata/venues", format_pref, data_dir)


def load_rulesets(format_pref: str = "parquet", data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load codified PKL competition rules."""
    return _load_df("metadata/rulesets", format_pref, data_dir)


def load_matches(
    season: Optional[Union[int, List[int]]] = None,
    format_pref: str = "parquet",
    data_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Load match records (1,060 matches).
    Filterable by season (e.g. season=10 or season=[8, 9, 10]).
    """
    df = _load_df("matches/matches", format_pref, data_dir)
    if season is not None:
        if isinstance(season, int):
            df = df[df["season_id"] == season].reset_index(drop=True)
        elif isinstance(season, (list, tuple, set)):
            df = df[df["season_id"].isin(season)].reset_index(drop=True)
    return df


def load_players(format_pref: str = "parquet", data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load master directory of all 805 registered PKL players and career totals."""
    return _load_df("players/players", format_pref, data_dir)


def load_player_matches(
    season: Optional[Union[int, List[int]]] = None,
    match_id: Optional[int] = None,
    format_pref: str = "parquet",
    data_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Load individual player-match boxscore records (26,760 entries).
    """
    df = _load_df("player_matches/player_match_stats", format_pref, data_dir)
    if season is not None:
        if isinstance(season, int):
            df = df[df["season_id"] == season]
        elif isinstance(season, (list, tuple, set)):
            df = df[df["season_id"].isin(season)]
    if match_id is not None:
        df = df[df["match_id"] == match_id]
    return df.reset_index(drop=True)


def load_raids(
    season: Optional[Union[int, List[int]]] = None,
    match_id: Optional[int] = None,
    format_pref: str = "parquet",
    data_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Load discrete play-by-play raid events (103,176 entries).
    """
    df = _load_df("raids_pbp/raids_pbp", format_pref, data_dir)
    if season is not None:
        if isinstance(season, int):
            df = df[df["season_id"] == season]
        elif isinstance(season, (list, tuple, set)):
            df = df[df["season_id"].isin(season)]
    if match_id is not None:
        df = df[df["match_id"] == match_id]
    return df.reset_index(drop=True)


def get_splits_info(data_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Load the official benchmark split configuration dictionary."""
    base = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    splits_path = base / "benchmark_splits" / "splits.json"
    with open(splits_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_benchmark_split(
    task: str = "matches",
    format_pref: str = "parquet",
    data_dir: Optional[Path] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Retrieves the strictly leakage-free train, validation, and test sets.
    Split Protocol:
      - Train: Seasons 1-8 (2014-2022) [786 matches]
      - Validation: Season 9 (2022)     [137 matches]
      - Test: Season 10 (2023-2024)     [136 matches]

    Supported tasks:
      - 'matches': Returns (train_matches, val_matches, test_matches)
      - 'raids': Returns (train_raids, val_raids, test_raids)
      - 'player_matches': Returns (train_pm, val_pm, test_pm)
    """
    splits_info = get_splits_info(data_dir)
    train_ids = set(splits_info["train"]["match_ids"])
    val_ids = set(splits_info["validation"]["match_ids"])
    test_ids = set(splits_info["test"]["match_ids"])

    if task == "matches":
        df = load_matches(format_pref=format_pref, data_dir=data_dir)
    elif task in ("raids", "raid_outcome", "win_probability"):
        df = load_raids(format_pref=format_pref, data_dir=data_dir)
    elif task == "player_matches":
        df = load_player_matches(format_pref=format_pref, data_dir=data_dir)
    else:
        raise ValueError(f"Unknown task: {task}. Choose from 'matches', 'raids', 'player_matches'.")

    train_df = df[df["match_id"].isin(train_ids)].reset_index(drop=True)
    val_df = df[df["match_id"].isin(val_ids)].reset_index(drop=True)
    test_df = df[df["match_id"].isin(test_ids)].reset_index(drop=True)

    return train_df, val_df, test_df
