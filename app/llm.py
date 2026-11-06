"""Claude API wrapper.

Two operations:
- research(): Claude with live web search / web fetch. Returns notes plus the list of
  pages the search tool *actually returned*. Only those URLs may be cited later, which
  is how the system prevents fabricated sources.
- structured(): Claude with a JSON schema (structured outputs) for reliable data.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Protocol

log = logging.getLogger(__name__)


class LLMError(RuntimeError):
    pass


@dataclass
class FoundSource:
    url: str
    title: str = ""
    page_age: str = ""
    evidence: list[str] = field(default_factory=list)


@dataclass
class ResearchResult:
    text: str
    sources: list[FoundSource]
    searches_used: int = 0


class LLM(Protocol):
    def research(self, system: str, prompt: str, max_searches: int = 8) -> ResearchResult: ...

    def structured(self, system: str, prompt: str, schema: dict, effort: str = "high", max_tokens: int = 32000) -> dict: ...


class ClaudeLLM:
    """Real Claude client (requires ANTHROPIC_API_KEY)."""

    FALLBACK_BETA = "server-side-fallback-2026-07-01"

    def __init__(self, api_key: str, model: str):
        import anthropic

        if not api_key:
            raise LLMError("ANTHROPIC_API_KEY is not configured")
        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key, max_retries=4, timeout=900)

    def _call(self, **kwargs: Any):
        # Streaming avoids HTTP timeouts on long generations; fallbacks="default" lets the
        # API re-route a safety decline to a fallback model instead of failing the stage.
        with self.client.beta.messages.stream(
            model=self.model,
            betas=[self.FALLBACK_BETA],
            fallbacks="default",
            thinking={"type": "adaptive"},
            **kwargs,
        ) as stream:
            msg = stream.get_final_message()
        if msg.stop_reason == "refusal":
            details = getattr(msg, "stop_details", None)
            raise LLMError(f"Claude declined this request ({getattr(details, 'category', None)}).")
        if msg.stop_reason == "max_tokens":
            raise LLMError("Claude response was cut off (max_tokens). Try again or reduce batch size.")
        return msg

    def research(self, system: str, prompt: str, max_searches: int = 8) -> ResearchResult:
        tools = [
            {"type": "web_search_20260209", "name": "web_search", "max_uses": max_searches},
            {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 4},
        ]
        user = {"role": "user", "content": prompt}
        assistant_blocks: list = []
        msg = None
        for _ in range(6):
            messages = [user] + ([{"role": "assistant", "content": assistant_blocks}] if assistant_blocks else [])
            msg = self._call(system=system, messages=messages, tools=tools, max_tokens=32000,
                             output_config={"effort": "medium"})
            assistant_blocks = assistant_blocks + list(msg.content)
            if msg.stop_reason != "pause_turn":
                break
        return extract_research(assistant_blocks)

    def structured(self, system: str, prompt: str, schema: dict, effort: str = "high", max_tokens: int = 32000) -> dict:
        msg = self._call(
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
        )
        text = next((b.text for b in msg.content if getattr(b, "type", "") == "text"), None)
        if text is None:
            raise LLMError("Claude returned no structured output")
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMError(f"Claude returned invalid JSON: {exc}") from exc


def extract_research(blocks: list) -> ResearchResult:
    """Pull notes text and the real, tool-returned sources out of response blocks."""
    found: dict[str, FoundSource] = {}
    texts: list[str] = []
    searches = 0

    def add(url: str, title: str = "", page_age: str = "", evidence: str | None = None):
        if not url:
            return
        src = found.setdefault(url, FoundSource(url=url))
        if title and not src.title:
            src.title = title
        if page_age and not src.page_age:
            src.page_age = page_age
        if evidence and evidence not in src.evidence and len(src.evidence) < 5:
            src.evidence.append(evidence[:500])

    for b in blocks:
        btype = getattr(b, "type", "")
        if btype == "server_tool_use" and getattr(b, "name", "") == "web_search":
            searches += 1
        elif btype == "web_search_tool_result":
            content = getattr(b, "content", None)
            if isinstance(content, list):  # error results are a single object, not a list
                for r in content:
                    add(getattr(r, "url", ""), getattr(r, "title", "") or "", getattr(r, "page_age", "") or "")
        elif btype == "web_fetch_tool_result":
            content = getattr(b, "content", None)
            url = getattr(content, "url", "") if content is not None else ""
            doc = getattr(content, "content", None)
            title = getattr(doc, "title", "") or ""
            add(url, title)
        elif btype == "text":
            texts.append(b.text)
            for c in getattr(b, "citations", None) or []:
                add(getattr(c, "url", ""), getattr(c, "title", "") or "", evidence=getattr(c, "cited_text", None))
    return ResearchResult(text="\n".join(texts).strip(), sources=list(found.values()), searches_used=searches)
