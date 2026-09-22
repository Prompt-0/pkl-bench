#!/usr/bin/env python3
"""
PKL-Bench: Complete Dataset Builder & Harmonizer for Pro Kabaddi League (Seasons 1-10)
Extracts, harmonizes, validates, and exports multi-tier research datasets in Parquet and CSV formats.
"""

import os
import json
import re
import glob
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np

BASE_RAW_DIR = "/usr/local/lib/python3.14/site-packages/kabaddiPy"
DATA_DIR = Path("/root/code/active/pkl-benchmark/data")

SEASON_DIR_MAP = {
    1: "Season_PKL_Season_1_2014",
    2: "Season_PKL_Season_2_2015",
    3: "Season_PKL_Season_3_2016",
    4: "Season_PKL_Season_4_2016",
    5: "Season_PKL_Season_5_2017",
    6: "Season_PKL_Season_6_2018",
    7: "Season_PKL_Season_7_2019",
    8: "Season_PKL_Season_8_2021",
    9: "Season_PKL_Season_9_2022",
    10: "Season_PKL_Season_10_2023",
}

SEASON_METADATA = [
    {
        "season_id": 1,
        "season_name": "Pro Kabaddi League Season 1, 2014",
        "year": 2014,
        "start_date": "2014-07-26",
        "end_date": "2014-08-31",
        "teams_count": 8,
        "format_type": "Double Round-Robin + Semi-Finals & Final",
        "champion_team_id": 3,
        "champion_team_name": "Jaipur Pink Panthers",
        "runner_up_team_id": 5,
        "runner_up_team_name": "U Mumba",
        "rule_era": "Inaugural PKL Rules (30s raid clock, 3rd empty raid do-or-die, bonus line active >=6 defenders)"
    },
    {
        "season_id": 2,
        "season_name": "Pro Kabaddi League Season 2, 2015",
        "year": 2015,
        "start_date": "2015-07-18",
        "end_date": "2015-08-23",
        "teams_count": 8,
        "format_type": "Double Round-Robin + Semi-Finals & Final",
        "champion_team_id": 5,
        "champion_team_name": "U Mumba",
        "runner_up_team_id": 1,
        "runner_up_team_name": "Bengaluru Bulls",
        "rule_era": "Introduction of Super Tackle (2 pts when <=3 defenders tackle raider)"
    },
    {
        "season_id": 3,
        "season_name": "Pro Kabaddi League Season 3, 2016",
        "year": 2016,
        "start_date": "2016-01-30",
        "end_date": "2016-03-05",
        "teams_count": 8,
        "format_type": "Double Round-Robin + Semi-Finals & Final",
        "champion_team_id": 6,
        "champion_team_name": "Patna Pirates",
        "runner_up_team_id": 5,
        "runner_up_team_name": "U Mumba",
        "rule_era": "Bi-annual edition (Winter 2016)"
    },
    {
        "season_id": 4,
        "season_name": "Pro Kabaddi League Season 4, 2016",
        "year": 2016,
        "start_date": "2016-06-25",
        "end_date": "2016-07-31",
        "teams_count": 8,
        "format_type": "Double Round-Robin + Semi-Finals & Final",
        "champion_team_id": 6,
        "champion_team_name": "Patna Pirates",
        "runner_up_team_id": 3,
        "runner_up_team_name": "Jaipur Pink Panthers",
        "rule_era": "Bi-annual edition (Summer 2016)"
    },
    {
        "season_id": 5,
        "season_name": "Pro Kabaddi League Season 5, 2017",
        "year": 2017,
        "start_date": "2017-07-28",
        "end_date": "2017-10-28",
        "teams_count": 12,
        "format_type": "Zonal System (Zone A & Zone B, 22 matches/team) + Super Playoffs",
        "champion_team_id": 6,
        "champion_team_name": "Patna Pirates",
        "runner_up_team_id": 28,
        "runner_up_team_name": "Gujarat Fortune Giants",
        "rule_era": "Expansion from 8 to 12 franchises; introduction of Zonal division"
    },
    {
        "season_id": 6,
        "season_name": "Pro Kabaddi League Season 6, 2018",
        "year": 2018,
        "start_date": "2018-10-05",
        "end_date": "2019-01-05",
        "teams_count": 12,
        "format_type": "Zonal System (Zone A & Zone B, 22 matches/team) + Super Playoffs",
        "champion_team_id": 1,
        "champion_team_name": "Bengaluru Bulls",
        "runner_up_team_id": 28,
        "runner_up_team_name": "Gujarat Fortune Giants",
        "rule_era": "Zonal System season 2"
    },
    {
        "season_id": 7,
        "season_name": "Pro Kabaddi League Season 7, 2019",
        "year": 2019,
        "start_date": "2019-07-20",
        "end_date": "2019-10-19",
        "teams_count": 12,
        "format_type": "Single Table Double Round-Robin (22 matches/team) + Top 6 Playoffs",
        "champion_team_id": 4,
        "champion_team_name": "Bengal Warriors",
        "runner_up_team_id": 2,
        "runner_up_team_name": "Dabang Delhi K.C.",
        "rule_era": "Reversion to single unified table; top 6 qualify for playoffs"
    },
    {
        "season_id": 8,
        "season_name": "Pro Kabaddi League Season 8, 2021-22",
        "year": 2021,
        "start_date": "2021-12-22",
        "end_date": "2022-02-25",
        "teams_count": 12,
        "format_type": "Single Table Bio-Bubble (Bengaluru Hub) + Top 6 Playoffs",
        "champion_team_id": 2,
        "champion_team_name": "Dabang Delhi K.C.",
        "runner_up_team_id": 6,
        "runner_up_team_name": "Patna Pirates",
        "rule_era": "Post-COVID single-venue bio-bubble hub"
    },
    {
        "season_id": 9,
        "season_name": "Pro Kabaddi League Season 9, 2022",
        "year": 2022,
        "start_date": "2022-10-07",
        "end_date": "2022-12-17",
        "teams_count": 12,
        "format_type": "Single Table Multi-City Caravan + Top 6 Playoffs",
        "champion_team_id": 3,
        "champion_team_name": "Jaipur Pink Panthers",
        "runner_up_team_id": 7,
        "runner_up_team_name": "Puneri Paltan",
        "rule_era": "Multi-city hub return (Bengaluru, Pune, Hyderabad, Mumbai)"
    },
    {
        "season_id": 10,
        "season_name": "Pro Kabaddi League Season 10, 2023-24",
        "year": 2023,
        "start_date": "2023-12-02",
        "end_date": "2024-03-01",
        "teams_count": 12,
        "format_type": "Full 12-City Caravan Format + Top 6 Playoffs",
        "champion_team_id": 7,
        "champion_team_name": "Puneri Paltan",
        "runner_up_team_id": 29,
        "runner_up_team_name": "Haryana Steelers",
        "rule_era": "Decennial 10th season; return to full 12 home-city caravan"
    }
]

