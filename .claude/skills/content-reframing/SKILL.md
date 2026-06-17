---
name: content-reframing
description: Reshape existing content for a non-technical audience. Use this skill whenever you're taking an internal artifact (plan, SOP, technical doc, meeting notes, migration runbook) and preparing it for a reader who isn't in the engineering context — specifically clients, internal non-technical team members (Mike, Arra, Beverly, Umer), or external partners and vendors. Triggers on keywords like "for Mike", "for the client", "for the vendor", "send to [X]", "layman", "plain language", "friendly", "non-technical", or when a request names an external party. Does NOT apply to artifacts for technical readers (Azhar, code comments, engineering plans, architecture docs).
---

# Content Reframing Skill

This skill takes existing internal content and reshapes it for a specific non-technical reader. It's a reframing skill, not a writing-from-scratch skill — the source material already exists, the job is to tune voice, structure, and detail to the reader.

---

## When this skill fires

**Proactively, when:**
- The user addresses an artifact to a named non-technical person or external party.
- The user asks for "layman," "plain language," "friendly," "non-technical," or "for [non-engineer]" framing.
- An artifact is clearly going to clients, vendors, partners, or non-engineering team members.

**Explicitly, when:**
- The user invokes the skill by name.
- An artifact's frontmatter or brief specifies an audience in one of the three buckets below.

**Does NOT fire for:**
- Internal engineering artifacts (Azhar briefs, code comments, architecture docs, technical plans).
- Commit messages, PR descriptions for engineering review.
- Source code or configuration.
- Content already covered by `kale-content` (new LinkedIn posts, internal knowledge HTML docs) — though reframing an internal artifact into a public-facing version is a future extension.

---

## The core move: write for the reader, not for yourself

Most drafts default to the writer's vocabulary and mental model. This skill's job is to flip that. Before touching the draft, name the reader explicitly, then ask three questions:

1. **What do they already know?** Anchor new information to their existing knowledge.
2. **What do they care about?** Lead with outcomes in their terms, not ours.
3. **What do they need to do?** If it's an action doc, the first thing they see should be what to do — not what the system is.

If you can't answer those three questions for the artifact in front of you, ask the user before rewriting.

---

## The three audience buckets

Pick one per artifact. If an artifact spans two audiences, split it into two artifacts.

### Bucket 1: Clients

**Who:** External business stakeholders — Chris Risch (N2), Brian Morrison (Terraboost), Greg Boyd (Riipen), Bethany Mascena Tracy (N2 Recruiting), Abby, and future client primary contacts.

**What they know:** Their own business, their own metrics, roughly what cold email delivery looks like as a service. They do not know: our internal codebase, our infrastructure naming, our team structure, our tooling stack.

**What they care about:**
- Their campaigns — are they sending, are they performing, are they at risk?
- Their numbers — replies, bookings, conversion, deliverability
- Timing — when something happens, when it resolves, when they'll see results
- Risk — what could go wrong, what's the fallback

**What trips them up:**
- Kale internal names (NPE-Bison, PE-Bison, Kale OS, Tier 1/2/3)
- Tool names without context (EmailBison, Instantly, Clay) — say "the sending platform" on first reference
- Implementation mechanics — DB fields, API endpoints, schema
- Passive voice about work "being done" without a named owner

**Voice:** Confident, business-framed, no Kale internals. Like a senior account manager briefing the client. First person plural for Kale ("we're migrating your sending infrastructure"). Specific about dates and numbers. Honest about risk.

**Structural defaults:**
- Open with what's happening and why it matters to them.
- Summarize the change in one or two sentences they could forward to their team.
- Call out any action or decision needed from their side upfront.
- End with timing and next check-in.

### Bucket 2: Internal non-technical team

**Who:** Mike, Arra, Beverly, Umer, and future non-engineering hires.

**What they know:** Kale operations end-to-end. Client names, verticals, the service model. They don't know: our code, our DB schema, our API details. Sub-voices inside this bucket:
- **Mike** wants revenue impact, client-facing implications, and timing. Skims past anything that sounds like "Roshan's domain."
- **Arra** wants dependencies, coordination, who-owns-what, and timelines.
- **Beverly / Umer** want step-by-step instructions with clear do / don't, and a way to verify success.

