"""Google Drive + Google Sheets delivery using OAuth (your own Google account).

Scope is `drive.file`: the app can only see and edit files it created itself — it cannot read
anything else in your Drive.
"""
from __future__ import annotations

import json
from pathlib import Path

import markdown as md

from .. import db, deliverables, store

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
ROOT_FOLDER_NAME = "Organic Social Clients"
FOLDER_MIME = "application/vnd.google-apps.folder"
DOC_MIME = "application/vnd.google-apps.document"


class GoogleError(RuntimeError):
    pass


class GoogleIntegration:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    # ---------- OAuth ----------
    def configured(self) -> bool:
        return bool(self.client_id and self.client_secret)

    def connected(self) -> bool:
        return self.configured() and bool(db.get_setting("google_token"))

    def _flow(self, state: str | None = None):
        from google_auth_oauthlib.flow import Flow

        cfg = {"web": {"client_id": self.client_id, "client_secret": self.client_secret,
                       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                       "token_uri": "https://oauth2.googleapis.com/token",
                       "redirect_uris": [self.redirect_uri]}}
        flow = Flow.from_client_config(cfg, scopes=SCOPES, state=state)
        flow.redirect_uri = self.redirect_uri
        return flow

    def auth_url(self) -> str:
        if not self.configured():
            raise GoogleError("Google OAuth client ID/secret not configured")
        flow = self._flow()
        url, state = flow.authorization_url(access_type="offline", prompt="consent", include_granted_scopes="true")
        db.set_setting("google_oauth_state", state)
        db.set_setting("google_oauth_verifier", getattr(flow, "code_verifier", None) or "")
        return url

    def finish(self, code: str, state: str) -> None:
        if state != db.get_setting("google_oauth_state"):
            raise GoogleError("OAuth state mismatch — please start the connection again")
        flow = self._flow(state=state)
        verifier = db.get_setting("google_oauth_verifier")
        if verifier:
            flow.code_verifier = verifier
        flow.fetch_token(code=code)
        db.set_setting("google_token", flow.credentials.to_json())
        db.set_setting("google_oauth_state", None)
        db.set_setting("google_oauth_verifier", None)

    def disconnect(self) -> None:
        db.set_setting("google_token", None)

    def _creds(self):
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials

        raw = db.get_setting("google_token")
        if not raw:
            raise GoogleError("Google is not connected")
        creds = Credentials.from_authorized_user_info(json.loads(raw), SCOPES)
        if not creds.valid and creds.refresh_token:
            creds.refresh(Request())
            db.set_setting("google_token", creds.to_json())
        return creds

    def _services(self):
        from googleapiclient.discovery import build

        creds = self._creds()
        return (build("drive", "v3", credentials=creds, cache_discovery=False),
                build("sheets", "v4", credentials=creds, cache_discovery=False))

    # ---------- Drive helpers ----------
    @staticmethod
    def _find(drive, name: str, parent: str | None, mime: str | None = None) -> str | None:
        safe = name.replace("\\", "\\\\").replace("'", "\\'")
        q = [f"name = '{safe}'", "trashed = false"]
        if parent:
            q.append(f"'{parent}' in parents")
        if mime:
            q.append(f"mimeType = '{mime}'")
        res = drive.files().list(q=" and ".join(q), fields="files(id)", pageSize=1).execute()
        files = res.get("files", [])
        return files[0]["id"] if files else None

    def _folder(self, drive, name: str, parent: str | None) -> str:
        fid = self._find(drive, name, parent, FOLDER_MIME)
        if fid:
            return fid
        body = {"name": name, "mimeType": FOLDER_MIME}
        if parent:
            body["parents"] = [parent]
        return drive.files().create(body=body, fields="id").execute()["id"]

    def _upload_doc(self, drive, name: str, html: str, parent: str) -> str:
        from googleapiclient.http import MediaInMemoryUpload

        media = MediaInMemoryUpload(html.encode("utf-8"), mimetype="text/html", resumable=False)
        existing = self._find(drive, name, parent, DOC_MIME)
        if existing:
            drive.files().update(fileId=existing, media_body=media).execute()
            return existing
        body = {"name": name, "mimeType": DOC_MIME, "parents": [parent]}
        return drive.files().create(body=body, media_body=media, fields="id").execute()["id"]

    # ---------- Delivery ----------
    def deliver(self, rid: int, local_files: list[str]) -> dict:
        drive, sheets = self._services()
        run = store.get_run(rid)
        client_name, slug, month = run["client_name"], run["client_slug"], run["month"]
        base = deliverables.client_dir(rid)

        root = self._folder(drive, ROOT_FOLDER_NAME, None)
        client_folder = self._folder(drive, f"Organic Social — {client_name}", root)
        sub_ids: dict[str, str] = {}
        uploaded = []
        for rel in local_files:
            if not rel.endswith(".md"):
                continue
            parts = Path(rel).parts
            parent = client_folder
            if len(parts) > 1:
                if parts[0] not in sub_ids:
                    sub_ids[parts[0]] = self._folder(drive, parts[0], client_folder)
                parent = sub_ids[parts[0]]
            text = (base / rel).read_text(encoding="utf-8")
            html = "<html><body>" + md.markdown(text, extensions=["tables", "fenced_code"]) + "</body></html>"
            name = Path(rel).stem if Path(rel).stem != "README" else f"{slug}_status"
            uploaded.append({"path": rel, "id": self._upload_doc(drive, name, html, parent)})

        sheet_id = self._ensure_sheet(drive, sheets, client_name, slug, client_folder)
        self._write_calendar_tab(sheets, sheet_id, rid, month)
        return {
            "folder_url": f"https://drive.google.com/drive/folders/{client_folder}",
            "sheet_url": f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit",
            "sheet_id": sheet_id,
            "files": uploaded,
        }

    def _ensure_sheet(self, drive, sheets, client_name: str, slug: str, folder: str) -> str:
        key = f"gsheet:{slug}"
        sid = db.get_setting(key)
        if sid:
            try:
                drive.files().get(fileId=sid, fields="id, trashed").execute()
                return sid
            except Exception:  # noqa: BLE001 — sheet deleted; create a new one
                pass
        created = sheets.spreadsheets().create(body={"properties": {"title": f"{client_name} — Content Calendar"}},
                                               fields="spreadsheetId").execute()
        sid = created["spreadsheetId"]
        meta = drive.files().get(fileId=sid, fields="parents").execute()
        drive.files().update(fileId=sid, addParents=folder, removeParents=",".join(meta.get("parents", [])), fields="id").execute()
        db.set_setting(key, sid)
        return sid

    def _tab_id(self, sheets, sheet_id: str, title: str) -> int | None:
        meta = sheets.spreadsheets().get(spreadsheetId=sheet_id, fields="sheets.properties").execute()
        for s in meta.get("sheets", []):
            if s["properties"]["title"] == title:
                return s["properties"]["sheetId"]
        return None

    def _write_calendar_tab(self, sheets, sheet_id: str, rid: int, month: str) -> None:
        tab = self._tab_id(sheets, sheet_id, month)
        if tab is None:
            res = sheets.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={"requests": [
                {"addSheet": {"properties": {"title": month}}}]}).execute()
            tab = res["replies"][0]["addSheet"]["properties"]["sheetId"]
        rows = [deliverables.CALENDAR_COLUMNS] + deliverables.calendar_rows(rid)
        sheets.spreadsheets().values().clear(spreadsheetId=sheet_id, range=f"'{month}'").execute()
        sheets.spreadsheets().values().update(spreadsheetId=sheet_id, range=f"'{month}'!A1", valueInputOption="RAW",
                                              body={"values": rows}).execute()
        ncols = len(deliverables.CALENDAR_COLUMNS)
        requests = [
            {"updateSheetProperties": {"properties": {"sheetId": tab, "gridProperties": {"frozenRowCount": 1}},
                                       "fields": "gridProperties.frozenRowCount"}},
            {"repeatCell": {"range": {"sheetId": tab, "startRowIndex": 0, "endRowIndex": 1},
                            "cell": {"userEnteredFormat": {"textFormat": {"bold": True},
                                                           "backgroundColor": {"red": 0.9, "green": 0.93, "blue": 0.98}}},
                            "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
            {"repeatCell": {"range": {"sheetId": tab, "startRowIndex": 1, "endRowIndex": len(rows), "startColumnIndex": 0, "endColumnIndex": ncols},
                            "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP", "verticalAlignment": "TOP"}},
                            "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"}},
            {"setDataValidation": {
                "range": {"sheetId": tab, "startRowIndex": 1, "endRowIndex": max(2, len(rows)),
                          "startColumnIndex": deliverables.APPROVAL_COL, "endColumnIndex": deliverables.APPROVAL_COL + 1},
                "rule": {"condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": v} for v in store.APPROVAL_STATUSES]},
                         "showCustomUi": True, "strict": True}}},
            {"updateDimensionProperties": {"range": {"sheetId": tab, "dimension": "COLUMNS", "startIndex": 0, "endIndex": ncols},
                                           "properties": {"pixelSize": 220}, "fields": "pixelSize"}},
        ]
        sheets.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={"requests": requests}).execute()

    # ---------- Approval sync ----------
    def read_approvals(self, sheet_id: str, month: str) -> list[tuple[str, str, str]]:
        _, sheets = self._services()
        res = sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"'{month}'").execute()
        rows = res.get("values", [])
        out = []
        for r in rows[1:]:
            if not r:
                continue
            status = r[deliverables.APPROVAL_COL] if len(r) > deliverables.APPROVAL_COL else ""
            comment = r[deliverables.COMMENT_COL] if len(r) > deliverables.COMMENT_COL else ""
            out.append((r[0], status, comment))
        return out

    def write_approval(self, sheet_id: str, month: str, post_key: str, status: str, comment: str) -> None:
        _, sheets = self._services()
        res = sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"'{month}'!A:A").execute()
        keys = [r[0] if r else "" for r in res.get("values", [])]
        if post_key not in keys:
            return
        row = keys.index(post_key) + 1
        col = lambda i: chr(ord("A") + i)
        sheets.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=f"'{month}'!{col(deliverables.APPROVAL_COL)}{row}:{col(deliverables.COMMENT_COL)}{row}",
            valueInputOption="RAW", body={"values": [[status, comment]]}).execute()
