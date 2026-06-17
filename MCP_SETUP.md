# MCP Setup Guide

This workspace uses six MCP (Model Context Protocol) servers that give Claude Code direct access to Kale's key platforms. Each requires API keys set as environment variables in your shell.

---

## Required Environment Variables

| Variable | Service | Purpose |
|---|---|---|
| `CLOUDFLARE_API_TOKEN` | Cloudflare | DNS, Workers, email routing, R2 storage |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare | Scopes API calls to Kale's account |
| `EMAILBISON_API_KEY` | EmailBison | Email infrastructure, deliverability data |
| `INSTANTLY_API_KEY` | Instantly | Campaign data, outreach analytics |
| `NOTION_TOKEN` | Notion | Database queries, page creation, search (for `/generate-automation-ideas`) |
| `FIREFLIES_API_KEY` | Fireflies | Meeting transcripts, summaries (for `/generate-automation-ideas`) |
| `SUNSAMA_MCP_TOKEN` | Sunsama | Daily task creation + reads for `/daily-priorities` Sunsama plan integration |
| `GOOGLE_SHEETS_CREDENTIALS_PATH` | Google Sheets | Service account JSON for inbox order sheet export |
| `GOOGLE_SHEETS_DELEGATE_TO` | Google Sheets | Email to impersonate via domain-wide delegation (overrides profile value) |
| `KALE_USER` | Workspace | Your profile key (`roshan` or `mike`). Loads per-user config from `config/profiles.json`. |

---

## Setup Instructions

Add the following to your `~/.zshrc` or `~/.bashrc`:

```bash
# Kale MCP — Cloudflare
export CLOUDFLARE_API_TOKEN="your-token-here"
export CLOUDFLARE_ACCOUNT_ID="your-account-id-here"

# Kale MCP — EmailBison
export EMAILBISON_API_KEY="your-key-here"

# Kale MCP — Instantly
export INSTANTLY_API_KEY="your-key-here"

# Kale MCP — Notion
export NOTION_TOKEN="ntn_your-token-here"

# Kale MCP — Fireflies
export FIREFLIES_API_KEY="your-key-here"

# Kale MCP — Sunsama (for /daily-priorities push to Sunsama plan)
export SUNSAMA_MCP_TOKEN="your-jwt-token-here"

# Kale — Google Sheets (inbox order provisioning)
export GOOGLE_SHEETS_CREDENTIALS_PATH="$HOME/.config/gcloud/kale-service-account.json"
export GOOGLE_SHEETS_DELEGATE_TO="automation@kaleacquisition.com"

# Kale — User profile (selects per-user config from config/profiles.json)
export KALE_USER="roshan"  # or "mike"
```

Then reload your shell:
```bash
source ~/.zshrc   # or source ~/.bashrc
```

---

## Verify MCP is Active

In a Claude Code session, run:
```
/mcp
```

You should see all six servers listed as connected. If any show as disconnected, check that the corresponding environment variables are set (`echo $CLOUDFLARE_API_TOKEN`).

---

## Notes

- **Never commit API keys** — they are excluded by `.gitignore` (`.env`, `.env.*`, `*.env`)
- **EmailBison and Instantly endpoint URLs** in `.mcp.json` are placeholders — verify actual MCP endpoint URLs with each service's documentation before relying on them for `/analytics-report`
- **Cloudflare MCP** is the most battle-tested of the three; the others are newer integrations
- Each team member sets their own env vars — keys are per-person, not shared through this repo

---

## Notion MCP Setup

The Notion MCP server runs locally via `npx @notionhq/notion-mcp-server` (stdio transport). It needs an internal integration token.

1. **Create an integration:** Go to [notion.so/profile/integrations](https://www.notion.so/profile/integrations) → **+ New integration** → name it "Kale Claude Code MCP" → select the Kale workspace → Submit
2. **Copy the token:** On the integration's Configuration tab, copy the **Internal Integration Secret** (starts with `ntn_`) → set as `NOTION_TOKEN`
3. **Grant page access:** Open each Notion page/database Claude needs access to → `...` menu → **+ Add Connections** → search for "Kale Claude Code MCP" and confirm. Key pages to connect:
   - The Automation Ideas database
   - Vision & Strategy page (parent of the DB)
   - Roshan's Rolling Thoughts
   - Collab page
   - Monthly Initiatives

> The integration can only see pages you explicitly connect. Connecting a parent page grants access to all children.

---

## Fireflies MCP Setup

Fireflies uses their official remote MCP server at `https://api.fireflies.ai/mcp` (HTTP transport).

1. **Get your API key:** Log in to [fireflies.ai](https://fireflies.ai) → Settings (gear icon) → **Developer Settings** → copy the API key
2. **Set the env var:** `export FIREFLIES_API_KEY="your-key-here"`

> Requires a Fireflies paid plan (Business or higher) for API access. The API key gives access to all org transcripts — Roshan's admin access covers all team meetings.

---

## Sunsama MCP Setup

Sunsama exposes a remote MCP server at `https://api.sunsama.com/mcp` that lets Claude push and read Sunsama tasks. Used by `/daily-priorities` to write the day's plan directly into Sunsama after the walkthrough.

1. **Get your token:** Log in to [sunsama.com](https://app.sunsama.com) → Settings → **Integrations** → **MCP** (or similar — Sunsama may rename) → copy the JWT token shown
2. **Set the env var:** `export SUNSAMA_MCP_TOKEN="eyJhbGc..."`
3. **Reload shell + restart Claude Code** for the MCP server to register

> The token is account-scoped. Treat it as a credential — don't commit, don't paste in shared chat. Regenerate from Sunsama if exposed.
