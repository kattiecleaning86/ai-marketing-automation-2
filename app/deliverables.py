"""Writes client deliverables (Markdown + CSV) into data/clients/<slug>/ using the CLAUDE.md layout."""
from __future__ import annotations

import csv
import io
from pathlib import Path

from . import db, store
from .config import settings

CALENDAR_COLUMNS = [
    "Post ID", "Date", "Platform", "Content Pillar", "Objective", "Topic", "Research Rationale", "Hook", "Caption", "CTA",
    "Hashtags", "Format", "Reel Script / Carousel Slide Copy", "Visual Direction", "Creative Brief", "KPI Objective",
    "Approval Status", "Reviewer Comments",
]
APPROVAL_COL = CALENDAR_COLUMNS.index("Approval Status")
COMMENT_COL = CALENDAR_COLUMNS.index("Reviewer Comments")


def client_dir(rid: int) -> Path:
    run = store.get_run(rid)
    return settings.clients_dir / run["client_slug"]


def _fname(run: dict, deliverable: str, ext: str) -> str:
    return f"{run['client_slug']}_{deliverable}_{run['month']}_v1.{ext}"


def _claims(items: list[dict] | None) -> str:
    if not items:
        return "- _None recorded._\n"
    out = []
    for c in items:
        ids = ", ".join(c.get("source_ids") or [])
        out.append(f"- {c.get('point','')} _({c.get('basis','')}{' — ' + ids if ids else ''})_")
    return "\n".join(out) + "\n"


def _list(items) -> str:
    return ", ".join(items) if items else "—"


def _research_footer(out: dict) -> str:
    s = f"\n---\n_Web searches used: {out.get('searches_used', 0)}."
    if out.get("unverified_refs_removed"):
        s += f" {out['unverified_refs_removed']} source references that did not match a retrieved page were removed automatically."
    return s + " Source IDs refer to `sources.md`._\n"


def calendar_rows(rid: int) -> list[list[str]]:
    rows = []
    for p in store.get_posts(rid):
        brief = p.get("brief") or {}
        rows.append([
            p["post_key"], f"{p['date']} {p.get('time') or ''}".strip(), p["platform"], p.get("content_pillar") or "",
            p.get("objective") or "", p.get("topic") or "",
            (p.get("research_rationale") or "") + (f" [Sources: {', '.join(p['source_ids'])}]" if p.get("source_ids") else ""),
            p.get("hook") or "", p.get("caption") or "", p.get("cta") or "", " ".join(p.get("hashtags") or []),
            p.get("format") or "", p.get("script_text") or "", p.get("visual_direction") or "",
            f"{p.get('brief_id') or ''} — {brief.get('summary','')}".strip(" —"), p.get("kpi_objective") or "",
            p.get("approval_status") or "Pending Review", p.get("reviewer_comment") or "",
        ])
    return rows


def calendar_csv(rid: int) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(CALENDAR_COLUMNS)
    w.writerows(calendar_rows(rid))
    return buf.getvalue()


