# /generate-content-ideas

> Scan recent work across repos, meetings, and learnings to surface LinkedIn post ideas. Lightweight by default — git-only scan runs in under a minute. Opt into Fireflies and Notion for richer signals.

**Usage:** `/generate-content-ideas [flags]`

**Flags:**
- `--days N` (default: 14) — git log lookback window
- `--sources git,fireflies,notion` (default: `git`) — which signal sources to scan
- `--draft [N]` — draft a standalone LinkedIn post for idea #N (or top idea if no number)
- `--from-session` — scan current conversation context for content angles (no git/API calls)

**Examples:**
- `/generate-content-ideas` — scan git across 3 repos, last 14 days
- `/generate-content-ideas --days 30 --sources git,fireflies` — deeper scan with meeting transcripts
- `/generate-content-ideas --draft 1` — draft the top idea as a LinkedIn post
- `/generate-content-ideas --from-session` — surface content angles from this session's work

---

## Step 1: Parse Arguments

Parse `$ARGUMENTS` for flags:

| Flag | Default | Notes |
|------|---------|-------|
| `--days N` | 14 | Lookback window for git log and Fireflies |
| `--sources` | `git` | Comma-separated. Valid: `git`, `fireflies`, `notion` |
| `--draft [N]` | — | If provided, skip to Step 9 (Draft) after scanning. N = idea number. |
| `--from-session` | — | If provided, skip to Step 8.5 (Session Scan). |

If `--from-session` is provided, skip Steps 2-4 entirely and jump to Step 8.5.

---

## Step 2: Load Context

Read these files:

1. `context/strategy.md` — current priorities (relevance filter)
2. `context/business-info.md` — company positioning (audience framing)
3. `context/roshan.md` or `context/mike.md` — founder voice/angle
4. `outputs/content-ideas.md` — previous scan (if exists, for dedup)

Detect the active user via (1) `KALE_USER` env var, (2) `config/local.json`, (3) ask interactively.

Note the founder's content angle:
- **Roshan**: technical/operational — building internal systems, deliverability engineering, AI-assisted workflows, scaling with small teams
- **Mike**: sales/positioning — client acquisition, market positioning, growth tactics, outreach strategy

---

## Step 3: Scan Git History (always runs unless `--from-session`)

Scan three repos. For each, check if it exists at the expected path before scanning:

| Repo | Primary path | Fallback path |
|------|-------------|---------------|
| kale-workspace | `.` (current dir) | — |
| kale-os | `../../kale-os` | `~/kale-os` |
| kale-wiki | `../kale-wiki` | — |

For each repo that exists, run:
```bash
git log --all --oneline --since="N days ago"
git log --all --format="%h %s" --since="N days ago" | head -80
```

Also check for new/modified content files:
```bash
git diff --name-only --diff-filter=AM HEAD~20 -- knowledge/ plans/ outputs/   # kale-workspace
git diff --name-only --diff-filter=AM HEAD~20 -- content/                      # kale-wiki
```

### Signal Extraction

For each commit, classify as signal or noise:

**Signal** (keep):
- Feature builds — commits with `feat:`, `add`, `build`, `implement` in the message
- System design — `redesign`, `refactor`, `architecture`, `migrate`
- Problem-solving — `fix:` sequences (3+ fixes on the same topic = a story), debugging trails
- Operational improvements — new scripts, automation, workflow changes
- Milestones — merge commits for significant PRs, releases

**Noise** (skip):
- `chore: auto-sync from kale-workspace`
- Version bumps, dependency updates
- Trivial formatting/typo fixes
- Single-line config changes

Group related commits into **clusters** — e.g., 5 commits about health scoring = one "health scoring build" cluster.

---

## Step 4: Scan Fireflies (opt-in via `--sources fireflies`)

> Skip if `--sources` doesn't include `fireflies`.

Call `fireflies_get_transcripts(limit: 20, fromDate: N days ago)`. Deduplicate by title+date (Fireflies creates ~2x records per meeting).

For each unique meeting with a summary, call `fireflies_get_summary(id)`.

