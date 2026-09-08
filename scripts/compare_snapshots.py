#!/usr/bin/env python3
"""Compare two search-to-inquiry snapshots to show movement over time.

Usage:
    python3 scripts/compare_snapshots.py --from 2026-09-07 --to 2026-09-14
    python3 scripts/compare_snapshots.py --latest  # compare last two snapshots
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

SNAPSHOTS_DIR = Path(__file__).resolve().parent.parent / "tracking" / "snapshots"


def load_snapshot(date: str) -> dict:
    path = SNAPSHOTS_DIR / f"{date}.yaml"
    if not path.exists():
        print(f"Error: snapshot {date} not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def compare_snapshots(old: dict, new: dict) -> str:
    lines = []
    lines.append(f"# Snapshot Comparison: {old['date']} → {new['date']}")
    lines.append("")

    # Domain changes
    lines.append("## Domain Status")
    lines.append("")
    lines.append("| Domain | Status (old→new) | Sitemap URLs (old→new) | Title changed |")
    lines.append("|--------|------------------|----------------------|---------------|")
    for domain in sorted(set(old.get("domains",{})) | set(new.get("domains",{}))):
        o = old.get("domains",{}).get(domain, {})
        n = new.get("domains",{}).get(domain, {})
        status = f"{o.get('homepage_status','?')}→{n.get('homepage_status','?')}"
        sitemap = f"{o.get('sitemap_urls','?')}→{n.get('sitemap_urls','?')}"
        title_changed = "YES" if o.get("homepage_title","") != n.get("homepage_title","") else ""
        lines.append(f"| {domain} | {status} | {sitemap} | {title_changed} |")

    # Key page changes
    lines.append("")
    lines.append("## Key Page Changes")
    lines.append("")
    for domain in sorted(set(old.get("key_pages",{})) | set(new.get("key_pages",{}))):
        old_pages = old.get("key_pages",{}).get(domain, {})
        new_pages = new.get("key_pages",{}).get(domain, {})
        changes = []
        for path in sorted(set(old_pages) | set(new_pages)):
            o = old_pages.get(path, {})
            n = new_pages.get(path, {})
            if o.get("title","") != n.get("title","") or o.get("status") != n.get("status"):
                changes.append(f"  - `{path}`: status {o.get('status','?')}→{n.get('status','?')}, title: \"{o.get('title','')}\" → \"{n.get('title','')}\"")
        if changes:
            lines.append(f"### {domain}")
            lines.extend(changes)
            lines.append("")

    # GSC query movement
    lines.append("## Search Console Query Movement")
    lines.append("")
    old_q = old.get("target_queries", {})
    new_q = new.get("target_queries", {})
    has_gsc = any(v.get("gsc_impressions") is not None for v in new_q.values())
    if has_gsc:
        lines.append("| Query | Impressions (old→new) | Clicks (old→new) | Position (old→new) | CTR (old→new) |")
        lines.append("|-------|----------------------|-------------------|-------------------|----------------|")
        for q in sorted(set(old_q) | set(new_q)):
            o = old_q.get(q, {})
            n = new_q.get(q, {})
            lines.append(f"| {q} | {o.get('gsc_impressions','—')}→{n.get('gsc_impressions','—')} | {o.get('gsc_clicks','—')}→{n.get('gsc_clicks','—')} | {o.get('gsc_position','—')}→{n.get('gsc_position','—')} | {o.get('gsc_ctr','—')}→{n.get('gsc_ctr','—')} |")
    else:
        lines.append("_No GSC data in snapshots. Run `capture_snapshot.py`, then manually add GSC data to the snapshot file._")

    # AI Overview
    lines.append("")
    lines.append("## AI Overview Presence")
    lines.append("")
    ai_data = any(v.get("ai_overview_present") is not None for v in new_q.values())
    if ai_data:
        for q in sorted(set(old_q) | set(new_q)):
            o = old_q.get(q, {}).get("ai_overview_present")
            n = new_q.get(q, {}).get("ai_overview_present")
            if o is not None or n is not None:
                lines.append(f"  - `{q}`: {o} → {n}")
    else:
        lines.append("_No AI Overview data in snapshots. Manually check and add to snapshot file._")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two search-to-inquiry snapshots")
    parser.add_argument("--from", dest="from_date", type=str, help="Old snapshot date")
    parser.add_argument("--to", dest="to_date", type=str, help="New snapshot date")
    parser.add_argument("--latest", action="store_true", help="Compare last two snapshots")
    args = parser.parse_args()

    if args.latest:
        snapshots = sorted(SNAPSHOTS_DIR.glob("*.yaml"))
        if len(snapshots) < 2:
            print("Need at least 2 snapshots to compare", file=sys.stderr)
            return 1
        old = load_snapshot(snapshots[-2].stem)
        new = load_snapshot(snapshots[-1].stem)
    elif args.from_date and args.to_date:
        old = load_snapshot(args.from_date)
        new = load_snapshot(args.to_date)
    else:
        parser.print_help()
        return 1

    print(compare_snapshots(old, new))
    return 0


if __name__ == "__main__":
    sys.exit(main())