def write_all(rid: int) -> list[str]:
    """(Re)write every deliverable that has data. Returns paths relative to the client folder."""
    run = store.get_run(rid)
    client = store.get_client(run["client_id"])
    base = client_dir(rid)
    written: list[str] = []

    def put(rel: str, text: str):
        path = base / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        written.append(rel)

    name, month = client["name"], run["month"]
    brief = client["brief"]
    put("00_onboarding/brief.md", f"# Client Brief — {name}\n\nTarget month: {month}\n\n" +
        "\n".join(f"- **{k.replace('_', ' ').title()}:** {v}" for k, v in brief.items() if v not in (None, "", [], {})) + "\n")

    st = {s["name"]: s for s in store.get_stages(rid)}
    out = lambda n: db.jload(st[n]["output_json"], {}) if st.get(n) else {}

    b = out("brand_analysis")
    if b.get("data"):
        d = b["data"]
        tov = d.get("tone_of_voice") or {}
        put("01_research/brand_analysis.md", f"""# Brand Analysis — {name}

## Summary
{d.get('summary','')}

**Positioning:** {d.get('positioning','')}

**Value proposition:** {d.get('value_proposition','')}

**Brand personality:** {_list(d.get('brand_personality'))}

## Tone of voice
{tov.get('description','')}

Example lines:
""" + "\n".join(f"> {l}" for l in tov.get("example_lines", [])) + f"""

## Visual identity
{d.get('visual_identity','')}

## Current content themes
{_list(d.get('current_content_themes'))}

## Social presence
{_claims(d.get('social_presence'))}
## Social SWOT
### Strengths
{_claims(d.get('strengths'))}
### Weaknesses
{_claims(d.get('weaknesses'))}
### Opportunities
{_claims(d.get('opportunities'))}
### Threats
{_claims(d.get('threats'))}
## Gaps & inconsistencies
{_claims(d.get('gaps_and_inconsistencies'))}
## Website pages analysed
""" + ("\n".join(f"- {p['url']} — {p['title']}" for p in b.get("website_pages", [])) or "- None could be retrieved") +
            ("\n\nWebsite fetch errors: " + "; ".join(b["website_errors"]) if b.get("website_errors") else "") +
            _research_footer(b))

    a = out("audience_market")
    if a.get("data"):
        d = a["data"]
        personas = "\n".join(f"""### {p['name']} _({p['basis']}{' — ' + ', '.join(p['source_ids']) if p['source_ids'] else ''})_
{p['description']}

- **Goals:** {_list(p['goals'])}
- **Pain points:** {_list(p['pain_points'])}
- **Objections:** {_list(p['objections'])}
- **Buying triggers:** {_list(p['buying_triggers'])}
- **Preferred platforms:** {_list(p['preferred_platforms'])}
- **Content they consume:** {_list(p['content_preferences'])}
- **Phrases they use:** {_list(p['phrases_they_use'])}
""" for p in d.get("personas", []))
        dates = "\n".join(f"| {k['date']} | {k['event']} | {k['relevance']} | {', '.join(k['source_ids']) or '—'} |" for k in d.get("key_dates", []))
        voc = "\n".join(f"> \"{v['quote']}\" — {v['where']} ({', '.join(v['source_ids']) or 'unsourced'})" for v in d.get("voice_of_customer", []))
        put("01_research/audience_market.md", f"""# Audience & Market Research — {name}

{d.get('summary','')}

## Personas
{personas}
## Market overview
{_claims(d.get('market_overview'))}
## Seasonality
{_claims(d.get('seasonality'))}
## Key dates — {month}
| Date | Event | Relevance | Sources |
|---|---|---|---|
{dates}

## Regulatory notes
{_claims(d.get('regulatory_notes'))}
## Voice of customer
{voc or '_No verifiable public quotes found._'}
""" + _research_footer(a))

    c = out("competitors")
    if c.get("data"):
        d = c["data"]
        table = "\n".join(f"| {x['name']} | {x['type']} | {x['website']} | {_list(x['platforms'])} | {x['posting_frequency']} | {_list(x['formats'])} | {x['tone']} | {', '.join(x['source_ids']) or '—'} |"
                          for x in d.get("competitors", []))
        details = "\n".join(f"""### {x['name']} ({x['type']})
- **Content pillars:** {_list(x['content_pillars'])}
- **Standout content:** {_list(x['standout_content'])}
- **Weaknesses:** {_list(x['weaknesses'])}
""" for x in d.get("competitors", []))
        put("01_research/competitors.md", f"""# Competitor Research — {name}

{d.get('summary','')}
{('> ⚠️ ' + c['warning']) if c.get('warning') else ''}

| Brand | Type | Website | Platforms | Frequency | Formats | Tone | Sources |
|---|---|---|---|---|---|---|---|
{table}

{details}
## Opportunities (white space)
{_claims(d.get('opportunities'))}
## Threats
{_claims(d.get('threats'))}
## Formats to adapt (never copy)
""" + "\n".join(f"- {f}" for f in d.get("formats_to_adapt", [])) + "\n" + _research_footer(c))

    t = out("trends")
    if t.get("data"):
        d = t["data"]
        rows = "\n".join(f"""### {x['trend']} — {x['platform']}
- **Evidence:** {x['evidence']} ({', '.join(x['source_ids'])})
- **Relevance:** {x['relevance']}
- **Pillar fit:** {_list(x['pillar_fit'])}
- **Risk / brand safety:** {x['risk_notes']}
- **Shelf life:** {x['shelf_life']}
""" for x in d.get("trends", []))
        rej = "\n".join(f"- {x['trend']}: {x['reason']}" for x in d.get("rejected", []))
        put(f"01_research/trends_{month}.md", f"# Trend Research — {name} — {month}\n\n{d.get('summary','')}\n\n{rows or '_No verifiable trends found._'}\n\n## Rejected trends\n{rej or '- None'}\n" + _research_footer(t))

    sources = store.get_sources(rid)
    if sources:
        put("01_research/sources.md", f"# Sources — {name} — {month}\n\nEvery source below was returned by a live web search/fetch "
            "or fetched directly from the client's website by the system. Access date is when the system retrieved it.\n\n"
            "| ID | Title | URL | Published/updated | Accessed | Stage |\n|---|---|---|---|---|---|\n" +
            "\n".join(f"| {s['sid']} | {(s['title'] or '').replace('|', '/')} | {s['url']} | {s['page_age'] or '—'} | {s['accessed_at'][:10]} | {s['stage']} |" for s in sources) + "\n")

    s = out("strategy")
    if s.get("data"):
        d = s["data"]
        objectives = "\n".join(f"### {o['platform']}\n{o['objective']}\n\n| Metric | Baseline | Target |\n|---|---|---|\n" +
                               "\n".join(f"| {k['metric']} | {k['baseline']} | {k['target']} |" for k in o["kpis"]) + "\n" for o in d.get("objectives", []))
        pillars = "\n".join(f"| {p['name']} | {p['mix_percent']}% | {p['funnel_stage']} | {p['purpose']} | {_list(p['example_topics'])} |" for p in d.get("content_pillars", []))
        plats = "\n".join(f"| {p['platform']} | {p['role']} | {_list(p['formats'])} | {p['cadence']} | {p['posting_windows']} ({p['posting_windows_basis']}) |" for p in d.get("platform_strategy", []))
        hs = d.get("hashtag_strategy") or {}
        put("02_strategy/organic_strategy.md", f"""# Organic Social Media Strategy — {name} — {month}

{d.get('summary','')}

**Positioning:** {d.get('positioning','')}

## Objectives & KPIs
{objectives}
## Messaging pillars
""" + "\n".join(f"- **{m['message']}** — proof: {_list(m['proof_points'])}" for m in d.get("messaging_pillars", [])) + f"""

## Content pillars
| Pillar | Mix | Funnel | Purpose | Example topics |
|---|---|---|---|---|
{pillars}

## Platform strategy
| Platform | Role | Formats | Cadence | Posting windows |
|---|---|---|---|---|
{plats}

## Engagement & community plan
""" + "\n".join(f"- {e}" for e in d.get("engagement_plan", [])) + f"""

## Hashtag strategy
- **Branded:** {_list(hs.get('branded'))}
- **Community:** {_list(hs.get('community'))}
- **Niche:** {_list(hs.get('niche'))}
- **Broad:** {_list(hs.get('broad'))}

**Social SEO keywords:** {_list(d.get('social_seo_keywords'))}

## Measurement plan
""" + "\n".join(f"- {m}" for m in d.get("measurement_plan", [])) + "\n\n## Test-and-learn hypotheses\n" +
            "\n".join(f"- {h}" for h in d.get("test_hypotheses", [])) + "\n")

    posts = store.get_posts(rid)
    if posts:
        put(f"03_calendar/{_fname(run, 'calendar', 'csv')}", calendar_csv(rid))
    if posts and any(p.get("caption") for p in posts):
        from collections import Counter
        mix = Counter(p.get("content_pillar") for p in posts)
        plat = Counter(p["platform"] for p in posts)
        body = [f"# Content — {name} — {month}\n",
                f"**Posts:** {len(posts)} · **Platforms:** " + ", ".join(f"{k} ({v})" for k, v in plat.items()) +
                "  \n**Pillar mix:** " + ", ".join(f"{k} {round(100 * v / len(posts))}%" for k, v in mix.items()) + "\n",
                "> Every post is **Pending Review** until a human approves it. Nothing is published automatically.\n"]
        for p in posts:
            body.append(f"""---
## {p['post_key']} · {p['date']} {p.get('time') or ''} · {p['platform']} · {p.get('format')}
**Pillar:** {p.get('content_pillar')} · **Objective:** {p.get('objective')} · **KPI:** {p.get('kpi_objective')} · **Approval:** {p.get('approval_status')}

**Topic:** {p.get('topic')}

**Research rationale:** {p.get('research_rationale')} {('(Sources: ' + ', '.join(p['source_ids']) + ')') if p.get('source_ids') else ''}

**Hook:** {p.get('hook') or ''}
{('Alternates: ' + ' / '.join(p['alt_hooks'])) if p.get('alt_hooks') else ''}

**Caption:**

{p.get('caption') or ''}

**CTA:** {p.get('cta') or ''}

**Hashtags:** {' '.join(p.get('hashtags') or [])}

**Alt text:** {p.get('alt_text') or ''}

**Reel script / carousel copy:**

```
{p.get('script_text') or ''}
```

**Visual direction:** {p.get('visual_direction') or ''}

**Creative brief:** {p.get('brief_id') or ''}
""")
        put(f"04_content/{_fname(run, 'content', 'md')}", "\n".join(body))
    if posts and any(p.get("brief_id") for p in posts):
        out_b = [f"# Creative Briefs — {name} — {month}\n"]
        for p in posts:
            br = p.get("brief") or {}
            if not br:
                continue
            out_b.append(f"""---
## {br.get('id')} — {p['platform']} {p.get('format')} — {p['date']}
**Post:** {p['post_key']} · **Objective/KPI:** {p.get('objective')} / {p.get('kpi_objective')} · **Reviewer:** {br.get('reviewer','')}

**Summary:** {br.get('summary','')}

**Deliverable specs:** {br.get('specs','')}

**Key message & hook:** {br.get('key_message','')} — "{p.get('hook') or ''}"

**On-screen / slide copy:** {br.get('on_screen_copy','')}

**Visual direction:** {br.get('mood_and_style','')}
- Colour palette: {br.get('colour_palette','')}
- Typography: {br.get('typography','')}
- Brand assets: {br.get('assets','')}

**Shot list / layout:**
""" + "\n".join(f"- {s}" for s in br.get("shot_list", [])) + f"""

**Audio:** {br.get('audio_direction','')}

**Accessibility:** {br.get('accessibility','')}

**Do:** {_list(br.get('dos'))}

**Don't:** {_list(br.get('donts'))}

**Script / slide copy:**
```
{p.get('script_text') or ''}
```
""")
        put(f"05_creative_briefs/{_fname(run, 'briefs', 'md')}", "\n".join(out_b))

    qa_out = out("qa")
    if qa_out:
        lines = [f"# Quality Assurance Report — {name} — {month}\n",
                 f"- Rule checks before fixes: {qa_out['rule_checks_before']['fail']} fails, {qa_out['rule_checks_before']['warn']} warnings",
                 f"- Rule checks after fixes: {qa_out['rule_checks_after']['fail']} fails, {qa_out['rule_checks_after']['warn']} warnings",
                 f"- Editor (Claude) review issues: {len(qa_out['editor_review_issues'])}",
                 f"- Posts auto-fixed: {', '.join(qa_out['auto_fixed_posts']) or 'none'}",
                 f"- Posts still failing (need a human decision): {', '.join(qa_out['open_fail_posts']) or 'none'}\n",
                 "## Checklist\nSources verified against retrieved pages · client facts vs brief · 16 calendar fields complete · "
                 "strategy alignment & pillar mix · brand voice · platform specs · language · compliance & risk · accessibility · "
                 "uniqueness · approval status = Pending Review\n",
                 "## Global issues"] + [f"- [{i['severity'].upper()}] {i['check']}: {i['issue']}" for i in qa_out["global_issues"]] + \
                ["", "## Per-post results"]
        for p in posts:
            issues = db.jload(p.get("qa_notes"), [])
            lines.append(f"### {p['post_key']} — {(p.get('qa_status') or '').upper()}")
            lines += [f"- [{i['severity'].upper()}] {i['check']}: {i['issue']}" for i in issues] or ["- No issues"]
        if qa_out.get("editor_notes"):
            lines += ["", "## Editor notes"] + [f"- {n}" for n in qa_out["editor_notes"]]
        put(f"06_qa/{_fname(run, 'qa', 'md')}", "\n".join(lines) + "\n")

    log_path = base / "07_delivery" / "delivery_log.md"
    if not log_path.exists():
        put("07_delivery/delivery_log.md", f"# Delivery Log — {name}\n")
    else:
        written.append("07_delivery/delivery_log.md")

    stages = store.get_stages(rid)
    put("README.md", f"""# {name} — Organic Social Status

- **Month:** {month}
- **Run status:** {run['status']}
- **Google Drive:** {run.get('drive_folder_url') or 'not uploaded'}
- **Calendar Sheet:** {run.get('sheet_url') or 'not created'}
- **Approval:** {sum(1 for p in posts if p['approval_status'] == 'Approved')}/{len(posts)} posts approved

| Stage | Status | Note |
|---|---|---|
""" + "\n".join(f"| {s['label']} | {s['status']} | {(s.get('note') or s.get('error') or '').replace('|', '/')} |" for s in stages) + "\n")
    return written


