# /capture-learning

> Capture a learning from daily work into Notion for team review. Lightweight — designed for quick knowledge capture, not polished resources.

**Usage:** `/capture-learning [topic]`

**Examples:**
- `/capture-learning deliverability-testing` — capture a deliverability insight
- `/capture-learning client-acme-campaign` — capture a client-specific learning
- `/capture-learning inbox-warmup-timing` — capture an operational finding

**Flags:**
- `--category [cat]` — pre-set category (deliverability, operations, client, sales, tooling, process)
- `--source [src]` — where this learning came from (meeting name, project, Slack thread)
- `--wiki-candidate` — flag as a candidate for wiki publication

---

## Step 1: Gather Learning Details

If `$ARGUMENTS` is provided, use it as the topic. Otherwise ask: "What did you learn? (brief topic)"

Ask the user for a description if not obvious from context:
- "Describe the learning in 2-3 sentences — what did you discover and why does it matter?"

If `--category` is not provided, infer the category from the topic and confirm:
- **deliverability** — inbox placement, warmup, DNS, sender reputation
- **operations** — process improvements, workflow, scaling
- **client** — per-client insights, what worked/didn't
- **sales** — outreach patterns, objection handling, ICP
- **tooling** — tool discoveries, integration learnings
- **process** — SOP refinements, new procedures

If `--source` contains a Slack URL (e.g., `https://kaleacquisition.slack.com/archives/C.../p...`):
1. Extract the channel ID and message timestamp from the URL
2. Use the Slack MCP (`slack_read_thread`) to fetch the thread context
3. Pre-fill the learning description from the thread content
4. Set the source attribution to `Slack: #channel-name YYYY-MM-DD`

If `--source` is not provided, infer from the current session context (which project repo, recent meeting, etc.) or ask.

---

## Step 2: Check for Existing Learnings DB

Check `automations/learnings.md` for a stored Notion database ID.

**If first run (no DB ID):**

Create the database via `notion-create-database`:

```
Title: "Learnings"
Properties:
  - "Learning" (title)
  - "Description" (rich_text)
  - "Category" (select: Deliverability, Operations, Client, Sales, Tooling, Process)
  - "Source" (rich_text) — where this came from (meeting, project, conversation)
  - "Source Project" (select: kale-wiki, kale-os, kale-workspace, other)
  - "Captured By" (rich_text) — who captured it
  - "Date" (date)
  - "Status" (select: Raw, Reviewed, Wiki Candidate, Published, Archived)
  - "Tags" (multi_select)
  - "Wiki Page" (rich_text) — if published, which wiki page it became
  - "Related Ideas" (rich_text) — link to automation ideas if relevant
```

Store the database ID and URL in `automations/learnings.md`.

**If subsequent run:**

Read the DB ID from `automations/learnings.md`.

---

## Step 3: Create Learning in Notion

Use `notion-create-pages` to create a page in the Learnings database:

- **Learning:** [topic title — clean, descriptive]
- **Description:** [user's description, expanded with any context from the current session]
- **Category:** [inferred or provided category]
- **Source:** [meeting name, project, conversation, etc.]
- **Source Project:** [current repo name, e.g., "kale-wiki"]
- **Captured By:** [active user from KALE_USER or session context]
- **Date:** today
- **Status:** "Wiki Candidate" if `--wiki-candidate`, otherwise "Raw"
- **Tags:** [auto-generated from topic — e.g., "warmup", "DNS" for a deliverability topic]

---

## Step 4: Update Local Cache

Append to `automations/learnings.md`:

```markdown
### [Topic Title]
**Category:** [cat] | **Source:** [src] | **Date:** [today] | **Status:** [status]
[Description — 1-2 sentences]
```

Keep the cache file sorted by date (newest first) with metadata header:

```markdown
# Learnings

> Cached summary of the [Learnings](NOTION_URL) Notion database.
> Updated by `/capture-learning`. Notion is the source of truth.

**Notion database ID:** UUID
**Notion database URL:** URL
**Total learnings:** N
**Wiki candidates:** M

---

## Recent Learnings

[entries...]
```

---

## Step 5: Confirm

Report to the user:

```
Learning captured: "[Topic Title]"
Category: [cat] | Source: [src] | Status: [status]
Notion: [page URL]

Team can review and curate in Notion.
To promote to a wiki page later: flag as "Wiki Candidate" in Notion, then run /create-resource.
```

If `--wiki-candidate` was set, add: "Flagged as wiki candidate — will surface in next `/check-freshness --gaps` scan."

---

## Error Handling

- **Notion API failure:** Save the learning locally to `automations/learnings.md` only. Report: "Couldn't reach Notion — learning saved locally. Will sync on next run."
- **Duplicate detection:** Before creating, search the Learnings DB for similar titles. If a close match exists, ask: "Similar learning exists: '[title]'. Update that one or create new?"