TEAM_REGISTRY = {
    1: {"team_name": "Bengaluru Bulls", "short_name": "Bengaluru", "code": "BLR", "city": "Bengaluru", "first_season": 1},
    2: {"team_name": "Dabang Delhi K.C.", "short_name": "Delhi", "code": "DEL", "city": "Delhi", "first_season": 1},
    3: {"team_name": "Jaipur Pink Panthers", "short_name": "Jaipur", "code": "JAI", "city": "Jaipur", "first_season": 1},
    4: {"team_name": "Bengal Warriors", "short_name": "Bengal", "code": "BEN", "city": "Kolkata", "first_season": 1},
    5: {"team_name": "U Mumba", "short_name": "Mumbai", "code": "MUM", "city": "Mumbai", "first_season": 1},
    6: {"team_name": "Patna Pirates", "short_name": "Patna", "code": "PAT", "city": "Patna", "first_season": 1},
    7: {"team_name": "Puneri Paltan", "short_name": "Pune", "code": "PUN", "city": "Pune", "first_season": 1},
    8: {"team_name": "Telugu Titans", "short_name": "Telugu", "code": "HYD", "city": "Hyderabad", "first_season": 1},
    28: {"team_name": "Gujarat Giants", "short_name": "Gujarat", "code": "GUJ", "city": "Ahmedabad", "first_season": 5},
    29: {"team_name": "Haryana Steelers", "short_name": "Haryana", "code": "HAR", "city": "Panchkula", "first_season": 5},
    30: {"team_name": "UP Yoddhas", "short_name": "U.P.", "code": "UP", "city": "Noida", "first_season": 5},
    31: {"team_name": "Tamil Thalaivas", "short_name": "Tamil", "code": "CHE", "city": "Chennai", "first_season": 5},
}

