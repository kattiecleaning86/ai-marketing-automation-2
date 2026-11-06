"""JSON schemas for Claude structured outputs (one per workflow stage)."""
from __future__ import annotations

PLATFORMS = ["Instagram", "Facebook", "TikTok", "LinkedIn", "YouTube Shorts", "Pinterest", "X", "Threads"]
FORMATS = ["Reel", "Short", "Carousel", "Static image", "Story", "Video", "Text post"]
OBJECTIVES = ["Awareness", "Engagement", "Traffic", "Leads", "Sales", "Community", "Retention"]
FUNNEL = ["Awareness", "Consideration", "Conversion", "Loyalty"]
BASIS = ["Fact", "Observation", "Assumption"]


def S() -> dict:
    return {"type": "string"}


def I() -> dict:
    return {"type": "integer"}


def A(items: dict) -> dict:
    return {"type": "array", "items": items}


def E(values: list[str]) -> dict:
    return {"type": "string", "enum": values}


def O(**props: dict) -> dict:
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


CLAIM = O(point=S(), basis=E(BASIS), source_ids=A(S()))

BRAND = O(
    summary=S(),
    positioning=S(),
    value_proposition=S(),
    brand_personality=A(S()),
    tone_of_voice=O(description=S(), example_lines=A(S())),
    visual_identity=S(),
    current_content_themes=A(S()),
    social_presence=A(CLAIM),
    strengths=A(CLAIM),
    weaknesses=A(CLAIM),
    opportunities=A(CLAIM),
    threats=A(CLAIM),
    gaps_and_inconsistencies=A(CLAIM),
)

AUDIENCE = O(
    summary=S(),
    personas=A(O(
        name=S(), description=S(), goals=A(S()), pain_points=A(S()), objections=A(S()),
        buying_triggers=A(S()), preferred_platforms=A(S()), content_preferences=A(S()),
        phrases_they_use=A(S()), basis=E(BASIS), source_ids=A(S()),
    )),
    market_overview=A(CLAIM),
    seasonality=A(CLAIM),
    key_dates=A(O(date=S(), event=S(), relevance=S(), source_ids=A(S()))),
    regulatory_notes=A(CLAIM),
    voice_of_customer=A(O(quote=S(), where=S(), source_ids=A(S()))),
)

COMPETITORS = O(
    summary=S(),
    competitors=A(O(
        name=S(), website=S(), type=E(["Direct", "Aspirational"]), platforms=A(S()),
        posting_frequency=S(), formats=A(S()), content_pillars=A(S()), tone=S(),
        standout_content=A(S()), weaknesses=A(S()), source_ids=A(S()),
    )),
    opportunities=A(CLAIM),
    threats=A(CLAIM),
    formats_to_adapt=A(S()),
)

STRATEGY = O(
    summary=S(),
    positioning=S(),
    objectives=A(O(platform=S(), objective=S(), kpis=A(O(metric=S(), baseline=S(), target=S())))),
    messaging_pillars=A(O(message=S(), proof_points=A(S()))),
    content_pillars=A(O(name=S(), purpose=S(), mix_percent=I(), funnel_stage=E(FUNNEL), example_topics=A(S()))),
    platform_strategy=A(O(
        platform=S(), role=S(), formats=A(S()), cadence=S(), posting_windows=S(),
        posting_windows_basis=E(["Client data", "Sourced", "Test hypothesis"]),
    )),
    engagement_plan=A(S()),
    hashtag_strategy=O(branded=A(S()), community=A(S()), niche=A(S()), broad=A(S())),
    social_seo_keywords=A(S()),
    measurement_plan=A(S()),
    test_hypotheses=A(S()),
)

TRENDS = O(
    summary=S(),
    trends=A(O(
        trend=S(), platform=S(), evidence=S(), source_ids=A(S()), relevance=S(),
        pillar_fit=A(S()), risk_notes=S(), shelf_life=S(),
    )),
    rejected=A(O(trend=S(), reason=S())),
)

CALENDAR = O(entries=A(O(
    slot=I(), content_pillar=S(), objective=E(OBJECTIVES), topic=S(), research_rationale=S(),
    source_ids=A(S()), format=E(FORMATS), kpi_objective=S(), suggested_time=S(),
)))

COPY = O(posts=A(O(
    post_key=S(), hook=S(), alt_hooks=A(S()), caption=S(), cta=S(), hashtags=A(S()), alt_text=S(),
)))

SCRIPTS = O(posts=A(O(
    post_key=S(),
    script_type=E(["reel_script", "carousel", "none"]),
    duration_seconds=I(),
    scenes=A(O(timestamp=S(), visual=S(), on_screen_text=S(), voiceover=S(), audio=S())),
    slides=A(O(slide_number=I(), headline=S(), body=S())),
    closing_cta=S(),
    subtitle_note=S(),
)))

BRIEFS = O(posts=A(O(
    post_key=S(),
    visual_direction=S(),
    summary=S(),
    specs=S(),
    key_message=S(),
    on_screen_copy=S(),
    mood_and_style=S(),
    colour_palette=S(),
    typography=S(),
    assets=S(),
    shot_list=A(S()),
    audio_direction=S(),
    accessibility=S(),
    dos=A(S()),
    donts=A(S()),
)))

QA_REVIEW = O(
    overall_notes=S(),
    issues=A(O(post_key=S(), severity=E(["fail", "warn"]), category=S(), issue=S(), fix_instruction=S())),
)

QA_FIX = O(posts=A(O(post_key=S(), hook=S(), caption=S(), cta=S(), hashtags=A(S()))))
