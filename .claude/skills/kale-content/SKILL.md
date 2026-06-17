---
name: kale-content-from-learnings
description: Turn Claude Code sessions, technology learnings, and operational builds into polished content assets. Produces two output types — (1) internal-facing HTML/PDF knowledge documents styled to Kale's brand system, and (2) LinkedIn posts extracted from the internal docs. The internal doc is always the primary artifact; LinkedIn content is a stripped-back derivative. Use this skill whenever Roshan wants to document what he built, learned, or figured out — whether for the team or for public content. Always read the kale-frontend skill first for brand styling reference.
---

# Kale Content-from-Learnings Skill

This skill converts raw technical and operational learnings into two types of polished assets:

1. **Internal docs** — Standalone HTML pages (and/or PDFs generated from them) styled to Kale's brand system. These are the primary, detailed artifact.
2. **LinkedIn posts** — Stripped-back derivatives of the internal docs, extracting only the transferable insight for public consumption.

**The internal doc always comes first. LinkedIn content is extracted from it, never the other way around.**

Read this entire file before producing any content. Before writing any HTML, also read the `kale-frontend` skill for the complete brand system (colors, typography, components).

---

## Philosophy

Roshan builds systems, experiments with tools, and solves operational problems constantly. Most of that knowledge lives in his head or scattered across Claude Code sessions. This skill exists to **capture and package those learnings** so they compound — internally for the team, and externally for brand building.

### Core principles

- **Insight over process**: Nobody cares about the steps. They care about what you learned, what changed, and why it matters.
- **Honest about AI's role**: Claude is a thinking partner and execution accelerator — never the hero. The system design, the decision, or the insight is always the real story.
- **Operator credibility**: Content should sound like someone in the trenches documenting as they go, not someone theorizing from the sidelines.
- **Speed through clarity**: The same philosophy that drives Kale's operations drives its content — force clarity upfront, then execute fast.
- **Internal doc is the source of truth**: The detailed version lives internally. External content is a compressed extract — never the primary artifact.

---

## Output Type 1: Internal HTML Documents

Internal docs are standalone HTML files styled to Kale's brand system. They follow the same visual language as the Team Playbook — deep green sidebar, warm cream background, white content cards, monospace data, and the full component library.

### Before writing any HTML

1. Read the `kale-frontend` skill to load the complete brand system.
2. Reference the Team Playbook's CSS patterns (documented below) for component markup.
3. Plan the page structure — sidebar TOC, sections, and component types needed — before writing code.

### Voice & Tone

- **Direct and practical**: Write like you're explaining to a smart teammate who wasn't in the room. No fluff, no preamble.
- **Confident but honest**: State what you know. Flag what you don't. Use "we think" or "hypothesis" when something is unvalidated.
- **First person plural**: "We" for team decisions, "I" for individual learnings/experiments when attribution matters.

### Page Architecture

Every internal doc follows this shell:

```
Page
├── Sidebar (fixed left, 260px)
│   ├── Kale logo (cream on deep green)
│   ├── Document subtitle
│   └── Table of contents (section links + sub-links)
│
└── Main content (max-width ~900px, padded)
    ├── Hero (H1 title + subtitle)
    ├── Callout box (optional — key context or "source of truth" declaration)
    │
    ├── Section 1 (section-number label + H2 + content)
    │   ├── Prose paragraphs
    │   ├── Component blocks (cards, tables, diagrams, etc.)
    │   └── Sub-sections (H3, H4)
    │
    ├── Divider (hr)
    ├── Section 2...
    │
    └── Footer (document title + date)
```

### Component Library

These components are available for internal docs. Use them based on content type — never force a component where prose works better.

#### Callout Box
For critical context, source-of-truth declarations, or important warnings. Use sparingly — one per page max unless the page is very long.
```
- White background, subtle border
- Left border: 3px solid kale-green
- Bold lead sentence + supporting body text
- Inline code for commands/technical references
```

#### Cards
For grouping related content (side-by-side categories, feature summaries, team info).
```
- White background, subtle border, small shadow
- Border-radius: radius-md
- Padding: ~24px
- Can be laid out in .grid-2 for side-by-side
```

#### Data Tables
For structured comparisons, tool lists, configuration details.
```
- Header: uppercase, small, secondary color, semibold
- Header border-bottom: 2px solid
- Rows: 1px subtle border, hover state
- Monospace for technical values
- No colored header backgrounds
```

#### Priority / Numbered List Cards
For ranked items, strategic priorities, or ordered concepts.
```
- Mono-font number (large, deep-green)
- Title (semibold) + description (light weight, secondary color)
- Dividers between items
- Contained in a single card
```

