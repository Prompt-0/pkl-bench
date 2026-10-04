import re

with open("scripts/build_dataset.py", "r") as f:
    code = f.read()

# Remove the early continue logic that breaks the score
old_loop_start = """    for idx, ev in enumerate(events_sorted):
        raw_event_name = clean_str(ev.get("event")).upper()
        # Filter out substitutions, timeouts, and cards which are not raids
        if "SUBSTITUTION" in raw_event_name or "TIMEOUT" in raw_event_name or "CARD" in raw_event_name or "REVIEW" in raw_event_name:
            continue
        # Also filter out rows with raider_id 0 unless it's a technical point
        if clean_int(ev.get("raider_id")) == 0 and "RAID" not in raw_event_name:
            continue

        seq_no = clean_int(ev.get("event_no") or ev.get("seq_no") or (idx + 1))"""

new_loop_start = """    for idx, ev in enumerate(events_sorted):
        raw_event_name = clean_str(ev.get("event")).upper()
        seq_no = clean_int(ev.get("event_no") or ev.get("seq_no") or (idx + 1))"""

code = code.replace(old_loop_start, new_loop_start)

# Add the filtering logic *after* the score is updated, right before appending to `raids`
old_append = """        raids.append({
            "match_id": match_id,"""

new_append = """        # Filter out non-raid events from being added to the raids tabular dataset
        # but only AFTER we have updated the running scores.
        is_valid_raid = True
        if "SUBSTITUTION" in raw_event_name or "TIMEOUT" in raw_event_name or "CARD" in raw_event_name or "REVIEW" in raw_event_name:
            is_valid_raid = False
        if clean_int(ev.get("raider_id")) == 0 and "RAID" not in raw_event_name:
            is_valid_raid = False

        if is_valid_raid:
            raids.append({
                "match_id": match_id,"""

# Since we indented the raids.append block, we need to replace the whole block or just use regex.
# Actually it's easier to just do it via regex substitution for the dict.

# Let's write a smarter regex or just replace the specific dict building part.
