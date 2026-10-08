"""
Phase 1 setup check — run this after `pip install -r requirements.txt` to
confirm your environment can actually pull StatsBomb data before writing
any analysis code.

Run from the project root:
    PYTHONPATH=src python scripts/test_environment.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main():
    print("=" * 60)
    print("SquadSync — Phase 1 Environment Check")
    print("=" * 60)

    # 1. Library imports
    try:
        import pandas  # noqa
        import networkx  # noqa
        import mplsoccer  # noqa
        from statsbombpy import sb  # noqa
        print("[OK] All required libraries import successfully")
    except ImportError as e:
        print(f"[FAIL] Missing library: {e}")
        print("       Run: pip install -r requirements.txt")
        sys.exit(1)

    # 2. StatsBomb data access
    try:
        from squadsync.data.statsbomb_loader import get_matches
        matches = get_matches()
        assert len(matches) == 34, f"Expected 34 matches, got {len(matches)}"
        print(f"[OK] StatsBomb data reachable — {len(matches)} matches found (Leverkusen 2023/24)")
    except Exception as e:
        print(f"[FAIL] Could not reach StatsBomb data: {e}")
        sys.exit(1)

    # 3. Required fields present
    try:
        from squadsync.data.statsbomb_loader import get_match_events
        from squadsync.config import REQUIRED_EVENT_FIELDS
        events = get_match_events(matches.iloc[0]["match_id"])
        missing = [f for f in REQUIRED_EVENT_FIELDS if f not in events.columns]
        if missing:
            print(f"[FAIL] Missing required fields: {missing}")
            sys.exit(1)
        print(f"[OK] All {len(REQUIRED_EVENT_FIELDS)} required fields present in event data")
    except Exception as e:
        print(f"[FAIL] Event field check failed: {e}")
        sys.exit(1)

    print("=" * 60)
    print("Environment ready. You can start on Phase 1/2 tasks.")
    print("=" * 60)


if __name__ == "__main__":
    main()
