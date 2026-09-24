# PKL-Bench: The Pro Kabaddi League Research Benchmark Dataset

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Data Format: Parquet & CSV](https://img.shields.io/badge/Format-Parquet%20%7C%20CSV-green.svg)](https://frictionlessdata.io/)
[![Dataset Tests: 16/16 Passed](https://img.shields.io/badge/Tests-16%2F16%20Passed-brightgreen.svg)]()
[![Matches: 1060](https://img.shields.io/badge/Matches-1%2C060-orange.svg)]()
[![Raids: 103k](https://img.shields.io/badge/Raid%20Events-103%2C176-red.svg)]()

**PKL-Bench** is the definitive, research-grade, multi-tier benchmark dataset and evaluation harness for professional Kabaddi analytics and machine learning. Covering **10 complete seasons** (2014–2024) of the **Pro Kabaddi League (PKL)**, PKL-Bench provides **1,060 matches**, **26,760 individual player boxscores**, and **103,176 granular, timestamped play-by-play raid events**.

Engineered according to FAIR principles (Findable, Accessible, Interoperable, Reusable), PKL-Bench includes formal [Datasheets for Datasets](docs/DATASHEET.md), a [Mathematical Methodology Guide](docs/METHODOLOGY.md), a [Domain Guide](docs/KABADDI_DOMAIN_GUIDE.md), and strict **leakage-free temporal splits** with verified baselines.

---

## ⚡ Quickstart

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/Prompt-0/pkl-bench.git
cd pkl-bench

# Install package and dependencies
pip install -e .
```

### 2. Python API (3-Line Data Loading)
```python
import pkl_bench as pb

# Load all 10 seasons of play-by-play raid events
raids_df = pb.load_raids()

# Load official leakage-free benchmark splits
train_raids, val_raids, test_raids = pb.get_benchmark_split(task="raids")
print(f"Train: {len(train_raids):,} | Val: {len(val_raids):,} | Test: {len(test_raids):,}")
```

### 3. Command-Line Interface (CLI)
```bash
# Display dataset tier statistics
pkl-bench info

# Run automated score conservation and integrity validation
pkl-bench validate

# Run official benchmark baselines
pkl-bench benchmark --task all
```

---

## 📊 Dataset Architecture & Multi-Tier Hierarchy

The dataset is structured across five relational tiers, distributed in both **Apache Parquet** (compressed with Snappy, strongly typed) and **Frictionless CSV** formats:

| Tier | Entity | Parquet File | Rows | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 0** | **Seasons** | `data/metadata/seasons.parquet` | 10 | Season years, formats, dates, champions & runners-up |
| **Tier 0** | **Teams** | `data/metadata/teams.parquet` | 12 | 12 franchise registries, codes, cities, debut years |
| **Tier 0** | **Venues** | `data/metadata/venues.parquet` | 28 | Stadium venues, cities, total matches hosted |
| **Tier 0** | **Rulesets** | `data/metadata/rulesets.parquet` | 1 | Codified PKL game rules, raid clocks, bonus lines |
| **Tier 1** | **Players** | `data/players/players.parquet` | 805 | Master athlete registry, roles, positions, career totals |
| **Tier 2** | **Matches** | `data/matches/matches.parquet` | 1,060 | Final scores, toss results, margins, point breakdowns |
| **Tier 3** | **Boxscores** | `data/player_matches/player_match_stats.parquet` | 26,760 | Player-match stats: raids, tackles, super 10s, high 5s |
| **Tier 4** | **Play-by-Play**| `data/raids_pbp/raids_pbp.parquet` | 103,176 | Sequential raid events: clocks, score diffs, outcomes |

---

## 🏆 Official Benchmark Leaderboard (Test Set: Season 10)

All baselines are evaluated strictly on the **out-of-sample Season 10 test set** (136 matches, 13,894 raids) without temporal lookahead leakage.

| Benchmark Task | Model | Primary Metric | Secondary Metric | Third Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1: Raid Outcome Prediction** | Majority Class | Accuracy: 0.4770 | Macro-F1: 0.1292 | Log-Loss: 18.8520 |
| | Multinomial Logistic | Accuracy: 0.5107 | Macro-F1: 0.2186 | Log-Loss: 1.0705 |
| | **HistGradientBoosting** | **Accuracy: 0.5319** | **Macro-F1: 0.2328** | **Log-Loss: 0.9804** |
| **Task 2: In-Game Win Probability** | Logistic Leverage | Brier: 0.2270 | ECE: 0.1882 | Log-Loss: 0.6446 |
| | **Calibrated GBDT** | **Brier: 0.1991** | **ECE: 0.1561** | **Log-Loss: 0.5827** |
| **Task 3: Pre-Match Outcome & Spread** | Random Guess | Accuracy: 0.5000 | Brier: 0.2500 | ROC-AUC: 0.5000 |
| | **Dynamic Kabaddi Elo** | **Accuracy: 0.7059** | **Brier: 0.1968** | **ROC-AUC: 0.7707** (MAE: 9.23) |

---

## 🔬 Strict Temporal Benchmark Split Protocol

Random $k$-fold cross-validation in sports causes severe **data leakage** because player rosters, franchise form, and tactical trends persist across games. PKL-Bench enforces a strict chronological partition:

- **Train Set (Seasons 1–8, 2014–2022)**: 787 matches | 75,777 raid events (74.2%)
- **Validation Set (Season 9, 2022)**: 137 matches | 13,505 raid events (12.9%)
- **Test Set (Season 10, 2023–2024)**: 136 matches | 13,894 raid events (12.8%)
- **Disjointness Guarantee**: $\text{Train} \cap \text{Val} = \emptyset$, $\text{Train} \cap \text{Test} = \emptyset$, $\text{Val} \cap \text{Test} = \emptyset$.

Explicit match IDs are codified in `data/benchmark_splits/splits.json`.

---

## ⚖️ Mathematical Score Conservation Audit

Every match in PKL-Bench satisfies the fundamental conservation equation of Kabaddi scoring:

$$\text{Total Score}_i = \text{Raid Points}_i + \text{Tackle Points}_i + \text{All-Out Bonus}_i + \text{Extra/Technical Points}_i$$

The automated audit in `pkl_bench.validator` confirms **100.0% adherence across all 1,060 matches** for both home and away teams with 0 discrepancies flagged.

---

## 📁 Repository Structure

```
pkl-benchmark/
├── pyproject.toml                     # Standard Python packaging configuration
├── README.md                          # Project documentation and leaderboard
├── data/                              # Multi-tier curated dataset
│   ├── metadata/                      # Seasons, teams, venues, rulesets
│   ├── players/                       # 805 players master registry
│   ├── matches/                       # 1,060 match summary records
│   ├── player_matches/                # 26,760 player boxscores
│   ├── raids_pbp/                     # 103,176 granular raid events
│   ├── benchmark_splits/              # splits.json (Train/Val/Test match IDs)
│   └── datapackage.json               # Frictionless Data open standard schema
├── pkl_bench/                         # Python evaluation harness & SDK
│   ├── __init__.py                    # Public API exports
│   ├── loader.py                      # Data loading and split retrieval
│   ├── metrics.py                     # Brier score, ECE, LogLoss, EPA
│   ├── validator.py                   # Score conservation & schema audit
│   ├── cli.py                         # Command-line interface
│   └── baselines/                     # Reference model implementations
│       ├── raid_outcome.py            # Task 1 baseline models
│       ├── win_probability.py         # Task 2 dynamic win probability
│       ├── match_winner.py            # Task 3 Dynamic Kabaddi Elo
│       └── player_impact.py           # Task 4 True Raider Impact (TRI)
├── docs/                              # Research documentation
│   ├── DATASHEET.md                   # Gebru et al. Datasheet for Datasets
│   ├── METHODOLOGY.md                 # MDP formulation and game dynamics
│   ├── BENCHMARK_SPEC.md              # Task specs & leaderboard protocol
│   └── KABADDI_DOMAIN_GUIDE.md        # Kabaddi rules, court layout, mechanics
├── examples/                          # Reproducible example scripts
│   └── quickstart.py                  # 30-second end-to-end demonstration
└── tests/                             # Test suite (16/16 passing)
    ├── test_loader.py
    ├── test_conservation.py
    ├── test_benchmarks.py
    └── test_metrics.py
```

---

## 📖 Citation

If you use PKL-Bench in your research, please cite:

```bibtex
@misc{pkl_bench_2026,
  author = {Ritesh},
  title = {PKL-Bench: The Pro Kabaddi League Research Benchmark Dataset and Evaluation Suite},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Prompt-0/pkl-bench}},
  note = {10 Seasons (2014-2024), 1,060 Matches, 103,176 Play-by-Play Raids}
}
```

---

## 📜 License

This dataset and codebase are distributed under the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)**.
