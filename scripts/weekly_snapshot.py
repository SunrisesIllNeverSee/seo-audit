#!/usr/bin/env python3
"""Weekly SEO snapshot capture for the Ello Cello ecosystem.

Runs the automated parts of the search-to-inquiry baseline capture
every Monday and commits the result. GSC data must be added manually.

Usage:
    python3 scripts/weekly_snapshot.py
"""
from __future__ import annotations

import datetime
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CAPTURE_SCRIPT = REPO_ROOT / "scripts" / "capture_snapshot.py"


def main() -> int:
    date = datetime.date.today().isoformat()
    print(f"Weekly SEO snapshot capture: {date}")

    # Run the capture script
    result = subprocess.run(
        [sys.executable, str(CAPTURE_SCRIPT), "--date", date],
        capture_output=True, text=True, timeout=120,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: capture failed: {result.stderr}", file=sys.stderr)
        return 1

    # Commit the snapshot
    snapshot_path = REPO_ROOT / "tracking" / "snapshots" / f"{date}.yaml"
    if not snapshot_path.exists():
        print(f"ERROR: snapshot file not found at {snapshot_path}", file=sys.stderr)
        return 1

    try:
        subprocess.run(["git", "add", str(snapshot_path)], cwd=str(REPO_ROOT), check=True)
        subprocess.run(
            ["git", "commit", "-m", f"chore(seo): weekly snapshot {date}"],
            cwd=str(REPO_ROOT), check=True,
        )
        subprocess.run(["git", "push"], cwd=str(REPO_ROOT), check=True, timeout=30)
        print(f"Committed and pushed snapshot for {date}")
    except subprocess.CalledProcessError as e:
        print(f"WARNING: git operation failed: {e}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("WARNING: git push timed out", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
