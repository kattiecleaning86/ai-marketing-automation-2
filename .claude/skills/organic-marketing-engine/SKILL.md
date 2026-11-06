---
name: organic-marketing-engine
description: Runs the complete organic social media workflow for one client and month inside Claude Code. It collects the brief, researches the website, audience, 3–5 competitors and current Instagram/Facebook/LinkedIn and industry trends with verifiable sources, then writes the strategy, a monthly calendar, captions, hooks, CTAs, hashtags, reel scripts, carousel copy and designer briefs. It runs QA and saves all deliverables (Markdown, CSV, Excel, Word) in the repo for human approval. Use when the user gives a client name, website and target month, says "new client", or asks to plan or refresh a client's month. Never publishes.
argument-hint: "<Client name> | <website> | <YYYY-MM>"
---

# Organic Marketing Engine

Runs the full workflow for **one client and one month** inside this Claude Code session. No API keys, hosting or paid services. Research uses `WebSearch` and `WebFetch` (or the `web-fetch` agent). Deliverables are files in `clients/<slug>/`.

## Inputs

Parse the arguments as `Client name | website | YYYY-MM`; commas also work as separators.
- If the month is missing, use **next calendar month**.
- If the website is missing, ask for it once. If there is none, continue and note it.
- If no client is given, create a blank brief with `python tools/new_client.py "<name>" <website> <month>` and ask the operator to fill it in, or offer to interview them (Stage 1).

## Ground rules (from CLAUDE.md)
- **Never publish or schedule anything.** Every post's `approval_status` is `Pending Review`.
- **Never fabricate.** Cite only sources you actually retrieved in this session. Record each in `sources.json` *as you use it*. Anything unverified is labelled `Assumption`.
- **Ask only for business decisions and facts you can't find.** Put questions together and suggest defaults. Never ask for API keys or hosting.
- Work inside `clients/<slug>/` only.

## Progress tracking
Create a task list with the 12 stages below and mark each one as it is completed. Write each stage's file **before** starting the next, so an interrupted run can resume from the files already on disk. When re-running a month, read the existing files first and continue from the first stage that is missing or incomplete.

---

## Stage 1 — Client brief
1. Run `python tools/new_client.py "<Client name>" <website> <YYYY-MM>`. This creates the folders and `00_onboarding/brief.md` and never overwrites existing files.
2. Fill in the brief from what the operator gave you and from public sources (website, public social profiles).
3. If **cadence** isn't given, default to Instagram 3/week, Facebook 2/week, LinkedIn 1/week, and record that in "Assumptions applied".
4. List missing essentials (tone, offers, approvers, sensitive topics) under **Open questions**, each with a default. Ask the operator once. If there's no reply, continue with the defaults marked `Assumed — confirm`.

## Stage 2 — Website & brand analysis → `01_research/brand_analysis.md`
- `WebFetch` the homepage plus up to 3 key pages (about, services or products, contact). If a page fails, record that and use `WebSearch` results.
- Use `WebSearch` for the brand's social profiles, reviews and press mentions.
- Write: positioning, value proposition, brand personality, tone of voice (3 example lines), visual identity (as observed), current content themes, social presence, a social-focused SWOT, and gaps or inconsistencies. Tag each point Fact (source ID), Observation or Assumption.

## Stage 3 — Industry & audience research → `01_research/audience_market.md`
- Research the industry or market in the client's region (size, growth, consumer behaviour, seasonality), key dates in the target month, and regulations that affect marketing claims. Expect about 4–8 searches.
- Build **2–4 personas**: goals, pain points, objections, buying triggers, preferred platforms, content habits, phrases they use. Base them on sources or the brief, and tag the basis.
- Voice of customer: quote public reviews or forums **verbatim only**, with the source.

## Stage 4 — Competitor research → `01_research/competitors.md`
- Identify **3–5 direct competitors** and 1–2 aspirational brands, including any the client named, using search.
- For each: website, active platforms, visible formats, content pillars, tone, standout content, weaknesses. Never invent follower counts or engagement numbers; quote them only if a page shows them, with the date.
- End with a comparison table, opportunities (white space), threats, and formats to adapt (never copy).
- If fewer than 3 can be verified, say so; don't pad the list.

