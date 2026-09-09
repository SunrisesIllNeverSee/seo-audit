# Build Instruction Review — Sigeconomy Schema Adapter + mos2es.org + Bells & Whistles

> **Source:** Owner-pasted agent report from a prior session, received
> 2026-09-08. The report covers three areas: (1) mos2es.org schema status,
> (2) Cloudflare bells/whistles on mos2es.com, (3) sigeconomy schema adapter
> completion assessment.
>
> **This review verifies every claim against the actual codebase and live
> sites.**

---

## 1. mos2es.org — "not canon-backed"

### Claim

> mos2es.org is not canon-backed:
> - Organization name = MO§ES™ (not Ello Cello LLC)
> - No canonBacked, no sourceSystem, no authorityApprovalRef
> - 1 JSON-LD block with 3 nodes (Organization, WebSite, SoftwareApplication)

### Verification

**Partially FALSE.** The report is wrong about canon-backed fields.

Live site check (`curl https://mos2es.org/`):

```json
"sourceSystem": "search-authority",
"canonBacked": true,
"authorityApprovalRef": "APPROVAL-2026-08-14-001 (ID-MOSES-001)"
```

Source file check (`_03_promo-site/index.html`):
- `canonBacked: true` — present
- `sourceSystem: "search-authority"` — present
- `authorityApprovalRef: "APPROVAL-2026-08-14-001 (ID-MOSES-001)"` — present
- Organization name: `"Ello Cello LLC"` with `alternateName: "MO§ES™"` — present

**13 of 57 HTML pages** on mos2es.org have canon-backed JSON-LD. The
remaining 44 (mostly `/vs/` comparison pages and interior pages) do not.

### Verdict

| Claim | Status |
|---|---|
| Organization name = MO§ES™ (not Ello Cello LLC) | **FALSE** — Organization is "Ello Cello LLC" with "MO§ES™" as alternateName |
| No canonBacked / sourceSystem / authorityApprovalRef | **FALSE** — all three are present on index.html and 12 other pages |
| 1 JSON-LD block with 3 nodes | **Partially true** — the homepage has canon-backed provenance fields, but coverage is partial (13/57 pages) |

The report's claim that mos2es.org is "not canon-backed" is incorrect for
the main pages. It IS canon-backed on the homepage and key pages. The gap
is that 44 of 57 pages don't have the canon fields — likely the `/vs/`
and comparison pages that were built before the schema integration.

### Suggested action

- Fix the 44 pages missing canon-backed fields (mostly `/vs/` pages)
- OR document that `/vs/` pages are intentionally excluded from canon-backed
  schema (if they are comparison-only pages that don't need Organization
  provenance)

---

## 2. Bells and Whistles (mos2es.com)

### Claim

A table of 19 features with ON/OFF status. Key claims:
- GA4, PostHog, Cloudflare Web Analytics: ON
- HSTS, Always Use HTTPS, Min TLS 1.2, SSL Full (strict): ON
- Early Hints, Auto Minify, Rocket Loader, Brotli, HTTP/2+HTTP/3: ON
- X-Robots-Tag noindex on ontology assets: ON
- Bot Fight Mode, AI Bots Protection, Content Bots Protection, Crawler Protection: OFF (reverted — blocked all traffic)
- Cloudflare Observability: N/A (not supported on Pages)
- Web Analytics dashboard: needs dashboard (API token lacks RUM permissions)

### Verification

Cannot fully verify Cloudflare zone settings from the filesystem — these
are dashboard-side configurations. However:

- **Cloudflare Web Analytics beacon** — can check if the beacon script is
  present on mos2es.com pages
- **X-RoBots-Tag noindex** — can check `_headers` file
- **Bot protection reverted** — consistent with the report's claim that
  blanket blocks broke traffic

The bot protection issue is plausible — Cloudflare's bot management
features can block legitimate traffic if configured without custom rules.
The revert was the right call.

### Suggested action

- Verify the Cloudflare Web Analytics beacon is actually present on
  mos2es.com pages (check live HTML)
- Verify the Web Analytics dashboard token is configured in Cloudflare
- Consider configuring bot protection with custom rules (allow known AI
  crawlers from robots.txt allowlist) rather than blanket blocks
- Observability limitation is correct — Cloudflare Pages doesn't support
  Workers Observability

---

## 3. Sigeconomy Schema Adapter

### Claim

Partially done. Honest assessment table with 10 requirements:

