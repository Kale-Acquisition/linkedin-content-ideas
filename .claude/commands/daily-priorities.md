# /daily-priorities

> Evening planning partner. Walks the roadmap tree (Initiatives → Workstreams → Milestones), surfaces what's converging this week, poses questions worth thinking through, and ends with a draft sequence you can adjust.

**Usage:** `/daily-priorities [flags]`

**Flags:**
- (no flag) — Full walkthrough + push to Sunsama, planning the next working day. Auto-detects: 5 PM–5 AM → tomorrow; otherwise today.
- `--today` / `--tomorrow` — Force the planning date
- `--focus [initiative-slug]` — Pin a specific initiative as the lead. Persisted to memory until changed.
- `--brief` — Skip the per-workstream question prompts; just the tree + draft sequence + Sunsama push
- `--no-sunsama-push` — Skip writing to Sunsama; render the plan as paste-text instead
- `--dry-run` — Render everything but make zero MCP writes (preview-only)

**Examples:**
- `/daily-priorities` — full walkthrough
- `/daily-priorities --focus service-delivery-3x` — set focus, then walk
- `/daily-priorities --brief` — fast version, no prompts

---

## Design principle

This is a **thinking partner**, not a task picker. Goal: give the user the data and the questions they'd ask themselves, then let them decide. The user owns the final call.

The roadmap tree is the spine: **Initiatives → Workstreams → Milestones**. Linear issues are supporting evidence, not the primary surface. Milestones are commitments; Linear `dueDate` fields are not.

Output is plain text. **No markdown links on task names** — keep references as plain text. The user reads roadmap docs in the wiki, not via inline links in this report.

The report ends with a *draft sequence* clearly framed as a starting point, not a prescription.

---

## Step 1: Parse `$ARGUMENTS`

| Flag | Effect |
|---|---|
| `--today` / `--tomorrow` | Override auto-detect for planning date |
| `--focus [slug]` | Set focus initiative; persist to memory |
| `--brief` | Drop per-workstream question prompts |
| `--no-sunsama-push` | Skip Step 8 MCP writes; render paste-text fallback instead |
| `--dry-run` | Render everything (including the would-be Sunsama tasks) but make zero MCP writes |

Resolve planning date: if local time is 5 PM–5 AM, default = tomorrow; else = today. Skip weekends to next Monday. Header: `# Evening planning — {today_short} → {planning_date_short}`.

If `--focus` provided, save to memory (`project_daily_focus.md`) before continuing.

---

## Step 2: Load context (best-effort)

Try to read; skip silently if missing:
1. `context/strategy.md`
2. `knowledge/operations/roadmap-boundary.md`
3. **`../kale-wiki/content/company/roadmap.data.json`** — the roadmap source of truth
4. The focus memory (`memory/project_daily_focus.md`)

If `roadmap.data.json` is missing, fall back to a degraded mode that walks Linear projects only — but warn the user explicitly that the report isn't grounded in the actual roadmap.

---

## Step 3: Build the planning window

Window: planning_date → planning_date + 7 days (configurable; default 7).

For each `workstream` in `roadmap.data.json`:
- Filter `milestones[]` where `targetDate` falls inside the window OR `status == "In Progress"` (in-progress milestones are always relevant regardless of date).
- Tag each milestone with: `daysUntilTarget`, `status`, `owner`, `criteriaSnippet` (first sentence of `title`).

For each `initiative` in `roadmap.data.json`:
- Find its workstreams via `initiativeSlug`.
- Sum the count of in-window milestones per workstream.
- Skip initiatives with zero in-window milestones across all workstreams.

Capture standalone workstreams (`initiativeSlug == null`) separately — they appear at the bottom under "Standalone".

---

## Step 4: Pull supporting Linear data

For each in-window milestone with `owner == "Roshan"` (or current active user), check whether there's a Linear issue tied to the same workstream that might be the underlying ticket:

`list_issues(assignee="me", project="{workstream Linear project name}", state in {started, unstarted}, limit=20)`

Use sparingly — supporting evidence only. Don't list every Linear issue. Surface only:
- Tickets explicitly named in milestone descriptions
- Blockers (status contains "Blocker", "Pending Client Approval")
- Items with `daysSinceUpdate > 14` if the milestone is stuck

Per-client tickets (Linear projects matching client roster like N2, Riipen, Terraboost-*) are pulled separately for the client section.

---

## Step 5: Render — walkthrough