RULESETS = [
    {
        "ruleset_id": "RS_STANDARD_PKL",
        "description": "Standard Pro Kabaddi League match regulations",
        "match_duration_minutes": 40,
        "half_duration_minutes": 20,
        "players_on_court": 7,
        "substitutes_allowed": 5,
        "raid_duration_seconds": 30,
        "do_or_die_threshold": 3,  # 3rd consecutive raid without point
        "bonus_line_min_defenders": 6,
        "super_tackle_max_defenders": 3,
        "super_tackle_points": 2,
        "super_raid_min_points": 3,
        "all_out_extra_points": 2,
        "technical_point_value": 1,
        "tiebreaker_format": "5-5 raids (golden raid in knockout)",
    }
]


def parse_clock_to_seconds(clock_str: Optional[str], half: int) -> int:
    """
    Converts clock MM:SS string and half to total match seconds remaining (0 to 2400).
    Kabaddi match has two 20-minute halves (2400 seconds total).
    In official PKL data:
    Clock often displays MM:SS remaining in that half (e.g., '19:24' means 19m24s remaining in half).
    """
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
        return 1200 if half == 1 else 0


def clean_int(val: Any, default: int = 0) -> int:
    if val is None:
        return default
    try:
        if isinstance(val, (int, float)):
            return int(val) if not np.isnan(val) else default
        val_str = str(val).strip()
        if val_str == "" or val_str.lower() == "nan":
            return default
        return int(float(val_str))
    except Exception:
        return default


def clean_str(val: Any, default: str = "") -> str:
    if val is None:
        return default
    s = str(val).strip()
    return default if s.lower() == "nan" else s


