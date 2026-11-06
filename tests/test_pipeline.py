import csv
import io

from app import db, deliverables, engine, store, worker
from app.qa import REQUIRED_FIELDS
from tests.conftest import BRIEF
from tests.fakes import FakeLLM, FakeSlack


def submit(client, **overrides):
    r = client.post("/brief", data={**BRIEF, **overrides})
    assert r.status_code == 200, r.text
    return db.q1("SELECT id FROM runs ORDER BY id DESC LIMIT 1")["id"]


def test_brief_form_renders(client):
    r = client.get("/brief")
    assert r.status_code == 200
    assert "Organic Social Media Brief" in r.text and "cadence_Instagram" in r.text


def test_brief_validation(client):
    r = client.post("/brief", data={"business_name": "", "consent": "yes"})
    assert r.status_code == 400
    assert "Please complete" in r.text
    assert db.q1("SELECT COUNT(*) AS n FROM runs")["n"] == 0


def test_honeypot_blocks_bots(client):
    r = client.post("/brief", data={**BRIEF, "website_confirm": "spam"})
    assert r.status_code == 200
    assert db.q1("SELECT COUNT(*) AS n FROM runs")["n"] == 0


def test_full_pipeline_without_integrations(client, fake):
    rid = submit(client)
    assert store.get_run(rid)["status"] == "queued"
    assert worker.process_next() is True

    run = store.get_run(rid)
    assert run["status"] == "awaiting_approval", run["error"]
    stages = {s["name"]: s for s in store.get_stages(rid)}
    for name in ("onboarding", "brand_analysis", "audience_market", "competitors", "strategy", "trends",
                 "calendar", "copy", "scripts", "briefs", "qa"):
        assert stages[name]["status"] == "done", (name, stages[name]["error"])
    # Not connected => honestly skipped, never pretended.
    assert stages["delivery"]["status"] == "skipped" and "Google not connected" in stages["delivery"]["note"]
    assert stages["notify"]["status"] == "skipped" and "Slack not configured" in stages["notify"]["note"]

    posts = store.get_posts(rid)
    # Dec 2026: Instagram 3/wk (Mon/Wed/Fri) = 14, TikTok 2/wk (Tue/Thu) = 9
    assert len(posts) == 23
    assert {p["platform"] for p in posts} == {"Instagram", "TikTok"}
    for p in posts:
        assert p["approval_status"] == "Pending Review"
        assert p["date"].startswith("2026-12-")
        for field, label in REQUIRED_FIELDS:
            assert p.get(field), f"{p['post_key']} missing {label}"
        assert p["brief_id"].startswith("CB-2026-12-")

    base = deliverables.client_dir(rid)
    for rel in ["00_onboarding/brief.md", "01_research/brand_analysis.md", "01_research/audience_market.md",
                "01_research/competitors.md", "01_research/trends_2026-12.md", "01_research/sources.md",
                "02_strategy/organic_strategy.md", "03_calendar/bean-there-coffee_calendar_2026-12_v1.csv",
                "04_content/bean-there-coffee_content_2026-12_v1.md", "05_creative_briefs/bean-there-coffee_briefs_2026-12_v1.md",
                "06_qa/bean-there-coffee_qa_2026-12_v1.md", "07_delivery/delivery_log.md", "README.md"]:
        assert (base / rel).exists(), rel
    rows = list(csv.reader(io.StringIO((base / "03_calendar/bean-there-coffee_calendar_2026-12_v1.csv").read_text())))
    assert rows[0] == deliverables.CALENDAR_COLUMNS
    assert len(rows) == 24
    assert "Slack not configured" in (base / "07_delivery/delivery_log.md").read_text()

    # QA ran the editor review and the automatic fix pass.
    qa_out = store.stage_output(rid, "qa")
    assert qa_out["auto_fixed_posts"]


def test_unverified_source_ids_are_removed(client, fake):
    fake.bogus_source = True
    rid = submit(client)
    worker.process_next()
    valid = {s["sid"] for s in store.get_sources(rid)}
    assert "S999" not in valid and "S404" not in valid
    for p in store.get_posts(rid):
        assert set(p["source_ids"]) <= valid
    brand = store.stage_output(rid, "brand_analysis")
    assert brand["unverified_refs_removed"] >= 1
    assert "S404" not in str(brand["data"])


