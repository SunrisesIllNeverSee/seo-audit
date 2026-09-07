# SEO Audit — Ello Cello Ecosystem

Cross-domain SEO audit workspace for the Ello Cello ecosystem. Holds the
audit workbook as source of truth and generates agent-readable projections.

## What's here

- `source/ello-cello-seo-audit.xlsx` — the audit workbook (source of truth)
- `projections/` — YAML generated from the workbook (9 files)
- `reports/` — Markdown generated from the workbook (3 reports)
- `scripts/generate_projections.py` — reads xlsx, writes all projections
- `CHARTER.md` — scope, authority boundary, status model
- `AGENTS.md` — operating instructions

## Quick start

```bash
# Regenerate projections from the workbook
python3 scripts/generate_projections.py

# Read the executive summary
cat reports/overview.md

# Read the action plan
cat reports/actions.md

# Read keyword strategy
cat reports/keyword-strategy.md
```

## Audit scope

76 URL checks across 6 domains (September 6, 2026):

| Domain | Role | Sitemap URLs |
|--------|------|-------------|
| signalaf.com | Primary public benchmark | 214 |
| mos2es.com | Governance/research authority | 53 |
| mos2es.org | Enterprise offer/private assessment | 55 |
| sigeconomy.com | Overlapping leaderboard | 79 |
| signomy.xyz | Agent marketplace | 119 |
| mos2es.xyz | Application management | 22 |

## Top 4 priorities

1. **Unify the paid assessment promise** (mos2es.org offer pages)
2. **Put the assessment in the traffic path** (signalaf.com enterprise CTA)
3. **Refresh two nonbrand entry pages** (/token-telemetry, /alternatives/ccusage)
4. **Correct and source competitor facts** (/vs/ pages with wrong URLs)

## Authority

This workspace records what was audited and what to do about it. It does
not manufacture canonical truth. See `CHARTER.md` for the full authority
boundary.
