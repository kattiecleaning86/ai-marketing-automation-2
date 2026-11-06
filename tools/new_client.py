"""Create a client workspace from the brief template.

Usage:
    python tools/new_client.py "Client Name" https://website.com 2026-12

Never overwrites existing files, so it is safe to run again for a new month.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CLIENTS, ROOT, slugify  # noqa: E402

FOLDERS = ["00_onboarding", "01_research", "02_strategy", "03_calendar", "04_content",
           "05_creative_briefs", "06_qa", "07_delivery"]
TEMPLATE = ROOT / "templates" / "client_brief_template.md"


def create(name: str, website: str, month: str, base: Path = CLIENTS) -> Path:
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month):
        raise ValueError("Month must look like YYYY-MM, e.g. 2026-12")
    slug = slugify(name)
    cdir = base / slug
    for f in FOLDERS:
        (cdir / f).mkdir(parents=True, exist_ok=True)

    brief = cdir / "00_onboarding" / "brief.md"
    if not brief.exists():
        text = TEMPLATE.read_text(encoding="utf-8")
        text = (text.replace("{{CLIENT_NAME}}", name).replace("{{WEBSITE}}", website)
                .replace("{{MONTH}}", month).replace("{{DATE}}", date.today().isoformat()))
        brief.write_text(text, encoding="utf-8")

    sources = cdir / "01_research" / "sources.json"
    if not sources.exists():
        sources.write_text(json.dumps({"client": name, "sources": []}, indent=2) + "\n", encoding="utf-8")

    readme = cdir / "README.md"
    if not readme.exists():
        readme.write_text(f"# {name} — Organic Social Status\n\n- Website: {website}\n- Current month: {month}\n"
                          f"- Stage reached: 1. Onboarding\n- Approval state: not started\n\n## Open questions\n- (none yet)\n",
                          encoding="utf-8")
    return cdir


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name")
    ap.add_argument("website")
    ap.add_argument("month", help="YYYY-MM")
    a = ap.parse_args()
    cdir = create(a.name, a.website, a.month)
    print(f"Client workspace ready: {cdir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
