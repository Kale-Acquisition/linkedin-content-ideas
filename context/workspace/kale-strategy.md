# Strategy

> Current strategic priorities. Claude reads this during `/prime` to align work with what matters most right now.

---

## Company Context

**Kale** is a growth agency that generates top-of-funnel pipeline for clients through cold email. Clients are companies that sell to local businesses — verticals vary by client (home services, dental, legal, etc.). Kale handles the full stack: infrastructure setup, deliverability management, lead sourcing, copywriting, campaign execution, and appointment booking.

**Services**

- **Email infrastructure** — domain/mailbox setup, warmup, deliverability monitoring and management
- **Lead sourcing** — custom list building from directories, Apollo, Clay enrichment, D7 Lead Finder, Outscraper
- **Campaign execution** — copy, sequencing, A/B testing, sending via Instantly and EmailBison
- **Lead management** — inbox management, reply handling, qualification via Missive
- **Reporting** — client-facing performance reports and deliverability audits

**Tech stack**

| Category | Tools |
|----------|-------|
| Sequencing / Sending | Instantly, EmailBison |
| Lead Data | Clay, Apollo, D7 Lead Finder, Outscraper, custom directory scraping |
| Lead Management | Missive |
| Automation | n8n, Clay |
| Comms | Slack, Gmail |
| Project Management | Linear |

**Stage** — Team of 7 (2 founders + 5 team members), growing. Under 10 clients, messy but repeatable service model, focused on fixing deliverability and building systems before scaling further. Team roster lives in `context/team.md`.

**Key dynamics**

- Deliverability is the core technical challenge. Inbox placement and reply rates need to be consistently good across all clients before the team can scale.
- Operations are still manual in many areas. Tooling and automation are needed to handle more clients without proportionally more work.
- The business model is service-based (agency), but the internal tooling ambition is product-grade — Kale OS is the vision for an operational cockpit.

---

## Current Focus Period

Q1 2026 — Foundation quarter. Fix the engine before pressing the gas.

## Strategic Priorities

1. **Deliverability and infrastructure management** — This is the top priority. Build a system for managing email infrastructure inventory, monitoring deliverability health, and maintaining inbox placement across all clients. Without reliable deliverability, nothing else scales.

2. **Internal tooling and automation** — Reduce manual work across lead sourcing, campaign setup, inbox management, and reporting. Every hour saved on operations is an hour that can go toward clients or growth.

3. **Client acquisition** — Grow the client base, as fast as operations can support. Mike drives pipeline; Roshan ensures the delivery side is ready.

## What Success Looks Like

- Deliverability is predictable and manageable — not firefighting
- Clear visibility into infrastructure health (domains, mailboxes, warmup status, reputation)
- Core operational workflows are automated or semi-automated
- Team can onboard a new client without everything slowing down
- Growing pipeline with clients who stay and refer

## How We Operate

**Two domains, clean boundary** — Mike faces outward (clients, market). Roshan faces inward (infrastructure, product). _Mike directs the delivery team. Roshan owns the machine they work on._

- **Mike — Revenue & Client Success:** owns the delivery team, client strategy, relationships, growth, and service delivery outcomes.
- **Roshan — Operations + Product & Platform:** owns the machine the team works on. Two functions:
  - **Operations** keeps the machine running — Service Ops (deliverability, data pipelines, infrastructure, process health across clients), Finance, Legal. Includes a dedicated L1 tech capacity for Mike's team.
  - **Product & Platform** makes the machine better — scores incoming signals, sequences the build queue, and ships the L2/L3 systems that scale how Kale operates.

**Service delivery vs. Service ops**
Service delivery is the team doing client work (Mike's domain). Service ops is the operational infrastructure they depend on (Roshan's domain). When the deliverability machinery breaks or a process is fragmented across clients, that's a Roshan problem. When a campaign needs to be re-strategized for a specific client, that's a Mike problem.

**Product intake**
Mike submits structured product requests (problem, impact, urgency). Arra surfaces patterns from coordination work. Roshan scores and sequences against strategic priorities. The build queue is visible — not a black box.

**The L1 floor**
30% of Roshan's build capacity is always reserved for L1 tech support to the delivery team — no matter what's in the product queue. The remaining 70% is allocated across Service Ops infrastructure, L2 shared tools, and L3 platform work based on what the business needs that season.

**Operating cadence**
Weekly Roshan ↔ Mike sync to review the queue, lock the next sprint, and surface signals from client work that should reshape what gets built.

**Build layers**

The layer of a build is determined by **how the team accesses it** — that's the testable bar. Maturity, automation, and time-to-build aren't separate axes; they're what each access pattern *requires* to be viable.

- **L1 — Local.** Clone the repo, run it. Roshan or Azhar uses it directly. *Maturity:* scrappy or polished — whatever the use case warrants. *Time:* days to weeks. *Lives in Service Ops by default.* Examples: one-off scripts, dev-only CLIs, local automations.

- **L2 — Reachable.** API endpoints, lightweight UIs, or accessible portals. The team uses it without cloning. *Maturity:* repeatable, semi-automated, documented — required, or the API/UI can't run reliably behind it. *Time:* weeks. Examples: an internal API on the email-infra repo, a Notion-based client portal Arra operates.

- **L3 — Ecosystem.** Integrated into Kale's durable ecosystem (Kale OS, wiki, productized dashboards). Anyone uses it appropriately. *Maturity:* durable, fully automated, platform-owned — required, or non-technical users break it. *Time:* months. Examples: Kale OS modules, productized client dashboards, integrated reporting.

L1 fixes graduate to L2 workflows, and L2 workflows graduate to L3 products as patterns prove themselves and access broadens. The graduation step is real work — it's *not* the same as polishing the L1; it's redesigning around a wider access surface. Layer graduation is a tracked output of the product function.

**What goes in the roadmap**
The founder roadmap is for **Service Ops + Product & Platform** work — systems Kale is building or maintaining for the operation as a whole. Per-client tactical execution (campaign sends, lead pulls, template fixes, client renewals) belongs in the relevant `kale-{client}` repo and Weekly Client Review, not on the roadmap. See `knowledge/operations/roadmap-boundary.md` for the full rule and decision tree. `/roadmap --triage` enforces this automatically.

## Key Decisions and Open Questions

- What does the deliverability management system actually look like? (Dashboard? Alerts? Manual checklists with some automation?)
- How much to invest in building Kale OS vs. using off-the-shelf tools?
- When is the team ready to scale client count — what's the threshold?
- How to price and package services as the offering matures?

## Decided

- **Product function architecture** (2026-04-13): Two-layer system. Notion Monthly Initiatives DB is the stakeholder-facing intake surface (requests from Mike, Arra, clients). Linear is the execution layer (build queue, sprints, git-linked issues). Claude Code `/roadmap` command bridges both. SLA model: Urgent (same-day triage) and Standard (weekly sync review). All build work (L1/L2/L3) flows through one queue. Weekly priority review is the decision point.