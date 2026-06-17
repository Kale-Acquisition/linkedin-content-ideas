# /roadmap

> View the build queue, triage stakeholder requests, and prepare for the weekly priority review.

**Usage:** `/roadmap [flags]`

**Flags:**
- (no flag) — Show current build queue from Linear, sorted by score
- `--meeting-prep` — Generate weekly sync agenda with score breakdowns + strategy drift detection
- `--triage` — Review new Notion intake entries (all Types: Build Request, Problem, Idea). Build Requests get scored and create Linear issues on accept. Problems and Ideas just flip Status to Accepted (Problems surface in `--pre-read`; Ideas in `/generate-automation-ideas`). Auto-rejects per-client tactical work per the boundary doc (see below).
- `--my-queue [person]` — Show one person's roadmap involvement: In Progress / Coming Up / Recently Shipped, plus L1↔L2 graduations involving them. Defaults to active user.
- `--layer L1|L2|L3` — Filter view by build layer
- `--ship [title]` — Mark a Linear issue as Done, record outcome
- `--promote [title]` — Graduate: L1→L2 or L2→L3
- `--deprioritize [title] [reason]` — Move to backlog with logged reason
- `--create-project [name]` — Create a new Linear project (workstream)
- `--add [title]` — Create a new Linear issue in a project
- `--rescore` — Rescore all open issues against current strategy
- `--advance "[updates]"` — Apply a batch of project updates conversationally. Parses intents (ship milestone, status flip, blocked, criterion met, etc.), proposes a checklist, applies on confirm, mirrors project-level changes to the wiki roadmap.
- `--sync-now` — Pull current Linear state and push execution updates (status, targetDate, owner, title) into `roadmap.data.json` in kale-wiki. Read-only on Linear; never overwrites wiki-side judgment statuses (`In Validation`, `Planned`, `Backlog`). Commits and pushes to kale-wiki master.
- `--backfill-linear-ids` — One-time (or top-up) helper that matches each roadmap milestone to its Linear backing item (Project Milestone for L2/L3, Issue for L1), and writes `linearMilestoneId` / `linearIssueId` into `roadmap.data.json`. Run before `--sync-now` works on a milestone; unmapped milestones are silently skipped by sync.
- `--pre-read` — Generate the L10 pre-read digest (rocks + Problems DB + client snapshot). Default = founder weekly. Add `--monthly` for the heavier monthly strategy version. Add `--fill-issues` to also close backing-issue gaps for the new sprint (the Saturday ritual).

**Examples:**
- `/roadmap` — view the current build queue
- `/roadmap --meeting-prep` — generate the weekly sync view
- `/roadmap --triage` — review and triage new stakeholder requests
- `/roadmap --layer L2` — show only L2 workflow items
- `/roadmap --ship "Bounce rate monitoring"` — mark as done
- `/roadmap --promote "Inbox warmup script"` — graduate L1→L2
- `/roadmap --deprioritize "Finance dashboard" "Not a priority this quarter"` — move to backlog
- `/roadmap --create-project "Data Pipeline"` — create a new workstream
- `/roadmap --add "Bounce rate alerting"` — add an issue to the queue
- `/roadmap --rescore` — recalibrate scores after strategy changes
- `/roadmap --advance "shipped Bison test migration, Deliverability Module is now in progress, blocked on Azhar's Supabase access"` — batch update post-L10
- `/roadmap --advance "Client Portal kicked off, Arra leading"` — status flip + lead change
- `/roadmap --advance "rename Knowledge Base to Living Knowledge Ecosystem"` — project rename, mirrored to wiki
- `/roadmap --advance "criterion met for Strategy Engine"` — flip `criteriaMet: true` on the workstream's completion criteria
- `/roadmap --my-queue` — show the active user's involvement across the roadmap
- `/roadmap --my-queue Azhar` — show Azhar's involvement (1:1 prep)
- `/roadmap --sync-now` — pull Linear state into wiki roadmap (post-L10 flips, mid-day status changes)
- `/roadmap --backfill-linear-ids` — match unmapped roadmap milestones to Linear items and store the IDs
- `/roadmap --pre-read` — generate pre-read for next L10 (Friday EOD or Saturday morning)
- `/roadmap --pre-read --monthly` — generate the monthly strategy L10 pre-read
- `/roadmap --pre-read --fill-issues` — pre-read + close backing-issue gaps for the new sprint (Saturday-ritual mode)

---

## Architecture

Two layers, one interface:

- **Notion Intake DB** (stakeholder-facing) — single intake surface for the team. Anyone (Mike, Arra, team) submits anything, tagged by `Type`: `Build Request` (problem + solution, ready to scope), `Problem` (something painful, no solution required), or `Idea` (longer-term, ready to be sequenced).
- **Linear** (execution) — Build queue. Issues with Layer labels (L1/L2/L3), native priority, git-linked branches. Where Roshan works.
- **This command** — bridges both. Default view reads Linear. `--triage` scans all New Intake entries regardless of Type and routes by Type (Build Request → Linear; Problem/Idea → flip Status to Accepted only, surfaced elsewhere). `--pre-read` reads Intake (filtered to `Type = Problem`) for the L10 problems section.

**SLA model:** Two tiers.
- **Urgent** — something is broken or blocking client work. Same-day triage. Bypasses scoring.
- **Standard** — everything else. Scored and ordered by composite score. Reviewed at weekly sync.

**Sprint cadence:** Sprints run **Saturday → Friday**. Pre-read is generated Friday EOD (end of sprint); the founder L10 happens the following Monday (day 3 of the new sprint, reviewing the just-completed sprint). When the doc says "this week," read it as "this sprint."

---

## Universal patterns

**Every new workstream starts with a "Discovery + Planning" milestone.** Auto-created by `--create-project`. Locks V1 scope, identifies remaining milestones with target dates, surfaces blockers and dependencies — before any execution work begins. Reason: the real milestone breakdown isn't knowable until you start working on it. Discovery codifies the learning loop instead of pretending you can plan it perfectly upfront.

This rule applies whenever a workstream is created — via `--create-project`, via `--triage` accepting a request as a new project, or manually. If you find yourself adding a workstream without this milestone, that's a bug in the entry path.

**Every milestone in someone's current sprint must have ≥1 backing Linear issue.** Status is derived from issue state for most transitions, with one manual flag (`In Validation`) for the soak period between "built" and "verified shipped":

- All linked issues open → milestone status = `Planned`
- Any issue closed, any open → `In Progress`
- All issues closed AND owner has flagged `In Validation` → `In Validation` (work is built, real-world check pending)
- All issues closed AND no `In Validation` flag → `Shipped`
- Zero issues attached on a sprint milestone → malformed, surface at L10

Owner picks the granularity — 1 issue or 7, whatever makes the work trackable. Issue count isn't the contract; the milestone shipping by the target date is.

**`In Validation` is the only manual status flag.** Use it when the build issues have closed but you want a real-world soak before declaring `Shipped` — e.g., a capture pipeline is wired up but you want to watch it run against real meetings/messages for a day or two first. Once verified, the owner flips it to `Shipped` (manual). If it never validates, flip back to `In Progress` and reopen the relevant issues. Same flag applies at the workstream level (rare, but valid).

**Enforcement scope (decided 2026-05-20):** sprint-only. Don't backfill all existing milestones in `roadmap.data.json`. Apply the rule to:
- New milestones (created via `--add-milestone`, `--advance "add milestone..."`, or `--create-project`)
- Any milestone currently in `sprintItems[]` for an active workstream — must have ≥1 issue by Monday's L10
- Future-planned milestones stay loose until they enter a sprint

Practical effects on this command:
- `--add-milestone` prompts for ≥1 issue title before creating the milestone in Linear
- `--advance` derives status from issue state for sprint milestones; manual status flips are still accepted for non-sprint milestones (backfill-grace)
- `--pre-read` and `--meeting-prep` flag any sprint milestone with zero backing issues as `(needs backing issue)`
- Wiki sync (`roadmap.data.json`): for sprint milestones, compute `status` from issue state; for non-sprint, accept the manual field

Why: empty milestones only signal at L10 (too late). Backing issues give daily standup a surface to point at, make Linear progress % meaningful again, and let Sunsama pull the work directly. See `project_milestone_linear_convention` memory for the full rationale.

---

## Scoring Model

Every Standard request is scored on 4 factors. Each score level maps to an observable gate — a condition you can point to, not a judgment call. Urgent requests bypass scoring entirely (Linear priority = 1, same-day triage).

### Factors

