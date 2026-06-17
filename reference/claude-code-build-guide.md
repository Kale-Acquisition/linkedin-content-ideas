# Building Systems with Claude Code

A practical guide for Kale's team on how to effectively build software systems using Claude Code.

> **This guide describes the principles behind the [Claude Workspace Template](claude-workspace-template/).** The template automates the build loop below with slash commands (`/prime`, `/create-plan`, `/implement`), but the process is still collaborative — Claude proposes, you decide. The commands handle the scaffolding, not the thinking.

---

## The Core Problem

Claude Code has no memory between sessions. Every time you start a new conversation, it's a blank slate. This means:

- It doesn't know your codebase
- It doesn't know your conventions
- It doesn't know what you built yesterday

**The solution:** A workspace template with persistent context files, slash commands, and a structured build loop that loads Claude Code with everything it needs to be effective.

---

## The Build Loop

Every successful build follows this pattern:

```
1. Context Loading (/prime) → 2. Planning (/create-plan) → 3. Execution (/implement) → 4. Verification
```

Most failed builds happen because people skip to step 3. Don't do that.

---

## Step 1: Context Loading — `/prime`

Before Claude Code writes any code, it needs to understand your project. Run `/prime` at the start of every session. It reads your core files and confirms understanding before any work begins.

### CLAUDE.md (Required)

This file lives in your project root. It's the first thing Claude Code reads and should give it the full picture. The workspace template includes a CLAUDE.md that documents the workspace structure, available commands, and session workflow.

**What to include:**

```markdown
# Project Name

## Overview
One paragraph explaining what this project is and why it exists.

## Workspace Structure
(The template provides this — document any customizations here)

## Commands
- `/prime` — Load context and start session
- `/create-plan` — Create an implementation plan
- `/implement` — Execute a plan
- `/kale-frontend` — Kale brand design system skill (example skill)

## Important Context
- We use the kale-frontend skill for all UI work (see .claude/commands/kale-frontend.md)
- All API calls go through /src/api/client.ts
- We follow [specific pattern] for state management

## Current Focus
[What you're actively building — update this frequently]
```

### The `context/` Directory

The workspace template uses a `context/` directory for background information that Claude reads during `/prime`. This is where you put:

| File | Purpose |
|------|---------|
| `context/roshan.md` | Who you are, your role, your working style |
| `context/business-info.md` | Company context, domain knowledge |
| `context/strategy.md` | Current priorities, goals, strategic direction |
| `context/current-data.md` | Live data, metrics, or state that changes frequently |

This replaces the manual approach of re-explaining context every session. `/prime` reads these files automatically and confirms understanding before starting.

### Skills (`.claude/commands/`)

Skills are detailed instruction sets for specific domains. They live as `.md` files in `.claude/commands/` and are invoked as slash commands (e.g., `/kale-frontend`).

**Good candidates for skills:**
- Design systems (colors, typography, components)
- API patterns your team uses
- Testing conventions
- Domain-specific logic

**Skill location:**
```
.claude/
  commands/
    kale-frontend.md   # Invoked via /kale-frontend
    my-skill.md        # Invoked via /my-skill
```

**Example:** Our `kale-frontend` skill contains all brand colors, typography rules, component patterns, and anti-patterns. When Claude Code reads it, every UI it builds automatically follows our design system. You invoke it with `/kale-frontend` — no need to manually tell Claude to read a file.

---

## Step 2: Planning — `/create-plan`

**This is the most underrated step.** Before any code gets written, create a plan.

### Why Planning Matters

1. Reveals gaps in your thinking before you've invested build time
2. Creates a checkpoint — if the plan looks wrong, stop and fix it
3. Gives Claude Code clear scope so it doesn't build things you didn't ask for
4. Makes it easy to resume if you hit context limits or need to split across sessions

### Using `/create-plan`

Instead of manually writing plan documents, use the `/create-plan` command:

```
/create-plan add a competitor analysis command
```

Claude will research the workspace, understand existing patterns, and produce a thorough plan document saved to `plans/` with a dated filename (e.g., `plans/2026-02-12-competitor-analysis-command.md`).

### Plan Output

The generated plan includes:
- **Overview** — what the plan accomplishes and why it matters
- **Current state** — relevant existing structure and gaps being addressed
- **Proposed changes** — new files, modified files, with full detail
- **Design decisions** — key choices and rationale
- **Step-by-step tasks** — detailed enough for `/implement` to execute without ambiguity
- **Validation checklist** — how to verify the implementation is complete
- **Success criteria** — measurable outcomes

### The Critical Step: Review the Plan

`/create-plan` produces a **draft**. Before executing:

1. **Read the plan** — does it capture what you actually want?
2. **Edit it** — add, remove, or refine steps. It's a markdown file in `plans/`, just open and edit.
3. **Resolve open questions** — the plan may flag decisions it needs from you.
4. **Only then:** run `/implement` to execute it.

The plan is your blueprint. Time spent refining it saves multiples in execution.

---

## Step 3: Execution — `/implement`

### Running the Plan

Once the plan is reviewed and ready, execute it:

```
/implement plans/2026-02-12-competitor-analysis-command.md
```

Claude reads the plan thoroughly, verifies prerequisites and blockers, then executes each step in order. If it encounters issues, it adapts when the intent is clear or asks you when it's uncertain.

### Work in Vertical Slices

**Wrong approach:**
1. Build all the components
2. Build all the API endpoints
3. Build all the tests
4. Wire everything together
5. Discover nothing works together

**Right approach:**
1. Build one complete feature end-to-end
2. Verify it works
3. Move to the next feature

### Checkpoint and Course-Correct

