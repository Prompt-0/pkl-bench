import re

with open("pkl_bench/baselines/player_impact.py", "r") as f:
    code = f.read()

old_logic = """    # Calculate baseline expectation across state partitions
    state_means = df.groupby(["is_do_or_die", "half"])["raid_points"].mean().to_dict()"""

new_logic = """    # Calculate baseline expectation strictly on Train Split (Seasons 1-8) to prevent leakage
    train_df = df[df["season_id"] <= 8]
    state_means = train_df.groupby(["is_do_or_die", "half"])["raid_points"].mean().to_dict()"""

code = code.replace(old_logic, new_logic)

with open("pkl_bench/baselines/player_impact.py", "w") as f:
    f.write(code)

