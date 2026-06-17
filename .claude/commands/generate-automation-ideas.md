# /generate-automation-ideas

> Scan Fireflies transcripts and Notion notes for automation opportunities. Extract, deduplicate, score, and write team-visible entries to the **Intake DB** (Type=Idea). Rich metadata (composite score, confidence, trend, sources, etc.) lives in the local cache `automations/ideas.md` and the wiki — Notion is the visibility surface only.

**Architecture (post-2026-05-07 unification):** The standalone Automation Ideas DB has been replaced by the unified **Intake DB** (`e362fa70b5764e6fa9a2451c9642daf7`, data source `65be880e-48e8-40cb-9f4a-b3e965cdfbd9`). All ideas this command discovers are written there with `Type = Idea`. The lean Intake schema only carries Title, Type, Submitter, Status, Linked Linear, Description, Submitted — so all the analytical fields (Composite Score, Pain Frequency, Trend, etc.) are managed in `automations/ideas.md` and rendered to the wiki page.

**Usage:** `/generate-automation-ideas [flags]`

**Flags:**
- `--days N` (default: 14) — Fireflies lookback window
- `--days all` or `--first-run` — full historical scan (warns about API call volume)
- `--sources fireflies,notion` (default: both) — which sources to scan
- `--rerank-only` — skip scanning, re-score all ideas against current strategy
- `--pick [idea-title]` — move an idea to In Progress and optionally kick off `/create-plan`
- `--queue [idea-title]` — move an idea to Queued status
- `--dismiss [idea-title] [reason]` — dismiss an idea with a reason
- `--complete [idea-title]` — mark an idea as Built with outcome notes
- `--stale` — surface stuck/forgotten ideas for review
- `--team-report` — summary grouped by rock first, then by assignee
- `--digest` — weekly digest formatted for Slack/email (includes rocks summary)

**Examples:**
- `/generate-automation-ideas` — scan last 14 days, both sources
- `/generate-automation-ideas --first-run` — full historical scan (first time setup)
- `/generate-automation-ideas --days 30 --sources fireflies` — Fireflies only, 30-day window
- `/generate-automation-ideas --rerank-only` — re-prioritize without scanning
- `/generate-automation-ideas --pick "Inbox warmup monitor"` — start working on an idea
- `/generate-automation-ideas --queue "Data cleaning automation"` — queue for later
- `/generate-automation-ideas --dismiss "Slack to Linear" "Low volume, not worth automating yet"` — dismiss with reason
- `/generate-automation-ideas --complete "Domain purchase automation"` — mark as built
- `/generate-automation-ideas --stale` — review stuck or forgotten ideas

---

## Step 1: Parse Arguments

Parse `$ARGUMENTS` for flags:

| Flag | Default | Notes |
|---|---|---|
| `--days N` | 14 | Number of days to look back in Fireflies. Use `all` for full history. |
| `--first-run` | false | Alias for `--days all`. Creates Notion DB if it doesn't exist. |
| `--sources` | `fireflies,notion` | Comma-separated. Valid: `fireflies`, `notion`. |
| `--rerank-only` | false | Skip scanning, jump to scoring (Step 7). |
| `--pick [title]` | — | Move idea to In Progress, assign to user. |
| `--queue [title]` | — | Move idea to Queued status. |
| `--dismiss [title] [reason]` | — | Dismiss idea with a reason. |
| `--complete [title]` | — | Mark idea as Built, record outcome. |
| `--stale` | false | Surface stuck/forgotten ideas for review. |
| `--team-report` | false | Group summary by rock, then by assignee. |
| `--digest` | false | Weekly digest format with rocks summary. |

If `--pick`, `--queue`, `--dismiss`, or `--complete` is provided, skip to Step 10 (Action Pipeline).
If `--stale` is provided, skip to Step 10.5 (Stale Review).
If `--rerank-only` is provided, skip to Step 7 (Score + Prioritize).

---

## Step 2: Load Context

Read these files for scoring and analysis context:

1. `context/strategy.md` — current priorities (used for Strategic Alignment scoring)
2. `context/current-data.md` — live metrics and workspace data
3. `context/business-info.md` — company context and domain knowledge
4. `automations/ideas.md` — local cache: last scan date, existing ideas with rich metadata

Extract from `automations/ideas.md`:
- **Last scan date** — determines incremental scan window
- **Existing ideas** — full record (title, description, scores, mentions, sources, Notion page URL) for dedup + trend analysis

The Intake DB ID is fixed and doesn't need to be looked up: `e362fa70b5764e6fa9a2451c9642daf7` (data source `65be880e-48e8-40cb-9f4a-b3e965cdfbd9`).

---

## Step 3: Load Existing Ideas

**Local cache is the source of truth for analytical state.** `automations/ideas.md` carries scores, mention counts, trends, sources — everything needed for ranking and trend computation.

**Notion is the visibility surface.** Each idea in the cache has a corresponding lean entry in the Intake DB (Type=Idea). The Notion page URL is stored alongside the idea in the cache so updates can target it.

On every run:
1. Read `automations/ideas.md` and parse the existing idea list (title, description, scores, mention count, sources, Notion page URL, Status).
2. The Rocks/Initiatives database is the **Monthly Initiatives** database (`60f6df9de6fe40aa806a40595e6ac348`, data source `8c616471-d3ed-431c-8861-32be406ccdab`). Used for rock-aware Strategic Alignment scoring; the relation isn't stored in Intake (Intake doesn't carry it), but rock linkage is stored in the local cache.

If `automations/ideas.md` is missing or empty, treat as first run — no existing ideas, scan everything, build the cache from scratch.

---

## Step 4: Scan Fireflies

> Skip if `--sources` doesn't include `fireflies`.

### First Run Strategy (~115 API calls — warn user before proceeding)

Tell the user: "First-run Fireflies scan will make ~115 API calls across all org meetings. This takes a few minutes. Proceed?"

1. **Paginate ALL transcripts:** Call `fireflies_get_transcripts(limit: 50, skip: 0)`, then `skip: 50`, `skip: 100`, etc. until no more results.
2. **Deduplicate:** Group by `meetingLink + dateString` (Fireflies creates ~2x records per meeting). Keep the record with the richest summary data.
3. **Filter:** Discard meetings with no summary data (older/unprocessed recordings).
4. **Get summaries:** Call `fireflies_get_summary(id)` for each unique meeting. Process in batches.
5. **Analyze for automation signals:** For each summary, Claude looks for:
   - Explicit: "we should automate...", "build a script for...", "if we had a tool..."
   - Pain signals: "this takes too long...", "manual process...", "every time we..."
   - Frequency signals: "repetitive...", "bottleneck...", "keep having to..."
   - Action items tagged to building/automating something
   - Discussions about workflow inefficiencies or tool gaps
6. **Deep dive top signals:** For the ~10 meetings with the strongest automation signals, call `fireflies_fetch(id)` for full transcript context to extract richer detail and quotes.
7. **Output:** A list of candidate ideas, each with:
   - Idea title (concise, action-oriented)
   - Description (what would be automated and why)
   - Source attribution (meeting title, date, speaker if available)
   - Evidence quotes (direct quotes from the transcript)
   - Estimated category

**IMPORTANT:** Do NOT use `mine: true` — scan all org meetings. Roshan has admin access to all org transcripts.

### Subsequent Run Strategy (~14 API calls)

1. Calculate `fromDate`: use last scan date from `automations/ideas.md`, or `--days` ago.
2. Call `fireflies_get_transcripts(limit: 50, fromDate: [date])`. Paginate if needed.
3. Same dedup → filter → summarize → analyze flow on the smaller set.

---

## Step 5: Scan Notion

> Skip if `--sources` doesn't include `notion`.

### Tier 1: Keyword Searches (Recency-Gated)

Run `notion-search` for each of these terms, adding a `created_date_range` filter with `start_date` set to 60 days ago (calculated from today):
- "automation ideas"
- "manual process"
- "automate"
- "workflow improvement"
- "bottleneck"
- "should build"
- "time-consuming"
- "repetitive"

