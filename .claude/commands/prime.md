# Prime

> Execute the following sections to initialize the session with full context, then summarize your understanding.

## Detect Active User

Resolve the active user using this priority order:

1. **`KALE_USER` env var** — check first. If set, use it.
2. **`config/local.json`** — if env var is not set, read this file (gitignored, per-machine). It contains `{ "user": "roshan" }` or similar.
3. **Ask interactively** — if neither source provides a user, ask: "Who's working today? (roshan / mike)" using AskUserQuestion. Use their answer to proceed.

Once resolved, load the matching profile from `config/profiles.json` and note the active user's name. If the user came from option 3, suggest they create `config/local.json` so they won't be asked again:

```
To skip this next time, create config/local.json:  { "user": "roshan" }
```

## Read

Read these files in order:

1. `config/profiles.json` — user profiles and per-user automation config
2. `context/team.md` — team roles and responsibilities (Arra, Azhar, Pandush, Beverly, Umer)
3. `context/strategy.md` — current priorities and strategic direction
4. `context/clients.md` — active client roster (if it exists)
5. `knowledge/index.md` — knowledge library table of contents

## Summary

After reading, provide a structured summary covering:

1. **Active user** — resolved user and how they were detected (env var / local config / asked)
2. **Strategy snapshot** — 3 bullets from `context/strategy.md` (current focus period + top priorities)
3. **Client roster** — table of active clients from `context/clients.md` with columns: Client | Vertical | Status | Services
4. **Knowledge library** — one line: total document count and topic areas covered
5. **Readiness confirmation** — confirm you're ready to help