```
# Evening planning — {Tue May 5, 2026} → {Wed May 6}

You've got **{N} active initiatives** with milestones moving in the next 7 days. Walk down the tree to figure out where {planning_day} should sit.

---

## {n}. {Initiative name} — target {date}{focus marker if matched}
*"{initiative.why one-liner, trimmed}"*

**{Workstream name}** *({priority} · {status} · target {workstream.targetDate})*{focus marker}
- {today_or_day_short} {date} — {milestone.title} *({status}{owner if not me})*
- ...

> *Worth thinking through:*
> - {question 1 — Claude composes based on milestone state}
> - {question 2}

**{Next workstream}** ...
```

**Focus marker:** If `--focus` matches the initiative slug, append `, your strategic top` to the heading. If it matches a workstream's parent, append `— your stated focus` to the workstream line.

**Day labels:** "Today", "Tomorrow", "Wed 5/6" (named day for upcoming weekdays in the window), "Mon 5/11" etc.

**Question prompts** (skip if `--brief`): For each workstream, Claude composes 1–3 questions specific to its milestone state. Examples of question shapes:
- *"X has been in progress — concretely, what % is left? Half a day or two days?"*
- *"Y depends on Z. If Z slips, Y slips with it."*
- *"This milestone's owner is {other person} — does {they} need anything from you to hit it?"*
- *"This is your only milestone {day} — is it 2 hours or 6 hours?"*
- *"X workstream has N milestones converging on {day}. Is that real, or is one or two better moved to {alt day}?"*

Don't pose generic questions ("How is this going?"). Each prompt should reference the specific milestone state visible in the data.

---

## Step 6: Day-stack-up section

After the tree, render a stack-up callout for any single day in the window with 3+ milestones across workstreams:

```
## {Friday 5/8} stack-up

If you don't move work, **{day} lands**: {milestone 1} · {m2} · {m3} *(owner)* · ...

That's {N} milestones on you, {M} on others. {one-line reality check on whether they co-fit}.

> *Worth thinking through:*
> - Which is most movable to {next day}?
> - Which is least movable / gates downstream work?
```

Only render if the data warrants it (≥3 milestones converging).

---

## Step 7: Draft sequence

```
## Draft {planning_day} sequence (starting point — adjust as you think)

1. **First thing:** {task} — {short why}
2. **Morning deep work (~{hrs}):** {task} — {short why}
3. **Afternoon (~{hrs}):** {task} — {short why}
4. **Late afternoon / end of day:** {task}
5. **15-min poke:** {quick win or blocker nudge}

This is a starting point — the prompts above are what to push back on before you commit to it.
```

Sequence rules:
- 4–6 items, time-anchored loosely ("morning", "afternoon")
- Lead with anything overdue from yesterday's commitments
- Then the heaviest deep-work milestone for the focus initiative
- Then secondary milestones
- 15-min items (nudges, scoping, quick admin) as fillers

Frame each step with a *why* (reason from the tree above), not just the task name.

---

## Step 8: Push the plan to Sunsama (via MCP)

After the draft sequence and before the closing prompt, write the day's plan directly into Sunsama via the Sunsama MCP server (`https://api.sunsama.com/mcp`, registered as `sunsama` in `.mcp.json`).

**Convention:** every roadmap milestone should have a backing Linear issue (see project memory `project_milestone_linear_convention`). Sunsama tasks reference the Linear issue by ID/URL so the integration can deep-link.

### Step 8a: Discover Sunsama tools (first run only)

The Sunsama MCP exposes a set of tools whose exact names are discoverable via the runtime tool list. On first invocation in a session, identify the relevant ones — the typical shape:

- A "list tasks" tool (filterable by date) — used for idempotency
- A "create task" tool — accepts title, date, time estimate, channel, notes, optional URL
- A "list channels" / "list streams" tool — used to validate channel mapping
- (Optionally) "update", "complete", "delete" tools for later commands

If exact tool names differ from this spec's expectations, prefer the actual MCP-exposed names. Tool discovery output supersedes guesses below.

### Step 8b: Resolve channel mapping

For each draft-sequence entry, the channel = the workstream name from the roadmap. Map workstream names to Sunsama channel IDs once per session:
1. Call the Sunsama "list channels" tool
2. Match by exact name (case-insensitive) — `Execution Pipeline`, `Living Knowledge Ecosystem`, etc.
3. If a workstream has no matching Sunsama channel, fall back to the user's default channel and emit a one-line warning: `⚠️ No Sunsama channel for "{workstream}" — used default. Add the channel in Sunsama if you want clean rollups.`

For client-tactical items, use a `Client work` channel (or default if absent).

### Step 8c: Idempotency check

Before creating tasks, call the Sunsama "list tasks" tool filtered to the planning date. If the title of any draft-sequence entry already exists in that day's Sunsama plan, skip creation for that entry (avoids duplicates if the user re-runs the command).

