"""
Tests for PKL-Bench Command-Line Interface (CLI).
"""

from __future__ import annotations

import sys
from io import StringIO
from unittest.mock import patch

from pkl_bench.cli import main


def test_cli_info():
    """Verify pkl-bench info runs and displays summary statistics."""
    test_args = ["pkl-bench", "info"]
    with patch.object(sys, "argv", test_args):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            main()
            output = mock_out.getvalue()
            assert "PKL-BENCH: PRO KABADDI LEAGUE RESEARCH DATASET" in output
            assert "Total Seasons:      10" in output
            assert "Total Matches:      1,060" in output


def test_cli_validate():
    """Verify pkl-bench validate executes and confirms integrity."""
    test_args = ["pkl-bench", "validate"]
    with patch.object(sys, "argv", test_args):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            main()
            output = mock_out.getvalue()
            assert "Integrity Validation Status: PASSED [100%]" in output
            assert "Team 1 Conservation Pass: 100.0%" in output
            assert "Team 2 Conservation Pass: 100.0%" in output


def test_cli_benchmark_match_winner():
    """Verify pkl-bench benchmark --task match_winner runs correctly."""
    test_args = ["pkl-bench", "benchmark", "--task", "match_winner"]
    with patch.object(sys, "argv", test_args):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            main()
            output = mock_out.getvalue()
            assert "TASK 3: PRE-MATCH OUTCOME & SPREAD FORECASTING" in output
            assert "Dynamic_Kabaddi_Elo" in output