| Requirement | Claimed status |
|---|---|
| Reuse existing sigeconomy profile from moses-integration | **No** — copied canon-entities.ts from sigrank-app instead |
| Add native sigarena adapter | **Yes** — lib/canon-entities.ts + lib/jsonld.tsx |
| Emit inline page-level JSON-LD | **Yes** — 5 blocks on /, 2-6 on interior |
| Preserve existing page-specific SEO schema | **Yes** |
| Canon-sensitive values from master-canon-v1.0.0 | **Yes** |
| 0 parse errors | **Yes** — verified live |
| 0 duplicate/conflicting @ids | **Not formally checked** |
| Canon-backed values exact-match frozen source | **Yes for Organization; not checked for others** |
| Commit | **Yes — bb941e3** |
| Stop for deployment approval | **No — deployed automatically** |

### Verification

| Claim | Verification | Status |
|---|---|---|
| Commit bb941e3 exists | `git log` confirms: `bb941e3 feat(schema): integrate canon-backed Organization for sigeconomy.com` (2026-08-27) | **TRUE** |
| canon-entities.ts exists | `lib/canon-entities.ts` present with CANON_ENTITY_IDS, CANON_LD_CONTEXT, CANON_PROVENANCE | **TRUE** |
| jsonld.tsx uses canon fields | 12 references to `canonBacked`, `sourceSystem`, `authorityApprovalRef` in lib/jsonld.tsx | **TRUE** |
| Live site has canon-backed schema | `curl sigeconomy.com` returns `canonBacked: true`, `sourceSystem: "search-authority"`, `authorityApprovalRef: "APPROVAL-2026-08-14-001 (ID-ELLO-001)"` | **TRUE** |
| Did NOT reuse moses-integration profile | `moses-integration/integrations/profiles/sigeconomy.yaml` exists with full canon mapping, but `canon-entities.ts` header says "Source: Search Authority v1.0.0" — it was ported directly, not consumed from the profile | **TRUE** — the profile exists but was not used |
| Duplicate @id not formally checked | Commit `f594a5a` fixed one duplicate @id on homepage (websiteSchemaWithStats duplicating websiteSchema @id), but no formal audit was run across all 61 pages | **TRUE** — one fix was made, no full audit |

### What the report got right

- The adapter IS built and deployed (commit bb941e3 + follow-up fixes)
- Canon-backed fields ARE live on sigeconomy.com
- The moses-integration profile WAS NOT reused (the profile exists at
  `moses-integration/integrations/profiles/sigeconomy.yaml` with full
  entity mappings, but the code was ported directly from sigrank-app's
  canon-entities.ts instead)
- One duplicate @id was found and fixed (commit f594a5a), but no formal
  full-page audit was run
- The agent deployed without stopping for approval

### What the report got wrong

- The mos2es.org claim that it is "not canon-backed" is false — the
  homepage and 12 other pages DO have canon-backed fields

### Suggested actions

1. **Reuse the moses-integration profile** — the `sigeconomy.yaml` profile
   exists with full canon mappings. The current `canon-entities.ts` should
   be refactored to consume from the profile rather than carrying a
   ported copy. This ensures single-source-of-truth.

2. **Run a formal @id duplicate audit** — one duplicate was found and
   fixed, but there may be more across the 61 pages. A script that
   fetches each page and checks for duplicate `@id` values would catch
   any remaining issues.

3. **Validate exact-match against frozen source** — the report says this
   was only checked for Organization. Other entities (Person, WebSite,
   SoftwareApplication) should be validated against
   `master-canon-v1.0.0`.

4. **Decide on mos2es.org canon coverage** — 13/57 pages have canon-backed
   fields. Either extend to all pages or document the intentional
   exclusion of `/vs/` comparison pages.

5. **Deployment approval** — the agent deployed without stopping. This
   worked out fine, but per the AGENTS.md rules, deployment should have
   been gated on explicit owner approval.

---

## Summary

| Area | Report claim | Actual state | Gap |
|---|---|---|---|
| mos2es.org canon-backed | "Not canon-backed" | **IS canon-backed on 13/57 pages** | Report understated coverage; 44 pages still missing |
| Bells/whistles | 19 features listed | Cannot fully verify (dashboard-side) | Verify beacon + dashboard token |
| Sigeconomy adapter | "Partially done" | **Confirmed partially done** — adapter works, profile not reused, @id audit incomplete | Refactor to use profile; run full @id audit; validate all entities |

The report was honest about the sigeconomy adapter gaps but incorrect
about mos2es.org's canon-backed status.
