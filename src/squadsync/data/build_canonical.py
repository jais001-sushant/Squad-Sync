"""
Phase 2 — Canonical Data Model Builder.

Pulls every match in the configured season, cleans the raw StatsBomb event
data, and writes three canonical tables to data/processed/ that every other
module (tactical, models, decision, assistant) reads from.

This is the ONE place raw StatsBomb quirks get handled — nothing downstream
should ever need to know about StatsBomb's specific column formats.

Run from project root:
    PYTHONPATH=src python -m squadsync.data.build_canonical
"""
import pandas as pd

from squadsync.config import DATA_PROCESSED
from squadsync.data.statsbomb_loader import get_matches, get_match_events


def build_matches_table() -> pd.DataFrame:
    """Canonical matches table: one row per match, clean column names."""
    matches = get_matches()
    canonical = matches[[
        "match_id", "match_date", "kick_off",
        "home_team", "away_team", "home_score", "away_score",
        "competition", "season", "referee",
    ]].copy()
    canonical["result"] = canonical.apply(
        lambda r: "home_win" if r["home_score"] > r["away_score"]
        else ("away_win" if r["away_score"] > r["home_score"] else "draw"),
        axis=1,
    )
    return canonical


def build_events_table(match_ids: list[int]) -> pd.DataFrame:
    """Canonical events table across all matches, with location split into
    separate x/y columns (easier for pandas filtering than list-in-cell)."""
    all_events = []
    for i, match_id in enumerate(match_ids, 1):
        print(f"  [{i}/{len(match_ids)}] loading match {match_id}...")
        events = get_match_events(match_id)
        all_events.append(events)
    events = pd.concat(all_events, ignore_index=True)

    # Split location fields into x/y — StatsBomb stores these as [x, y] lists
    for col in ["location", "pass_end_location", "shot_end_location"]:
        if col in events.columns:
            events[f"{col}_x"] = events[col].apply(lambda v: v[0] if v is not None and len(v) == 2 else None)
            events[f"{col}_y"] = events[col].apply(lambda v: v[1] if v is not None and len(v) == 2 else None)

    keep_cols = [
        "match_id", "id", "index", "period", "timestamp", "minute", "second",
        "type", "possession", "possession_team", "play_pattern",
        "team", "player", "player_id", "position",
        "location_x", "location_y", "duration", "under_pressure",
        "pass_recipient", "pass_recipient_id", "pass_length", "pass_angle",
        "pass_end_location_x", "pass_end_location_y", "pass_outcome",
        "pass_type", "pass_height",
        "shot_statsbomb_xg", "shot_outcome",
        "shot_end_location_x", "shot_end_location_y", "shot_body_part",
    ]
    return events[[c for c in keep_cols if c in events.columns]]


def build_players_table(events: pd.DataFrame) -> pd.DataFrame:
    """Canonical players table: one row per player, derived from event data."""
    players = (
        events.dropna(subset=["player_id"])
        [["player_id", "player", "team"]]
        .drop_duplicates(subset=["player_id"])
        .reset_index(drop=True)
    )
    return players


def main():
    print("Building canonical matches table...")
    matches = build_matches_table()
    matches.to_parquet(DATA_PROCESSED / "matches.parquet", index=False)
    print(f"  -> {len(matches)} matches saved to data/processed/matches.parquet")

    print("\nBuilding canonical events table (this pulls all matches, uses cache after first run)...")
    events = build_events_table(matches["match_id"].tolist())
    events.to_parquet(DATA_PROCESSED / "events.parquet", index=False)
    print(f"  -> {len(events)} events saved to data/processed/events.parquet")

    print("\nBuilding canonical players table...")
    players = build_players_table(events)
    players.to_parquet(DATA_PROCESSED / "players.parquet", index=False)
    print(f"  -> {len(players)} players saved to data/processed/players.parquet")

    print("\nDone. All modules should now read from data/processed/, not data/raw/.")


if __name__ == "__main__":
    main()