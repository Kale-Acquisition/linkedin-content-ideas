# /inbox-order

> Generate an inbox order — personas, domains, availability checks, and Google Sheet — for a client.

**Usage:** `/inbox-order ClientName [--personas N] [--seed N] [--website URL] [--dry-run] [--check-only]`

---

## Step 1: Parse Arguments

Parse `$ARGUMENTS` as follows:

- **Client name** — the first non-flag word(s). If missing, ask the user for it before proceeding.
- **`--personas N`** — number of personas (default: 8)
- **`--seed N`** — random seed for reproducible generation
- **`--website URL`** — client website / forwarding domain (written to sheet cell B9)
- **`--dry-run`** — preview only, no RDAP checks or sheet export
- **`--check-only`** — generate + RDAP check, skip sheet export

Build the CLI command with these rules:
- Always add `--output-json` (enables downstream automation)
- Always add `--personas N` explicitly (use 8 if not specified)
- Include any other flags the user passed

## Step 2: Run the Script

Run `inbox_order.py` using Bash with piped stdin to auto-confirm all interactive prompts.

**Python path:** `/c/Users/rosha/AppData/Local/Microsoft/WindowsApps/python3.exe`
**Script path:** `automations/scripts/inbox_order.py`
**Timeout:** 600000 (10 minutes — RDAP checks can be slow)

**Pipe sequences by mode:**

| Mode | Pipe input |
|---|---|
| `--dry-run` | `printf 'ClientName\n'` |
| `--check-only` | `printf 'ClientName\ny\ny\n'` |
| Full run (sheets configured) | `printf 'ClientName\n\ny\ny\nn\n'` |
| Full run (no sheets) | `printf 'ClientName\ny\ny\nn\n'` |

To determine which full-run pipe to use:
- Check if `GOOGLE_SHEETS_CREDENTIALS_PATH` is set in the environment
- If set: use the "sheets configured" pipe (extra `\n` to accept default template ID)
- If not set: use the "no sheets" pipe

The `ClientName` in the pipe must match the client name parsed from arguments.

Always answer `n` to the purchase confirmation prompt — Claude cannot purchase domains.

**Example commands:**

```bash
# Dry run
printf 'Acme\n' | /c/Users/rosha/AppData/Local/Microsoft/WindowsApps/python3.exe automations/scripts/inbox_order.py --dry-run --output-json --personas 8

# Check only
printf 'Acme\ny\ny\n' | /c/Users/rosha/AppData/Local/Microsoft/WindowsApps/python3.exe automations/scripts/inbox_order.py --check-only --output-json --personas 8

# Full run (sheets configured)
printf 'Acme\n\ny\ny\nn\n' | /c/Users/rosha/AppData/Local/Microsoft/WindowsApps/python3.exe automations/scripts/inbox_order.py --output-json --personas 8 --website acme.com

# Full run (no sheets)
printf 'Acme\ny\ny\nn\n' | /c/Users/rosha/AppData/Local/Microsoft/WindowsApps/python3.exe automations/scripts/inbox_order.py --output-json --personas 8
```

## Step 3: Show Summary

After the script completes, parse the output and present a clean summary:

```
## Inbox Order: [ClientName]

| Metric | Value |
|---|---|
| Personas | N |
| Domains | N |
| Inboxes | N |
| Est. cost | $X,XXX.XX |
| QA | All checks passed / N warnings |
| Sheet | [link] or N/A |
| JSON | [filepath] |
| Domain list | [filepath] |
```

If QA warnings were present, list them.

If a sheet URL was returned, include it as a clickable link.

## Step 4: Next Steps

Based on the mode, provide appropriate next steps:

- **`--dry-run`:** "Run again without `--dry-run` to check domain availability via RDAP."
- **`--check-only`:** "Review the domains above. Run without `--check-only` for full sheet export."
- **Full run:** "Purchase domains at https://dash.cloudflare.com/, then update the Google Sheet with purchase status."

If `--website` was provided, confirm it was written to sheet cell B9.