def append_delivery_log(rid: int, text: str) -> None:
    path = client_dir(rid) / "07_delivery" / "delivery_log.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n## {db.now()} (run #{rid})\n{text}\n")


def slack_message(rid: int) -> str:
    run = store.get_run(rid)
    posts = store.get_posts(rid)
    from collections import Counter
    mix = Counter(p.get("content_pillar") for p in posts)
    plats = sorted({p["platform"] for p in posts})
    qa_out = store.stage_output(rid, "qa")
    trends = store.stage_output(rid, "trends").get("data", {}).get("trends", [])
    open_fails = qa_out.get("open_fail_posts", [])
    lines = [
        f":calendar: *{run['client_name']} — Organic Social Content for {run['month']}* is ready for review.",
        f"• Posts: {len(posts)} across {', '.join(plats)}",
        "• Pillar mix: " + ", ".join(f"{k} {round(100 * v / max(1, len(posts)))}%" for k, v in mix.items()),
        "• Trends covered: " + (", ".join(t["trend"] for t in trends[:4]) or "none verified"),
        f"• QA: {len(qa_out.get('auto_fixed_posts', []))} posts auto-fixed, {len(open_fails)} need your decision"
        + (f" ({', '.join(open_fails)})" if open_fails else ""),
        f":white_check_mark: Review & approve: {settings.base_url}/admin/runs/{rid}",
    ]
    if run.get("sheet_url"):
        lines.append(f":page_facing_up: Calendar (Sheet): {run['sheet_url']}")
    if run.get("drive_folder_url"):
        lines.append(f":file_folder: Drive folder: {run['drive_folder_url']}")
    lines.append("Please set Approval Status for each post (Approved / Changes Requested / Rejected). "
                 "*Nothing will be published until it is marked Approved — and this system never publishes automatically.*")
    return "\n".join(lines)
