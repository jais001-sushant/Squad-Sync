# SquadSync — Dataset & Data Source Reference

Same content shared with our mentor (see the formatted PDF/DOCX version shared
separately) — kept here in markdown so it lives alongside the code and stays
easy to update.

## 1. Core Training Data

| Dataset | Purpose | Link | Access |
|---|---|---|---|
| StatsBomb Open Data | Core event data (passes, shots, pressures) with x,y coordinates. **Primary source — currently in use.** | https://github.com/statsbomb/open-data | Free registration at statsbomb.com/resource-centre. `pip install statsbombpy` |
| Wyscout Public Event Dataset (Pappalardo et al., 2019) | Larger event-data corpus, backup/supplement | https://figshare.com/collections/Soccer_match_event_dataset/4415000/2 | Free, no signup |
| Football-Data.co.uk | Match results, odds, baseline for prediction models | https://www.football-data.co.uk/data.php | Free CSV, no signup |

## 2. Sync / Current-Season Data

| Source | Purpose | Link | Free Tier |
|---|---|---|---|
| football-data.org | Scheduled sync of fixtures/results for live demo | https://www.football-data.org | 12 competitions, 10 req/min, free API key |
| API-Football | Broader league coverage, player-level stats | https://www.api-football.com | 100 req/day free (via RapidAPI) |

## 3. Supplementary (Scrape-Based — use cautiously)

| Source | Purpose | Link |
|---|---|---|
| FBref | Detailed xG, pressing, possession metrics | https://fbref.com |
| Understat | Additional xG/shot-quality data | https://understat.com |
| Transfermarkt | Player market values (only if recruitment module built) | https://www.transfermarkt.com |

## 4. Bonus Free Source

| Source | Purpose | Link |
|---|---|---|
| Openfootball / football.db | Public-domain results database | https://github.com/openfootball |

## 5. Video / Future-Scope (not built yet)

| Source | Purpose | Link |
|---|---|---|
| SoccerNet | Action-spotting video dataset | https://github.com/SoccerNet |
| Metrica Sports Sample Data | Small tracking-data sample | https://github.com/metrica-sports/sample-data |

## Current Working Dataset

**StatsBomb Open Data — Bayer Leverkusen 2023/24 unbeaten Bundesliga season**
- `competition_id = 9`, `season_id = 281`
- 34 matches, ~3,800-4,000 events each, 91 columns per event
- Verified reachable and complete — see `docs/architecture.md`

## Cost

All sources above are free at project scale. No paid datasets are in use.
Premium sources (Sportmonks, Wyscout API, SkillCorner tracking) remain a
future option if the project reaches a stage where sponsorship becomes
available — not needed for the current phases.