### Step 8d: Resolve Linear issue references

For each draft-sequence entry whose underlying work has a backing Linear issue, fetch the Linear URL via Linear MCP. Include it in the Sunsama task notes so the deep-link works.

To find the right Linear issue:
- Filter `list_issues(assignee="me", project="{workstream Linear project}", state in {started, unstarted})` for the relevant workstream
- Match by title similarity to the draft-sequence entry, or by milestone reference
- If no match found, omit the Linear URL and note `(no backing Linear issue — milestone-only)` in the description

### Step 8e: Create tasks

For each draft-sequence entry not skipped by 8c, call the Sunsama "create task" tool with:
- `title` — short, action-oriented (e.g., `"Sequencer push to all 3 platforms"`)
- `date` — the planning date (ISO `YYYY-MM-DD`)
- `timeEstimate` (or whatever the field is) — minutes, derived from the parenthetical (`~1h` → 60, `~30m` → 30)
- `channel` / `channelId` — resolved in 8b
- `notes` (or `description`) — the "why" line + milestone slug + Linear URL if found
- Any other required fields per the MCP tool's schema

Run creates **in parallel** when supported; otherwise sequentially.

### Step 8f: Render confirmation block in chat

After tasks are pushed, render a brief confirmation:

```
## Pushed to Sunsama — {planning_day}

✅ {N} tasks created · {M} skipped (already in Sunsama)
{If any warnings, list them here}

Tomorrow's plan is in Sunsama. Open the app, set time blocks, you're done.
```

### Failure modes

- **Sunsama MCP unavailable / token invalid** → fall back to rendering the paste-text block (the original Step 8 format from before this revision). Print a clear banner: `⚠️ Sunsama MCP not reachable — falling back to paste-text. Check $SUNSAMA_MCP_TOKEN and restart Claude Code.`
- **Some creates succeed, some fail** → report partial results in the confirmation block and list the failed entries with their error reasons.
- **`--dry-run` flag set** → skip 8e entirely; render the would-be tasks as a preview block (same paste-text format) prefixed with `# Sunsama push preview (not written)`.
- **`--no-sunsama-push` flag set** → skip 8e; render paste-text only.

### Paste-text fallback format (when MCP unavailable, --no-sunsama-push, or --dry-run)

```
## Sunsama plan for {planning_day}

— {Task name}
  ⏱ {time} · 📁 {Channel} · Why: {one-line why}
  → {Linear: ISSUE-ID | Milestone-only — no Linear issue}

— {Task name}
  ...
```

---

## Step 9: Closing prompt

End with a single line:

> *Open question for you: {one synthesized question Claude composes — usually about whether the focus is right, or whether a Friday-stacking is acceptable, or what to defer to next week}*

This invites the user to talk back.

---

## Memory — focus initiative

Persist the chosen focus to `memory/project_daily_focus.md`:

```
---
name: Daily-priorities focus
description: Current strategic focus for /daily-priorities runs
type: project
---

Focus initiative: `{slug}` ({name})
Set: {YYYY-MM-DD}

Why this is focus: {short reason if user provided one, else "user explicitly set"}
```

Read it on every run. If absent, prompt user once (only on the first run) and ask which initiative to focus on, with the active list as choices.

---

## Empty states

- **No `roadmap.data.json` available:** print a banner: `⚠️ Roadmap data not found at ../kale-wiki/content/company/roadmap.data.json. Falling back to Linear-only view, which doesn't reflect the actual roadmap commitments.` Then walk Linear projects instead of milestones.
- **No active initiatives in window:** `> ✅ No roadmap milestones in the next 7 days. Either everything's shipped or planning is overdue.`
- **No focus set:** Surface all initiatives equally; don't promote any. Mention at the bottom: *"Set a focus with `--focus [slug]` to highlight one initiative across runs."*

---

## What this command will NOT do

- Will not pick tasks for you. It surfaces, prompts, and drafts — you decide.
- Will not link task names as markdown URLs in the body — plain text only.
- Will not write to disk except for the focus memory file.
- Will not edit Linear or the roadmap data.
- Will not auto-create missing Linear issues for milestones — it flags them so you can create them via `/roadmap` or directly in Linear.
- Will not surface every Linear issue — supporting evidence only, tied to specific milestones or blockers.
- Will not list per-client noise (e.g., 14× duplicate analytics tickets) inline; aggregate as a one-line "skip / batch later" tail if needed.
- Will not duplicate Sunsama tasks on re-runs — the idempotency check in Step 8c skips entries already present for the planning date.
- Will not modify or delete existing Sunsama tasks. Only creates. To clear a day, the user removes manually in Sunsama (or a future `--reset-sunsama` flag).