## Stage 5 — Organic social strategy → `02_strategy/organic_strategy.md`
- **Objectives and KPIs** per platform. Give a baseline only if known; otherwise write "Unknown — measure in month 1".
- **3–5 content pillars**: purpose, `mix_percent` (adding up to 100), funnel stage, example topics.
- Messaging pillars with proof points.
- Platform roles, formats and cadence. Label posting windows as Sourced or Test hypothesis.
- Engagement and community plan; hashtag tiers (branded, community, niche, broad); social SEO keywords.
- Measurement plan and test-and-learn hypotheses.

## Stage 6 — Current trend research → `01_research/trends_<YYYY-MM>.md`
Research, with dated sources, aiming for 90 days old or less:
- **Instagram**, **Facebook** and **LinkedIn**: recent official feature and algorithm updates (official newsrooms and help centres first), format trends, recommended practices.
- **Industry trends** for the client's category and region.
- Cultural moments and seasonal events in the target month.

For each trend record: trend, platform, evidence with source ID, relevance, pillar fit, brand-safety risk, shelf life. List the trends you rejected and why.

If a platform changed a limit (caption length, hashtag count), update `tools/platform_rules.json` and cite the source in the trends file.

## Stage 7 — Monthly content calendar → `03_calendar/<slug>_calendar_<YYYY-MM>.json`
1. Work out the posting dates from the cadence. Spread each platform across the week: 1/wk Tue; 2/wk Tue+Thu; 3/wk Mon+Wed+Fri; 4/wk Mon+Tue+Thu+Fri; 5/wk Mon–Fri. Cap at 40 posts unless the operator asks for more.
2. Plan every slot: pillar (matching the strategy mix), objective, a specific topic, format (vary formats to suit the platform), and a **research rationale** that cites source IDs and explains "why this, why now". Anchor posts to key dates and verified trends.
3. Write the JSON using the schema below. IDs are `P01…`, and creative brief IDs are `CB-<YYYY-MM>-<NN>` with matching numbers.

## Stage 8 — Content production (same JSON)
For every post write:
- `hook` plus 2 `alt_hooks`;
- a platform-ready `caption` in the brand voice;
- one `cta` aligned with the objective;
- `hashtags`: each starts with `#`, CamelCase, kept within `platform_rules.json`;
- `alt_text` for images.

Then add the script:
- **Reel / Story / Video:** a full scene-by-scene `script` (time, visual or shot, on-screen text, voiceover or dialogue, audio note, licensed audio only), plus `closing_cta` and `subtitle_note`.
- **Carousel:** slide-by-slide copy, from a cover hook slide through value slides to a CTA slide, 5–10 slides, readable on mobile.
- Other formats: `{"type": "none"}`.

Only include statistics that appear in a cited source.

## Stage 9 — Creative briefs (same JSON, `creative_brief` object)
Write `visual_direction` (one paragraph) and a brief a designer can work from without follow-up questions:
- summary; specs (aspect ratio, pixel size, duration, file type, safe zones, frame or slide count);
- key message; on-screen copy; mood and style (describe references, never copy them);
- colour palette, typography, brand assets (Canva Brand Kit if the client has one);
- shot list or layout; audio direction; accessibility (captions, contrast, alt text);
- dos and don'ts; deadline; reviewer.

## Stage 10 — Quality checks
1. Run `python tools/build_exports.py clients/<slug> <YYYY-MM>`, then `python tools/qa_check.py clients/<slug> <YYYY-MM>`.
2. Fix every **FAIL** in the JSON and re-run until there are 0 failures. Fix warnings where it makes sense, or explain why one is acceptable.
3. Editorial review of every post, as a strict senior editor:
   - claims backed by sources or the brief; no invented client facts;
   - no health, financial or legal claims; avoided words respected;
   - brand voice; grammar and spelling; inclusive language; cultural sensitivity;
   - audio and copyright; accessibility; hook and CTA strength.

   Fix the problems, then write `06_qa/<slug>_qa_<YYYY-MM>.md` with the checklist results, the issues you fixed, and any open risks that need the operator's decision.

