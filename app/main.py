"""Web application: public client brief form + password-protected admin dashboard."""
from __future__ import annotations

import logging
import secrets
from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import db, deliverables, services, store, worker
from .config import settings
from .schemas import PLATFORMS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
HERE = Path(__file__).parent
templates = Jinja2Templates(directory=HERE / "templates")
security = HTTPBasic(auto_error=False)

BRIEF_TEXT_FIELDS = [
    "business_name", "contact_name", "contact_email", "website", "industry", "locations", "products_services",
    "price_positioning", "current_offers", "primary_goal", "targets_90_day", "target_audience", "languages",
    "mission_values", "tone_of_voice", "words_to_use", "words_to_avoid", "visual_guidelines", "canva_brand_kit",
    "social_handles", "what_worked", "competitors_known", "compliance_notes", "sensitive_topics", "approvers",
    "content_resources", "on_camera_people", "ugc_rights", "timezone", "additional_notes",
]


def next_month() -> str:
    t = date.today()
    return f"{t.year + (t.month == 12)}-{(t.month % 12) + 1:02d}"


def create_app() -> FastAPI:
    db.init(settings.db_path)
    app = FastAPI(title="Organic Marketing Engine", docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
    if settings.start_worker:
        worker.start()

    def admin(creds: HTTPBasicCredentials | None = Depends(security)) -> str:
        if not settings.admin_password:
            raise HTTPException(503, "Admin dashboard disabled: set ADMIN_PASSWORD to enable it.")
        ok = creds is not None and secrets.compare_digest(creds.username.encode(), settings.admin_username.encode()) \
            and secrets.compare_digest(creds.password.encode(), settings.admin_password.encode())
        if not ok:
            raise HTTPException(401, "Authentication required", headers={"WWW-Authenticate": "Basic"})
        return creds.username

    def render(request: Request, template: str, status_code: int = 200, **ctx):
        return templates.TemplateResponse(request, template, ctx, status_code=status_code)

    # ------------------------------------------------------------ public
    @app.get("/healthz", response_class=PlainTextResponse)
    def healthz():
        return "ok"

    @app.get("/")
    def home():
        return RedirectResponse("/brief")

    @app.get("/brief", response_class=HTMLResponse)
    def brief_form(request: Request):
        return render(request, "brief.html", platforms=PLATFORMS, default_month=next_month())

    @app.post("/brief", response_class=HTMLResponse)
    async def brief_submit(request: Request):
        form = await request.form()
        if form.get("website_confirm"):  # honeypot field, hidden from humans
            return render(request, "thanks.html", name="")
        brief = {k: (form.get(k) or "").strip() for k in BRIEF_TEXT_FIELDS}
        errors = [label for key, label in (("business_name", "Business name"), ("contact_email", "Contact email"),
                                           ("website", "Website"), ("industry", "Industry"))
                  if not brief.get(key)]
        cadence = {}
        for p in PLATFORMS:
            try:
                n = int(form.get(f"cadence_{p}") or 0)
            except ValueError:
                n = 0
            if n > 0:
                cadence[p] = min(n, 7)
        if not cadence:
            errors.append("At least one platform with posts per week")
        month = (form.get("target_month") or next_month()).strip()
        if len(month) != 7 or month[4] != "-":
            errors.append("Target month (YYYY-MM)")
        if not form.get("consent"):
            errors.append("Confirmation checkbox")
        if errors:
            return render(request, "brief.html", platforms=PLATFORMS, default_month=month, errors=errors,
                          values=dict(form), status_code=400)
        brief["cadence"] = cadence
        brief["target_month"] = month
        client = store.create_client(brief["business_name"], brief["contact_email"], brief)
        status = "queued"
        if not settings.auto_start_runs:
            status = "paused"
        elif store.runs_today() >= settings.max_runs_per_day:
            status = "paused"
            db.log(None, f"Daily run limit ({settings.max_runs_per_day}) reached — run for {client['name']} paused", "warn")
        rid = store.create_run(client["id"], month, status=status)
        if status == "queued":
            worker.wake()
        return render(request, "thanks.html", name=client["name"], rid=rid)

    # ------------------------------------------------------------ admin
    @app.get("/admin", response_class=HTMLResponse)
    def dashboard(request: Request, user: str = Depends(admin)):
        runs = db.q("""SELECT r.*, c.name AS client_name, c.slug AS client_slug,
                         (SELECT COUNT(*) FROM posts p WHERE p.run_id=r.id) AS n_posts,
                         (SELECT COUNT(*) FROM posts p WHERE p.run_id=r.id AND p.approval_status='Approved') AS n_approved,
                         (SELECT s.name FROM stages s WHERE s.run_id=r.id AND s.status IN ('running','failed','pending')
                          ORDER BY s.position LIMIT 1) AS current_stage
                       FROM runs r JOIN clients c ON c.id=r.client_id ORDER BY r.id DESC""")
        for r in runs:
            r["current_label"] = store.STAGE_LABELS.get(r["current_stage"] or "", "—")
        return render(request, "dashboard.html", runs=runs, health=health_status(), brief_url=f"{settings.base_url}/brief")

    @app.get("/admin/runs/{rid}", response_class=HTMLResponse)
    def run_detail(request: Request, rid: int, user: str = Depends(admin)):
        run = store.get_run(rid)
        if not run:
            raise HTTPException(404)
        client = store.get_client(run["client_id"])
        posts = store.get_posts(rid)
        for p in posts:
            p["qa_issues"] = db.jload(p.get("qa_notes"), [])
        base = deliverables.client_dir(rid)
        files = sorted(str(f.relative_to(base)) for f in base.rglob("*") if f.is_file()) if base.exists() else []
        events = db.q("SELECT * FROM events WHERE run_id=? ORDER BY id DESC LIMIT 60", (rid,))
        return render(request, "run.html", run=run, client=client, stages=store.get_stages(rid), posts=posts,
                      files=files, events=events, sources=store.get_sources(rid), statuses=store.APPROVAL_STATUSES,
                      google_connected=services.google().connected())

    @app.get("/admin/runs/{rid}/files/{path:path}")
    def run_file(rid: int, path: str, user: str = Depends(admin)):
        base = deliverables.client_dir(rid).resolve()
        target = (base / path).resolve()
        if base not in target.parents or not target.is_file():
            raise HTTPException(404)
        return FileResponse(target, filename=target.name)

    @app.post("/admin/runs/{rid}/start")
    def run_start(rid: int, user: str = Depends(admin)):
        run = store.get_run(rid)
        if not run:
            raise HTTPException(404)
        if run["status"] in ("failed", "paused", "awaiting_approval"):
            db.ex("UPDATE stages SET status='pending', error=NULL WHERE run_id=? AND status='failed'", (rid,))
            if run["status"] == "awaiting_approval":  # re-attempt skipped integrations (e.g. after connecting Google)
                db.ex("UPDATE stages SET status='pending', note=NULL WHERE run_id=? AND status='skipped'", (rid,))
            store.set_run(rid, status="queued", error=None)
            db.log(rid, f"Run (re)started by {user}")
            worker.wake()
        return RedirectResponse(f"/admin/runs/{rid}", status_code=303)

    @app.post("/admin/runs/{rid}/rerun-stage")
    def rerun_stage(rid: int, stage: str = Form(...), user: str = Depends(admin)):
        names = [s for s, _ in store.STAGES]
        if stage not in names:
            raise HTTPException(400)
        idx = names.index(stage)
        for later in names[idx:]:
            store.set_stage(rid, later, status="pending", error=None, note=None)
        # The calendar stage recreates all posts. For later content stages, clear that stage's
        # output (and the stages after it) on posts that are not yet approved, so they regenerate.
        content_cols = [("copy", "caption"), ("scripts", "script_text"), ("briefs", "brief_id")]
        if stage in dict(content_cols):
            start = [s for s, _ in content_cols].index(stage)
            for _, col in content_cols[start:]:
                db.ex(f"UPDATE posts SET {col}=NULL WHERE run_id=? AND approval_status != 'Approved'", (rid,))
        store.set_run(rid, status="queued", error=None)
        db.log(rid, f"{user} requested a re-run from: {store.STAGE_LABELS[stage]}")
        worker.wake()
        return RedirectResponse(f"/admin/runs/{rid}", status_code=303)

    @app.post("/admin/posts/{pid}/approval")
    def post_approval(pid: int, status: str = Form(...), comment: str = Form(""), user: str = Depends(admin)):
        post = store.get_post(pid)
        if not post:
            raise HTTPException(404)
        try:
            store.set_approval(pid, status, comment.strip(), user)
        except ValueError:
            raise HTTPException(400, "Invalid status")
        db.log(post["run_id"], f"{post['post_key']} set to '{status}' by {user}")
        run = store.get_run(post["run_id"])
        g = services.google()
        if run.get("sheet_id") and g.connected():
            try:
                g.write_approval(run["sheet_id"], run["month"], post["post_key"], status, comment.strip())
            except Exception as exc:  # noqa: BLE001
                db.log(post["run_id"], f"Could not update Google Sheet: {exc}", "warn")
        deliverables.write_all(post["run_id"])
        return RedirectResponse(f"/admin/runs/{post['run_id']}#{post['post_key']}", status_code=303)

    @app.post("/admin/runs/{rid}/sync-sheet")
    def sync_sheet(rid: int, user: str = Depends(admin)):
        run = store.get_run(rid)
        g = services.google()
        if not (run and run.get("sheet_id") and g.connected()):
            raise HTTPException(400, "No Google Sheet connected for this run")
        changed = 0
        posts = {p["post_key"]: p for p in store.get_posts(rid)}
        for key, status, comment in g.read_approvals(run["sheet_id"], run["month"]):
            p = posts.get(key)
            if p and status in store.APPROVAL_STATUSES and (status != p["approval_status"] or comment != (p.get("reviewer_comment") or "")):
                store.set_approval(p["id"], status, comment, f"{user} (via Google Sheet)")
                changed += 1
        db.log(rid, f"Synced approvals from Google Sheet: {changed} changes")
        deliverables.write_all(rid)
        return RedirectResponse(f"/admin/runs/{rid}", status_code=303)

    @app.post("/admin/clients/{cid}/new-run")
    def new_run(cid: int, month: str = Form(...), user: str = Depends(admin)):
        if not store.get_client(cid):
            raise HTTPException(404)
        rid = store.create_run(cid, month.strip())
        worker.wake()
        return RedirectResponse(f"/admin/runs/{rid}", status_code=303)

    # ------------------------------------------------------------ settings
    @app.get("/admin/settings", response_class=HTMLResponse)
    def settings_page(request: Request, msg: str = "", user: str = Depends(admin)):
        return render(request, "settings.html", health=health_status(), msg=msg,
                      redirect_uri=f"{settings.base_url}/admin/google/callback", base_url=settings.base_url)

    @app.post("/admin/settings")
    async def settings_save(request: Request, user: str = Depends(admin)):
        form = await request.form()
        for key in services.CONFIG_KEYS:
            val = (form.get(key) or "").strip()
            if val:
                db.set_setting(f"cfg:{key}", val)
            elif form.get(f"clear_{key}"):
                db.set_setting(f"cfg:{key}", None)
        return RedirectResponse("/admin/settings?msg=Saved", status_code=303)

    @app.post("/admin/settings/slack-test")
    def slack_test(user: str = Depends(admin)):
        try:
            services.slack().send(":wave: Test message from the Organic Marketing Engine. Slack notifications are working.")
            msg = "Slack test message sent"
        except Exception as exc:  # noqa: BLE001
            msg = f"Slack test failed: {exc}"
        return RedirectResponse(f"/admin/settings?msg={msg}", status_code=303)

    @app.get("/admin/google/connect")
    def google_connect(user: str = Depends(admin)):
        try:
            return RedirectResponse(services.google().auth_url(), status_code=303)
        except Exception as exc:  # noqa: BLE001
            return RedirectResponse(f"/admin/settings?msg=Google connection failed: {exc}", status_code=303)

    @app.get("/admin/google/callback")
    def google_callback(code: str = "", state: str = "", error: str = "", user: str = Depends(admin)):
        if error:
            return RedirectResponse(f"/admin/settings?msg=Google authorization declined: {error}", status_code=303)
        try:
            services.google().finish(code, state)
            msg = "Google Drive & Sheets connected"
        except Exception as exc:  # noqa: BLE001
            msg = f"Google connection failed: {exc}"
        return RedirectResponse(f"/admin/settings?msg={msg}", status_code=303)

    @app.post("/admin/google/disconnect")
    def google_disconnect(user: str = Depends(admin)):
        services.google().disconnect()
        return RedirectResponse("/admin/settings?msg=Google disconnected", status_code=303)

    return app


def health_status() -> dict:
    g = services.google()
    return {
        "claude": bool(services.config_value("ANTHROPIC_API_KEY")),
        "claude_source": services.config_source("ANTHROPIC_API_KEY"),
        "model": settings.model,
        "google_configured": g.configured(),
        "google_connected": g.connected(),
        "slack": services.slack().configured(),
        "slack_source": services.config_source("SLACK_WEBHOOK_URL"),
        "admin_password": bool(settings.admin_password),
        "base_url": settings.base_url,
    }


app = create_app()
