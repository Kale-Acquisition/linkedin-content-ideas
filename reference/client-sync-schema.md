# Client Sync Schema

> Authoritative schema for all client knowledge landing spots.
> Read by: auto-sync trigger (to know what to write), `apply-client-sync.py` (to validate and route), the `/create-client` and Notion Client Hub population workflows.
> Updated when: a new landing spot is added, a section is added/removed, or the Notion Client Hub structure changes.

---

## Overview

Client knowledge lives in five landing spots arranged in a one-way flow:

```
Notion Client Hub  ─┐
                    ├─►  .sync/clients/{slug}.md  ─►  client repo context/*.md (mirror files)
Supabase (deferred) ┘                              │
                                                   └─►  context/current-state.md (synthesized)

kale-workspace context/  ─►  client repo context/workspace/*.md (synced shared files)
```

Client repo `context/` mirrors the Notion Client Hub one-to-one — six client-specific mirror files plus a derived synthesis page. Shared Kale context is namespaced under `context/workspace/` to keep it cleanly separated from client-specific content.

---

## Landing Spot 1: `.sync/clients/{slug}.md` (kale-workspace)

**Role:** Intermediary. Written by the auto-sync trigger; read by GitHub Actions → `apply-client-sync.py` → client repos.

**File naming:** `{slug}.md` where slug matches the full client repo name (e.g., `kale-n2.md` for the `kale-n2` repo).

### Supported TARGETs

A sync file MAY contain any subset of the following `<!-- TARGET: path -->` markers. Each marker introduces a block of content destined for the listed path in the client repo. `apply-client-sync.py` writes the block to that path.

| TARGET path | Source | Required Section Headings |
|---|---|---|
| `context/overview.md` | Notion Internal Hub page + Clients DB row + roster | Profile, Health, Active Services, Key Contacts, Geo |
| `context/strategy.md` | Notion Strategy DB rows (Client Approved=true), grouped by `Category` | ICP, Messaging, Campaign, Playbook, Analysis |
| `context/customer-success.md` | Notion CS / Success DB rows, grouped by `Type` | Check-ins, Updates, Issues, Wins, Renewals |
| `context/data.md` | Notion Data DB rows, grouped by `Type` | Lead Lists, Domain Lists, Enrichments, Analyses, Other |
| `context/reporting.md` | Notion Reporting DB rows, grouped by `Type` (Supabase metrics layered on later) | Milestones, Weekly Reviews, Progress Meetings, QBRs, Client-Specific |
| `context/infra.md` | Supabase `kale-analytics` (deferred) | Persona Layout, Domain Inventory, Sending Capacity, Monthly Cost |

**Section names mirror Arra's existing DB property values.** Each row's `Category` (Strategy) or `Type` (CS, Data, Reporting) determines which section it lands in. No new Notion properties required — the sync respects what's already there.

If a sync file contains no TARGETs, `apply-client-sync.py` emits a WARNING and skips it.

### Deprecated TARGETs

The following TARGETs are no longer supported. `apply-client-sync.py` will emit a WARNING when it encounters them and will not write to the path.

| Deprecated TARGET | Reason | Replacement |
|---|---|---|
| `context/current-state.md` | Now derived, not directly synced | Synthesized from the 6 mirror files by the synthesis job |
| `context/project-info.md` | Folded into `overview.md` | `context/overview.md` |
| `context/project-goals.md` | Folded into `overview.md` (Success Criteria) and `strategy.md` (Active Commitments) | `context/overview.md` + `context/strategy.md` |
| `knowledge/meetings/YYYY-MM-DD-*.md` | Raw meetings live in Supabase + Notion; decisions distill into the relevant mirror | Distill into `strategy.md`, `customer-success.md`, or `data.md` |

### Header format per mirror file

```markdown
# {Mirror Title} — {Client Display Name}

_Last synced: YYYY-MM-DD. Source: {source}_

## {Required Section 1}

...
```

The `_Last synced:` line is injected by `apply-client-sync.py` at write time with the current UTC date.

### Section formats

Use bullet lists, not tables, for client details. Client realities are heterogeneous — not every field applies to every client.

Example (`overview.md`):
```markdown
## Profile

- Vertical: {industry}
- Status: {Active|Paused|Onboarding|Churned}
- Start date: {YYYY-MM}
- Repo: Kale-Acquisition/kale-{slug}

## Health

{Green|Yellow|Red} — {one-sentence current situation}

## Active Services

- Infrastructure
- Campaigns
- Lead Sourcing
- Inbox Management
- Reporting

## Key Contacts

- {Name, Title} — {role on the engagement}

## Geo

{Geographic focus}
```

Example (`customer-success.md` — grouped by CS.Type):
```markdown
## Check-ins

- 2026-05-15 — Bison migration concern raised by Chris Risch (Mike) [In progress]
- 2026-05-08 — Neighborhood list expansion approved (Mike) [Done]

## Updates

- 2026-05-15 — Dashboard expansion in progress (Roshan) [In progress]

## Issues

- 2026-05-15 — Bison performance regression, 3–4x decline (Roshan) [In progress]

## Wins

- 2026-05-12 — 31 deals closed by mid-May (Mike) [Done]

## Renewals

_None yet._
```

