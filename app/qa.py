"""Deterministic (rule-based) quality checks for calendar entries.

These run in code, so they are exact and repeatable. A second, Claude-based review checks
brand voice and unsupported claims (see engine.stage_qa).
"""
from __future__ import annotations

import re
from collections import Counter

# Hard platform limits (post fails QA) and recommended maxima (warning only).
CAPTION_LIMITS = {"Instagram": 2200, "TikTok": 4000, "LinkedIn": 3000, "X": 280, "Threads": 500,
                  "Pinterest": 500, "Facebook": 63206, "YouTube Shorts": 5000}
HASHTAG_HARD_MAX = {"Instagram": 30}
HASHTAG_RECOMMENDED_MAX = {"Instagram": 15, "TikTok": 6, "LinkedIn": 5, "X": 3, "Threads": 3,
                           "Facebook": 5, "Pinterest": 10, "YouTube Shorts": 5}
VIDEO_FORMATS = {"Reel", "Short", "Video", "Story"}

REQUIRED_FIELDS = [
    ("date", "Date"), ("platform", "Platform"), ("content_pillar", "Content pillar"),
    ("objective", "Objective"), ("topic", "Topic"), ("research_rationale", "Research rationale"),
    ("hook", "Hook"), ("caption", "Caption"), ("cta", "CTA"), ("hashtags", "Hashtags"),
    ("format", "Format"), ("script_text", "Reel script / carousel slide copy"),
    ("visual_direction", "Visual direction"), ("brief_id", "Creative brief"),
    ("kpi_objective", "KPI objective"), ("approval_status", "Approval status"),
]

NUMBER_CLAIM = re.compile(r"\b\d+(?:[.,]\d+)?\s?(?:%|percent|x\b|times\b|million|billion)", re.I)


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (text or "").lower()).strip()


def check_posts(posts: list[dict], valid_source_ids: set[str], pillar_targets: dict[str, int] | None = None) -> dict:
    """Return {"posts": {post_key: [issues]}, "global": [issues], "counts": {...}}.

    Each issue is {"severity": "fail"|"warn", "check": str, "issue": str}.
    """
    per_post: dict[str, list[dict]] = {p["post_key"]: [] for p in posts}

    def add(key: str, sev: str, check: str, issue: str):
        per_post[key].append({"severity": sev, "check": check, "issue": issue})

    hooks = Counter(_norm(p.get("hook", "")) for p in posts if p.get("hook"))
    topics = Counter(_norm(p.get("topic", "")) for p in posts if p.get("topic"))

    for p in posts:
        k = p["post_key"]
        for field, label in REQUIRED_FIELDS:
            val = p.get(field)
            if val in (None, "", []):
                add(k, "fail", "Completeness", f"Missing field: {label}")
        plat = p.get("platform", "")
        cap = p.get("caption") or ""
        tags = p.get("hashtags") or []
        if plat in CAPTION_LIMITS and len(cap) > CAPTION_LIMITS[plat]:
            add(k, "fail", "Platform specs", f"Caption is {len(cap)} chars; {plat} limit is {CAPTION_LIMITS[plat]}")
        if plat in HASHTAG_HARD_MAX and len(tags) > HASHTAG_HARD_MAX[plat]:
            add(k, "fail", "Platform specs", f"{len(tags)} hashtags; {plat} allows {HASHTAG_HARD_MAX[plat]}")
        elif plat in HASHTAG_RECOMMENDED_MAX and len(tags) > HASHTAG_RECOMMENDED_MAX[plat]:
            add(k, "warn", "Platform specs", f"{len(tags)} hashtags; recommended max for {plat} is {HASHTAG_RECOMMENDED_MAX[plat]}")
        for t in tags:
            if not re.fullmatch(r"#[\w]+", t or ""):
                add(k, "warn", "Hashtags", f"Malformed hashtag: {t!r}")
                break
        fmt = p.get("format", "")
        script = p.get("script") or {}
        if fmt in VIDEO_FORMATS and not script.get("scenes"):
            add(k, "fail", "Completeness", f"{fmt} has no scene-by-scene script")
        if fmt == "Carousel" and len(script.get("slides") or []) < 2:
            add(k, "fail", "Completeness", "Carousel needs at least 2 slides of copy")
        if p.get("hook") and hooks[_norm(p["hook"])] > 1:
            add(k, "warn", "Uniqueness", "Hook duplicates another post's hook")
        if p.get("topic") and topics[_norm(p["topic"])] > 1:
            add(k, "warn", "Uniqueness", "Topic duplicates another post")
        sids = p.get("source_ids") or []
        bad = [s for s in sids if s not in valid_source_ids]
        if bad:
            add(k, "fail", "Sources", f"Cites unknown source IDs: {', '.join(bad)}")
        if NUMBER_CLAIM.search(cap) and not sids:
            add(k, "warn", "Sources", "Caption contains a number/statistic but the post cites no source")
        if p.get("approval_status") not in ("Pending Review", "Changes Requested", "Approved", "Rejected"):
            add(k, "fail", "Approval", "Invalid approval status")

    global_issues: list[dict] = []
    if pillar_targets and posts:
        counts = Counter(p.get("content_pillar") for p in posts)
        for pillar, target in pillar_targets.items():
            actual = round(100 * counts.get(pillar, 0) / len(posts))
            if abs(actual - target) > 15:
                global_issues.append({"severity": "warn", "check": "Pillar mix",
                                      "issue": f"Pillar '{pillar}' is {actual}% of posts vs target {target}%"})
        unknown = [p for p in counts if p not in pillar_targets]
        if unknown:
            global_issues.append({"severity": "warn", "check": "Pillar mix",
                                  "issue": f"Posts use pillars not in the strategy: {', '.join(map(str, unknown))}"})

    all_issues = [i for v in per_post.values() for i in v] + global_issues
    return {
        "posts": per_post,
        "global": global_issues,
        "counts": {
            "fail": sum(1 for i in all_issues if i["severity"] == "fail"),
            "warn": sum(1 for i in all_issues if i["severity"] == "warn"),
        },
    }
