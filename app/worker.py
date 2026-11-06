"""Background worker: processes queued runs one at a time in a daemon thread."""
from __future__ import annotations

import logging
import threading
import time

from . import db, engine, services, store

log = logging.getLogger(__name__)
_wake = threading.Event()
_thread: threading.Thread | None = None


def recover_interrupted() -> None:
    """Runs that were 'running' when the server stopped are resumed from their unfinished stage."""
    for r in db.q("SELECT id FROM runs WHERE status='running'"):
        db.ex("UPDATE stages SET status='pending' WHERE run_id=? AND status='running'", (r["id"],))
        store.set_run(r["id"], status="queued")
        db.log(r["id"], "Server restarted mid-run — resuming from the unfinished stage")


def process_next() -> bool:
    row = db.q1("SELECT id FROM runs WHERE status='queued' ORDER BY id LIMIT 1")
    if not row:
        return False
    engine.run_pipeline(row["id"], services.get_llm(), services.integrations())
    return True


def _loop() -> None:
    while True:
        try:
            while process_next():
                pass
        except Exception:  # noqa: BLE001
            log.exception("Worker loop error")
        _wake.wait(timeout=15)
        _wake.clear()


def start() -> None:
    global _thread
    if _thread and _thread.is_alive():
        return
    recover_interrupted()
    _thread = threading.Thread(target=_loop, name="workflow-worker", daemon=True)
    _thread.start()


def wake() -> None:
    _wake.set()
