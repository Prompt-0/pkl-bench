#!/usr/bin/env python3
"""
PKL-Bench: 30-Second Quickstart Demonstration
Loads data, inspects splits, and evaluates a baseline model in under 15 lines of code.
"""

import pkl_bench as pb

def main():
    print("=== 1. Loading Datasets ===")
    matches = pb.load_matches()
    raids = pb.load_raids()
    players = pb.load_players()

    print(f"Loaded {len(matches):,} matches across {matches['season_id'].nunique()} seasons.")
    print(f"Loaded {len(raids):,} discrete raid events.")
    print(f"Loaded {len(players):,} registered professional athletes.")

    print("\n=== 2. Auditing Score Conservation Law ===")
    audit = pb.audit_score_conservation(matches)
    print(f"Mathematical Conservation Adherence: {audit['team1_conservation_pass_rate_pct']}%")

    print("\n=== 3. Loading Official Benchmark Splits ===")
    train_raids, val_raids, test_raids = pb.get_benchmark_split(task="raids")
    print(f"Train Raids (S1-S8): {len(train_raids):,}")
    print(f"Val Raids (S9):      {len(val_raids):,}")
    print(f"Test Raids (S10):    {len(test_raids):,}")

    print("\n=== 4. Running Raid Outcome Baseline (HistGradientBoosting) ===")
    from pkl_bench.baselines.raid_outcome import RaidOutcomeBaseline, prepare_raid_features
    
    X_train, y_train = prepare_raid_features(train_raids)
    X_test, y_test = prepare_raid_features(test_raids)

    model = RaidOutcomeBaseline(model_type="gradient_boosting")
    model.fit(X_train, y_train)
    eval_res = model.evaluate(X_test, y_test)

    print(f"Test Accuracy: {eval_res['accuracy']:.4f}")
    print(f"Test Macro-F1: {eval_res['macro_f1']:.4f}")
    print(f"Test Log-Loss: {eval_res['log_loss']:.4f}")

    print("\n✓ PKL-Bench Quickstart completed successfully!")

if __name__ == "__main__":
    main()
