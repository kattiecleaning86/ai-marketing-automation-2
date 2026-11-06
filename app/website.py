"""Fetch a client's website and extract readable text for brand analysis."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (compatible; OrganicMarketingEngine/1.0; brand-analysis)"
INTERESTING = re.compile(r"about|story|services|products|shop|menu|team|mission|values|pricing|faq", re.I)


@dataclass
class Page:
    url: str
    title: str
    description: str
    text: str


@dataclass
class SiteSnapshot:
    pages: list[Page] = field(default_factory=list)
    social_links: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def as_prompt(self, max_chars: int = 18000) -> str:
        if not self.pages:
            return "Website could not be retrieved. Errors: " + "; ".join(self.errors or ["none recorded"])
        parts = []
        budget = max_chars
        for p in self.pages:
            chunk = f"### {p.url}\nTitle: {p.title}\nMeta description: {p.description}\n{p.text}\n"
            parts.append(chunk[:budget])
            budget -= len(chunk)
            if budget <= 0:
                break
        if self.social_links:
            parts.append("Social links found on site: " + ", ".join(self.social_links))
        return "\n".join(parts)


SOCIAL_HOSTS = ("instagram.com", "facebook.com", "tiktok.com", "linkedin.com", "youtube.com",
                "pinterest.com", "x.com", "twitter.com", "threads.net")


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if url and not re.match(r"^https?://", url, re.I):
        url = "https://" + url
    return url


def _parse(url: str, html: str) -> tuple[Page, list[str], list[str]]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()
    title = (soup.title.string or "").strip() if soup.title and soup.title.string else ""
    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    desc = (desc_tag.get("content") or "").strip() if desc_tag else ""
    text = re.sub(r"\s+", " ", soup.get_text(" ")).strip()[:6000]
    links, socials = [], []
    host = urlparse(url).netloc
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"]).split("#")[0]
        h = urlparse(href).netloc.lower()
        if any(s in h for s in SOCIAL_HOSTS):
            socials.append(href)
        elif h == host and INTERESTING.search(href):
            links.append(href)
    return Page(url=url, title=title, description=desc, text=text), links, socials


def fetch_site(url: str, max_pages: int = 5, client: httpx.Client | None = None) -> SiteSnapshot:
    snap = SiteSnapshot()
    url = normalize_url(url)
    if not url:
        snap.errors.append("No website provided")
        return snap
    own = client is None
    client = client or httpx.Client(timeout=20, follow_redirects=True, headers={"User-Agent": USER_AGENT})
    try:
        queue, seen = [url], set()
        while queue and len(snap.pages) < max_pages:
            u = queue.pop(0)
            if u in seen:
                continue
            seen.add(u)
            try:
                r = client.get(u)
                if r.status_code >= 400 or "html" not in r.headers.get("content-type", "html"):
                    snap.errors.append(f"{u}: HTTP {r.status_code}")
                    continue
                page, links, socials = _parse(str(r.url), r.text)
                snap.pages.append(page)
                for s in socials:
                    if s not in snap.social_links:
                        snap.social_links.append(s)
                if len(seen) == 1:
                    queue.extend(dict.fromkeys(links))
            except httpx.HTTPError as exc:
                snap.errors.append(f"{u}: {exc.__class__.__name__}")
    finally:
        if own:
            client.close()
    return snap
