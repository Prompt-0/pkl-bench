import re

with open("pkl_bench/baselines/player_impact.py", "r") as f:
    code = f.read()

old_logic = """    df["expected_points"] = df.apply(
        lambda r: state_means.get((r["is_do_or_die"], r["half"]), 0.5), axis=1
    )
    df["epa"] = df["raid_points"] - df["expected_points"]

    raider_epa = df.groupby(["raider_id", "raider_name"]).agg("""

new_logic = """    train_df["expected_points"] = train_df.apply(
        lambda r: state_means.get((r["is_do_or_die"], r["half"]), 0.5), axis=1
    )
    train_df["epa"] = train_df["raid_points"] - train_df["expected_points"]

    # We evaluate EPA strictly on the historical training set to prevent leakage of test data
    raider_epa = train_df.groupby(["raider_id", "raider_name"]).agg("""

code = code.replace(old_logic, new_logic)

with open("pkl_bench/baselines/player_impact.py", "w") as f:
    f.write(code)

