# SquadSync — Project Plan & Repo Structure

Football Intelligence Platform — B.Tech Major Project
Team: Suvrat Joshi, Sushant Jaiswal, Shivam Venkatesh · Mentor: Prof. Lalit Sachan

This document is the single source of truth for how the project is structured and
sequenced. Update it as we go — if something changes, edit this file in the same PR
as the code change that caused it.

---

## 0. Core Principle

> The core platform must remain fully viable even if every advanced module is dropped.

Every phase below produces something that **runs and can be shown**, not just code that
compiles. If a phase isn't demoable, it isn't done.

---

## 1. Phase-by-Phase Plan (20 Weeks)

### Phase 1 — Requirements & Data Evaluation (Weeks 1–2)
**Goal:** Agree on scope, confirm data sources actually give us what the architecture needs.

- Finalize the dataset stack (already decided): StatsBomb Open Data (core), Football-Data.co.uk
  (baseline), football-data.org (sync), Wyscout public dataset (backup)
- Every teammate: get StatsBomb resource-centre access + confirm `statsbombpy` pulls data locally
- Explore the Bayer Leverkusen 2023/24 free dataset (already in use — see teammate's passing
  network) as our first working dataset
- Write down exact fields we need from StatsBomb events (player, team, x/y location, pass
  outcome, timestamp, etc.)

**Deliverable:** A short data-availability note confirming StatsBomb's fields cover our
planned Statistical + Tactical layers.

---

### Phase 2 — Data Acquisition & Canonical Data Model (Weeks 3–4)
**Goal:** One shared schema everyone's code reads from and writes to. This is the phase
that prevents three people building on three different assumptions.

- Build the ingestion script: StatsBomb JSON → cleaned tables (matches, events, players, teams)
- Store as Parquet files or a local SQLite DB under `data/processed/` — no need for Postgres yet
- Define the canonical schema in `docs/architecture.md` (table names, columns, types)
- Add the football-data.org sync script (scheduled pull for current fixtures/results)

**Deliverable:** `src/squadsync/data/` module that any teammate can import and get clean
DataFrames from — no one touches raw StatsBomb JSON directly after this phase.

---

### Phase 3 — EDA & Baseline Statistical Intelligence (Weeks 5–6)
**Goal:** Answer "what happened?" — Level 1 of the Intelligence Hierarchy.

- Match-level stats: possession, shots, xG, passing accuracy
- Player-level stats: minutes, touches, pass completion, defensive actions
- Team-level stats: formation usage, aggregate patterns across matches

**Deliverable:** A statistical dashboard/notebook covering the full Leverkusen dataset
(not just one match), reproducible by anyone on the team.

---

### Phase 4 — Feature Engineering (Weeks 7–8)
**Goal:** Turn raw events into model-ready features for everything downstream.

- Rolling-window team form (last 5 matches: goals, xG, results)
- Player-level rolling performance features
- Match context features: home/away, rest days, opponent strength

**Deliverable:** A reusable `features/` pipeline that both the ML models (Phase 5) and the
tactical modules (Phase 6) can pull from.

---

