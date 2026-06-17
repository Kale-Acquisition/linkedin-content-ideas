# Create Client

> Create a new client repo with standard structure, update the workspace roster, configure access, and add to the sync pipeline.

## Arguments

Parse `$ARGUMENTS` for the client name. If no name is provided, ask for it.

## Step 1: Gather Client Info

Ask the user for any details not provided in the arguments:

| Field | Required | Default |
|-------|----------|---------|
| **Client name** | Yes | — |
| **Vertical** | Yes | — |
| **Primary contact** | Yes | — (first name + role, e.g. "John, Owner") |
| **Geo focus** | Yes | — (e.g. "Dallas TX", "Southeast US") |
| **Services** | No | All five: infrastructure, campaigns, leads, inbox, reporting |

Derive from the client name:
- **Repo slug**: `kale-` + lowercase hyphenated name (e.g., `kale-acme-hvac`)
- **Date**: today's date as YYYY-MM

## Step 2: Confirm

Show a summary table and ask the user to confirm before proceeding:

```
## New Client Repo

| Field | Value |
|-------|-------|
| Client | [name] |
| Repo | Kale-Acquisition/kale-[slug] |
| Vertical | [vertical] |
| Contact | [contact] |
| Geo | [geo] |
| Services | [services] |

Proceed?
```

Wait for explicit confirmation before continuing.

## Step 3: Create GitHub Repo

```bash
gh repo create Kale-Acquisition/kale-[slug] --template Kale-Acquisition/kale-client --private --clone
```

This clones the new repo as a sibling directory (`../kale-[slug]`). The `kale-client` template includes the full client delivery structure (`infrastructure/`, `campaigns/`, `leads/`, `inbox/`, `reporting/`) plus the six Notion-mirror context files and the `context/workspace/` shared-context namespace.

## Step 4: Pre-fill Placeholders

The `kale-client` template has every directory and mirror-file shell already in place. The only customization needed is replacing placeholder tokens in the seven files that carry them.

**Files with placeholder tokens to replace:**
- `CLAUDE.md`
- `context/overview.md`
- `context/strategy.md`
- `context/customer-success.md`
- `context/data.md`
- `context/reporting.md`
- `context/infra.md`
- `context/current-state.md`

**Tokens to replace across all of the above:**

| Token | Replace with |
|-------|--------------|
| `[CLIENT NAME]` | the client's display name (e.g., "Acme HVAC") |
| `[SLUG]` | the repo slug (e.g., `acme-hvac`) |
| `[VERTICAL]` | the client's vertical |
| `[CONTACT NAME, ROLE]` | primary contact (e.g., "John Doe, Owner") |
| `[GEO]` | geo focus |
| `[SERVICES]` | comma-separated services (or "Infrastructure, Campaigns, Lead Sourcing, Inbox Management, Reporting") |
| `[YYYY-MM]` | today as `YYYY-MM` (start date) |
| `[YYYY-MM-DD]` | today as `YYYY-MM-DD` (last-synced placeholder; real timestamps come from auto-sync) |

Status field in `CLAUDE.md` should stay as `Onboarding`.

The six mirror files (`overview.md`, `strategy.md`, `customer-success.md`, `data.md`, `reporting.md`, `infra.md`) are intentionally otherwise empty — they will be populated by the auto-sync from the Notion Client Hub once Arra adds the client to the hub. Do not pre-fill operational content; that's the Notion Client Hub's job.

## Step 5: Commit and Push Client Repo

```bash
cd ../kale-[slug]
git add -A
git commit -m "chore: initialize client repo for [Client Name]"
git push
```

## Step 6: Update kale-workspace

Return to kale-workspace and make these updates:

### 6a. Add to `context/clients.md`

Append a new entry to the Active Clients section:

```markdown
### [Client Name]

- **Vertical:** [vertical]
- **Status:** Onboarding
- **Services:** [services]
- **Start date:** [YYYY-MM]
- **Primary contact:** [contact]
- **Geo focus:** [geo]
- **Repo:** Kale-Acquisition/kale-[slug]
- **Notes:** New client, onboarding in progress
```

### 6b. Add to `config/access-policy.yaml`

Add a new entry under the APPROVER REVIEW section:

```yaml
  kale-[slug]:
    gtm-ops: push
    project-ops: push
    branch_protection:
      branch: master
      required_reviews: 1
      required_reviewers: [approvers]
      enforce_admins: false
    codeowners:
      "/*": [roshan]
```

### 6c. Add to `.github/workflows/sync-downstream.yml`

Add `kale-[slug]` to the `matrix.repo` list in the `sync-tier3` job.

## Step 7: Apply Access Policy

```bash
python scripts/apply-access-policy.py --repo kale-[slug]
```

## Step 8: Hand-off to Arra

Arra populates the Notion Client Hub for the new client (Strategy, Customer Success, Data sub-pages). Once she has, the next auto-sync run will write content into the six mirror files in the new repo and the synthesis job will generate `context/current-state.md`.

Until then, the mirror files remain as placeholder shells. Claude in the client repo will see them and understand the client is pending Notion population.

## Step 9: Summary

Print a summary:

```
## Client Created: [Client Name]

| Detail | Value |
|--------|-------|
| Repo | Kale-Acquisition/kale-[slug] |
| URL | https://github.com/Kale-Acquisition/kale-[slug] |
| Local path | ../kale-[slug] |
| Status | Onboarding |
| Access | founders: admin, gtm-ops: push, project-ops: push |
| Sync | Added to sync-downstream.yml matrix |

**Updated in kale-workspace:**
- context/clients.md — added to roster
- config/access-policy.yaml — added repo with permissions
- .github/workflows/sync-downstream.yml — added to sync matrix

**Next steps:**
1. Arra populates the Notion Client Hub (Strategy, CS, Data) for [Client Name]
2. Commit and push kale-workspace changes to activate sync pipeline
3. Run `/inbox-order [Client Name]` to generate the initial domain/mailbox order
```
