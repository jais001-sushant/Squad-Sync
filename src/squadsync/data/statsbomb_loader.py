"""
StatsBomb Open Data loader for SquadSync.

Wraps statsbombpy so the rest of the codebase never touches raw StatsBomb
calls directly — if StatsBomb's API changes, this is the one file to fix.

Usage:
    from squadsync.data.statsbomb_loader import get_matches, get_match_events

    matches = get_matches()
    events = get_match_events(matches.iloc[0]["match_id"])
"""
import warnings
import pandas as pd
from statsbombpy import sb

from squadsync.config import (
    BUNDESLIGA_COMPETITION_ID,
    BUNDESLIGA_2023_24_SEASON_ID,
    DATA_RAW,
)

# StatsBomb's free open data intentionally omits some fields (e.g. competition
# stage) that trigger noisy warnings in statsbombpy — safe to silence for our use case.
warnings.filterwarnings("ignore", category=UserWarning)


def get_matches(
    competition_id: int = BUNDESLIGA_COMPETITION_ID,
    season_id: int = BUNDESLIGA_2023_24_SEASON_ID,
) -> pd.DataFrame:
    """Return the match list for a competition/season. Defaults to Leverkusen's
    2023/24 unbeaten Bundesliga season (our Phase 1-2 working dataset)."""
    return sb.matches(competition_id=competition_id, season_id=season_id)


def get_match_events(match_id: int, cache: bool = True) -> pd.DataFrame:
    """Return event data for a single match. Caches raw pulls to data/raw/
    as Parquet so we don't re-hit StatsBomb every run during development."""
    cache_path = DATA_RAW / f"events_{match_id}.parquet"
    if cache and cache_path.exists():
        return pd.read_parquet(cache_path)

    events = sb.events(match_id=match_id)
    if cache:
        events.to_parquet(cache_path, index=False)
    return events


def get_all_season_events(
    competition_id: int = BUNDESLIGA_COMPETITION_ID,
    season_id: int = BUNDESLIGA_2023_24_SEASON_ID,
    cache: bool = True,
) -> pd.DataFrame:
    """Pull and concatenate events for every match in a season.
    Warning: this is 34 matches for the Leverkusen dataset — first run will
    take a few minutes; subsequent runs use the per-match cache."""
    matches = get_matches(competition_id, season_id)
    all_events = []
    for match_id in matches["match_id"]:
        events = get_match_events(match_id, cache=cache)
        all_events.append(events)
    return pd.concat(all_events, ignore_index=True)


if __name__ == "__main__":
    # Quick manual check: run `python -m squadsync.data.statsbomb_loader`
    matches = get_matches()
    print(f"Matches available: {len(matches)}")
    sample_events = get_match_events(matches.iloc[0]["match_id"])
    print(f"Events in first match: {len(sample_events)}")
    print(f"Columns: {len(sample_events.columns)}")
