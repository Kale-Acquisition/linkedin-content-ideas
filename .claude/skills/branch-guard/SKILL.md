---
name: branch-guard
description: >
  Enforce feature branch workflow. MUST activate BEFORE making any code changes
  (creating files, editing source code, writing scripts, modifying configs) when the
  current git branch is master or main. Applies to: implementing plans, fixing bugs,
  adding features, refactoring, or any task that modifies source code or project files.
  Does NOT apply to documentation-only edits in kale-workspace (plans/, outputs/,
  knowledge/, context/, resources/).
---

# Branch Guard

Enforce feature branches for all implementation work. Never commit code changes directly to `master` or `main`.

## Procedure

Run this check BEFORE any file creation or modification that constitutes implementation work.

### 1. Check if branching applies

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

If not a git repo, skip entirely.

```bash
git branch --show-current
```

If the current branch is NOT `master` or `main`, you are already on a feature branch — skip and continue working.

### 2. Determine branch name

**From a plan file** (e.g., during `/implement`):
- Extract slug from plan path: `plans/YYYY-MM-DD-<slug>.md` → `feature/<slug>`
- Example: `plans/2026-03-23-add-competitor-analysis.md` → `feature/add-competitor-analysis`

**From an ad-hoc request** (no plan file):
- Format: `feature/YYYY-MM-DD-<short-kebab-description>`
- Example: "add health check endpoint" → `feature/2026-03-23-health-check-endpoint`
- Keep the slug under 50 characters.

### 3. Create the branch

```bash
# Stash uncommitted changes if present
git stash --include-untracked 2>/dev/null

# Create and switch to the feature branch (or check it out if it exists)
git checkout -b feature/<slug> 2>/dev/null || git checkout feature/<slug>

# Restore stashed changes
git stash pop 2>/dev/null
```

If `git stash pop` reports conflicts, alert the user immediately before proceeding.

### 4. Confirm

Report to the user:

> Created branch `feature/<slug>` from `master`. All changes will be made here.

or if the branch already existed:

> Switched to existing branch `feature/<slug>`. Continuing work here.

### 5. Block until confirmed

Do NOT create, edit, or write any files until the feature branch is confirmed active. This is a hard gate.
