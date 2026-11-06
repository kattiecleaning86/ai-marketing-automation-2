"""Automatic quality checks for a client's monthly calendar.

Usage:
    python tools/qa_check.py clients/<client-slug> 2026-12

Checks the calendar JSON against the rules in CLAUDE.md / SKILL.md and writes
06_qa/<slug>_qa-auto_<month>.md. Exit code 1 if any check FAILS.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (APPROVAL_STATUSES, REQUIRED, VIDEO_FORMATS, calendar_path, client_dir,  # noqa: E402
                    load_json, load_rules)

STAT = re.compile(r"\b\d+(?:[.,]\d+)?\s?(?:%|percent\b|x\b|times\b|million\b|billion\b)", re.I)
URL = re.compile(r"^https?://[^\s]+$")


def _norm(t: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (t or "").lower()).strip()


def check(cal: dict, sources: dict, month: str, rules: dict | None = None) -> dict:
    rules = rules or load_rules()
    posts = cal.get("posts", [])
    src_ids = {s["id"] for s in sources.get("sources", [])}
    issues: dict[str, list[tuple[str, str, str]]] = {"_global": []}

    def add(key, sev, chk, msg):
        issues.setdefault(key, []).append((sev, chk, msg))

    # --- sources registry
    for s in sources.get("sources", []):
        for f in ("id", "title", "url", "accessed"):
            if not s.get(f):
                add("_global", "FAIL", "Sources", f"Source {s.get('id', '?')} is missing '{f}'")
        if s.get("url") and not URL.match(s["url"]):
            add("_global", "FAIL", "Sources", f"Source {s.get('id')} has an invalid URL")
    dup = [k for k, v in Counter(s.get("url") for s in sources.get("sources", [])).items() if v > 1]
    if dup:
        add("_global", "WARN", "Sources", f"Duplicate source URLs: {', '.join(dup)}")

    if not posts:
        add("_global", "FAIL", "Completeness", "Calendar has no posts")

    hooks = Counter(_norm(p.get("hook", "")) for p in posts)
    topics = Counter(_norm(p.get("topic", "")) for p in posts)
    ids = Counter(p.get("id") for p in posts)
    brief_ids = Counter((p.get("creative_brief") or {}).get("id") for p in posts)
    cap_max, tag_hard, tag_rec = rules["caption_max_chars"], rules["hashtags_hard_max"], rules["hashtags_recommended_max"]

    for p in posts:
        k = p.get("id") or "?"
        issues.setdefault(k, [])
        if ids[k] > 1:
            add(k, "FAIL", "Completeness", "Duplicate post ID")
        for f in REQUIRED:
            v = p.get(f)
            if v in (None, "", [], {}):
                add(k, "FAIL", "Completeness", f"Missing field: {f}")
        if p.get("date") and not str(p["date"]).startswith(month):
            add(k, "FAIL", "Calendar", f"Date {p['date']} is outside {month}")
        plat, cap, tags = p.get("platform", ""), p.get("caption") or "", p.get("hashtags") or []
        if plat in cap_max and len(cap) > cap_max[plat]:
            add(k, "FAIL", "Platform specs", f"Caption {len(cap)} chars > {plat} limit {cap_max[plat]}")
        if plat in tag_hard and len(tags) > tag_hard[plat]:
            add(k, "FAIL", "Platform specs", f"{len(tags)} hashtags > {plat} hard limit {tag_hard[plat]}")
        elif plat in tag_rec and len(tags) > tag_rec[plat]:
            add(k, "WARN", "Platform specs", f"{len(tags)} hashtags > recommended {tag_rec[plat]} for {plat}")
        bad_tags = [t for t in tags if not re.fullmatch(r"#\w+", t)]
        if bad_tags:
            add(k, "FAIL", "Hashtags", f"Malformed hashtags: {' '.join(bad_tags)}")
        fmt, script = p.get("format"), p.get("script") or {}
        if fmt in VIDEO_FORMATS and len(script.get("scenes") or []) < 2:
            add(k, "FAIL", "Completeness", f"{fmt} needs a scene-by-scene script (2+ scenes)")
        if fmt == "Carousel" and len(script.get("slides") or []) < 3:
            add(k, "FAIL", "Completeness", "Carousel needs slide-by-slide copy (3+ slides)")
        b = p.get("creative_brief") or {}
        for f in ("id", "summary", "specs", "key_message", "mood_and_style", "dos", "donts"):
            if not b.get(f):
                add(k, "FAIL", "Creative brief", f"Creative brief missing '{f}'")
        if b.get("id") and brief_ids[b["id"]] > 1:
            add(k, "FAIL", "Creative brief", "Duplicate creative brief ID")
        if p.get("approval_status") not in APPROVAL_STATUSES:
            add(k, "FAIL", "Approval", f"Invalid approval status: {p.get('approval_status')!r}")
        elif p.get("approval_status") == "Approved" and not p.get("approved_by"):
            add(k, "FAIL", "Approval", "Marked Approved without a named human approver (approved_by)")
        unknown = [s for s in p.get("source_ids") or [] if s not in src_ids]
        if unknown:
            add(k, "FAIL", "Sources", f"Cites source IDs not in sources.json: {', '.join(unknown)}")
        if not p.get("source_ids"):
            add(k, "WARN", "Sources", "Research rationale cites no source ID")
        text = " ".join([cap, p.get("hook", ""), " ".join(s.get("body", "") for s in script.get("slides") or [])])
        if STAT.search(text) and not p.get("source_ids"):
            add(k, "FAIL", "Sources", "Contains a statistic but cites no source")
        if p.get("hook") and hooks[_norm(p["hook"])] > 1:
            add(k, "WARN", "Uniqueness", "Hook repeats another post's hook")
        if p.get("topic") and topics[_norm(p["topic"])] > 1:
            add(k, "WARN", "Uniqueness", "Topic repeats another post")
        if fmt in ("Static image", "Carousel") and not p.get("alt_text"):
            add(k, "WARN", "Accessibility", "No alt text")

    pillars = {pl["name"]: pl.get("mix_percent", 0) for pl in cal.get("pillars", [])}
    if posts and pillars:
        counts = Counter(p.get("content_pillar") for p in posts)
        tol = rules.get("pillar_mix_tolerance_percent", 15)
        for name, target in pillars.items():
            actual = round(100 * counts.get(name, 0) / len(posts))
            if abs(actual - target) > tol:
                add("_global", "WARN", "Pillar mix", f"'{name}' is {actual}% vs target {target}%")
        stray = [c for c in counts if c not in pillars]
        if stray:
            add("_global", "FAIL", "Pillar mix", f"Posts use pillars not in the strategy: {', '.join(map(str, stray))}")

    flat = [i for v in issues.values() for i in v]
    return {"issues": issues, "fail": sum(1 for i in flat if i[0] == "FAIL"),
            "warn": sum(1 for i in flat if i[0] == "WARN"), "posts": len(posts)}


def report_md(cal: dict, res: dict, month: str) -> str:
    lines = [f"# Automatic QA Report — {cal.get('client', '')} — {month}", "",
             f"**Result: {'PASS' if res['fail'] == 0 else 'FAIL'}** — {res['posts']} posts, "
             f"{res['fail']} failures, {res['warn']} warnings", "",
             "Generated by `tools/qa_check.py`. The editorial review (brand voice, claims, compliance) is recorded "
             "separately in the QA report written during the workflow.", "", "## Global"]
    lines += [f"- **{s}** {c}: {m}" for s, c, m in res["issues"].get("_global", [])] or ["- No issues"]
    lines += ["", "## Per post"]
    for k, items in res["issues"].items():
        if k == "_global":
            continue
        lines.append(f"- **{k}**: " + ("; ".join(f"{s} {c} — {m}" for s, c, m in items) if items else "pass"))
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("client")
    ap.add_argument("month")
    a = ap.parse_args()
    cdir = client_dir(a.client)
    cal = load_json(calendar_path(cdir, a.month))
    sources = load_json(cdir / "01_research" / "sources.json")
    res = check(cal, sources, a.month)
    out = cdir / "06_qa" / f"{cdir.name}_qa-auto_{a.month}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report_md(cal, res, a.month), encoding="utf-8")
    print(f"{'PASS' if res['fail'] == 0 else 'FAIL'}: {res['posts']} posts, {res['fail']} failures, {res['warn']} warnings")
    for k, items in res["issues"].items():
        for s, c, m in items:
            print(f"  [{s}] {k} {c}: {m}")
    print(f"Report: {out}")
    return 1 if res["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
