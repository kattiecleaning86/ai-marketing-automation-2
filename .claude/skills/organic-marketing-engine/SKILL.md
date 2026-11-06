---
name: organic-marketing-engine
description: End-to-end organic social media marketing workflow for a client — onboarding, brand/audience/market/competitor research, strategy, verified trend research, monthly content calendar, full content production (hooks, captions, CTAs, hashtags, reel scripts, carousel copy), creative briefs, QA, Google Drive/Sheets delivery, and Slack approval notification. Use whenever starting, continuing, or refreshing organic social work for any client or month. Never publishes content; everything ends at human approval.
---

# Organic Marketing Engine

A reusable, repeatable workflow for producing a complete month of organic social media marketing for one client. Run all 12 stages in order. Each stage has inputs, actions, outputs, and an exit check. Do not skip stages; if a stage is blocked, record why in the client README and continue with whatever does not depend on it.

## Ground Rules (always apply)

- **No publishing.** This skill ends at "awaiting human approval". Never post, schedule, or arm any publishing tool.
- **No fabrication.** Every statistic, trend, or market claim needs: claim, source, URL, publish date, access date. Unverifiable items are labelled `Assumption` or removed.
- **One client at a time.** Work only inside `clients/<client-slug>/`. Never reuse another client's data.
- **Ask only for what is necessary:** credentials, authorizations, permissions, business decisions. Batch questions, give a recommended default for each.
- **Integrations only if authorized.** If Drive/Sheets/Slack/Canva access is not configured, produce local files and mark the delivery step as `Pending integration`.

## Inputs

- Client name (required) and target month `YYYY-MM` (default: next calendar month).
- Any brief, brand guidelines, assets, or links the operator supplies.

## Outputs (per client, per month)

```
clients/<client-slug>/
  00_onboarding/brief.md
  01_research/brand_analysis.md
  01_research/audience_market.md
  01_research/competitors.md
  01_research/trends_<YYYY-MM>.md
  01_research/sources.md
  02_strategy/organic_strategy.md
  03_calendar/<client-slug>_calendar_<YYYY-MM>_v1.csv
  04_content/<client-slug>_content_<YYYY-MM>_v1.md
  05_creative_briefs/<client-slug>_briefs_<YYYY-MM>_v1.md
  06_qa/<client-slug>_qa_<YYYY-MM>_v1.md
  07_delivery/delivery_log.md
  README.md
```

---

## Stage 1 — Client Onboarding & Brief Collection

**Goal:** Capture everything needed to work autonomously for the rest of the workflow.

**Actions**
1. Create the client folder structure above (slug = lowercase, hyphenated client name).
2. Fill `00_onboarding/brief.md` with what is already known. Collect or confirm:
   - Business: name, website, industry, locations served, products/services, price positioning, current offers.
   - Goals: primary business goal (awareness, leads, sales, community, retention) and 90-day targets.
   - Audience: who they serve, known customer segments, languages.
   - Brand: mission, values, tone of voice, words to use/avoid, visual guidelines (logo, colors, fonts), existing Canva brand kit.
   - Channels: active platforms + handles, posting history, follower counts (from public profiles), what has worked/not worked.
   - Competitors the client already knows about.
   - Constraints: compliance/legal limits, sensitive topics, approval chain, approvers' names, turnaround times.
   - Content resources: photo/video library, people available to appear on camera, UGC rights.
   - Cadence/budget decisions: posts per week per platform, production capacity.
   - Access status: Google Drive folder, Google Sheet, Slack channel, Canva — authorized yes/no.
3. Pull what you can from public sources (website, public social profiles) before asking anything.
4. Compile only the **missing, essential** items into one batched question list for the operator, each with a recommended default.

**Exit check:** brief complete or gaps explicitly listed with defaults applied and marked `Assumed — confirm`.

---

## Stage 2 — Brand Analysis

**Goal:** Understand how the brand currently shows up and where it can win.

**Actions**
- Review website and each active social profile (bio, highlights, last 20–30 posts where visible).
- Document: positioning statement, unique value proposition, brand personality, tone of voice (with 3 example lines), visual identity, current content themes, best-performing visible posts (by public engagement), gaps and inconsistencies.
- Produce a brand SWOT focused on social.

**Output:** `01_research/brand_analysis.md` — mark each point as Fact / Observation / Assumption.

---

## Stage 3 — Audience & Market Research

**Goal:** Define who the content is for and what they care about.

**Actions**
- Build 2–4 audience personas: demographics (only from sources or client data), goals, pain points, objections, buying triggers, content they consume, preferred platforms, language/phrases they use.
- Research the market: category size/growth (sourced), seasonality, key dates/holidays/events for the target month and region, regulatory notes.
- Mine verifiable voice-of-customer signals: public reviews, comments, forums, Q&A — quote only what is public and attribute it.

**Output:** `01_research/audience_market.md` with sources logged in `01_research/sources.md`.

---

## Stage 4 — Competitor Research

**Goal:** Find white space and proven formats.

