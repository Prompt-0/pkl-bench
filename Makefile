PYTHON ?= $(shell which uv >/dev/null 2>&1 && echo "uv run python" || echo "python3")
PYTEST ?= $(shell which uv >/dev/null 2>&1 && echo "uv run pytest" || echo "pytest")
PKL_BENCH ?= $(shell which uv >/dev/null 2>&1 && echo "uv run pkl-bench" || echo "pkl-bench")
PIP ?= $(shell which uv >/dev/null 2>&1 && echo "uv pip" || echo "pip")

.PHONY: install test validate benchmark plots paper arxiv clean help

help:
	@echo "PKL-Bench Developer Commands:"
	@echo "  make install    - Install pkl-bench in editable mode with dev dependencies"
	@echo "  make test       - Run test battery via pytest"
	@echo "  make validate   - Execute score conservation & integrity audits"
	@echo "  make benchmark  - Run official benchmark baselines"
	@echo "  make plots      - Regenerate publication figures in paper/figures/"
	@echo "  make paper      - Recompile research paper PDF via tectonic"
	@echo "  make arxiv      - Build clean arXiv submission zip (paper + bbl + figures)"
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
	tectonic --keep-intermediates paper/pkl_bench_paper.tex

arxiv: paper
	python3 -c "import zipfile, os; z = zipfile.ZipFile('pkl_bench_arxiv_submission.zip', 'w', zipfile.ZIP_DEFLATED); z.write('paper/pkl_bench_paper.tex', 'pkl_bench_paper.tex'); z.write('paper/pkl_bench_paper.bbl', 'pkl_bench_paper.bbl'); z.write('paper/references.bib', 'references.bib'); [z.write(os.path.join('paper/figures', f), os.path.join('figures', f)) for f in sorted(os.listdir('paper/figures')) if f.endswith('.pdf')]; z.close()"
	@echo "✓ pkl_bench_arxiv_submission.zip packaged successfully"

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/ .ruff_cache/ __pycache__ pkl_bench/__pycache__ tests/__pycache__ *.pyc paper/*.aux paper/*.out paper/*.log
