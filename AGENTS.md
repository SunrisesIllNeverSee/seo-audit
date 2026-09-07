# seo-audit — Operating Instructions

## Startup order

1. Read `CHARTER.md` (governing rules).
2. Read this file.
3. Read `projections/actions.yaml` for current recommendations.
4. Read `reports/overview.md` for executive summary.

## Structure

```
source/          — the xlsx workbook (source of truth, do not edit by hand)
projections/     — YAML generated from the workbook (agent-readable)
reports/         — Markdown generated from the workbook (human-readable)
scripts/         — generator and utilities
tracking/        — implementation status (STATUS.yaml)
```

## Regenerating projections

After updating the workbook in `source/`:

```bash
python3 scripts/generate_projections.py
```

This reads the xlsx and writes all YAML + Markdown files. Do not edit
projections or reports by hand — they are generated.

## Tracking implementation

Implementation status lives in `tracking/STATUS.yaml` (not in stickypads).
Each action has a status: identified, in-progress, implemented, verified,
deferred, or superseded.

## Core rules

- The xlsx is the source of truth. Projections are generated.
- Do not edit projections/ or reports/ by hand.
- Do not create `_final`, `_new`, `_updated` versions of files.
- Do not deploy changes to product repos from here — implement there.
- Do not track work in stickypads — track it here.
