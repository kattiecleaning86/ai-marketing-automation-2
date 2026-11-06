"""Workflow engine: runs the 13 stages of the organic-marketing-engine skill for one run.

Each stage saves its output to the database before the next starts, so a crash or a failed
stage can be retried without redoing finished work. Nothing in this module (or anywhere in
the app) publishes to social media: the final state of every run is "awaiting_approval".
"""
from __future__ import annotations

import calendar as cal
import json
import logging
import traceback
from datetime import date
from typing import Any, Callable

from . import db, deliverables, prompts, qa, schemas, store
from .config import settings
from .llm import LLM, LLMError
from .website import fetch_site

log = logging.getLogger(__name__)

WEEKDAY_PATTERNS = {1: [1], 2: [1, 3], 3: [0, 2, 4], 4: [0, 1, 3, 4], 5: [0, 1, 2, 3, 4],
                    6: [0, 1, 2, 3, 4, 5], 7: [0, 1, 2, 3, 4, 5, 6]}
VIDEO = {"Reel", "Short", "Video", "Story"}


class StageSkipped(Exception):
    """Raised by a stage that could not run for an expected reason (e.g. integration not connected)."""


class Ctx:
    def __init__(self, rid: int, llm: LLM | None, integrations: dict):
        self.rid = rid
        self.run = store.get_run(rid)
        self.client = store.get_client(self.run["client_id"])
        self.brief: dict = self.client["brief"]
        self.month: str = self.run["month"]
        self._llm = llm
        self.integrations = integrations

    @property
    def llm(self) -> LLM:
        if self._llm is None:
            raise LLMError("Claude is not configured. Add ANTHROPIC_API_KEY in the app settings, then click Retry.")
        return self._llm

    def out(self, stage: str) -> dict:
        return store.stage_output(self.rid, stage)

    def sources(self) -> list[dict]:
        return store.get_sources(self.rid)

    def valid_ids(self) -> set[str]:
        return {s["sid"] for s in self.sources()}


# ---------------------------------------------------------------- helpers

