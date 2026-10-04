import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Add parent directory to path to import pkl_bench
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pkl_bench as pb
from pkl_bench.baselines.match_winner import KabaddiEloBaseline
from pkl_bench.baselines.win_probability import WinProbabilityBaseline, prepare_win_prob_features
from pkl_bench.loader import get_benchmark_split

FIGURES_DIR = Path(__file__).resolve().parent.parent / "paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def plot_phase_transitions(df_raids: pd.DataFrame):
    print("Generating Figure 1: Empirical Phase Transitions...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    outcomes = df_raids["outcome_category"].value_counts(normalize=True) * 100
    colors = ["#4A90E2", "#7ED321", "#D0021B", "#F5A623", "#9013FE", "#50E3C2"]

    # Take top 5 to match the 5 classes
    outcomes = outcomes.head(5)

    ax1.bar(outcomes.index.astype(str), outcomes.values, color=colors[:len(outcomes)], edgecolor="black", alpha=0.85)
    ax1.set_ylabel("Percentage of Total Raids (%)")
    ax1.set_title(f"Raid Outcome Distribution (N={len(df_raids):,})")
    ax1.set_xticks(range(len(outcomes)))
    ax1.set_xticklabels(outcomes.index.astype(str), rotation=25, ha="right", fontsize=9)
    ax1.set_ylim(0, max(outcomes.values) * 1.15)

    for i, v in enumerate(outcomes.values):
        ax1.text(i, v + 1, f"{v:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Empirical data for Phase Transitions
    # Calculate strike rate per defender count
    # Defender count is NOT explicitly in df_raids but we can approximate it or use empty/success.
    # The reviewer said: "The dataset has no defender-count column at all."
    # Since defender_count isn't explicitly recorded cleanly, we will plot Super Tackle rate by half or something,
    # OR we can just plot the clock vs raid success rate (which IS empirical).

    # Let's plot Raid Success Rate over time (Clock)
    df_clean = df_raids[df_raids["clock_seconds_remaining"].notna()].copy()
    df_clean["minute_bin"] = (2400 - df_clean["clock_seconds_remaining"]) // 120
    df_clean["is_success"] = df_clean["outcome_category"].isin(["SUCCESSFUL_RAID", "SUPER_RAID"])

    minute_stats = df_clean.groupby("minute_bin")["is_success"].mean() * 100

    ax2.plot(minute_stats.index * 2, minute_stats.values, "o-", color="#D0021B", linewidth=2.2, markersize=7)
    ax2.set_xlabel("Elapsed Match Time (Minutes)")
    ax2.set_ylabel("Raid Success Rate (%)")
    ax2.set_title("Empirical Raid Success over Match Duration")
    ax2.set_ylim(0, 100)
    ax2.axvline(20, color="gray", linestyle="--", alpha=0.4, label="Half-Time")
    ax2.legend()

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig1_phase_transitions.pdf")
    plt.close(fig)
    print("  ✓ Saved fig1_phase_transitions (.pdf)")


def plot_win_prob_calibration():
    print("Generating Figure 2: Win Probability Calibration...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    train_raids, val_raids, test_raids = get_benchmark_split(task="raids")
    df_matches = pb.load_matches()

    X_train, y_train = prepare_win_prob_features(train_raids, df_matches)
    X_test, y_test = prepare_win_prob_features(test_raids, df_matches)

    # Train actual models
    gbdt = WinProbabilityBaseline(model_type="calibrated_gbdt").fit(X_train, y_train)
    logistic = WinProbabilityBaseline(model_type="logistic_leverage").fit(X_train, y_train)

    p_gbdt = gbdt.predict_proba(X_test)
    p_log = logistic.predict_proba(X_test)

    # Calculate empirical calibration
    from sklearn.calibration import calibration_curve
    prob_true_gb, prob_pred_gb = calibration_curve(y_test, p_gbdt, n_bins=10)
    prob_true_log, prob_pred_log = calibration_curve(y_test, p_log, n_bins=10)

    ax1.plot([0, 1], [0, 1], "k--", alpha=0.7, label="Perfect Calibration")
    ax1.plot(prob_pred_gb, prob_true_gb, "s-", color="#4A90E2", linewidth=2, label="Calibrated GBDT")
    ax1.plot(prob_pred_log, prob_true_log, "^-", color="#F5A623", linewidth=1.8, label="Logistic Leverage")

    ax1.set_xlabel("Mean Predicted Probability")
    ax1.set_ylabel("Observed Fraction of Positives")
    ax1.set_title("Task 2: Win Probability Calibration (Test S10)")
    ax1.legend(loc="upper left")
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    # Sample Match Win Probability Trajectories
    # Find a close match and a blowout in test_raids
    match_ids = test_raids["match_id"].unique()
    # Pick a random match, just get the real features and plot
    if len(match_ids) > 2:
        m_close = match_ids[10]
        m_blowout = match_ids[20]

        for m_id, label, color in [(m_close, "Match A", "#E94E77"), (m_blowout, "Match B", "#50E3C2")]:
            m_df = test_raids[test_raids["match_id"] == m_id].copy()
            X_m, _ = prepare_win_prob_features(m_df, df_matches)
            if len(X_m) > 0:
                p_m = gbdt.predict_proba(X_m)
                time_elapsed = 40 - (X_m[:, 1] / 60) # X_m[:, 1] is seconds remaining
                ax2.plot(time_elapsed, p_m, color=color, linewidth=2.2, label=label)

    ax2.axhline(0.5, color="gray", linestyle=":", alpha=0.6)
    ax2.axvline(20, color="gray", linestyle="--", alpha=0.4, label="Half-Time")
    ax2.set_xlabel("Match Elapsed Time (Minutes)")
    ax2.set_ylabel("P(Team 1 Wins)")
    ax2.set_title("Real-Time Win Probability Trajectories")
    ax2.legend(loc="lower right", fontsize=9)
    ax2.set_xlim(0, 40)
    ax2.set_ylim(0, 1.05)

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig2_win_prob_calibration.pdf")
    plt.close(fig)
    print("  ✓ Saved fig2_win_prob_calibration (.pdf)")


def plot_elo_franchises(df_matches: pd.DataFrame):
    print("Generating Figure 3: Dynamic Elo Ratings...")
    fig, ax = plt.subplots(figsize=(10, 5))

    elo_baseline = KabaddiEloBaseline(k_factor=30.0, home_advantage=20.0, mean_reversion=0.15)
    history = {tid: [] for tid in [1, 2, 3, 5, 6, 7]}  # BLR, DEL, JAI, MUM, PAT, PUN
    match_indices = []

    current_season = None
    sorted_matches = df_matches.sort_values(["season_id", "match_id"]).reset_index(drop=True)

    for idx, row in sorted_matches.iterrows():
        sid = getattr(row, "season_id")
        if current_season is not None and sid != current_season:
            elo_baseline.reset_season()
        current_season = sid

        elo_baseline.update_match(getattr(row, "team1_id"), getattr(row, "team2_id"), getattr(row, "team1_score"), getattr(row, "team2_score"))

        if idx % 10 == 0:
            match_indices.append(idx)
            for tid in history:
                history[tid].append(elo_baseline.get_rating(tid))

    team_meta = {
        1: ("Bengaluru Bulls", "#D0021B", "-"),
        2: ("Dabang Delhi K.C.", "#4A90E2", "-"),
        3: ("Jaipur Pink Panthers", "#E94E77", "-"),
        5: ("U Mumba", "#F5A623", "--"),
        6: ("Patna Pirates", "#7ED321", "-"),
        7: ("Puneri Paltan", "#9013FE", "-"),
    }

    for tid, (tname, color, style) in team_meta.items():
        ax.plot(match_indices, history[tid], label=tname, color=color, linestyle=style, linewidth=1.8, alpha=0.9)

    ax.axhline(1500, color="gray", linestyle=":", alpha=0.5, label="Baseline (1500)")
    ax.set_xlabel("Match Sequence (Seasons 1 through 10, N=1,060)")
    ax.set_ylabel("Dynamic Kabaddi Elo Rating")
    ax.set_title("Franchise Trajectories Across 10 Seasons of the Pro Kabaddi League")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", framealpha=0.9)

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig3_elo_trajectories.pdf")
    plt.close(fig)
    print("  ✓ Saved fig3_elo_trajectories (.pdf)")


def plot_score_distributions(df_matches: pd.DataFrame):
    print("Generating Figure 4: Score Distributions...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    total_points = df_matches["team1_score"] + df_matches["team2_score"]
    margins = df_matches["score_margin"]

    ax1.hist(total_points, bins=30, color="#4A90E2", edgecolor="black", alpha=0.75)
    mean_pts = total_points.mean()
    median_pts = total_points.median()
    ax1.axvline(mean_pts, color="red", linestyle="--", linewidth=1.8, label=f"Mean: {mean_pts:.1f} pts")
    ax1.axvline(median_pts, color="orange", linestyle=":", linewidth=1.8, label=f"Median: {median_pts:.1f} pts")
    ax1.set_xlabel("Combined Match Points (Team 1 + Team 2)")
    ax1.set_ylabel("Match Count")
    ax1.set_title("Total Scoring Distribution Across 1,060 Matches")
    ax1.legend(loc="upper right")

    ax2.hist(margins, bins=25, color="#7ED321", edgecolor="black", alpha=0.75)
    pct_close = (margins <= 5).mean() * 100
    ax2.axvline(5.5, color="red", linestyle="--", linewidth=1.8, label=f"≤ 5 Pts Diff ({pct_close:.1f}%)")
    ax2.set_xlabel("Point Differential (|Team 1 - Team 2|)")
    ax2.set_ylabel("Match Count")
    ax2.set_title("Margin of Victory Distribution")
    ax2.legend(loc="upper right")

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "fig4_score_and_raid_distributions.pdf")
    plt.close(fig)
    print("  ✓ Saved fig4_score_and_raid_distributions (.pdf)")


def main():
    print("GENERATING RESEARCH PAPER PUBLICATION FIGURES (REAL DATA)")
    df_matches = pb.load_matches()
    df_raids = pb.load_raids()

    plot_phase_transitions(df_raids)
    plot_win_prob_calibration()
    plot_elo_franchises(df_matches)
    plot_score_distributions(df_matches)
    print("\n✓ All publication figures generated successfully!")


if __name__ == "__main__":
    main()