**Look for content-worthy moments:**
- Someone explaining something non-obvious to a teammate or client
- "We realized...", "The thing that actually worked was...", "We stopped doing X and started doing Y"
- Client reactions to something Kale built
- Strategic pivots or hard decisions discussed in real time
- Good metaphors or framings that translate to a public audience
- Disagreements that led to better outcomes

Extract: meeting title, date, speaker, relevant quote/summary snippet, content angle.

---

## Step 5: Scan Notion (opt-in via `--sources notion`)

> Skip if `--sources` doesn't include `notion`.

Light touch — no database creation, no writes:

1. **Automation Ideas DB** (`ed8a1f2c6d2b4efea1917b0c3b496bc2`): Query for ideas with Status = "Built" or "In Progress". Completed automations are natural build stories.
2. **Learnings DB**: Search for recent entries, especially those flagged as "Wiki Candidate" — these are pre-validated content signals.
3. **Curated pages**: Fetch pages from `config/profiles.json` (`notion_curated_pages`) for the active user. Skim for new content since the lookback window.

Extract: title, category, description, content angle.

---

## Step 6: Cluster & Generate Ideas

Group related signals across all scanned sources into content ideas. Each idea should represent a **single, postable angle** — not a broad topic.

For each idea, generate:

| Field | Description |
|-------|-------------|
| **Topic** | The hook — specific, concrete. Write it as a potential first line. e.g., "We stopped scoring inbox health and started diagnosing it" |
| **Why interesting** | 1-2 sentences on what makes this non-obvious or counterintuitive |
| **Content type** | One of: **Build Story** ("we built X, here's what happened"), **Operational Insight** ("here's what we learned running X"), **System Design** ("why we chose X over Y"), **Decision Record** ("the tradeoff we made and why"), **Metric Reveal** ("here are the numbers behind X"), **Failure Lesson** ("what didn't work and what we learned") |
| **Source evidence** | Which commits, meetings, wiki pages, or learnings inform it |
| **Readiness** | **Ready to write** = enough context exists to draft now. **Needs more time** = still in progress, wait for outcome. |
| **Founder fit** | Roshan (technical/ops), Mike (sales/positioning), or Both |

### Dedup

If `outputs/content-ideas.md` exists from a previous scan, compare new ideas against it:
- If an idea matches a previous one, mark it as "Still relevant" with updated evidence
- Only surface genuinely new angles as new

### Quality filter

Before including an idea, check:
- Could this be a real LinkedIn post, or is it too internal/niche?
- Is there a clear before/after arc?
- Would another founder/operator find the insight useful?

If the answer to all three isn't yes, drop the idea.

---

## Step 7: Score Audience Resonance

Score each idea on 4 traits aligned with the kale-content skill's topic quality criteria:

| Trait | Weight | 5 (Strong) | 1 (Weak) |
|-------|--------|------------|----------|
| **Specificity** | 30% | Concrete numbers, tools, timeframes ("cut bounce rate from 8% to 1.2%") | Vague ("improved our systems") |
| **Transferability** | 30% | Other operators/founders could apply this insight directly | Only makes sense with Kale-specific context |
| **Non-obviousness** | 25% | Counterintuitive, goes against conventional wisdom, or reveals hidden dynamics | Common knowledge in the industry |
| **Narrative arc** | 15% | Clear problem to shift to outcome transformation | No discernible before/after |

**Composite** = (Specificity x 0.30) + (Transferability x 0.30) + (Non-obviousness x 0.25) + (Narrative arc x 0.15)

Rating:
- **Strong** (>= 3.5) — high-confidence post idea, likely to resonate
- **Decent** (>= 2.5) — worth considering, may need a sharper angle
- **Weak** (< 2.5) — omit from output unless no strong/decent ideas found

---

## Step 8: Write Output & Present Summary

### Write to file

Overwrite `outputs/content-ideas.md`:

