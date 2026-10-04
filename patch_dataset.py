import re

with open("scripts/build_dataset.py", "r") as f:
    code = f.read()

# 1. Update parse_clock_to_seconds signature and logic
old_clock = """def parse_clock_to_seconds(clock_str: Optional[str], half: int) -> int:
    \"\"\"
    Converts clock MM:SS string and half to total match seconds remaining (0 to 2400).
    Kabaddi match has two 20-minute halves (2400 seconds total).
    In official PKL data:
    Clock often displays MM:SS remaining in that half (e.g., '19:24' means 19m24s remaining in half).
    \"\"\"
    if not clock_str or not isinstance(clock_str, str) or ":" not in clock_str:
        return 1200 if half == 1 else 0
    try:
        parts = clock_str.split(":")
        minutes = int(parts[0])
        seconds = int(parts[1])
        half_sec_remaining = minutes * 60 + seconds
        if half == 1:
            return 1200 + half_sec_remaining
        else:
            return min(1200, half_sec_remaining)
    except Exception:
        return 1200 if half == 1 else 0"""

new_clock = """def parse_clock_to_seconds(clock_str: Optional[str], half: int, season_id: int) -> int:
    \"\"\"
    Converts clock MM:SS string and half to total match seconds remaining (0 to 2400).
    In Seasons 1-5, the clock counts UP (elapsed time).
    In Seasons 6-10, the clock counts DOWN (remaining time).
    \"\"\"
    if not clock_str or not isinstance(clock_str, str) or ":" not in clock_str:
        return 1200 if half == 1 else 0
    try:
        parts = clock_str.split(":")
        minutes = int(parts[0])
        seconds = int(parts[1])
        val = minutes * 60 + seconds
        
        # Clamp to 1200 (sometimes goes slightly over like 20:01)
        val = min(1200, val)
        
        if season_id <= 5:
            # val is elapsed time, so remaining is 1200 - val
            half_sec_remaining = 1200 - val
        else:
            # val is remaining time
            half_sec_remaining = val
            
        if half == 1:
            return 1200 + half_sec_remaining
        else:
            return half_sec_remaining
    except Exception:
        return 1200 if half == 1 else 0"""

code = code.replace(old_clock, new_clock)

# 2. Update extract_raids_pbp
code = code.replace("seconds_left = parse_clock_to_seconds(clock_str, half)", "seconds_left = parse_clock_to_seconds(clock_str, half, season_id)")

# 3. Filter non-raids in extract_raids_pbp
old_loop_start = """    for idx, ev in enumerate(events_sorted):
        seq_no = clean_int(ev.get("event_no") or ev.get("seq_no") or (idx + 1))"""

new_loop_start = """    for idx, ev in enumerate(events_sorted):
        raw_event_name = clean_str(ev.get("event")).upper()
        # Filter out substitutions, timeouts, and cards which are not raids
        if "SUBSTITUTION" in raw_event_name or "TIMEOUT" in raw_event_name or "CARD" in raw_event_name or "REVIEW" in raw_event_name:
            continue
        # Also filter out rows with raider_id 0 unless it's a technical point
        if clean_int(ev.get("raider_id")) == 0 and "RAID" not in raw_event_name:
            continue
            
        seq_no = clean_int(ev.get("event_no") or ev.get("seq_no") or (idx + 1))"""

code = code.replace(old_loop_start, new_loop_start)

# 4. Handle tie label (Update Task 1 benchmark target)
# The tie label isn't in build_dataset, it's in metrics/baselines.

with open("scripts/build_dataset.py", "w") as f:
    f.write(code)

