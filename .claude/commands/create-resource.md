# /create-resource

> Create a Kale knowledge resource — MDX page in kale-wiki, deployed via Cloudflare Pages.

**Usage:** `/create-resource [topic-or-doc-path]`

**Examples:**
- `/create-resource cold email deliverability` — create from a topic
- `/create-resource knowledge/deliverability/inbox-placement.md` — create from an existing knowledge doc
- `/create-resource` — start a blank resource with a discussion

---

## Step 1: Parse Input

Parse `$ARGUMENTS` to determine the resource source:

- **Topic name** (e.g., "cold email deliverability") — Claude will research `knowledge/` and discuss the resource with the user
- **File path** (e.g., `knowledge/deliverability/inbox-placement.md`) — Claude reads the file as source material
- **Empty** — Claude asks the user what they want to create

If a file path is provided, read it. If a topic is provided, search `knowledge/` for relevant docs using Grep/Glob.

## Step 2: Generate Slug and Choose Section

Convert the topic/title into a URL-safe slug:
- Lowercase, hyphen-separated
- No special characters
- Short but descriptive (e.g., "cold-email-deliverability", "inbox-provisioning")

Ask which wiki section to target. The 6 sections are:

| Section | Use for |
|---------|---------|
| `company` | Who we are, where we're headed, how we think |
| `services` | What we deliver and how we deliver it |
| `systems` | Tools and infrastructure powering Kale |
| `playbooks` | Step-by-step guides for recurring workflows |
| `onboarding` | Getting started at Kale — for team and clients |
| `knowledge` | Accumulated learnings and institutional knowledge |

Confirm with the user: "I'll create `content/[section]/[slug].mdx` — the page will live at `wiki.kaleacquisition.com/[section]/[slug]`. Good?"

## Step 3: Create Branch in kale-wiki

Create a git branch in the kale-wiki repo:

```bash
cd ../kale-wiki && git checkout -b resource/[slug]
```

## Step 4: Discuss the Resource

Read `.claude/skills/kale-content/SKILL.md` for content guidance.

Shape the resource with the user by discussing:
1. **Core insight / purpose** — What's the one thing this resource makes clear?
2. **Audience** — Team-wide, technical, or process-focused?
3. **Doc type** — Playbook (multi-section), focused knowledge doc (2-4 sections), or process/SOP (step-by-step)?
4. **Key components** — Which MDX components are needed?

Available MDX components in kale-wiki:
- `<Callout>` — critical context, source-of-truth declarations
- `<Alert>` — warnings, info notices
- `<Card>` — grouping related content
- `<Grid2>` — side-by-side card layouts
- `<CompareBlock>` — right/wrong, before/after comparisons
- `<FlowDiagram>` — sequential processes, workflows
- `<TierDiagram>` — hierarchical relationships
- `<Tree>` — file/directory structures
- `<PersonCard>` — team member info
- `<IdeaCard>` — idea/concept cards

Keep this discussion brief and natural. If the source material is clear enough, propose answers and let the user confirm rather than asking open-ended questions.

## Step 5: Generate MDX

Create the file at `../kale-wiki/content/[section]/[slug].mdx`.

### Frontmatter

Every MDX file starts with YAML frontmatter:

```yaml
---
title: "[Resource Title]"
description: "[One-line description]"
visibility: public
sources: [Claude Code]
updated: "[YYYY-MM-DD]"
order: [number]
---
```

For the `order` value, check existing pages in the target section and pick a number that places the new page appropriately (usually at the end).

### Content structure

Write the content using MDX:
- Use Markdown headings (`##`, `###`) for sections
- Use the available MDX components where appropriate
- Follow the content quality standards from `.claude/skills/kale-content/SKILL.md`

### Content rules (from the skill)
- Prose over bullets — default to paragraphs
- Sentence case for all headings
- Technical terms in monospace backticks
- Components used appropriately — don't force diagrams where prose works
- Every section has substantive content (no stubs)

### Key differences from standalone HTML
- No inlined CSS — the wiki provides shared styles via its layout
- No sidebar TOC markup — the wiki generates navigation automatically
- No `<style>` tags, no `<script>` tags — pure MDX content
- No favicon or logo embedding — handled by the wiki shell
- Components are MDX imports, not HTML classes

## Step 6: Build and Verify

Run the wiki build to catch any MDX errors:

```bash
cd ../kale-wiki && npm run build
```

If the build fails, fix the MDX syntax and rebuild. Common issues:
- Unescaped `<` or `{` characters (must use `\<` or `\{` in MDX)
- Missing component imports (components are auto-available, but check usage)
- Invalid frontmatter YAML

## Step 7: Push Branch and Open Draft PR

Push the branch and open a draft PR to guarantee a Cloudflare Pages preview deploy:

```bash
cd ../kale-wiki && git add content/[section]/[slug].mdx && git commit -m "draft: [slug] resource" && git push -u origin resource/[slug]
```

Then open a draft pull request in kale-wiki:

```bash
cd ../kale-wiki && gh pr create --draft --title "Resource: [Title]" --body "Draft resource — iterating via /create-resource in kale-workspace."
```

Cloudflare Pages builds a preview deploy for every PR. The preview URL will appear in the PR's deployment status checks. Check for it with:

```bash
cd ../kale-wiki && gh pr view --json url --jq '.url'
```

The user can also find the preview URL in the GitHub PR page (under "Deployments") or in the Cloudflare Pages dashboard.

## Step 8: Summary

Present the result:

```
## Resource Created: [Title]

| Detail | Value |
|--------|-------|
| Slug | [slug] |
| Section | [section] |
| Branch | resource/[slug] |
| File | content/[section]/[slug].mdx |
| PR | [GitHub PR URL] |
| Preview | Check PR deployment status or Cloudflare Pages dashboard |
| Production URL | wiki.kaleacquisition.com/[section]/[slug] (after merge) |
| Status | Draft |

**Next steps:**
- Check the Cloudflare Pages preview deploy (linked in the PR) to review
- Give feedback in chat — I'll edit, rebuild, and push
- Run `/release-resource [slug]` when ready to finalize
```

---

## Iteration (Between Create and Release)

No special command needed. The user reviews the preview and gives feedback in natural conversation:

- "Make the intro shorter"
- "Add a troubleshooting section"
- "Use a CompareBlock for the before/after"

For each iteration:

1. Edit `../kale-wiki/content/[section]/[slug].mdx` with the requested changes
2. Build to verify: `cd ../kale-wiki && npm run build`
3. Commit and push to update the preview: `cd ../kale-wiki && git add -A && git commit -m "update: [slug] — [change summary]" && git push`
4. Tell the user the preview will update shortly

Keep iterations fast — edit, build, push, confirm.
