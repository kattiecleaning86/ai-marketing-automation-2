# AI Organic Social Media Marketing Automation

A web application that turns a client's brief into a complete, researched month of organic social media content, ready for human approval.

**It never publishes anything.** Every post stays `Pending Review` until a person approves it. The app has no code that can post to social media.

## What happens when a client submits the brief form

| # | Stage | How it works |
|---|---|---|
| 1 | Save client brief | Stored in the database and written to `00_onboarding/brief.md` |
| 2 | Brand & website analysis | The app downloads the client's website and Claude researches the brand with live web search |
| 3 | Audience & market research | Claude web search, then personas, market overview, key dates and regulations |
| 4 | Competitor research | 3–5 direct competitors plus 1–2 aspirational brands, found with web search |
| 5 | Organic social strategy | Pillars, KPIs, platform roles, cadence, hashtags, measurement plan |
| 6 | Current trend research | Only trends backed by a dated web source are kept |
| 7 | Monthly content calendar | Posting dates are worked out in code from the cadence; Claude plans each slot |
| 8 | Captions, hooks, CTAs, hashtags | Written for each post |
| 9 | Reel scripts & carousel copy | Scene-by-scene scripts and slide-by-slide copy |
| 10 | Designer & video editor briefs | One creative brief per post (`CB-YYYY-MM-NN`) |
| 11 | Quality check | Rule-based checks in code, then a review by Claude as editor, then one automatic fix pass |
| 12 | Google Drive & Sheets delivery | Google Docs in a client folder, plus a calendar Sheet with an Approval Status dropdown |
| 13 | Slack approval notification | A message to your channel with links for review |

### How the system avoids made-up research
Claude may only cite sources that the web search tool actually returned during the run. The app records those URLs itself, labels them `S1`, `S2`, and so on, and deletes any citation that doesn't match one. Points it can't back up are labelled `Assumption`. Every source is listed in `01_research/sources.md` with the date it was accessed.

## Technology
- Python with FastAPI, server-rendered pages, and a SQLite database. One process and one data folder.
- Claude API (`claude-opus-5-5`) with the server-side web search and web fetch tools, and structured outputs.
- Google Drive and Sheets through OAuth, using the `drive.file` scope only (the app can see only files it created).
- Slack through an Incoming Webhook.
- A background worker that runs one job at a time. Each stage is saved as it finishes, so a failed run can be retried from the stage that failed.

## Pages
- `/brief`: the public brief form to share with clients.
- `/admin`: the dashboard (username `admin`, password from `ADMIN_PASSWORD`).
- `/admin/runs/<id>`: stage progress, deliverables, per-post approval, sources and the activity log.
- `/admin/settings`: API keys, Google connection and a Slack test.

## Setup
See **[docs/SETUP.md](docs/SETUP.md)** for step-by-step instructions written for non-developers. Current implementation status is in [docs/STATUS.md](docs/STATUS.md).

## Developers
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set ADMIN_PASSWORD
uvicorn app.main:app --reload
python -m pytest -q
```
The tests use a fake Claude client (`tests/fakes.py`), so they run offline and cost nothing. The running app never uses the fake.

Project rules live in [CLAUDE.md](CLAUDE.md). The workflow specification lives in [.claude/skills/organic-marketing-engine/SKILL.md](.claude/skills/organic-marketing-engine/SKILL.md).
