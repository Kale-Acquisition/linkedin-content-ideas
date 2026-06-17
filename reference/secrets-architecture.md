# Secrets & Identity Architecture

> How Kale manages API keys, user identity, and activity tracking across shared systems.
> This document syncs to all Kale repos via the template pipeline.

---

## Overview

Kale runs shared systems (data pipeline, automation workflows, etc.) that multiple team members use. Connector API keys (Outscraper, Reoon, Apollo, etc.) live server-side — team members never configure them locally. User identity comes from GitHub, which everyone already has. Activity is logged to Supabase for attribution and debugging.

**Principle:** The fewer secrets on developer machines, the better. Shared systems hold the keys and act on behalf of authenticated users.

---

## Three-Layer Secrets Model

### Layer 1: Deployment secrets (Railway env vars)

Third-party connector API keys used by the data pipeline and other deployed services.

| Example keys | Managed by |
|---|---|
| `OUTSCRAPER_API_KEY`, `REOON_API_KEY`, `FIRECRAWL_API_KEY` | Roshan / Azhar |
| `APOLLO_API_KEY`, `AI_ARK_API_KEY`, `OPENAI_API_KEY` | Roshan / Azhar |
| `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | Roshan / Azhar |

These keys are set in the Railway dashboard. Only engineering has access. The pipeline uses them server-side when executing actions on behalf of team members.

**Adding a new connector key:**
1. Get the API key from the service provider
2. Add it as an env var in Railway (dashboard or CLI)
3. Reference it in the pipeline code via `process.env.NEW_KEY`
4. No changes needed on any team member's machine

### Layer 2: Application secrets (Supabase Vault)

Secrets consumed by Supabase Edge Functions, cron jobs, and database-level automation. Stored in `vault.secrets`, read via `vault.decrypted_secrets`.

| Example keys | Used by |
|---|---|
| `service_role_key` | Edge Functions, cron triggers |
| `CRON_SECRET` | Scheduled function invocations |

**When to use Vault vs Railway env vars:**
- **Vault** — for anything running inside Supabase (Edge Functions, PL/pgSQL, cron jobs)
- **Railway env vars** — for anything running outside Supabase (data pipeline, external services)

**Managing Vault secrets:**
```sql
-- Add a secret
INSERT INTO vault.secrets (name, secret) VALUES ('my_key', 'the-value');

-- Update a secret
UPDATE vault.secrets SET secret = 'new-value' WHERE name = 'my_key';

-- Read (from Edge Functions or PL/pgSQL only)
SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'my_key';
```

### Layer 3: CI/CD secrets (GitHub org-level)

Secrets used by GitHub Actions workflows across the Kale-Acquisition org.

| Secret | Purpose |
|---|---|
| `SYNC_PAT` | Template and client repo sync workflows |
| Deployment tokens | Auto-deploy workflows (per-repo or org-level) |

Managed in **GitHub → Kale-Acquisition → Settings → Secrets and variables → Actions**. Repository access policies control which repos can see each secret.

---

## User Identity: GitHub Auth

GitHub login is the gate to using any shared Kale system. It provides verified identity with zero additional setup.

### How it works

**Client side** (the tool/CLI/skill triggering an action):
```bash
# Get the authenticated GitHub username
gh api user --jq .login
# → "roshankathir"
```

This is sent as a request header with every pipeline call:
```
X-Kale-User: roshankathir
```

**Server side** (the pipeline receiving the request):
1. Read `X-Kale-User` from the request header
2. (Optional) Verify org membership: `GET /orgs/Kale-Acquisition/members/{username}`
3. Log the username with the action
4. Proceed with the requested operation using server-side API keys

### Why GitHub identity

- **Zero setup** — everyone on the team already has `gh auth` configured
- **Verified** — tied to their actual GitHub account, not an honor-system header
- **No key management** — nothing to issue, distribute, rotate, or revoke
- **Org-aware** — can check GitHub team membership for role-based access later

---

## Activity Logging

Every action through shared systems is logged to the `pipeline_activity` table in Supabase (kale-analytics).

### Schema

```sql
CREATE TABLE pipeline_activity (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  github_username text NOT NULL,        -- who triggered this
  action text NOT NULL,                 -- 'scrape', 'enrich', 'verify', 'export'
  connector text,                       -- 'outscraper', 'reoon', 'apollo', etc.
  client_slug text,                     -- 'n2', 'riipen', null for internal
  repo text,                            -- which repo triggered it
  params jsonb DEFAULT '{}',            -- action-specific inputs
  status text NOT NULL DEFAULT 'running', -- 'running', 'success', 'failed'
  error text,                           -- null on success
  result_summary jsonb DEFAULT '{}',    -- outcomes: {rows_scraped: 150, duplicates: 12}
  credits_used integer DEFAULT 0,       -- API calls / rows / units consumed
  started_at timestamptz DEFAULT now(),
  completed_at timestamptz              -- null while running
);

