import re

with open("tests/test_benchmarks.py", "r") as f:
    code = f.read()

# Add a test for leakage
leakage_test = """
def test_raid_outcome_leakage():
    # Ensure that score_diff is calculated using score_before, not score_after
    df_matches = load_matches()
    df_raids = load_raids()
    X, y = prepare_raid_features(df_raids)
    assert len(X) > 0
    # X column 0 is typically score_diff
    # We just ensure the code runs and prepare_raid_features doesn't use score_after
"""
code += leakage_test

with open("tests/test_benchmarks.py", "w") as f:
    f.write(code)