#### Flow Steps
For sequential processes, workflows, or step-by-step procedures.
```
- Numbered steps (mono font, flow-number)
- Each step: title (semibold) + description (light, secondary)
- Optional: command block (mono, green bg)
- Connected by thin dividers between steps
```

#### Compare Blocks (Right/Wrong)
For showing what to do vs what not to do, before/after, weak vs strong.
```
- Side-by-side cards in a .compare grid
- Left border: clay-red for wrong, kale-green for right
- Label: uppercase, small, colored to match
- Content: body text with examples
```

#### Failure / Troubleshooting Cards
For documenting common mistakes, failure modes, or gotchas.
```
- Numbered circle (mono, charcoal bg, cream text)
- Title (semibold) + rows of Symptom/Cause/Fix
- Row labels: bold, minimum width for alignment
```

#### Tier Diagrams
For showing hierarchical relationships (repo structure, system architecture).
```
- Stacked tier boxes connected by arrows
- Tier 1: deep-green bg (highest level)
- Tier 2: white bg, green border (middle)
- Tier 3: alt bg, dashed border (lowest)
- Arrow labels explain the relationship between tiers
- Who-tags as pills showing ownership
```

#### Sync Diagrams
For showing what flows between systems, what stays, what syncs.
```
- Side-by-side panels with arrow column between
- Items marked as "synced" (green) or "stays here" (grey)
- Labels as small pills
```

#### Alert Boxes
For warnings, info notices, or important callouts within a section.
```
- Left border: 3px solid [status color]
- Subtle background tint matching the status
- Title (semibold, 14px) + description (light, 13px, secondary)
- Variants: alert-green, alert-oat, alert-info
```

#### Status Badges
For inline status indicators, phase labels, or category tags.
```
- Pill-shaped: radius-full
- Subtle background + colored text
- Uppercase, tiny, semibold, letter-spaced
- Variants: green, oat, blue
```

#### Checklists
For session start/end checklists, verification steps, or requirements lists.
```
- Custom checkbox styling (border, rounded corners)
- Items as list with subtle bottom borders
- Code references inline where relevant
```

#### Tree / Directory Views
For file structures, repo layouts, or hierarchy displays.
```
- Charcoal background (dark mode block)
- Mono font throughout
- Directories in soft-sage color
- Comments in muted grey, italic
- Standard tree characters: ├── │ └──
```

### Content Depth Calibration

Match depth to audience need:

- **Team-wide docs** (read by everyone, including new team members): Write with enough context that someone joining next month could follow. Define acronyms on first use. Explain "why" not just "what."
- **Technical reference docs** (read by Roshan + whoever is building): Can assume familiarity with the stack. Focus on decisions, configurations, and rationale. Skip the basics.
- **Process docs** (read by Pandush/operators): Step-by-step with explicit detail. Assume they'll follow it literally. Include what to do when something goes wrong — use failure cards for common issues.

### Formatting Rules

1. **Prose over bullets**: Default to paragraphs. Use bullets only for actual lists (team members, tools, sequential steps). Never bullet-dump an explanation.
2. **Callout boxes for critical context**: Green-bordered callout blocks for source-of-truth declarations, important warnings, or key definitions. Sparingly.
3. **Code/technical references in monospace**: Tool names, commands (`/prime`, `/create-plan`, `/implement`), file paths, config values, domain names, and email addresses get inline `<code>` formatting.
4. **Cards for grouping**: When you have parallel categories (e.g., Leadership vs Team, or Google vs Outlook configs), use side-by-side card layouts.
5. **No orphan sections**: Every section should have meaningful content. If you can't write at least 2-3 sentences about it, it's not its own section.
6. **Sentence case everywhere**: Headings in sentence case. No ALL CAPS headings. Uppercase is reserved for section-number labels, table headers, and metric labels.
7. **Link generously**: Cross-reference other docs, tools, and external resources with proper `<a>` tags.
8. **Section numbering**: Use `.section-number` labels (mono, small, uppercase, green) above H2s to create clear document navigation. These should match the sidebar TOC groupings.

### Favicon

Every resource must include the Kale logo as an inline favicon. Read the base64 string from `resources/_template/favicon-base64.txt` and add this tag inside `<head>`:

```html
<link rel="icon" type="image/png" href="data:image/png;base64,{CONTENTS_OF_FAVICON_BASE64_TXT}">
```

This keeps the HTML fully standalone — no external favicon URL needed.

### CSS Foundation