**What they care about:**
- Client impact (for Mike)
- Coordination across the team (for Arra)
- Process clarity and executability (for Beverly / Umer)
- Their specific role in whatever you're documenting

**What trips them up:**
- Technical vocabulary they don't use in their own work
- Missing ownership ("someone will do X")
- Implicit context — assuming they remember the last conversation
- Long preambles — they skim

**Voice:** Warm, clear, action-oriented. Second person when giving instructions ("you'll do X"). Name people explicitly — never "the team" when you mean "Arra and Pandush." Short paragraphs. Lead with the ask if there's one.

**Structural defaults:**
- If the artifact has an ask for them, open with it.
- Use headed sections they can scan: "What's changing," "What you need to do," "Timing."
- For SOPs and procedural docs: numbered steps, verify-success line at the end of each step.
- Avoid tables unless the data genuinely is tabular; prose reads faster for skimmers.

### Bucket 3: External partners / vendors

**Who:** Cheapinboxes, Premium Inboxes, infrastructure vendors, tool partner support teams, and future external collaborators we pay or partner with.

**What they know:** Their own craft — the sequencer platforms, mailbox provisioning, domain management. They do not know our internal naming, our codebase, our team dynamics, or our reasons for any decision.

**What they care about:**
- Exactly what to do, in what order
- What not to touch
- How to report progress back to us
- What to do when something's unclear
- What the timeline is and how tight it is

**What trips them up:**
- Internal code names (PE-Bison, NPE-Bison) without translation — they see a name we gave something, not a thing in the world
- Justifications and context they don't need to execute
- Dense tables of acronyms
- Ambiguity about what "we" vs "you" refers to
- Missing contact info or escalation path

**Voice:** Professional, direct, partner-tone. Short sentences. Second person for their actions, first person for ours. Tag names consistently — if you call it "the new Bison" once, keep calling it that.

**Structural defaults:**
- Open with a one-paragraph scope: what you're asking them to do, for which work, by when.
- Name the platforms in plain terms ("the new Bison instance" > "PE-Bison") and only introduce internal codenames if they'll see them in dashboards.
- Separate what they do from what we do — with named columns or sections.
- Always include a "flag instead of improvise" section with examples of what to escalate.
- End with contact info and a clear next-step expectation.

---

## Rewrite rules

Apply these when moving from the internal draft to the audience-facing version.

### Jargon swaps (not exhaustive — build intuition, don't memorize)

| Internal | Client / non-tech team / vendor |
|---|---|
| Schema / DB / database | "the data we track about each [thing]" |
| Ingestion pipeline | "how information flows into our system" |
| NPE-Bison / PE-Bison | "the existing Bison / the new Bison" (or "the shared sender / the new sender") |
| Sequencer | "the sending platform" (or platform name: Instantly, Bison) |
| Tenant / instance | "account" or "workspace" |
| Invariant / assertion | "rule" or "the check that fails if…" |
| Backfill | "fill in the historical data" |
| Deliverability / inbox placement | "how often emails actually land in the inbox" (for client; keep as-is for technical vendors) |
| Rotation / warmup / reputation | Translate to what it means operationally, not mechanically |
| Migration / cutover | "moving [thing] from X to Y" |
| Additive change | "we're adding new fields, not changing existing ones" |
| Repo / branch / commit | Avoid entirely unless talking to Azhar |

**Rule of thumb:** if you wouldn't say the word out loud in a meeting with this reader, don't write it in a doc for them.

### Structural swaps

- **Dense technical tables → prose or bulleted lists** when the reader will skim. A 7-column table is an ask to concentrate; prose is an invitation to read.
- **Context-first → action-first** for anything the reader needs to execute. Lead with what to do; put the why below if they need it.
- **Passive voice → named ownership.** "The inbox will be migrated" becomes "Cheapinboxes will migrate the inbox." Every sentence about work has a named actor.
- **Acronyms → spelled out on first use** or replaced with plain-language descriptors.
- **Long paragraphs → short paragraphs.** One idea per paragraph. If a paragraph has three ideas, it's three paragraphs.

### Tone markers that signal "I'm writing for myself not you"

If the draft contains any of these, rewrite:
- "Note that…" (condescending) → just state the thing
- "It should be noted that…" → cut entirely
- "Simply…" (implies they're failing if it's not simple) → cut the word
- "Obviously…" → cut
- Hedging chains ("we might potentially want to consider…") → pick a verb and commit
- Nominalized verbs ("perform a migration of") → use the verb ("migrate")

