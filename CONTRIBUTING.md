# Contributing to PKL-Bench

Thank you for your interest in contributing to **PKL-Bench**! We welcome contributions from researchers, sports analysts, data scientists, and engineers worldwide.

As an open-science benchmark designed according to FAIR principles (Findable, Accessible, Interoperable, Reusable), PKL-Bench aims to advance machine learning and quantitative game theory in asymmetric contact sports.

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for all contributors regardless of background, gender, sexual orientation, disability, physical appearance, or religion. Please be respectful and constructive in all communications and issue threads.

---

## Development Setup

1. **Fork and Clone the Repository**:
   ```bash
   git clone https://github.com/Prompt-0/pkl-bench.git
   cd pkl-bench
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in Editable Mode with Developer Dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify the Installation**:
   ```bash
   make test
   make validate
   ```

---

## Contribution Workflows

### 1. Submitting a New Benchmark Baseline

We actively welcome new machine learning and statistical models to the PKL-Bench Leaderboard (e.g., Deep Reinforcement Learning, Transformers, Spatial Point Process models).

When submitting a model:
- **Strict Leakage-Free Protocol**: You **must** train exclusively on the official Training Set (Seasons 1–8) and tune hyperparameters on the Validation Set (Season 9). The Test Set (Season 10) must **only** be evaluated once for final reporting.
  ```python
  import pkl_bench as pb
  train_raids, val_raids, test_raids = pb.get_benchmark_split(task="raids")
  ```
- **Standard Metrics**:
  - **Task 1 (Raid Outcome)**: Multiclass Log-Loss, Accuracy, Macro-F1.
  - **Task 2 (In-Game Win Probability)**: Brier Score, Expected Calibration Error (ECE), Log-Loss.
  - **Task 3 (Match Winner & Spread)**: Binary Accuracy, ROC-AUC, Margin MAE.
  - **Task 4 (Player Valuation)**: Cumulative Expected Points Added (EPA), EPA per raid.
- **Reproducibility**: Provide a standalone, deterministic script in `examples/` or within `pkl_bench/baselines/` with fixed random seeds (`random_state=42`).

### 2. Reporting Data Errata & Scorecard Discrepancies

If you identify a data discrepancy (e.g., an uncredited bonus point, incorrect timestamp, or misspelled player name):
1. Open an issue on GitHub titled: `[Data Errata] Season X Match Y - Description`.
2. Cite official PKL match scorecards or video timestamps.
3. Note that every proposed data modification must satisfy the **Score Conservation Law**:
   $$\text{Total Score}_i = \text{Raid Points}_i + \text{Tackle Points}_i + \text{All-Out Bonus}_i + \text{Extra Points}_i$$
   Run `pkl-bench validate` before submitting any pull request that modifies data files.

### 3. Pull Request Guidelines

- **Atomic Commits**: Follow Conventional Commits format (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
- **Test Coverage**: Any new feature or baseline must include corresponding unit tests in `tests/`.
- **Formatting & Linting**: Verify code quality before submitting:
  ```bash
  ruff check .
  pytest -v
  ```

---

## Scholarly Citation

If you use PKL-Bench in academic publications, please cite:

```bibtex
@misc{dobhal2026pklbench,
  author = {Dobhal, Ritesh},
  title = {PKL-Bench: The Pro Kabaddi League Research Benchmark Dataset and Evaluation Suite},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Prompt-0/pkl-bench}},
  note = {University of Delhi. ORCID: 0009-0009-2773-4972. 10 Seasons (2014-2024), 1,060 Matches, 90,644 Play-by-Play Raids}
}
```