Limit to 5 results per keyword. Deduplicate pages across keyword results.

**Post-filter:** For each result page, check its `last_edited_time`. If the page hasn't been edited since the last scan date (from `automations/ideas.md`), skip it and log: "Skipped [page title] — unchanged since last scan". Only fetch and extract from pages that have been modified since the last scan.

### Tier 2: Curated Always-Scan Pages (No Date Filter)

Read the active user's `notion_curated_pages` from `config/profiles.json` using the `KALE_USER` env var. If `KALE_USER` is not set, ask the user interactively: "Who is running this? (roshan/mike)" and use their profile.

Fetch each curated page via `notion-fetch` regardless of age. For example, if `KALE_USER=roshan`, the pages would be:
- **Roshan's Rolling Thoughts** — personal notes, often contains automation ideas
- **Collab page** — has AI Call Workflow Automation spec and other joint ideas
- **Monthly Initiatives** — filter to "Systems & Automation" category items

For each curated page, compare `last_edited_time` from the fetch response against the last scan date. If unchanged since last scan, skip detailed extraction — just confirm existing ideas from this source remain valid and log: "Curated page [title] unchanged — existing ideas confirmed".

### Extraction

For pages that passed freshness filtering (modified since last scan), call `notion-fetch` and analyze content for:
- Explicit automation ideas or feature requests
- Described manual processes that could be automated
- Tool/system wishlists
- Workflow improvement notes

**Output:** Candidate ideas with page title, URL, and relevant excerpts as evidence.

---

## Step 6: Merge (Semantic Deduplication)

For each candidate idea extracted from scanning, match against the existing ideas in the local cache (`automations/ideas.md`).

### Match Against Existing Ideas

1. **Title check** — exact or substring match against existing cached idea titles → MATCH
2. **Semantic check** — Claude compares descriptions: "Do these describe the same manual process or propose the same solution?" → MATCH if yes
3. **Category + context tiebreaker** — same category AND same system/tool AND same user role → MATCH

### If MATCH (existing idea found):
- Append new source to the cached `sources` list
- Update `last_mentioned` to today
- Increment `mention_count`
- Append new evidence quotes to cached `evidence`
- If the new mention adds detail, enrich the cached `description`

### If NEW (no match):
- Add to cache with:
  - `status`: New
  - `mention_count`: 1
  - `first_identified`: today
  - `last_mentioned`: today
  - `sources`: the source attribution
  - `evidence`: relevant quotes
  - `notion_page_url`: null (will be populated in Step 9 after creating the Intake entry)

### Candidate-to-Candidate Dedup
If two candidates from the same scan match each other but not an existing idea, merge them into one new idea with both sources.

---

## Step 7: Score + Prioritize

> This step runs for all ideas (new + existing) on every scan, and is the only step when `--rerank-only` is used.
> Step 7 now includes trend computation (formerly Step 8) — trends are derived from score deltas, not mention counts.

### Pre-scoring: Load Rocks

Query the Monthly Initiatives DB (Rocks DB ID from `automations/ideas.md`, data source `8c616471-d3ed-431c-8861-32be406ccdab`) for all initiatives with Quarter = current quarter and Status = "Active". These are used for rock-aware Strategic Alignment scoring below.

### Pre-scoring: Save Previous Scores

For each idea, save the current `Composite Score` → `Previous Score` before rescoring. If `Previous Score` is empty (first run after upgrade), it will be set to the new Composite Score after scoring (no trend change).

### Pre-scoring: Time Decay

For each idea where `Last Mentioned` is 30+ days ago: reduce Pain Frequency by 1 (floor of 1). This prevents stale single-mention ideas from lingering at PF=2.

### Scoring Formula (4 Dimensions)

Read `context/strategy.md` fresh for current priorities.

