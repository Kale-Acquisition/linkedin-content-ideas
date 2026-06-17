---
name: explain-changes
description: >
  Explain accumulated working-tree changes in business-impact terms and recommend
  what to do with them. Invoke with /explain-changes (or when the user asks "what
  changed?", "what's in my working tree?", "explain these changes", "what are all
  these untracked files?"). Groups changes by impact, separates shippable work from
  throwaway scratch, and recommends commit / cleanup / risk actions. Explains and
  recommends only — never stages, commits, or deletes on its own.
---

# Explain Changes

Give the operator a fast, impact-first read on everything sitting in the working tree, then tell them what to do with it. Most of these scripts and edits accumulate during long operational sessions; this skill makes the pile legible before a commit or branch merge.

## When this fires

Manually, via `/explain-changes`, or when the user asks what's changed / what the untracked files are. It is read-and-advise only. Do **not** stage, commit, push, or delete anything — recommend those actions and let the operator decide.

## Procedure

### 1. Confirm git context

```bash
git rev-parse --is-inside-work-tree   # bail with a plain note if not a repo
git branch --show-current
```

Report the current branch up front. If on `master`/`main`, flag that any shippable code should move to a feature branch (see the branch-guard skill) — but still explain the changes.

### 2. Gather the full picture

```bash
git status --short                    # tracked mods + untracked, machine-readable
git diff --stat                       # size of unstaged tracked changes
git diff --stat --cached              # size of staged changes (if any)
```

For each **modified tracked file**, read enough of `git diff <file>` to state what the change *does* — not just that it changed. For **untracked files**, read the first ~30 lines to classify intent (real source vs. scratch probe vs. generated output).

### 3. Classify every change into one of three buckets

| Bucket | What belongs here | Signal |
|---|---|---|
| **Shippable** | Code/config/connector changes and new source meant to merge | Tracked file edits under `src/`, `clients/`, real new modules; `scripts/*.ts` that are reusable tooling |
| **Durable artifacts** | Things that commit but aren't code | `iteration-log/entries/*.json`, `outputs/`, `docs/`, `knowledge/`, `plans/` |
| **Throwaway / scratch** | One-off ops & investigation scripts | `_`-prefixed files, `fire_*.mjs`, ad-hoc `.mjs` probes, anything that hardcodes a campaign/pull id or is obviously single-use |

The `_`-prefix is the house convention for "scratch, delete me." Treat `_*.mjs` and one-off `fire_*` / `_probe_*` / `_check_*` scripts as throwaway unless their content says otherwise.

### 4. Explain — grouped by impact, not by file

Follow Roshan's global business-impact framing:

- Lead each shippable change with **what it means for the pipeline / client / campaign**, one line each. (e.g. "Instantly pushes stop dropping leads under rate-limit bursts" — not "added fetchWithRetry with 429 backoff".)
- **Group by impact** (what got faster / safer / new / fixed), not file-by-file.
- Keep implementation detail to one compressed line per change.
- Minimize code blocks — a scannable table or bullets beats a diff dump.

### 5. Recommend actions

After the explanation, give a short, scannable action list:

- **Commit** — which shippable changes belong together as logical commit(s), with a suggested subject line. Respect the active feature branch; never recommend committing to `master`/`main` directly.
- **Clean up** — which throwaway scripts to delete or `.gitignore` before the branch merges. List them explicitly.
- **Risks / do-not-commit** — call out anything dangerous to commit, especially:
  - **Hardcoded secrets** (API keys, bearer tokens, service-role keys) in scratch scripts — scan untracked `.mjs`/`.ts` for key-shaped strings and flag the file. This is the most common footgun in ops scripts.
  - Files that don't match their described purpose, or large generated blobs.
- **Branch note** — if shippable changes are unrelated to the current feature branch's purpose, say so and suggest splitting them out.

### 6. Stop

End with the recommendations. Do not act on them. If the operator says "commit the shippable set" or "clean up the scratch," then proceed — honoring the no-auto-delete-branch rule and feature-branch hygiene.

## Output shape

1. One line: current branch + headline count ("11 untracked, 3 modified, on `feature/…`").
2. **Shippable** — grouped by impact.
3. **Durable artifacts** — one line.
4. **Throwaway** — listed, marked for cleanup.
5. **Recommended actions** — commit / clean up / risks, scannable.

Keep the whole thing tight. The point is to make a messy working tree legible in ~20 seconds, then hand the operator clear next steps.
