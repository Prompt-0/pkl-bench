"""
Benchmark Task 1: Discrete Raid Outcome Prediction
Given pre-raid game state (clock, half, do-or-die flag, score difference, team matchup),
predict the multi-class outcome distribution:
{EMPTY_RAID, SUCCESSFUL_RAID, UNSUCCESSFUL_RAID, SUPER_RAID, SUPER_TACKLE}
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import StandardScaler
from ..loader import get_benchmark_split
from ..metrics import multiclass_log_loss, classification_report_dict, brier_score


TARGET_CLASSES = ["EMPTY_RAID", "SUCCESSFUL_RAID", "UNSUCCESSFUL_RAID", "SUPER_RAID", "SUPER_TACKLE"]


def prepare_raid_features(df_raids: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extracts numerical feature matrix X and categorical target vector y.
    Features:
      1. is_do_or_die (0 or 1)
      2. clock_seconds_remaining (0 to 2400)
      3. half (1 or 2)
      4. score_diff (relative to raiding team: score_raiding - score_defending)
      5. raiding_team_id
      6. defending_team_id
    """
    # Clean targets
    valid_mask = df_raids["outcome_category"].isin(TARGET_CLASSES)
    df_clean = df_raids[valid_mask].copy()

    # Score diff approx:
    # If raiding team is team1, score_diff = team1_score_after - team2_score_after
    score_diff = df_clean["team1_score_after"] - df_clean["team2_score_after"]
    # Adjust sign if raiding team is team2
    is_team2 = (df_clean["raiding_team_id"] != df_clean["defending_team_id"]) & (df_clean["raiding_team_id"] > 10)
    score_diff = np.where(is_team2, -score_diff, score_diff)

    score_diff_clean = np.nan_to_num(score_diff, nan=0.0)

    features = np.column_stack([
        df_clean["is_do_or_die"].astype(float).values,
        df_clean["clock_seconds_remaining"].fillna(1200).values,
        df_clean["half"].values,
        score_diff_clean,
        df_clean["raiding_team_id"].values,
        df_clean["defending_team_id"].values
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

    results = {
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
