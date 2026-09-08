#!/usr/bin/env python3
"""Capture a dated search-to-inquiry baseline snapshot.

Captures what we can measure automatically:
- Live HTTP status for all domains
- Sitemap URL counts
- Page-level title/H1 extraction for key pages
- llms.txt presence
- robots.txt status

What requires manual input (prompted at the end):
- Google Search Console: impressions, clicks, CTR, position
- AI Overview presence for target queries
- Bing indexing status

The snapshot is saved to tracking/snapshots/YYYY-MM-DD.yaml.
A comparison script can diff two snapshots to show movement.

Usage:
    python3 scripts/capture_snapshot.py
    python3 scripts/capture_snapshot.py --date 2026-09-08
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

TRACKING_DIR = Path(__file__).resolve().parent.parent / "tracking"
SNAPSHOTS_DIR = TRACKING_DIR / "snapshots"

DOMAINS = [
    "https://signalaf.com",
    "https://mos2es.com",
    "https://mos2es.org",
    "https://sigeconomy.com",
    "https://signomy.xyz",
    "https://mos2es.xyz",
]

KEY_PAGES = {
    "signalaf.com": [
        "/",
        "/token-telemetry",
        "/alternatives/ccusage-alternatives",
        "/ai-operator-scoring",
        "/operator-performance",
        "/hall",
        "/metrics/cache-hit-rate",
        "/tools/operator-class-checker",
    ],
    "mos2es.org": [
        "/",
        "/baseline-assessment",
        "/pilot",
        "/pilot-readout",
    ],
    "sigeconomy.com": [
        "/",
        "/vs/ccusage",
        "/vs/tokscale",
    ],
}

TARGET_QUERIES = [
    # ── Category / discovery (unbranded — hardest to rank for) ──
    "ai operator",
    "ai operator scoring",
    "ai operator leaderboard",
    "ai user leaderboard",
    "ai operator performance",
    "ai operator evaluation",
    "ai power user",
    "best ai user",
    "best ai coder",
    "how do i check my ai coding efficiency",
    "ai coding metrics tools",
    "ai benchmarking tools for operators",
    "model evals vs operator evals",
    "public llm operator evals",
    "performative evals for ai users",
    "enterprise ai baseline assessment",
    # ── Branded ──
    "sigrank",
    "signalaf",
    "signalaf.com",
    "what is sigrank",
    "what is signalaf",
    "npx sigrank",
    "sigrank mcp server",
    "how do i install sigrank",
    "sigeconomy.com",
    "moses governance",
    "mo§es",
    # ── Metrics ──
    "token telemetry",
    "yield in ai usage",
    "yield formula for ai coding",
    "leverage in ai token usage",
    "velocity in ai token usage",
    "snr in ai coding",
    "10xdev",
    "cache hit rate",
    "token cascade efficiency",
    "signal vs noise ai",
    # ── Tools / alternatives ──
    "ccusage alternative",
    "cc usage alternative",
    "ccusage alternatives",
    "alternatives to ccusage",
    "what is ccusage",
    "tokscale",
    # ── Comparisons ──
    "sigrank vs ccusage",
    "sigrank vs lmsys arena",
    "sigrank vs cursor",
    "sigrank vs langfuse",
    # ── Concepts / governance ──
    "commitment conservation law",
    "what is token cascade",
    "telescoping identity token cascade",
]


def fetch_url(url: str, timeout: int = 10) -> tuple[int, str]:
    """Fetch a URL and return (status_code, body_text)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; ElloAudit/1.0)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, str(e)


def extract_title_h1(html: str) -> tuple[str, str]:
    """Extract <title> and first <h1> from HTML."""
    import re
    title = ""
    h1 = ""
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    if h1_match:
        h1 = re.sub(r"<[^>]+>", "", h1_match.group(1)).strip()
    return title, h1


def count_sitemap_urls(sitemap_url: str) -> int:
    """Count URLs in a sitemap.xml."""
    status, body = fetch_url(sitemap_url, timeout=15)
    if status != 200 or not body:
        return 0
    import re
    urls = re.findall(r"<loc>(.*?)</loc>", body)
    return len(urls)


def capture_snapshot(date: str) -> dict:
    """Capture a complete snapshot for the given date."""
    snapshot = {
        "date": date,
        "captured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "domains": {},
        "key_pages": {},
        "target_queries": {q: {"gsc_impressions": None, "gsc_clicks": None, "gsc_position": None, "gsc_ctr": None, "ai_overview_present": None} for q in TARGET_QUERIES},
        "manual_data_needed": True,
        "notes": "",
    }

    for domain_url in DOMAINS:
        domain = domain_url.replace("https://", "")
        status, body = fetch_url(domain_url)
        title, h1 = extract_title_h1(body) if body else ("", "")

        sitemap_status, _ = fetch_url(f"{domain_url}/sitemap.xml")
        sitemap_count = count_sitemap_urls(f"{domain_url}/sitemap.xml") if sitemap_status == 200 else 0

        robots_status, _ = fetch_url(f"{domain_url}/robots.txt")
        llms_status, _ = fetch_url(f"{domain_url}/llms.txt")

        snapshot["domains"][domain] = {
            "homepage_status": status,
            "sitemap_status": sitemap_status,
            "sitemap_urls": sitemap_count,
            "robots_status": robots_status,
            "llms_txt_status": llms_status,
            "homepage_title": title,
            "homepage_h1": h1,
        }

    for domain, pages in KEY_PAGES.items():
        base = f"https://{domain}"
        snapshot["key_pages"][domain] = {}
        for path in pages:
            url = base + path
            status, body = fetch_url(url)
            title, h1 = extract_title_h1(body) if body else ("", "")
            snapshot["key_pages"][domain][path] = {
                "status": status,
                "title": title,
                "h1": h1,
            }

    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a dated search-to-inquiry baseline snapshot")
    parser.add_argument("--date", type=str, default=None, help="Date in YYYY-MM-DD format (defaults to today)")
    args = parser.parse_args()

    date = args.date or datetime.date.today().isoformat()
    print(f"Capturing snapshot for {date}...")

    snapshot = capture_snapshot(date)

    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = SNAPSHOTS_DIR / f"{date}.yaml"

    # Write as YAML
    import yaml
    with open(output_path, "w") as f:
        yaml.dump(snapshot, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\nSnapshot saved to: {output_path}")
    print(f"\nDomains captured: {len(snapshot['domains'])}")
    print(f"Key pages captured: {sum(len(v) for v in snapshot['key_pages'].values())}")
    print(f"Target queries tracked: {len(snapshot['target_queries'])}")

    print("\n" + "=" * 60)
    print("MANUAL DATA NEEDED (Google Search Console)")
    print("=" * 60)
    print("The following data cannot be captured automatically.")
    print("Export from Google Search Console and append to the snapshot:")
    print()
    print("For each target query, record:")
    print("  - gsc_impressions: total impressions (last 28 days)")
    print("  - gsc_clicks: total clicks (last 28 days)")
    print("  - gsc_position: average position")
    print("  - gsc_ctr: click-through rate")
    print("  - ai_overview_present: does signalaf.com appear in AI Overview? (true/false)")
    print()
    print("Target queries to check:")
    for q in TARGET_QUERIES:
        print(f"  - {q}")
    print()
    print(f"Edit: {output_path}")
    print("Add the GSC data under target_queries > {query} > gsc_*")

    return 0


if __name__ == "__main__":
    sys.exit(main())
