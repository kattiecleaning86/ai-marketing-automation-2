"""Application settings, read from environment variables (or a local .env file)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv(path: Path) -> None:
    """Minimal .env loader: KEY=VALUE lines, no overrides of real env vars."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv(ROOT / ".env")


def _bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    data_dir: Path = field(default_factory=lambda: Path(os.environ.get("DATA_DIR", ROOT / "data")))
    base_url: str = field(default_factory=lambda: os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/"))
    admin_password: str = field(default_factory=lambda: os.environ.get("ADMIN_PASSWORD", ""))
    admin_username: str = field(default_factory=lambda: os.environ.get("ADMIN_USERNAME", "admin"))

    # Claude
    anthropic_api_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""))
    model: str = field(default_factory=lambda: os.environ.get("CLAUDE_MODEL", "claude-opus-5-5"))

    # Workflow
    auto_start_runs: bool = field(default_factory=lambda: _bool("AUTO_START_RUNS", True))
    max_runs_per_day: int = field(default_factory=lambda: int(os.environ.get("MAX_RUNS_PER_DAY", "10")))
    max_posts_per_month: int = field(default_factory=lambda: int(os.environ.get("MAX_POSTS_PER_MONTH", "40")))
    start_worker: bool = field(default_factory=lambda: _bool("START_WORKER", True))

    # Google (OAuth "Web application" client from Google Cloud Console)
    google_client_id: str = field(default_factory=lambda: os.environ.get("GOOGLE_CLIENT_ID", ""))
    google_client_secret: str = field(default_factory=lambda: os.environ.get("GOOGLE_CLIENT_SECRET", ""))

    # Slack (Incoming Webhook URL)
    slack_webhook_url: str = field(default_factory=lambda: os.environ.get("SLACK_WEBHOOK_URL", ""))

    @property
    def db_path(self) -> Path:
        return self.data_dir / "app.db"

    @property
    def clients_dir(self) -> Path:
        return self.data_dir / "clients"


settings = Settings()


def reload_settings() -> Settings:
    """Re-read environment (used by tests)."""
    global settings
    settings = Settings()
    return settings
