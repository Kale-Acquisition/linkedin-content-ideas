# Notion Sync

> Poll Notion client portal databases for every active client and write sync data to `.sync/clients/`. GitHub Actions then distributes to client repos automatically.

**Scope:** Notion only. Fireflies capture is a separate n8n webhook workflow. Slack capture is a separate n8n webhook workflow. Instantly and EmailBison are Phase 3.

## Overview

For each active client, this command produces a `.sync/clients/<slug>.md` file containing up to **four** `<!-- TARGET: path -->` blocks that mirror the Notion Client Hub:

| TARGET | Source | Section routing |
|---|---|---|
| `context/overview.md` | Notion Internal Hub page + Clients DB row + roster | Page properties → fixed sections |
| `context/strategy.md` | Notion Strategy DB (Client Approved=true) | `Category` (ICP / Messaging / Campaign / Playbook / Analysis) |
| `context/customer-success.md` | Notion CS / Success DB | `Type` (Check-in / Update / Issue / Win / Renewal) |
| `context/data.md` | Notion Data DB | `Type` (Lead List / Domain List / Enrichment / Analysis / Other) |
| `context/reporting.md` | Notion Reporting DB | `Type` (Milestone / Weekly Review / Progress Meeting / QBR / Client-Specific) |

`context/infra.md` is **not** written by this command — it's sourced from Supabase via a separate (deferred) sync. Empty data is fine: each mirror block is still written with required section headers; downstream `synthesize-current-state.py` renders `_No data yet_` placeholders per section.

**Section names mirror Arra's existing DB property values.** No new Notion properties are required — rows route to mirror sections via the `Category` (Strategy) or `Type` (CS, Data, Reporting) property already on each row.

After all clients are synced, the command also rewrites `context/clients-live.md` (workspace-only) and commits/pushes — GitHub Actions then runs `apply-client-sync.py` against the changed sync files, which writes the mirror files in each client repo and re-synthesizes `current-state.md`.

> Authoritative schema reference: `reference/client-sync-schema.md`.

## Arguments

- `--client [name]` — sync only one client (default: all active)
- `--dry-run` — show what would change without writing
- `--insights` — generate cross-client health summary after syncing

## Step 1: Load Client Roster

Read `context/clients.md`. For each client with status **Active** or **Onboarding**, extract:
- Client display name and repo slug
- `notion_db_ids` field — the database IDs for this client's Hub (front page, Strategy, CS, Data; Reporting and Infra are deferred but the IDs can be carried for future use)

If a client has no `notion_db_ids`, log a warning and skip them.

## Step 2: For Each Client, Query Notion

Use `mcp__claude_ai_Notion__notion-fetch` or `notion-query-data-source` against stable IDs. Never freeform-search — the data lives in the databases.

### Source A — Internal Hub page + Clients DB row → `context/overview.md`

Required sections: `## Profile`, `## Health`, `## Active Services`, `## Key Contacts`, `## Geo`.

The Internal Hub page (one per client, distinct from the client-facing `Client View` page) is the operator-only view. Until it exists, fall back to the Clients DB row (`collection://1a043dec-a6cb-4e8c-8b31-4e740f170f41`) and the roster in `context/clients.md`.

- `## Profile` — vertical, status, start date, repo slug. Pull from Internal Hub page properties; fall back to roster.
- `## Health` — Green/Yellow/Red + one sentence on the current situation. Pull from Internal Hub property; fall back to most recent CS DB `Check-in` row's title.
- `## Active Services` — bullet list (Infrastructure, Campaigns, Lead Sourcing, Inbox Management, Reporting, etc.). From Internal Hub property or roster.
- `## Key Contacts` — `{Name, Title} — {role on engagement}` bullets. From Internal Hub property; otherwise omit.
- `## Geo` — geographic focus. From Internal Hub property; fall back to roster.

### Source B — Strategy DB (Client Approved=true) → `context/strategy.md`

Query Strategy DB rows where `Client` relation = this client AND `Client Approved` = true. Group rows by `Category` property.

Required sections: `## ICP`, `## Messaging`, `## Campaign`, `## Playbook`, `## Analysis`.

Each section lists rows in that Category, sorted by `Due Date` ascending (no date → end):

```markdown
- {Due Date or "—"} — {Deliverable} ({Owner}) [{Status}]{newline}  {Notes (if present, indented)}
```

If a Category has no rows, render the section body as `_None yet._`.

### Source C — CS / Success DB → `context/customer-success.md`

Query CS DB rows where `Client` relation = this client. Group by `Type` property. Sort each group by `Date` descending (most recent first), cap at 10 per section.

Required sections: `## Check-ins`, `## Updates`, `## Issues`, `## Wins`, `## Renewals`.

Each bullet: `- {Date} — {Item} ({Owner}) [{Status}]` plus an indented `Notes` line if present. Empty sections render `_None yet._`.

### Source D — Data DB → `context/data.md`

Query Data DB rows where `Client` relation = this client. Group by `Type` property. Sort each group by `Run Date` descending, cap at 10 per section.

Required sections: `## Lead Lists`, `## Domain Lists`, `## Enrichments`, `## Analyses`, `## Other`.

