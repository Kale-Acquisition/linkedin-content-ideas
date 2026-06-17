# /rocks

> Manage quarterly rocks — strategic initiatives that guide automation priorities and team focus.

**Usage:** `/rocks [flags]`

**Flags:**
- (no flag) — Show current quarter's rocks with status, progress, and linked ideas
- `--set` — Interactive: create a new rock in Notion
- `--review` — Quarterly review: outcomes, linked ideas completed, carryovers
- `--link [idea-title] [rock-title]` — Link an automation idea to a rock

**Examples:**
- `/rocks` — view current quarter's rocks and linked ideas
- `/rocks --set` — create a new rock interactively
- `/rocks --review` — end-of-quarter review
- `/rocks --link "Deliverability monitoring dashboard" "Hit 90% inbox placement"`

**Design principle:** Rocks are created and managed in Notion directly via the Monthly Initiatives database. This command reads from Notion and provides views/summaries. It does NOT try to be the primary creation interface — `--set` is a convenience shortcut.

---

## Step 1: Parse Arguments

Parse `$ARGUMENTS` for flags:

| Flag | Default | Notes |
|---|---|---|
| `--set` | false | Create a new rock in Notion interactively |
| `--review` | false | Quarterly review mode |
| `--link [idea] [rock]` | — | Link an automation idea to a rock |

If `--set` is provided, skip to Step 4 (Create Rock).
If `--review` is provided, skip to Step 5 (Quarterly Review).
If `--link` is provided, skip to Step 6 (Link Idea to Rock).
Otherwise, proceed to Step 2 (Load Rocks).

---

## Step 2: Load Context

Read these files:

1. `automations/ideas.md` — extract Rocks DB ID (stored in metadata header) and Automation Ideas DB ID
2. `context/strategy.md` — current priorities for context

**The Rocks/Initiatives database is the Monthly Initiatives database in Notion:**
- **Database ID:** `60f6df9de6fe40aa806a40595e6ac348`
- **Data source ID:** `8c616471-d3ed-431c-8861-32be406ccdab`
- **Location:** Vision & Strategy page

This database serves dual purpose: it holds both monthly project initiatives (with Owner, Contributors, Category, Department, etc.) and quarterly rocks (using the Quarter, Status, Success Criteria, and Progress Notes fields). Rocks are initiatives tagged with a Quarter and Status.

**To load rocks:** Query the Monthly Initiatives data source, filtering by Quarter = current quarter (e.g., "Q1 2026") and Status = "Active".

---

## Step 3: Show Current Rocks (Default View)

For each active rock in the current quarter:

1. Fetch the rock's properties from Notion
2. Query the Automation Ideas DB for ideas where the `Rock` relation points to this rock
3. Count ideas by status (Built, In Progress, Queued, New)

Present as:

```
## [Quarter] Rocks

### 1. [Rock Title]
**Owner:** [Owner] | **Status:** [Status] | **Category:** [Category]
**Success criteria:** [criteria text]
**Linked ideas:** [N] ([X] Built, [Y] In Progress, [Z] Queued, [W] New)
  - [Idea Title] — [Status] | Priority: [p]
  - [Idea Title] — [Status] | Priority: [p]
  - ...
**Progress:** [Progress Notes or "No notes yet"]

### 2. [Rock Title]
...

### Unlinked High-Priority Ideas
_(Ideas with composite score >= 3.5 not linked to any rock — consider linking)_
- **[Idea]** — Score: [score] | [Category]
- ...
```

---

## Step 4: Create Rock (`--set`)

Interactive rock creation:

1. Ask: "What's the rock? (one sentence — what you're committing to this quarter)"
2. Ask: "Who owns it? (Roshan / Mike / Shared)" — note: this sets the Category or adds a note; Owner in Monthly Initiatives is a person field
3. Ask: "What quarter? (default: current quarter)"
4. Ask: "What category?" (default: infer from context — Deliverability, Systems & Automation, etc.)
5. Ask: "Success criteria? (how will you know it's achieved?)"

Create the rock in Notion via `notion-create-pages` in the Monthly Initiatives database with:
- Project Name: [title]
- Quarter: [selected]
- Status: Active
- Category: [selected]
- Success Criteria: [text]
- Start Date: today

Confirm creation and show the rock.

---

## Step 5: Quarterly Review (`--review`)

1. Query all initiatives for the current quarter (or most recently completed quarter)
2. For each rock, fetch linked ideas and their statuses
3. Present:

```
## Quarterly Review — [Quarter]

### [Rock Title]
**Owner:** [Owner] | **Status:** [Achieved/Active/Carried Over/Dropped]
**Category:** [Category]
**Success criteria:** [criteria]
**Outcome:** [Progress Notes — or prompt user to summarize]

**Linked ideas:**
- [Idea] — Built ✓ (completed [date])
- [Idea] — In Progress (started [date])
- [Idea] — Queued (not started)

**Verdict:** [Achieved / Carry over to next quarter / Drop]
```

4. For each rock, ask the user: "Mark as Achieved, Carry Over, or Drop?"
5. Update the rock's Status in Notion accordingly
6. If Carried Over, ask: "Create the same rock for next quarter?" and if yes, create it via Step 4 logic

---

## Step 6: Link Idea to Rock (`--link`)

1. Parse the idea title and rock title from arguments
2. Fuzzy-match the idea title against the Automation Ideas DB
   - If no match, list the top 5 ideas and ask the user to pick
3. Fuzzy-match the rock title against the Monthly Initiatives DB (filter to Active status)
   - If no match, list all active rocks and ask the user to pick
4. Update the idea's `Rock` relation property to point to the matched initiative
5. Confirm: "Linked **[Idea]** → **[Rock]**"

---

## Error Handling

- **No Monthly Initiatives DB:** This should not happen — the DB already exists at `60f6df9de6fe40aa806a40595e6ac348`. If the ID is wrong, report the error and suggest verifying the Notion URL.
- **No rocks for current quarter:** Suggest running `--set` to create some, or tagging existing Monthly Initiatives with the current Quarter
- **Notion API errors:** Report clearly and suggest checking MCP connection
- **No linked ideas for a rock:** Show "No ideas linked yet — run `/rocks --link [idea] [rock]` to connect ideas"