def extract_match_record(root: Dict[str, Any], season_id: int, file_path: str) -> Optional[Dict[str, Any]]:
    md = root.get("match_detail", {})
    teams_list = root.get("teams", {}).get("team", [])
    if len(teams_list) < 2:
        return None

    t1, t2 = teams_list[0], teams_list[1]
    match_id = clean_int(md.get("match_id"))
    if match_id == 0:
        # Try extracting from filename
        m = re.search(r'ID_(\d+)', file_path)
        if m:
            match_id = int(m.group(1))

    match_num = clean_str(md.get("match_number") or md.get("event_name"))
    date_str = clean_str(md.get("date"))
    venue_dict = md.get("venue", {}) if isinstance(md.get("venue"), dict) else {}
    venue_id = clean_int(venue_dict.get("id"))
    venue_name = clean_str(venue_dict.get("name"))

    toss_dict = md.get("toss", {}) if isinstance(md.get("toss"), dict) else {}
    toss_winner_id = clean_int(toss_dict.get("winner"))
    toss_selection = clean_str(toss_dict.get("selection"))

    t1_id = clean_int(t1.get("id"))
    t1_name = clean_str(t1.get("name"))
    t1_score = clean_int(t1.get("score"))
    t1_stats = t1.get("stats", {}) or {}
    t1_pts = t1_stats.get("points", {}) or {}
    t1_raids = t1_stats.get("raids", {}) or {}
    t1_tackles = t1_stats.get("tackles", {}) or {}

    t2_id = clean_int(t2.get("id"))
    t2_name = clean_str(t2.get("name"))
    t2_score = clean_int(t2.get("score"))
    t2_stats = t2_stats = t2.get("stats", {}) or {}
    t2_pts = t2_stats.get("points", {}) or {}
    t2_raids = t2_stats.get("raids", {}) or {}
    t2_tackles = t2_stats.get("tackles", {}) or {}

    # Winner logic
    is_tie = (t1_score == t2_score)
    margin = abs(t1_score - t2_score)
    if is_tie:
        winner_id = None
        winner_name = "Tie"
    elif t1_score > t2_score:
        winner_id = t1_id
        winner_name = t1_name
    else:
        winner_id = t2_id
        winner_name = t2_name

    # Points breakdown helper
    def get_points(p_dict):
        r_dict = p_dict.get("raid_points", {}) if isinstance(p_dict.get("raid_points"), dict) else {}
        t_dict = p_dict.get("tackle_points", {}) if isinstance(p_dict.get("tackle_points"), dict) else {}
        raid_pts = clean_int(r_dict.get("total") if isinstance(r_dict, dict) else p_dict.get("raid_points"))
        tackle_pts = clean_int(t_dict.get("total") if isinstance(t_dict, dict) else p_dict.get("tackle_points"))
        all_out_pts = clean_int(p_dict.get("all_out"))
        extra_pts = clean_int(p_dict.get("extras"))
        return raid_pts, tackle_pts, all_out_pts, extra_pts

    t1_raid_pts, t1_tackle_pts, t1_ao_pts, t1_ext_pts = get_points(t1_pts)
    t2_raid_pts, t2_tackle_pts, t2_ao_pts, t2_ext_pts = get_points(t2_pts)

    stage = clean_str(md.get("stage") or "League")

    return {
        "match_id": match_id,
        "season_id": season_id,
        "match_number": match_num,
        "match_date": date_str,
        "stage": stage,
        "venue_id": venue_id,
        "venue_name": venue_name,
        "team1_id": t1_id,
        "team1_name": t1_name,
        "team2_id": t2_id,
        "team2_name": t2_name,
        "toss_winner_id": toss_winner_id,
        "toss_selection": toss_selection,
        "team1_score": t1_score,
        "team2_score": t2_score,
        "winner_id": winner_id,
        "winning_team_name": winner_name,
        "score_margin": margin,
        "is_tie": is_tie,
        "team1_raid_points": t1_raid_pts,
        "team1_tackle_points": t1_tackle_pts,
        "team1_all_out_points": t1_ao_pts,
        "team1_extra_points": t1_ext_pts,
        "team2_raid_points": t2_raid_pts,
        "team2_tackle_points": t2_tackle_pts,
        "team2_all_out_points": t2_ao_pts,
        "team2_extra_points": t2_ext_pts,
        "team1_raids_total": clean_int(t1_raids.get("total")),
        "team1_raids_successful": clean_int(t1_raids.get("successful")),
        "team1_raids_unsuccessful": clean_int(t1_raids.get("unsuccessful")),
        "team1_raids_empty": clean_int(t1_raids.get("Empty") or t1_raids.get("empty")),
        "team1_super_raids": clean_int(t1_raids.get("super_raids")),
        "team2_raids_total": clean_int(t2_raids.get("total")),
        "team2_raids_successful": clean_int(t2_raids.get("successful")),
        "team2_raids_unsuccessful": clean_int(t2_raids.get("unsuccessful")),
        "team2_raids_empty": clean_int(t2_raids.get("Empty") or t2_raids.get("empty")),
        "team2_super_raids": clean_int(t2_raids.get("super_raids")),
        "team1_tackles_total": clean_int(t1_tackles.get("total")),
        "team1_tackles_successful": clean_int(t1_tackles.get("successful")),
        "team1_super_tackles": clean_int(t1_tackles.get("super_tackles")),
        "team2_tackles_total": clean_int(t2_tackles.get("total")),
        "team2_tackles_successful": clean_int(t2_tackles.get("successful")),
        "team2_super_tackles": clean_int(t2_tackles.get("super_tackles")),
        "team1_all_outs": clean_int(t1_stats.get("all_outs")),
        "team2_all_outs": clean_int(t2_stats.get("all_outs")),
    }