```markdown
# Content Ideas

> Scanned [date] by `/generate-content-ideas`. Rerun to refresh.

**Scan:** Git ([N] days, [repos scanned], [M] commits)[, Fireflies ([P] meetings)][, Notion ([Q] pages)]
**Ideas:** [S] strong, [D] decent

---

## Strong Ideas

### 1. "[Topic/Hook]"
**Type:** [Content Type] | **Fit:** [Founder] | **Resonance:** [score] | **Readiness:** [Ready/Needs time]
**Why interesting:** [1-2 sentences]
**Sources:**
- [repo]: `[commit message]` ([date])
- [Fireflies]: "[meeting]" — [relevant quote/context]
**Draft angle:** [1 sentence suggesting how to frame the LinkedIn post]

### 2. ...

## Decent Ideas

### N. ...

---

## How to use these
- **Draft a post now:** `/generate-content-ideas --draft 1`
- **Create a full wiki resource:** `/create-resource [topic]`
- **Capture for later:** ideas persist in outputs/content-ideas.md until next scan
```

### Present in chat

Compact summary:

```
## Content Ideas — [Date]

**Scanned:** [sources summary]
**Ideas:** [S] strong, [D] decent

### Top Ideas
1. "[Topic]" — [Content Type] | [score]
2. "[Topic]" — [Content Type] | [score]
3. "[Topic]" — [Content Type] | [score]

**Draft one?** `/generate-content-ideas --draft 1`
**Full list:** outputs/content-ideas.md
```

---

## Step 8.5: Session Scan (only if `--from-session`)

> Runs instead of Steps 2-5 when `--from-session` is provided.

1. **Analyze the current conversation context** — what was built, discussed, decided, or debugged this session. Look at:
   - Tools used and files modified
   - Problems solved and approaches tried
   - Decisions made and their reasoning
   - Surprises, failures, or non-obvious outcomes

2. **Extract content angles** using the same idea generation criteria as Step 6.

3. **Score and output** as normal (Steps 7-8).

This is the "end of session" mode — quick capture of content angles from what just happened, without any git or API calls.

---

## Step 9: Draft (only if `--draft` flag)

> Runs after scanning (or directly if a previous scan exists in `outputs/content-ideas.md`).

If `--draft [N]` is provided:

1. **Load the idea**: If N is specified, use idea #N from the current scan or from `outputs/content-ideas.md`. If no N, use the top-ranked idea.

2. **Load LinkedIn format rules**: Read `.claude/skills/kale-content/SKILL.md` — specifically the "Output Type 2: LinkedIn Content" section and the "Operator's Diary Series" format.

3. **Gather source material**: For the selected idea, read the actual source evidence:
   - For git commits: `git show [hash]` or `git diff` for relevant changes
   - For Fireflies: re-fetch the meeting summary if needed
   - For wiki pages: read the MDX content

4. **Generate a standalone LinkedIn post**:
   - Follow Operator's Diary format:
     ```
     Operator's Diary #[n]

     [Hook line — concrete, specific outcome]

     [Context — what was broken or limited]

     [The shift — what changed, the decision or realization]

     [How it works now — concrete details, not vague claims]

     [The real insight — non-obvious takeaway]

     [Soft CTA or series signal]
     ```
   - 150-250 words (max 350, minimum 100)
   - No emoji, no hashtag spam
   - AI as supporting character, never the hero
   - Strip proprietary detail — no client names, specific configs, internal tool names
   - First person: "I built," "we decided," "here's what I learned"

5. **Save to file**: Write the draft to `outputs/linkedin-draft-[slug].md` where slug is derived from the topic.

6. **Present in chat**: Display the full draft and ask for feedback. The user can iterate — request edits, change the angle, sharpen the hook, etc.

---

## Error Handling

- **Missing repo**: If kale-os or kale-wiki doesn't exist at the expected path, skip it and note: "Skipped [repo] — not found at [path]". Continue with available repos.
- **No signals found**: If no content-worthy commits in the lookback window, suggest: "No strong signals in the last [N] days. Try `--days 30` for a wider window, or `--sources git,fireflies` to include meeting transcripts."
- **Fireflies API errors**: Log the error, continue with git-only results. Report partial scan.
- **Empty session** (`--from-session` with no substantive work): Report "This session doesn't have enough context for content ideas. Try running a standard scan instead."
