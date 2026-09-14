# SquadSync

Football Intelligence Platform — B.Tech Major Project
Team: Suvrat Joshi, Sushant Jaiswal, Shivam Venkatesh · Mentor: Prof. Lalit Sachan

See [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) for the full phase-by-phase roadmap
and repo structure explanation, and [`docs/architecture.md`](./docs/architecture.md)
for the canonical data schema.

## Setup (do this first, before writing any analysis code)

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd squadsync

# 2. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Confirm your environment can actually pull data
python scripts/test_environment.py
```

You should see three `[OK]` lines ending in "Environment ready." If anything
fails, fix it before starting Phase 1/2 work — don't debug data access issues
in the middle of writing analysis code.

## Data Source

Primary dataset: **StatsBomb Open Data — Bayer Leverkusen's unbeaten 2023/24
Bundesliga title-winning season** (34 matches, full event data). Free,
requires no download step — pulled live via `statsbombpy` and cached locally
in `data/raw/` (gitignored, not shared via git).

Full dataset reference (all sources, links, and access notes) is in
[`docs/dataset_reference.md`](./docs/dataset_reference.md).

## Project Structure

See [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) section 2 for the full folder
layout and reasoning. Quick orientation:

- `src/squadsync/data/` — data loading (start here, Phase 1-2)
- `src/squadsync/tactical/` — passing networks, formations (Phase 6)
- `src/squadsync/models/` — prediction models (Phase 5, 7)
- `src/squadsync/decision/` — decision-support layer (Phase 8)
- `src/squadsync/assistant/` — orchestration/LLM layer (Phase 5 scaffold → 9)
- `notebooks/` — exploration and prototyping
- `docs/` — architecture, dataset reference, evaluation framework

## Current Phase

**Phase 2 — Data Acquisition & Canonical Data Model. In progress / core built.**
`squadsync.data.build_canonical` produces `data/processed/matches.parquet`,
`events.parquet`, and `players.parquet` from the full 34-match season —
verified working (137,765 events, 372 players, 39,214 passes). Next: agree
on any remaining schema tweaks (see "Open Questions" in `docs/architecture.md`),
then move to Phase 3 (EDA & baseline statistical intelligence).