def extract_player_matches(root: Dict[str, Any], match_id: int, season_id: int) -> List[Dict[str, Any]]:
    records = []
    teams_list = root.get("teams", {}).get("team", [])
    for t in teams_list:
        team_id = clean_int(t.get("id"))
        for p in t.get("squad", []):
            p_id = clean_int(p.get("id"))
            if p_id == 0:
                continue
            pts = p.get("points", {}) or {}
            r_pts = pts.get("raid_points", {}) or {}
            t_pts = pts.get("tackle_points", {}) or {}
            raids = p.get("raids", {}) or {}
            tackles = p.get("tackles", {}) or {}

            played = bool(p.get("played", False))
            starter = bool(p.get("starter", False))
            captain = bool(p.get("captain", False))

            tot_pts = clean_int(pts.get("total"))
            raid_tot = clean_int(r_pts.get("total") if isinstance(r_pts, dict) else r_pts)
            raid_touch = clean_int(r_pts.get("touch") if isinstance(r_pts, dict) else 0)
            raid_bonus = clean_int(r_pts.get("raid_bonus") if isinstance(r_pts, dict) else 0)

            tackle_tot = clean_int(t_pts.get("total") if isinstance(t_pts, dict) else t_pts)
            tackle_capture = clean_int(t_pts.get("capture") if isinstance(t_pts, dict) else 0)

            super_10 = (raid_tot >= 10)
            high_5 = (tackle_tot >= 5)

            records.append({
                "match_id": match_id,
                "season_id": season_id,
                "team_id": team_id,
                "player_id": p_id,
                "player_name": clean_str(p.get("name")),
                "jersey_no": clean_str(p.get("jersey")),
                "role": clean_str(p.get("role")),
                "skill": clean_str(p.get("skill")),
                "played": played,
                "starter": starter,
                "captain": captain,
                "total_points": tot_pts,
                "raid_points_total": raid_tot,
                "raid_touch_points": raid_touch,
                "raid_bonus_points": raid_bonus,
                "raids_total": clean_int(raids.get("total")),
                "raids_successful": clean_int(raids.get("successful")),
                "raids_unsuccessful": clean_int(raids.get("unsuccessful")),
                "raids_empty": clean_int(raids.get("Empty") or raids.get("empty")),
                "super_raids": clean_int(raids.get("super_raids")),
                "tackle_points_total": tackle_tot,
                "tackles_total": clean_int(tackles.get("total")),
                "tackles_successful": clean_int(tackles.get("successful")),
                "tackles_unsuccessful": clean_int(tackles.get("unsuccessful")),
                "super_tackles": clean_int(tackles.get("super_tackles")),
                "super_10": super_10,
                "high_5": high_5,
                "green_cards": clean_int(p.get("green_card_count")),
                "yellow_cards": clean_int(p.get("yellow_card_count")),
                "red_cards": clean_int(p.get("red_card_count")),
            })
    return records


