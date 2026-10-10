"""
Project-wide constants and paths.
Import from here instead of hardcoding paths/ids in individual scripts.
"""
from pathlib import Path

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_INTERIM = PROJECT_ROOT / "data" / "interim"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_EXTERNAL = PROJECT_ROOT / "data" / "external"
OUTPUTS_FIGURES = PROJECT_ROOT / "outputs" / "figures"
OUTPUTS_REPORTS = PROJECT_ROOT / "outputs" / "reports"

# --- StatsBomb: Bundesliga 2023/24 (Bayer Leverkusen unbeaten season) ---
# Confirmed via sb.competitions() — do not change unless switching dataset.
BUNDESLIGA_COMPETITION_ID = 9
BUNDESLIGA_2023_24_SEASON_ID = 281

# --- Canonical column names we depend on downstream ---
# If StatsBomb ever changes their schema, this is the one place to update.
REQUIRED_EVENT_FIELDS = [
    "match_id", "id", "index", "period", "timestamp", "minute", "second",
    "type", "possession", "possession_team", "play_pattern", "team",
    "player", "player_id", "position", "location", "duration",
    "under_pressure", "related_events",
    "pass_recipient", "pass_recipient_id", "pass_length", "pass_angle",
    "pass_end_location", "pass_outcome", "pass_type", "pass_height",
    "shot_statsbomb_xg", "shot_outcome", "shot_end_location", "shot_body_part",
]

for _p in (DATA_RAW, DATA_INTERIM, DATA_PROCESSED, DATA_EXTERNAL, OUTPUTS_FIGURES, OUTPUTS_REPORTS):
    _p.mkdir(parents=True, exist_ok=True)