| Dimension | Weight | Score 1-5 | Criteria |
|---|---|---|---|
| Strategic Alignment | 40% | 5 = linked to active rock OR P1 deliverability | 4 = P2 automation | 3 = P3 growth | 2 = indirect support | 1 = tangential |
| Pain Frequency | 25% | 5 = 5+ mentions across 3+ sources | 4 = 3-4 mentions | 3 = 2 mentions | 2 = 1 strong signal | 1 = 1 weak signal |
| Time Savings | 20% | 5 = 10+ hrs/wk | 4 = 5-10 | 3 = 2-5 | 2 = 1-2 | 1 = <1 |
| Feasibility | 15% | 5 = <1 day, existing tools | 4 = 1-3 days | 3 = ~1 week | 2 = new infra needed | 1 = major project |

**Rock-aware SA scoring:** If an idea has a `Rock` relation pointing to an Active rock, it gets SA=5 automatically — it's been explicitly committed to. If not linked but thematically aligns with a rock, SA scoring proceeds as before using strategy.md.

### Composite Score

**Composite** = (SA × 0.40) + (PF × 0.25) + (TS × 0.20) + (F × 0.15)

Priority mapping:
- **High:** >= 3.5
- **Medium:** >= 2.5
- **Low:** < 2.5

### Post-scoring: Recency Boost

If an idea was mentioned in the current scan (new evidence added in Step 6), add +0.5 to composite (cap at 5.0). Explicit and easy to reason about.

### Post-scoring: Confidence Indicator

Based on evidence quantity — metadata only, does NOT affect composite:

| Level | Criteria |
|-------|----------|
| High | 4+ mentions across 2+ source types (Fireflies + Notion) |
| Medium | 2-3 mentions OR multiple source types |
| Low | Single mention from single source |

Set the `Confidence` select field accordingly.

### Post-scoring: Compute Trends (from score delta)

Compare new Composite Score against Previous Score:
- **Rising:** composite increased by 0.3+
- **Stable:** within ±0.3
- **Declining:** composite decreased by 0.3+

If Previous Score was empty (first run after upgrade), set Previous Score = new Composite Score and leave Trend unchanged.

Set the `Trend` select field accordingly.

### Apply Scores

For each idea:
1. Calculate dimension scores based on evidence, mention count, description, strategy alignment, and rock linkage
2. Apply time decay to PF if applicable
3. Compute composite score
4. Apply recency boost if applicable
5. Compute confidence indicator
6. Compute trend from score delta
7. Store all scoring data in the local cache (`automations/ideas.md`) — Intake doesn't carry analytical fields:
   - `priority` (High/Medium/Low)
   - `strategic_alignment` (SA score, 1-5)
   - `pain_frequency` (PF score, 1-5)
   - `time_savings_score` (TS score, 1-5)
   - `feasibility_score` (F score, 1-5)
   - `feasibility` (Easy/Medium/Hard) — 5-4=Easy, 3=Medium, 2-1=Hard
   - `time_savings` (e.g., "~5 hrs/wk on manual inbox checks")
   - `composite_score`
   - `previous_score`
   - `confidence` (High/Medium/Low)
   - `trend` (Rising/Stable/Declining)
   - `rock_link` (linked rock title, if any)

---

## Step 9: Write to Intake (Notion) + Regenerate Cache

### Write to Intake DB (lean schema)

The Intake DB only carries Title, Type, Submitter, Status, Linked Linear, Description, Submitted. The Description field carries everything humans need to see in Notion — a 2-3 sentence idea summary plus a one-line "score & sources" footer.