| Factor | Weight | What it answers |
|---|---|---|
| **Strategic Alignment (SA)** | 40% | Does this serve what we said matters? |
| **Impact (IM)** | 25% | Who's affected and how badly? |
| **Return (RE)** | 20% | What does the business get when it's built? |
| **Feasibility (FE)** | 15% | How hard is it? |

### Composite Formula

**Composite** = (SA x 0.40) + (IM x 0.25) + (RE x 0.20) + (FE x 0.15)

Range: 1.00–5.00.

### Score-to-Priority Mapping

| Condition | Linear Priority | Meaning |
|---|---|---|
| SLA = Urgent | 1 (Urgent) | Bypass scoring, same-day |
| Score >= 3.5 | 2 (High) | Top of Standard queue |
| Score >= 2.5 | 3 (Medium) | Middle of Standard queue |
| Score < 2.5 | 4 (Low) | Bottom / backlog |

### Strategic Alignment (SA) — 40%

Anchored to `context/strategy.md`. Priorities are numbered — scoring is mechanical.

| Score | Gate |
|---|---|
| **5** | Request directly serves **Priority 1** (deliverability & infrastructure management) |
| **4** | Request directly serves **Priority 2** (internal tooling & automation) |
| **3** | Request directly serves **Priority 3** (client acquisition) |
| **2** | Supports a priority but indirectly — one step removed (e.g., "better reporting" supports deliverability but isn't deliverability work itself) |
| **1** | Can't map to any of the three priorities |

**Assessment:** Read the request, read `strategy.md`, match. If the request names a priority area, the score is mechanical. If it doesn't obviously map, default to 2 and explain why. When `strategy.md` changes, scores shift — priorities are defined there, not in Claude's head.

### Impact (IM) — 25%

Who is affected and what happens if we don't build it. The requestor's seniority or emphasis doesn't change the score — the gate is who's affected, not who's asking.

| Score | Gate |
|---|---|
| **5** | Multiple clients named as affected, OR revenue/retention at risk (client churn, contract at stake) |
| **4** | One specific client named as affected, OR an external-facing process is broken/degraded |
| **3** | Internal team affected — a process the team does daily/weekly is slow, manual, or error-prone |
| **2** | Improvement to something that works but could be better — no one is blocked or slowed significantly |
| **1** | No clear affected party or the problem is hypothetical/future |

**Assessment:** Look for named clients, named people, or described frequency in the request. If none present, ask: "Who's affected by this and what happens if we don't build it?"

### Return (RE) — 20%

What does the business get when this is built? Not just time savings — also quality, reliability, revenue protection, visibility. The question: **"What breaks or stays broken if we don't build this?"**

| Score | Gate |
|---|---|
| **5** | Directly protects or enables revenue — prevents client churn, unblocks new client onboarding, or fixes something clients see |
| **4** | Significantly improves output quality or reliability — fewer errors, better data, consistent delivery across clients |
| **3** | Saves meaningful recurring time (2-5+ hrs/wk) OR gives visibility that doesn't exist today (monitoring, reporting, dashboards) |
| **2** | Minor improvement to time, quality, or visibility — things work fine without it but would be better with it |
| **1** | Minimal ongoing benefit — one-time fix, cosmetic, or "nice to have" with no measurable return |

**Assessment:** Look at what changes when this is built. "Clients are complaining about X" = revenue protection (5). "We can't see whether Y is working" = visibility (3). "This would be cleaner" = 2.

### Feasibility (FE) — 15%

How long to build. Weighted lowest deliberately — easy things don't automatically win, they just break ties.

| Score | Gate |
|---|---|
| **5** | Hours — config change, script tweak, existing tool. Typical L1. |
| **4** | 1-3 days — small build with known patterns, no new infrastructure |
| **3** | ~1 week — moderate build, may need design decisions. Typical L2. |
| **2** | 2-4 weeks — significant build, new infrastructure or integrations required |
| **1** | Months — large platform build, multiple phases, unknown territory. Typical L3. |

**Assessment:** Layer selection gives a strong signal (L1→4-5, L2→3-4, L3→1-2). If the layer and description conflict, flag it.

### Explainability

When scoring an item, write one sentence per factor citing the evidence:

```
Score: 3.60 -> High priority

- SA: 4 — Campaign setup automation directly serves P2 (internal tooling & automation)
- IM: 3 — Affects the delivery team's daily workflow; no specific client blocked
- RE: 4 — Improves consistency across clients, reduces setup errors (quality + reliability)
- FE: 3 — ~1 week build, needs Instantly API integration (L2)
```

If Roshan disagrees with any line, he says which factor and why — adjust that one number, the rest stay anchored to their evidence.

### Bias Controls

| Bias | How scoring prevents it |
|---|---|
| **Recency** (whatever happened last feels urgent) | Impact gates require naming who's affected, not just what happened recently |
| **Loudest voice** (whoever pushes hardest gets priority) | SA is anchored to the written strategy, not to who's asking |
| **Easy wins** (default to quick fixes) | Feasibility is only 15% weight — hard-but-important work doesn't get buried |
| **Sunk cost** (keep building because we started) | Rescoring can demote items that no longer align with current strategy |
| **Shiny object** (exciting ideas over strategic ones) | SA is 40% of the score — excitement without strategic alignment scores low |

### Score Block Format

Appended to the Linear issue description when scoring:

```
---
**Score:** 3.85
SA:4 | IM:3 | RE:4 | FE:4
Scored: 2026-04-14
```

This is human-readable and machine-parseable. The `/roadmap` command reads it for sorting. If someone edits it manually in Linear, that's fine — the score is advisory, not sacred.

---

## Key IDs

| Resource | ID |
|---|---|
| **Notion Intake DB** | `e362fa70b5764e6fa9a2451c9642daf7` |
| **Notion Intake data source** | `65be880e-48e8-40cb-9f4a-b3e965cdfbd9` |
| **Linear Technology team** | `65896885-284f-4c32-b1f7-1100b2c58748` |
| **Linear Operations team** | `c475290d-3edf-4d31-a67c-97498ea2db10` |
| **Linear label: L1** | `788469cb-fa4c-4dfa-9e73-0e9a05041758` |
| **Linear label: L2** | `f7e00350-96f9-4c0c-a201-0ebfe3da33aa` |
| **Linear label: L3** | `a6e770b7-6b1b-4eaf-b8fd-a771d897ee39` |
| **Linear label: request** | `97b47ddf-835e-488b-8ad2-07bdda1a1695` |

---

## Step 1: Parse Arguments

Parse `$ARGUMENTS` for flags:

| Flag | Default | Notes |
|---|---|---|
| `--meeting-prep` | false | Generate weekly sync view |
| `--triage` | false | Review Notion requests |
| `--layer` | — | Filter: L1, L2, or L3 |
| `--ship [title]` | — | Mark issue as Done |
| `--promote [title]` | — | Graduate layer |
| `--deprioritize [title] [reason]` | — | Move to backlog |
| `--create-project [name]` | — | Create a Linear project |
| `--add [title]` | — | Create a Linear issue |
| `--rescore` | false | Rescore all open issues against current strategy |
| `--advance "[updates]"` | — | Apply a batch of conversational updates |
| `--pre-read` | false | Generate L10 pre-read digest |
| `--monthly` | false | (with `--pre-read`) Use the monthly strategy format |
| `--fill-issues` | false | (with `--pre-read`) Also close backing-issue gaps for the new sprint |

Routing:
- If `--triage`, skip to Step 4 (Triage).
- If `--meeting-prep`, skip to Step 5 (Meeting Prep).
- If `--ship`, skip to Step 6 (Ship).
- If `--promote`, skip to Step 7 (Promote).
- If `--deprioritize`, skip to Step 8 (Deprioritize).
- If `--create-project`, skip to Step 9 (Create Project).
- If `--add`, skip to Step 10 (Add Issue).
- If `--rescore`, skip to Step 11 (Rescore).
- If `--pre-read`, skip to Step 12 (Pre-read). If `--fill-issues` is also set, continue into Step 12.5 (Fill backing issues) after pre-read renders.
- If `--advance`, skip to Step 13 (Advance).
- Otherwise, proceed to Step 2 (Default View).

---

## Step 2: Load Linear Issues

Query Linear for issues across the Technology and Operations teams. **Query by state type, not state name** — different teams customize state names (e.g., Technology uses "In Development" while Sales uses "In Progress", Clients uses "To Do This Week" while Sales uses "Todo"), but state types are universal across the workspace.

Linear state types:
- `backlog` — everywhere called "Backlog"
- `unstarted` — ready to start ("Todo", "Todo This Week", "To Do This Week")
- `started` — actively being worked ("In Progress", "In Development", "QA", "Pending Client Approval")
- `completed` — everywhere called "Done"
- `canceled` — "Canceled", "Duplicate", sometimes "Blocker"

Use `list_issues` with these calls:

1. **Active (started):** `list_issues(team: "Technology", state: "started", limit: 50)` and `list_issues(team: "Operations", state: "started", limit: 50)` — catches "In Development", "QA", etc.
2. **Queued (unstarted):** `list_issues(team: "Technology", state: "unstarted", limit: 50)` and `list_issues(team: "Operations", state: "unstarted", limit: 50)` — catches "Todo This Week", etc.
3. **Recently Done (completed):** `list_issues(team: "Technology", state: "completed", updatedAt: "-P14D", limit: 20)` and `list_issues(team: "Operations", state: "completed", updatedAt: "-P14D", limit: 20)`

If `--layer` is specified, filter results to only issues that have the matching label (L1, L2, or L3).

**Note:** Throughout the rest of this document, "In Progress" refers to issues with state type `started` and "Todo" refers to type `unstarted`. When writing states back via `save_issue` (in `--ship`, `--deprioritize`), use the state name directly since "Done" and "Backlog" are consistent across all teams in this workspace.

---

## Step 3: Render Default View

Present the build queue:

```
## Build Queue — Sprint of [most recent Saturday date]

### In Progress ([count])
[For each issue, sorted by score (highest first), then Urgent-SLA issues at top:]
- **[Title]** — [Layer label] | Score: [composite] ([SA/IM/RE/FE]) | Team: [team] | Project: [project]
  Branch: `[gitBranchName]`
  [If has labels including "request":] Requestor: [from description or Notion link]
  [If no score block in description:] (unscored)

### Next Up ([count], sorted by score)
[Issues in Todo state, sorted by composite score (parsed from description). Unscored issues sort last at their current Linear priority:]
- **[Title]** — [Layer label] | Score: [composite] ([SA/IM/RE/FE]) | Project: [project]

### L1 Floor
[Issues with L1 label, any status except Done:]
- **[Title]** — [status] | [assignee]

### Recently Shipped (last 2 weeks)
[Issues in Done state, last 14 days:]
- **[Title]** — [Layer label] | Done: [completedAt date] | Project: [project]
```

If there are no issues in a section, show: `_(none)_`

At the end, show a summary line:
```
**Queue:** [X] in progress, [Y] queued, [Z] shipped last 2 weeks
```

---

## Step 4: Triage (`--triage`)

Triage every New Intake entry regardless of Type. Build Requests are bridged into Linear (scored, with full accept/decline/skip flow). Problems and Ideas are reviewed and either Accepted (surfaced in `--pre-read` or `/generate-automation-ideas` respectively) or Declined — no Linear creation, no scoring.

### Step 4.1: Load New entries (all Types)

Query the **Intake DB** (data source `65be880e-48e8-40cb-9f4a-b3e965cdfbd9`) for untriaged entries. Filter for:
- `Status` = "New"
- (no Type filter — scan Build Request, Problem, and Idea together)

Sort by `Submitted` ascending (oldest first), so the longest-waiting entries get triaged first.

**Skip entries that are incomplete:**
- Title is empty or contains "[Template]" → skip (placeholder, not a real entry)
- Description is empty → flag during presentation, but still show

(Intake DB doesn't have a separate Urgency field — urgency is set during triage by Roshan, only relevant for Build Requests.)

### Step 4.1.5: Backfill Missing Submitter

For each loaded entry, check if the `Submitter` field is empty. Stakeholders sometimes forget to set it. Resolve in this order:

1. **Infer from page creator:** Use `notion-fetch` on the page and look at the `created_by` metadata. If the creator is a known stakeholder (Mike, Arra, or another team member), set the Submitter to that user via `notion-update-page` before presenting the request.
2. **Ask during triage:** If the creator isn't a known stakeholder or is ambiguous, flag it during Step 4.2 presentation: `⚠ Submitter field is blank on this entry — who submitted this?` and prompt Roshan for the answer, then set it before creating the Linear issue.

To look up a user ID for setting Submitter, use `notion-search(query_type: "user", query: "[name]")`. The Submitter field accepts a JSON array of user IDs, e.g. `["cbadf6cf-6cd5-4eee-b49b-8adbf52d36a7"]`.

**Why this matters:** Submitter is the accountability link — it's how we know who to loop back to when the work ships, and it's how `--meeting-prep` attributes requests to stakeholders. A blank Submitter breaks that chain.

### Step 4.1.6: Boundary check

Before presenting an entry, check whether it belongs on the founder roadmap at all. The roadmap is for **Service Ops + Product & Platform** work — see `knowledge/operations/roadmap-boundary.md`.

Apply the boundary check to **Build Requests only**. Problems and Ideas are reflective signals, not execution work — they don't carry the same tactical/strategic boundary risk and should always be presented (so Roshan can mark Accepted or Declined with context).

**Hard reject** (Build Request only — don't present, don't score, don't create a Linear issue): a request that names a specific client and uses execution-level verbs ("send", "pull", "rerun", "fix template", "renew", "compile", "redo"). This is per-client tactical execution and belongs in the relevant `kale-{client}` repo + Weekly Client Review.

For each rejected request:
- Update the Notion entry: `Status` → "Declined", append a triage note to `Description`: `[Boundary-declined YYYY-MM-DD]: Per-client tactical work — belongs in kale-{client} repo + Weekly Client Review, not the founder roadmap. See knowledge/operations/roadmap-boundary.md.`
- Note in the triage output: `Boundary-rejected: [title] — [client] tactical, redirected.`

**Flag, don't reject** (present with a warning): a request that has only one signal (named client OR execution verbs, not both). Add a line to the request presentation: `⚠ Boundary check: borderline — confirm this isn't kale-{client} tactical work before scoring.`

If unsure between hard-reject and flag, flag. Better to present and let Roshan decide than to drop something quietly.

### Step 4.2: Present Each Entry

For each untriaged entry, display (Type-aware header):

```
### [Type]: [Title]
**Submitter:** [Submitter field — or "⚠ inferred from page creator: [name]" / "⚠ ASK: who submitted?"]
**Description:** [Description text]
**Submitted:** [Submitted date]
**Notion URL:** [page URL]
```

Group entries by Type when presenting (Build Requests first, then Problems, then Ideas) so Roshan stays in one mode at a time.

Then ask: **"Accept, Decline, or Skip?"**

For **Build Requests** only, also ask: **"Urgent or Standard SLA?"** (Roshan calls this at triage time, not the submitter.)

For **Problems** and **Ideas**, no SLA / scoring / Linear creation — accept = move to "Accepted" status; decline = mark "Declined" with reason. They surface elsewhere (Problems in `--pre-read`, Ideas in `/generate-automation-ideas`).

### Step 4.3: Accept

Branch by Type:

**Build Request → create Linear issue.** Prompt for:
1. **Urgency** — Urgent or Standard?
2. **Layer** — L1, L2, or L3?
3. **Team** — Technology or Operations? (default: Technology for L2/L3, Operations for L1)
4. **Score:**
   - If Urgency = "Urgent": skip scoring, set Linear priority = 1 (Urgent). Note in output: "Urgent SLA — scoring bypassed."
   - If Urgency = "Standard": Read `context/strategy.md` for current priorities. Propose a score using the Scoring Model rubrics:
     ```
     Score: 3.85 -> High priority
     - SA: 4 — [one sentence citing evidence]
     - IM: 3 — [one sentence citing evidence]
     - RE: 4 — [one sentence citing evidence]
     - FE: 3 — [one sentence citing evidence]
     Confirm or adjust?
     ```
     Roshan confirms or adjusts individual factors (e.g., "make IM a 4"). Recalculate composite if adjusted.
   - Derive Linear priority from composite using the Score-to-Priority Mapping table.
5. **Project** — assign to existing Linear project, or none?

Create the Linear issue via `save_issue`:
- **title:** the Title from the Intake entry
- **teamId:** selected team ID
- **priority:** derived from score (1=Urgent, 2=High, 3=Medium, 4=Low) per the mapping table
- **labels:** the selected Layer label ID + the `request` label ID
- **description:** Include:
  - Description text from the Intake entry
  - Link back to Notion entry: `[Notion intake](https://notion.so/[page-id])`
  - Submitter name
  - Score block (see Score Block Format in Scoring Model section)

Then update the Notion entry: `Status` → "Accepted"; `Linked Linear` → the Linear issue URL.

**Problem → mark Accepted only.** No Linear creation, no scoring. Update the Notion entry:
- `Status` → "Accepted"
- (Optional) Append a triage note to `Description` if Roshan adds context: `[Triaged YYYY-MM-DD]: [note]`

The accepted Problem will surface in the next `--pre-read` for L10 IDS discussion.

**Idea → mark Accepted only.** No Linear creation, no scoring. Update the Notion entry:
- `Status` → "Accepted"
- (Optional) Append a triage note to `Description` if Roshan adds context: `[Triaged YYYY-MM-DD]: [note]`

The accepted Idea is now in scope for `/generate-automation-ideas` to pick up and rank.

### Step 4.4: Decline

If declined, ask for a brief reason. Update the Notion entry:
- Set `Status` to "Declined"
- Append to `Description`: `[Declined YYYY-MM-DD]: [reason]`

(Same flow regardless of Type.)

### Step 4.5: Skip

Move to the next entry without action.

### Step 4.6: Summary

After processing all entries, show counts broken out by Type:
```
**Triage complete:**
  Build Requests — [A] accepted (→ Linear), [B] declined, [C] skipped
  Problems       — [D] accepted, [E] declined, [F] skipped
  Ideas          — [G] accepted, [H] declined, [I] skipped
```

---

## Step 5: Meeting Prep (`--meeting-prep`)

Generate the weekly sync agenda pre-filled with real data.

### Step 5.1: Load Data

Run these in parallel:
1. **Linear issues** — same queries as Step 2 (In Progress, Todo, Done last 14 days across both teams)
2. **Notion intake** — same query as Step 4.1 (Intake DB, Status=New, all Types). Group results by Type for the agenda render.
3. **Context files** — read `context/strategy.md` and `context/clients.md` for strategy drift detection

### Step 5.2: Strategy Drift Check

For each scored issue (has a score block with `Scored: [date]` in description):
- Check if `strategy.md` has been modified since the scored date
- Check if `clients.md` has changed (new clients, status changes) since the scored date
- If either changed, flag the issue for potential rescoring

### Step 5.3: Render Agenda

```
# Weekly Priority Review — [date]

## 1. Shipped This Sprint
[Issues that moved to Done in last 7 days (Sat → Fri window):]
- **[Title]** — [Layer] | Completed: [date]
[If none:] _Nothing shipped this sprint._

## 2. In Progress
[Active issues:]
- **[Title]** — [Layer] | Score: [composite] ([SA/IM/RE/FE]) | Assignee: [name]
  [If has blockers or stale (no update in 5+ days):] ⚠ No update in [N] days
  [If unscored:] (unscored)

## 3. L1 Floor Check
[L1-labeled issues from last 7 days (any status):]
- **[Title]** — [status] | [resolved/in progress]
[Summary:] _[X] L1 items this sprint._

## 4. New Intake ([count] pending, across all Types)
[Notion entries not yet triaged, grouped by Type:]
- **Build Requests ([n]):** [Title] — Requestor: [name]
- **Problems ([n]):** [Title] — Submitter: [name]
- **Ideas ([n]):** [Title] — Submitter: [name]
[If none:] _No new intake entries._
[If any:] _Run `/roadmap --triage` to process these — Build Requests get scored into Linear, Problems/Ideas just flip to Accepted._

## 5. Queue Review (top 5 by score)
[Top 5 Todo issues by composite score, with score breakdown:]
1. **[Title]** — [Layer] | Score: [composite] (SA:[n] IM:[n] RE:[n] FE:[n]) | Project: [project]
2. ...
[Unscored issues listed separately at the end]

## 6. Strategy Drift
[If any issues flagged in Step 5.2:]
⚠ Strategy or client context updated since these items were scored:
- **[Title]** — scored [date], strategy updated [date]
_Run `/roadmap --rescore` to recalibrate, or review at sync._
[If no drift:] _No strategy changes since last scoring._

## 7. Signals
_Bring to meeting: anything from client work that should reshape priorities. Captured signals can trigger rescoring._
```

---

## Step 6: Ship (`--ship`)

Mark a Linear issue as Done.

1. Parse the title from arguments
2. Search Linear issues: `list_issues(query: "[title]", limit: 10)` across Technology and Operations teams
3. If multiple matches, present them and ask which one
4. Ask: "Any outcome notes?" (optional — what was the result, what shipped)
5. Update the issue via `save_issue`:
   - Set state to "Done"
6. If outcome notes provided, add a comment to the issue via `save_comment`
7. Confirm: **"Shipped: [Title]"**

---

## Step 7: Promote (`--promote`)

Graduate an issue from one layer to the next.

1. Parse the title from arguments
2. Search Linear issues: `list_issues(query: "[title]", limit: 10)`
3. Read current labels — determine current layer (L1, L2, or L3)
4. Determine next layer:
   - L1 → L2
   - L2 → L3
   - L3 → already at top, inform user
5. Update the issue via `save_issue`:
   - Remove old layer label, add new layer label
6. Add a comment: `Graduated from [old layer] to [new layer]. [Reason if provided.]`
7. Confirm: **"Promoted [Title]: [old] → [new]"**

---

## Step 8: Deprioritize (`--deprioritize`)

Move an issue to backlog with a logged reason.

1. Parse the title and reason from arguments
2. Search Linear issues: `list_issues(query: "[title]", limit: 10)`
3. Update the issue via `save_issue`:
   - Set state to "Backlog"
   - Set priority to 4 (Low)
4. Add a comment: `Deprioritized: [reason]`
5. Confirm: **"Deprioritized: [Title] — [reason]"**

---

## Step 9: Create Project (`--create-project`)

Create a new Linear project (workstream) with standard configuration.

1. Parse the project name from arguments. If not provided, ask: "What's the workstream name?"
2. Prompt for configuration (with defaults):

| Field | Prompt | Default |
|---|---|---|
| **Team** | "Technology or Operations?" | Technology |
| **Lead** | "Who leads this?" | Roshan Kathir (me) |
| **Status** | "Planned, In Progress, or Backlog?" | In Progress |
| **Description** | "One paragraph — what does this workstream deliver? What does success look like?" | _(required)_ |
| **Start date** | "Start date?" | today |
| **Target date** | "Target date? (optional)" | none |
| **Priority** | "Priority? (1=Urgent, 2=High, 3=Medium, 4=Low)" | 3 (Medium) |

3. Create via `save_project`:
   - `name`: project name
   - `addTeams`: [selected team ID]
   - `lead`: selected lead (user ID or "me")
   - `state`: selected status
   - `description`: the description
   - `startDate`: start date (ISO format)
   - `targetDate`: target date if provided
   - `priority`: selected priority

4. **Create the Discovery + Planning milestone (mandatory).** This is the universal first milestone for every new workstream — see the *Universal patterns* section above. Don't skip; don't ask for confirmation; just do it.

   Call `save_milestone`:
   - `projectId`: the project ID returned in step 3
   - `name`: "Discovery + Planning"
   - `description`: "Lock V1 scope. Identify the remaining milestones with target dates and owners. Surface blockers and dependencies. Done when this workstream's full milestone breakdown is set and the next concrete milestone is ready to start."
   - `targetDate`: `startDate + 7 days` (one week to discover)

5. Confirm with project details and Linear URL:
```
**Created project: [Name]**
Team: [team] | Lead: [lead] | Status: [status]
First milestone: Discovery + Planning (target: [date])
URL: [linear URL]

Next: add issues with `/roadmap --add "[issue title]"`, or use Discovery + Planning as week 1 to lock the rest of the milestones.
```

---

## Step 10: Add Issue (`--add`)

Create a new Linear issue in the build queue.

1. Parse the issue title from arguments. If not provided, ask: "What needs to be built?"
2. Prompt for configuration (with defaults):

| Field | Prompt | Default |
|---|---|---|
| **Project** | "Which project/workstream?" | _(list active projects, let user pick)_ |
| **Team** | "Technology or Operations?" | Inherit from project, or Technology |
| **Layer** | "L1 (quick fix), L2 (workflow), or L3 (platform)?" | L2 |
| **Description** | "What needs to happen? (optional)" | none |
| **Assignee** | "Assigned to?" | me |

3. To list active projects for selection, call `list_projects(state: "started", limit: 20)` (project state type `started` = "In Progress"). Present as a numbered list. User picks by number or types a name.

4. **Score:** Read `context/strategy.md` for current priorities. Propose a score using the Scoring Model rubrics based on the issue title, description, and layer:
   ```
   Score: 3.85 -> High priority
   - SA: 4 — [one sentence citing evidence]
   - IM: 3 — [one sentence citing evidence]
   - RE: 4 — [one sentence citing evidence]
   - FE: 3 — [one sentence citing evidence]
   Confirm or adjust?
   ```
   Roshan confirms or adjusts individual factors. Recalculate composite if adjusted. Derive Linear priority from composite using the Score-to-Priority Mapping table.

5. Create via `save_issue`:
   - `title`: issue title
   - `teamId`: selected team ID
   - `projectId`: selected project ID
   - `priority`: derived from score (1=Urgent, 2=High, 3=Medium, 4=Low) per the mapping table
   - `labels`: [selected Layer label ID] + any additional labels
   - `description`: description (if provided) + score block (see Score Block Format in Scoring Model section)
   - `assigneeId`: selected assignee (or "me")

6. Confirm:
```
**Created: [Title]**
[Layer] | Score: [composite] ([SA/IM/RE/FE]) | Project: [project] | Team: [team]
Branch: `[gitBranchName]`
URL: [linear URL]
```

---

## Step 11: Rescore (`--rescore`)

Rescore all open issues against current strategy. Use when strategy has shifted, new clients have been added, or priorities need recalibration.

1. **Load context fresh:** Read `context/strategy.md` and `context/clients.md` for current priorities and client roster.

2. **Load open issues:** Query Linear for all In Progress and Todo issues across Technology and Operations teams (same queries as Step 2, items 1 and 2).

3. **For each issue:**
   a. Parse the existing score block from the issue description (look for `**Score:**` pattern)
   b. If no score block exists, assess from scratch using the issue title, description, labels, and project
   c. Recalculate all 4 factors (SA, IM, RE, FE) using the Scoring Model rubrics
   d. Compute new composite score
   e. Determine if Linear priority should change based on the score-to-priority mapping

4. **For each issue where the score changed:**
   a. Update the score block in the issue description via `save_issue`
   b. Update Linear priority if the derived priority changed
   c. Add a comment: `Rescored: [old score] → [new score]. [one-line explanation of what changed]`

5. **Report:**
```
**Rescore complete — [X] issues reviewed**

### Changed ([Y] issues)
- **[Title]** — [old score] → [new score] ([old priority] → [new priority])
  SA: [old]→[new] — [reason]
  IM: [old]→[new] — [reason]
  RE: [old]→[new] — [reason]
  FE: [old]→[new] — [reason]

### Unchanged ([Z] issues)
- **[Title]** — [score] (no change)
```

---

## Step 12: Pre-read (`--pre-read`)

Generate the L10 pre-read digest. Default = founder weekly format. Pass `--monthly` for the heavier monthly strategy version.

**When to run:**
- Friday EOD before the founder weekly L10
- 48h before the monthly strategy L10 (with `--monthly`)

**Inputs:**
- Linear (rocks + active workstream milestones, recent shipped, recent new)
- Notion Intake DB (`e362fa70b5764e6fa9a2451c9642daf7`) filtered to `Type = Problem` — Status in [New, Accepted, In Progress] for the active problems list
- Notion Monthly Initiatives DB — current month's rocks + status
- Client sync data in `.sync/clients/` — any client at risk or any notable shift

### Founder weekly format

```
# Founder L10 Pre-read — sprint ending [Friday date]

## Headlines (last 7 days — the just-completed sprint)
- [Anything urgent that hit, max 5 bullets]

## Rock progress
**Roshan**
1. [Rock A] — [Green/Yellow/Red] · [one-line status]
2. [Rock B] — [Green/Yellow/Red] · [one-line status]

**Mike**
1. [Rock A] — ...
2. [Rock B] — ...

## Problems — new or moved this sprint
- [Problem title] · [Submitter] — [1-line]
(Only items in Intake DB where Type = Problem AND (Submitted in the last 7 days OR status changed in the last 7 days — the just-completed Sat → Fri sprint))

## Open issues to consider for IDS
Top 3-5 from Intake DB filtered to Type = Problem AND Status = New, sorted by Submitted date (newest first).

## Client snapshot
- [Client] · [health] · [1-line on what's notable]
(One line per active client.)

## Carry-forward
Outstanding to-dos from last L10. Not yet done = surfaces here.
```

### Monthly format (with `--monthly`)

Everything from weekly, plus:

```
## Initiative health
For each active initiative:
- Milestones shipped this month
- Milestones drifting (>2 weeks behind plan)
- Problems addressed — still open? still right initiative?

## Candidate rocks for next month
[2 per founder, draft titles only — discussed live in the meeting]

## Kill list
Anything currently planned but not actually being worked on. Suggest dropping.
```

### Output

1. Write to `outputs/l10-prep/[YYYY-MM-DD]-l10-pre-read.md` (or `-monthly-pre-read.md`)
2. Post to `#l10-prep` Slack channel via `mcp__claude_ai_Slack__slack_send_message_draft` (don't auto-send — let the user review and ship the draft)
3. Print the file path + Slack draft link

### Error handling

- **Intake DB unreachable:** Skip Problems sections, note in output
- **No client sync data:** Note "Client sync stale — run `/sync-all-clients`"
- **No active rocks in Monthly Initiatives:** Note "No rocks set for this month — set with `/rocks --set`"

### Step 12.5: Fill backing issues (`--fill-issues`, opt-in flag)

When `--pre-read` is invoked with `--fill-issues`, run the regular pre-read first, then close backing-issue gaps for the new sprint. Designed for Saturday morning at sprint kickoff: pre-read still reports on the just-completed sprint (looking back for the next L10), and `--fill-issues` operates on the new sprint that just started (looking forward).

**Pre-condition:** `sprintItems[]` in `roadmap.data.json` must already reflect the new sprint's commitment list. The flow doesn't change `sprintItems` — it backfills issues into whatever's there. If Roshan hasn't updated `sprintItems` yet, the flow will detect this (e.g., last week's milestones all `Shipped`) and prompt: "Sprint items appear to be the previous sprint's. Update sprintItems before running fill-issues?"

#### Step 12.5.1: Detect gaps

For each workstream:

1. Iterate `sprintItems[]`. Skip milestones already `Shipped` or `Backlog`.
2. For each remaining sprint milestone, find its Linear counterpart:
   - Query `list_milestones(project: workstream.slug)`.
   - Match by title — case-insensitive substring or Levenshtein < 30% (same rule as `--advance` Step 13.5).
   - If matched: query backing issues via `list_issues(project: workstream.slug, milestone: <linearMilestoneId>)` (or via `get_milestone` with includeIssues if available).
   - If not matched: the wiki milestone is wiki-only — flag as needing a Linear milestone first.
3. Count open + closed issues for the milestone. **Zero issues = gap.**

For each gap, capture: workstream name, milestone slug + title, owner, target date, Linear milestone id (or `null` if wiki-only), wiki tier (L1/L2/L3), wiki priority.

#### Step 12.5.2: Draft proposals

For each gap, propose **one** backing issue by default (owner picks more during confirm):

| Field | Default |
|---|---|
| **Title** | Action-phrased reframing of the milestone title. Strip wiki noise — drop the trailing context after `—`. E.g., milestone *"Bev runs N2's list-build end-to-end on her own — no Roshan in the loop for the weekly run."* → issue *"Bev runs N2 list-build solo end-to-end this sprint"*. |
| **Description** | Three lines: (1) link to wiki workstream + milestone slug; (2) target date; (3) one-sentence layman's "why this matters" pulled from the wiki workstream's `summary` field (memory: [[feedback_sunsama_layman_description]]) |
| **Assignee** | `milestone.owner` (wiki) → resolve to Linear user via `list_users(query: owner)` |
| **Layer label** | Inherit from workstream `tier` (L1/L2/L3) |
| **Priority** | Inherit from workstream `priority` |
| **projectMilestone** | Linear milestone id, or — if the wiki milestone is wiki-only — propose creating the Linear milestone first (Step 12.5.4) |

For *Discovery + Planning* style milestones, default to a single placeholder issue: *"Scope [workstream] V1 for sprint — lock milestones with target dates and owners."*

#### Step 12.5.3: Confirm checklist

Render a numbered checklist:

```
## Sprint prep — Sat [date] → Fri [date] (Sprint [N])

Gaps detected: [count] sprint milestone(s) with zero backing Linear issues.

1. [Workstream] → [milestone slug] · [owner] · target [date]
   Linear milestone: [exists ("X") / NOT yet created]
   → Proposing:
     [a] [Create Linear milestone "..." in <project>]   (only if wiki-only)
     [b] Issue: "[draft title]"
         Assignee: [Owner] · Layer: [L1/L2/L3] · Priority: [High/Medium/Low]
   Accept (Y/n/edit/+more)?

2. [...]

Apply which?  yes / no / 1,3 / skip 2 / edit 2 [new instruction] / 2: +more
```

User responses:
- `yes` / `all` — apply all proposed
- `no` / `cancel` — abort, "No issues created."
- comma list — apply listed only
- `skip N` — apply all except N
- `edit N [text]` — re-draft N from the new instruction
- `N: +more` — for gap N, prompt for additional sub-issues (titles only); add each as a separate backing issue
- `N: assign [name]` — change assignee for N before applying

#### Step 12.5.4: Apply

For each approved gap, in order:

1. **If wiki-only milestone:** create the Linear milestone via `save_milestone(project, name, targetDate, description)`.
2. **Create the backing issue(s):**
   - `save_issue(teamId, title, description, assigneeId, projectMilestone, projectId, priority, labels)`
   - `labels` includes the layer label id.
   - `projectMilestone` links the issue to the Linear milestone created/found above.
3. Capture the created issue URL + id for the report.

Do not abort on a single failure — log and continue.

#### Step 12.5.5: Re-check + report

Re-scan `sprintItems[]` for gaps. Append to the pre-read output file (`outputs/l10-prep/[YYYY-MM-DD]-l10-pre-read.md`):

```
---

## Sprint prep — issues filled

✓ [N] milestones now have backing issues (was [M] gaps).
[For each created issue:]
- [Workstream] → [milestone title] · created: "[issue title]" ([issue url])
[If any remaining gaps:]
⚠ [K] gaps remaining — skipped or failed:
- [Workstream] → [milestone title] — [reason]
```

Also print to the user terminal:

```
**Fill-issues complete** — [N] created, [S] skipped, [F] failed.
[N] milestones moved from "needs backing issue" to "backed."
[K] gaps still open: [list]
```

#### Step 12.5.6: Edge cases

- **Wiki milestone marked `In Validation` but zero backing issues** — Flag as malformed during gap detection. Surface in the checklist with `⚠ malformed: In Validation flag set but no issues to derive from. Drop the flag, then re-run.` Don't auto-fix.
- **Owner not on active roster** — Prompt: "Owner [name] not found in Linear users. Assign to whom?"
- **`sprintItems` looks like last sprint's commitments** — Detect when ≥80% of `sprintItems` milestones are `Shipped`. Prompt: "Sprint items look like the previous sprint. Update `sprintItems` before running fill-issues?"
- **Linear milestone exists but doesn't match wiki title closely** — Surface as ambiguous: "Closest Linear milestone is X; create new one or attach to X?"
- **No `--fill-issues` flag passed** — Skip this step entirely; pre-read behaves as before.

---

## Step 13: Advance (`--advance`)

Apply a batch of conversational project updates. Parse intents from a single string, propose a numbered checklist of Linear changes, get user confirmation, apply the approved changes, and mirror project-level changes (rename, status, milestone) to the wiki roadmap.

**When to run:**
- After a founder L10 to push decisions into Linear in one go
- Mid-week when something ships, kicks off, or gets blocked
- Anytime the wiki dashboard would otherwise go stale

**Inputs:**
- A single quoted string passed as `--advance "..."`. Multi-clause is encouraged (separate clauses with commas, semicolons, or "and").
- If the string is missing, show usage + the most recent `--advance` example from this command's docs and exit.

### Step 13.1: Parse Intents

Extract one or more **intents** from the input string. Each intent is one of:

| Intent | Trigger phrases | Required fields |
|---|---|---|
| `ship_milestone` | "shipped X", "X is done", "completed X", "finished X", "X shipped" | milestone_match (title or partial) |
| `start_project` | "X kicked off", "starting X", "X in progress", "X is now in progress", "began X" | project_match |
| `start_milestone` | "started X", "working on X", "X in progress" (when X resolves to a milestone) | milestone_match |
| `validate_milestone` | "X is in validation", "validating X", "X is soaking", "verifying X", "X built but not shipped" | milestone_match |
| `validate_project` | "X is in validation" (when X is a project) | project_match |
| `block_project` | "blocked on Y", "X blocked", "X paused", "stuck on Y" (Y is the reason) | project_match (or last-mentioned project), reason |
| `add_milestone` | "add milestone X to Y", "new milestone X for Y" | project_match, milestone_title |
| `change_priority` | "make X urgent", "deprioritize X", "X is high priority", "X is low priority" | project_match (or issue_match), priority_value |
| `comment` | "note: ...", "outcome: ...", "log on X: ..." | target_match, comment_text |
| `rename_project` | "rename X to Y" | project_match, new_name |
| `change_lead` | "Y leading X", "X owned by Y", "assign X to Y" | project_match, lead_match |
| `complete_project` | "X is done" / "completed X" (when X is a project, not a milestone) | project_match |
| `cancel_project` | "kill X", "cancel X", "drop X" | project_match |
| `criterion_met` | "criterion met for X", "definition of done met for X", "X meets criteria" | project_match |
| `unclear` | anything else | raw_text |

**Resolving ambiguity at parse time:**
- "shipped X" — assume milestone first, fall back to issue/project if no milestone matches
- "X in progress" — check if X resolves to a project name (start_project) or a milestone (start_milestone); prefer project if both match
- Subjectless clauses ("blocked on Z") attach to the most recently mentioned project in the input. If none, mark as `unclear`.

**Resolution against Linear:**
- For each intent with a `*_match` field, run `list_projects(query: "[match]", limit: 5)` and `list_issues(query: "[match]", limit: 5)` (or `get_project(query, includeMilestones: true)` if context suggests a milestone).
- If 0 matches, mark intent as `unresolved` with the raw match text.
- If 1 match, attach the resolved Linear ID to the intent.
- If 2+ matches, mark as `ambiguous` with the candidate list — disambiguate during the propose step.

### Step 13.2: Propose the Checklist

Render all parsed intents as a numbered checklist. Group by status (resolved → ambiguous → unresolved → unclear). Format:

```
**Proposed updates from:** "[original input string]"

### Resolved ([N])
1. ✓ **Ship milestone** — "Bison test migration" in *Instantly → PE-Bison Migration*
   → Will mark milestone done. Add an outcome comment? (y/N)
2. ✓ **Start project** — *Deliverability Module*
   → Will move project state from Backlog to In Progress. Mirror to wiki? (Y/n — default Yes)
3. ✓ **Mark blocked** — *Deliverability Module*
   → Will add comment: "Blocked on Azhar's Supabase access". Project state stays In Progress.

### Ambiguous ([M])
4. ⚠ **Ship "campaign launch"** matched 2 milestones:
   - a) "Acme campaign launch" in *Campaign Execution Standardization*
   - b) "Riipen campaign launch" in *Client Lifecycle + Attribution*
   → Pick a, b, or skip.

### Unresolved ([P])
5. ✗ **Mark blocked: "Deliverability Module"** — couldn't find a project named "Deliverability Module".
   → Searched Linear, no match. Re-check the name?

### Unclear ([Q])
6. ❓ "the new dashboard idea" — couldn't extract a clear intent. Skip, or restate?

---

**Apply which?** Type one of:
- `yes` / `all` — apply all resolved (1, 2, 3)
- `no` / `cancel` — apply nothing
- `1,3` — apply listed
- `skip 2` — apply all resolved except 2
- `edit 4 [new instruction]` — re-parse line 4
- `4: a` — pick option a for ambiguous line 4
```

### Step 13.3: User Confirmation Loop

Wait for user input. Handle:
- `yes` / `all` — proceed to Apply (Step 13.4) with all `resolved` items
- `no` / `cancel` — abort, print "No changes applied."
- Comma list (`1,3,5`) — apply only listed lines
- `skip N` — apply all resolved except N
- `edit N [new text]` — re-run Step 13.1 just on the new text, replace line N with the result, re-render the checklist
- `N: a` — for an ambiguous line, set the resolved choice and move it to the resolved bucket
- Anything else — re-prompt with usage

Loop until the user gives a terminal answer (yes/no/specific list).

### Step 13.4: Apply

For each approved intent, run the matching MCP call. Track success/failure per intent. Apply intents in order; do not abort on a single failure — log and continue.

| Intent | MCP call(s) |
|---|---|
| `ship_milestone` | `save_milestone(id, ...)` to mark done. If outcome comment, also `save_comment(milestoneId or projectId, ...)`. |
| `start_project` | `save_project(id, state: "In Progress")`. |
| `start_milestone` | `save_milestone(id, ...)` to set in-progress equivalent (Linear milestones don't have native states — use a status note in description, or mark as `started: true` if available). |
| `validate_milestone` | No Linear-side state change (Linear milestones don't have an In Validation state). Wiki-only flag — update `roadmap.data.json` milestone.status to `"In Validation"`. Add a `save_comment(milestoneId, ...)` noting the validation gate so the change is visible in Linear. |
| `validate_project` | No Linear-side state change. Wiki-only flag — update `roadmap.data.json` workstream.status to `"In Validation"`. Add a `save_comment(projectId, ...)` noting the validation gate. |
| `block_project` | `save_comment(projectId, body: "Blocked: [reason]")`. State is unchanged unless explicit. |
| `add_milestone` | `save_milestone(projectId, name, description?, targetDate?)`. |
| `change_priority` | `save_project(id, priority: N)` or `save_issue(id, priority: N)`. |
| `comment` | `save_comment(targetId, body)`. |
| `rename_project` | `save_project(id, name: "[new name]")`. |
| `change_lead` | `save_project(id, lead: "[user name/id]")`. Resolve lead via `list_users(query)` if name-only. |
| `complete_project` | `save_project(id, state: "Completed")`. |
| `cancel_project` | `save_project(id, state: "Canceled")`. |
| `criterion_met` | No Linear-side change (criteriaMet is a wiki-only field). Update `roadmap.data.json` only — see Step 13.5. |

**For each applied intent:** capture the resulting URL, name, and old/new values for the report.

### Step 13.5: Mirror to Wiki Roadmap

After Linear changes are applied, walk the applied intents and update `kale-wiki/content/company/roadmap.data.json` for the three mirror cases:

1. **`rename_project`** — find the workstream in `roadmap.data.json` whose `name` matches the OLD project name (case-insensitive). Update its `name` to the new value.
2. **`start_project` / `complete_project` / `cancel_project`** — find the workstream by current name; update `status`:
   - `start_project` → `"In Progress"`
   - `complete_project` → `"Done"`
   - `cancel_project` → remove the workstream entry from the JSON (after a confirm prompt)
3. **`ship_milestone`** — find the workstream containing this Linear milestone; if a wiki milestone exists in `milestones[]` whose `name` fuzzy-matches the Linear milestone title (case-insensitive substring or Levenshtein < 30%), update its `status` to `"Shipped"`.
4. **`validate_milestone`** — same fuzzy-match as `ship_milestone`; update the wiki milestone's `status` to `"In Validation"`.
5. **`validate_project`** — find the workstream by current name; update its top-level `status` to `"In Validation"`.
6. **`criterion_met`** — find the workstream by name; set `criteriaMet: true` on it. If the workstream has no `completionCriteria` defined, surface a warning: "No completion criteria defined for [project] — criterion-met flagged but no criterion to meet. Define one before re-running."

**Implementation:**
- Read `kale-wiki/content/company/roadmap.data.json` (use `Read` tool — it's been read in this codebase before).
- Apply the JSON changes in memory.
- Write back via `Write` tool.
- If `kale-wiki/` is a git repo with the wiki branch flow, **don't auto-commit** — leave the file dirty and tell the user to commit/push when ready. The wiki has its own deployment cadence.

If no mirror cases apply (e.g., user only added a milestone or commented), skip this step entirely.

### Step 13.6: Report

Print a final summary:

```
**Advance complete — [X] applied, [Y] skipped, [Z] failed**

### Applied
✓ Shipped milestone "Bison test migration" — Instantly → PE-Bison Migration
   https://linear.app/.../milestone/...
✓ Started project Deliverability Module (Backlog → In Progress)
   https://linear.app/.../project/deliverability-module-cc746cb89686
✓ Comment added on Deliverability Module: "Blocked on Azhar's Supabase access"

### Skipped
- (line 4) "campaign launch" — ambiguous, not picked

### Failed
- (none)

### Wiki mirror
✓ kale-wiki/content/company/roadmap.data.json — Deliverability Module status flipped to In Progress
- Run `cd ../kale-wiki && git status` to review and commit when ready.
```

### Step 13.7: Error Handling

- **Empty input string:** Show usage + the latest `/roadmap --advance` example. Exit cleanly.
- **No resolved intents:** "Couldn't extract any actionable intents from that input. Try restating with explicit verbs (shipped, started, blocked, etc.)."
- **Linear API error during apply:** Mark that intent as Failed, log error in the report, continue with the next.
- **Wiki file missing or unreadable:** Report `kale-wiki/content/company/roadmap.data.json not found — wiki mirror skipped` and continue.
- **Ambiguous match with no user pick:** Skip that intent, log in the Skipped section.

---

## Step 14: My Queue (`--my-queue`)

Show one person's roadmap involvement, suitable for self-check ("what's on me?") or 1:1 prep ("what's on Azhar?").

### Step 14.1: Resolve the person

- If a name is supplied (`/roadmap --my-queue Azhar`), use it verbatim.
- If no name is supplied, default to the active user from `/prime`. If no active user is detected, prompt: "Whose queue? (e.g., Azhar)"
- Validate against the roster derived from `roadmap.data.json` (`designLead`, `buildLead`, `engineers[]` across all workstreams). If the name doesn't match, suggest the closest match by Levenshtein.

### Step 14.2: Read the data

Read `../kale-wiki/content/company/roadmap.data.json` directly. Apply the same derivation as `lib/roadmap-derive.ts → groupByPerson` (in conversation, replicate the logic — don't import the TS file).

For the resolved person, build:
- **In Progress:** workstreams where they're designLead/buildLead/in engineers AND status === "In Progress"
- **Coming Up:** same membership AND status === "Planned"
- **Recently Shipped:** same membership AND status === "Shipped" with a shipped milestone in the last 30 days
- **Layer graduations involving them:** any `nextStep`/`grewFrom` pair where the person appears on either side

### Step 14.3: Render

```
**[Person]'s queue** — as of [today]

### In Progress ([N])
- Strategy Engine — *Design* — next: [milestone] (date)
- Living Knowledge Ecosystem — *Engineer* — next: [milestone] (date)
- ...

### Coming Up ([N])
- ...

### Recently Shipped (last 30 days, [N])
- ...

### Layer graduations involving you ([N])
- L1 [name] → L2 [name]
- ...
```

If a section is empty, show "(none)" rather than omitting the section.

### Step 14.4: Error handling

- **Person not found in roster:** "[Name] doesn't appear on the roadmap as designLead, buildLead, or engineer. Closest match: [suggestion]?"
- **roadmap.data.json missing:** Report path and exit. The wiki repo must be present alongside this workspace.

---

## Step 15: Sync Now (`--sync-now`)

Pull current Linear state and push execution updates into `roadmap.data.json` in the kale-wiki repo. Designed for two cases:

1. **Manual trigger after a meeting** — you just flipped a bunch of statuses in Linear during L10 or a working session; this propagates them to the wiki without you editing JSON.
2. **Scheduled run** — fired by the same remote trigger that runs `/notion-sync`; keeps the wiki fresh between manual runs.

**Inputs (optional):**
- `--dry-run` — show the diff, don't write
- `--workstream [slug]` — sync only one workstream (default: all)
- `--no-commit` — write but don't commit/push (useful for chained ops)

### Step 15.1: Load roadmap.data.json

Read `../kale-wiki/content/company/roadmap.data.json`. Validate it exists. Build an in-memory map: `{workstream_slug → workstream object → [milestones]}`.

For each milestone, record:
- `linearMilestoneId` (L2/L3) or `linearIssueId` (L1) — required for sync; if missing, skip and add to the "unmapped" report
- Current `status`, `targetDate`, `owner`, `title`

### Step 15.2: Query Linear

Group milestones by Linear project (workstream URL → project ID). For each project, two calls:

- `get_project(id, includeMilestones: true)` — returns the project's status, lead, targetDate, AND its Project Milestones with `id`, `name`, `description`, `targetDate`, `progress`
- `list_issues(project: <id>, limit: 250)` — returns all issues in the project (needed for L1 milestones that are backed by issues, and for L2/L3 sprint milestones where status derives from issue state per the universal pattern)

Cache results per project; don't re-query.

### Step 15.3: Compute the diff

For each milestone in roadmap.data.json:

**If it has `linearMilestoneId` (L2/L3 — Linear Project Milestone):**
- `targetDate` ← Linear milestone `targetDate` (if different)
- `title` ← Linear milestone `name` (if different and Linear is newer)
- `status` derivation:
  - Linear `progress: "100%"` (or all child issues closed) → wiki `Shipped`
  - Any child issue closed AND others open → wiki `In Progress`
  - All issues open / no issues → leave wiki `status` alone (it's wiki-managed: Planned / In Validation / Backlog)

**If it has `linearIssueId` (L1 — backing issue):**
- `targetDate` ← issue `dueDate`
- `title` ← issue `title`
- `owner` ← issue assignee name (mapped to roster — Roshan / Mike / Arra / Azhar / Bev / Umer)
- `status` derivation:
  - Issue `state.type == "completed"` → wiki `Shipped`
  - Issue `state.type == "started"` → wiki `In Progress`
  - Issue `state.type == "canceled"` → leave wiki status alone (probably wants explicit handling; surface as a warning)
  - Otherwise → leave wiki `status` alone

**Never overwrite `In Validation`** — it's a wiki-side soak flag. If the wiki currently reads `In Validation`, only sync to `Shipped` (Linear says done) or leave it (Linear still open). Don't write `In Progress` over `In Validation`.

**Workstream-level fields** (in addition to milestone-level):
- `targetDate` ← Linear project `targetDate`
- `owner` ← Linear project `lead.name`
- `status` derivation (project-level):
  - Linear `status.type == "completed"` → wiki `Shipped`
  - Linear `status.type == "started"` → wiki `In Progress`
  - Linear `status.type == "canceled"` → wiki `Backlog` (or surface for review)
  - Otherwise → leave wiki status alone

### Step 15.4: Present the diff

Show a compact, readable diff grouped by workstream. For each changed field:

```
Living Knowledge Ecosystem
  → workstream targetDate: 2026-06-19 → 2026-06-26
  → milestone "Fireflies capture live"
      status: In Validation → Shipped (Linear: completed)
  → milestone "Git capture live"
      targetDate: 2026-05-29 → 2026-06-02 (Linear updated)

Execution Pipeline
  → milestone "N2 pipeline scales to higher data volume"
      status: In Progress → Shipped

Unmapped (5 milestones — won't sync until linkedIds are set):
  - kos-discovery-planning (Kale OS Foundation)
  - kb-cross-repo-routing (Living Knowledge Ecosystem)
  - …

Apply N updates to roadmap.data.json? (y/N)
```

If `--dry-run`, stop here.

### Step 15.5: Apply

On confirm:

1. Write changes to `../kale-wiki/content/company/roadmap.data.json` (preserve formatting — read full file, mutate the parsed object, write back with stable key order and 2-space indent).
2. Bump `allocation.updated` to today's date (the file already tracks this for the tier bar render).
3. If `--no-commit`, stop.
4. Otherwise: `cd ../kale-wiki && git add content/company/roadmap.data.json && git commit -m "chore(roadmap): linear → wiki sync ([N] updates)" && git push origin master`

Report:
```
Synced [N] updates across [M] workstreams. Pushed to kale-wiki master.
Cloudflare Pages redeploys in ~60 seconds.
[X] milestones unmapped — run /roadmap --backfill-linear-ids to close the gap.
```

### Step 15.6: Notes and edge cases

- **Idempotent** — running twice with no Linear changes produces no commit.
- **Cross-repo write** — same pattern as `--advance` mirror; if kale-wiki isn't a sibling repo, surface "kale-wiki not found at ../kale-wiki — clone it alongside this workspace."
- **In Validation preservation** — explicit. Treat it as a write-protected status from Linear's side.
- **No two-way sync** — this command only reads Linear and writes wiki. The wiki narrative fields (`why`, `summary`, `problems`, `completionCriteria`, `sprintItems`, `sprintNote`, `criteriaMet`) are never touched. Those stay manual via `--advance`.
- **`sprintNote` format** — `sprintNote` is an **array of short bullet strings** (rendered as a bulleted `<ul>` in the wiki), not a paragraph. When authoring or updating it (via `--advance` or sprint setup), write tight, scannable bullets — one per key point, each capturing the essence of the week's plan — never a prose block. A plain string still renders (as a `<p>`) for backwards-compat, but the array form is the convention; don't regress an existing array to a string.
- **Sprint-milestone status from issue state** — per the universal pattern, a sprint milestone's status derives from its backing issues. For L2/L3 milestones that are in `sprintItems[]`, also pull the project's open/closed issue counts via `list_issues(project, limit:250)` and apply the planned/in-progress/in-validation/shipped derivation. Non-sprint milestones use the simpler progress-based rule above.

---

## Step 16: Backfill Linear IDs (`--backfill-linear-ids`)

One-time (or top-up) helper that maps each roadmap milestone to its Linear backing item and writes `linearMilestoneId` (L2/L3) or `linearIssueId` (L1) into `roadmap.data.json`. Without this, `--sync-now` has nothing to sync.

**Inputs (optional):**
- `--workstream [slug]` — backfill one workstream only
- `--dry-run` — show proposed matches, don't write
- `--auto-accept` — accept high-confidence matches (>90%) without prompting

### Step 16.1: Identify gaps

Load roadmap.data.json. For each milestone, check whether it has a `linearMilestoneId` (L2/L3 workstream's tier) or `linearIssueId` (L1 workstream's tier). Skip milestones that already have one.

### Step 16.2: Query Linear per workstream

For each workstream with at least one unmapped milestone:

- L2/L3: `get_project(workstream.url, includeMilestones: true)` — returns Project Milestones
- L1: `list_issues(project: workstream.url, limit: 250)` — returns issues

### Step 16.3: Fuzzy match by name/title

For each unmapped roadmap milestone, score each Linear candidate using a fuzzy string-similarity (e.g., token-set ratio) against the candidate's name (Project Milestone) or title (Issue).

Buckets:
- **High confidence (≥90%)** — auto-accept if `--auto-accept`; otherwise list for one-click confirm
- **Medium (60–89%)** — prompt for confirm: "Match `[roadmap title]` → `[linear name]` (score: X%)? (y/n/skip/edit)"
- **Low (<60%)** — no match proposed; list as "no clear Linear backing — create one with `--add-milestone` or `--add`"

### Step 16.4: Present the matching plan

Grouped by workstream:

```
Living Knowledge Ecosystem (5 unmapped, L2)
  ✓ kb-cross-repo-routing → Linear milestone "Cross-repo learning routing" (98%)
  ✓ kb-search → Linear milestone "Basic search works — wiki + Claude" (94%)
  ? kb-team-adoption → Linear milestone "Team training rolled out" (72%)  [confirm]
  ✗ kb-promotion → no clear match; closest: "Intelligence layer" (54%)  [create or skip]
  …

Email Infrastructure Inventory (3 unmapped, L1 — issue-backed)
  ✓ eiv1-bulk-rotations → Linear issue "Implement bulk rotation execution" (91%)
  …

Apply N high-confidence matches automatically?
Resolve M medium-confidence (interactive)?
Skip P low-confidence?
```

### Step 16.5: Apply and write

For each accepted match, write `linearMilestoneId` or `linearIssueId` into the milestone object in `roadmap.data.json`. Commit and push to kale-wiki master:

```
chore(roadmap): backfill linear backing IDs ([N] milestones)
```

Report unmapped milestones at the end as a punch list: titles that need new Linear items created (point to `--add-milestone` / `--add`).

### Step 16.6: Notes

- **Run order matters** — backfill before sync. Sync silently skips anything unmapped.
- **Re-run safe** — only touches milestones missing the ID field. Safe to re-run after adding new milestones.
- **Match by structure, not just name** — for L2/L3, scope candidates to the workstream's Linear project (don't match across projects). For L1, same.

---

## Error Handling

- **No Linear issues found:** Show empty queue message, suggest creating projects with `--create-project` and issues with `--add`
- **No Notion requests found (on --triage):** "No pending requests. Queue is clear."
- **No active projects (on --add):** Suggest `--create-project` first
- **Linear API errors:** Report clearly, suggest checking MCP connection via `/mcp`
- **Notion API errors:** Report clearly, suggest checking MCP connection
- **Ambiguous issue title match:** Present top matches and ask user to pick
- **Missing labels on issues:** If an issue has no Layer label, show it as "Unclassified" — don't hide it
