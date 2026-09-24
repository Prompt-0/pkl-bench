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
	pip install -e ".[dev]"

test:
	pytest -v

validate:
	pkl-bench validate

benchmark:
	pkl-bench benchmark --task all

plots:
	python scripts/generate_plots.py

paper: plots
	tectonic paper/pkl_bench_paper.tex

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ __pycache__/ pkl_bench/__pycache__ tests/__pycache__
