"""
Benchmark Task 2: Dynamic In-Game Win Probability Modeling
Predicts P(Team 1 Wins | Match State at raid t) throughout the course of a 40-minute contest.
"""

from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from ..loader import get_benchmark_split, load_matches
from ..metrics import brier_score, expected_calibration_error, multiclass_log_loss


def prepare_win_prob_features(df_raids: pd.DataFrame, df_matches: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    Pairs each raid state with final match outcome.
    Features:
      1. score_diff: team1_score_after - team2_score_after
      2. seconds_remaining: total match seconds left (0 to 2400)
      3. half: 1 or 2
      4. scaled_leverage: score_diff / sqrt(seconds_remaining + 1)
      5. possession: 1 if team1 is raiding, 0 otherwise
    Target:
      1 if team1 won the match, 0 if team1 lost or tied
    """
    # Match winner mapping: match_id -> team1_won (1 or 0)
    match_winner_map = {}
    team1_map = {}
    for _, row in df_matches.iterrows():
        mid = row["match_id"]
        t1 = row["team1_id"]
        team1_map[mid] = t1
        match_winner_map[mid] = 1 if row["winner_id"] == t1 else 0

    valid_mask = df_raids["match_id"].isin(match_winner_map)
    df_valid = df_raids[valid_mask].copy()

    mids = df_valid["match_id"].values
    t1_ids = np.array([team1_map[m] for m in mids])
    targets = np.array([match_winner_map[m] for m in mids])

    score_diff = (df_valid["team1_score_after"] - df_valid["team2_score_after"]).fillna(0).values
    sec_left = df_valid["clock_seconds_remaining"].fillna(1200).values
    half = df_valid["half"].values
    leverage = score_diff / np.sqrt(sec_left + 1.0)
    possession = (df_valid["raiding_team_id"].values == t1_ids).astype(float)

    X = np.column_stack([
        score_diff,
        sec_left,
        half,
        leverage,
        possession
    ])
    return X, targets


class WinProbabilityBaseline:
    def __init__(self, model_type: str = "calibrated_gbdt"):
        self.model_type = model_type
        if model_type == "logistic_leverage":
            self.model = LogisticRegression(max_iter=1000)
        elif model_type == "calibrated_gbdt":
            base_gb = HistGradientBoostingClassifier(max_iter=100, learning_rate=0.08, random_state=42)
            self.model = CalibratedClassifierCV(estimator=base_gb, method="sigmoid", cv=3)
        else:
            raise ValueError(f"Unknown model_type: {model_type}")

    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        if self.model_type == "logistic_leverage":
            # Use single scaled leverage feature for interpretable physics-based baseline
            self.model.fit(X_train[:, [3]], y_train)
        else:
            self.model.fit(X_train, y_train)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.model_type == "logistic_leverage":
            return self.model.predict_proba(X[:, [3]])[:, 1]
        return self.model.predict_proba(X)[:, 1]

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        p_win = self.predict_proba(X_test)
        bs = brier_score(y_test, p_win)
        ece = expected_calibration_error(y_test, p_win, n_bins=10)

        # Binary cross entropy
        eps = 1e-15
        p_clipped = np.clip(p_win, eps, 1 - eps)
        logloss = -float(np.mean(y_test * np.log(p_clipped) + (1 - y_test) * np.log(1 - p_clipped)))

        return {
            "model_type": self.model_type,
            "brier_score": bs,
            "expected_calibration_error": ece,
            "log_loss": logloss,
            "sample_count": len(y_test)
        }


def run_win_probability_benchmark(model_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Executes the standard Task 2 benchmark on official train/val/test splits.
    """
    if model_types is None:
        model_types = ["logistic_leverage", "calibrated_gbdt"]

    train_raids, val_raids, test_raids = get_benchmark_split(task="raids")
    df_matches = load_matches()

    X_train, y_train = prepare_win_prob_features(train_raids, df_matches)
    X_val, y_val = prepare_win_prob_features(val_raids, df_matches)
    X_test, y_test = prepare_win_prob_features(test_raids, df_matches)

    results = {
        "train_samples": len(X_train),
        "val_samples": len(X_val),
        "test_samples": len(X_test),
        "validation_evaluations": {},
        "test_evaluations": {}
    }

    for m in model_types:
        baseline = WinProbabilityBaseline(model_type=m)
        baseline.fit(X_train, y_train)

        val_eval = baseline.evaluate(X_val, y_val)
        test_eval = baseline.evaluate(X_test, y_test)

        results["validation_evaluations"][m] = val_eval
        results["test_evaluations"][m] = test_eval

    return results
