# Apex Web Studios — QA Report, December 2026 (v1)

- **Date:** 2026-11-07
- **Scope:** 18 calendar entries, the content doc, creative briefs, strategy and research
- **Result:** **Passed with holds.** There are no open `Fail` items. Every source-verification and client-input item is escalated below. **All 18 posts remain `Pending Review`.**

## Checklist

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | **Sources** | **Fix → escalated** | Every stat and trend in the content has a source ID in `sources.md`. **No fabricated data.** However, all T-sources are *search-located*, not read in full (network policy). They must be opened and confirmed before approval (list below). The outdated speed stat (C08) and vendor stats (C03, C04) were deliberately kept **out** of content. |
| 2 | **Client facts** | Pass (with confirmations) | Prices and inclusions were checked line by line against the pricing page (B04, read 2026-11-06). Guarantee wording matches B04. "48 hours" and "dedicated project manager" match B04. Testimonial quotes match B08 verbatim. **No self-reported stats used** (they conflict across pages). |
| 3 | **Completeness** | Pass | Automated check: 18 rows × 16 columns, no empty cells, column order exactly as the skill specifies. |
| 4 | **Strategy alignment** | Pass | Each post has a pillar, objective, funnel stage, persona and KPI. Mix: Educate 39% (target 40%), Proof 11% (15%), Behind the Build 22% (20%), Offers 17% (15%), Community 11% (10%). Proof is lower because testimonial permissions are pending. Add a third proof post in January once case studies exist. |
| 5 | **Brand voice & visuals** | Pass | Confident and direct, using the site's own lines ("No surprises. No radio silence. No hidden costs."; "No confusing proposals…"). Superlatives and guarantees removed. Briefs use the site palette and fonts. |
| 6 | **Platform specs** | Pass | Automated: Instagram captions 147–695 characters (limit 2,200); LinkedIn 357–946 (limit 3,000). Hashtags: Instagram ≤ 5, LinkedIn 3. Aspect ratios and durations set in each brief. |
| 7 | **Language** | Pass | Canadian/US-neutral spelling (colour in internal docs; captions avoid region-specific spellings where possible). No health, financial or legal claims. Accessibility posts carry "general information, not legal advice". Verbatim client quotes were chosen to avoid reproducing typos. Pronoun-neutral wording for named clients. |
| 8 | **Compliance & risk** | Pass with holds | No ranking or results guarantees. "Small Business Saturday" (American Express trademark) not used. AI-search figures are attributed and labelled as correlations. The ADA figure is qualified as covering all Title III claims. Audio: licensed or in-app library only. Testimonials and team appearances need consent (holds below). |
| 9 | **Accessibility** | Pass | Alt text written for every post. Burned-in captions specified for all video. Contrast ≥ 4.5:1 in briefs. CamelCase hashtags (automated check). Emoji kept light. |
| 10 | **Uniqueness** | Pass | No duplicate hooks (automated check). The package topic appears twice with different angles (LinkedIn full price list on Dec 9; Instagram Starter-only on Dec 18). No competitor content reused. All visuals use Apex's own or demo material (Instagram originality, TR8). |
| 11 | **Approval status** | Pass | 18 of 18 posts are `Pending Review` (automated count). |

## Holds — sources to verify before approval (open each URL and confirm the claim)

| Post | Claim used | Source |
|---|---|---|
| Dec 1 LinkedIn | Adobe forecast of a record US online holiday season | T53 |
| Dec 3 LinkedIn | 5,006 federal ADA Title III lawsuits in H1 2026, +9% YoY (all Title III) | T45 |
| Dec 3 both | IDPD on Dec 3 | T56 |
| Dec 3 LinkedIn | WCAG AA contrast 4.5:1 for body text | W3C WCAG 2.1 SC 1.4.3 (standard reference: https://www.w3.org/TR/WCAG21/#contrast-minimum — not fetched in session) |
| Dec 4 Instagram | Hanukkah begins at sundown Dec 4, 2026 | T57, T58 |
| Dec 8 LinkedIn | 68% zero-click (SparkToro via Search Engine Land); ~58% lower CTR (Ahrefs); cited pages earn more clicks (Seer) | T35, T34, T37 |
| Dec 10 Instagram | Google I/O 2026 announced AI Mode features that check availability with local businesses | T38 |
| Dec 15 LinkedIn | Wix Harmony launched Jan 2026; Squarespace Blueprint AI | T49, T50 |

**Fastest path:** allow the hosts listed in `sources.md` for this repo's environment, and Claude re-verifies all of these automatically. The alternative is a manual check by the operator.

## Holds — client input required

| Post | What's needed |
|---|---|
| Dec 2 Instagram | Confirm the Hour 0–48 process reflects reality; nominate an on-camera PM |
| Dec 9 Instagram | Written permission: Body Rituals Spa, UpkeepX, Copy Smart reviews |
| Dec 9 LinkedIn, Dec 18 Instagram | Confirm December prices and inclusions unchanged |
| Dec 16 Instagram | 3 team members: names, roles, on-camera consent |
| Dec 17 LinkedIn | PM nominee; confirm the described update practice |
| Dec 22 LinkedIn | Written permission from Jamar Root |
| Dec 24 Instagram | Holiday office hours |
| Dec 29 LinkedIn | 3 real team reflections, photos, consent |
| Dec 30 Instagram | January call availability |

**Ready to approve once sources are verified (no client input needed):** Dec 1, Dec 3 (×2), Dec 4, Dec 8, Dec 10, Dec 15, Dec 22 Instagram.

## Issues found and fixed during QA

1. A testimonial caption described UpkeepX and Copy Smart by business type, which was not in the source. Replaced with their names only.
2. Starter package copy said "not a template", an inference. Replaced with the site's own wording, "tailored layout design".
3. The Jamar Root hook quoted a phrase containing a typo. Switched to a different verbatim sentence from the same review.
4. Pronouns were inferred for a named client. Rewritten to be neutral.
5. Instagram hashtag sets of 6–7 trimmed to ≤ 5.

## Open risks for human decision

- **Self-reported stats conflict** across the website (e.g. "+1K Clients" vs "45+ Clients"). Recommend fixing the site before social pushes traffic there.
- **Homepage testimonial cards appear mismatched:** a video-testimonial name sits next to another client's quote (B01). Fix before the Proof posts link to the site.
- **Instagram account identity:** `@apexwebstudios` (site) vs `@apex_web_design` (search result).
- **Competitor set is provisional**, built on the wrong-market assumption and snippet data.
