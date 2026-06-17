# Sync Client Context

> Pull current client context from the Notion client hub into a client repo's context files. Notion → repo direction.

## Arguments

Parse `$ARGUMENTS` for the client name. If no name is provided, read `context/clients.md` and ask the user which client to sync.

## Step 1: Find the Client

1. Read `context/clients.md` to find the client entry.
2. Extract the repo slug from the **Repo** field (e.g., `Kale-Acquisition/client-acme-hvac` → `client-acme-hvac`).
3. Verify the client repo exists locally at `../kale-[slug]`. If not, offer to clone it: `gh repo clone Kale-Acquisition/kale-[slug] ../kale-[slug]`

## Step 2: Read from Notion

Use Notion MCP tools to find and read the client's hub page:

1. **Search for the client page** — Use `mcp__notion__API-post-search` (or the Claude AI Notion tools) to search for a page matching the client name. If the Notion client hub is a database, query it for the client entry.

2. **Extract key context** from the client's Notion page(s):

   | What to extract | Where it goes |
   |-----------------|---------------|
   | Current status and activity | `context/current-state.md` → Status section |
   | Key metrics (domains, mailboxes, placement, reply rates) | `context/current-state.md` → Infrastructure + Campaigns sections |
   | Recent meeting notes (last 2-3 summaries) | `context/current-state.md` → What's Working / In Progress |
   | Strategy or account plan updates | `context/project-goals.md` → if goals have evolved |
   | Any blockers or issues flagged | `context/current-state.md` → Blockers section |

3. If no Notion page is found for this client, report that and ask the user if they want to create one or skip the Notion sync.

## Step 3: Read Current Repo State

Before writing, read the client repo's current context files to understand what's there:

- `../kale-[slug]/context/current-state.md`
- `../kale-[slug]/context/project-goals.md`
- `../kale-[slug]/context/project-info.md`

## Step 4: Update Client Repo

Write the extracted Notion context into the client repo's files:

1. **`context/current-state.md`** — This is the primary target. Update the sections with fresh data from Notion while preserving the file's structure:
   - Status (overall client status)
   - Infrastructure metrics (domains, mailboxes, warmup, placement)
   - Campaign status (what's running, performance)
   - What's Working / In Progress / Blockers / Next Steps

2. **`context/project-goals.md`** — Only update if the client's goals or success criteria have meaningfully changed based on Notion data. Don't overwrite stable goals.

3. **`context/project-info.md`** — Only update the Status field in the Client Profile table if it changed (e.g., Onboarding → Active).

**Important:** Preserve any content that was manually added to these files. The sync should *update* sections with Notion data, not blow away local content. If a section has detailed local content that Notion doesn't have, keep the local content.

## Step 5: Update Roster (If Status Changed)

If the client's status changed (e.g., Onboarding → Active, Active → Paused):

1. Update the **Status** field in `context/clients.md` in kale-workspace.
2. If infrastructure counts changed significantly, update the **Infrastructure** field too.

## Step 6: Report

Show what was synced:

```
## Synced: [Client Name]

**Source:** Notion client hub page
**Target:** ../kale-[slug]

### Changes:
- context/current-state.md — [updated Status, Infrastructure metrics, Campaign status]
- context/project-goals.md — [no changes / updated success criteria]
- context/clients.md — [no changes / updated status: Onboarding → Active]

### Notion Data Summary:
[Brief summary of what was extracted from Notion]
```

## Notes

- This command depends on the Notion client hub existing. If the hub structure changes, update the extraction logic in Step 2.
- The command searches by client name, not hardcoded database IDs — this makes it resilient to Notion restructuring.
- Run this periodically (e.g., weekly) to keep client repos current. It's not automated — it's a manual pull.
- If Notion MCP tools are not available (no API key configured), the command should gracefully report that and suggest manual updates.
