import os
import sys
import tempfile
from pathlib import Path

# Configure before the app is imported.
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="ome-test-")
os.environ["ADMIN_PASSWORD"] = "test-pass"
os.environ["START_WORKER"] = "false"
os.environ["ANTHROPIC_API_KEY"] = ""
os.environ["SLACK_WEBHOOK_URL"] = ""
os.environ["GOOGLE_CLIENT_ID"] = ""
os.environ["GOOGLE_CLIENT_SECRET"] = ""
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest  # noqa: E402

from app import db, engine, services  # noqa: E402
from app.config import settings  # noqa: E402
from app.website import Page, SiteSnapshot  # noqa: E402
from tests.fakes import FakeLLM  # noqa: E402


@pytest.fixture
def fake(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "data_dir", tmp_path)
    db.init(settings.db_path)
    llm = FakeLLM()
    monkeypatch.setattr(services, "llm_factory", lambda: llm)
    monkeypatch.setattr(engine, "fetch_site", lambda url: SiteSnapshot(
        pages=[Page(url="https://client.example/", title="Home", description="Coffee roasters", text="We roast coffee.")]))
    return llm


@pytest.fixture
def client(fake):
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app, headers=basic("admin", "test-pass"))


def basic(user, pw):
    import base64
    return {"Authorization": "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode()}


BRIEF = {
    "business_name": "Bean There Coffee", "contact_email": "owner@example.com", "website": "client.example",
    "industry": "Specialty coffee shop", "locations": "Leeds, UK", "target_audience": "Young professionals",
    "tone_of_voice": "Warm and witty", "primary_goal": "Brand awareness", "target_month": "2026-12",
    "cadence_Instagram": "3", "cadence_TikTok": "2", "consent": "yes",
}