### Phase 5 — Baseline Predictive Models + Assistant Scaffolding Starts (Weeks 9–10)
**Goal:** First working prediction model, and start the thin Assistant shell in parallel
(per our earlier plan — don't leave this until Week 17).

- Baseline match-outcome model (Win/Draw/Loss) using Football-Data.co.uk + engineered features
- Probabilistic output: P(Win) + P(Draw) + P(Loss) = 1, not a single hard answer
- **In parallel:** scaffold the Assistant shell — LLM + basic tool-calling into whatever
  modules exist so far (even just "give me Team X's stats"). This is intentionally dumb
  right now; it just needs to exist so Week 17–18 is integration, not a from-scratch build.

**Deliverable:** A baseline prediction model with an accuracy/F1 benchmark, and a
skeleton Assistant that can answer one simple stats question end-to-end.

---

### Phase 6 — Tactical Pattern Detection (Weeks 11–12)
**Goal:** Level 2 — "how did it happen?" This is where the passing-network work
your teammate already built lives and grows.

- Extend the passing network script: full matches (not just one half), across multiple
  matches, using `networkx` (degree/betweenness centrality, density) + `mplsoccer` for viz
- Formation detection from average player positions
- Pressing intensity / defensive-line shape (stretch goal within this phase)

**Deliverable:** Tactical module that produces a passing network + key-passer/centrality
report for any match in our dataset, not just the one example.

---

### Phase 7 — Prediction Refinement, Context & Opponent Analysis (Weeks 13–14)
**Goal:** Level 3–4 — "why did it happen?" and "what might happen next?"

- Add context features: venue, schedule congestion, opponent style clustering
- Improve the baseline predictor with tactical + context features
- Opponent modelling: cluster teams by playing style using tactical features from Phase 6

**Deliverable:** An improved prediction model with a measurable accuracy gain over the
Phase 5 baseline, plus an opponent-style profile report.

---

### Phase 8 — Decision Support Layer (Weeks 15–16)
**Goal:** Level 5 — "what should we do?"

- Translate model outputs into actionable suggestions (formation, pressing trigger,
  matchup exploitation) with the `{Action, Evidence, Confidence, Conditions, Alternative}`
  structure from the synopsis — never an absolute claim
- Fan Mode vs Team Mode output framing (educational explanation vs. decision-support)

**Deliverable:** A decision-support report generator for a given match/opponent.

---

### Phase 9 — Assistant Integration (Weeks 17–18)
**Goal:** Connect the now-mature Assistant shell (started Phase 5) to every module built
so far.

- Assistant routes natural-language queries to: stats DB, tactical engine, prediction
  models, or decision layer
- Guardrails: assistant explains *why* it's giving an answer (evidence bundle), never
  invents stats
- End-to-end demo workflow: "Analyse our next opponent and summarise their tactical
  tendencies" → real output pulling from multiple modules

**Deliverable:** Working end-to-end Assistant demo, not a from-scratch build (because
Phase 5 already gave it a skeleton to grow from).

---

### Phase 10 — Evaluation, Refinement & Documentation (Weeks 19–20)
**Goal:** Prove it works, not just demo it once.

- Run the full evaluation framework (prediction accuracy/F1, tactical classification
  quality, assistant groundedness + tool-selection accuracy, unsupported-claim rate)
- Final documentation, architecture diagrams, final report
- Buffer time for whatever slipped — budget this honestly, don't assume zero slippage

**Deliverable:** Final report + working demo + evaluation results.

---

## 2. Repository Structure

```
squadsync/
├── README.md                  # Project overview, setup instructions
├── PROJECT_PLAN.md             # This file
├── requirements.txt            # Python dependencies
├── .gitignore                  # Excludes data/raw, .env, __pycache__, etc.
│
├── data/
│   ├── raw/                    # Untouched pulls from StatsBomb/APIs — gitignored
│   ├── interim/                # Partially cleaned data — gitignored
│   ├── processed/              # Canonical schema outputs (Parquet/SQLite) — gitignored
│   └── external/               # Small reference files that ARE committed (e.g. team-name mappings)
│
├── notebooks/                  # EDA and exploration — one prefix per person/topic
│   ├── 01_data_exploration.ipynb
│   ├── 02_passing_network_prototype.ipynb
│   └── ...
│
├── src/
│   └── squadsync/
│       ├── __init__.py
│       ├── config.py            # Paths, constants, competition/season IDs
│       ├── data/                 # Phase 2 — ingestion, canonical schema builder, sync job
│       │   ├── statsbomb_loader.py
│       │   ├── sync_job.py
│       │   └── canonical_schema.py
│       ├── features/             # Phase 4 — feature engineering
│       │   └── build_features.py
│       ├── models/                # Phase 5, 7 — prediction models
│       │   ├── baseline_predictor.py
│       │   └── opponent_clustering.py
│       ├── tactical/              # Phase 6 — passing networks, formations
│       │   ├── passing_network.py
│       │   └── formation_detection.py
│       ├── decision/              # Phase 8 — decision support layer
│       │   └── recommendation_engine.py
│       ├── assistant/             # Phase 5 (scaffold) → Phase 9 (full) — orchestration/LLM
│       │   ├── tools.py
│       │   ├── orchestrator.py
│       │   └── prompts.py
│       └── viz/                   # Shared plotting helpers (mplsoccer wrappers)
│           └── pitch_plots.py
│
├── tests/                      # Unit tests, mirroring src/squadsync/ structure
│
├── docs/
│   ├── architecture.md          # Canonical schema definition + system architecture
│   ├── dataset_reference.md     # The dataset doc we already shared with mentor
│   └── evaluation.md            # Evaluation framework & results log
│
├── outputs/
│   ├── figures/                 # Generated charts (gitignored or LFS if large)
│   └── reports/                 # Generated decision-support / briefing reports
│
└── scripts/                     # Small standalone run scripts (e.g. run_sync.py)
```

**Why this shape:** `src/squadsync/` mirrors the phases exactly, so whoever's working on
Phase 6 (tactical) only ever touches `tactical/`, and the Assistant (Phase 5 scaffold →
Phase 9 full build) has its own folder from day one instead of being bolted on later.

---

## 3. Git Workflow

- `main` — always working, always demoable. Never commit broken code directly to `main`.
- One branch per phase/module: `feature/passing-network`, `feature/canonical-schema`,
  `feature/baseline-predictor`, etc.
- Every merge to `main` goes through a Pull Request, reviewed by at least one other
  teammate — even a 2-minute glance catches schema mismatches early.
- Commit messages: `[phase-tag] short description` e.g. `[tactical] add formation detection from average positions`
- `data/raw/` and `data/processed/` stay out of git entirely (`.gitignore`) — datasets are
  pulled fresh by each teammate via the scripts in `src/squadsync/data/`, not committed as
  files. Only tiny reference files go in `data/external/`.

---

## 4. Immediate Next Steps (This Week)

1. Create the GitHub repo, add this file + the folder skeleton (empty `.gitkeep` files
   are fine for now)
2. Everyone installs: `statsbombpy`, `mplsoccer`, `pandas`, `networkx`, and confirms they
   can pull the Leverkusen dataset locally
3. Move your teammate's existing passing-network script into
   `notebooks/02_passing_network_prototype.ipynb` as a starting reference — don't rewrite
   it yet, just get it into the repo
4. Agree on the canonical schema fields together (30-minute call) before anyone writes
   the Phase 2 ingestion code
5. Assign Phase 1–2 ownership: someone owns the StatsBomb ingestion script, someone owns
   the sync job, someone starts exploring the existing passing-network code for what to
   extend in Phase 6

---

*Last updated: initial version. Revise this file whenever scope changes — treat it as
living documentation, not a one-time plan.*
