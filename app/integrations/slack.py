"""Slack notifications via an Incoming Webhook (https://api.slack.com/messaging/webhooks).

Used only to notify a human that content is ready for review. It cannot publish anything.
"""
from __future__ import annotations

import httpx


class SlackError(RuntimeError):
    pass


class SlackIntegration:
    def __init__(self, webhook_url: str, http: httpx.Client | None = None):
        self.webhook_url = (webhook_url or "").strip()
        self.http = http

    def configured(self) -> bool:
        return self.webhook_url.startswith("https://hooks.slack.com/")

    def send(self, text: str) -> None:
        if not self.configured():
            raise SlackError("Slack webhook URL is not configured")
        client = self.http or httpx.Client(timeout=20)
        try:
            r = client.post(self.webhook_url, json={"text": text, "unfurl_links": False})
        finally:
            if self.http is None:
                client.close()
        if r.status_code != 200 or r.text.strip() != "ok":
            raise SlackError(f"Slack rejected the message: HTTP {r.status_code} {r.text[:200]}")
