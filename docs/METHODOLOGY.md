# PKL-Bench: Research Methodology & Modeling Framework

## Abstract
This document details the mathematical formulation, data curation protocol, and evaluation methodology underpinning **PKL-Bench**, the standardized benchmark dataset for the Pro Kabaddi League (PKL). We formulate Kabaddi as an asymmetric, discrete-time Markov Decision Process (MDP) with phase-dependent risk-reward dynamics, specify the score conservation verification protocol, and define the temporal evaluation framework.

---

## 1. Game-Theoretic & MDP Formulation of Kabaddi

### 1.1 Asymmetric Discrete-Time Formulation
Unlike symmetric invasion games (such as soccer or basketball) where both teams concurrently field equal players on an open pitch, Kabaddi is fundamentally **asymmetric and sequential**. 

At any raid index $t \in \{1, \dots, T\}$, one team designated as the **Attacking Team** sends exactly one player (the **Raider** $r \in \mathcal{R}$) into the half-court of the **Defending Team**, which fields $N_{def} \in \{1, 2, \dots, 7\}$ active defenders.

The match state at raid $t$ is formulated as a tuple:
$$S_t = \langle \Delta_t, \tau_t, h_t, N_{def, t}, D_t, B_t, r_t, \mathcal{D}_t \rangle$$

Where:
- $\Delta_t = \text{Score}_{attack, t} - \text{Score}_{defense, t}$: Point differential relative to the raiding team.
- $\tau_t \in [0, 1200]$: Clock seconds remaining in the current half.
- $h_t \in \{1, 2\}$: Current match half.
- $N_{def, t} \in \{1, \dots, 7\}$: Number of active defenders on the mat.
- $D_t \in \{0, 1\}$: Binary Do-or-Die indicator ($D_t = 1$ if the raiding team has registered two consecutive empty raids).
- $B_t \in \{0, 1\}$: Bonus line eligibility ($B_t = 1 \iff N_{def, t} \ge 6$).
- $r_t \in \mathcal{P}$: Raider identity and latent skill embedding.
- $\mathcal{D}_t \subset \mathcal{P}, |\mathcal{D}_t| = N_{def, t}$: Set of active defenders on court.

### 1.2 The Action and Outcome Space
During the 30-second raid window, the interaction collapses into discrete outcome categories:
$$\mathcal{Y} = \{\text{EMPTY}, \text{SUCCESSFUL\_TOUCH}, \text{BONUS\_ONLY}, \text{SUPER\_RAID}, \text{UNSUCCESSFUL\_TACKLE}, \text{SUPER\_TACKLE}\}$$

The payoff function $R(S_t, y)$ governs the state transition:
- **Empty Raid** ($y = \text{EMPTY}$): $\Delta_{t+1} = \Delta_t$, no revivals, no dismissals.
- **Successful Touch Raid** ($y = \text{SUCCESSFUL\_TOUCH}$, $k$ defenders touched): 
  $$\text{Score}_{attack} \leftarrow \text{Score}_{attack} + k$$
  $k$ defenders dismissed to the out-box; up to $k$ teammates revived.
- **Super Raid** ($y = \text{SUPER\_RAID}$): $k \ge 3$ points scored.
- **Unsuccessful Raid / Tackle** ($y = \text{UNSUCCESSFUL\_TACKLE}$):
  $$\text{Score}_{defense} \leftarrow \text{Score}_{defense} + 1$$
  Raider $r_t$ dismissed; one defender revived.
- **Super Tackle** ($y = \text{SUPER\_TACKLE}$): If $N_{def, t} \le 3$, successful tackle yields **2 points** to the defending team.

### 1.3 Strategic Phase Transitions
Kabaddi exhibits two crucial structural discontinuities (phase transitions) that make it an exceptional testbed for machine learning and game theory:
1. **The Bonus Threshold ($N_{def} = 6$)**: When the defense drops to 5 players, the bonus line deactivates ($B_t = 0$). The raider can no longer earn a risk-free point without physical contact, forcing aggressive penetration.
2. **The Super Tackle Regime ($N_{def} \le 3$)**: Defensive tackle payoff jumps from 1 point to 2 points ($+100\%$), while raider risk remains 1 dismissal. Consequently, defending teams often adopt conservative chain formations to bait aggressive raiders into traps.

---

## 2. Mathematical Score Conservation Law

Every official PKL match is governed by an absolute conservation equation. For each team $i \in \{1, 2\}$:
$$\text{Total Score}_i = \text{Raid Points}_i + \text{Tackle Points}_i + \text{All-Out Points}_i + \text{Extra Points}_i$$

Where:
- $\text{Raid Points}_i = \text{Touch Points}_i + \text{Bonus Points}_i$
- $\text{Tackle Points}_i = \text{Capture Points}_i + \text{Super Tackle Bonus}_i$
- $\text{All-Out Points}_i = 2 \times (\text{All-Outs Inflicted on Opponent})$
- $\text{Extra Points}_i = \text{Technical Points (Opponent Line Violation, Jersey Pull, Yellow/Red Card Penalties)}$

### Verification Audit
In PKL-Bench, every single match record was programmatically validated against this conservation law. Across all 1,060 matches, the conservation equation holds with **100.0% adherence**, ensuring zero corrupted point bookkeeping.

---

## 3. Strict Temporal Benchmark Protocol

In sports analytics, standard random $k$-fold cross-validation is invalid because:
1. **Team and Player Identity Leakage**: Training on Match 10 and testing on Match 5 allows models to learn player form and tactical setups that did not yet exist in the training window.
2. **Tactical Meta-Game Drift**: League-wide defensive styles, rule adaptations, and auction rosters evolve monotonically across time.

To ensure benchmark integrity, PKL-Bench adopts a **strict chronological partition**:

```
[  Seasons 1 - 8 (2014 - 2022)  ] [ Season 9 (2022) ] [ Season 10 (2023-24) ]
|-------------------------------|-------------------|-----------------------|
        TRAIN (787 Matches)         VAL (137 Matches)      TEST (136 Matches)
           74.2% of Data              12.9% of Data           12.8% of Data
```

### Partition Properties:
- **Train Set**: Historical foundations, spanning 8 seasons across 8-team and 12-team eras.
- **Validation Set**: Season 9 (2022) for model selection, feature engineering, and hyperparameter tuning.
- **Test Set**: Season 10 (2023–2024) held strictly out-of-sample for final benchmark comparison.
- **Disjointness**: $Train \cap Val = \emptyset$, $Train \cap Test = \emptyset$, $Val \cap Test = \emptyset$. Total matches: exactly 1,060.
