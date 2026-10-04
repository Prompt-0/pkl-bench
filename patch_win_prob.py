import re
with open("pkl_bench/baselines/win_probability.py", "r") as f:
    code = f.read()

old_loop = """    for _, row in df_matches.iterrows():
        mid = row["match_id"]
        t1 = row["team1_id"]
        team1_map[mid] = t1
        match_winner_map[mid] = 1 if row["winner_id"] == t1 else 0"""

new_loop = """    for _, row in df_matches.iterrows():
        # Drop ties for clean binary win probability task
        if row["winner_id"] == 0 or pd.isna(row["winner_id"]) or row["is_tie"]:
            continue
        mid = row["match_id"]
        t1 = row["team1_id"]
        team1_map[mid] = t1
        match_winner_map[mid] = 1 if row["winner_id"] == t1 else 0"""

code = code.replace(old_loop, new_loop)
with open("pkl_bench/baselines/win_probability.py", "w") as f:
    f.write(code)

