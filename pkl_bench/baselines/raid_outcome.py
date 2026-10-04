"""
Benchmark Task 1: Discrete Raid Outcome Prediction
Given pre-raid game state (clock, half, do-or-die flag, score difference, team matchup),
predict the multi-class outcome distribution:
{EMPTY_RAID, SUCCESSFUL_RAID, UNSUCCESSFUL_RAID, SUPER_RAID, SUPER_TACKLE}
"""

from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from ..loader import get_benchmark_split
from ..metrics import classification_report_dict, multiclass_log_loss

TARGET_CLASSES = ["EMPTY_RAID", "SUCCESSFUL_RAID", "UNSUCCESSFUL_RAID", "SUPER_RAID", "SUPER_TACKLE"]


def prepare_raid_features(
    df_raids: pd.DataFrame,
    df_matches: Optional[pd.DataFrame] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extracts numerical feature matrix X and categorical target vector y.
    Features:
      1. is_do_or_die (0 or 1)
      2. clock_seconds_remaining (0 to 2400)
      3. half (1 or 2)
      4. score_diff (relative to raiding team: score_raiding - score_defending)
    """
    # Clean targets
    valid_mask = df_raids["outcome_category"].isin(TARGET_CLASSES)
    df_clean = df_raids[valid_mask].copy()

    if df_matches is None:
        from ..loader import load_matches
        df_matches = load_matches()

    m_sub = df_matches[["match_id", "team1_id", "team2_id"]].drop_duplicates()
    df_merged = df_clean.merge(m_sub, on="match_id", how="left")

    # True score differential from perspective of raiding team
    is_t1 = (df_merged["raiding_team_id"] == df_merged["team1_id"])
    score_diff = np.where(
        is_t1,
        df_merged["team1_score_before"] - df_merged["team2_score_before"],
        df_merged["team2_score_before"] - df_merged["team1_score_before"],
    )
    score_diff_clean = np.nan_to_num(score_diff, nan=0.0)

    features = np.column_stack([
        df_clean["is_do_or_die"].astype(float).values,
        df_clean["clock_seconds_remaining"].fillna(1200).values,
        df_clean["half"].values,
        score_diff_clean
    ])

    targets = df_clean["outcome_category"].values
    return features, targets


class RaidOutcomeBaseline:
    def __init__(self, model_type: str = "gradient_boosting"):
        self.model_type = model_type
        self.scaler = StandardScaler()
        if model_type == "majority":
            self.model = DummyClassifier(strategy="most_frequent")
        elif model_type == "logistic_regression":
            self.model = LogisticRegression(max_iter=1000, solver="lbfgs")
        elif model_type == "gradient_boosting":
            self.model = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=42)
        else:
            raise ValueError(f"Unknown model_type: {model_type}")

    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        preds = self.predict(X_test)
        probs = self.predict_proba(X_test)

        # Classes in model
        classes = list(self.model.classes_)
        # Re-index probs to match TARGET_CLASSES
        prob_matrix = np.zeros((len(X_test), len(TARGET_CLASSES)))
        for idx, cls in enumerate(classes):
            if cls in TARGET_CLASSES:
                target_idx = TARGET_CLASSES.index(cls)
                prob_matrix[:, target_idx] = probs[:, idx]

        report = classification_report_dict(y_test, preds)
        # Log loss over present classes
        try:
            ll = multiclass_log_loss(y_test, probs, labels=classes)
        except Exception:
            ll = float("nan")

        return {
            "model_type": self.model_type,
            "accuracy": report["accuracy"],
            "macro_f1": report["macro_f1"],
            "weighted_f1": report["weighted_f1"],
            "log_loss": ll,
            "classes": classes
        }


def run_raid_outcome_benchmark(model_types: Optional[list] = None) -> Dict[str, Any]:
    """
    Executes the standard Task 1 benchmark across models on official train/val/test splits.
    """
    if model_types is None:
        model_types = ["majority", "logistic_regression", "gradient_boosting"]

    train_df, val_df, test_df = get_benchmark_split(task="raids")

    X_train, y_train = prepare_raid_features(train_df)
    X_val, y_val = prepare_raid_features(val_df)
    X_test, y_test = prepare_raid_features(test_df)

    results: Dict[str, Any] = {
        "train_samples": len(X_train),
        "val_samples": len(X_val),
        "test_samples": len(X_test),
        "validation_evaluations": {},
        "test_evaluations": {}
    }

    for m in model_types:
        baseline = RaidOutcomeBaseline(model_type=m)
        baseline.fit(X_train, y_train)

        val_eval = baseline.evaluate(X_val, y_val)
        test_eval = baseline.evaluate(X_test, y_test)

        results["validation_evaluations"][m] = val_eval
        results["test_evaluations"][m] = test_eval

    return results
