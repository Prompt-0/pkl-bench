"""
Command-Line Interface (CLI) for PKL-Bench.
"""

import sys
import argparse
import json
import pprint
from .validator import validate_dataset_integrity, audit_score_conservation
from .baselines import (
    run_raid_outcome_benchmark,
    run_win_probability_benchmark,
    run_match_winner_benchmark,
    calculate_player_impact_metrics
)
from .loader import load_matches, load_raids, load_players


def main():
    parser = argparse.ArgumentParser(
        prog="pkl-bench",
        description="PKL-Bench: Pro Kabaddi League Benchmark Dataset & Analytics Suite"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # info
    info_p = subparsers.add_parser("info", help="Display dataset overview and tier statistics")

    # validate
    val_p = subparsers.add_parser("validate", help="Run full data integrity and score conservation audits")

    # benchmark
    bench_p = subparsers.add_parser("benchmark", help="Execute standard machine learning benchmark baselines")
    bench_p.add_argument(
        "--task",
        choices=["raid_outcome", "win_probability", "match_winner", "all"],
        default="all",
        help="Benchmark task to run"
    )

    args = parser.parse_args()

    if args.command == "info" or args.command is None:
        print("=" * 65)
        print("PKL-BENCH: PRO KABADDI LEAGUE RESEARCH DATASET")
        print("=" * 65)
        matches = load_matches()
        raids = load_raids()
        players = load_players()
        print(f"Total Seasons:      10 (2014 - 2024)")
        print(f"Total Matches:      {len(matches):,}")
        print(f"Total Raid Events:  {len(raids):,}")
        print(f"Unique Players:     {len(players):,}")
        print(f"Standard Splits:    Train: Seasons 1-8 | Val: Season 9 | Test: Season 10")
        print("=" * 65)

    elif args.command == "validate":
        print("Running comprehensive dataset integrity suite...")
        res = validate_dataset_integrity()
        passed = res.get("overall_validation_passed", False)
        print(f"Integrity Validation Status: {'PASSED [100%]' if passed else 'FAILED'}")
        print("\nPrimary Key Checks:")
        for k, v in res["primary_key_uniqueness"].items():
            print(f"  {k:25s}: {'PASS' if v else 'FAIL'}")
        print("\nForeign Key Checks:")
        for k, v in res["foreign_key_integrity"].items():
            print(f"  {k:35s}: {'PASS' if v else 'FAIL'}")
        print("\nScore Conservation Audit:")
        sc = res["score_conservation"]
        print(f"  Matches Audited:          {sc['matches_evaluated']}")
        print(f"  Team 1 Conservation Pass: {sc['team1_conservation_pass_rate_pct']}%")
        print(f"  Team 2 Conservation Pass: {sc['team2_conservation_pass_rate_pct']}%")
        print(f"  Discrepancies Flagged:    {sc['total_discrepancies_flagged']}")

    elif args.command == "benchmark":
        task = args.task
        print(f"Executing Benchmark Task: {task.upper()}...")

        if task in ("raid_outcome", "all"):
            print("\n" + "-" * 50)
            print("TASK 1: DISCRETE RAID OUTCOME PREDICTION")
            print("-" * 50)
            res_raid = run_raid_outcome_benchmark()
            print("Validation (Season 9) Results:")
            for m, r in res_raid["validation_evaluations"].items():
                print(f"  {m:25s} | Acc: {r['accuracy']:.4f} | Macro-F1: {r['macro_f1']:.4f} | LogLoss: {r['log_loss']:.4f}")
            print("\nTest (Season 10) Out-of-Sample Results:")
            for m, r in res_raid["test_evaluations"].items():
                print(f"  {m:25s} | Acc: {r['accuracy']:.4f} | Macro-F1: {r['macro_f1']:.4f} | LogLoss: {r['log_loss']:.4f}")

        if task in ("win_probability", "all"):
            print("\n" + "-" * 50)
            print("TASK 2: DYNAMIC IN-GAME WIN PROBABILITY MODELING")
            print("-" * 50)
            res_wp = run_win_probability_benchmark()
            print("Validation (Season 9) Results:")
            for m, r in res_wp["validation_evaluations"].items():
                print(f"  {m:25s} | Brier Score: {r['brier_score']:.4f} | ECE: {r['expected_calibration_error']:.4f} | LogLoss: {r['log_loss']:.4f}")
            print("\nTest (Season 10) Out-of-Sample Results:")
            for m, r in res_wp["test_evaluations"].items():
                print(f"  {m:25s} | Brier Score: {r['brier_score']:.4f} | ECE: {r['expected_calibration_error']:.4f} | LogLoss: {r['log_loss']:.4f}")

        if task in ("match_winner", "all"):
            print("\n" + "-" * 50)
            print("TASK 3: PRE-MATCH OUTCOME & SPREAD FORECASTING")
            print("-" * 50)
            res_mw = run_match_winner_benchmark()
            print(f"Model: {res_mw['model']}")
            val_m = res_mw["validation_s9"]
            test_m = res_mw["test_s10"]
            print(f"  Val (S9):  Acc: {val_m['accuracy']:.4f} | Brier: {val_m['brier_score']:.4f} | ROC-AUC: {val_m['roc_auc']:.4f} | Margin MAE: {val_m['margin_mae']:.2f}")
            print(f"  Test (S10): Acc: {test_m['accuracy']:.4f} | Brier: {test_m['brier_score']:.4f} | ROC-AUC: {test_m['roc_auc']:.4f} | Margin MAE: {test_m['margin_mae']:.2f}")


if __name__ == "__main__":
    main()
