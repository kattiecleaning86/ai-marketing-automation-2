# AI Organic Social Media Marketing Automation

A complete organic social media workflow that runs **inside Claude Code** on your existing Claude subscription.
No API keys, no hosting, no paid servers, no external databases. Everything Claude produces is saved as files in this repository.

## How to run it for a new client

1. Open this repository in **Claude Code on the web** (claude.ai/code), the desktop app, or the CLI.
2. Type:

   ```
   /new-client Bean There Coffee | https://beantherecoffee.com | 2027-01
   ```

   That is: client name | website | month to plan (YYYY-MM).
3. Claude runs all 12 stages on its own. It may ask you a few questions (tone, offers, approvers). If you don't answer, it continues with sensible defaults and marks each one "Assumed — confirm".
4. When it's done, download from `clients/<client-name>/07_delivery/`:
   - **`…_calendar_<month>.xlsx`**: the Excel calendar, with an Approval Status dropdown on every post
   - **`…_approval-pack_<month>.docx`**: a Word document with everything (research, strategy, content, briefs, QA)
5. Approve by typing, for example:

   ```
   /approve bean-there-coffee 2027-01: approve P01-P08, change P09: make it a carousel, reject P12
   ```

   Or fill in the Approval Status column in the Excel file and give it back to Claude.

**Next month:** run `/new-client` again with the same name and the new month. The existing brief and files are kept.

**No details yet?** Type `/new-client` with nothing after it. Claude asks for the basics, or creates a blank brief at `clients/<name>/00_onboarding/brief.md` for you or the client to fill in. The template is in `templates/client_brief_template.md`.

## What Claude does (the 12 stages)
| # | Stage | Output |
|---|---|---|
| 1 | Client brief | `00_onboarding/brief.md` |
| 2 | Website and brand analysis | `01_research/brand_analysis.md` |
| 3 | Industry and audience research, with personas | `01_research/audience_market.md` |
| 4 | 3–5 competitors | `01_research/competitors.md` |
| 5 | Organic social strategy | `02_strategy/organic_strategy.md` |
| 6 | Instagram, Facebook, LinkedIn and industry trends | `01_research/trends_<month>.md` |
| 7 | Research-backed monthly calendar | `03_calendar/…json` and `.csv` |
| 8 | Hooks, captions, CTAs, hashtags, reel scripts, carousel slides | `04_content/…md` |
| 9 | Designer and video-editor creative briefs | `05_creative_briefs/…md` |
| 10 | Quality checks (automatic and editorial) | `06_qa/` |
| 11 | Downloadable Excel and Word files | `07_delivery/` |
| 12 | Approval package | `07_delivery/approval_summary.md`, committed and pushed |

## Built-in safeguards
- **Nothing is ever published.** Every post starts as "Pending Review". Only you can approve, and approvals record your name.
- **No made-up research.** Every fact cites a source ID listed in `01_research/sources.md` with its URL and access date. Anything unverified is labelled "Assumption".
- **Automatic QA.** The QA tool checks all 16 calendar fields, platform limits (including Instagram's 5-hashtag cap), scripts and slides, source IDs, unsourced statistics, duplicates and pillar mix.

## Example
`clients/sample-harbor-hearth-bakery/` is a complete December 2026 run for a **fictional** bakery: 30 real sources, 20 posts, Excel and Word downloads, QA passed.

## Files in this repo
| Path | Purpose |
|---|---|
| `CLAUDE.md` | Project rules Claude follows in every session |
| `.claude/skills/organic-marketing-engine/SKILL.md` | The full 12-stage workflow |
| `.claude/commands/new-client.md`, `approve.md` | The `/new-client` and `/approve` commands |
| `templates/client_brief_template.md` | Blank client brief |
| `tools/new_client.py` | Creates a client folder |
| `tools/qa_check.py` | Automatic quality checks |
| `tools/build_exports.py` | Builds the CSV, Excel and Word files |
| `tools/platform_rules.json` | Platform limits (updated from research) |
| `tests/` | Tests for the tools (`python -m pytest -q`) |

## Notes
- The Excel and Word files are built with two free Python libraries. If Claude reports they are missing, it installs them with `pip install -r requirements.txt`.
- Research uses Claude Code's built-in web search and page reading. If your cloud environment's network settings block a website, Claude uses search results instead and says so in the report. To let Claude read client and competitor websites directly, set the environment's network access to allow them (cloud environment menu → Edit → Network access).
