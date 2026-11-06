from types import SimpleNamespace as NS
from unittest.mock import MagicMock

import httpx

from app import qa
from app.integrations.slack import SlackError, SlackIntegration
from app.llm import extract_research
from app.website import fetch_site


def post(**kw):
    base = dict(post_key="P01", date="2026-12-01", platform="Instagram", content_pillar="Educate", objective="Awareness",
                topic="t", research_rationale="r", hook="h", caption="c", cta="cta", hashtags=["#A"], format="Static image",
                script_text="N/A", visual_direction="v", brief_id="CB-1", kpi_objective="k", approval_status="Pending Review",
                source_ids=[], script={})
    base.update(kw)
    return base


def test_qa_passes_clean_post():
    res = qa.check_posts([post()], set())
    assert res["counts"] == {"fail": 0, "warn": 0}


def test_qa_platform_limits_and_completeness():
    res = qa.check_posts([
        post(post_key="P01", platform="X", caption="x" * 300),
        post(post_key="P02", hashtags=[f"#t{i}" for i in range(31)]),
        post(post_key="P03", format="Reel", script={}),
        post(post_key="P04", cta=""),
        post(post_key="P05", source_ids=["S9"]),
        post(post_key="P06", caption="Sales grew 45% last year"),
    ], valid_source_ids={"S1"})
    msgs = {k: [i["issue"] for i in v] for k, v in res["posts"].items()}
    assert any("limit is 280" in m for m in msgs["P01"])
    assert any("allows 30" in m for m in msgs["P02"])
    assert any("scene-by-scene" in m for m in msgs["P03"])
    assert any("Missing field: CTA" in m for m in msgs["P04"])
    assert any("unknown source IDs" in m for m in msgs["P05"])
    assert any("statistic" in m for m in msgs["P06"])


def test_qa_duplicates_and_pillar_mix():
    posts = [post(post_key=f"P{i}", hook="Same hook", topic=f"t{i}") for i in range(4)]
    res = qa.check_posts(posts, set(), {"Educate": 50, "Inspire": 50})
    assert any(i["check"] == "Uniqueness" for i in res["posts"]["P0"])
    assert any("Inspire" in i["issue"] for i in res["global"])


def test_extract_research_collects_only_tool_returned_sources():
    blocks = [
        NS(type="server_tool_use", name="web_search"),
        NS(type="web_search_tool_result", content=[NS(url="https://a.example/1", title="A", page_age="2026-10-02")]),
        NS(type="web_search_tool_result", content=NS(error_code="max_uses_exceeded")),  # error object, not list
        NS(type="web_fetch_tool_result", content=NS(url="https://b.example/2", content=NS(title="B"))),
        NS(type="text", text="Notes.", citations=[NS(url="https://a.example/1", title="A", cited_text="quote")]),
    ]
    res = extract_research(blocks)
    assert res.searches_used == 1
    assert {s.url for s in res.sources} == {"https://a.example/1", "https://b.example/2"}
    a = next(s for s in res.sources if s.url.endswith("/1"))
    assert a.evidence == ["quote"] and a.page_age == "2026-10-02"
    assert res.text == "Notes."


def test_slack_send_success_and_error():
    seen = {}

    def ok(request):
        seen["body"] = request.content
        return httpx.Response(200, text="ok")

    s = SlackIntegration("https://hooks.slack.com/services/T/B/X", http=httpx.Client(transport=httpx.MockTransport(ok)))
    s.send("hello")
    assert b"hello" in seen["body"]
    bad = SlackIntegration("https://hooks.slack.com/services/T/B/X",
                           http=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(404, text="no_service"))))
    try:
        bad.send("x")
        raise AssertionError("expected SlackError")
    except SlackError as e:
        assert "no_service" in str(e)
    assert not SlackIntegration("https://evil.example/hook").configured()


def test_fetch_site_extracts_text_and_socials():
    pages = {
        "https://shop.example/": '<html><head><title>Shop</title><meta name="description" content="Desc"></head><body>'
                                 '<p>Hello world</p><a href="/about">About</a><a href="https://instagram.com/shop">IG</a>'
                                 '<script>bad()</script></body></html>',
        "https://shop.example/about": "<html><title>About</title><body>Our story</body></html>",
    }

    def handler(request):
        html = pages.get(str(request.url).rstrip("/") + ("/" if str(request.url).count("/") == 2 else ""))
        return httpx.Response(200 if html else 404, text=html or "", headers={"content-type": "text/html"})

    snap = fetch_site("shop.example", client=httpx.Client(transport=httpx.MockTransport(handler)))
    assert [p.title for p in snap.pages] == ["Shop", "About"]
    assert "Hello world" in snap.pages[0].text and "bad()" not in snap.pages[0].text
    assert snap.social_links == ["https://instagram.com/shop"]


def test_google_deliver_calls_drive_and_sheets(fake, tmp_path, monkeypatch):
    from app import deliverables, store
    from app.integrations.google import GoogleIntegration

    cid = store.create_client("Acme", "a@example.com", {"business_name": "Acme"})["id"]
    rid = store.create_run(cid, "2026-12")
    files = deliverables.write_all(rid)
    drive, sheets = MagicMock(), MagicMock()
    drive.files().list().execute.return_value = {"files": []}
    drive.files().create().execute.return_value = {"id": "F1"}
    drive.files().get().execute.return_value = {"parents": ["root"]}
    sheets.spreadsheets().create().execute.return_value = {"spreadsheetId": "SHEET1"}
    sheets.spreadsheets().get().execute.return_value = {"sheets": []}
    sheets.spreadsheets().batchUpdate().execute.return_value = {"replies": [{"addSheet": {"properties": {"sheetId": 7}}}]}
    g = GoogleIntegration("id", "secret", "http://localhost/cb")
    monkeypatch.setattr(g, "_services", lambda: (drive, sheets))
    out = g.deliver(rid, files)
    assert out["sheet_id"] == "SHEET1"
    assert out["sheet_url"].endswith("/SHEET1/edit")
    assert out["folder_url"].endswith("/F1")
    values_call = sheets.spreadsheets().values().update.call_args
    assert values_call.kwargs["body"]["values"][0] == deliverables.CALENDAR_COLUMNS