def clean_source_ids(obj: Any, valid: set[str], dropped: list[str]) -> Any:
    """Remove any source ID that is not in the verified source list (anti-fabrication)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "source_ids" and isinstance(v, list):
                keep = [s for s in v if s in valid]
                dropped.extend(s for s in v if s not in valid)
                obj[k] = list(dict.fromkeys(keep))
            else:
                clean_source_ids(v, valid, dropped)
    elif isinstance(obj, list):
        for v in obj:
            clean_source_ids(v, valid, dropped)
    return obj


def research_and_structure(ctx: Ctx, stage: str, research_prompt: str, struct_prompt: str, schema: dict,
                           max_searches: int = 8) -> dict:
    res = ctx.llm.research(prompts.RESEARCH_SYSTEM, research_prompt, max_searches=max_searches)
    store.add_sources(ctx.rid, res.sources, stage)
    db.log(ctx.rid, f"{stage}: web research used {res.searches_used} searches, {len(res.sources)} pages returned")
    prompt = "\n\n".join([
        prompts.brief_block(ctx.brief),
        "RESEARCH NOTES (from live web research just performed):\n" + (res.text or "(no notes)"),
        prompts.sources_block(ctx.sources()),
        struct_prompt,
    ])
    data = ctx.llm.structured(prompts.SYSTEM, prompt, schema)
    dropped: list[str] = []
    clean_source_ids(data, ctx.valid_ids(), dropped)
    if dropped:
        db.log(ctx.rid, f"{stage}: removed {len(dropped)} unverifiable source references", "warn")
    return {"data": data, "research_notes": res.text, "searches_used": res.searches_used,
            "unverified_refs_removed": len(dropped)}


def compact(obj: Any, limit: int = 12000) -> str:
    text = json.dumps(obj, ensure_ascii=False)
    return text if len(text) <= limit else text[:limit] + "…(truncated)"


def platforms_from_brief(brief: dict) -> dict[str, int]:
    cad = brief.get("cadence") or {}
    out = {}
    for p in schemas.PLATFORMS:
        try:
            n = int(cad.get(p, 0) or 0)
        except (TypeError, ValueError):
            n = 0
        if n > 0:
            out[p] = min(n, 7)
    return out or {"Instagram": 3}


def build_slots(month: str, cadence: dict[str, int], cap: int) -> list[dict]:
    year, mon = map(int, month.split("-"))
    total = lambda c: sum(len([d for d in range(1, cal.monthrange(year, mon)[1] + 1)
                               if date(year, mon, d).weekday() in WEEKDAY_PATTERNS[n]]) for n in c.values())
    cadence = dict(cadence)
    while total(cadence) > cap and any(n > 1 for n in cadence.values()):
        biggest = max(cadence, key=cadence.get)
        cadence[biggest] -= 1
    slots = []
    days = cal.monthrange(year, mon)[1]
    for d in range(1, days + 1):
        dt = date(year, mon, d)
        for plat, n in cadence.items():
            if dt.weekday() in WEEKDAY_PATTERNS[n]:
                slots.append({"date": dt.isoformat(), "platform": plat, "weekday": dt.strftime("%A")})
    slots = slots[:cap]
    for i, s in enumerate(slots, 1):
        s["slot"] = i
    return slots


def render_script(fmt: str, script: dict) -> str:
    if not script or script.get("script_type") == "none":
        return f"N/A — {fmt} format uses no video script or slide copy"
    lines = []
    if script.get("script_type") == "reel_script" or script.get("scenes"):
        if script.get("duration_seconds"):
            lines.append(f"Duration: {script['duration_seconds']}s")
        for sc in script.get("scenes") or []:
            lines.append(f"[{sc.get('timestamp','')}] VISUAL: {sc.get('visual','')} | ON-SCREEN TEXT: {sc.get('on_screen_text','')} "
                         f"| VO/DIALOGUE: {sc.get('voiceover','')} | AUDIO: {sc.get('audio','')}")
    if script.get("slides"):
        for sl in script["slides"]:
            lines.append(f"Slide {sl.get('slide_number')}: {sl.get('headline','')} — {sl.get('body','')}")
    if script.get("closing_cta"):
        lines.append(f"Closing CTA: {script['closing_cta']}")
    if script.get("subtitle_note"):
        lines.append(f"Subtitles/accessibility: {script['subtitle_note']}")
    return "\n".join(lines) or f"N/A — {fmt} format uses no video script or slide copy"


def strategy_context(ctx: Ctx) -> str:
    strat = ctx.out("strategy").get("data", {})
    brand = ctx.out("brand_analysis").get("data", {})
    return "\n\n".join([
        prompts.brief_block(ctx.brief),
        "BRAND ANALYSIS (summary): " + compact({k: brand.get(k) for k in ("summary", "positioning", "tone_of_voice", "brand_personality", "visual_identity")}, 4000),
        "STRATEGY: " + compact(strat, 9000),
    ])


def batched(items: list, n: int):
    for i in range(0, len(items), n):
        yield items[i:i + n]


# ---------------------------------------------------------------- stages

def stage_onboarding(ctx: Ctx) -> dict:
    missing = [k for k in ("business_name", "website", "industry", "target_audience", "primary_goal", "tone_of_voice")
               if not ctx.brief.get(k)]
    return {"saved": True, "client_slug": ctx.client["slug"], "missing_fields": missing,
            "assumptions": [f"'{m}' not provided — the system will infer it and label it as an assumption" for m in missing]}


def stage_brand_analysis(ctx: Ctx) -> dict:
    snap = fetch_site(ctx.brief.get("website", ""))
    store.add_sources(ctx.rid, [{"url": p.url, "title": f"{ctx.client['name']} website — {p.title}"} for p in snap.pages], "brand_analysis")
    db.log(ctx.rid, f"brand_analysis: fetched {len(snap.pages)} website pages ({len(snap.errors)} errors)")
    name = ctx.client["name"]
    research = (f"Research the brand '{name}' (website: {ctx.brief.get('website','n/a')}; social handles: "
                f"{ctx.brief.get('social_handles','n/a')}; industry: {ctx.brief.get('industry','n/a')}; location: "
                f"{ctx.brief.get('locations','n/a')}). First use web_fetch to read the brand's website homepage "
                "(and its about/services page if linked). Then find its public social media profiles and what they post, "
                "public customer reviews and their recurring themes, press coverage, and how the brand presents itself. "
                "Report only what you can verify.")
    struct = ("WEBSITE CONTENT (fetched directly from the client's site):\n" + snap.as_prompt() +
              "\n\nTASK: Produce the brand analysis (Stage 2). Mark each claim Fact (with source IDs), Observation "
              "(seen on the website/profiles) or Assumption. The SWOT must focus on social media.")
    out = research_and_structure(ctx, "brand_analysis", research, struct, schemas.BRAND, max_searches=6)
    out["website_pages"] = [{"url": p.url, "title": p.title} for p in snap.pages]
    out["website_errors"] = snap.errors
    out["social_links_found"] = snap.social_links
    return out


def stage_audience_market(ctx: Ctx) -> dict:
    research = (f"Research the target audience and market for a {ctx.brief.get('industry','')} business in "
                f"{ctx.brief.get('locations','')} targeting: {ctx.brief.get('target_audience','')}. Find: market size/growth "
                f"and trends (with publisher and date), seasonality and key dates/holidays/events in {ctx.month} for that "
                "region, regulations affecting marketing in this category, and public voice-of-customer signals "
                "(reviews, forums, Q&A) describing needs, pain points and objections.")
    struct = (f"TASK: Produce Stage 3 — 2 to 4 audience personas, market overview, seasonality, key dates for {ctx.month}, "
              "regulatory notes and voice-of-customer quotes. Quotes must be verbatim from sources; otherwise omit them.")
    return research_and_structure(ctx, "audience_market", research, struct, schemas.AUDIENCE, max_searches=8)


def stage_competitors(ctx: Ctx) -> dict:
    known = ctx.brief.get("competitors_known") or "none provided"
    research = (f"Identify 3 to 5 direct competitors and 1 to 2 aspirational brands for '{ctx.client['name']}' "
                f"({ctx.brief.get('industry','')}, {ctx.brief.get('locations','')}). Competitors named by the client: {known}. "
                "For each, find their website and social media profiles and describe what they post (formats, themes, "
                "tone, approximate frequency, standout posts) based on what is publicly visible.")
    struct = ("TASK: Produce Stage 4 competitor research. Include 3–5 direct competitors and 1–2 aspirational brands. "
              "Do not invent follower counts or engagement numbers. Then list opportunities, threats and formats to adapt (never copy).")
    out = research_and_structure(ctx, "competitors", research, struct, schemas.COMPETITORS, max_searches=10)
    n_direct = sum(1 for c in out["data"].get("competitors", []) if c.get("type") == "Direct")
    if n_direct < 3:
        out["warning"] = f"Only {n_direct} direct competitors could be verified (target 3–5)."
        db.log(ctx.rid, out["warning"], "warn")
    return out


def stage_strategy(ctx: Ctx) -> dict:
    cadence = platforms_from_brief(ctx.brief)
    prompt = "\n\n".join([
        prompts.brief_block(ctx.brief),
        "BRAND ANALYSIS: " + compact(ctx.out("brand_analysis").get("data"), 7000),
        "AUDIENCE & MARKET: " + compact(ctx.out("audience_market").get("data"), 7000),
        "COMPETITORS: " + compact(ctx.out("competitors").get("data"), 6000),
        prompts.sources_block(ctx.sources()),
        f"PLATFORMS AND POSTS PER WEEK (agreed cadence): {cadence}",
        "TASK: Produce Stage 5 — the organic social media strategy. 3–5 content pillars whose mix_percent values sum "
        "to 100. KPIs: only state a baseline if it is in the brief, otherwise write 'Unknown — measure in month 1'. "
        "Posting windows: mark the basis honestly ('Test hypothesis' unless sourced or from client data).",
    ])
    data = ctx.llm.structured(prompts.SYSTEM, prompt, schemas.STRATEGY)
    clean_source_ids(data, ctx.valid_ids(), [])
    pillars = data.get("content_pillars") or []
    total = sum(max(0, p.get("mix_percent") or 0) for p in pillars)
    if pillars and total != 100:
        for p in pillars:
            p["mix_percent"] = round(100 * (p.get("mix_percent") or 0) / total) if total else round(100 / len(pillars))
    return {"data": data, "cadence": cadence}


def stage_trends(ctx: Ctx) -> dict:
    plats = ", ".join(platforms_from_brief(ctx.brief))
    research = (f"Research current social media trends relevant to a {ctx.brief.get('industry','')} brand for {ctx.month} "
                f"on {plats}. Today is {date.today().isoformat()}. Look for: recent official platform feature or algorithm "
                "announcements (official newsrooms/help centres), format trends, cultural moments and seasonal events in "
                f"{ctx.month} for {ctx.brief.get('locations','the client region')}, and industry-specific conversations. "
                "Only report trends with a dated, verifiable source. Note how old each source is.")
    pillars = [p.get("name") for p in ctx.out("strategy").get("data", {}).get("content_pillars", [])]
    struct = (f"CONTENT PILLARS: {pillars}\nTASK: Produce Stage 6. Include only trends backed by source IDs; "
              "list trends you rejected (unverifiable, off-brand, risky or stale) with reasons.")
    out = research_and_structure(ctx, "trends", research, struct, schemas.TRENDS, max_searches=10)
    before = len(out["data"].get("trends", []))
    out["data"]["trends"] = [t for t in out["data"].get("trends", []) if t.get("source_ids")]
    removed = before - len(out["data"]["trends"])
    if removed:
        out["data"]["rejected"].extend({"trend": "(removed by system)", "reason": "No verified source"} for _ in range(removed))
    return out


def stage_calendar(ctx: Ctx) -> dict:
    cadence = platforms_from_brief(ctx.brief)
    slots = build_slots(ctx.month, cadence, settings.max_posts_per_month)
    strat = ctx.out("strategy").get("data", {})
    pillar_names = [p["name"] for p in strat.get("content_pillars", [])]
    prompt = "\n\n".join([
        strategy_context(ctx),
        "AUDIENCE & MARKET (key dates, personas): " + compact(ctx.out("audience_market").get("data"), 5000),
        "COMPETITOR OPPORTUNITIES: " + compact(ctx.out("competitors").get("data", {}).get("opportunities"), 2500),
        "VERIFIED TRENDS: " + compact(ctx.out("trends").get("data", {}).get("trends"), 5000),
        prompts.sources_block(ctx.sources()),
        "POSTING SLOTS (fixed — return exactly one entry per slot number):\n" + "\n".join(
            f"slot {s['slot']}: {s['date']} ({s['weekday']}) on {s['platform']}" for s in slots),
        f"TASK: Plan the {ctx.month} content calendar (Stage 7). content_pillar must be one of {pillar_names}. Balance the "
        "pillar mix to the strategy, vary formats to suit each platform, avoid repeated topics, anchor posts to key dates and "
        "verified trends. research_rationale explains why this post and why now, citing source IDs where relevant. "
        "suggested_time like '18:00' with basis noted only if sourced; otherwise give a test time.",
    ])
    data = ctx.llm.structured(prompts.SYSTEM, prompt, schemas.CALENDAR, max_tokens=48000)
    clean_source_ids(data, ctx.valid_ids(), [])
    by_slot = {e["slot"]: e for e in data.get("entries", [])}
    db.ex("DELETE FROM posts WHERE run_id=?", (ctx.rid,))
    created = 0
    for s in slots:
        e = by_slot.get(s["slot"])
        if not e:
            db.log(ctx.rid, f"calendar: Claude returned no plan for slot {s['slot']} — slot dropped", "warn")
            continue
        fmt = e["format"]
        if s["platform"] in ("LinkedIn", "X", "Threads", "Facebook") and fmt == "Short":
            fmt = "Video"
        key = f"P{s['slot']:02d}"
        db.ex("""INSERT INTO posts (run_id, post_key, date, time, platform, content_pillar, objective, topic,
                 research_rationale, source_ids_json, format, kpi_objective, approval_status)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?, 'Pending Review')""",
              (ctx.rid, key, s["date"], e.get("suggested_time", ""), s["platform"], e["content_pillar"], e["objective"],
               e["topic"], e["research_rationale"], db.jdump(e.get("source_ids", [])), fmt, e["kpi_objective"]))
        created += 1
    return {"posts_created": created, "slots": len(slots), "cadence": cadence}


def stage_copy(ctx: Ctx) -> dict:
    todo = [p for p in store.get_posts(ctx.rid) if not p.get("caption")]
    base = strategy_context(ctx)
    for batch in batched(todo, 6):
        prompt = "\n\n".join([
            base, prompts.sources_block(ctx.sources()),
            "POSTS TO WRITE:\n" + compact([{k: p[k] for k in ("post_key", "date", "platform", "format", "content_pillar",
                                                              "objective", "topic", "research_rationale", "source_ids", "kpi_objective")}
                                           for p in batch], 8000),
            "TASK (Stage 8): For each post write: hook (scroll-stopping first line / first 1–3 seconds), 2 alt_hooks, a "
            "platform-ready caption in the brand voice (respect platform length norms; X max 280 characters), one clear CTA "
            "aligned to the objective, hashtags (each starting with #, CamelCase, tiered branded/niche/community per the "
            "strategy, within platform norms), and alt_text for the visual. Only include statistics that appear in the "
            "SOURCE LIST quotes or the brief.",
        ])
        data = ctx.llm.structured(prompts.SYSTEM, prompt, schemas.COPY)
        for item in data.get("posts", []):
            store.update_post(ctx.rid, item["post_key"], hook=item["hook"], alt_hooks=item["alt_hooks"], caption=item["caption"],
                              cta=item["cta"], hashtags=[h if h.startswith("#") else "#" + h for h in item["hashtags"]],
                              alt_text=item["alt_text"])
    return {"posts_written": len(todo)}


def stage_scripts(ctx: Ctx) -> dict:
    posts = store.get_posts(ctx.rid)
    todo = []
    for p in posts:
        if p.get("script_text"):
            continue
        if p["format"] in VIDEO or p["format"] == "Carousel":
            todo.append(p)
        else:
            store.update_post(ctx.rid, p["post_key"], script={"script_type": "none"}, script_text=render_script(p["format"], {}))
    base = strategy_context(ctx)
    for batch in batched(todo, 4):
        prompt = "\n\n".join([
            base,
            "POSTS:\n" + compact([{k: p[k] for k in ("post_key", "platform", "format", "topic", "hook", "caption", "cta", "objective")}
                                  for p in batch], 9000),
            "TASK (Stage 8 continued): For Reel/Short/Video/Story posts write a complete scene-by-scene script "
            "(script_type 'reel_script', duration_seconds, scenes with timestamp, visual/shot, on-screen text, voiceover or "
            "dialogue, audio note — licensed/platform-library audio only; slides empty). For Carousel posts write "
            "slide-by-slide copy (script_type 'carousel', cover hook slide → value slides → CTA slide, 5–10 slides, mobile-"
            "readable word counts; scenes empty, duration_seconds 0). Open with the post's hook.",
        ])
        data = ctx.llm.structured(prompts.SYSTEM, prompt, schemas.SCRIPTS)
        fmt = {p["post_key"]: p["format"] for p in batch}
        for item in data.get("posts", []):
            if item["post_key"] in fmt:
                store.update_post(ctx.rid, item["post_key"], script=item, script_text=render_script(fmt[item["post_key"]], item))
    return {"scripts_written": len(todo)}


def stage_briefs(ctx: Ctx) -> dict:
    posts = store.get_posts(ctx.rid)
    todo = [p for p in posts if not p.get("brief_id")]
    base = strategy_context(ctx)
    approver = ctx.brief.get("approvers") or "Marketing Manager"
    for batch in batched(todo, 6):
        prompt = "\n\n".join([
            base, f"VISUAL GUIDELINES FROM CLIENT: {ctx.brief.get('visual_guidelines','not provided')}",
            f"CONTENT RESOURCES: {ctx.brief.get('content_resources','not provided')}; ON-CAMERA: {ctx.brief.get('on_camera_people','not provided')}",
            "POSTS:\n" + compact([{k: p[k] for k in ("post_key", "date", "platform", "format", "topic", "hook", "script_text", "kpi_objective")}
                                  for p in batch], 10000),
            "TASK (Stage 9): For each post write visual_direction (one paragraph for the calendar) and a full creative brief "
            "a designer or video editor can execute without follow-up: summary, specs (aspect ratio, dimensions, duration, "
            "file type, safe zones, frame/slide count for that platform and format), key message, on-screen copy, mood and "
            "style (describe references, do not link), colour palette, typography, brand assets to use, shot list (video) "
            "or layout notes, audio direction (licensed only), accessibility (captions, contrast, alt text), dos and donts.",
        ])
        data = ctx.llm.structured(prompts.SYSTEM, prompt, schemas.BRIEFS)
        for item in data.get("posts", []):
            key = item["post_key"]
            num = key[1:]
            brief = dict(item, id=f"CB-{ctx.month}-{num}", reviewer=approver)
            store.update_post(ctx.rid, key, visual_direction=item["visual_direction"], brief_id=brief["id"], brief=brief)
    return {"briefs_written": len(todo)}


def _qa_snapshot(ctx: Ctx) -> tuple[list[dict], dict]:
    posts = store.get_posts(ctx.rid)
    strat = ctx.out("strategy").get("data", {})
    targets = {p["name"]: p["mix_percent"] for p in strat.get("content_pillars", [])}
    return posts, qa.check_posts(posts, ctx.valid_ids(), targets)


def stage_qa(ctx: Ctx) -> dict:
    posts, rules = _qa_snapshot(ctx)
    brand = ctx.out("brand_analysis").get("data", {})
    review_issues: list[dict] = []
    notes = []
    for batch in batched(posts, 10):
        prompt = "\n\n".join([
            prompts.brief_block(ctx.brief),
            "BRAND VOICE: " + compact(brand.get("tone_of_voice"), 1500),
            prompts.sources_block(ctx.sources()),
            "POSTS: " + compact([{k: p.get(k) for k in ("post_key", "platform", "format", "hook", "caption", "cta", "hashtags",
                                                         "script_text", "source_ids", "research_rationale")} for p in batch], 14000),
            "TASK (Stage 10 QA): Review each post as a strict senior editor. Flag as 'fail': statistics or factual claims "
            "not supported by the SOURCE LIST or brief; invented client facts (prices, offers, awards, results); health, "
            "financial or legal claims; words the client asked to avoid; copyright/audio licensing problems. Flag as 'warn': "
            "off-brand tone, weak hook/CTA, spelling/grammar, accessibility, cultural sensitivity. Give a precise "
            "fix_instruction for each issue. Do not report issues that are not there.",
        ])
        data = ctx.llm.structured(prompts.SYSTEM, prompt, schemas.QA_REVIEW)
        review_issues.extend(data.get("issues", []))
        notes.append(data.get("overall_notes", ""))

    # One automatic fix pass for posts with failing issues in copy.
    fix_needed: dict[str, list[str]] = {}
    for i in review_issues:
        if i["severity"] == "fail":
            fix_needed.setdefault(i["post_key"], []).append(i["fix_instruction"])
    for key, issues in rules["posts"].items():
        for i in issues:
            if i["severity"] == "fail" and i["check"] in ("Platform specs", "Hashtags"):
                fix_needed.setdefault(key, []).append(i["issue"])
    fixed = []
    if fix_needed:
        target = [p for p in posts if p["post_key"] in fix_needed]
        for batch in batched(target, 6):
            prompt = "\n\n".join([
                strategy_context(ctx), prompts.sources_block(ctx.sources()),
                "POSTS AND REQUIRED FIXES: " + compact([{"post_key": p["post_key"], "platform": p["platform"], "hook": p["hook"],
                                                         "caption": p["caption"], "cta": p["cta"], "hashtags": p["hashtags"],
                                                         "fixes": fix_needed[p["post_key"]]} for p in batch], 12000),
                "TASK: Rewrite hook, caption, CTA and hashtags to resolve every listed fix. Remove unsupported claims "
                "rather than inventing support. Keep everything else the same.",
            ])
            data = ctx.llm.structured(prompts.SYSTEM, prompt, schemas.QA_FIX)
            for item in data.get("posts", []):
                if item["post_key"] in fix_needed:
                    store.update_post(ctx.rid, item["post_key"], hook=item["hook"], caption=item["caption"], cta=item["cta"],
                                      hashtags=[h if h.startswith("#") else "#" + h for h in item["hashtags"]])
                    fixed.append(item["post_key"])

    posts, rules_after = _qa_snapshot(ctx)
    fixed_set = set(fixed)
    open_review = [i for i in review_issues if not (i["severity"] == "fail" and i["post_key"] in fixed_set)]
    for p in posts:
        issues = rules_after["posts"].get(p["post_key"], []) + [
            {"severity": i["severity"], "check": i["category"], "issue": i["issue"]} for i in open_review if i["post_key"] == p["post_key"]]
        status = "fail" if any(i["severity"] == "fail" for i in issues) else ("warn" if issues else "pass")
        store.update_post(ctx.rid, p["post_key"], qa_status=status, qa_notes=db.jdump(issues))
    return {
        "rule_checks_before": rules["counts"],
        "rule_checks_after": rules_after["counts"],
        "global_issues": rules_after["global"],
        "editor_review_issues": review_issues,
        "auto_fixed_posts": sorted(fixed_set),
        "editor_notes": [n for n in notes if n],
        "open_fail_posts": [p["post_key"] for p in store.get_posts(ctx.rid) if p.get("qa_status") == "fail"],
    }


def stage_delivery(ctx: Ctx) -> dict:
    local = deliverables.write_all(ctx.rid)
    google = ctx.integrations.get("google")
    if google is None or not google.connected():
        raise StageSkipped(f"Google not connected — deliverables saved locally only ({len(local)} files). "
                           "Connect Google in Settings, then click Retry to upload.")
    result = google.deliver(ctx.rid, local)
    store.set_run(ctx.rid, drive_folder_url=result["folder_url"], sheet_url=result["sheet_url"], sheet_id=result["sheet_id"])
    deliverables.append_delivery_log(ctx.rid, f"Uploaded {len(result['files'])} files to Google Drive: {result['folder_url']}; "
                                              f"calendar Sheet: {result['sheet_url']}")
    return {"local_files": local, **result}


def stage_notify(ctx: Ctx) -> dict:
    slack = ctx.integrations.get("slack")
    if slack is None or not slack.configured():
        msg = deliverables.slack_message(ctx.rid)
        deliverables.append_delivery_log(ctx.rid, "Slack not configured — message drafted below for manual sending:\n\n" + msg)
        raise StageSkipped("Slack not configured — approval message drafted in the delivery log.")
    text = deliverables.slack_message(ctx.rid)
    slack.send(text)
    deliverables.append_delivery_log(ctx.rid, "Slack approval notification sent.")
    return {"sent": True, "message": text}


STAGE_FUNCS: dict[str, Callable[[Ctx], dict]] = {
    "onboarding": stage_onboarding, "brand_analysis": stage_brand_analysis, "audience_market": stage_audience_market,
    "competitors": stage_competitors, "strategy": stage_strategy, "trends": stage_trends, "calendar": stage_calendar,
    "copy": stage_copy, "scripts": stage_scripts, "briefs": stage_briefs, "qa": stage_qa, "delivery": stage_delivery,
    "notify": stage_notify,
}


# ---------------------------------------------------------------- runner

def run_pipeline(rid: int, llm: LLM | None, integrations: dict) -> str:
    """Run all unfinished stages. Returns the final run status."""
    store.set_run(rid, status="running", error=None)
    ctx = Ctx(rid, llm, integrations)
    for st in store.get_stages(rid):
        if st["status"] in ("done", "skipped"):
            continue
        name = st["name"]
        store.set_stage(rid, name, status="running", started_at=db.now(), error=None, note=None)
        db.log(rid, f"Stage started: {store.STAGE_LABELS[name]}")
        try:
            output = STAGE_FUNCS[name](ctx)
            store.set_stage(rid, name, status="done", output=output, finished_at=db.now())
            db.log(rid, f"Stage finished: {store.STAGE_LABELS[name]}")
        except StageSkipped as skip:
            store.set_stage(rid, name, status="skipped", note=str(skip), finished_at=db.now())
            db.log(rid, f"Stage skipped: {store.STAGE_LABELS[name]} — {skip}", "warn")
        except Exception as exc:  # noqa: BLE001 — any failure stops the run so a human can retry
            msg = f"{exc.__class__.__name__}: {exc}"
            store.set_stage(rid, name, status="failed", error=msg, finished_at=db.now())
            store.set_run(rid, status="failed", error=f"{store.STAGE_LABELS[name]} failed — {msg}")
            db.log(rid, f"Stage failed: {store.STAGE_LABELS[name]} — {msg}", "error")
            log.error("Run %s stage %s failed:\n%s", rid, name, traceback.format_exc())
            try:
                deliverables.write_all(rid)
            except Exception:  # noqa: BLE001
                pass
            slack = integrations.get("slack")
            if slack is not None and slack.configured():
                try:
                    slack.send(f":warning: Organic social run #{rid} for {ctx.client['name']} ({ctx.month}) failed at "
                               f"*{store.STAGE_LABELS[name]}*: {msg}\nOpen the dashboard to retry: {settings.base_url}/admin/runs/{rid}")
                except Exception:  # noqa: BLE001
                    pass
            return "failed"
        try:
            deliverables.write_all(rid)
        except Exception as exc:  # noqa: BLE001
            db.log(rid, f"Could not write local deliverables: {exc}", "warn")
    store.set_run(rid, status="awaiting_approval")
    db.log(rid, "All stages complete — awaiting human approval. Nothing has been published.")
    return "awaiting_approval"