Each bullet for a Lead List row:

```markdown
- {Run Date} — {Dataset} · {Record Count} records, {Validation Rate %}% valid · ICP: {ICP} · Geo: {Geo} · ${Run Cost} ({Status})
```

Trim fields that are empty. Other Types use a similar format, dropping list-specific fields.

### Source E — Reporting DB → `context/reporting.md`

Query Reporting DB rows where `Client` relation = this client. Group by `Type` property. Sort by `Date` descending, cap at 10 per section.

Required sections: `## Milestones`, `## Weekly Reviews`, `## Progress Meetings`, `## QBRs`, `## Client-Specific`.

Each bullet: `- {Date} — {Report} ({Owner}) — [link]({Link})`. Indent `Notes` on next line if present.

> **Note:** Reporting was previously marked "Supabase-deferred." Notion's Reporting DB tracks report **records** (when sent, by whom, link). Supabase will later layer **headline metrics** (open rates, reply rates, etc.) as additional sections — without conflicting with these row-based sections.

### Deprecated — do NOT write

These TARGETs are rejected by `apply-client-sync.py` and must not appear in sync files:
- `context/current-state.md` — now synthesized downstream from the 4 mirrors (+ reporting/infra shells).
- `context/project-info.md`, `context/project-goals.md` — folded into `overview.md` and `strategy.md`.
- `knowledge/meetings/YYYY-MM-DD-*.md` — raw meetings stay in Supabase + Notion. Distill key decisions into `strategy.md` (commitments), `customer-success.md` (blockers/next steps), or `data.md` (list specs) instead.

## Step 3: Write Sync Data Files

For each client, write `.sync/clients/<slug>.md` with the five TARGET blocks in this order: `overview.md`, `strategy.md`, `customer-success.md`, `data.md`, `reporting.md`.

Header format per TARGET block:

```markdown
<!-- TARGET: context/{mirror}.md -->
# {Mirror Title} — {Client Display Name}

_Last synced: YYYY-MM-DD. Source: Notion._

## {Required Section 1}

...
```

`apply-client-sync.py` validates required sections per TARGET against `SUPPORTED_TARGETS` and emits warnings for missing ones. Always include every required section header even when empty — write `_None yet._` as the body if there's no content.

## Step 4: Rewrite clients-live.md

After all clients are synced, rewrite `context/clients-live.md` from the fresh sync data. Pull from the per-mirror blocks:

- **Status** — from `overview.md` block: status + repo + last-synced date
- **Health** — from `overview.md` `## Health` line
- **Focus** — most recent `customer-success.md` `## Check-ins` bullet (date + title), or fall back to the top `strategy.md` `## Campaign` row
- **Blocker** — top item from `customer-success.md` `## Issues` (with owner in parens), or `None`
- **Urgent** — top open Strategy row across `## Campaign` and `## Messaging` (Status != Done), with due date

```markdown
# Clients — Live State

> Compact snapshot for /prime. Rewritten by auto-sync on each run.
> Last rewritten: YYYY-MM-DD HH:MM UTC

---

## {Client Display Name}
Status: {Active|Paused|At-Risk} · Health: {Green|Yellow|Red} · Repo: kale-{slug} · Last synced: YYYY-MM-DD
Focus: {one sentence}
Blocker: {top blocker (owner), or None}
Urgent: {top next step (owner)}
```

## Step 5: Commit and Push

```bash
git add .sync/clients/ context/clients-live.md
git diff --cached --quiet || git commit -m "chore: notion sync (YYYY-MM-DD)"
git push
```

The push triggers GitHub Actions (`sync-client-repos.yml`):
1. Detects changed `.sync/clients/*.md` files
2. Runs `apply-client-sync.py` per changed client — writes the 5 mirror files in the client repo
3. `apply-client-sync.py` calls `synthesize-current-state.py` as its final step — regenerates `context/current-state.md` from all 6 mirror files (the 5 Notion-sourced ones + the Supabase-deferred `infra.md` shell)

## Step 6: Generate Insights (if --insights or automated run)

After syncing, assess client health across all active clients:

| Client | Health | Last activity | Blockers >7 days | Attention needed |
|---|---|---|---|---|

Write to `outputs/client-insights/YYYY-MM-DD.md`.

## Notes

- **Empty Notion is fine.** Mirror blocks are still written with required headers and `_None yet._` bodies. Downstream synthesis falls back to `_No data yet — see {mirror}._` per section. The mechanism works the moment this command runs, regardless of how much data Arra has populated.
- **Idempotent** — running twice with the same Notion data produces no new commits.
- **Skip on missing IDs** — if a client's `notion_db_ids` is incomplete, log a warning and skip; don't fail the whole run.
- **Infra** — not written by this command. The `infra.md` mirror file exists as a shell in each client repo and stays until the Supabase → mirror sync ships. `reporting.md` is now Notion-sourced; Supabase metrics layer on later.
- **Sub-page expansion** — the Hub front page may contain linked sub-pages (campaign briefs, ICP docs). Pull primary properties only; deep-link bodies stay in Notion.
