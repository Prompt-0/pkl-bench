"""
Tests for baseline model execution and reproducible benchmark runs.
"""

import pytest
import numpy as np
from pkl_bench.baselines.raid_outcome import RaidOutcomeBaseline
from pkl_bench.baselines.win_probability import WinProbabilityBaseline
from pkl_bench.baselines.match_winner import KabaddiEloBaseline


def test_raid_outcome_baseline():
    X_dummy = np.random.randn(50, 6)
    y_dummy = np.random.choice(["EMPTY_RAID", "SUCCESSFUL_RAID", "UNSUCCESSFUL_RAID"], size=50)

    model = RaidOutcomeBaseline(model_type="majority")
    model.fit(X_dummy, y_dummy)
    preds = model.predict(X_dummy)
    assert len(preds) == 50

    eval_dict = model.evaluate(X_dummy, y_dummy)
    assert "accuracy" in eval_dict
    assert "log_loss" in eval_dict


def test_win_probability_baseline():
    X_dummy = np.column_stack([
        np.random.randint(-15, 15, size=60),
        np.random.randint(10, 2400, size=60),
        np.random.choice([1, 2], size=60),
        np.random.randn(60),
        np.random.choice([0, 1], size=60),
    ])
    y_dummy = np.random.choice([0, 1], size=60)

    wp_model = WinProbabilityBaseline(model_type="logistic_leverage")
    wp_model.fit(X_dummy, y_dummy)
    probs = wp_model.predict_proba(X_dummy)
    assert len(probs) == 60
    assert (probs >= 0.0).all() and (probs <= 1.0).all()


def test_kabaddi_elo():
    elo = KabaddiEloBaseline(k_factor=30.0)
    # Team 1 beats Team 2 by 10 points
    p1_initial, _ = elo.predict_match(1, 2)
    assert p1_initial > 0.45 and p1_initial < 0.65

    elo.update_match(1, 2, team1_score=35, team2_score=25)
    r1_after = elo.get_rating(1)
    r2_after = elo.get_rating(2)
    assert r1_after > 1500.0
    assert r2_after < 1500.0
