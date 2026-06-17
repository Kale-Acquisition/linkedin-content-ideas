# Sync Template

Sync portable files from kale-workspace to kale-template, then guide you through reviewing and committing the changes.

## Variables

template_path: $ARGUMENTS (optional — path to kale-template repo, defaults to `../kale-template`)

---

## Instructions

### Step 1: Resolve the target path

If `$ARGUMENTS` is provided, use it as the template path. Otherwise use `../kale-template`.

### Step 2: Run the sync script

Run:
```
python scripts/sync-to-template.py <template_path>
```

Report the output — which directories and files were copied, which were skipped.

If the script errors (target not found, not a git repo), stop and tell the user what went wrong.

### Step 3: Guide the review

After a successful sync, tell the user:

1. **Navigate to kale-template:**
   ```
   cd <template_path>
   ```

2. **Review what changed:**
   ```
   git diff
   git status
   ```

3. **If the changes look right, commit and push:**
   ```
   git add -A
   git commit -m "Sync from kale-workspace — <brief description of what changed>"
   git push
   ```

### Step 4: Remind about existing project repos

Note that this sync updates kale-template only. Any project repos already created from the template (Tier 3) are **independent snapshots** — they won't receive these updates automatically. If a new command or skill is important enough, copy it into existing project repos manually.
