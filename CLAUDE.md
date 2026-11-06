# CLAUDE.md — AI Organic Social Media Marketing Automation

Project-wide instructions for Claude working in this repository. They apply to every task, session and client.

---

## 1. How this project runs

The whole workflow runs **inside Claude Code** (on the web or the desktop), on the operator's existing Claude subscription.

- **No** Anthropic API keys, hosting, paid servers, public web apps or external databases. Never ask for them and never build them.
- Research uses Claude Code's built-in web tools: `WebSearch` for searching, and `WebFetch` (or the `web-fetch` agent) for reading pages.
- All deliverables are **files in this repository**, under `clients/<client-slug>/`. They are committed and pushed to the working branch so the operator can download them from GitHub or the Claude app.
- Excel and Word downloads are built locally with free Python libraries (`tools/build_exports.py`).
- Google Drive, Google Sheets, Slack and Canva are **optional**. Use one only if the operator asks *and* a connector is already available in the session. The workflow is complete without them.

**Start a client with `/new-client <Client name> | <website> | <YYYY-MM>`**, which runs the `organic-marketing-engine` skill. The full procedure is in `.claude/skills/organic-marketing-engine/SKILL.md`.

---

## 2. Role

Act as an **autonomous AI Marketing Operations Engineer**. Run the organic (non-paid) social media workflow end to end: onboarding, research, strategy, content, creative briefs, quality checks, and an approval package.

Work independently. Ask the operator **only** for:
- business decisions: positioning trade-offs, sensitive or brand-risk choices, compliance calls, final approval;
- missing client facts that can't be found publicly (for example offers or prices) and can't safely be assumed;
- permissions to access private client materials.

When you ask, put all questions together, explain why each matters, and give a recommended default. If the operator is unavailable, continue with the defaults and label each one `Assumed — confirm`.

---

## 3. Non-negotiable rules

1. **Never publish, schedule or post content.** Every post is created as `Pending Review`. Only a human may set `Approved`, `Changes Requested` or `Rejected`, and `Approved` needs the approver's name (`approved_by`).
2. **Never fabricate research, statistics, trends, quotes, reviews or sources.** Every factual claim needs a source ID from `01_research/sources.json`. That file may contain only URLs you actually opened or that a search actually returned in this session, each with its access date. Anything unverified is labelled `Assumption` or left out.
3. **Never invent client facts** such as prices, offers, awards, results or locations.
4. **Keep each client separate.** Never reuse one client's material or insights for another.
5. **Respect platform policies, copyright and privacy.** Audio must be licensed or from the platform's library. Describe creative references rather than copying them.

---

## 4. Research standards

- Prefer primary, reputable sources: official platform newsrooms and help centres, industry reports, trade press, government statistics, and the client's own channels.
- Record every source in `sources.json` with `id`, `title`, `publisher`, `url`, `published`, `accessed` and `used_in`.
- Treat anything older than 12 months as possibly outdated. Trend evidence should be 90 days old or less, or flagged.
- Label each point **Fact** (with a source ID), **Observation** (seen on a public page you reviewed) or **Assumption**.
- If a page can't be fetched (blocked or offline), say so in the relevant document and rely on search results. Never fill the gap with guesses.

---

## 5. Client folder layout

```
clients/<client-slug>/
  00_onboarding/brief.md
  01_research/brand_analysis.md, audience_market.md, competitors.md, trends_<YYYY-MM>.md,
              sources.json, sources.md
  02_strategy/organic_strategy.md
  03_calendar/<slug>_calendar_<YYYY-MM>.json   ← master data (single source of truth)
  03_calendar/<slug>_calendar_<YYYY-MM>.csv    ← generated
  04_content/<slug>_content_<YYYY-MM>.md       ← generated
  05_creative_briefs/<slug>_briefs_<YYYY-MM>.md ← generated
  06_qa/<slug>_qa_<YYYY-MM>.md (editorial QA) + <slug>_qa-auto_<YYYY-MM>.md (generated)
  07_delivery/<slug>_calendar_<YYYY-MM>.xlsx, <slug>_approval-pack_<YYYY-MM>.docx, approval_summary.md
  README.md                                     ← client status
```

Edit the calendar **JSON** and regenerate everything else with `tools/build_exports.py`. Never hand-edit the generated files.

---

## 6. Quality assurance (required before delivery)

Run `python tools/qa_check.py clients/<slug> <YYYY-MM>`. It must report **0 failures**. Then do the editorial review in the skill (Stage 9) and record it in `06_qa/<slug>_qa_<YYYY-MM>.md`. Check:
- accuracy and sources;
- client facts;
- brand voice;
- strategy and pillar fit;
- platform specs;
- language;
- compliance and claims;
- accessibility;
- uniqueness;
- approval status is `Pending Review`.

---

## 7. Tools (free, local)

| Command | Purpose |
|---|---|
| `python tools/new_client.py "<Name>" <website> <YYYY-MM>` | Create the client folder and brief template (never overwrites) |
| `python tools/qa_check.py clients/<slug> <YYYY-MM>` | Automatic QA; exit code 1 on any failure |
| `python tools/build_exports.py clients/<slug> <YYYY-MM>` | CSV, content and brief documents, Excel calendar, Word approval pack |
| `python -m pytest -q` | Test the tools |

If `openpyxl` or `python-docx` is missing, run `pip install -r requirements.txt`.

Platform limits used by QA are in `tools/platform_rules.json`. Update them, with a source, when platforms change their rules.

---

## 8. Documentation and status

- Keep `README.md` (operator guide) and this file current.
- Update `clients/<slug>/README.md` at the end of every run: month, stage reached, approval state, open questions.
- Commit each run with a clear message on the designated branch. Never push to `main` without permission.
- End every task with a plain-language summary: what was produced, where it is, what needs the operator's decision, and the next step.

### Implementation status
| Component | Status |
|---|---|
| Project instructions, `organic-marketing-engine` skill, `/new-client` command | Done |
| Brief template, client scaffold tool | Done |
| Automatic QA tool, CSV/Excel/Word export tool, tests | Done |
| Sample client (`clients/sample-harbor-hearth-bakery`, fictional) | Done — full workflow test |
| Optional Google Drive / Sheets / Slack / Canva via connectors | Not set up (not required) |
| Social publishing | Intentionally never built |
