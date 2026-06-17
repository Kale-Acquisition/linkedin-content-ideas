# kale-template Repository Structure

> This document describes what the `kale-template` GitHub repo should contain and which files are maintained by kale-workspace via `scripts/sync-to-template.py`.

`kale-template` is a GitHub Template Repository — team members click "Use this template" to create new project repos. It provides real company-wide context, shared skills, and empty structure from day one.

---

## Sync Contract

Files marked **SYNCED** are maintained by kale-workspace and should never be edited directly in kale-template (they will be overwritten on next sync). Files marked **TEMPLATE-ONLY** live only in kale-template and must be maintained there directly.

```
kale-template/
├── CLAUDE.md                          [TEMPLATE-ONLY] — skeleton with [PROJECT] placeholders
├── .mcp.json                          [SYNCED] — same MCP server config as workspace
├── MCP_SETUP.md                       [SYNCED] — env var setup instructions
├── .gitignore                         [TEMPLATE-ONLY] — sensible defaults
├── .claude/
│   └── commands/                      [SYNCED] — portable commands only (workspace-only excluded)
│   └── skills/                        [SYNCED] — all skills from kale-workspace
├── context/
│   ├── business-info.md               [SYNCED] — real Kale company context
│   ├── strategy.md                    [SYNCED] — real current strategy
│   ├── team.md                        [SYNCED] — team roles (Arra, Azhar, Pandush, Beverly, Umer)
│   ├── clients.md                     [SYNCED] — active client roster
│   ├── project-info.md                [TEMPLATE-ONLY] — empty shell, fill in per project
│   ├── project-goals.md               [TEMPLATE-ONLY] — empty shell, fill in per project
│   └── current-state.md               [TEMPLATE-ONLY] — empty shell, fill in per project
├── knowledge/                         [TEMPLATE-ONLY] — empty structure only (no contents)
├── automations/                       [TEMPLATE-ONLY] — empty structure only
├── plans/                             [TEMPLATE-ONLY] — empty
├── outputs/                           [TEMPLATE-ONLY] — empty
├── .github/
│   └── CODEOWNERS                     [SYNCED — generated] — per-repo, from access-policy.yaml
├── scripts/
│   └── sync-from-workspace.py         [SYNCED] — pull workspace updates into this project repo
└── reference/                         [SYNCED] — reference docs from kale-workspace
```

---

## Template-Only Files to Create Manually

These files do not exist in kale-workspace and must be created/maintained in kale-template directly:

### `CLAUDE.md` (skeleton)

A project-focused CLAUDE.md with `[PROJECT]` placeholders where project-specific content goes. Should reference the three-tier system and explain that it's a project repo (Tier 3), not the shared workspace.

Key sections:
- What This Is — `[PROJECT NAME]`, what it does, link to kale-workspace for team context
- Workspace Structure — same structure as kale-workspace but project-specific
- Context Files — explain `project-info.md`, `project-goals.md`, `current-state.md`
- Commands — same commands as workspace (they're synced)
- Current Focus — `[Fill in what you're actively building]`

### `context/project-info.md` (empty shell)

```markdown
# Project Info

> Fill in: what this project is, why it exists, tech stack, key decisions.

## Overview
[What this project does and why it exists]

## Tech Stack
[Languages, frameworks, key dependencies]

## Client(s)

[Which client(s) this project serves. Use "Internal" for internal tools, "All" for cross-client tools, or name specific clients from context/clients.md.]

- **Client:** [Client Name]
- **Scope:** [What this project does for this client]

## Key Architectural Decisions
[Important choices made and why]

## Repo Structure
[Key directories and what they contain]
```

### `context/project-goals.md` (empty shell)

```markdown
# Project Goals

> Fill in: what success looks like, milestones, current priorities.

## Goal
[One-sentence mission for this project]

## Success Criteria
[How you'll know it's working]

## Current Milestones
[What you're working toward right now]
```

### `context/current-state.md` (empty shell)

```markdown
# Current State

> Update frequently. What's working, what's broken, what's in progress.

## Status
[Overall project status]

## What's Working
[Completed and stable]

## In Progress
[Actively being built]

## Blockers
[What's blocking progress]

## Next Steps
[Immediate priorities]
```

---

## GitHub Template Setup

1. Create the `kale-template` repo on GitHub
2. Go to **Settings → General → Template repository** → enable the checkbox
3. The repo will show a "Use this template" button — this is how team members create new project repos
4. Run `python scripts/sync-to-template.py ../kale-template` from kale-workspace to populate synced files

---

## How Syncing Works

1. Edit commands, skills, reference docs, or context files in **kale-workspace**
2. Run `python scripts/sync-to-template.py ../kale-template` to push updates to template
3. Review changes with `git diff` in kale-template, then commit and push
4. New project repos created after this point will get the updated files automatically
5. Existing project repos are **not updated** — they are one-time snapshots from "Use this template"

The sync is **one-way** (workspace → template) and **manual** (you decide when to sync). There is no automatic or live sync.

---

## What Stays in kale-workspace Only

These files are never synced to the template:

| File/Dir | Reason |
|---|---|
| `context/roshan.md` | Personal to Roshan (founder) |
| `context/mike.md` | Personal to Mike (founder) |
| `context/current-data.md` | Live workspace metrics, too specific |
| `knowledge/` contents | Accumulated workspace knowledge |
| `automations/` contents | Workspace-specific tools and scripts |
| `plans/` contents | Workspace work products |
| `outputs/` contents | Workspace work products |
| `scripts/sync-to-template.py` | Only meaningful in kale-workspace |
| Workspace-only commands | `generate-automation-ideas`, `inbox-order`, `create-resource`, `release-resource`, `sync-template` |
