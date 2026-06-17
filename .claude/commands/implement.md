# Implement

Execute an implementation plan created by `/create-plan`. Read the plan thoroughly, execute each step in order, and report on the completed work.

## Variables

plan_path: $ARGUMENTS (path to the plan file, e.g., `plans/2026-01-28-add-guest-research-command.md`)

---

## Instructions

### Phase 0: Branch Guard

Before making any changes, ensure you are on a feature branch — never implement directly on `master` or `main`.

1. **Check if this is a git repo:**
   ```bash
   git rev-parse --is-inside-work-tree 2>/dev/null
   ```
   If not a git repo, skip to Phase 1.

2. **Check the current branch:**
   ```bash
   git branch --show-current
   ```
   - If already on a branch other than `master` or `main`, report it and proceed to Phase 1.
   - If on `master` or `main`, continue to step 3.

3. **Create a feature branch from the plan path:**
   - Extract the slug: strip `plans/`, the `YYYY-MM-DD-` date prefix, and `.md` suffix.
   - Example: `plans/2026-03-23-add-competitor-analysis.md` → `feature/add-competitor-analysis`
   ```bash
   # Stash any uncommitted changes
   git stash --include-untracked 2>/dev/null
   # Create the feature branch
   git checkout -b feature/<slug>
   # Restore stashed changes
   git stash pop 2>/dev/null
   ```
   If `git stash pop` reports conflicts, stop and alert the user.

4. **Report the branch:**
   > Created branch `feature/<slug>` from `master`. All implementation changes will be made here.

**Do not proceed to Phase 1 until the feature branch is confirmed active.**

---

### Phase 1: Understand the Plan

1. **Read the plan file completely.** Do not skim — understand every section.
2. **Verify prerequisites:**
   - Are there open questions that need answers before proceeding?
   - Are there dependencies on external resources or user decisions?
   - If blockers exist, stop and ask the user before proceeding.
3. **Confirm the plan is ready:**
   - Status should be "Draft" or "Ready"
   - All sections should be filled out (no placeholder text remaining)

---

### Phase 2: Execute the Plan

1. **Follow the Step-by-Step Tasks in exact order.**
   - Complete each step fully before moving to the next
   - If a step involves creating a file, write the complete file — not a stub
   - If a step involves modifying a file, read the file first, then apply changes precisely

2. **For each task:**
   - Read any files that will be affected
   - Make the changes specified
   - Verify the change is correct before proceeding

3. **Handle issues gracefully:**
   - If a step can't be completed as written, note the issue and adapt if the intent is clear
   - If you're unsure how to proceed, ask the user rather than guessing
   - Document any deviations from the plan

---

### Phase 3: Validate

1. **Run through the Validation Checklist** from the plan
   - Check off each item
   - Note any that fail

2. **Verify Success Criteria** are met
   - Confirm each criterion is satisfied
   - Note any gaps

3. **Check cross-references and consistency:**
   - Ensure new files are referenced where they should be
   - Verify CLAUDE.md is updated if workspace structure changed
   - Confirm naming conventions are followed

---

### Phase 4: Update Plan Status

After implementation, update the plan file:

1. Change `**Status:** Draft` to `**Status:** Implemented`
2. Add an Implementation Notes section at the end:

```markdown
---

## Implementation Notes

**Implemented:** <YYYY-MM-DD>

### Summary

<Brief summary of what was done>

### Deviations from Plan

<List any changes made during implementation, or "None">

### Issues Encountered

<List any problems hit and how they were resolved, or "None">
```

---

## Quality Standards

- **Thoroughness:** Every step in the plan is executed, not skipped
- **Precision:** Changes match what the plan specifies
- **Completeness:** Files are fully written, not stubbed out
- **Consistency:** All cross-references and documentation updated
- **Traceability:** Deviations are documented

---

## Report

After implementation, provide:

1. **Summary:** Bulleted list of work completed
2. **Files changed:** List all files created, modified, or deleted
3. **Validation results:** Status of each checklist item
4. **Deviations:** Any changes from the original plan
5. **Next steps:** Any follow-up actions needed (if applicable)

Format:

```
## Implementation Complete

### Summary
- <What was done>
- <What was done>

### Files Changed
**Created:**
- `path/to/new-file.md`

**Modified:**
- `path/to/modified-file.md`

**Deleted:**
- (none)

### Validation
- [x] <Passed check>
- [x] <Passed check>

### Deviations from Plan
<None, or list deviations>

### Plan Status
Updated `plans/YYYY-MM-DD-{name}.md` status to "Implemented"
```
