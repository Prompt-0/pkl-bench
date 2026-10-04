with open("pkl_bench/baselines/match_winner.py", "r") as f:
    mw = f.read()
mw = mw.replace("elo.update_match(t1, t2, s1, s2, home_team_id=-1)", "if sid <= 8:\n            elo.update_match(t1, t2, s1, s2, home_team_id=-1)")
with open("pkl_bench/baselines/match_winner.py", "w") as f:
    f.write(mw)
