# Slack Emoji Capture — Routing Reference

React to any Slack message with one of these emojis to route it into the knowledge system.
No form to fill. No command to run. Just react.

---

## The three emojis

| Emoji | Name | Meaning | Use when |
|---|---|---|---|
| 📌 | Pin | Save this — knowledge worth keeping | You see a finding, insight, update, or result worth capturing |
| ⚡ | Zap | Blocker — something is stuck or at risk | You're flagging something that's blocking progress |
| ✅ | Check | Resolved — something closed or shipped | A blocker is gone, a task is done, something shipped |

## Where things land

React in a **client channel** → goes to that client's repo + Notion CS/Success DB
React in an **internal channel** → goes to kale-workspace knowledge library

| Channel | Repo destination | Path |
|---|---|---|
| `#kale-n2` | kale-n2 | `knowledge/` (📌) · `## Blockers` in current-state.md (⚡) |
| `#kale-n2-recruiting` | kale-n2-recruiting | same |
| `#kale-terraboost` | kale-terraboost | same |
| `#kale-riipen` | kale-riipen | same |
| `#kale-infra` | kale-workspace | `knowledge/deliverability/` |
| `#kale-automations` | kale-workspace | `knowledge/operations/` |
| `#kale-acquisition` | kale-workspace | `knowledge/operations/` |

## What gets written to Git (📌)

```markdown
<!-- Captured from Slack #channel by @author on YYYY-MM-DD -->
# {first 80 chars of message text}

{full message text}

{thread context if reaction was on a thread reply}

**Source:** Slack `#{channel}` · {message link}
```

**Filename:** `YYYY-MM-DD-{slug-from-message-text}.md` in the target directory.

## Technical implementation

Built by Azhar as an n8n workflow. Trigger: Slack `reaction_added` event. Filters on `pushpin`, `zap`, `white_check_mark` emojis. Routes by channel name → repo mapping (hardcoded in n8n). Writes to Git via GitHub API.

Arra's Linear task automation is separate — it uses a different trigger and is not affected by these emojis.

## Notes

- Works on any message, including thread replies
- If you react by mistake, let Roshan know — the file can be removed from the repo manually
- The n8n workflow must be running for reactions to trigger writes; check with Roshan if a reaction seems to have been missed
