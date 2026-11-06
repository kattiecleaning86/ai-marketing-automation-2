"""Build the downloadable deliverables from the calendar JSON and research Markdown.

Usage:
    python tools/build_exports.py clients/<client-slug> 2026-12

Creates:
    01_research/sources.md                           source table (from sources.json)
    03_calendar/<slug>_calendar_<month>.csv          calendar (all 16 fields)
    04_content/<slug>_content_<month>.md             full copy for every post
    05_creative_briefs/<slug>_briefs_<month>.md      designer / video-editor briefs
    07_delivery/<slug>_calendar_<month>.xlsx         spreadsheet with Approval Status dropdown
    07_delivery/<slug>_approval-pack_<month>.docx    Word document with every deliverable
Requires: openpyxl, python-docx  (pip install -r requirements.txt)
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import APPROVAL_STATUSES, COLUMNS, calendar_path, cell, client_dir, load_json, render_script  # noqa: E402


# ---------------------------------------------------------------- Markdown deliverables

def _ls(items) -> str:
    return ", ".join(items) if items else "—"


def content_md(cal: dict) -> str:
    posts = cal["posts"]
    plat = Counter(p["platform"] for p in posts)
    mix = Counter(p["content_pillar"] for p in posts)
    out = [f"# Content — {cal['client']} — {cal['month']}", "",
           f"**Posts:** {len(posts)} · **Platforms:** " + ", ".join(f"{k} ({v})" for k, v in plat.items()),
           "**Pillar mix:** " + ", ".join(f"{k} {round(100 * v / len(posts))}%" for k, v in mix.items()), "",
           "> Every post is **Pending Review** until you approve it. Nothing is published automatically.", ""]
    for p in posts:
        srcs = f" (Sources: {', '.join(p['source_ids'])})" if p.get("source_ids") else ""
        out += ["---", f"## {p['id']} · {p['date']} {p.get('time', '')} · {p['platform']} · {p['format']}", "",
                f"**Pillar:** {p['content_pillar']} · **Objective:** {p['objective']} · **KPI:** {p['kpi_objective']} · "
                f"**Approval:** {p['approval_status']}", "",
                f"**Topic:** {p['topic']}", "", f"**Research rationale:** {p['research_rationale']}{srcs}", "",
                f"**Hook:** {p['hook']}", ""]
        if p.get("alt_hooks"):
            out += ["**Alternative hooks:** " + " / ".join(p["alt_hooks"]), ""]
        out += ["**Caption:**", "", p["caption"], "", f"**CTA:** {p['cta']}", "",
                f"**Hashtags:** {' '.join(p.get('hashtags', []))}", ""]
        if p.get("alt_text"):
            out += [f"**Alt text:** {p['alt_text']}", ""]
        out += ["**Reel script / carousel slide copy:**", "", "```", render_script(p), "```", "",
                f"**Visual direction:** {p['visual_direction']}", "",
                f"**Creative brief:** {p['creative_brief']['id']} (see creative briefs document)", ""]
    return "\n".join(out)


def briefs_md(cal: dict) -> str:
    out = [f"# Creative Briefs — {cal['client']} — {cal['month']}", "",
           "One brief per post. Designers and video editors should be able to produce each asset from its brief alone.", ""]
    for p in cal["posts"]:
        b = p["creative_brief"]
        out += ["---", f"## {b['id']} — {p['platform']} {p['format']} — {p['date']}", "",
                f"**Post:** {p['id']} · **Objective / KPI:** {p['objective']} / {p['kpi_objective']}"
                f" · **Reviewer:** {b.get('reviewer', '')} · **Deadline:** {b.get('deadline', '')}", "",
                f"**Summary:** {b['summary']}", "", f"**Deliverable specs:** {b['specs']}", "",
                f"**Key message:** {b['key_message']}", "", f"**Hook:** {p['hook']}", "",
                f"**On-screen / slide copy:** {b.get('on_screen_copy', '')}", "",
                f"**Mood & style:** {b['mood_and_style']}", "",
                f"- Colour palette: {b.get('colour_palette', '')}", f"- Typography: {b.get('typography', '')}",
                f"- Brand assets: {b.get('assets', '')}", "", "**Shot list / layout:**", ""]
        out += [f"- {s}" for s in b.get("shot_list", [])] or ["- —"]
        out += ["", f"**Audio:** {b.get('audio_direction', 'N/A')}", "", f"**Accessibility:** {b.get('accessibility', '')}", "",
                f"**Do:** {_ls(b.get('dos'))}", "", f"**Don't:** {_ls(b.get('donts'))}", "",
                "**Script / slide copy:**", "", "```", render_script(p), "```", ""]
    return "\n".join(out)


def sources_md(cal: dict, sources: dict) -> str:
    rows = ["# Sources — " + cal["client"] + " — " + cal["month"], "",
            sources.get("_note", "Every source below was retrieved during the research for this month."), "",
            "| ID | Title | Publisher | URL | Published | Accessed | Used in | Supports |",
            "|---|---|---|---|---|---|---|---|"]
    for x in sources.get("sources", []):
        cells = [x.get("id", ""), x.get("title", ""), x.get("publisher", ""), x.get("url", ""), x.get("published", ""),
                 x.get("accessed", ""), ", ".join(x.get("used_in", [])), x.get("note", "")]
        rows.append("| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |")
    return "\n".join(rows) + "\n"


def write_csv(cal: dict, path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([h for _, h in COLUMNS])
        for p in cal["posts"]:
            w.writerow([cell(p, k) for k, _ in COLUMNS])


# ---------------------------------------------------------------- Excel

def write_xlsx(cal: dict, sources: dict, path: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    wb = Workbook()
    ws = wb.active
    ws.title = "Calendar"
    ws.append([h for _, h in COLUMNS])
    for p in cal["posts"]:
        ws.append([cell(p, k) for k, _ in COLUMNS])
    head = PatternFill("solid", fgColor="DCE4F5")
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    widths = {"Post ID": 8, "Date": 16, "Platform": 12, "Format": 13, "Approval Status": 18, "Objective": 13}
    for i, (_, h) in enumerate(COLUMNS, start=1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = widths.get(h, 42)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions
    col = [h for _, h in COLUMNS].index("Approval Status") + 1
    letter = ws.cell(1, col).column_letter
    dv = DataValidation(type="list", formula1='"' + ",".join(APPROVAL_STATUSES) + '"', allow_blank=False,
                        showDropDown=False, errorTitle="Approval status", error="Choose a status from the list")
    ws.add_data_validation(dv)
    dv.add(f"{letter}2:{letter}{max(2, len(cal['posts']) + 1)}")

    s = wb.create_sheet("Summary")
    posts = cal["posts"]
    s.append(["Client", cal["client"]]); s.append(["Month", cal["month"]]); s.append(["Posts", len(posts)])
    s.append([]); s.append(["Platform", "Posts"])
    for k, v in Counter(p["platform"] for p in posts).items():
        s.append([k, v])
    s.append([]); s.append(["Content pillar", "Target %", "Actual %"])
    actual = Counter(p["content_pillar"] for p in posts)
    for pl in cal.get("pillars", []):
        s.append([pl["name"], pl.get("mix_percent"), round(100 * actual.get(pl["name"], 0) / max(1, len(posts)))])
    s.append([]); s.append(["Approval status", "Posts"])
    for st in APPROVAL_STATUSES:
        s.append([st, sum(1 for p in posts if p.get("approval_status") == st)])
    s.column_dimensions["A"].width = 30

    src = wb.create_sheet("Sources")
    src.append(["ID", "Title", "Publisher", "URL", "Published", "Accessed", "Used in"])
    for c in src[1]:
        c.font = Font(bold=True)
    for x in sources.get("sources", []):
        src.append([x.get("id"), x.get("title"), x.get("publisher", ""), x.get("url"), x.get("published", ""),
                    x.get("accessed"), ", ".join(x.get("used_in", []))])
    for letter_, w in zip("ABCDEFG", (6, 50, 22, 60, 14, 12, 30)):
        src.column_dimensions[letter_].width = w
    wb.save(path)


# ---------------------------------------------------------------- Word

INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|_[^_]+_)")


def _runs(par, text: str) -> None:
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            par.add_run(part[2:-2]).bold = True
        elif part.startswith("`") and part.endswith("`"):
            par.add_run(part[1:-1]).font.name = "Courier New"
        elif part.startswith("_") and part.endswith("_") and len(part) > 2:
            par.add_run(part[1:-1]).italic = True
        else:
            par.add_run(part)


def md_to_docx(doc, text: str) -> None:
    from docx.shared import Pt

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        st = line.strip()
        if st.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            p = doc.add_paragraph()
            r = p.add_run("\n".join(block))
            r.font.name = "Courier New"
            r.font.size = Pt(9)
        elif st.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            rows = [st]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            ncol = max(len(r) for r in cells)
            t = doc.add_table(rows=len(cells), cols=ncol)
            t.style = "Table Grid"
            for ri, r in enumerate(cells):
                for ci in range(ncol):
                    par = t.cell(ri, ci).paragraphs[0]
                    _runs(par, r[ci] if ci < len(r) else "")
                    if ri == 0:
                        for run in par.runs:
                            run.bold = True
            continue
        elif m := re.match(r"^(#{1,4})\s+(.*)", st):
            doc.add_heading(m.group(2), level=min(len(m.group(1)), 4))
        elif re.match(r"^[-*]\s+", st):
            _runs(doc.add_paragraph(style="List Bullet"), re.sub(r"^[-*]\s+", "", st))
        elif re.match(r"^\d+\.\s+", st):
            _runs(doc.add_paragraph(style="List Number"), re.sub(r"^\d+\.\s+", "", st))
        elif st.startswith(">"):
            _runs(doc.add_paragraph(style="Intense Quote"), st.lstrip("> "))
        elif st in ("---", "***"):
            pass
        elif st:
            _runs(doc.add_paragraph(), st)
        i += 1


PACK_ORDER = [
    "07_delivery/approval_summary.md", "00_onboarding/brief.md", "01_research/brand_analysis.md", "01_research/audience_market.md",
    "01_research/competitors.md", "01_research/trends_{month}.md", "02_strategy/organic_strategy.md",
    "04_content/{slug}_content_{month}.md", "05_creative_briefs/{slug}_briefs_{month}.md",
    "06_qa/{slug}_qa_{month}.md", "06_qa/{slug}_qa-auto_{month}.md", "01_research/sources.md",
]


def write_docx(cdir: Path, cal: dict, path: Path) -> list[str]:
    from docx import Document

    doc = Document()
    doc.add_heading(f"{cal['client']} — Organic Social Approval Pack — {cal['month']}", 0)
    doc.add_paragraph("Prepared for review. Nothing in this pack has been published. Approve, request changes or reject "
                      "each post in the calendar spreadsheet (Approval Status column).")
    included = []
    for rel in PACK_ORDER:
        rel = rel.format(slug=cdir.name, month=cal["month"])
        f = cdir / rel
        if f.exists():
            doc.add_page_break()
            md_to_docx(doc, f.read_text(encoding="utf-8"))
            included.append(rel)
    doc.save(path)
    return included


# ---------------------------------------------------------------- main

def build(cdir: Path, month: str) -> dict:
    cal = load_json(calendar_path(cdir, month))
    src_file = cdir / "01_research" / "sources.json"
    sources = load_json(src_file) if src_file.exists() else {"sources": []}
    slug = cdir.name
    out = {
        "csv": cdir / "03_calendar" / f"{slug}_calendar_{month}.csv",
        "content": cdir / "04_content" / f"{slug}_content_{month}.md",
        "briefs": cdir / "05_creative_briefs" / f"{slug}_briefs_{month}.md",
        "xlsx": cdir / "07_delivery" / f"{slug}_calendar_{month}.xlsx",
        "docx": cdir / "07_delivery" / f"{slug}_approval-pack_{month}.docx",
    }
    for p in out.values():
        p.parent.mkdir(parents=True, exist_ok=True)
    if sources.get("sources"):
        (cdir / "01_research" / "sources.md").write_text(sources_md(cal, sources), encoding="utf-8")
    write_csv(cal, out["csv"])
    out["content"].write_text(content_md(cal), encoding="utf-8")
    out["briefs"].write_text(briefs_md(cal), encoding="utf-8")
    write_xlsx(cal, sources, out["xlsx"])
    included = write_docx(cdir, cal, out["docx"])
    return {"files": out, "docx_sections": included}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("client")
    ap.add_argument("month")
    a = ap.parse_args()
    try:
        res = build(client_dir(a.client), a.month)
    except ModuleNotFoundError as e:
        sys.exit(f"Missing library ({e.name}). Run: pip install -r requirements.txt")
    for name, p in res["files"].items():
        print(f"{name:8} {p}")
    print(f"Approval pack sections: {len(res['docx_sections'])}")


if __name__ == "__main__":
    main()