def extract_raids_pbp(root: Dict[str, Any], match_id: int, season_id: int, player_name_map: Dict[int, str]) -> List[Dict[str, Any]]:
    """
    Extracts chronologically sequenced raid events from the match.
    Harmonizes event classifications and tracks live scores and defender estimates.
    """
    events_raw = []
    # Check if events list is in root['events']['event']
    ev_dict = root.get("events", {})
    if isinstance(ev_dict, dict) and "event" in ev_dict:
        events_raw = ev_dict["event"]
    elif isinstance(ev_dict, list):
        events_raw = ev_dict

    # Fallback: if root events is empty, gather from player squads
    if not events_raw:
        seen_seq = set()
        teams_list = root.get("teams", {}).get("team", [])
        for t in teams_list:
            for p in t.get("squad", []):
                for ev in p.get("events", []):
                    s = ev.get("event_no") or ev.get("seq_no")
                    if s not in seen_seq:
                        seen_seq.add(s)
                        events_raw.append(ev)

    if not events_raw:
        return []

    # Sort events by sequence number
    def get_seq(e):
        return clean_int(e.get("event_no") or e.get("seq_no") or 0)
    events_sorted = sorted(events_raw, key=get_seq)

    raids = []
    # Track state
    curr_score_t1 = 0
    curr_score_t2 = 0

    for idx, ev in enumerate(events_sorted):
        seq_no = clean_int(ev.get("event_no") or ev.get("seq_no") or (idx + 1))
        half = clean_int(ev.get("event_half") or 1)
        clock_str = clean_str(ev.get("clock"))
        seconds_left = parse_clock_to_seconds(clock_str, half)

        raider_id = clean_int(ev.get("raider_id"))
        raiding_team_id = clean_int(ev.get("raiding_team_id"))
        defending_team_id = clean_int(ev.get("defending_team_id"))
        defender_id = clean_int(ev.get("defender_id")) or None

        raw_event_name = clean_str(ev.get("event")).upper()
        event_text = clean_str(ev.get("event_text"))

        raid_pts = clean_int(ev.get("raid_points"))
        raid_touch = clean_int(ev.get("raid_touch_points"))
        raid_bonus = clean_int(ev.get("raid_bonus_points"))
        def_pts = clean_int(ev.get("defending_points") or ev.get("defending_capture_points"))

        is_dod = bool(ev.get("do_or_die", False))
        is_super_raid = bool(ev.get("super_raid", False) or raid_pts >= 3)
        is_super_tackle = bool(ev.get("super_tackle", False) or (def_pts >= 2 and raid_pts == 0))

        # Outcome categorization
        if "EMPTY" in raw_event_name:
            outcome_category = "EMPTY_RAID"
        elif is_super_raid:
            outcome_category = "SUPER_RAID"
        elif is_super_tackle:
            outcome_category = "SUPER_TACKLE"
        elif "UNSUCCESSFUL" in raw_event_name or def_pts > 0:
            outcome_category = "UNSUCCESSFUL_RAID"
        elif "SUCCESSFUL" in raw_event_name or raid_pts > 0:
            outcome_category = "SUCCESSFUL_RAID"
        else:
            outcome_category = "EMPTY_RAID" if (raid_pts == 0 and def_pts == 0) else "OTHER"

        # Score parsing
        ev_score = ev.get("score")
        score_t1_after = None
        score_t2_after = None
        if isinstance(ev_score, list) and len(ev_score) == 2:
            score_t1_after = clean_int(ev_score[0])
            score_t2_after = clean_int(ev_score[1])
        elif isinstance(ev_score, dict):
            score_t1_after = clean_int(ev_score.get("team1"))
            score_t2_after = clean_int(ev_score.get("team2"))

        # Score diff relative to raiding team
        score_diff_after = None
        if score_t1_after is not None and score_t2_after is not None:
            # Check which team is raiding team
            # Let's see: ev_score usually corresponds to team 1 and team 2
            curr_score_t1 = score_t1_after
            curr_score_t2 = score_t2_after

        # Raider name
        raider_name = player_name_map.get(raider_id, clean_str(ev.get("raider_name") or ""))
        if not raider_name and event_text:
            # Fallback raider name extraction from event_text
            raider_name = event_text.split("raid")[0].split("raids")[0].strip()

        defender_name = player_name_map.get(defender_id) if defender_id else None

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
            "team1_score_after": curr_score_t1,
            "team2_score_after": curr_score_t2,
            "event_text": event_text
        })
    return raids


