# PKL-Bench: Official Benchmark Specification & Leaderboard

This specification establishes standard tasks, formal evaluation protocols, and reference baseline leaderboards for the Pro Kabaddi League (PKL) research benchmark.

---

## Benchmark Leaderboard Summary (Test Set: Season 10)

| Task | Baseline Model | Primary Metric | Secondary Metric | Third Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1: Raid Outcome** | Majority Class | Accuracy: 0.4770 | Macro-F1: 0.1292 | Log-Loss: 18.8520 |
| | Multinomial Logistic | Accuracy: 0.5107 | Macro-F1: 0.2186 | Log-Loss: 1.0705 |
| | **HistGradientBoosting** | **Accuracy: 0.5319** | **Macro-F1: 0.2328** | **Log-Loss: 0.9804** |
| **Task 2: Win Probability** | Logistic Leverage | Brier: 0.2270 | ECE: 0.1882 | Log-Loss: 0.6446 |
| | **Calibrated GBDT** | **Brier: 0.1991** | **ECE: 0.1561** | **Log-Loss: 0.5827** |
| **Task 3: Match Winner** | Random Baseline | Accuracy: 0.5000 | Brier: 0.2500 | ROC-AUC: 0.5000 |
| | **Dynamic Kabaddi Elo** | **Accuracy: 0.7059** | **Brier: 0.1968** | **ROC-AUC: 0.7707** (MAE: 9.23) |

---

## Task 1: Discrete Raid Outcome Prediction

### 1.1 Problem Statement
Predict the categorical outcome of an individual raid event given the game state at the instant of the raid's commencement.

### 1.2 Target Classes
- `EMPTY_RAID` (0 points, raider returns safely)
- `SUCCESSFUL_RAID` (1 point, touch or bonus)
- `UNSUCCESSFUL_RAID` (Raider tackled by defense; 1 point to defense)
- `SUPER_RAID` ($\ge 3$ points to raiding team)
- `SUPER_TACKLE` (Defense tackles raider with $\le 3$ active defenders; 2 points to defense)

### 1.3 Inputs & Features
- `is_do_or_die` (bool)
- `clock_seconds_remaining` (int, 0 to 2400)
- `half` (int, 1 or 2)
- `score_diff` (int, raiding team lead or deficit)
- `raiding_team_id`, `defending_team_id` (int)
- Optional: Historical player strike rates, defender ratings, lineup embeddings.

### 1.4 Primary Metrics
- **Multiclass Log-Loss**: $\mathcal{L}_{CE} = -\frac{1}{N}\sum_{i=1}^N \sum_{c=1}^C y_{i,c} \log \hat{p}_{i,c}$
- **Macro-Averaged F1 Score**: $\frac{1}{C}\sum_{c=1}^C F1_c$ (critical for evaluating rare classes like Super Raids and Super Tackles).
- **Classification Accuracy**: $\frac{1}{N}\sum_{i=1}^N \mathbb{I}(y_i = \hat{y}_i)$.

---

## Task 2: In-Game Dynamic Win Probability Modeling

### 2.1 Problem Statement
At any raid event $t$ throughout regulation time (40 minutes), estimate the calibrated probability that Team 1 will win the match:
$$P(\text{Team 1 Wins} \mid S_t) \in [0, 1]$$

### 2.2 Inputs & Features
- `score_diff`: $\text{Score}_{\text{team1}, t} - \text{Score}_{\text{team2}, t}$
- `seconds_remaining`: Match seconds remaining ($0 \le \tau \le 2400$)
- `half`: 1 or 2
- `scaled_leverage`: $\frac{\text{score\_diff}}{\sqrt{\text{seconds\_remaining} + 1}}$
- `possession`: 1 if Team 1 is conducting the raid, 0 if Team 2 is raiding.

### 2.3 Primary Metrics
- **Brier Score**: $\text{BS} = \frac{1}{N}\sum_{i=1}^N (p_i - y_i)^2 \in [0, 1]$ (lower is better).
- **Expected Calibration Error (ECE)**: Evaluates reliability across 10 equal probability bins.
- **Negative Log-Likelihood (Log-Loss)**.

---

## Task 3: Pre-Match Outcome & Margin Forecasting

### 3.1 Problem Statement
Prior to the coin toss of match $m$, predict the binary match winner and the expected margin of victory $\hat{\Delta} = \text{Score}_{\text{team1}} - \text{Score}_{\text{team2}}$.

### 3.2 Evaluation Metrics
- **Pre-Match Win Accuracy**
- **ROC-AUC**
- **Brier Score**
- **Margin Mean Absolute Error (MAE)**: $\frac{1}{M}\sum_{m=1}^M |\Delta_m - \hat{\Delta}_m|$

---

## Task 4: Player Valuation & Impact Rating

### 4.1 True Raider Impact (TRI)
$$\text{TRI} = \frac{\sum (\text{Raid Points}) - 1.25 \times \sum (\text{Unsuccessful Raids}) + 0.5 \times \sum (\text{Super Raids})}{\text{Total Raids Attempted}}$$

### 4.2 True Defender Impact (TDI)
$$\text{TDI} = \frac{\sum (\text{Tackle Points}) - 1.0 \times \sum (\text{Unsuccessful Tackles}) + 1.0 \times \sum (\text{Super Tackles})}{\text{Total Tackles Attempted}}$$

---

## Reproducibility Protocol

To reproduce baseline figures or submit a new model:
```bash
# 1. Install pkl-bench
pip install -e .

# 2. Run official benchmarks
pkl-bench benchmark --task all
```
