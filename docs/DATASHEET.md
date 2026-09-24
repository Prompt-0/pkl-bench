# Datasheet for Dataset: PKL-Bench

Following the framework proposed by Timnit Gebru et al. (*Datasheets for Datasets*, Communications of the ACM, Dec 2021).

---

## 1. Motivation

### For what purpose was the dataset created?
**PKL-Bench** was created to address the acute lack of standardized, granular, research-grade benchmark datasets for contact and invasion team sports from non-Western origins, specifically **Kabaddi**. While sports analytics has flourished in association football (SoccerNet, StatsBomb), basketball (NBA Play-by-Play), and cricket (Cricsheet), professional Kabaddi—despite being watched by over 230 million viewers annually—has lacked a unified, open, play-by-play benchmark dataset with rigorous evaluation protocols. PKL-Bench standardizes 10 full seasons of the Pro Kabaddi League (2014–2024), providing 1,060 matches, 26,760 player boxscores, and 103,176 granular, timestamped raid events.

### Who created the dataset and on whose behalf?
The dataset was engineered, harmonized, and verified by **Ritesh Dobhal** (University of Delhi; GitHub: [\texttt{Prompt-0}](https://github.com/Prompt-0)) for the global sports analytics, machine learning, and sequential decision-making / reinforcement learning research communities.

### Who funded the creation of the dataset?
Open scientific research initiative; self-funded under open-science principles.

---

## 2. Composition

### What do the instances that comprise the dataset represent?
The dataset is structured across five hierarchical tiers:
1. **Tier 0 (Metadata)**: League seasons, 12 team franchise registries, 28 stadium venues, and codified competition rules.
2. **Tier 1 (Players)**: Master registry of 805 professional athletes, tactical roles, positions, and career aggregates.
3. **Tier 2 (Matches)**: 1,060 completed PKL matches with final scores, halves, toss decisions, venue linkages, and point breakdowns.
4. **Tier 3 (Player Matches)**: 26,760 individual player boxscores recording raids, tackles, super 10s, high 5s, cards, and points.
5. **Tier 4 (Play-by-Play Raids)**: 103,176 sequential raid events recording clock time, half, score differential, do-or-die status, raider ID, primary defender ID, and outcomes.

### How many instances are there in total?
- **Seasons**: 10
- **Franchise Teams**: 12
- **Venues**: 28
- **Matches**: 1,060
- **Registered Players**: 805
- **Player Match Boxscores**: 26,760
- **Discrete Raid Events**: 103,176

### Does the dataset contain all possible instances or is it a sample?
The dataset represents the **complete universe** of official Pro Kabaddi League matches from Season 1 (July 2014) through the conclusion of Season 10 (March 2024). No sampling or filtering was performed.

### What data does each instance consist of?
Each instance is typed and documented under Frictionless Data standards in `datapackage.json`.
- Parquet format (Snappy compressed, columnar binary).
- CSV format (UTF-8 encoded standard text).

### Is any information missing from individual instances?
All 1,060 matches have 100% complete match records, scores, winners, and team statistics. In play-by-play raid events for Seasons 1–5, certain broadcast sensor fields (such as optical player coordinate tracking) were not captured by the league broadcaster; however, all core state variables (clock, sequence, raider, defender, touch points, bonus points, technical points, and score states) are complete.

---

## 3. Collection Process

### How was the data collected?
Raw feeds and match center records were aggregated from official Pro Kabaddi League match records and Sportz Interactive microservices feeds, cross-verified with open-source scrapers (`kabaddiPy`), and programmatically audited against verified match scorecards.

### Who was involved in the data collection process?
Automated ETL ingestion scripts with human-in-the-loop verification of tiebreaker scenarios, rule modifications, and player name disambiguation.

### Over what timeframe was the data collected?
Historical data covers the 10-year span from July 26, 2014 to March 1, 2024.

---

## 4. Preprocessing, Cleaning, & Validation

### What preprocessing or cleaning was done?
1. **Schema Harmonization**: Earlier seasons (S1–S5) had slight variations in JSON nesting compared to modern seasons (S6–S10). All 10 seasons were harmonized into a uniform tabular structure.
2. **Entity Disambiguation**: Player IDs were reconciled across name variants (e.g. spelling changes in jersey rosters).
3. **Score Conservation Audit**: An automated conservation law audit was executed across all 1,060 matches:
   $$\text{Total Score} = \text{Raid Points} + \text{Tackle Points} + \text{All-Out Points} + \text{Technical/Extra Points}$$
   **Result**: 100.0% pass rate on both Team 1 and Team 2 across all 1,060 matches.
4. **Timestamp Monotonicity**: Clock records were parsed and normalized into `clock_seconds_remaining` (0 to 2400 seconds) reflecting exact match time.

### Were any samples discarded?
Duplicate match records or corrupted JSON stubs were identified and removed. Exactly 1,060 unique matches were retained.

---

## 5. Uses & Benchmark Tasks

### Has the dataset been used for specific tasks already?
Yes. PKL-Bench defines four formal benchmark tasks with reproducible baselines:
1. **Task 1: Discrete Raid Outcome Prediction** (Empty, Success, Unsuccessful, Super Raid, Super Tackle).
2. **Task 2: Dynamic In-Game Win Probability Modeling** ($P(\text{Team 1 Wins} \mid \text{Raid State}_t)$).
3. **Task 3: Pre-Match Outcome & Margin Forecasting** (Dynamic Elo and spread prediction).
4. **Task 4: Player Valuation & Impact Rating** (True Raider Impact and Defender Impact).

### What is the official benchmark split protocol?
To prevent catastrophic temporal data leakage common in random k-fold sports cross-validation, PKL-Bench establishes strict temporal splits:
- **Train Set**: Seasons 1–8 (2014–2022) — 787 matches (74.2%)
- **Validation Set**: Season 9 (2022) — 137 matches (12.9%)
- **Test Set**: Season 10 (2023–2024) — 136 matches (12.8%)

Splits are strictly disjoint ($Train \cap Val = \emptyset$, $Train \cap Test = \emptyset$, $Val \cap Test = \emptyset$).

---

## 6. Distribution & Licensing

### How will the dataset be distributed?
Distributed via standard Git repository with Parquet and CSV formats, and installable as a Python package (`pip install -e .`).

### What is the license?
**Creative Commons Attribution 4.0 International (CC-BY-4.0)**.
Users are free to share and adapt the material for any purpose, including commercial, with appropriate credit.

---

## 7. Maintenance

### Who is supporting and maintaining the dataset?
Ritesh Dobhal (University of Delhi; GitHub: [Prompt-0/pkl-bench](https://github.com/Prompt-0/pkl-bench)). Updates will be issued following subsequent PKL seasons (Season 11+).
Issues and errata can be reported via GitHub Issues.