## Stage 11 — Files & downloads
1. Make sure `01_research/sources.json` is complete (every cited ID, with URL and access date).
2. Run `python tools/build_exports.py clients/<slug> <YYYY-MM>` again. If libraries are missing, run `pip install -r requirements.txt` first. It produces:
   - `01_research/sources.md` (source table generated from `sources.json`)
   - `03_calendar/…csv`, `04_content/…md`, `05_creative_briefs/…md`
   - `07_delivery/<slug>_calendar_<YYYY-MM>.xlsx`: calendar, summary and sources sheets, with an **Approval Status dropdown**
   - `07_delivery/<slug>_approval-pack_<YYYY-MM>.docx`: every document in one Word file
3. Run `python tools/qa_check.py …` one last time (it must show 0 failures) and `python -m pytest -q`.

## Stage 12 — Prepare for approval
1. Write `07_delivery/approval_summary.md` with:
   - posts by platform and pillar;
   - key dates and trends used;
   - QA result;
   - open questions and assumptions to confirm;
   - how to approve: set the Approval Status per post in the Excel file, or tell Claude "approve P01–P05, change P06: …";
   - the statement: **"Nothing has been published."**
2. Update `clients/<slug>/README.md` with the status.
3. `git add clients/<slug> tools/platform_rules.json`, then commit (`<Client> — organic social plan <YYYY-MM>`) and push to the working branch.
4. Reply to the operator in plain language: what was produced, the file paths (Excel and Word first), what needs their decision, and how to approve.

---

## Approval follow-ups
When the operator says, for example, "approve P01–P05, change P07 to a carousel":
- set `approval_status` and `approved_by` (the operator's name or "Operator"), plus `reviewer_comments` where given;
- for change requests, rewrite the post and keep it `Pending Review`;
- then re-run the exports and QA, and commit.

Approval only marks content as ready. You still never post it.

---

## Calendar JSON schema

```json
{
  "client": "Client Name",
  "month": "2026-12",
  "timezone": "America/Los_Angeles",
  "pillars": [{"name": "Educate", "mix_percent": 40, "funnel_stage": "Awareness"}],
  "posts": [{
    "id": "P01",
    "date": "2026-12-01",
    "time": "11:00",
    "platform": "Instagram",
    "content_pillar": "Educate",
    "objective": "Awareness",
    "topic": "…",
    "research_rationale": "Why this post, why now …",
    "source_ids": ["S3", "S7"],
    "hook": "…",
    "alt_hooks": ["…", "…"],
    "caption": "…",
    "cta": "…",
    "hashtags": ["#BrandName", "#NicheTag"],
    "format": "Carousel",
    "script": {
      "type": "carousel",
      "slides": [{"n": 1, "headline": "…", "body": "…"}],
      "scenes": [{"time": "0-3s", "visual": "…", "on_screen_text": "…", "voiceover": "…", "audio": "…"}],
      "duration_seconds": 0,
      "closing_cta": "…",
      "subtitle_note": "…"
    },
    "alt_text": "…",
    "visual_direction": "…",
    "creative_brief": {
      "id": "CB-2026-12-01", "summary": "…", "specs": "…", "key_message": "…", "on_screen_copy": "…",
      "mood_and_style": "…", "colour_palette": "…", "typography": "…", "assets": "…",
      "shot_list": ["…"], "audio_direction": "…", "accessibility": "…",
      "dos": ["…"], "donts": ["…"], "deadline": "2026-11-24", "reviewer": "…"
    },
    "kpi_objective": "Saves ≥ 3% of reach",
    "approval_status": "Pending Review",
    "approved_by": "",
    "reviewer_comments": ""
  }]
}
```

Formats: `Reel`, `Carousel`, `Static image`, `Story`, `Video`, `Text post`. Objectives: `Awareness`, `Engagement`, `Traffic`, `Leads`, `Sales`, `Community`, `Retention`.

## sources.json schema
```json
{"client": "…", "sources": [{"id": "S1", "title": "…", "publisher": "…", "url": "https://…",
  "published": "2026-10-14", "accessed": "2026-11-06", "used_in": ["trends", "P03"], "note": "what it supports"}]}
```