def test_slack_notification_sent(client, fake, monkeypatch):
    slack = FakeSlack()
    from app import services
    monkeypatch.setattr(services, "integrations", lambda: {"google": services.google(), "slack": slack})
    rid = submit(client)
    worker.process_next()
    assert store.get_run(rid)["status"] == "awaiting_approval"
    assert len(slack.sent) == 1
    msg = slack.sent[0]
    assert "Bean There Coffee" in msg and "ready for review" in msg
    assert "Nothing will be published until it is marked Approved" in msg
    assert f"/admin/runs/{rid}" in msg


def test_failure_then_retry_resumes(client, fake):
    fake.fail_on = "current social media trends"
    rid = submit(client)
    worker.process_next()
    run = store.get_run(rid)
    assert run["status"] == "failed" and "Current trend research" in run["error"]
    stages = {s["name"]: s["status"] for s in store.get_stages(rid)}
    assert stages["strategy"] == "done" and stages["trends"] == "failed" and stages["calendar"] == "pending"
    calls_before = len(fake.calls)

    r = client.post(f"/admin/runs/{rid}/start", follow_redirects=False)
    assert r.status_code == 303
    worker.process_next()
    assert store.get_run(rid)["status"] == "awaiting_approval"
    # Earlier stages were not repeated: the first new call is the trends research.
    assert fake.calls[calls_before] == "research"


def test_missing_claude_key_fails_clearly(client, monkeypatch):
    from app import services
    monkeypatch.setattr(services, "llm_factory", lambda: None)
    rid = submit(client)
    worker.process_next()
    run = store.get_run(rid)
    assert run["status"] == "failed"
    assert "ANTHROPIC_API_KEY" in run["error"]
    stages = {s["name"]: s["status"] for s in store.get_stages(rid)}
    assert stages["onboarding"] == "done"


def test_admin_requires_password(fake):
    from fastapi.testclient import TestClient

    from app.main import app
    anon = TestClient(app)
    assert anon.get("/admin").status_code == 401
    from tests.conftest import basic
    assert TestClient(app, headers=basic("admin", "wrong")).get("/admin").status_code == 401


def test_dashboard_and_approval(client, fake):
    rid = submit(client)
    worker.process_next()
    assert client.get("/admin").status_code == 200
    page = client.get(f"/admin/runs/{rid}")
    assert page.status_code == 200 and "Content calendar" in page.text
    post = store.get_posts(rid)[0]
    r = client.post(f"/admin/posts/{post['id']}/approval", data={"status": "Approved", "comment": "Looks great"},
                    follow_redirects=False)
    assert r.status_code == 303
    updated = store.get_post(post["id"])
    assert updated["approval_status"] == "Approved" and updated["approved_by"] == "admin"
    assert client.post(f"/admin/posts/{post['id']}/approval", data={"status": "Published"}).status_code == 400
    # file download works and path traversal is blocked
    assert client.get(f"/admin/runs/{rid}/files/README.md").status_code == 200
    assert client.get(f"/admin/runs/{rid}/files/../../app.db").status_code in (404, 422)
    assert client.get(f"/admin/runs/{rid}/files/..%2F..%2Fapp.db").status_code == 404


def test_rerun_copy_keeps_approved_posts(client, fake):
    rid = submit(client)
    worker.process_next()
    posts = store.get_posts(rid)
    store.set_approval(posts[0]["id"], "Approved", "", "admin")
    client.post(f"/admin/runs/{rid}/rerun-stage", data={"stage": "copy"})
    assert store.get_post(posts[1]["id"])["caption"] is None
    assert store.get_post(posts[0]["id"])["caption"]
    worker.process_next()
    assert store.get_run(rid)["status"] == "awaiting_approval"
    assert all(p["caption"] for p in store.get_posts(rid))


def test_settings_page_saves_keys(client):
    assert client.get("/admin/settings").status_code == 200
    client.post("/admin/settings", data={"SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/T/B/X"})
    from app import services
    assert services.slack().configured()
    assert "settings page" == services.config_source("SLACK_WEBHOOK_URL")


def test_build_slots_respects_cap():
    slots = engine.build_slots("2026-12", {"Instagram": 7, "TikTok": 7, "LinkedIn": 5}, cap=40)
    assert len(slots) <= 40
    assert all(s["date"].startswith("2026-12") for s in slots)
    assert [s["slot"] for s in slots] == list(range(1, len(slots) + 1))
