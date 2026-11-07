# Apex Web Studios — Client Status

| Item | Status |
|---|---|
| Client | Apex Web Studios — https://apexwebstudios.net/ (HQ Milton, ON; offices in LA and Birmingham, UK) |
| Slug | `apexwebstudios` |
| Current month | **2026-12** |
| Stage reached | 10 of 12: QA complete. Stages 11–12 (Drive/Sheets, Slack) are `Pending integration`. |
| Approval state | **18 of 18 posts Pending Review.** Nothing scheduled or published. |
| Review requested by | 2026-11-20, which leaves time for production before Dec 1 |

## Deliverables (2026-12, v1)

- Onboarding: [`00_onboarding/brief.md`](00_onboarding/brief.md) (includes 11 batched questions with defaults)
- Research: [`01_research/`](01_research/) — brand analysis, audience & market, competitors (provisional), trends, source register
- Strategy: [`02_strategy/organic_strategy.md`](02_strategy/organic_strategy.md)
- Calendar: [`03_calendar/apexwebstudios_calendar_2026-12_v1.csv`](03_calendar/apexwebstudios_calendar_2026-12_v1.csv)
- Content: [`04_content/apexwebstudios_content_2026-12_v1.md`](04_content/apexwebstudios_content_2026-12_v1.md). The generator script that produces the calendar, content and briefs from one source is at [`04_content/_source/generate_2026-12.py`](04_content/_source/generate_2026-12.py).
- Briefs: [`05_creative_briefs/apexwebstudios_briefs_2026-12_v1.md`](05_creative_briefs/apexwebstudios_briefs_2026-12_v1.md)
- QA: [`06_qa/apexwebstudios_qa_2026-12_v1.md`](06_qa/apexwebstudios_qa_2026-12_v1.md)
- Delivery log and Slack draft: [`07_delivery/delivery_log.md`](07_delivery/delivery_log.md)

## Blockers

1. **Source verification.** Trend and platform sources were found through web search, but their pages are blocked by the network policy. Fix: allow the hosts listed in `01_research/sources.md` for the `ai-marketing-automation-2` environment, or verify manually.
2. **Social profiles unreachable.** Instagram, Facebook, LinkedIn and X are blocked, and Trustpilot and Clutch block bots. The social audit and KPI baselines are pending; the operator should share analytics.
3. **Client inputs and permissions** for 10 posts (see the QA report).

## Open questions

See the brief's §"Batched questions". The top three:
1. Which Instagram account is official?
2. Testimonial reuse permission.
3. Confirm December pricing.

## Next steps

1. Operator answers the brief questions and supplies client inputs.
2. Claude verifies sources (once hosts are allowed), applies the answers, and produces v2.
3. Human sets Approval Status per post.
4. Production starts from the briefs (assets due 3 business days before each post).