**Actions**
- Identify 3–5 direct competitors and 1–2 aspirational/adjacent brands (client-named + researched).
- For each: platforms, approx. posting frequency, formats used, content pillars, tone, visible engagement on recent posts, standout posts, weaknesses.
- Summarize in a comparison table, then list: opportunities (gaps), threats, formats/angles to adapt (never copy).

**Output:** `01_research/competitors.md`.

---

## Stage 5 — Organic Social Media Strategy

**Goal:** A clear, client-specific plan that every post maps back to.

**Define**
- **Objectives & KPIs** per platform (e.g. reach, saves, shares, profile visits, link clicks, DMs, follower growth, engagement rate) with baseline (if known) and target.
- **Positioning & messaging pillars** — key messages and proof points.
- **Content pillars** (3–5) with purpose, % of mix, and example topics. e.g. Educate / Inspire / Behind-the-scenes / Community & UGC / Offer.
- **Platform strategy:** role of each platform, formats, cadence, best posting windows (sourced or from client data; otherwise mark as test hypothesis).
- **Funnel mapping:** awareness / consideration / conversion / loyalty per pillar.
- **Engagement & community plan:** reply guidelines, comment prompts, collaboration/creator ideas.
- **Hashtag & keyword strategy:** branded, community, niche, broad tiers; social SEO keywords.
- **Measurement plan:** what to track, review cadence, test-and-learn hypotheses.

**Output:** `02_strategy/organic_strategy.md`.

---

## Stage 6 — Current Trend Research

**Goal:** Ground the month in what is actually current and relevant.

**Actions**
- Research, with dated verifiable sources: platform feature/algorithm updates (official newsrooms/help centers), format trends, cultural moments and relevant seasonal events for the target month, industry-specific conversations, trending audio/formats where they can be verified.
- For each trend record: trend, platform, evidence (source + URL + date + access date), relevance to the client, fit with pillars, risk/brand-safety notes, shelf life.
- Reject trends that cannot be verified or do not fit the brand. **Never invent a trend.** If live research tools are unavailable, state that and mark the trend section `Pending verification`.

**Output:** `01_research/trends_<YYYY-MM>.md` + entries in `01_research/sources.md`.

---

## Stage 7 — Monthly Content Calendar

**Goal:** A complete, balanced posting plan for the month.

**Actions**
- Apply the cadence agreed in Stage 1 across each platform.
- Balance pillar mix and funnel stages per the strategy; avoid repeating topics or hooks.
- Anchor posts to key dates/events and verified trends from Stage 6.
- Every entry must include **all** of the fields below.

### Required Calendar Fields

| # | Field | Description |
|---|---|---|
| 1 | **Date** | Publish date `YYYY-MM-DD` (+ suggested time and time zone if known) |
| 2 | **Platform** | Instagram, Facebook, TikTok, LinkedIn, YouTube Shorts, Pinterest, X, Threads, etc. |
| 3 | **Content pillar** | One of the strategy's pillars |
| 4 | **Objective** | Awareness / Engagement / Traffic / Leads / Sales / Community / Retention |
| 5 | **Topic** | Specific subject of the post |
| 6 | **Research rationale** | Why this post, why now — cite the research finding, persona insight, competitor gap, or trend (with source ID from `sources.md`) |
| 7 | **Hook** | First line / first 1–3 seconds that stops the scroll |
| 8 | **Caption** | Full, platform-ready caption |
| 9 | **CTA** | One clear call-to-action |
| 10 | **Hashtags** | Platform-appropriate set, tiered per strategy |
| 11 | **Format** | Reel / Short / Carousel / Static image / Story / Video / Text post / Live / etc. |
| 12 | **Reel script or carousel slide copy** | Scene-by-scene script (time, visual, on-screen text, VO/dialogue, audio) or slide-by-slide copy; `N/A` only for formats without either |
| 13 | **Visual direction** | Look, composition, colours, on-screen text style, assets to use |
| 14 | **Creative brief** | Reference ID linking to the full brief in `05_creative_briefs/` (e.g. `CB-2026-12-07`) plus a one-line summary |
| 15 | **KPI objective** | Primary metric + target for this post (e.g. "Saves ≥ 3% of reach") |
| 16 | **Approval status** | `Pending Review` by default; later `Changes Requested` / `Approved` / `Rejected` — set only by a human |

**Output:** `03_calendar/<client-slug>_calendar_<YYYY-MM>_v1.csv` with exactly these columns in this order:

```
Date,Platform,Content Pillar,Objective,Topic,Research Rationale,Hook,Caption,CTA,Hashtags,Format,Reel Script / Carousel Slide Copy,Visual Direction,Creative Brief,KPI Objective,Approval Status
```

Also add a short calendar overview (pillar mix %, platform split, key dates) at the top of the content document.

---

## Stage 8 — Complete Content Production

**Goal:** Every calendar entry is fully written and ready for design/editing.

