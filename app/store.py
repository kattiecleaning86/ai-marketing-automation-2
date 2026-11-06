"""Read/write helpers for clients, runs, stages, sources and posts."""
from __future__ import annotations

import re
from typing import Any

from . import db

STAGES: list[tuple[str, str]] = [
    ("onboarding", "1. Save client brief"),
    ("brand_analysis", "2. Brand & website analysis"),
    ("audience_market", "3. Audience & market research"),
    ("competitors", "4. Competitor research"),
    ("strategy", "5. Organic social strategy"),
    ("trends", "6. Current trend research"),
    ("calendar", "7. Monthly content calendar"),
    ("copy", "8. Captions, hooks, CTAs, hashtags"),
    ("scripts", "9. Reel scripts & carousel copy"),
    ("briefs", "10. Designer & video editor briefs"),
    ("qa", "11. Quality check"),
    ("delivery", "12. Google Drive & Sheets delivery"),
    ("notify", "13. Slack approval notification"),
]
STAGE_LABELS = dict(STAGES)
APPROVAL_STATUSES = ["Pending Review", "Changes Requested", "Approved", "Rejected"]


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return s or "client"


# ---------- clients / runs ----------

def create_client(name: str, email: str, brief: dict) -> dict:
    base = slugify(name)
    slug, n = base, 2
    while db.q1("SELECT id FROM clients WHERE slug=?", (slug,)):
        existing = db.q1("SELECT * FROM clients WHERE slug=?", (slug,))
        if existing and existing["name"].strip().lower() == name.strip().lower():
            db.ex("UPDATE clients SET brief_json=?, contact_email=?, updated_at=? WHERE id=?",
                  (db.jdump(brief), email, db.now(), existing["id"]))
            return get_client(existing["id"])
        slug, n = f"{base}-{n}", n + 1
    cid = db.ex("INSERT INTO clients (slug, name, contact_email, brief_json, created_at, updated_at) VALUES (?,?,?,?,?,?)",
                (slug, name.strip(), email, db.jdump(brief), db.now(), db.now()))
    return get_client(cid)


def get_client(cid: int) -> dict | None:
    row = db.q1("SELECT * FROM clients WHERE id=?", (cid,))
    if row:
        row["brief"] = db.jload(row["brief_json"], {})
    return row


def create_run(client_id: int, month: str, status: str = "queued") -> int:
    rid = db.ex("INSERT INTO runs (client_id, month, status, created_at, updated_at) VALUES (?,?,?,?,?)",
                (client_id, month, status, db.now(), db.now()))
    for pos, (name, _) in enumerate(STAGES):
        db.ex("INSERT INTO stages (run_id, name, position, status) VALUES (?,?,?,?)", (rid, name, pos, "pending"))
    db.log(rid, f"Run created for {month} (status: {status})")
    return rid


def get_run(rid: int) -> dict | None:
    row = db.q1("SELECT r.*, c.name AS client_name, c.slug AS client_slug FROM runs r JOIN clients c ON c.id=r.client_id WHERE r.id=?", (rid,))
    return row


def set_run(rid: int, **fields: Any) -> None:
    fields["updated_at"] = db.now()
    cols = ", ".join(f"{k}=?" for k in fields)
    db.ex(f"UPDATE runs SET {cols} WHERE id=?", (*fields.values(), rid))


def runs_today() -> int:
    row = db.q1("SELECT COUNT(*) AS n FROM runs WHERE created_at >= date('now')")
    return row["n"] if row else 0


# ---------- stages ----------

def get_stages(rid: int) -> list[dict]:
    rows = db.q("SELECT * FROM stages WHERE run_id=? ORDER BY position", (rid,))
    for r in rows:
        r["label"] = STAGE_LABELS.get(r["name"], r["name"])
    return rows


def stage_output(rid: int, name: str) -> dict:
    row = db.q1("SELECT output_json FROM stages WHERE run_id=? AND name=?", (rid, name))
    return db.jload(row["output_json"], {}) if row else {}


def set_stage(rid: int, name: str, **fields: Any) -> None:
    if "output" in fields:
        fields["output_json"] = db.jdump(fields.pop("output"))
    cols = ", ".join(f"{k}=?" for k in fields)
    db.ex(f"UPDATE stages SET {cols} WHERE run_id=? AND name=?", (*fields.values(), rid, name))


# ---------- sources ----------

def add_sources(rid: int, found: list, stage: str) -> list[dict]:
    """Register sources the search tool really returned. Returns their records (with IDs)."""
    out = []
    for f in found:
        url = f.url if hasattr(f, "url") else f["url"]
        existing = db.q1("SELECT * FROM sources WHERE run_id=? AND url=?", (rid, url))
        if existing:
            out.append(_src(existing))
            continue
        n = (db.q1("SELECT COUNT(*) AS n FROM sources WHERE run_id=?", (rid,)) or {"n": 0})["n"] + 1
        sid = f"S{n}"
        title = getattr(f, "title", None) if hasattr(f, "title") else f.get("title")
        page_age = getattr(f, "page_age", None) if hasattr(f, "page_age") else f.get("page_age")
        evidence = getattr(f, "evidence", None) if hasattr(f, "evidence") else f.get("evidence")
        db.ex("INSERT INTO sources (run_id, sid, url, title, page_age, evidence_json, stage, accessed_at) VALUES (?,?,?,?,?,?,?,?)",
              (rid, sid, url, title or "", page_age or "", db.jdump(evidence or []), stage, db.now()))
        out.append(_src(db.q1("SELECT * FROM sources WHERE run_id=? AND sid=?", (rid, sid))))
    return out


def _src(row: dict) -> dict:
    row = dict(row)
    row["evidence"] = db.jload(row.pop("evidence_json", None), [])
    return row


def get_sources(rid: int) -> list[dict]:
    rows = db.q("SELECT * FROM sources WHERE run_id=? ORDER BY CAST(SUBSTR(sid, 2) AS INTEGER)", (rid,))
    return [_src(r) for r in rows]


# ---------- posts ----------

JSON_FIELDS = {"source_ids_json": "source_ids", "alt_hooks_json": "alt_hooks", "hashtags_json": "hashtags",
               "script_json": "script", "brief_json": "brief"}


def _post(row: dict) -> dict:
    row = dict(row)
    for col, key in JSON_FIELDS.items():
        row[key] = db.jload(row.pop(col, None), [] if key in ("source_ids", "alt_hooks", "hashtags") else {})
    return row


def get_posts(rid: int) -> list[dict]:
    return [_post(r) for r in db.q("SELECT * FROM posts WHERE run_id=? ORDER BY date, time, post_key", (rid,))]


def get_post(pid: int) -> dict | None:
    row = db.q1("SELECT * FROM posts WHERE id=?", (pid,))
    return _post(row) if row else None


def update_post(rid: int, post_key: str, **fields: Any) -> None:
    for col, key in JSON_FIELDS.items():
        if key in fields:
            fields[col] = db.jdump(fields.pop(key))
    if not fields:
        return
    cols = ", ".join(f"{k}=?" for k in fields)
    db.ex(f"UPDATE posts SET {cols} WHERE run_id=? AND post_key=?", (*fields.values(), rid, post_key))


def set_approval(pid: int, status: str, comment: str, who: str) -> None:
    if status not in APPROVAL_STATUSES:
        raise ValueError("Invalid approval status")
    db.ex("UPDATE posts SET approval_status=?, reviewer_comment=?, approved_by=?, approved_at=? WHERE id=?",
          (status, comment, who, db.now(), pid))
