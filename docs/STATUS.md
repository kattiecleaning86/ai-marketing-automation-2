# Implementation Status

_Last updated: 2026-11-06_

## Built and tested
| Component | Status | Notes |
|---|---|---|
| Public client brief form (`/brief`) | Done | Required-field validation, spam honeypot, cadence per platform, target month |
| Database (SQLite) | Done | Clients, runs, stages, sources, posts, approvals, events, settings |
| Workflow engine (13 stages) | Done | Saves each stage; resumes after a crash; retries from the failed stage; can re-run from any stage |
| Background worker | Done | One run at a time; daily run limit |
| Claude integration | Built — **real API not yet exercised** | Web search/fetch + structured outputs. Needs `ANTHROPIC_API_KEY` |
| Anti-fabrication source check | Done | Citations must match pages the search tool returned; others removed |
| Website fetch for brand analysis | Done | Plus Claude web_fetch as backup |
| Deterministic QA rules | Done | 16 required fields, platform caption/hashtag limits, scripts/slides, duplicates, sources, pillar mix |
| Claude editor QA + auto-fix pass | Done | |
| Local deliverables (Markdown + CSV) | Done | `data/clients/<slug>/00_onboarding … 07_delivery` |
| Google Drive + Sheets delivery | Built — **not yet tested against a live Google account** | OAuth `drive.file`; Docs, calendar Sheet with dropdown, two-way approval sync |
| Slack approval notification | Built — **not yet tested against a live workspace** | Incoming Webhook; also sends alerts for failed runs |
| Admin dashboard, approvals, settings | Done | HTTP Basic auth (`ADMIN_PASSWORD`) |
| Automated tests | 20 passing | `python -m pytest -q`; they use a fake Claude client and fake Google/Slack |
| Deployment files | Done | `Dockerfile`, `render.yaml` |

## Not built (by design or pending)
| Item | Reason |
|---|---|
| Social media publishing | Deliberately not built. Content is never published automatically. |
| Canva integration | Not built. The Canva Connect API needs a reviewed Canva app; for now the creative briefs are written for designers to build in Canva by hand. |
| Client-facing review portal | Approvals happen in the admin dashboard or the Google Sheet. |

## Needs the operator
- Claude API key (required to run).
- Hosting account (Render recommended) to get a public form link.
- Google OAuth client ID/secret + one-time "Connect Google" click (optional).
- Slack Incoming Webhook URL (optional).
