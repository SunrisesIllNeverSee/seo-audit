# seo-audit — Charter

## Objective

Track, coordinate, and project the Ello Cello ecosystem SEO audit.
This workspace holds the audit workbook as the source of truth and
generates agent-readable projections (YAML + Markdown) from it.

## Authority boundary

This workspace records **what was audited** and **what to do about it**.
It does NOT manufacture canonical truth — that belongs to Search Authority.
Findings and recommendations are candidates that may drive changes in
product repos (signalaf-app, mos2es.org, sigeconomy.com).

## What this workspace does

- Stores the audit workbook (xlsx) as the source of truth
- Generates YAML projections for agent consumption
- Generates Markdown reports for human consumption
- Tracks implementation status of audit recommendations
- References original evidence — does not move or duplicate it

## What this workspace does NOT do

- Does not deploy changes to any product repo
- Does not modify canonical content
- Does not create redirects or merge pages
- Does not track work in stickypads (stickypads is the owner's inbox, not a project tracker)
- Does not replace repository-local coordination kits

## Source of truth

`source/ello-cello-seo-audit.xlsx` is the source of truth. All projections
are generated from it. When the workbook is updated, re-run the generator:

```bash
python3 scripts/generate_projections.py
```

## Status model

- **identified** — audit finding, no action taken
- **in-progress** — implementation started in a product repo
- **implemented** — change deployed and verified
- **verified** — acceptance check from the audit confirmed passing
- **deferred** — intentionally not acting on this finding
- **superseded** — replaced by a newer finding or audit

## Lifecycle

1. Audit workbook arrives in `source/`
2. Generator produces projections and reports
3. Recommendations are reviewed and prioritized
4. Implementation happens in the relevant product repos
5. Status is tracked back here in `tracking/STATUS.yaml`
6. When a new audit arrives, the old one is archived with provenance

## Domains in scope

- signalaf.com — primary public benchmark
- mos2es.com — governance/research authority
- mos2es.org — enterprise offer/private assessment
- sigeconomy.com — overlapping public leaderboard
- signomy.xyz — agent marketplace
- mos2es.xyz — application management product

## Cross-references

- AI Search Observatory: `/Users/dericmchenry/Developer/_8_dev-tools/1_custom/monitors/ai-search-observatory-benchmark`
- Search Authority: `/Users/dericmchenry/Developer/_control/search-authority`
- signalaf-app: `/Users/dericmchenry/Developer/active/SigRank-repos/_01_sigrank-app`
