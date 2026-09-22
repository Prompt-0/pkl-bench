"""
Benchmark Task 3: Pre-Match Outcome & Margin Forecasting
Dynamic Elo rating system tailored to Kabaddi scoring dynamics with margin-of-victory scaling.
"""

from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score, mean_absolute_error
from ..loader import load_matches, get_benchmark_split, load_teams
from ..metrics import brier_score


class KabaddiEloBaseline:
    """
    Dynamic sequential Elo rating engine for Pro Kabaddi League.
    Features:
      - Initial rating: 1500
      - Margin-of-victory multiplier: log(1 + margin)
      - Inter-season regression to mean: 20%
    """
    def __init__(self, k_factor: float = 32.0, home_advantage: float = 25.0, mean_reversion: float = 0.20):
        self.k_factor = k_factor
        self.home_advantage = home_advantage
        self.mean_reversion = mean_reversion
        self.ratings: Dict[int, float] = {}
        self.history: List[Dict[str, Any]] = []

    def get_rating(self, team_id: int) -> float:
        return self.ratings.get(team_id, 1500.0)

    def reset_season(self):
        """Regresses ratings toward the 1500 mean between seasons."""
        for tid in self.ratings:
            self.ratings[tid] = (1 - self.mean_reversion) * self.ratings[tid] + self.mean_reversion * 1500.0

    def predict_match(self, team1_id: int, team2_id: int, is_home: bool = True) -> Tuple[float, float]:
        """
        Returns (p_team1_win, predicted_spread).
        """
        r1 = self.get_rating(team1_id) + (self.home_advantage if is_home else 0.0)
        r2 = self.get_rating(team2_id)
        diff = r1 - r2
        p1 = 1.0 / (1.0 + 10.0 ** (-diff / 400.0))
        predicted_margin = diff / 25.0  # Approx 25 Elo points per 1 kabaddi point
        return p1, predicted_margin

    def update_match(self, team1_id: int, team2_id: int, team1_score: int, team2_score: int, is_home: bool = True):
        p1, _ = self.predict_match(team1_id, team2_id, is_home=is_home)

        if team1_score > team2_score:
            s1 = 1.0
        elif team1_score == team2_score:
            s1 = 0.5
        else:
            s1 = 0.0

        margin = abs(team1_score - team2_score)
        mov_mult = np.log2(1.0 + max(1, margin))
        k = self.k_factor * mov_mult

        delta = k * (s1 - p1)
        self.ratings[team1_id] = self.get_rating(team1_id) + delta
        self.ratings[team2_id] = self.get_rating(team2_id) - delta


def run_match_winner_benchmark() -> Dict[str, Any]:
    """
    Evaluates dynamic Elo rating system on PKL benchmark splits.
    Train: S1-S8 sequential warmup
    Val: S9 evaluation
    Test: S10 evaluation
    """
    df_matches = load_matches().sort_values(["season_id", "match_id"]).reset_index(drop=True)
    elo = KabaddiEloBaseline(k_factor=30.0, home_advantage=20.0, mean_reversion=0.15)

    current_season = None
    y_val_true, y_val_prob, y_val_margin_true, y_val_margin_pred = [], [], [], []
    y_test_true, y_test_prob, y_test_margin_true, y_test_margin_pred = [], [], [], []

    for _, row in df_matches.iterrows():
        sid = row["season_id"]
        if current_season is not None and sid != current_season:
            elo.reset_season()
        current_season = sid

        t1 = row["team1_id"]
        t2 = row["team2_id"]
        s1 = row["team1_score"]
        s2 = row["team2_score"]
        actual_margin = s1 - s2
        t1_won = 1 if s1 > s2 else 0

        p1, pred_margin = elo.predict_match(t1, t2)

        if sid == 9:
            y_val_true.append(t1_won)
            y_val_prob.append(p1)
            y_val_margin_true.append(actual_margin)
            y_val_margin_pred.append(pred_margin)
        elif sid == 10:
            y_test_true.append(t1_won)
            y_test_prob.append(p1)
            y_test_margin_true.append(actual_margin)
            y_test_margin_pred.append(pred_margin)

        elo.update_match(t1, t2, s1, s2)

    def calc_metrics(y_true, y_prob, m_true, m_pred):
        y_pred_cls = [1 if p >= 0.5 else 0 for p in y_prob]
        acc = accuracy_score(y_true, y_pred_cls)
        bs = brier_score(y_true, y_prob)
        auc = roc_auc_score(y_true, y_prob) if len(set(y_true)) > 1 else 0.5
        mae = mean_absolute_error(m_true, m_pred)
        return {
            "accuracy": float(acc),
            "brier_score": float(bs),
            "roc_auc": float(auc),
            "margin_mae": float(mae),
            "matches_evaluated": len(y_true)
        }

    return {
        "model": "Dynamic_Kabaddi_Elo",
        "validation_s9": calc_metrics(y_val_true, y_val_prob, y_val_margin_true, y_val_margin_pred),
        "test_s10": calc_metrics(y_test_true, y_test_prob, y_test_margin_true, y_test_margin_pred),
        "final_ratings": {t: round(r, 1) for t, r in sorted(elo.ratings.items(), key=lambda x: x[1], reverse=True)}
    }
