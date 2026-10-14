PYTHON ?= $(shell which uv >/dev/null 2>&1 && echo "uv run python" || echo "python3")
PYTEST ?= $(shell which uv >/dev/null 2>&1 && echo "uv run pytest" || echo "pytest")
PKL_BENCH ?= $(shell which uv >/dev/null 2>&1 && echo "uv run pkl-bench" || echo "pkl-bench")
PIP ?= $(shell which uv >/dev/null 2>&1 && echo "uv pip" || echo "pip")

.PHONY: install test validate benchmark plots paper clean help

help:
	@echo "PKL-Bench Developer Commands:"
	@echo "  make install    - Install pkl-bench in editable mode with dev dependencies"
	@echo "  make test       - Run test battery via pytest"
	@echo "  make validate   - Execute score conservation & integrity audits"
	@echo "  make benchmark  - Run official benchmark baselines"
	@echo "  make plots      - Regenerate publication figures in paper/figures/"
	@echo "  make paper      - Recompile research paper PDF via tectonic"
	@echo "  make clean      - Clean temporary and build artifacts"

install:
	$(PIP) install -e ".[dev]"

test:
	$(PYTEST) -v

validate:
	$(PKL_BENCH) validate

benchmark:
	$(PKL_BENCH) benchmark --task all

plots:
	$(PYTHON) scripts/generate_plots.py

paper: plots
	tectonic paper/pkl_bench_paper.tex

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/ .ruff_cache/ __pycache__ pkl_bench/__pycache__ tests/__pycache__ *.pyc