def run_pipeline():
    print("=" * 70)
    print("PKL-BENCH: Research Dataset Generation Pipeline")
    print("=" * 70)

    matches_list = []
    player_matches_list = []
    raids_pbp_list = []
    venues_dict = {}
    player_registry = {}  # id -> {name, role, career_stats...}

    # Step 1: Scan and parse all seasons
    total_files_scanned = 0
    total_matches_parsed = 0

    for season_id, season_folder in sorted(SEASON_DIR_MAP.items()):
        folder_path = os.path.join(BASE_RAW_DIR, "MatchData_pbp", season_folder)
        if not os.path.exists(folder_path):
            print(f"Warning: Folder {folder_path} does not exist!")
            continue

        json_files = sorted(glob.glob(os.path.join(folder_path, "*.json")))
        print(f"Season {season_id:02d} ({season_folder}): Found {len(json_files)} match files.")

        for fpath in json_files:
            total_files_scanned += 1
            try:
                with open(fpath, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
            except Exception as e:
                print(f"Error reading {fpath}: {e}")
                continue

            root = data.get("gameData", data)

            # Match record
            match_rec = extract_match_record(root, season_id, fpath)
            if not match_rec:
                continue

            match_id = match_rec["match_id"]
            matches_list.append(match_rec)
            total_matches_parsed += 1

            # Track venues
            v_id = match_rec["venue_id"]
            v_name = match_rec["venue_name"]
            if v_name:
                if v_id not in venues_dict:
                    # extract city from name if possible
                    city = v_name.split(",")[-1].strip() if "," in v_name else v_name
                    venues_dict[v_id] = {
                        "venue_id": v_id,
                        "venue_name": v_name,
                        "city": city,
                        "matches_hosted": 1
                    }
                else:
                    venues_dict[v_id]["matches_hosted"] += 1

            # Player match records
            pm_recs = extract_player_matches(root, match_id, season_id)
            player_matches_list.extend(pm_recs)

            # Build player registry
            player_names = {}
            for pm in pm_recs:
                pid = pm["player_id"]
                pname = pm["player_name"]
                player_names[pid] = pname
                if pid not in player_registry:
                    player_registry[pid] = {
                        "player_id": pid,
                        "player_name": pname,
                        "role": pm["role"],
                        "first_season": season_id,
                        "latest_season": season_id,
                        "career_matches": 1 if pm["played"] else 0,
                        "career_raid_points": pm["raid_points_total"],
                        "career_tackle_points": pm["tackle_points_total"],
                        "career_total_points": pm["total_points"],
                        "career_super_raids": pm["super_raids"],
                        "career_super_10s": 1 if pm["super_10"] else 0,
                        "career_high_5s": 1 if pm["high_5"] else 0,
                        "career_super_tackles": pm["super_tackles"],
                    }
                else:
                    reg = player_registry[pid]
                    reg["latest_season"] = max(reg["latest_season"], season_id)
                    if pm["played"]:
                        reg["career_matches"] += 1
                    reg["career_raid_points"] += pm["raid_points_total"]
                    reg["career_tackle_points"] += pm["tackle_points_total"]
                    reg["career_total_points"] += pm["total_points"]
                    reg["career_super_raids"] += pm["super_raids"]
                    if pm["super_10"]:
                        reg["career_super_10s"] += 1
                    if pm["high_5"]:
                        reg["career_high_5s"] += 1
                    reg["career_super_tackles"] += pm["super_tackles"]
                    if not reg["role"] and pm["role"]:
                        reg["role"] = pm["role"]

            # Raids PBP
            raids = extract_raids_pbp(root, match_id, season_id, player_names)
            raids_pbp_list.extend(raids)

    print(f"\nProcessing Complete:")
    print(f"  Total JSON files scanned: {total_files_scanned}")
    print(f"  Total matches extracted: {total_matches_parsed}")
    print(f"  Total player match appearances: {len(player_matches_list)}")
    print(f"  Total discrete raid events: {len(raids_pbp_list)}")
    print(f"  Total unique players registered: {len(player_registry)}")
    print(f"  Total unique venues recorded: {len(venues_dict)}")

    # Convert to DataFrames
    df_matches = pd.DataFrame(matches_list)
    df_player_matches = pd.DataFrame(player_matches_list)
    df_raids = pd.DataFrame(raids_pbp_list)
    df_seasons = pd.DataFrame(SEASON_METADATA)
    df_rulesets = pd.DataFrame(RULESETS)

    teams_data = []
    for tid, tinfo in sorted(TEAM_REGISTRY.items()):
        teams_data.append({
            "team_id": tid,
            "team_name": tinfo["team_name"],
            "short_name": tinfo["short_name"],
            "team_code": tinfo["code"],
            "home_city": tinfo["city"],
            "first_season": tinfo["first_season"]
        })
    df_teams = pd.DataFrame(teams_data)
    df_venues = pd.DataFrame(list(venues_dict.values())).sort_values("matches_hosted", ascending=False)
    df_players = pd.DataFrame(list(player_registry.values())).sort_values("career_total_points", ascending=False)

    # Ingest external player auction / career data if available
    auction_csv_path = os.path.join(BASE_RAW_DIR, "Player-Wise-Data", "Player_Team_Lineup_merged.csv")
    if os.path.exists(auction_csv_path):
        df_lineups = pd.read_csv(auction_csv_path)
        print(f"Loaded player lineup records: {len(df_lineups)}")
    else:
        df_lineups = pd.DataFrame()

    # Deduplicate matches by match_id if any duplicate files existed
    orig_match_len = len(df_matches)
    df_matches = df_matches.drop_duplicates(subset=["match_id"]).sort_values(["season_id", "match_id"]).reset_index(drop=True)
    if len(df_matches) < orig_match_len:
        print(f"Deduplicated matches from {orig_match_len} to {len(df_matches)}")

    # Step 2: Build Standard Benchmark Splits
    # Temporal Split:
    # Train: Seasons 1-8 (2014-2022)
    # Val: Season 9 (2022)
    # Test: Season 10 (2023-2024)
    train_match_ids = df_matches[df_matches["season_id"] <= 8]["match_id"].tolist()
    val_match_ids = df_matches[df_matches["season_id"] == 9]["match_id"].tolist()
    test_match_ids = df_matches[df_matches["season_id"] == 10]["match_id"].tolist()

    splits_dict = {
        "description": "PKL-Bench Official Temporal Leakage-Free Splits",
        "protocol": "Strict temporal ordering (Train <= S8, Val = S9, Test = S10) to prevent lookahead leakage",
        "train": {
            "seasons": [1, 2, 3, 4, 5, 6, 7, 8],
            "num_matches": len(train_match_ids),
            "match_ids": train_match_ids
        },
        "validation": {
            "seasons": [9],
            "num_matches": len(val_match_ids),
            "match_ids": val_match_ids
        },
        "test": {
            "seasons": [10],
            "num_matches": len(test_match_ids),
            "match_ids": test_match_ids
        }
    }

    # Step 3: Export Datasets to Parquet and CSV
    export_manifest = [
        ("metadata/seasons", df_seasons),
        ("metadata/teams", df_teams),
        ("metadata/venues", df_venues),
        ("metadata/rulesets", df_rulesets),
        ("matches/matches", df_matches),
        ("players/players", df_players),
        ("player_matches/player_match_stats", df_player_matches),
        ("raids_pbp/raids_pbp", df_raids),
    ]

    print("\nExporting Datasets to Parquet and CSV...")
    for rel_path, df in export_manifest:
        out_p = DATA_DIR / f"{rel_path}.parquet"
        out_c = DATA_DIR / f"{rel_path}.csv"
        out_p.parent.mkdir(parents=True, exist_ok=True)

        # Write Parquet with Snappy compression
        df.to_parquet(out_p, compression="snappy", index=False)
        # Write CSV
        df.to_csv(out_c, index=False)

        size_parquet_mb = out_p.stat().st_size / (1024 * 1024)
        size_csv_mb = out_c.stat().st_size / (1024 * 1024)
        print(f"  ✓ {rel_path:35s}: {len(df):7d} rows | Parquet: {size_parquet_mb:6.2f} MB | CSV: {size_csv_mb:6.2f} MB")

    # Export splits.json
    splits_file = DATA_DIR / "benchmark_splits" / "splits.json"
    splits_file.parent.mkdir(parents=True, exist_ok=True)
    with open(splits_file, "w") as fp:
        json.dump(splits_dict, fp, indent=2)
    print(f"  ✓ benchmark_splits/splits.json: {splits_file.stat().st_size / 1024:.1f} KB")

    print("\n" + "=" * 70)
    print("PKL-BENCH DATASET GENERATION SUCCESSFUL!")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
