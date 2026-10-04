import re

with open("scripts/build_dataset.py", "r") as f:
    code = f.read()

# Replace the append block to add indentation and the `if is_valid_raid:` check
old_append_block = """        raids.append({
            "match_id": match_id,
            "season_id": season_id,
            "raid_sequence_no": seq_no,
            "half": half,
            "clock": clock_str,
            "clock_seconds_remaining": seconds_left,
            "raiding_team_id": raiding_team_id,
            "defending_team_id": defending_team_id,
            "raider_id": raider_id,
            "raider_name": raider_name,
            "is_do_or_die": is_dod,
            "outcome_category": outcome_category,
            "raid_points": raid_pts,
            "raid_touch_points": raid_touch,
            "raid_bonus_points": raid_bonus,
            "defending_points": def_pts,
            "is_super_raid": is_super_raid,
            "is_super_tackle": is_super_tackle,
            "primary_defender_id": defender_id,
            "primary_defender_name": defender_name,
            "team1_score_before": score_t1_before,
            "team2_score_before": score_t2_before,
            "team1_score_after": curr_score_t1,
            "team2_score_after": curr_score_t2,
            "event_text": event_text
        })"""

new_append_block = """        is_valid_raid = True
        if "SUBSTITUTION" in raw_event_name or "TIMEOUT" in raw_event_name or "CARD" in raw_event_name or "REVIEW" in raw_event_name:
            is_valid_raid = False
        if clean_int(ev.get("raider_id")) == 0 and "RAID" not in raw_event_name:
            is_valid_raid = False

        if is_valid_raid:
            raids.append({
                "match_id": match_id,
                "season_id": season_id,
                "raid_sequence_no": seq_no,
                "half": half,
                "clock": clock_str,
                "clock_seconds_remaining": seconds_left,
                "raiding_team_id": raiding_team_id,
                "defending_team_id": defending_team_id,
                "raider_id": raider_id,
                "raider_name": raider_name,
                "is_do_or_die": is_dod,
                "outcome_category": outcome_category,
                "raid_points": raid_pts,
                "raid_touch_points": raid_touch,
                "raid_bonus_points": raid_bonus,
                "defending_points": def_pts,
                "is_super_raid": is_super_raid,
                "is_super_tackle": is_super_tackle,
                "primary_defender_id": defender_id,
                "primary_defender_name": defender_name,
                "team1_score_before": score_t1_before,
                "team2_score_before": score_t2_before,
                "team1_score_after": curr_score_t1,
                "team2_score_after": curr_score_t2,
                "event_text": event_text
            })"""

code = code.replace(old_append_block, new_append_block)

# Fix minor typo
code = code.replace("t2_stats = t2_stats = t2.get(\"stats\", {}) or {}", "t2_stats = t2.get(\"stats\", {}) or {}")

with open("scripts/build_dataset.py", "w") as f:
    f.write(code)