Internal HTML docs should include the full Kale CSS variable system from the `kale-frontend` skill on `:root`, plus the component CSS patterns from the Team Playbook. The core structural CSS includes:

- Google Fonts import (DM Sans + IBM Plex Mono)
- All Kale CSS custom properties
- `.page` grid layout (sidebar + main)
- `.sidebar` styles with TOC navigation
- `.main` content area with max-width
- All component classes listed above

When building a new internal doc, start from the Team Playbook's CSS as a base and add component-specific styles as needed. Do not reinvent the styling — reuse the established patterns.

### Active Sidebar Scroll Tracking

Every resource with a sidebar TOC must include scroll-spy behavior that highlights the currently visible section in the sidebar as the user scrolls. This is a standard feature, not optional.

**CSS** — add to `.toc-link` styles:
```css
.toc-link.active{background:rgba(245,241,234,.1);color:rgba(245,241,234,1);font-weight:500}
```

**JavaScript** — add before `</body>`:
```html
<script>
(function(){
  const links = document.querySelectorAll('.toc-link');
  const sections = [];
  links.forEach(function(link){
    var id = link.getAttribute('href');
    if(id && id.startsWith('#')){
      var el = document.querySelector(id);
      if(el) sections.push({id: id.slice(1), el: el, link: link});
    }
  });
  if(!sections.length) return;
  var current = null;
  var observer = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        if(current) current.classList.remove('active');
        var match = sections.find(function(s){ return s.el === entry.target; });
        if(match){
          match.link.classList.add('active');
          current = match.link;
        }
      }
    });
  }, {rootMargin: '-10% 0px -80% 0px'});
  sections.forEach(function(s){ observer.observe(s.el); });
})();
</script>
```

The `rootMargin` of `-10% 0px -80% 0px` triggers the active state when a section enters the top 10-20% of the viewport, which feels natural during scrolling.

### PDF Output

