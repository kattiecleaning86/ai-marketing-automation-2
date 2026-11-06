"""Tests for the local workflow tools. Run: python -m pytest -q"""
import copy
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build_exports  # noqa: E402
import new_client  # noqa: E402
import qa_check  # noqa: E402
from common import COLUMNS  # noqa: E402

SOURCES = {"sources": [{"id": "S1", "title": "Report", "publisher": "Pub", "url": "https://example.org/r",
                        "published": "2026-10-01", "accessed": "2026-11-06", "used_in": ["trends"]}]}


def post(i=1, **kw):
    p = {
        "id": f"P{i:02d}", "date": f"2026-12-{i:02d}", "time": "18:00", "platform": "Instagram",
        "content_pillar": "Educate", "objective": "Awareness", "topic": f"Topic {i}",
        "research_rationale": "Why now", "source_ids": ["S1"], "hook": f"Hook {i}", "alt_hooks": ["a", "b"],
        "caption": "A caption", "cta": "Save this", "hashtags": ["#One", "#Two"], "format": "Carousel",
        "script": {"type": "carousel", "slides": [{"n": n, "headline": f"H{n}", "body": "b"} for n in (1, 2, 3)]},
        "alt_text": "Alt", "visual_direction": "Bright", "kpi_objective": "Saves",
        "creative_brief": {"id": f"CB-2026-12-{i:02d}", "summary": "s", "specs": "1080x1350", "key_message": "k",
                           "mood_and_style": "m", "dos": ["d"], "donts": ["n"], "shot_list": ["x"]},
        "approval_status": "Pending Review", "reviewer_comments": "",
    }
    p.update(kw)
    return p


def cal(posts):
    return {"client": "Test Co", "month": "2026-12", "pillars": [{"name": "Educate", "mix_percent": 100}], "posts": posts}


def fails(res):
    return [(k, m) for k, v in res["issues"].items() for s, c, m in v if s == "FAIL"]


def test_clean_calendar_passes():
    res = qa_check.check(cal([post(1), post(2)]), SOURCES, "2026-12")
    assert res["fail"] == 0, fails(res)


def test_qa_catches_problems():
    posts = [
        post(1, cta=""),
        post(2, source_ids=["S99"]),
        post(3, platform="X", caption="x" * 300),
        post(4, format="Reel", script={"type": "reel", "scenes": []}),
        post(5, caption="Sales grew 40% this year", source_ids=[]),
        post(6, approval_status="Approved"),
        post(7, date="2027-01-02"),
        post(8, content_pillar="Mystery"),
        post(9, hashtags=["#ok", "bad tag"]),
    ]
    msgs = " | ".join(m for _, m in fails(qa_check.check(cal(posts), SOURCES, "2026-12")))
    for expected in ["Missing field: cta", "S99", "limit 280", "scene-by-scene", "statistic",
                     "without a named human approver", "outside 2026-12", "not in the strategy", "Malformed"]:
        assert expected in msgs, expected


def test_instagram_hard_hashtag_limit():
    res = qa_check.check(cal([post(1, hashtags=[f"#t{i}" for i in range(6)])]), SOURCES, "2026-12")
    assert any("hard limit" in m for _, m in fails(res))


def test_new_client_scaffold_is_idempotent(tmp_path):
    cdir = new_client.create("Bean & Co.", "https://bean.example", "2026-12", base=tmp_path)
    assert cdir.name == "bean-co"
    brief = cdir / "00_onboarding" / "brief.md"
    assert "Bean & Co." in brief.read_text() and "2026-12" in brief.read_text()
    brief.write_text("edited")
    new_client.create("Bean & Co.", "https://bean.example", "2027-01", base=tmp_path)
    assert brief.read_text() == "edited"  # never overwritten
    assert json.loads((cdir / "01_research" / "sources.json").read_text())["sources"] == []


def test_build_exports(tmp_path):
    cdir = new_client.create("Test Co", "https://t.example", "2026-12", base=tmp_path)
    posts = [post(1), post(2, platform="LinkedIn", format="Text post", script={"type": "none"})]
    (cdir / "03_calendar" / "test-co_calendar_2026-12.json").write_text(json.dumps(cal(posts)))
    (cdir / "01_research" / "sources.json").write_text(json.dumps(SOURCES))
    (cdir / "02_strategy" / "organic_strategy.md").write_text("# Strategy\n\n| A | B |\n|---|---|\n| 1 | **2** |\n\n- point\n")
    res = build_exports.build(cdir, "2026-12")
    rows = list(csv.reader(res["files"]["csv"].open()))
    assert rows[0] == [h for _, h in COLUMNS] and len(rows) == 3
    assert "Slide 1: H1" in rows[1][12] and rows[2][12].startswith("N/A")

    from openpyxl import load_workbook
    wb = load_workbook(res["files"]["xlsx"])
    assert wb.sheetnames == ["Calendar", "Summary", "Sources"]
    ws = wb["Calendar"]
    assert ws["Q1"].value == "Approval Status" and ws["Q2"].value == "Pending Review"
    assert ws.data_validations.dataValidation[0].formula1.startswith('"Pending Review')

    from docx import Document
    d = Document(res["files"]["docx"])
    text = "\n".join(p.text for p in d.paragraphs)
    assert "Approval Pack" in text and "Strategy" in text
    assert len(d.tables) == 2  # strategy table + generated sources table
    assert "https://example.org/r" in (cdir / "01_research" / "sources.md").read_text()
    assert "02_strategy/organic_strategy.md" in res["docx_sections"]
    assert "CB-2026-12-01" in res["files"]["briefs"].read_text()


def test_sample_client_passes_qa():
    """The committed sample client must stay QA-clean."""
    cdir = ROOT / "clients" / "sample-harbor-hearth-bakery"
    if not cdir.exists():
        return
    month = "2026-12"
    data = json.loads((cdir / "03_calendar" / f"{cdir.name}_calendar_{month}.json").read_text())
    sources = json.loads((cdir / "01_research" / "sources.json").read_text())
    res = qa_check.check(data, sources, month)
    assert res["fail"] == 0, fails(res)
    assert all(p["approval_status"] == "Pending Review" for p in data["posts"])
    assert copy.deepcopy(data)  # valid JSON structure
