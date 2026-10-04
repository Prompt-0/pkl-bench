import re

with open("scripts/build_dataset.py", "r") as f:
    code = f.read()

old_logic = """        if score_t1_after is not None and score_t2_after is not None:
            # Check which team is raiding team
            # Let's see: ev_score usually corresponds to team 1 and team 2
            curr_score_t1 = score_t1_after
            curr_score_t2 = score_t2_after

        # Raider name"""

new_logic = """        score_t1_before = curr_score_t1
        score_t2_before = curr_score_t2

        if score_t1_after is not None and score_t2_after is not None:
            curr_score_t1 = score_t1_after
            curr_score_t2 = score_t2_after

        # Raider name"""

code = code.replace(old_logic, new_logic)

old_append = """            "primary_defender_name": defender_name,
            "team1_score_after": curr_score_t1,
            "team2_score_after": curr_score_t2,"""

new_append = """            "primary_defender_name": defender_name,
            "team1_score_before": score_t1_before,
            "team2_score_before": score_t2_before,
            "team1_score_after": curr_score_t1,
            "team2_score_after": curr_score_t2,"""

code = code.replace(old_append, new_append)

with open("scripts/build_dataset.py", "w") as f:
    f.write(code)

