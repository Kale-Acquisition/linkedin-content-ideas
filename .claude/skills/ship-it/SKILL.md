---
name: ship-it
description: >
  Push the current feature branch, open a PR, and merge it — the "push PR merge" combo.
  Use when the user says "push pr merge", "ship it", "push and merge", "ship this branch",
  or otherwise asks to take committed work on a feature branch all the way to the default
  branch in one step. Encodes Roshan's git hygiene: NEVER deletes the branch on merge.
  Does NOT apply when on master/main with no feature branch to ship.
---

# Ship It

Take the current feature branch from local commits → pushed → PR → merged into the default branch, in one flow. Mirrors the manual `git push` + `gh pr create` + `gh pr merge` combo.

## Hard rules

- **Never pass `--delete-branch`** to `gh pr merge`. Never `git push origin --delete`. Branches stay after merge (Roshan's archive-over-cleanup preference).
- **Never skip hooks or signing** (`--no-verify`, `--no-gpg-sign`) unless the user explicitly asks.
- Use `gh` for all GitHub operations.

## Procedure

### 1. Preflight

```bash
git rev-parse --is-inside-work-tree 2>/dev/null || { echo "not a git repo"; exit 1; }
BRANCH=$(git branch --show-current)
DEFAULT=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
```

- If `BRANCH` is the default branch (`master`/`main`) or empty: **stop**. There's no feature branch to ship. Tell the user — they likely need to branch and commit first.

### 2. Commit any pending work

```bash
git status --short
```

- If the working tree is clean → continue.
- If there are uncommitted changes: these are presumably the work to ship. Stage and commit them with a clear message summarizing the change. End the message with the Co-Authored-By trailer the environment specifies. Confirm the message with the user only if the intent is ambiguous.

### 3. Push

```bash
git push -u origin "$BRANCH"
```

### 4. Open the PR (or reuse an existing one)

```bash
gh pr view "$BRANCH" --json number -q .number 2>/dev/null
```

- If a PR already exists for the branch, reuse its number — skip creation.
- Otherwise create it. Derive a concise title from the branch name / commit subjects. Write a short body: **What** (1–3 bullets) and **Validation** (how it was checked). End the body with:
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

```bash
gh pr create --base "$DEFAULT" --head "$BRANCH" --title "<title>" --body "<body>"
```

Capture the PR number from the returned URL.

### 5. Merge

```bash
gh pr merge <N> --merge --admin
```

- Default to `--merge` (merge commit), matching Roshan's pattern. Use `--squash` only if the user asks.
- `--admin` bypasses required checks where the user has rights; drop it if the user wants checks enforced.
- **No `--delete-branch`.**

### 6. Sync local default branch

```bash
git checkout "$DEFAULT"
git pull --ff-only
```

### 7. Report

Tell the user: PR URL, merge confirmation, that the branch was preserved, and that local `$DEFAULT` is synced. Note if any step needed a fallback (e.g. PR already existed, checks bypassed).

## Failure handling

- **Push rejected (non-fast-forward):** the remote branch moved. Surface it — don't force-push unless the user explicitly asks.
- **Merge blocked (conflicts / failing required checks):** report the blocker. Don't bypass checks beyond the agreed `--admin`. Conflicts need resolving on the branch first.
- **`gh` not authenticated:** suggest the user run `! gh auth login` in the session.