CREATE INDEX idx_activity_user ON pipeline_activity (github_username, started_at DESC);
CREATE INDEX idx_activity_client ON pipeline_activity (client_slug, started_at DESC);
CREATE INDEX idx_activity_connector ON pipeline_activity (connector, started_at DESC);
```

### What gets tracked

| Field | Example | Purpose |
|---|---|---|
| `github_username` | `"pandush"` | Who did it |
| `action` | `"scrape"` | What kind of operation |
| `connector` | `"outscraper"` | Which API was called |
| `client_slug` | `"n2"` | Which client it was for |
| `repo` | `"kale-n2"` | Where the action was triggered from |
| `params` | `{"query": "HVAC Dallas", "limit": 500}` | What was requested |
| `credits_used` | `500` | Raw units consumed (API calls, rows, etc.) |
| `result_summary` | `{"rows": 487, "duplicates": 13}` | What came back |

### Example queries

```sql
-- Who's been active this week?
SELECT github_username, COUNT(*), SUM(credits_used)
FROM pipeline_activity
WHERE started_at > now() - interval '7 days'
GROUP BY github_username;

-- Outscraper usage this month (for budget tracking)
SELECT SUM(credits_used), COUNT(*)
FROM pipeline_activity
WHERE connector = 'outscraper' AND started_at > date_trunc('month', now());

-- What did Pandush run for N2 yesterday?
SELECT action, connector, params, status, result_summary
FROM pipeline_activity
WHERE github_username = 'pandush' AND client_slug = 'n2'
  AND started_at > now() - interval '1 day'
ORDER BY started_at DESC;

-- Failed actions in the last 24 hours
SELECT github_username, action, connector, error, started_at
FROM pipeline_activity
WHERE status = 'failed' AND started_at > now() - interval '1 day';
```

---

## Setup by Role

| Role | People | Local setup required |
|------|--------|---------------------|
| **Engineering** | Roshan, Azhar | `gh auth login` + MCP keys (Cloudflare, Notion, etc. — for local Claude Code MCP servers only) |
| **Operators** | Pandush, Arra | `gh auth login` |
| **VAs** | Beverly, Umer | `gh auth login` |

Operators and VAs need nothing beyond GitHub auth. MCP keys are only needed by engineering for local Claude Code sessions — they're separate from the pipeline.

---

## Key Rotation

| Secret type | Where it lives | Who rotates | How |
|---|---|---|---|
| Connector API keys | Railway env vars | Roshan / Azhar | Railway dashboard or CLI |
| Supabase Vault secrets | Supabase | Roshan | `UPDATE vault.secrets SET secret = '...' WHERE name = '...'` |
| CI/CD secrets | GitHub org settings | Roshan | GitHub org settings → Secrets UI |
| User identity | GitHub | N/A | It's their GitHub account — no rotation needed |

---

## Upgrade Path

This architecture is designed for a small team (<15 people). If Kale grows beyond that, or brings on external contractors who shouldn't have GitHub org membership:

- **Supabase Auth** — add email-based login (magic links). Team members sign in once, session auto-refreshes. Gives you fine-grained permissions without GitHub dependency.
- **Role-based access via GitHub Teams** — before adding Supabase Auth, you can gate pipeline actions by checking GitHub team membership (e.g., `engineering` can run destructive operations, `gtm-ops` can run scrapes, `viewers` can only check status).

Don't add these until you need them. GitHub identity covers everything at current scale.
