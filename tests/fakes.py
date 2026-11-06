"""Test doubles. FakeLLM is used ONLY by the automated tests — never by the running app."""
from __future__ import annotations

import re

from app import schemas
from app.llm import FoundSource, ResearchResult


def fill(schema: dict, name: str = "value", i: int = 0):
    t = schema.get("type")
    if "enum" in schema:
        return schema["enum"][i % len(schema["enum"])]
    if t == "object":
        return {k: fill(v, k, i) for k, v in schema["properties"].items()}
    if t == "array":
        return [fill(schema["items"], name, j) for j in range(2)]
    if t == "integer":
        return 30 if name == "duration_seconds" else i + 1
    if name == "source_ids":
        return "S1"
    return f"Test {name.replace('_', ' ')} {i + 1}"


class FakeLLM:
    def __init__(self, fail_on: str | None = None, bogus_source: bool = False):
        self.calls: list[str] = []
        self.fail_on = fail_on
        self.bogus_source = bogus_source

    def research(self, system, prompt, max_searches=8):
        self.calls.append("research")
        if self.fail_on and self.fail_on in prompt:
            self.fail_on = None
            raise RuntimeError("simulated research failure")
        n = len(self.calls)
        return ResearchResult(text="Fake research notes for tests.", searches_used=2, sources=[
            FoundSource(url=f"https://example.org/report-{n}", title=f"Example report {n}", page_age="2026-10-01",
                        evidence=["Example cited text"]),
            FoundSource(url=f"https://example.org/news-{n}", title=f"Example news {n}"),
        ])

    def structured(self, system, prompt, schema, effort="high", max_tokens=32000):
        self.calls.append("structured")
        data = fill(schema)
        keys = re.findall(r'"post_key": "(P\d+)"', prompt)
        if schema is schemas.STRATEGY:
            data["content_pillars"] = [
                {"name": n, "purpose": "p", "mix_percent": m, "funnel_stage": "Awareness", "example_topics": ["t"]}
                for n, m in (("Educate", 40), ("Behind the scenes", 30), ("Community", 30))]
        elif schema is schemas.CALENDAR:
            slots = [int(s) for s in re.findall(r"^slot (\d+):", prompt, re.M)]
            pillars = ["Educate", "Behind the scenes", "Community"]
            fmts = ["Reel", "Carousel", "Static image"]
            data["entries"] = [{"slot": s, "content_pillar": pillars[s % 3], "objective": "Awareness",
                                "topic": f"Topic {s}", "research_rationale": "Because research says so",
                                "source_ids": ["S1", "S999"] if self.bogus_source else ["S1"],
                                "format": fmts[s % 3], "kpi_objective": "Saves >= 3% of reach", "suggested_time": "18:00"}
                               for s in slots]
        elif schema in (schemas.COPY, schemas.QA_FIX):
            data["posts"] = [{**fill(schema["properties"]["posts"]["items"], i=n), "post_key": k,
                              "hook": f"Hook for {k}", "hashtags": ["#BrandTag", "#NicheTag"]} for n, k in enumerate(keys)]
        elif schema is schemas.SCRIPTS:
            data["posts"] = [{**fill(schema["properties"]["posts"]["items"], i=n), "post_key": k} for n, k in enumerate(keys)]
            for item in data["posts"]:
                item["script_type"] = "reel_script"
        elif schema is schemas.BRIEFS:
            data["posts"] = [{**fill(schema["properties"]["posts"]["items"], i=n), "post_key": k} for n, k in enumerate(keys)]
        elif schema is schemas.QA_REVIEW:
            data["issues"] = [{"post_key": keys[0], "severity": "fail", "category": "Claims",
                               "issue": "Unsupported claim", "fix_instruction": "Remove the claim"}] if keys else []
        elif schema is schemas.COMPETITORS:
            item = schema["properties"]["competitors"]["items"]
            data["competitors"] = [dict(fill(item, i=n), type="Direct") for n in range(3)]
        if self.bogus_source and schema is schemas.BRAND:
            data["strengths"][0]["source_ids"] = ["S1", "S404"]
        return data


class FakeSlack:
    def __init__(self):
        self.sent: list[str] = []

    def configured(self):
        return True

    def send(self, text):
        self.sent.append(text)