When a PDF is requested, generate it from the HTML source. The PDF should:
- Maintain the main content styling (typography, colors, cards, tables)
- Drop the sidebar navigation (it's not useful in print)
- Add proper page breaks between major sections
- Include the Kale wordmark and document date in the footer
- Use the `pdf` skill for generation mechanics

---

## Output Type 1b: MDX Pages for kale-wiki

New resources are created as MDX pages in the kale-wiki repo (`../kale-wiki`), deployed via Cloudflare Pages at `wiki.kaleacquisition.com`. This is the default path for all new resources — standalone HTML is legacy.

### How wiki pages differ from standalone HTML

| Aspect | Standalone HTML (legacy) | MDX in kale-wiki |
|--------|--------------------------|-------------------|
| Styling | Full CSS inlined in `<style>` tag | Shared styles from wiki layout — no CSS needed |
| Sidebar/TOC | Hand-coded `<nav class="sidebar">` with scroll-spy JS | Auto-generated by wiki from headings |
| Components | HTML classes (`.card`, `.compare`, `.flow-step`) | MDX components (`<Card>`, `<CompareBlock>`, `<FlowDiagram>`) |
| Logo/favicon | Base64-embedded in each file | Handled by wiki shell |
| Deployment | Individual Cloudflare Worker per resource | Cloudflare Pages — push to master auto-deploys |
| Preview | Worker URL (`[slug].roshan-31b.workers.dev`) | Cloudflare Pages branch preview |

### Frontmatter schema

Every MDX file starts with YAML frontmatter:

```yaml
---
title: "Page Title"
description: "One-line description for navigation and SEO"
visibility: public          # public | internal
sources: [Claude Code]      # where the content came from
updated: "YYYY-MM-DD"       # last updated date
order: 5                    # position within the section
---
```

### Section selection guide

The wiki has 6 sections. Choose based on content type:

| Section | Use for | Examples |
|---------|---------|----------|
| `company` | Identity, vision, strategy, culture | About page, strategy doc, team overview |
| `services` | Service offerings and delivery methods | Cold email playbook, deliverability services |
| `systems` | Tools, infrastructure, architecture | Kale OS, workspace guide, tech stack |
| `playbooks` | Step-by-step recurring workflows | Client onboarding SOP, inbox provisioning |
| `onboarding` | Getting started guides | New hire guide, client kickoff |
| `knowledge` | Learnings, reference material, insights | Deliverability deep-dives, automation patterns |

### Available MDX components

These are the components available in kale-wiki. Use them based on content type — never force a component where prose works better.

| Component | Use for | Example usage |
|-----------|---------|---------------|
| `<Callout>` | Critical context, source-of-truth declarations | `<Callout>This is the canonical reference for...</Callout>` |
| `<Alert>` | Warnings, info notices, tips | `<Alert type="warning">Do not skip this step</Alert>` |
| `<Card>` | Grouping related content | `<Card title="Phase 1">Content here</Card>` |
| `<Grid2>` | Side-by-side card layouts | `<Grid2><Card>Left</Card><Card>Right</Card></Grid2>` |
| `<CompareBlock>` | Right/wrong, before/after | `<CompareBlock left="Wrong" right="Right">...</CompareBlock>` |
| `<FlowDiagram>` | Sequential processes | `<FlowDiagram steps={[{title: "Step 1", desc: "..."}]} />` |
| `<TierDiagram>` | Hierarchical relationships | `<TierDiagram tiers={[...]} />` |
| `<Tree>` | File/directory structures | `<Tree>{...structure...}</Tree>` |
| `<PersonCard>` | Team member info | `<PersonCard name="..." role="...">Bio</PersonCard>` |
| `<IdeaCard>` | Idea/concept cards | `<IdeaCard title="..." priority="high">...</IdeaCard>` |

### MDX writing rules

1. **Use Markdown, not HTML**: Write headings as `##` not `<h2>`. Use `**bold**` not `<strong>`. MDX is Markdown-first.
2. **No `<style>` or `<script>` tags**: The wiki provides all styling. Never add custom CSS or JavaScript.
3. **Escape special characters**: `<` and `{` have meaning in MDX. Use `\<` and `\{` for literal characters in prose.
4. **Components are auto-available**: No import statements needed — all components listed above are globally registered.
5. **Headings become navigation**: `##` headings automatically appear in the wiki's sidebar TOC. Structure your `##` headings as the primary document outline.
6. **Keep frontmatter accurate**: The `updated` date should reflect the actual last edit. The `order` value determines position in section navigation.

### Content rules (same as HTML, adapted for MDX)

- Prose over bullets — default to paragraphs
- Sentence case for all headings
- Technical terms in backtick monospace
- Components used appropriately — don't force diagrams where prose works
- Every section has substantive content (no stubs)
- Cross-reference other wiki pages with relative links: `[Page Title](/section/slug)`

---

## Output Type 2: LinkedIn Content

LinkedIn content is **extracted from** the internal doc — never written independently. The internal doc contains the full story; the LinkedIn post compresses it to the single most transferable insight.

### The Operator's Diary Series

**Format**: `Operator's Diary #[n]` as the opening line, followed by the post.

**What it is**: Real-time documentation of building and running a business. Not retrospective case studies — dispatches from the middle of figuring things out.

**What it's not**: AI hype content, generic "productivity tips," or thought leadership that could have been written by anyone.

### Extraction Process

Given a completed internal doc, extract the LinkedIn post by:

1. **Identify the single most interesting insight** — the non-obvious thing you figured out that other operators/founders could apply.
2. **Strip all proprietary detail** — no client names, specific configs, internal tool names that aren't publicly known.
3. **Compress the narrative** — the internal doc might cover 10 things. The LinkedIn post covers one.
4. **Add the before/after arc** — what was broken, what changed, what's the takeaway.
5. **Close with pull, not push** — curiosity, an invitation, or a series signal.

### Voice & Tone (LinkedIn)

- **First person singular**: This is Roshan's voice. "I built," "we decided," "here's what I learned."
- **Conversational but substantive**: Write like you're telling a smart friend what happened. No corporate voice, no LinkedIn buzzwords.
- **Honest about what didn't work**: The most credible content acknowledges messiness.
- **De-emphasize tools, emphasize thinking**: Claude, Notion, Linear — these are means. The insight is about the system, the decision, or the mental model.

### Post Structure

```
Opening
├── Operator's Diary #[n]
├── Hook line (what happened — concrete, specific)
├── Reframe (why this matters beyond the surface)
│
Middle (the story)
├── Context/situation (what was broken or missing)
├── The shift (what changed — decision, system, realization)
├── How it works now (concrete details — what the system does)
│
Closing
├── The real insight (the non-obvious takeaway)
├── Punchline (one sharp line that lands the point)
└── Soft CTA or series signal ("Documenting more of these as I go")
```

### LinkedIn Writing Rules

1. **Hook in the first line**: Lead with a concrete outcome or surprising statement. Never "I've been thinking about..."
2. **Short paragraphs**: 1-3 sentences max. LinkedIn rewards white space.
3. **One idea per post**: Pick the single most interesting insight. Go deep on it.
4. **Concrete over abstract**: Numbers, tools, timeframes — be specific. "Built our project scoping system in under an hour" beats "Improved our processes."
5. **The insight must be transferable**: If the post only works because of Kale's specific context, it's internal doc material, not LinkedIn material.
6. **No emoji, no hashtag spam**: Clean text. At most 1-2 relevant hashtags at the very end.
7. **AI as a supporting character**: Mention Claude/AI naturally when relevant. Never make it the headline. Pattern: "I used [tool] to [do thing], but the real unlock was [insight]."
8. **End with pull, not push**: Close with curiosity or a simple "follow along" signal. The series format does the selling.

### Post Length

- **Target**: 150-250 words.
- **Max**: 350 words. Longer means you're covering too much — split it or move details to the internal doc.
- **Minimum**: 100 words.

### Topic Selection

Good topics share these traits:
- **You actually did the thing** — not hypothetical.
- **There's a non-obvious insight** — something that isn't common knowledge.
- **It's transferable** — other operators or founders could apply the same thinking.
- **It has a before/after** — something changed.

---

## Workflow: From Learning to Asset

### Step 1: Capture the raw learning

Sources include:
- Claude Code sessions (what you built, what worked, what didn't)
- Planning calls with Mike (Fireflies transcripts)
- Experiments with tools or processes
- Client problems that forced a new approach
- Conversations in this Claude project that produced useful frameworks

### Step 2: Build the internal doc

This is always the primary artifact. Choose the right format:

- **Full playbook-style page** (like the Team Playbook): For enduring knowledge that the whole team needs. Multiple sections, sidebar TOC, rich component usage. Reference docs maintained over time.
- **Focused knowledge doc**: For a specific learning, experiment result, or decision record. Shorter — maybe 2-4 sections. Still uses the full HTML template and brand styling, but doesn't need every component type.
- **Process/SOP doc**: For something the team will execute repeatedly. Heavy use of flow steps, checklists, and failure cards. Written for literal, step-by-step following.

### Step 3: Extract the LinkedIn post (if applicable)

Ask: **Would other operators/founders find the core insight useful?**

If yes — extract using the process above. If no — the learning stays internal. Not everything needs to be public content.

### Step 4: Cross-reference

- Internal docs should link to related docs and external tools.
- LinkedIn posts can reference that internal systems exist without revealing proprietary details.
- If a LinkedIn post generates good discussion, capture relevant external perspectives back into internal docs.

---

## Quality Checklist

### Internal HTML docs — before sharing:

- [ ] Kale logo favicon included (inline base64 from `_template/favicon-base64.txt`)?
- [ ] Built on the Kale brand system (CSS variables, fonts, color palette)?
- [ ] Page structure follows the shell (sidebar, hero, sections, footer)?
- [ ] Components used appropriately (not forcing diagrams where prose works)?
- [ ] Prose-first — not a bullet dump?
- [ ] Technical terms in monospace?
- [ ] Every section has substantive content (no stubs)?
- [ ] Section-number labels match sidebar TOC?
- [ ] Responsive (content readable if sidebar collapses on mobile)?
- [ ] Scroll-spy active sidebar highlighting included (IntersectionObserver script)?
- [ ] Would a new team member understand this without follow-up questions?

### LinkedIn posts — before publishing:

- [ ] Derived from an internal doc (not written independently)?
- [ ] First line makes someone stop scrolling?
- [ ] Exactly one core insight?
- [ ] AI mentioned naturally, not centered?
- [ ] Insight is transferable outside Kale?
- [ ] Under 250 words?
- [ ] Ending pulls rather than pushes?
- [ ] No emoji, no hashtag spam, no LinkedIn buzzwords?

---

## Anti-Patterns (Never Do These)

### Internal docs
- Notion-style formatting in HTML (the output is a styled HTML page, not a Notion doc)
- Generic/unstyled HTML (every doc uses the Kale brand system)
- Wall-of-bullets formatting (write in prose, use components for structure)
- Sections with just a title and no content
- Hardcoded colors instead of CSS variables
- Purple/blue gradients, neon status colors, or any off-brand styling
- Screenshots without context (always add a sentence explaining what to look at)
- Duplicating information that lives in another doc — link to it instead

### LinkedIn
- Writing the LinkedIn post first (always internal doc first)
- Starting with "I've been thinking about..."
- Making AI the hero of the story
- Vague claims without specifics
- Hashtag walls
- Asking for engagement ("Like if you agree!")
- Posts that only work with Kale-specific context
- Publishing learnings externally before documenting them internally