**For each entry produce**
- **Hooks:** primary hook + 2 alternates for A/B consideration.
- **Caption:** final copy written in brand voice, with line breaks, platform-appropriate length, accessibility in mind (camel-case hashtags, minimal emoji clutter).
- **CTA:** specific and aligned to the objective.
- **Hashtags:** within platform norms; branded + niche + community mix; no banned or irrelevant tags.
- **Reel/short-form script:** duration, scene-by-scene table (timestamp, shot/visual, on-screen text, voiceover/dialogue, audio/sound note), closing CTA, caption/subtitle note.
- **Carousel copy:** slide-by-slide (cover hook slide → value slides → CTA slide), with word counts suitable for mobile.
- **Alt text** for images and **subtitles** note for video.

**Output:** `04_content/<client-slug>_content_<YYYY-MM>_v1.md`, organized by date, and synced into the calendar CSV.

---

## Stage 9 — Creative Briefs (Designers & Video Editors)

**Goal:** Hand-off documents that let a designer or editor produce the asset without follow-up questions.

**Each brief (ID `CB-<YYYY-MM>-<NN>`) includes**
- Post reference (date, platform, format) and objective/KPI.
- Deliverable specs: dimensions/aspect ratio, duration, file type, safe zones, number of frames/slides.
- Key message and hook; full on-screen copy / slide copy.
- Visual direction: mood, style references (describe; link only to properly sourced references), colour palette, typography, brand assets, Canva template link if available.
- Shot list (video): scenes, angles, b-roll, talent, props, locations.
- Audio: music/sound direction (use licensed or platform-library audio only).
- Accessibility: captions, contrast, alt text.
- Do / Don't list from brand guidelines.
- Deadline and reviewer.

**Output:** `05_creative_briefs/<client-slug>_briefs_<YYYY-MM>_v1.md`.

---

## Stage 10 — Quality Assurance

**Goal:** Nothing ships with errors, fabricated claims, or brand drift.

Run and record every check (Pass / Fix / Fail with notes):

- [ ] **Sources:** every stat/trend has a verifiable, dated source in `sources.md`; no fabricated data.
- [ ] **Client facts:** offers, prices, product details match the brief.
- [ ] **Completeness:** all 16 calendar fields filled for every entry.
- [ ] **Strategy alignment:** each post maps to pillar, objective, funnel stage, KPI; pillar mix matches strategy.
- [ ] **Brand voice & visuals:** tone, vocabulary, do/don't lists respected.
- [ ] **Platform specs:** caption length, hashtag counts, aspect ratios, durations.
- [ ] **Language:** spelling, grammar, clarity, inclusive language, localisation.
- [ ] **Compliance & risk:** no misleading/health/financial/legal claims; disclosures; copyright and audio licensing; brand-safety of trends.
- [ ] **Accessibility:** alt text, subtitles, readable contrast, camel-case hashtags.
- [ ] **Uniqueness:** no duplicate hooks/topics; no copied competitor content.
- [ ] **Approval status:** every entry is `Pending Review`.

Fix everything fixable, re-check, then write `06_qa/<client-slug>_qa_<YYYY-MM>_v1.md` with a summary, issues found/fixed, and any open risks needing human decisions.

**Exit check:** zero open `Fail` items, or failures escalated to the operator.

---

## Stage 11 — Google Drive & Google Sheets Delivery

**Prerequisite:** operator-authorized Google access. If not available, skip to local delivery and log `Pending integration`.

**Actions**
1. In Google Drive, create/find `Organic Social — <Client Name>` and mirror the local folder structure; upload research, strategy, content, briefs, and QA docs for the month.
2. In Google Sheets, create/update `<Client Name> — Content Calendar` with one tab per month (`YYYY-MM`), columns exactly as in Stage 7, header frozen, `Approval Status` as a dropdown (`Pending Review`, `Changes Requested`, `Approved`, `Rejected`), and a column for reviewer comments.
3. Share only with authorized people/permissions agreed by the operator.
4. Record all links, file versions, and timestamps in `07_delivery/delivery_log.md`.

---

## Stage 12 — Slack Approval Notification

**Prerequisite:** operator-authorized Slack access and a designated channel/approvers. If not available, draft the message in `07_delivery/delivery_log.md` for the operator to send.

**Message template**
```
:calendar: <Client Name> — Organic Social Content for <Month YYYY> is ready for review.

• Posts: <N> across <platforms>
• Pillar mix: <summary>
• Key dates/trends covered: <summary>
• QA: passed (<N> issues fixed, <N> open items needing decisions)

:page_facing_up: Calendar (Sheet): <link>
:file_folder: Drive folder: <link>

Please review and set Approval Status for each post in the Sheet
(Approved / Changes Requested / Rejected) by <date>.
Nothing will be published until it is marked Approved.
```

**Rules**
- Slack is for notification and approval collection only — it must never trigger publishing.
- Record send time and recipients in the delivery log.

---

## Completion & Status Update

At the end of every run:
1. Update `clients/<client-slug>/README.md`: month, stage reached, approval state, open questions, blockers.
2. Update the implementation status in `CLAUDE.md` / `docs/STATUS.md` if anything about the system changed.
3. Report back to the operator in plain language: what was produced, where it is, what needs their decision or approval, and the recommended next step.
