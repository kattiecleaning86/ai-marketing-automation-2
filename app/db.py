"""SQLite storage. One file, no server, safe for a single-instance app."""
from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    contact_email TEXT,
    brief_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    month TEXT NOT NULL,
    status TEXT NOT NULL,              -- queued | running | awaiting_approval | failed | paused
    error TEXT,
    drive_folder_url TEXT,
    sheet_url TEXT,
    sheet_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS stages (
    run_id INTEGER NOT NULL REFERENCES runs(id),
    name TEXT NOT NULL,
    position INTEGER NOT NULL,
    status TEXT NOT NULL,              -- pending | running | done | failed | skipped
    output_json TEXT,
    note TEXT,
    error TEXT,
    started_at TEXT,
    finished_at TEXT,
    PRIMARY KEY (run_id, name)
);
CREATE TABLE IF NOT EXISTS sources (
    run_id INTEGER NOT NULL REFERENCES runs(id),
    sid TEXT NOT NULL,
    url TEXT NOT NULL,
    title TEXT,
    page_age TEXT,
    evidence_json TEXT,
    stage TEXT,
    accessed_at TEXT NOT NULL,
    PRIMARY KEY (run_id, sid)
);
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL REFERENCES runs(id),
    post_key TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT,
    platform TEXT NOT NULL,
    content_pillar TEXT,
    objective TEXT,
    topic TEXT,
    research_rationale TEXT,
    source_ids_json TEXT DEFAULT '[]',
    hook TEXT,
    alt_hooks_json TEXT DEFAULT '[]',
    caption TEXT,
    cta TEXT,
    hashtags_json TEXT DEFAULT '[]',
    alt_text TEXT,
    format TEXT,
    script_json TEXT,
    script_text TEXT,
    visual_direction TEXT,
    brief_id TEXT,
    brief_json TEXT,
    kpi_objective TEXT,
    approval_status TEXT NOT NULL DEFAULT 'Pending Review',
    reviewer_comment TEXT,
    approved_by TEXT,
    approved_at TEXT,
    qa_status TEXT,
    qa_notes TEXT,
    UNIQUE (run_id, post_key)
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    ts TEXT NOT NULL,
    level TEXT NOT NULL,
    message TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

_lock = threading.Lock()
_db_path: Path | None = None


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def init(path: Path) -> None:
    global _db_path
    path.parent.mkdir(parents=True, exist_ok=True)
    _db_path = path
    with connect() as conn:
        conn.executescript(SCHEMA)


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    if _db_path is None:
        raise RuntimeError("Database not initialised")
    conn = sqlite3.connect(_db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        with _lock:
            yield conn
            conn.commit()
    finally:
        conn.close()


def q(sql: str, params: tuple | list = ()) -> list[dict[str, Any]]:
    with connect() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def q1(sql: str, params: tuple | list = ()) -> dict[str, Any] | None:
    rows = q(sql, params)
    return rows[0] if rows else None


def ex(sql: str, params: tuple | list = ()) -> int:
    with connect() as conn:
        cur = conn.execute(sql, params)
        return cur.lastrowid


def log(run_id: int | None, message: str, level: str = "info") -> None:
    ex("INSERT INTO events (run_id, ts, level, message) VALUES (?,?,?,?)", (run_id, now(), level, message))


def get_setting(key: str, default: str | None = None) -> str | None:
    row = q1("SELECT value FROM settings WHERE key=?", (key,))
    return row["value"] if row else default


def set_setting(key: str, value: str | None) -> None:
    if value is None:
        ex("DELETE FROM settings WHERE key=?", (key,))
    else:
        ex("INSERT INTO settings (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))


def jload(raw: str | None, default: Any = None) -> Any:
    if not raw:
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return default


def jdump(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)