---

## Self-review checklist

Before marking a reframed draft done, run through these five questions. If any answer is "no" or "not sure," keep editing.

1. **Could the reader execute this without asking a follow-up question?** If there's ambiguity, resolve it in the draft, not in their head.
2. **Does every paragraph earn its place for this reader?** Cut anything that's there for your benefit, not theirs.
3. **Am I explaining the "why" in terms they care about, not terms I care about?** Their metrics, their timing, their risk — not our implementation.
4. **Would they read past paragraph 1?** The first paragraph earns the second. Lead with what they need, not with context they'll skim.
5. **Did I use any word or acronym I wouldn't say out loud in a meeting with them?** If yes, replace.

---

## Before / after examples

Drawn from the 2026-04-22 vendor handoff doc for the Instantly → PE-Bison migration, which was originally drafted for an engineering reader and needed reframing for Cheapinboxes + Premium Inboxes.

### Example 1 — Opening

**Internal-voice draft:**

> Kale is consolidating all client-sending inboxes that currently live in Instantly onto a new Bison instance — **PE-Bison** (Personal Environment Bison). The existing **NPE-Bison** (Non-Personal Environment) instance stays untouched and continues to operate as it does today.

**Reframed for vendors:**

> We're moving inboxes from one sending platform (Instantly) to another (a new Bison account we've just set up — we'll call it "the new Bison" in this doc). You're the team doing the actual moves. Our existing Bison account — the one with `outbound.kaleacquisition.com` in the URL — stays exactly as it is. Don't touch anything in that one.

Why it's better: names platforms in plain terms, names "you" and "us" explicitly, drops the acronyms, replaces abstract "consolidate" with concrete "move."

### Example 2 — Describing preserved settings

**Internal-voice draft:**

> Replicate the following per-inbox state across platforms: daily_limit (preserve exactly — no ramp, leverage retained mailbox-level reputation), warmup_enabled flag, custom_tags (per supplied mapping file), campaign assignments, send schedule / timezone.

**Reframed for vendors:**

> For every inbox you move, five things need to match what they were on Instantly:
>
> - The daily send limit. Don't reduce it or ramp it up — these mailboxes already have their reputation built, they can send at full volume right away.
> - Whether warmup was on or off.
> - Tags. Use the tag mapping spreadsheet we sent — every Instantly tag has a matching one in the new Bison.
> - Which campaign the inbox sends from.
> - The send schedule and timezone.

Why it's better: prose + list over a compact jargon-heavy sentence, plain-language explanation of the warmup decision, concrete reference to the mapping file.

### Example 3 — The "don't" rules

**Internal-voice draft:**

> Dual-tenant invariant: an inbox MUST NOT exist in an active/connected state on Instantly and PE-Bison simultaneously. Violations will be detected by the sync reconciliation and flagged as errors.

**Reframed for vendors:**

> Never leave an inbox connected to both Instantly and the new Bison at the same time. Always disconnect from Instantly first, then connect to the new Bison. Our system will page us if it ever sees the same inbox live in both places, so we'd rather you go slower and be clean than move fast and double-connect.

Why it's better: "invariant," "reconciliation," and "flagged as errors" become a plain-language rule; the why is anchored to something the vendor cares about (they'd rather go slow than cause an alert).

---

## Workflow when the skill fires

1. **Name the audience explicitly** before drafting. Pick the bucket. If unclear, ask the user.
2. **Read the source artifact in full** — the internal version you're reframing from.
3. **Draft in the audience's voice**, using the rewrite rules and structural defaults above.
4. **Run the self-review checklist.** Edit until all five answers are yes.
5. **Return the reframed version** alongside (not replacing) the internal version. The internal version may still be needed for engineering reference.

---

## What this skill does NOT do

- It doesn't invent content that isn't in the source artifact. If the source is missing information the audience needs, flag the gap — don't fabricate.
- It doesn't simplify to the point of misleading. "Plain language" doesn't mean "lose accuracy." If something is actually complex or risky, say so plainly.
- It doesn't replace thinking about whether the artifact should exist at all. If the right move is a phone call instead of a doc, say that.
