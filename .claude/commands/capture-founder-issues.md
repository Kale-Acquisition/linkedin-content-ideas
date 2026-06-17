# /capture-founder-issues

> Scan a recent Mike↔Roshan call for L10 IDS-worthy issues, confirm with the user, and write them to the **Founder Issues** Notion DB.

**Usage:** `/capture-founder-issues [meeting]`

`[meeting]` is optional. Accepts a Fireflies meeting URL, a meeting title fragment, or `latest` (default). When omitted, picks the most recent Mike↔Roshan call.

**Examples:**
- `/capture-founder-issues` — pull most recent founder call, propose issues
- `/capture-founder-issues latest` — same as above
- `/capture-founder-issues "L10 May 19"` — search by title fragment
- `/capture-founder-issues https://app.fireflies.ai/view/...` — specific meeting

---

## Constants

- **Founder Issues DB URL:** `https://www.notion.so/af83e21008f141edb4d888f9038eadfa`
- **Founder Issues data source ID:** `6dc94b7c-0324-48ed-bc6f-9dcf9ecf2626`
- **Founder emails (for participant filter):**
  - Roshan: `roshan@kaleacquisition.com`
  - Mike: `mike@usekale.com`

If either email no longer resolves to a Fireflies account, fall back to filtering by name string match in the transcript speakers.

---

## Step 1: Resolve the meeting

Three cases:

1. **URL passed** — extract the transcript ID from the Fireflies URL, call `fireflies_get_transcript`.
2. **Title fragment passed** — call `fireflies_get_transcripts` with `keyword=<fragment>`, `scope=title`, `limit=5`. If multiple match, ask the user to pick. If none, fall back to case 3.
3. **No arg or `latest`** — call `fireflies_get_transcripts` with `participants=[roshan_email, mike_email]`, `limit=5`. Take the most recent. If none in the last 14 days, ask: "No recent Mike↔Roshan calls found — should I search wider, or do you want to paste a meeting URL?"

Confirm the chosen meeting before scanning: "Scanning **[title]** from [date]. Continue? (y/n)"

---

## Step 2: Pull the transcript

Call `fireflies_get_transcript` with the resolved transcript ID. You get sentences (with speaker labels) and metadata.

---

## Step 3: Auto-detect IDS-worthy items

Scan the transcript for founder-level issues. **Do not require trigger phrases** — detect on your own using these heuristics:

**Surface as candidates:**
- Recurring tensions either founder voiced
- Unresolved decisions that surfaced but didn't close
- Strategic, people, process, tech, client, or finance friction that's founder-scoped
- Anything one of them explicitly punted ("we'll come back to this", "table it", "park this", "let's IDS this")
- Explicit markers like "founder issue:" or "IDS this:" — bonus signal, not required

**Filter OUT:**
- Tactical execution items (those belong in Linear / the Intake DB)
- Status updates and information sharing with no tension or unresolved choice
- Anything that's already an open milestone or in-progress Linear issue (cross-check the roadmap if helpful — keep light, don't block on it)
- Decisions that fully closed during the call (no follow-up needed)

For each candidate, capture:
- **Suggested title** — lean, names the issue, not the solution. Max 80 chars.
- **Source quote(s)** — one or two short sentences from the transcript that sourced this
- **Why it's IDS-worthy** — one line of Claude's reasoning
- **Who raised it** — Mike or Roshan, inferred from speaker labels (whoever first voiced the tension)

---

## Step 4: Confirm with the user

Present the candidates as a numbered list. For each:

```
[1] [Suggested Title]
    Raised by: Mike
    Quote: "…short quote that surfaced this…"
    Why: [one-line reasoning]
    [a]ccept  [e]dit  [s]kip
```

The user goes through them one by one or with batched input (e.g., `1a 2s 3e`). For `edit`, ask which fields to change (title and/or description).

If the user wants to add an issue Claude missed, allow: `+ [new title]` followed by a prompt for the source context.

---

## Step 5: Write to Notion

For each accepted item, call `notion-create-pages` with:

- **Parent:** `data_source_id = 6dc94b7c-0324-48ed-bc6f-9dcf9ecf2626`
- **Properties:**
  - `Title` — accepted title
  - `Description` — the source quote + light context (1-3 sentences max, no solution)
  - `Raised By` — the founder's Notion person ID (resolve via `notion-get-users` if not cached; cache the two user IDs after first lookup)
  - `Status` — `New`
- **Content:** optional — paste the relevant transcript excerpt as a blockquote, with the meeting title and date as a link to the Fireflies URL underneath.

---

## Step 6: Report

```
Captured N founder issues from "[Meeting Title]" ([date]):

  - [Title 1] (raised by Mike)
  - [Title 2] (raised by Roshan)
  - …

View in Notion: https://www.notion.so/af83e21008f141edb4d888f9038eadfa
```

If the user skipped everything, just say: "No issues captured — closed out."

---

## Notes

- **Permission scoping** — Founder Issues DB is restricted to Roshan and Mike in the Notion UI. The MCP server's integration must be granted access to the DB once; if `notion-create-pages` returns an access error, surface it with: "Founder Issues DB isn't shared with the integration yet — grant access in Notion (Share → Connect → claude.ai Notion integration), then re-run."
- **No trigger-phrase contract** — Claude detects on its own. Phrases like "founder issue:" or "IDS this:" are just additional signals; never tell the user they're required.
- **Long-term path** — when `kb-fireflies-capture` lands, fold this into the same routing pipeline (Mike↔Roshan calls auto-trigger this scan; the confirmation step stays manual).
