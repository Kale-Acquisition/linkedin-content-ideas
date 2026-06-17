# Sync From Workspace

Pull the latest company context from kale-workspace into this project repo — commands, skills, strategy, business info — without touching project-specific files.

## Variables

workspace_path: $ARGUMENTS (optional — path to kale-workspace repo, defaults to `../kale-workspace`)

---

## Instructions

### Step 1: Resolve the workspace path

If `$ARGUMENTS` is provided, use it as the workspace path. Otherwise use `../kale-workspace`.

### Step 2: Run the sync script

Run:
```
python scripts/sync-from-workspace.py <workspace_path>
```

Report the output — which directories and files were copied, which were skipped, which are protected.

If the script errors (workspace not found, not a git repo, syncing into itself), stop and tell the user what went wrong.

### Step 3: Guide the review

After a successful sync, tell the user:

1. **Review what changed:**
   ```
   git diff
   git status
   ```

2. **If the changes look right, commit and push:**
   ```
   git add -A
   git commit -m "chore: sync company context from kale-workspace"
   git push
   ```

### Step 4: Remind about what was not touched

Note that project-specific files were protected and not overwritten:
- `CLAUDE.md` — your project-specific config
- `context/project-info.md`
- `context/project-goals.md`
- `context/current-state.md`

These are yours to maintain. Only company-wide context (strategy, business info, commands, skills) was updated.