Rows route to sections via the `Type` (or `Category` for Strategy) property value on each Notion row. Each bullet shows date — title (owner) [status]. Empty sections render as `_None yet._`.

---

## Landing Spot 2: `context/{mirror}.md` (client repos — 6 files)

**Role:** Operational source of truth for each client, one file per Notion Client Hub component. Written by `apply-client-sync.py` from the sync file's TARGET blocks. Read by Claude Code sessions in the client repo.

**Schema:** Per-file required section headings as listed in Landing Spot 1's TARGET table.

**Manual edits:** Allowed. Client repo team members may update these files between syncs. Changes will be overwritten on the next sync — flag important manual edits for incorporation into the Notion Client Hub before the next sync.

---

## Landing Spot 3: `context/current-state.md` (client repos — synthesized)

**Role:** One-page synthesis read first by Claude in a client repo session. Derived from the 6 mirror files — NOT directly written by sync.

**Writer:** The synthesis job (`scripts/synthesize-current-state.py`, called as the final step of `apply-client-sync.py` after mirror files are written).

**Synthesis rule:**

| Output section | Source | What gets plucked |
|---|---|---|
| `## Status` | `overview.md` `## Health` | First paragraph (Green/Yellow/Red + situation) |
| `## Infrastructure` | `infra.md` `## Persona Layout` + `## Sending Capacity` | Top bullets (Supabase-sourced when wired) |
| `## Campaigns` | `reporting.md` `## Weekly Reviews` + `## Milestones` | Most recent reports |
| `## What's Working` | `customer-success.md` `## Wins` | Top 3 bullets |
| `## In Progress` | `customer-success.md` `## Updates` + `data.md` `## Lead Lists` | Top 3 bullets across both |
| `## Blockers` | `customer-success.md` `## Issues` | Top 3 bullets |
| `## Next Steps` | `strategy.md` `## Campaign` + `## Messaging` | Top 3 active deliverables (Status != Done) |

If a mirror file is missing or empty, the corresponding synthesis section reads: `_No data yet — see [mirror file]._`

**Header format:**

```markdown
# Current State — {Client Display Name}

_Last synthesized: YYYY-MM-DD HH:MM UTC from 6 mirror files. Manual edits will be overwritten._
```

**Manual edits:** Discouraged. Edit the mirror files instead; resynthesize via `python scripts/synthesize-current-state.py {slug}`.

---

## Landing Spot 4: `context/workspace/*.md` (client repos and all tier-3 repos)

**Role:** Shared Kale context, synced from kale-workspace into every tier-3 repo. Namespaced under `workspace/` to keep client-specific content cleanly separated.

**Writer:** `sync-downstream.yml` GitHub Action runs `sync-to-template.py` on push to master.

**Files:**

| Path in client repo | Source in kale-workspace | Content |
|---|---|---|
| `context/workspace/team.md` | `context/team.md` | Team roster and roles |
| `context/workspace/business-info.md` | `context/business-info.md` | Kale company context |
| `context/workspace/clients.md` | `context/clients.md` | Full client roster (includes self for cross-reference) |
| `context/workspace/kale-strategy.md` | `context/strategy.md` | Kale-level strategy (renamed to avoid collision with client `strategy.md`) |

**No-longer-synced files** (removed by the structural migration):

- `context/arra.md`, `context/azhar.md`, `context/beverly.md`, `context/pandush.md`, `context/umer.md` — redundant with `team.md`
- `context/front_end_design_skill.md`, `context/kale_knowledge_resource_building_skill.md` — misfiled, belong in `.claude/skills/`

**Manual edits:** Disallowed. Edit the source file in kale-workspace; changes flow downstream automatically.

---

## Landing Spot 5: `context/clients-live.md` (kale-workspace only)

**Role:** Compact per-client snapshot for `/prime` to load. Written by the auto-sync trigger on each run. Workspace-only — does not sync to template or tier-3 repos.

**Format:** One `##` block per active client, 4–5 lines of content.

```markdown
# Clients — Live State

> Compact snapshot for /prime. Rewritten by auto-sync on each run.
> For full detail: `.sync/clients/{slug}.md` or client repo `context/current-state.md`.
> Last rewritten: YYYY-MM-DD HH:MM UTC

---

## {Client Display Name}
Status: {Active|Paused|At-Risk} · Health: {Green|Yellow|Red} · Repo: kale-{slug} · Last synced: YYYY-MM-DD
Focus: {one sentence — the main thing happening right now}
Blocker: {top blocker, owner in parens}
Urgent: {top action item, owner in parens}
```

**Required fields per block:** Status line, Focus, Blocker, Urgent. If no active blocker, write `Blocker: None`.

---

## Landing Spot 6: Notion Client Hub Pages

**Role:** Team's live operational view. Source of truth for `overview.md`, `strategy.md`, `customer-success.md`, `data.md`. Read by the auto-sync trigger (Notion → sync files).

### Page structure

Each client hub page contains six sub-sections matching the six mirror files. See the Notion Client Hub template for the property and database structure.

### Write direction

**Currently:** One-way (Notion → git). Humans edit in Notion; auto-sync writes mirror files in git.

**Future (Phase 3 of broader sync work, not in this plan):** Selective writeback for status/health from Supabase events. Manual page content is never overwritten.
