"""Builds the Claude client and integrations from env vars or values saved in Settings."""
from __future__ import annotations

from typing import Callable

from . import db
from .config import settings
from .integrations.google import GoogleIntegration
from .integrations.slack import SlackIntegration
from .llm import LLM, ClaudeLLM

# Keys the Settings page may store. Environment variables always take precedence.
CONFIG_KEYS = {
    "ANTHROPIC_API_KEY": "anthropic_api_key",
    "SLACK_WEBHOOK_URL": "slack_webhook_url",
    "GOOGLE_CLIENT_ID": "google_client_id",
    "GOOGLE_CLIENT_SECRET": "google_client_secret",
}


def config_value(env_name: str) -> str:
    attr = CONFIG_KEYS[env_name]
    return getattr(settings, attr) or db.get_setting(f"cfg:{env_name}", "") or ""


def config_source(env_name: str) -> str:
    if getattr(settings, CONFIG_KEYS[env_name]):
        return "environment"
    return "settings page" if db.get_setting(f"cfg:{env_name}") else "not set"


def _default_llm() -> LLM | None:
    key = config_value("ANTHROPIC_API_KEY")
    return ClaudeLLM(key, settings.model) if key else None


# Tests replace this factory with a fake; production uses the real Claude client.
llm_factory: Callable[[], LLM | None] = _default_llm


def get_llm() -> LLM | None:
    return llm_factory()


def google() -> GoogleIntegration:
    return GoogleIntegration(config_value("GOOGLE_CLIENT_ID"), config_value("GOOGLE_CLIENT_SECRET"),
                             f"{settings.base_url}/admin/google/callback")


def slack() -> SlackIntegration:
    return SlackIntegration(config_value("SLACK_WEBHOOK_URL"))


def integrations() -> dict:
    return {"google": google(), "slack": slack()}