`/implement` follows the plan, but you should monitor progress and intervene when needed:

- **Check intermediate output** — don't wait until the end to review
- **Course-correct early** — if something looks off, stop and redirect
- **Use `outputs/` for deliverables** — work products go in the `outputs/` directory so they persist across sessions

### Use the Filesystem as Memory

Instead of keeping state in conversation, write it to files:

| Instead of... | Do this... |
|---------------|------------|
| "Remember we need to add X later" | Add a task to the plan or create a follow-up plan |
| "We decided to use Y approach" | It's captured in the plan's Design Decisions section |
| "The current status is Z" | The plan's status field tracks this (`Draft` → `Implemented`) |

Context files in `context/`, plans in `plans/`, and outputs in `outputs/` — everything survives across sessions.

---

## Step 4: Verification

### Built-In Validation

`/implement` has a built-in validation phase. After executing all steps, it:

1. Runs through the plan's **Validation Checklist**
2. Verifies **Success Criteria** are met
3. Checks cross-references and consistency (including CLAUDE.md updates)
4. Updates the plan status to "Implemented" with notes on any deviations

### Don't Stop at "Implemented"

Even with built-in validation, always verify yourself:

- **Run the code** — Does it actually execute?
- **Check the files** — Were they created where expected?
- **Test the behavior** — Does it do what you asked?
- **Check edge cases** — What happens with bad input?

### Build Verification Into the Plan

Your plan's success criteria should be testable:

**Weak:** "Dashboard is built"

**Strong:** "I can run `npm start`, navigate to /dashboard, and see client health data populated from the API"

---

## Workspace Structure

The workspace template provides this structure out of the box:

```
workspace/
├── CLAUDE.md                  # Entry point — Claude reads this first, always loaded
├── .claude/
│   └── commands/              # Slash commands and skills
│       ├── prime.md           # /prime — session initialization
│       ├── create-plan.md     # /create-plan — create implementation plans
│       ├── implement.md       # /implement — execute plans
│       └── kale-frontend.md   # /kale-frontend — design system skill (example)
├── context/                   # Background context, read by /prime
│   ├── roshan.md              # Who you are, your role
│   ├── business-info.md       # Company context, domain knowledge
│   ├── strategy.md            # Current priorities and goals
│   └── current-data.md        # Live data and metrics
├── plans/                     # Implementation plans from /create-plan
├── outputs/                   # Work products and deliverables
├── reference/                 # Templates, examples, reusable patterns
└── scripts/                   # Automation scripts (if applicable)
```

---

## Common Failure Modes

### 1. Context Starvation
**Symptom:** Claude Code invents patterns that don't match your codebase.
**Cause:** It didn't have enough context about your existing conventions.
**Fix:** Better CLAUDE.md, skills in `.claude/commands/`, and `context/` files. Run `/prime` at session start.

### 2. Scope Creep
**Symptom:** You asked for one thing, it built three, and none are quite right.
**Cause:** Vague instructions without clear scope boundaries.
**Fix:** Use `/create-plan` with explicit "in scope / out of scope" before executing.

### 3. No Verification
**Symptom:** "It said it's done" but the code doesn't work.
**Cause:** Trusting output without testing.
**Fix:** Always run, check, and test — even though `/implement` validates, verify yourself.

### 4. Lost Progress
**Symptom:** Long session, hit context limit, lost track of what was done.
**Cause:** No checkpoints saved to files.
**Fix:** Plans in `plans/` track status automatically. Use `outputs/` for deliverables. Update `context/` as needed.

### 5. Re-explaining Everything
**Symptom:** Every session starts with 10 minutes of context-setting.
**Cause:** No persistent documentation.
**Fix:** `/prime` loads everything from CLAUDE.md, `context/`, and `plans/` in seconds. Put your patterns in skills.

---

## Quick Reference

### Session Start Checklist
- [ ] CLAUDE.md exists and is current
- [ ] `context/` files populated with background info
- [ ] Run `/prime` to load context
- [ ] Plan exists for what you're building (or create one with `/create-plan`)

### Session End Checklist
- [ ] Plans updated (status reflects work done)
- [ ] Outputs saved to `outputs/` if applicable
- [ ] Any new decisions captured in plans or `context/`
- [ ] Code verified (runs, tested)

### Key Files
| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CLAUDE.md` | Workspace overview, entry point | When structure changes |
| `context/*.md` | Background context for `/prime` | When priorities/data shift |
| `.claude/commands/*.md` | Skills and slash commands | When patterns evolve |
| `plans/*.md` | Implementation plans | Each feature/session |
| `outputs/` | Deliverables and work products | During/after sessions |
| `reference/` | Templates and reusable patterns | As useful patterns emerge |

### Key Commands
| Command | What It Does |
|---------|-------------|
| `/prime` | Load context, confirm understanding, start session |
| `/create-plan [request]` | Create a detailed plan in `plans/` |
| `/implement [plan-path]` | Execute a plan step-by-step with validation |
| `/kale-frontend` | Load Kale design system for UI work |

---

## Getting Started

1. **Download the workspace template** and customize it to your project
2. **Fill in `context/`** with your role, company info, strategy, and current data
3. **Customize CLAUDE.md** to reflect your project's specifics
4. **Add skills** in `.claude/commands/` for any domain-specific patterns (design systems, API conventions, etc.)
5. **Start Claude Code** and run `/prime` to load context
6. **Use `/create-plan`** to plan your first feature, review and refine the plan, then **run `/implement`** to execute it
7. **Verify everything** before calling it done

The upfront investment in context files and plans pays off quickly — builds go faster, outputs are more consistent, and you waste zero time re-explaining context.
