"""Shared helpers for the organic-marketing-engine tools (no paid services, no API keys)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIENTS = ROOT / "clients"
RULES_FILE = Path(__file__).resolve().parent / "platform_rules.json"

APPROVAL_STATUSES = ["Pending Review", "Changes Requested", "Approved", "Rejected"]
FORMATS = ["Reel", "Carousel", "Static image", "Story", "Video", "Text post", "Short", "Live"]
VIDEO_FORMATS = {"Reel", "Story", "Video", "Short"}

# Column order for the calendar spreadsheet (the 16 required fields, plus ID and comments).
COLUMNS = [
    ("id", "Post ID"), ("date", "Date"), ("platform", "Platform"), ("content_pillar", "Content Pillar"),
    ("objective", "Objective"), ("topic", "Topic"), ("research_rationale", "Research Rationale"),
    ("hook", "Hook"), ("caption", "Caption"), ("cta", "CTA"), ("hashtags", "Hashtags"), ("format", "Format"),
    ("script", "Reel Script / Carousel Slide Copy"), ("visual_direction", "Visual Direction"),
    ("creative_brief", "Creative Brief"), ("kpi_objective", "KPI Objective"),
    ("approval_status", "Approval Status"), ("reviewer_comments", "Reviewer Comments"),
]
REQUIRED = [k for k, _ in COLUMNS if k not in ("id", "reviewer_comments")]


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "client"


def client_dir(slug_or_path: str) -> Path:
    p = Path(slug_or_path)
    if p.exists() and p.is_dir():
        return p.resolve()
    return CLIENTS / slugify(slug_or_path)


def calendar_path(cdir: Path, month: str) -> Path:
    return cdir / "03_calendar" / f"{cdir.name}_calendar_{month}.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rules() -> dict:
    return load_json(RULES_FILE)


def render_script(post: dict) -> str:
    s = post.get("script") or {}
    kind = s.get("type", "none")
    if kind == "none" or not (s.get("scenes") or s.get("slides")):
        return f"N/A — {post.get('format', '')} format uses no video script or slide copy"
    lines = []
    if s.get("scenes"):
        if s.get("duration_seconds"):
            lines.append(f"Duration: {s['duration_seconds']}s")
        for sc in s["scenes"]:
            lines.append(f"[{sc.get('time', '')}] VISUAL: {sc.get('visual', '')} | ON-SCREEN TEXT: {sc.get('on_screen_text', '')}"
                         f" | VO/DIALOGUE: {sc.get('voiceover', '')} | AUDIO: {sc.get('audio', '')}")
    for sl in s.get("slides") or []:
        lines.append(f"Slide {sl.get('n', '')}: {sl.get('headline', '')} — {sl.get('body', '')}")
    if s.get("closing_cta"):
        lines.append(f"Closing CTA: {s['closing_cta']}")
    if s.get("subtitle_note"):
        lines.append(f"Subtitles/accessibility: {s['subtitle_note']}")
    return "\n".join(lines)


def cell(post: dict, key: str) -> str:
    """Flatten one calendar field into spreadsheet text."""
    val = post.get(key)
    if key == "hashtags":
        return " ".join(val or [])
    if key == "script":
        return render_script(post)
    if key == "creative_brief":
        b = val or {}
        return f"{b.get('id', '')} — {b.get('summary', '')}".strip(" —")
    if key == "research_rationale":
        ids = post.get("source_ids") or []
        return (val or "") + (f" [Sources: {', '.join(ids)}]" if ids else "")
    if key == "date":
        return f"{val or ''} {post.get('time') or ''}".strip()
    return "" if val is None else str(val)
