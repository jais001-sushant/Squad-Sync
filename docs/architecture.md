# SquadSync — Architecture & Canonical Data Model

This is the schema reference for Phase 2. Verified against a live pull of
StatsBomb's Bayer Leverkusen 2023/24 dataset — not theoretical.

## Confirmed Data Access

- Competition: Bundesliga (`competition_id = 9`)
- Season: 2023/2024 (`season_id = 281`)
- Matches available: **34** (Leverkusen's full unbeaten title-winning season)
- Events per match: ~3,800–4,000
- Columns per event: 91

Verified via `squadsync.data.statsbomb_loader.get_matches()` and `get_match_events()`.

## Canonical Event Fields (Phase 2 target schema)

These are the StatsBomb columns our downstream modules depend on. Field names
match StatsBomb's raw schema exactly (no renaming) to avoid a translation
layer that could silently drift out of sync.

| Field | Type | Used By |
|---|---|---|
| `match_id` | int | all modules — join key |
| `id` | str (uuid) | event identifier |
| `index` | int | event order within match |
| `period`, `minute`, `second`, `timestamp` | int/str | time-based filtering (e.g. first half only) |
| `type` | str | event type (Pass, Shot, Duel, etc.) — primary filter |
| `possession`, `possession_team` | int/str | possession-based analysis |
| `play_pattern` | str | build-up pattern classification (Phase 6) |
| `team`, `player`, `player_id`, `position` | str/int | attribution — who did what |
| `location` | [x, y] | spatial analysis, passing network node positions |
| `duration` | float | event duration |
| `under_pressure` | bool | pressing intensity (Phase 6 stretch goal) |
| `pass_recipient`, `pass_recipient_id` | str/int | **passing network edges** |
| `pass_length`, `pass_angle`, `pass_end_location` | float/[x,y] | pass characteristics |
| `pass_outcome` | str | completed vs incomplete (null = completed) |
| `pass_type`, `pass_height` | str | pass classification |
| `shot_statsbomb_xg` | float | xG — statistical + predictive layers |
| `shot_outcome`, `shot_end_location`, `shot_body_part` | str/[x,y] | shot analysis |

Full column list (91 fields) is available by running:
```python
from squadsung.data.statsbomb_loader import get_match_events
events = get_match_events(match_id=3895292)
print(sorted(events.columns.tolist()))
```

## Storage Convention

- **`data/raw/`** — untouched per-match Parquet caches of StatsBomb pulls
  (e.g. `events_3895292.parquet`). Gitignored — everyone generates their own
  via `statsbomb_loader.py`.
- **`data/processed/`** — cleaned, joined tables ready for feature engineering
  (Phase 4) and modeling (Phase 5+). This is what Phase 3 (EDA) and beyond
  should read from, not `data/raw/` directly.
- **`data/external/`** — small, committed reference files (e.g. team name
  normalization mappings) — these ARE checked into git since they're tiny
  and needed by everyone.

## Module → Phase Mapping

| Module (`src/squadsync/`) | Phase | Reads From |
|---|---|---|
| `data/` | 1–2 | StatsBomb API, football-data.org |
| `features/` | 4 | `data/processed/` |
| `models/` | 5, 7 | `features/` output |
| `tactical/` | 6 | `data/processed/` (event-level, needs `location`/`pass_recipient`) |
| `decision/` | 8 | `models/` + `tactical/` output |
| `assistant/` | 5 (scaffold), 9 (full) | all of the above, via tool calls |

## Open Questions (revisit as we go)

- Do we need `pass_end_location`/`shot_end_location` unpacked into separate
  x/y columns during Phase 2 cleaning, or keep as list-in-cell? (Recommend:
  unpack during cleaning — easier for pandas filtering later.)
- Football-data.org sync job (Phase 2) writes to a separate table or merges
  into the same `data/processed/` matches table? (Recommend: separate table,
  joined by team name + date, since StatsBomb and football-data.org won't
  share match IDs.)