- **New ideas:** Batch create via `notion-create-pages` against the Intake data source (`65be880e-48e8-40cb-9f4a-b3e965cdfbd9`). For each idea:
  - `Title`: idea title
  - `Type`: "Idea"
  - `Submitter`: leave blank (the bot doesn't have a Notion user ID; Roshan can set himself if he wants attribution)
  - `Status`: "New" (or "Accepted" for High-priority, score >= 3.5 — surfaces a clear queue signal in Notion)
  - `Description`: the idea description + a footer line with score, confidence, and sources, e.g.:
    > Automate the deliverability monitoring dashboard so we get alerted when inbox placement drops, rather than finding out three days later from a client.
    >
    > _Score: 3.85 (High) · Confidence: High · Sources: Fireflies "L10 2/15", Notion "Rolling Thoughts" · Generated by /generate-automation-ideas on 2026-05-07_
  - `Linked Linear`: leave blank (only set if/when promoted to a Linear issue)
  - Capture the returned Notion page URL and store it in the local cache as `notion_page_url`.

- **Updated ideas:** Call `notion-update-page` for the existing Notion page URL. Only update fields that changed:
  - `Status`: only if it changed (e.g., New → Accepted on score increase, or via action pipeline)
  - `Description`: re-render with updated score / sources / mention footer
  - Don't touch `Title` (titles stay stable; if an idea's name changes, it's effectively a new idea)

### Regenerate Local Cache

Overwrite `automations/ideas.md` with a fresh summary. Format:

```markdown
# Automation Ideas

> Cached summary of the [Automation Ideas](NOTION_URL) Notion database.
> Updated by `/generate-automation-ideas`. Notion is the source of truth.

**Notion database ID:** UUID
**Notion database URL:** URL
**Rocks database ID:** UUID (Monthly Initiatives DB)
**Rocks data source ID:** UUID
**Last scan:** YYYY-MM-DD
**Last scan sources:** Fireflies (N days, M meetings), Notion (P pages)
**First full scan:** YYYY-MM-DD
**Total active ideas:** N (H High / M Medium / L Low)

---

## High Priority

### 1. [Idea Title]
**Status:** New | **Category:** Deliverability | **Mentions:** 5 | **Trend:** Rising
**Score:** 3.8 (prev: 3.3) | **Confidence:** High | **ROI:** 2.5
**Rock:** [Rock Title] _(or "Unlinked")_
**First seen:** 2026-02-15 | **Last mentioned:** 2026-03-01
**Sources:** Fireflies: "L10 2/15", "Client Review 2/20"; Notion: "Rolling Thoughts"
**Summary:** [2-3 sentences]
**Feasibility:** Medium | **Time Savings:** ~5 hrs/wk

## Medium Priority
[...]

## Low Priority
[...]

## Archive
### Built
#### [Idea Title]
**Completed:** YYYY-MM-DD | **Outcome:** [one-line outcome note]

### Dismissed
#### [Idea Title]
**Dismissed:** YYYY-MM-DD | **Reason:** [dismiss reason]

## Scan History
| Date | Sources | New | Updated | Total |
|---|---|---|---|---|
| YYYY-MM-DD | Fireflies (N days, M meetings), Notion (P pages) | X | Y | Z |
```

---

## Step 9.5: Regenerate Wiki Page

> Runs after Step 9, unless `--rerank-only` produced no score changes and no ideas were added or updated.

If new ideas were added OR existing ideas were updated OR priorities changed during this scan:

1. **Regenerate** `../kale-wiki/content/systems/automation-layer.mdx` with updated idea data:
   - Update the stats line (total ideas, high/medium/low counts)
   - Rebuild all `<IdeaCard>` components for High Priority ideas with current data (description, badges, meta including score, confidence, ROI, rock linkage, trend)
   - Rebuild the Medium and Low Priority tables
   - Update the category breakdown table
   - Update the `updated` frontmatter field to today's date
   - Preserve the page's narrative sections ("Where these ideas came from", "How this list stays current", etc.) — only update data-driven sections
   - Add a "Progress by Rock" section if rocks exist, showing linked ideas per rock
   - Update the CTA alert to mention new lifecycle flags (`--queue`, `--complete`, `--stale`)
2. **Verify** the MDX is valid:
   - No unclosed JSX tags
   - All `<IdeaCard>` props are properly formatted
   - Frontmatter is valid YAML
3. **Build check** (if kale-wiki has a build script):
   - Run `cd ../kale-wiki && npm run build` to verify no build errors
   - If build fails, fix the MDX and retry

If no changes occurred (no new ideas, no updates, no priority changes), report: "Wiki page is up to date — no rebuild needed" and skip Step 9.6.

---

## Step 9.6: Push Wiki Update

> Only runs if Step 9.5 regenerated the MDX page successfully.

1. In `../kale-wiki`, commit the updated `content/systems/automation-layer.mdx`:
   - Stage only the automation-layer.mdx file
   - Commit message: "Update automation layer — [N] ideas ([summary of changes])"
2. Push to the current branch (typically `master`)
   - This triggers a Cloudflare Pages deploy to `kale-wiki.pages.dev`
3. Report: "Wiki page updated and pushed — deploy will be live at https://kale-wiki.pages.dev/systems/automation-layer/"
4. If push fails:
   - Report the error but do NOT block scan results
   - Note: "Push failed. Review changes in `../kale-wiki/content/systems/automation-layer.mdx` and push manually."

---

## Step 10: Action Pipeline

> Runs when `--pick`, `--queue`, `--dismiss`, or `--complete` is provided. All four share the same fuzzy-match-or-list-top-5 pattern.

### Shared: Fuzzy Match

1. Search existing ideas in Notion for a title match (fuzzy — substring or close match)
2. If no match found, list the top 5 ideas and ask the user to pick one

### `--pick [title]`

1. Fuzzy match the idea
2. Update the matched Notion (Intake) entry: `Status` → "In Progress"
3. Update the local cache (`automations/ideas.md`): `status` → In Progress, `assigned_to` → current user, `picked_date` → today
4. Ask the user: "Want me to create an implementation plan? I'll run `/create-plan [idea description]`"
5. If yes, output the `/create-plan` invocation for the user to run
6. If a plan is created, update the idea's `plan_link` field in the local cache

### `--queue [title]`

1. Fuzzy match the idea
2. Update the matched Notion (Intake) entry: `Status` → "Accepted" (Intake's "queue / committed-to" state)
3. Update the local cache: `status` → Queued
4. Confirm: "**[Idea]** queued for later."

### `--dismiss [title] [reason]`

1. Fuzzy match the idea
2. Update the matched Notion (Intake) entry: `Status` → "Declined", append to `Description`: `[Dismissed YYYY-MM-DD]: [reason]`
3. Update the local cache: `status` → Dismissed, `dismiss_reason` → reason
4. Confirm: "**[Idea]** dismissed — [reason]"

### `--complete [title]`

1. Fuzzy match the idea
2. Ask the user: "One-line outcome note? (e.g., 'Saves ~3 hrs/wk, fully automated')"
3. Update the matched Notion (Intake) entry: `Status` → "Done", append to `Description`: `[Built YYYY-MM-DD]: [outcome]`
4. Update the local cache: `status` → Built, `completed_date` → today, `outcome` → user note
5. Confirm: "**[Idea]** marked as Built. Outcome recorded."

---

## Step 10.5: Stale Review

> Only runs when `--stale` is provided.

Stale-review queries read from the **local cache** (`automations/ideas.md`), not Notion — Notion's lean Intake schema doesn't carry the dates/counts needed for staleness detection.

1. From the local cache:
   - **Stuck ideas:** `status` = In Progress AND `picked_date` is 14+ days ago
   - **Forgotten ideas:** `status` = Queued AND `last_mentioned` is 30+ days ago
   - **Stale new ideas:** `status` = New AND `last_mentioned` is 30+ days ago AND `mention_count` = 1
2. Present as an actionable list:

```
## Stale Ideas Review

### Stuck (In Progress 14+ days)
1. **[Idea]** — picked [date], [N] days ago
   → Suggested: continue / dismiss / re-queue

### Forgotten (Queued, no recent mentions)
1. **[Idea]** — last mentioned [date], [N] days ago
   → Suggested: dismiss / keep queued

### Low-Signal (single mention, 30+ days old)
1. **[Idea]** — mentioned once on [date]
   → Suggested: dismiss / validate
```

3. Ask user which to act on and execute via Step 10 logic (--pick, --queue, --dismiss, --complete)

---

## Step 11: Present Summary

### Standard Summary

```
## Automation Ideas — [Date]

**Scan:** Fireflies ([N] days, [M] meetings), Notion ([P] pages)
**New ideas:** [N] | **Updated:** [M] | **Total active:** [T]

### Top Priorities
1. **[Idea]** — [one-liner] | Score: [score] | Confidence: [conf] | Trend: [trend]
2. ...
3. ...

### Progress by Rock
**[Rock: Hit 90% inbox placement]** (Roshan) — 2/4 linked ideas in progress
  - Deliverability monitoring dashboard — In Progress
  - Inbox health scoring — Queued
  - Bounce rate monitoring — New
  - Domain/inbox provisioning — Built ✓

**[Rock: Automate campaign setup]** (Shared) — 0/2 started
  - Net new lead logic — High priority, not started
  - D7 search scheduling — Medium priority, not started

**Unlinked High-Priority Ideas** (consider linking to a rock)
  - [Idea] — Score: [score]
  - ...

### Best ROI (Easy Wins)
1. **[Idea]** — ROI: [score] | Feasibility: Easy | Time Savings: ~X hrs/wk
2. ...

### Low Confidence (Validate These)
- **[Idea]** — single mention, consider validating before building
- ...

### Trending Up
- **[Idea]** — score increased by [delta] | [category]

### New This Scan
- **[Idea]** — [one-liner] _(from [source])_
- ...

### Updated
- **[Idea]** — +[N] mentions _(newly found in [source])_
- ...

### Ready to Build (Queued)
- **[Idea]** — Score: [score] | Feasibility: [f]
- ...

### Stale Ideas (30+ days, no new mentions)
- **[Idea]** — last mentioned [date] | [category]
- ...

**Wiki page:** [Updated and pushed / Up to date / Push failed] — https://kale-wiki.pages.dev/systems/automation-layer/
**Notion DB:** [URL]
**Local cache:** automations/ideas.md
**Build something?** Run `/generate-automation-ideas --pick [idea title]`
```

**ROI Calculation (for "Best ROI" section):**
`ROI = Time Savings Score / (6 - Feasibility Score)`
Higher ROI = high time savings with easy feasibility. Used for display only, not stored in Notion.

### Team Report (`--team-report`)

Group ideas by rock first, then by assignee within each rock. Unlinked ideas shown separately:
```
## Team Report — [Date]

### Rock: [Rock Title] (Owner)
**Roshan:**
- **[Idea]** — Status: In Progress | Score: [score] | Trend: [trend]
- ...

**Mike:**
- ...

### Rock: [Rock Title] (Owner)
...

### Unlinked Ideas
**Roshan:**
- **[Idea]** — Status: In Progress | Priority: High
- ...

**Unassigned:**
- **[Idea]** — Priority: High (consider assigning)
- ...
```

### Digest (`--digest`)

Compact format suitable for Slack or email, with rocks summary at top:
```
**Automation Ideas Digest — Week of [Date]**

**Rocks Status:**
- [Rock] (Owner) — [X/Y] ideas in progress
- [Rock] (Owner) — [X/Y] ideas in progress

[N] new ideas | [M] updated | [T] total active

Top 3 priorities:
1. [Idea] — [one-liner] (Score: [score])
2. [Idea] — [one-liner] (Score: [score])
3. [Idea] — [one-liner] (Score: [score])

Easy wins: [Idea] (ROI: [score]), [Idea] (ROI: [score])
Trending up: [Idea], [Idea]
Stale (needs review): [Idea], [Idea]

Full backlog: [Notion URL]
```

---

## Error Handling

- **Fireflies API errors:** Log the error, continue with whatever data was retrieved. Report partial results.
- **Notion API errors:** If DB creation fails, fall back to local-only mode (populate `automations/ideas.md` without Notion). Inform user.
- **No results from scanning:** Report "No automation signals found in the scanned period" and suggest expanding `--days`.
- **Rate limiting:** If hitting rate limits, pause and inform the user. Process what's available.
