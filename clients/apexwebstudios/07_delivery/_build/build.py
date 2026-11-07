#!/usr/bin/env python3
"""Build all final Apex Web Studios deliverables (CSV, XLSX, and JSON specs for the DOCX renderer)."""
import csv, json, os, sys
from collections import Counter
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from posts import POSTS, SITE  # noqa: E402

CLIENT = os.path.abspath(os.path.join(HERE, "..", ".."))
DELIV = os.path.join(CLIENT, "07_delivery")
SPECS = os.path.join(HERE, "specs")
os.makedirs(SPECS, exist_ok=True)
SLUG, MONTH, TZ = "apexwebstudios", "2026-12", "ET"
TODAY = "2026-11-07"

# ------------------------------------------------------------------ sources (verified register, abridged for client docs)
SRC = {
 "B01": ("Apex Web Studios — Homepage", "https://apexwebstudios.net/", "Verified 2026-11-07"),
 "B02": ("Apex Web Studios — About Us", "https://apexwebstudios.net/about-us", "Verified 2026-11-06"),
 "B03": ("Apex Web Studios — Service pages (Web Design & Development; UI/UX Design)", "https://apexwebstudios.net/web-design-and-development", "Verified 2026-11-07"),
 "B04": ("Apex Web Studios — Pricing", "https://apexwebstudios.net/pricing", "Verified 2026-11-07"),
 "B06": ("Apex Web Studios — Terms and Conditions (updated July 10, 2026)", "https://apexwebstudios.net/terms-and-conditions", "Verified 2026-11-06"),
 "B08": ("Apex Web Studios — Testimonials", "https://apexwebstudios.net/testimonials", "Verified 2026-11-07"),
 "B09": ("Apex Web Studios — Blog index", "https://apexwebstudios.net/blogs", "Verified 2026-11-06"),
 "B16": ("X — @ApexWebStudios public profile", "https://x.com/ApexWebStudios", "Observed 2026-11-07"),
 "B17": ("Instagram — @apex_web_design public metadata", "https://www.instagram.com/apex_web_design/", "Observed 2026-11-07"),
 "T03": ("TechCrunch — Instagram cracks down on content aggregators (2026-04-30)", "https://techcrunch.com/2026/04/30/instagram-restricts-reach-of-content-aggregators-in-new-crackdown/", "Verified"),
 "T04": ("Social Media Today — Instagram prioritizes original content (2026-04-30)", "https://www.socialmediatoday.com/news/instagram-updates-algorithm-to-benefit-original-creators/819016/", "Verified"),
 "T05": ("Social Media Today — Instagram allows scheduling of Trial Reels (2026-04-02)", "https://www.socialmediatoday.com/news/instagram-allows-creators-to-schedule-trial-reels/816549/", "Verified"),
 "T09": ("Social Media Today — LinkedIn updates its feed algorithm (2026-03-12)", "https://www.socialmediatoday.com/news/linkedin-updates-its-feed-algorithm/814638/", "Verified"),
 "T12": ("Social Media Today — LinkedIn video creation tips (2026-05-25)", "https://www.socialmediatoday.com/news/linkedin-shares-video-creation-tips-based-on-platform-trends/821050/", "Verified"),
 "T14": ("Meta Newsroom — Threads reaches 500M monthly users (2026-06-16)", "https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/", "Verified"),
 "T18": ("YouTube Blog — Shorts series (2026-09-23)", "https://blog.youtube/news-and-events/made-on-youtube-creators-shorts-series-tv-features/", "Verified"),
 "T21": ("Buffer — Best content format on social platforms in 2026 (2026-03-19)", "https://buffer.com/resources/data-best-content-format-social-media/", "Verified"),
 "T23": ("Socialinsider — LinkedIn organic benchmarks (updated 2026-11-06)", "https://www.socialinsider.io/social-media-benchmarks/linkedin", "Verified (corrected wording)"),
 "T24": ("Buffer — How often to post on LinkedIn (2025-08-28, >12 months old)", "https://buffer.com/resources/how-often-to-post-on-linkedin/", "Verified — outdated flag"),
 "T25": ("Buffer — Best time to post on LinkedIn (2026-09-09)", "https://buffer.com/resources/best-time-to-post-on-linkedin/", "Verified"),
 "T26": ("Buffer — Best time to post on Instagram (2026-09-23)", "https://buffer.com/resources/when-is-the-best-time-to-post-on-instagram/", "Verified"),
 "T28": ("Emplifi — Q3 2026 social media benchmarks (2026-10-15)", "https://emplifi.io/resources/blog/q3-2026-social-media-benchmarks/", "Verified"),
 "T29": ("Sprout Social — 2026 Social Media Content Strategy Report (2026-01-09)", "https://sproutsocial.com/insights/data/2026-social-media-content-strategy-report/", "Verified (corrected wording)"),
 "T30": ("Sprout Social — The state of social media in 2026 (2026-09-23)", "https://sproutsocial.com/insights/the-state-of-social-media/", "Verified (corrected wording)"),
 "T31": ("Hootsuite — Social Media Trends 2026", "https://www.hootsuite.com/research/social-trends", "Verified"),
 "T32": ("Hootsuite Blog — Social media trends 2026 (2026-01-18)", "https://blog.hootsuite.com/social-media-trends/", "Verified"),
 "T33": ("Hootsuite Blog — Organic reach (2026-03-16)", "https://blog.hootsuite.com/organic-reach-declining/", "Verified"),
 "T34": ("Ahrefs — AI Overviews reduce clicks (update) (2026-02-04)", "https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/", "Verified"),
 "T37": ("Seer Interactive — 2026 CTR research (2026-04-24)", "https://www.seerinteractive.com/news/search-engine-land-and-other-search-pubs-cite-seers-2026-ctr-research", "Verified"),
 "T38": ("Google — Search I/O 2026 updates (2026-05-19)", "https://blog.google/products-and-platforms/products/search/search-io-2026/", "Verified (corrected scope)"),
 "T45": ("Seyfarth Shaw — 2026 Mid-Year ADA Title III report (2026-09-09)", "https://www.adatitleiii.com/2026/09/2026-mid-year-report-ada-title-iii-federal-lawsuit-numbers-are-climbing/", "Verified"),
 "T46": ("Seyfarth Shaw — Website accessibility lawsuit filings in 2025 (2026-03-25)", "https://www.adatitleiii.com/2026/03/federal-court-website-accessibility-lawsuit-filings-bounce-back-in-2025/", "Verified"),
 "T50": ("Squarespace — Best small business website builders (updated 2026-09-15)", "https://www.squarespace.com/blog/best-small-business-website-builder", "Verified"),
 "T53": ("Adobe — US holiday shopping season forecast (2026-09-28)", "https://news.adobe.com/news/2026/09/adobe-us-holiday-shopping-season-to-hit-record", "Verified"),
 "T54": ("NRF — 2026 holiday sales forecast (2026-10-15)", "https://nrf.com/media-center/press-releases/nrf-forecasts-2026-holiday-sales-growth-as-consumers-remain-resilient", "Verified"),
 "T56": ("UN DESA — International Day of Persons with Disabilities 2026", "https://social.desa.un.org/issues/disability/events/2026-international-day-of-persons-with-disabilities-idpd", "Verified"),
 "T57": ("Hebcal — Chanukah 2026", "https://www.hebcal.com/holidays/chanukah-2026", "Verified"),
 "T61": ("Social Media Today — Instagram limits hashtags to five (2025-12-18)", "https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/", "Verified (trade press quoting Instagram)"),
}

def src_line(i):
    t, u, s = SRC[i]
    return f"{i} — {t} — {u} ({s})"

# ------------------------------------------------------------------ helpers
def is_video(p): return p["format"] in ("Reel", "Vertical video")
def is_slides(p): return "slides" in p
def ig(p): return p["platform"] != "LinkedIn"

def script_text(p):
    if is_video(p):
        s = " | ".join(f"[{t}] VISUAL: {v} / ON-SCREEN: {o} / VO: {vo} / AUDIO: {a}" for t, v, o, vo, a in p["script"])
        return s + (f" | {p['end_note']}" if p.get("end_note") else "")
    if is_slides(p):
        return " | ".join(f"{lab}: {h} — {b}" for lab, h, b in p["slides"])
    return "N/A (single image). Copy on image: " + " / ".join(p.get("copy_on_image", []))

def due(d):
    y, m, dd = map(int, d.split("-")); x = date(y, m, dd); k = 0
    while k < 3:
        x -= timedelta(days=1)
        if x.weekday() < 5: k += 1
    return x.isoformat()

def link_of(p):
    return p.get("link") or ""

SPEC = {
    "Reel": "9:16 · 1080×1920 px · MP4 (H.264) · 30–60 s · burned-in captions · keep key text inside the central safe area (avoid the top ~250 px and bottom ~400 px) · cover frame with a 4:5-safe title",
    "Vertical video": "9:16 · 1080×1920 px · MP4 · 45–60 s · burned-in captions plus an SRT file",
    "Carousel": "4:5 · 1080×1350 px per slide · PNG · slide count as listed · about 25 words or fewer per slide",
    "Document carousel (PDF)": "4:5 · 1080×1350 px pages exported as one PDF (10 pages or fewer) · about 30 words or fewer per page · document title = hook",
    "Static image": "4:5 · 1080×1350 px · PNG",
    "Text post + image": "4:5 · 1080×1350 px PNG (legible as a thumbnail)",
}
BRAND_DO = ["Dark backgrounds (#0A0A0A / #1A1A1A) with red #D23030 as the single accent colour",
            "Urbanist for headlines, Inter for body copy, IBM Plex Mono for numbers and labels (the website's typefaces)",
            "Real team members, Apex's own screens and website, or purpose-made demo sites only",
            "High contrast and large type: every asset must read clearly on a phone",
            "Apex logo (the light version on dark backgrounds) bottom-right or on the end card"]
BRAND_DONT = ["No other studios' designs, client work without written permission, or stock 'handshake' clichés",
              "No guarantee language (rankings, results) and no unconfirmed self-reported statistics (e.g. '+1K clients')",
              "No legal-advice wording on accessibility content",
              "Licensed audio only (the platform's in-app library or licensed tracks)",
              "Purple (#811EA1) only as a tiny accent, if at all; one accent colour per frame"]

pill = Counter(p["pillar"] for p in POSTS if not p["tier"].startswith("Reserve"))
STD = [p for p in POSTS if not p["tier"].startswith("Reserve")]
LITE = [p for p in POSTS if p["tier"].startswith("Core")]
READY = [p for p in POSTS if p["readiness"].startswith("Ready")]
BLOCKED = [p for p in POSTS if p["readiness"].startswith("Blocked")]

# ------------------------------------------------------------------ CSV (exact 16 columns)
HEADER = ["Date", "Platform", "Content Pillar", "Objective", "Topic", "Research Rationale", "Hook", "Caption", "CTA",
          "Hashtags", "Format", "Reel Script / Carousel Slide Copy", "Visual Direction", "Creative Brief", "KPI Objective", "Approval Status"]

def row16(p):
    return [f"{p['date']} {p['time']} {TZ}", p["platform"], p["pillar"], p["objective"], p["topic"], p["rationale"] + " Sources: " + ", ".join(p["sources"]),
            p["hook"], p["caption"], p["cta"], p["hashtags"], p["format"], script_text(p), p["visual"],
            f"{p['cb']} — see Creative Briefs document", p["kpi"], "Pending Review"]

with open(os.path.join(CLIENT, "03_calendar", f"{SLUG}_calendar_{MONTH}_v2.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL); w.writerow(HEADER)
    for p in POSTS: w.writerow(row16(p))

# ------------------------------------------------------------------ XLSX
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

F = "Arial"
BLACK, RED, GREY, LIGHT = "0A0A0A", "D23030", "383838", "F2F2F2"
hdr_font = Font(name=F, bold=True, color="FFFFFF", size=10)
hdr_fill = PatternFill("solid", fgColor=BLACK)
body = Font(name=F, size=9)
bold = Font(name=F, size=9, bold=True)
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
PILL_FILL = {"Build Smarter (Educate)": "DDEBF7", "Proof & Results": "E2EFDA", "Behind the Build": "FFF2CC",
             "Offers & Packages": "FCE4D6", "Community & Moments": "EDE7F6"}

wb = Workbook()

def title_block(ws, title, sub):
    ws["A1"] = title; ws["A1"].font = Font(name=F, size=16, bold=True, color=BLACK)
    ws["A2"] = sub; ws["A2"].font = Font(name=F, size=9, italic=True, color=GREY)

def header(ws, r, cols, widths):
    for i, (c, wdt) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row=r, column=i, value=c)
        cell.font, cell.fill, cell.alignment, cell.border = hdr_font, hdr_fill, Alignment(wrap_text=True, vertical="center"), border
        ws.column_dimensions[get_column_letter(i)].width = wdt
    ws.row_dimensions[r].height = 30

# --- Read Me
ws = wb.active; ws.title = "Read Me"
title_block(ws, "Apex Web Studios — December 2026 Organic Social Content Calendar", f"Version 2 (final for review) · Prepared {TODAY} · Status: ALL POSTS PENDING REVIEW, NOTHING IS SCHEDULED OR PUBLISHED")
rows = [
 ("How to use this workbook", ""),
 ("1. Calendar 2026-12", "One row per post. Columns A–P follow the agency calendar standard. Set 'Approval Status' (column P) with the dropdown: Pending Review / Changes Requested / Approved / Rejected. Write feedback in 'Reviewer Comments' (column Q)."),
 ("Editable cells", "Only columns P (Approval Status) and Q (Reviewer Comments) are for reviewers. Everything else is generated from the master content file. Request copy changes in column Q."),
 ("Example", "P = 'Changes Requested'; Q = 'Swap hook to alternate #2; keep caption.'"),
 ("2. Overview", "Live counts by pillar, platform, plan tier, readiness and approval status. These update automatically as you change column P."),
 ("3. Creative Briefs", "Designer and video-editor specifications per post (brief ID = column N on the calendar)."),
 ("4. Sources", "Every research source used, with link and verification status. Only sources marked Verified/Observed are used in post copy."),
 ("5. Client Inputs Needed", "The facts and permissions still missing. Posts that depend on them are marked 'Blocked: client input' in column V."),
 ("Plan tiers", f"Core (Lite) = {len(LITE)} posts that need no client input except a same-day price check. Standard = {len(STD)} posts (recommended). Reserve = 1 optional post."),
 ("Posting frequency basis", "No posting frequency was supplied by the client. Observed public activity is low (X: 57 posts since Jan 2023, newest Jul 30, 2026; Instagram @apex_web_design: 10 posts lifetime). Instagram, Facebook and LinkedIn metrics were not publicly accessible. The Standard plan (about 4 posts/week: 2 LinkedIn + 2 Instagram cross-posted to Facebook) is a realistic ramp-up; the Lite plan (2 posts/week) suits limited production capacity."),
 ("Times", "All times are Eastern Time (Milton, ON head office). Windows are based on Buffer's 2026 studies (LinkedIn weekdays 3–8 p.m.; Instagram Wed 12 p.m. / Thu 9 a.m.) and are starting hypotheses to refine with Apex's own analytics."),
 ("Verification legend", "Verified = source page read and claim confirmed (2026-11-06/07). Observed = seen on a public page. Unverified items are not used in post copy."),
]
for i, (a, b) in enumerate(rows, 4):
    ws.cell(row=i, column=1, value=a).font = Font(name=F, size=10, bold=True)
    c = ws.cell(row=i, column=2, value=b); c.font = Font(name=F, size=10); c.alignment = wrap
ws.column_dimensions["A"].width = 28; ws.column_dimensions["B"].width = 120

# --- Calendar
cal = wb.create_sheet("Calendar 2026-12")
extra = ["Reviewer Comments", "Post ID", "Day", "Plan Tier", "Series", "Readiness", "Client Input Needed", "Funnel Stage", "Persona", "Alternate Hooks", "First Comment (LinkedIn)", "Link / UTM", "Alt Text", "Story Companion", "Sources Used", "Asset Due (for review)"]
cols = HEADER + extra
widths = [16, 16, 18, 12, 30, 45, 34, 60, 28, 30, 16, 70, 40, 18, 28, 16] + [30, 8, 6, 16, 18, 22, 34, 14, 22, 34, 40, 40, 40, 36, 16, 14]
header(cal, 1, cols, widths)
for r, p in enumerate(POSTS, 2):
    vals = row16(p) + ["", p["id"], p["day"], p["tier"], p["series"], p["readiness"], p["client_input"] or "—", p["funnel"], p["persona"],
                       " | ".join(p["alt_hooks"]), p.get("first_comment") or "—", link_of(p) or "—", p["alt_text"], p["story"], ", ".join(p["sources"]), due(p["date"])]
    for c, v in enumerate(vals, 1):
        cell = cal.cell(row=r, column=c, value=v); cell.font = body; cell.alignment = wrap; cell.border = border
    cal.cell(row=r, column=3).fill = PatternFill("solid", fgColor=PILL_FILL[p["pillar"]])
    cal.cell(row=r, column=7).font = bold
    cal.cell(row=r, column=17).fill = PatternFill("solid", fgColor="FFFFE0")
    cal.row_dimensions[r].height = 260
last = len(POSTS) + 1
cal.freeze_panes = "C2"
cal.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{last}"
dv = DataValidation(type="list", formula1='"Pending Review,Changes Requested,Approved,Rejected"', allow_blank=False)
dv.error = "Choose a status from the list"; dv.prompt = "Set by a human reviewer only"
cal.add_data_validation(dv); dv.add(f"P2:P{last}")
for txt, colr in [("Approved", "C6EFCE"), ("Changes Requested", "FFEB9C"), ("Rejected", "FFC7CE"), ("Pending Review", "E7E6E6")]:
    cal.conditional_formatting.add(f"P2:P{last}", FormulaRule(formula=[f'$P2="{txt}"'], fill=PatternFill("solid", fgColor=colr)))
cal.conditional_formatting.add(f"V2:V{last}", FormulaRule(formula=['LEFT($V2,7)="Blocked"'], fill=PatternFill("solid", fgColor="FFC7CE")))

# --- Overview (formulas)
ov = wb.create_sheet("Overview", 1)
title_block(ov, "Plan Overview — December 2026", "Counts are live formulas over 'Calendar 2026-12'")
CR = f"'Calendar 2026-12'"
def table(start, title, labels, colref, target=None):
    ov.cell(row=start, column=1, value=title).font = Font(name=F, size=11, bold=True, color=RED)
    hdrs = ["Item", "Posts (all)", "Share"] + (["Strategy target"] if target else [])
    for i, h in enumerate(hdrs, 1):
        c = ov.cell(row=start + 1, column=i, value=h); c.font, c.fill, c.border = hdr_font, hdr_fill, border
    r0 = start + 2
    for k, lab in enumerate(labels):
        r = r0 + k
        ov.cell(row=r, column=1, value=lab).font = body
        ov.cell(row=r, column=2, value=f'=COUNTIF({CR}!${colref}$2:${colref}${last},"{lab}")').font = body
        c = ov.cell(row=r, column=3, value=f"=IF(SUM($B${r0}:$B${r0+len(labels)-1})=0,0,B{r}/SUM($B${r0}:$B${r0+len(labels)-1}))"); c.number_format = "0%"; c.font = body
        if target:
            t = ov.cell(row=r, column=4, value=target[k]); t.number_format = "0%"; t.font = Font(name=F, size=9, color="0000FF")
        for cc in range(1, len(hdrs) + 1): ov.cell(row=r, column=cc).border = border
    tr = r0 + len(labels)
    ov.cell(row=tr, column=1, value="Total").font = bold
    ov.cell(row=tr, column=2, value=f"=SUM(B{r0}:B{tr-1})").font = bold
    return tr + 2

nr = table(4, "Content pillars (all 18 rows incl. reserve)", list(PILL_FILL.keys()), "C", [0.40, 0.15, 0.20, 0.15, 0.10])
nr = table(nr, "Platforms", ["LinkedIn", "Instagram + Facebook (cross-post)"], "B")
nr = table(nr, "Plan tier", ["Core (Lite + Standard)", "Standard", "Reserve (optional)"], "T")
nr = table(nr, "Approval status (updates as reviewers work)", ["Pending Review", "Changes Requested", "Approved", "Rejected"], "P")
ov.cell(row=nr, column=1, value="Readiness").font = Font(name=F, size=11, bold=True, color=RED)
ov.cell(row=nr + 1, column=1, value="Ready for review (any)").font = body
ov.cell(row=nr + 1, column=2, value=f'=COUNTIF({CR}!$V$2:$V${last},"Ready*")').font = body
ov.cell(row=nr + 2, column=1, value="Blocked: client input").font = body
ov.cell(row=nr + 2, column=2, value=f'=COUNTIF({CR}!$V$2:$V${last},"Blocked*")').font = body
ov.cell(row=nr + 4, column=1, value="Strategy targets (blue) are inputs from the Organic Social Strategy document, section 5.").font = Font(name=F, size=8, italic=True, color=GREY)
ov.column_dimensions["A"].width = 40; ov.column_dimensions["B"].width = 12; ov.column_dimensions["C"].width = 10; ov.column_dimensions["D"].width = 16

# --- Creative Briefs sheet
cb = wb.create_sheet("Creative Briefs")
bcols = ["Brief ID", "Post ID", "Publish", "Platform", "Format", "Deliverable Specs", "Hook / Key Message", "Visual Direction", "Shot List / Slide Count", "Audio", "Alt Text", "Asset Due", "Reviewer", "Blocked Until"]
header(cb, 1, bcols, [14, 8, 16, 16, 16, 40, 34, 44, 40, 30, 40, 12, 18, 34])
for r, p in enumerate(POSTS, 2):
    shots = "; ".join(f"{t}: {v}" for t, v, *_ in p["script"]) if is_video(p) else (f"{len(p['slides'])} slides/pages" if is_slides(p) else "Single image")
    audio = "Licensed in-app track; burned-in captions" if is_video(p) else "N/A"
    vals = [p["cb"], p["id"], f"{p['date']} {p['time']} {TZ}", p["platform"], p["format"], SPEC[p["format"]], p["hook"], p["visual"], shots, audio, p["alt_text"], due(p["date"]), "Apex marketing (operator)", p["client_input"] or "—"]
    for c, v in enumerate(vals, 1):
        cell = cb.cell(row=r, column=c, value=v); cell.font = body; cell.alignment = wrap; cell.border = border
    cb.row_dimensions[r].height = 150
cb.freeze_panes = "B2"

# --- Sources
ss = wb.create_sheet("Sources")
header(ss, 1, ["ID", "Source", "URL", "Status", "Used in posts"], [8, 60, 70, 30, 24])
used = {}
for p in POSTS:
    for s in p["sources"]: used.setdefault(s, []).append(p["id"])
for r, (k, (t, u, s)) in enumerate(SRC.items(), 2):
    vals = [k, t, u, s, ", ".join(used.get(k, [])) or "Strategy / research"]
    for c, v in enumerate(vals, 1):
        cell = ss.cell(row=r, column=c, value=v); cell.font = body; cell.alignment = wrap; cell.border = border
    ss.cell(row=r, column=3).hyperlink = u; ss.cell(row=r, column=3).font = Font(name=F, size=9, color="0563C1", underline="single")
nr = len(SRC) + 3
ss.cell(row=nr, column=1, value="Removed / unverified (not used in any post):").font = bold
removed = ["68.01% zero-click searches (Search Engine Land; site blocked automated verification)",
           "Google AI 'calls businesses to check availability' (actual announcement: US only, select categories; rollout unconfirmed)",
           "Wix Harmony launch date (press release site blocked verification)",
           "'Unlabelled AI content is what consumers most want brands to stop posting' (not on the Sprout Social pages)",
           "BrightLocal '45% use AI for local recommendations' (figure not visible on page)",
           "All LA competitor follower counts from search snippets (never verified; wrong market)"]
for i, t in enumerate(removed, nr + 1):
    ss.cell(row=i, column=2, value=t).font = body

# --- Client inputs
ci = wb.create_sheet("Client Inputs Needed")
header(ci, 1, ["#", "Missing item", "Why it matters", "Affects", "Default applied"], [4, 50, 50, 22, 44])
INPUTS = [
 ("Instagram/Facebook/LinkedIn analytics (followers, reach, last 90 days)", "Sets KPI baselines; the profiles were behind login walls", "All KPIs", "KPIs expressed relative to the November baseline"),
 ("Confirm the official Instagram account (@apexwebstudios is linked from the website; @apex_web_design shows 471 followers / 10 posts and is not linked)", "Avoid posting to or reporting on the wrong account", "All Instagram posts", "@apexwebstudios"),
 ("Written permission to feature named reviews (Body Rituals Spa, UpkeepX, Copy Smart, Jamar Root)", "Consent and compliance", "P07, P15", "Posts held until confirmed"),
 ("Team members for camera (names, roles, signed consent)", "Behind-the-Build posts", "P02, P11, P12, P18", "Posts held until confirmed"),
 ("Holiday office hours Dec 24 – Jan 1", "Accurate customer information", "P16", "Placeholder in the caption"),
 ("Same-day price check (USD/CAD/GBP)", "Price posts quote the published prices", "P08, P13", "Prices as published on 2026-11-07"),
 ("January free-call availability", "CTA in P17", "P17", "Assumed available"),
 ("Production capacity (Lite 8 vs Standard 17 posts)", "Realistic cadence", "Whole plan", "Standard recommended"),
 ("Which self-reported stats are accurate (homepage '100% On-Time Delivery' vs '98%' on the web design page; '+1K Clients Globally' vs '45+ Clients Worldwide')", "Website consistency; these stats are excluded from content until resolved", "Future proof posts", "No self-reported stats used"),
 ("Direct competitors Apex actually loses deals to", "The v1 competitor list was unsupported and has been removed", "Research / strategy", "Category substitutes analysed instead"),
]
for r, row in enumerate(INPUTS, 2):
    for c, v in enumerate((r - 1,) + row, 1):
        cell = ci.cell(row=r, column=c, value=v); cell.font = body; cell.alignment = wrap; cell.border = border

for s in wb.worksheets:
    s.sheet_view.showGridLines = s.title not in ("Read Me", "Overview")
xlsx_path = os.path.join(DELIV, f"{SLUG}_content-calendar_{MONTH}_final.xlsx")
wb.save(xlsx_path)

# ------------------------------------------------------------------ DOCX specs
def H1(t): return {"t": "h1", "text": t}
def H2(t): return {"t": "h2", "text": t}
def H3(t): return {"t": "h3", "text": t}
def P(t): return {"t": "p", "text": t}
def UL(items): return {"t": "ul", "items": items}
def OL(items): return {"t": "ol", "items": items}
def TB(headers, rows, widths=None): return {"t": "table", "headers": headers, "rows": rows, "widths": widths}
def NOTE(label, text, tone="info"): return {"t": "callout", "label": label, "text": text, "tone": tone}
def CODE(text): return {"t": "code", "text": text}
def BR(): return {"t": "pagebreak"}

def cover(title, subtitle):
    return {"title": title, "subtitle": subtitle, "client": "Apex Web Studios", "period": "December 2026",
            "version": f"Version 2 · Final for client review · {TODAY}",
            "status": "Status: PENDING REVIEW. Nothing in this document has been scheduled or published."}

VERIFY_LEGEND = NOTE("How to read the labels", "VERIFIED = we opened and read the source page (or the client's own website) and confirmed the claim on 6–7 Nov 2026. OBSERVED = seen directly on a public page. ASSUMPTION = our working assumption, to be confirmed by Apex. UNVERIFIED = could not be confirmed; never used in post copy.")

def sources_section(ids):
    return [H2("Sources"), UL([f"{SRC[i][0]}: {SRC[i][1]} ({SRC[i][2]})" for i in ids])]

def cal_summary_table(posts):
    return TB(["#", "Date (ET)", "Platform", "Format", "Pillar", "Topic", "Tier", "Readiness"],
              [[p["id"], f"{p['day']} {p['date'][5:]} {p['time']}", "LinkedIn" if not ig(p) else "IG + FB", p["format"], p["pillar"].split(" (")[0], p["topic"], p["tier"].split(" (")[0], p["readiness"]] for p in posts],
              [500, 1100, 750, 1100, 1100, 2700, 800, 1300])

# ===== 1. STRATEGY
S = []
S += [H1("1. Executive summary"),
      P("Apex Web Studios is a full-service software development and marketing studio. Its head office is in Milton, Ontario, with offices in Los Angeles and Birmingham (UK). It publishes transparent package pricing from $599 and offers 13 services, from websites and mobile apps to AI agents, SEO and social media marketing (VERIFIED, apexwebstudios.net)."),
      P("Its own social channels are under-used. The X account has 57 posts since January 2023, and its newest post is dated 30 July 2026. The only Instagram account with public metadata (@apex_web_design, which is not linked from the website) shows 10 posts and 471 followers (OBSERVED, 7 Nov 2026). Instagram, Facebook and LinkedIn metrics for the accounts linked from the website were behind login walls."),
      P("This strategy positions Apex on social as the plain-English build-and-grow partner for small businesses and founders. The approach is to teach owners how to get more from their website, show the real team and process, and be openly transparent about price. Every post maps to a pillar, a funnel stage and a KPI. Every external statistic is verified and linked."),
      UL(["**Primary goal (ASSUMPTION — confirm):** generate qualified free-call bookings and inquiries from organic social.",
          "**Platforms:** LinkedIn (authority and B2B) plus Instagram, cross-posted to Facebook (reach and trust with SMB owners). X is paused until activity resumes (inactive since July 2026).",
          "**Realistic cadence:** about 4 posts per week in December (Standard plan, 17 posts), or 2 per week (Lite plan, 8 posts) if production capacity is limited. This is a ramp-up from near-dormant activity, not a volume target.",
          "**December anchors:** post-Cyber Monday website checks, the International Day of Persons with Disabilities (Dec 3), AI search, transparent pricing, client proof, the holidays and 2027 planning.",
          "**Guardrails:** no publishing without written approval, no unverified statistics, no self-reported website stats until Apex confirms which are correct."]),
      VERIFY_LEGEND,
      H1("2. Business snapshot (verified)"),
      TB(["Item", "Verified fact", "Source"], [
          ["Positioning line", "“Apex Web Studios is Canada's trusted software development and marketing agency.”", "B01"],
          ["Core promise", "“No surprises. No radio silence. No hidden costs.” and “No Confusing Proposals / No Lengthy Contracts / No Hidden Cost”", "B02, B01"],
          ["Offices", "Milton ON (head office) · Los Angeles CA · Birmingham UK", "B01"],
          ["Services (13)", "Mobile Apps · Website Design & Development · SaaS · UI/UX · AI Agents · Digital Marketing · White Label · Branding · Web Apps · Custom Software · E-commerce Automation · MVP · Videos & Animation", "B01"],
          ["Web packages (USD, one-time)", "Starter $599 · Growth $1,199 · Professional Business $1,999 · Corporate Elite $3,199 · E-commerce Growth $4,999 · Platinum Enterprise $7,999", "B04"],
          ["Speed promise", "First design concepts within 48 hours: Starter, Growth and Professional Business only", "B04"],
          ["Project management", "Dedicated project manager on Starter through E-commerce Growth; Platinum lists a dedicated team", "B04"],
          ["Process", "Product Discovery → Experience Design → Engineering & Development → Testing & Optimization → Release & Maintenance", "B03"],
          ["Accessibility capability", "“WCAG Compliance & Accessibility Standards” (UI/UX service)", "B03"],
          ["Social media services sold", "Bronze $449/mo (3 posts/week) · Silver $749/mo (5 posts/week) · Gold $1,199/mo (5 posts/week), each bundled with ad campaigns", "B04"],
          ["Review claims (on Apex's own site)", "Trustpilot 4.7 (200 reviews) · Google 4.7 (55) · Clutch 4.9 (25). Not confirmed on the platforms themselves, which block automated access.", "B08"],
          ["Primary CTA", "“Book a Free Call”", "B01"],
      ], [2000, 5800, 1200]),
      H2("Website issues to fix before social sends traffic there (OBSERVED)"),
      UL(["Conflicting self-reported stats: “100% On-Time Delivery” (homepage) vs “98% On Time Delivery” (web design page); “+1K Clients Globally” vs “45+ Clients Worldwide”. These are excluded from all content until Apex confirms the correct figures.",
          "Country positioning conflict: “Canada's trusted…” (homepage) vs “…in the USA” (footer).",
          "There is no portfolio or case-study page (/portfolio redirects to the homepage), so proof content relies on verbatim reviews for now.",
          "The blog's newest post is from 4 Nov 2025.",
          "The Gold social package sells TikTok and YouTube management, but Apex has no TikTok or YouTube presence of its own."]),
      H1("3. Objectives & KPIs"),
      P("No analytics baseline was supplied and the profiles were not publicly measurable. KPIs are therefore set relative to Apex's own November 2026 baseline, captured on 1 December. Industry benchmarks are shown only for context, because their methods differ and they are not targets."),
      TB(["Platform", "Role", "Primary KPIs", "December target", "Context benchmark (verified)"], [
          ["LinkedIn", "Authority with founders and marketing leads; B2B leads", "Engagement rate per impression; comments; link clicks (first comment); follows", "Engagement rate at or above the November average +10%; 30+ link clicks across the month", "Socialinsider: native documents 6.40% engagement by impressions (Q3 2026); overall average 5.20% in 2025 (T23)"],
          ["Instagram (+ Facebook)", "Reach and trust with SMB owners", "Non-follower reach; saves; shares; profile visits; DMs", "Saves at 2–3% or more of reach on carousels and educational Reels; 5+ DMs/inquiries", "Emplifi: Instagram engagement rate per impression 1.52% worldwide, Q3 2026 (T28)"],
          ["All", "Leads", "Free-call bookings with source = social (UTM + form field)", "Establish the baseline; aim for 3+ attributed bookings", "—"],
      ], [1300, 1700, 2100, 2000, 1900]),
      NOTE("Tracking setup (do before Dec 1)", "Every link carries UTM tags (utm_source = linkedin / instagram / facebook, utm_medium = organic_social, utm_campaign = 2026-12_<post>). Add a “How did you hear about us?” field to the free-call form.", "action"),
      H1("4. Audience personas"),
      P("Personas are ASSUMPTIONS built from Apex's own services, package names, industries served and public reviews. No CRM or demographic data was supplied, so no demographics are stated."),
      TB(["Persona", "Evidence it exists (verified)", "What they need", "Main objection", "Content that moves them", "Platform"], [
          ["P1 Local Service Owner (1–20 staff)", "Starter/Growth packages; testimonials from a spa, a jewellery business and a historical society (B04, B08)", "A credible site that brings calls and bookings; being found", "“Agencies are expensive / go quiet”", "Checklists, quick fixes, transparent pricing, reviews", "Instagram, Facebook"],
          ["P2 Startup Founder", "MVP, SaaS, App and AI Agent services; “startups” in the site description (B01, B03)", "Speed, a trustworthy technical partner, cost clarity", "“Can a broad studio go deep?”", "Process, team, honest comparisons", "LinkedIn"],
          ["P3 Growing SMB Marketing Lead", "SEO/PPC/SMM retainers; review: “our current services with them are SEO, PPC Social media marketing” (B08)", "Pipeline growth; one accountable partner", "Reach is falling; AI search confusion", "AI-search explainers, data-backed posts", "LinkedIn, Instagram"],
          ["P4 Agency Partner", "White Label Services page (B03)", "Reliable, discreet delivery", "Quality and confidentiality", "Process and PM posts (secondary in December)", "LinkedIn"],
      ], [1300, 2000, 1500, 1300, 1700, 1200]),
      H1("5. Positioning, messaging & content pillars"),
      P("**Core message:** Build it right. Grow it after. One team for both. (Derived from Apex's own line “First We Write The Code – Then We Write The Growth Story”, B01.)"),
      TB(["Message", "Proof point (verified)", "Never say"], [
          ["Transparent, no-surprise pricing", "Six published web packages, $599–$7,999 (B04)", "“Cheapest”, “guaranteed results”"],
          ["Build and growth in one place", "13 services incl. SEO, PPC, social, branding (B01)", "Unconfirmed client counts or percentages"],
          ["People you can reach", "Dedicated PM on most packages (B04); reviews praising communication (B08)", "“24/7” or response-time promises not confirmed by Apex"],
          ["Ready for AI search and accessibility", "AI Agent and SEO services; WCAG design standards (B03)", "Legal advice; promised AI citations or rankings"],
      ], [2600, 3600, 2800]),
      TB(["Pillar", "Purpose", "Target mix", "December (Standard plan)", "Funnel stage"], [
          ["Build Smarter (Educate)", "Teach owners and founders how to get more from their website", "40%", f"{pill['Build Smarter (Educate)']} posts", "Awareness → Consideration"],
          ["Proof & Results", "Let clients speak, word for word", "15%", f"{pill['Proof & Results']} posts", "Consideration"],
          ["Behind the Build", "Show the real team and process; counter the agency-silence fear", "20%", f"{pill['Behind the Build']} posts", "Consideration / Loyalty"],
          ["Offers & Packages", "Turn interest into free calls with transparent pricing", "15%", f"{pill['Offers & Packages']} posts", "Conversion"],
          ["Community & Moments", "Inclusive seasonal goodwill and practical information", "10%", f"{pill['Community & Moments']} posts", "Loyalty"],
      ], [2000, 3000, 1000, 1700, 1300]),
      H2("Signature content series"),
      TB(["Series", "Format", "Promise to the audience", "December posts"], [
          ["60-Second Site Check", "Instagram Reels and carousels", "One fix you can do today, no jargon", "P03, P09, P14"],
          ["Plain-English Web / Plain-English AI", "LinkedIn PDF documents and text posts", "What's changing (AI search, accessibility, AI builders), explained with sourced data", "P01, P04, P06, P10"],
          ["Price Tag, Explained", "LinkedIn document, Instagram carousel and Reel", "Exactly what each package includes, and when not to buy", "P08, P13, P17"],
          ["Inside Apex", "Reels and LinkedIn video", "The real people and process behind every build", "P02, P11, P12, (P18)"],
          ["In Their Words", "Carousel and quote card", "Verbatim client reviews, never edited", "P07, P15"],
      ], [2200, 2000, 3200, 1600]),
      H1("6. Platform strategy & realistic posting frequency"),
      H2("What we observed"),
      UL(["No posting frequency was provided by Apex.",
          "X (@ApexWebStudios): 57 posts since joining in January 2023; newest visible post 30 July 2026; 10 followers (OBSERVED, B16).",
          "Instagram @apex_web_design: 10 posts lifetime, 471 followers; not linked from apexwebstudios.net, so ownership is unconfirmed (OBSERVED, B17).",
          "Instagram @apexwebstudios, Facebook and LinkedIn: not publicly measurable (login or bot walls).",
          "For reference, Apex's entry-level social package for its own clients specifies 3 posts per week (B04)."]),
      H2("Recommended cadence"),
      TB(["Plan", "LinkedIn", "Instagram → Facebook", "Total December", "When to choose it"], [
          ["Lite", "4 posts (Dec 1–10)", "4 posts (Dec 3–30)", f"{len(LITE)} posts", "Limited production capacity; every post needs no client input except a same-day price check"],
          ["Standard (recommended)", "about 2/week", "about 2–3/week", f"{len(STD)} posts", "Realistic ramp-up from a dormant baseline; about 4 posts/week, lighter in the holiday week"],
          ["Reserve", "+1", "—", "+1 post", "Only if team inputs arrive by Dec 22"],
      ], [1500, 1600, 1700, 1300, 2900]),
      P("Context: Buffer's analysis of 2M posts suggests 2–5 LinkedIn posts per week (T24; published Aug 2025, so more than 12 months old and treated as directional only). Volume is deliberately below that range's upper end. Consistency matters more than volume when restarting dormant channels."),
      H2("Posting windows (starting hypotheses, Eastern Time)"),
      UL(["LinkedIn: weekdays at 16:00. Buffer (4.8M posts) found engagement is “generally between 3 p.m. and 8 p.m. on weekdays” (T25).",
          "Instagram: Wednesday 12:00 and Thursday 09:00 as primary slots. Buffer (9.6M posts) names “Thursday at 9 a.m., Wednesday at 12 p.m., and Wednesday at 6 p.m.” (T26). Friday and Tuesday noon slots are tests.",
          "Facebook: automatic cross-post from Instagram at the same time.",
          "Review after four weeks using Apex's own analytics; the windows are hypotheses, not rules."]),
      H2("Platform rules we follow (verified)"),
      UL(["**Originality:** Instagram removes recommendation eligibility for accounts that mostly repost others' content (T03), and prioritises original content (T04). All visuals use Apex's own team, screens or demo sites.",
          "**Trial Reels** can be scheduled and are shown to non-followers first (T05). Use them to test alternate hooks on educational Reels.",
          "**No engagement bait on LinkedIn:** LinkedIn's updated ranking filters out prompts like “Comment ‘Yes’ if you agree” (T09). Our CTAs ask genuine questions or point to the first-comment link.",
          "**LinkedIn video:** “Space out similar topics so each video has room to land” (T12).",
          "**Hashtags:** Instagram is limiting posts to five hashtags (T61). Maximum 5 on Instagram, 3 on LinkedIn, all in CamelCase for screen readers.",
          "**Human-made first:** Sprout Social reports consumers say brands should make human-generated content their #1 priority (T29), and that audiences want clear disclosure when AI is involved (T30). Disclose any AI-generated visuals."]),
      H1("7. Funnel, CTAs & link system"),
      TB(["Stage", "Content", "CTA style", "Destination"], [
          ["Awareness", "60-Second Site Check, Plain-English Web/AI", "Save this · Comment your answer", "Profile / first comment"],
          ["Consideration", "Inside Apex, In Their Words, AI builder vs agency", "Ask the team · Read more reviews", "/testimonials, DMs"],
          ["Conversion", "Price Tag, Explained; rehire your website", "Book a free call", "/contact-us, /pricing (UTM-tagged)"],
          ["Loyalty", "Moments, team reflections", "None or a soft CTA", "—"],
      ], [1500, 3000, 2300, 2200]),
      H1("8. Community management playbook"),
      UL(["Reply to every comment and DM within one business day (Apex's own promise: “No radio silence”).",
          "Educational posts: answer the question publicly, then offer a DM for specifics.",
          "Price objections: acknowledge them, link to the published pricing, and offer a free call. Never argue or discount in public.",
          "Negative or service complaints: thank the person, take it to DM within the day, log it, and never delete legitimate criticism.",
          "Accessibility or legal questions: share general guidance only, with “speak to a qualified professional” for compliance specifics.",
          "Mistaken identity (other businesses named “Apex Web Studios” exist): politely confirm Apex's website and offices.",
          "Escalate to the operator for anything involving a current client project, refunds or legal matters."]),
      H2("Reply starters"),
      TB(["Situation", "Suggested reply"], [
          ["Question on an educational post", "Great question, [name]. Short answer: [answer]. Happy to look at your specific site if you send us a DM."],
          ["“Too expensive”", "Totally fair. Our full price list is public at apexwebstudios.net/pricing, and sometimes the right answer is a smaller package or a DIY builder. Happy to talk it through on a free call, with no obligation."],
          ["Complaint", "Thanks for flagging this, [name]. We want to make it right. We've sent you a DM so we can look into it today."],
      ], [2500, 6500]),
      H1("9. Hashtags & social SEO"),
      TB(["Tier", "Instagram (max 5)", "LinkedIn (3)"], [
          ["Branded", "#ApexWebStudios (always)", "#ApexWebStudios (always)"],
          ["Niche", "#WebDesign #WebAccessibility #SmallBusinessWebsite #LocalSEO #SocialSEO", "#WebDevelopment #WebAccessibility #AISearch"],
          ["Community", "#SmallBusinessTips #SmallBusinessOwner #NewBusiness", "#SmallBusiness"],
      ], [1800, 4200, 3000]),
      P("Social search: Hootsuite reports that Google has started indexing public Instagram content and that social content must adapt to multi-modal discovery (T31). Every caption opens with a clear, keyword-led line. On-screen text repeats the topic, and every image has alt text."),
      H1("10. Measurement & test-and-learn"),
      UL(["Weekly (Fridays): reach, engagement, saves, shares, link clicks and DMs per post; a log of comments and replies.",
          "Monthly report (first week of January): pillar and series performance, best hooks, attributed leads, recommendations for February.",
          "Test 1: on LinkedIn, PDF documents vs text and image posts on engagement rate (Buffer reports PDF carousels have the highest median engagement, 21.77%, T21).",
          "Test 2: Instagram Trial Reels using the primary vs the alternate hook on P03 and P09; publish the winner to the main grid.",
          "Test 3: 'Price Tag, Explained' posts vs other CTAs on DMs and free-call clicks."]),
      H1("11. 90-day roadmap"),
      TB(["Month", "Focus", "Key actions"], [
          ["December 2026", "Restart and prove consistency", "Standard plan (17 posts); tracking set up; confirm the official accounts; collect consents"],
          ["January 2027", "Proof and conversion", "Publish 1–2 case studies (with client permission); repeat the best series; new-year free-call push; review the cadence with real data"],
          ["February 2027", "Scale what works", "Add a third weekly Instagram post if capacity allows; consider a Shorts series (YouTube now supports Shorts seasons/episodes, T18) to back the Gold package's YouTube offer"],
      ], [1600, 2400, 5000]),
      H1("12. Risks & guardrails"),
      UL(["Nothing is published or scheduled without written approval (the Approval Status column in the calendar).",
          "Statistics in copy come only from verified sources, attributed in the caption or first comment.",
          "Inconsistent website stats are excluded until fixed.",
          "Reviews are used verbatim and only with permission.",
          "Accessibility posts are clearly labelled “general information, not legal advice”.",
          "Licensed audio only; no third-party designs or client work without written permission."]),
      H1("13. Information still needed from Apex"),
      TB(["Missing item", "Affects", "Default until supplied"], [[a, c, d] for a, b, c, d in INPUTS], [4600, 1800, 2600]),
     ]
S += sources_section(["B01", "B02", "B03", "B04", "B08", "B16", "B17", "T03", "T04", "T05", "T09", "T12", "T18", "T21", "T23", "T24", "T25", "T26", "T28", "T29", "T30", "T31", "T61"])
json.dump({"cover": cover("Organic Social Media Strategy", "Strategy, positioning, cadence and measurement plan"), "blocks": S},
          open(os.path.join(SPECS, "strategy.json"), "w"), ensure_ascii=False)

# ===== 3. CAPTIONS
C = [H1("About this document"),
     P(f"This document holds the full publish-ready copy for all {len(POSTS)} December posts ({len(STD)} Standard plan + 1 Reserve): primary hook, two alternate hooks, the complete caption, CTA, LinkedIn first comment, hashtags, link, alt text and an Instagram Story companion. Every statistic is attributed to a verified source. Text in [square brackets] needs Apex's input before approval."),
     VERIFY_LEGEND,
     H2("Plan at a glance"), cal_summary_table(POSTS), BR()]
for p in POSTS:
    C += [H1(f"{p['id']} · {p['day']} {p['date']} · {p['time']} ET · {p['platform']}"),
          TB(["Field", "Detail"], [["Format / series", f"{p['format']} · {p['series']}"], ["Pillar / objective / funnel", f"{p['pillar']} · {p['objective']} · {p['funnel']}"],
                                   ["Topic", p["topic"]], ["Plan tier", p["tier"]], ["Readiness", p["readiness"]], ["Creative brief", p["cb"]], ["KPI", p["kpi"]]], [2200, 6800])]
    if p["client_input"]:
        C.append(NOTE("Client input needed", p["client_input"], "warn"))
    C += [H3("Hooks"), UL([f"**Primary:** {p['hook']}"] + [f"Alternate {i}: {h}" for i, h in enumerate(p["alt_hooks"], 1)]),
          H3("Caption (copy exactly)"), CODE(p["caption"]),
          H3("CTA"), P(p["cta"])]
    if p.get("first_comment"):
        C += [H3("First comment (post immediately after publishing)"), P(p["first_comment"])]
    if link_of(p):
        C += [H3("Link (link in bio / sticker)"), P(link_of(p))]
    C += [H3("Hashtags"), P(p["hashtags"]), H3("Alt text"), P(p["alt_text"])]
    if p["story"] and not p["story"].startswith("n/a"):
        C += [H3("Story companion"), P(p["story"])]
    C += [H3("Why this post (research rationale)"), P(p["rationale"]),
          P("Sources: " + "; ".join(f"{s} {SRC[s][1]}" for s in p["sources"] if s in SRC)), BR()]
json.dump({"cover": cover("Captions, Hooks, CTAs & Hashtags", f"Publish-ready copy for all {len(POSTS)} December 2026 posts"), "blocks": C},
          open(os.path.join(SPECS, "captions.json"), "w"), ensure_ascii=False)

# ===== 4. SCRIPTS & CAROUSELS
R = [H1("About this document"),
     P("This document contains the scene-by-scene scripts for every Reel and video, and the slide-by-slide or page-by-page copy for every carousel and LinkedIn document. On-screen text is final copy; voiceover is written to be read naturally, about 2.5 words per second. All video carries burned-in captions."),
     TB(["Post", "Date", "Format", "Length / slides", "Topic"],
        [[p["id"], p["date"], p["format"], (p["script"][-1][0].split("–")[-1] if is_video(p) else (f"{len(p['slides'])} slides" if is_slides(p) else "1 image")), p["topic"]] for p in POSTS], [700, 1100, 1700, 1300, 4200]),
     BR()]
for p in POSTS:
    R += [H1(f"{p['id']} · {p['date']} · {p['platform']} · {p['format']}"), P(f"**Topic:** {p['topic']}  ·  **Hook:** {p['hook']}  ·  **Brief:** {p['cb']}")]
    if p["client_input"]:
        R.append(NOTE("Client input needed", p["client_input"], "warn"))
    if is_video(p):
        R += [H3("Scene-by-scene script"), TB(["Time", "Shot / visual", "On-screen text", "Voiceover / dialogue", "Audio"], [list(s) for s in p["script"]], [800, 2300, 2000, 2700, 1200])]
        if p.get("end_note"): R.append(P(p["end_note"]))
        R += [P("**Captions/subtitles:** burned-in captions for all speech, plus auto-captions enabled on the platform. **Cover frame:** the hook as large text over the first frame, kept 4:5 grid-safe.")]
    elif is_slides(p):
        R += [H3("Slide / page copy"), TB(["#", "Slide", "Headline", "Supporting copy"], [[str(i), lab, h, b] for i, (lab, h, b) in enumerate(p["slides"], 1)], [500, 1500, 3300, 3700])]
    else:
        R += [H3("Copy on image"), UL(p.get("copy_on_image", []))]
    R += [P(f"**Visual direction:** {p['visual']}"), P(f"**Alt text:** {p['alt_text']}"), BR()]
json.dump({"cover": cover("Reel Scripts & Carousel Content", "Scene-by-scene scripts and slide-by-slide copy"), "blocks": R},
          open(os.path.join(SPECS, "scripts.json"), "w"), ensure_ascii=False)

# ===== 5. CREATIVE BRIEFS
CBD = [H1("Brand system for all December assets"),
       TB(["Element", "Specification (from apexwebstudios.net)"], [
           ["Colours", "Near-black #0A0A0A / #1A1A1A · dark grey #383838 · light grey #F0F0F0 · white #FFFFFF · accent red #D23030 (logo red #FF0000) · purple #811EA1 as a rare accent only"],
           ["Typefaces", "Urbanist (headlines) · Inter / Inter Display (body) · IBM Plex Mono (numbers, labels, step counters)"],
           ["Logo", "Use the light version on dark backgrounds, the dark version on light ones. Download from apexwebstudios.net/images/app-logo.svg and app-logo-light.svg."],
           ["Look and feel", "Dark, confident, technical-but-human. One accent colour per frame. Real people and real screens."],
           ["Canva", "No Apex brand kit has been supplied. Build a Canva brand kit from this table before production."]], [1800, 7200]),
       H2("Do"), UL(BRAND_DO), H2("Don't"), UL(BRAND_DONT),
       H2("Accessibility requirements (every asset)"),
       UL(["Burned-in captions on all video with speech; supply an SRT file for LinkedIn video.", "High text contrast and large type (body text 24 px or more on 1080 px canvases).", "Never convey meaning by colour alone.", "No flashing or strobing effects.", "Alt text is supplied per post (below) and goes into the platform's alt-text field."]),
       H2("Production schedule"),
       P("Final assets are due for review 3 business days before each publish date. Reviewer: Apex marketing (operator). Posts marked 'Blocked' must not be produced until the listed input is supplied."),
       TB(["Brief", "Post", "Publish", "Format", "Asset due", "Status"], [[p["cb"], p["id"], f"{p['date']} {p['time']}", p["format"], due(p["date"]), p["readiness"]] for p in POSTS], [1500, 700, 1500, 2000, 1300, 2000]),
       BR()]
for p in POSTS:
    CBD += [H1(f"{p['cb']} · {p['topic']}"),
            TB(["Field", "Detail"], [
                ["Post", f"{p['id']} · {p['day']} {p['date']} {p['time']} ET · {p['platform']}"],
                ["Format", p["format"]],
                ["Deliverable specs", SPEC[p["format"]]],
                ["Objective / KPI", f"{p['objective']} · {p['kpi']}"],
                ["Key message / hook", p["hook"]],
                ["Audience", p["persona"]],
                ["Asset due", f"{due(p['date'])} · reviewer: Apex marketing (operator)"],
                ["Status", p["readiness"] + (f". Blocked until: {p['client_input']}" if p["client_input"] else "")],
            ], [2200, 6800]),
            H3("Visual direction"), P(p["visual"])]
    if is_video(p):
        CBD += [H3("Shot list and on-screen text"), TB(["Time", "Shot / visual", "On-screen text", "Audio"], [[t, v, o, a] for t, v, o, vo, a in p["script"]], [900, 3600, 3000, 1500]),
                H3("Talent, props, location"), UL(["Talent: Apex team volunteers with signed on-camera consent (never clients without permission).", "Location: Apex office or a tidy home-office setting with good natural light.", "Screens: Apex's own site or purpose-made demo pages; blur any real client data."]),
                H3("Audio"), P("Licensed track from Instagram's or LinkedIn's in-app library (or a licensed stock track), kept low under the voiceover. Use a lapel or shotgun mic for speech.")]
    elif is_slides(p):
        CBD += [H3(f"Slide copy ({len(p['slides'])} frames)"), TB(["#", "Headline", "Supporting copy"], [[str(i), h, b] for i, (lab, h, b) in enumerate(p["slides"], 1)], [500, 3800, 4700])]
    else:
        CBD += [H3("Copy on image"), UL(p.get("copy_on_image", []))]
    CBD += [H3("Alt text (paste into the platform)"), P(p["alt_text"]), BR()]
json.dump({"cover": cover("Creative Briefs", "Designer and video-editor briefs CB-2026-12-01 to CB-2026-12-18"), "blocks": CBD},
          open(os.path.join(SPECS, "briefs.json"), "w"), ensure_ascii=False)

# ===== 6. RESEARCH REPORT
TRENDS = [
 ("Accessibility: International Day of Persons with Disabilities, Dec 3", "All", "Observed on 3 Dec 2026, theme “The CRPD at 20: Building on Progress, Advancing the Future”", "T56", "Apex offers WCAG-standard design (B03); the best-fit date of the month", "Used: P03, P04"),
 ("Website accessibility lawsuits rising (US)", "All", "“Plaintiffs filed 3,117 website accessibility lawsuits in federal court in 2025 – a 27% increase from 2024.” H1 2026: 5,006 Title III suits of all types (+9%)", "T46, T45", "A business reason for SMBs to act; educational framing only", "Used: P04"),
 ("AI Overviews and clicks: a mixed picture", "Search", "Ahrefs: an AI Overview “correlates with a 58% lower average clickthrough rate for the top-ranking page” (Dec 2025 data). Seer: AIO CTR “rebound 85% in the first two months of 2026”", "T34, T37", "Apex sells SEO and AI; a balanced view builds credibility", "Used: P06"),
 ("Google agentic search features", "Search", "Google can call businesses for users “for select categories like home repair, beauty or pet care”, rolling out “to everyone in the U.S.”", "T38", "Relevant to US local clients only; rollout unconfirmed", "Not used in December copy (scope too narrow)"),
 ("Social is search", "Instagram / all", "“Google has started indexing public Instagram content”; “Social has become a search engine, not just a feed.”", "T31, T32", "Apex sells SEO and social; teach owners to write findable posts", "Used: P09; strategy"),
 ("Holiday e-commerce peak", "All", "Adobe forecast $15.1B on Cyber Monday and $275.1B for the US season (Nov 1–Dec 31); NRF forecasts 4.2% holiday sales growth", "T53, T54", "Website readiness during the peak", "Used: P01"),
 ("AI website builders are mainstream", "Category", "Squarespace's “Blueprint AI website builder guides you through a few simple choices…”", "T50", "The main substitute for Starter-tier buyers", "Used: P10"),
 ("Instagram originality enforcement", "Instagram", "Accounts that regularly repost others' content “will no longer be eligible for recommendations”", "T03, T04", "Use only Apex's own footage and work", "Strategy rule"),
 ("Trial Reels scheduling", "Instagram", "Creators can schedule Trial Reels shown to non-followers first", "T05", "Test hooks with prospects", "Strategy test plan"),
 ("LinkedIn filters engagement bait", "LinkedIn", "Ranking updated to “filter out engagement bait” such as “Comment ‘Yes’ if you agree”", "T09", "Genuine-question CTAs only", "Strategy rule"),
 ("LinkedIn PDF documents perform strongly", "LinkedIn", "Buffer: PDF carousels “median engagement rate of 21.77%” vs video 7.35%. Socialinsider: documents 6.40% (Q3 2026)", "T21, T23", "Document-heavy LinkedIn mix", "P01, P04, P08, P10, P18"),
 ("Instagram 5-hashtag limit", "Instagram", "“Instagram will gradually update the number of hashtags… to five.”", "T61", "Maximum 5 hashtags", "All Instagram posts"),
 ("Human-made content preferred", "All", "“Consumers say brands should make human-generated content their #1 priority.” Audiences want “clear disclosure when AI is involved”", "T29, T30", "Real team on camera; disclose any AI visuals", "Strategy; P11, P18"),
 ("Shorts series on YouTube", "YouTube", "Shorts can be structured “into seasons and episodes… custom thumbnails and sequential playback”", "T18", "Future “Website Rescue” series; supports the Gold package's YouTube offer", "2027 roadmap"),
 ("Threads at 500M monthly users", "Threads", "“Threads has reached 500 million monthly active users”", "T14", "Low-cost test channel for 2027", "Not in December scope"),
]
RS = [H1("1. Executive summary"),
      P("This report covers the research behind Apex Web Studios' December 2026 organic social plan. It records the client's verified brand facts and an audit of its public social presence. It reviews the competitor set, removing unsupported entries. It lists the current trends and dates used in the content, each with a live source link and a verification status."),
      UL(["**Client facts:** the full website was read (34 pages, 6 Nov 2026), and the facts used in content were re-checked on 7 Nov 2026. All prices, package inclusions and reviews used in posts are VERIFIED verbatim.",
          "**Sources:** the external sources cited in the content were opened and read on 7 Nov 2026. Claims that could not be confirmed were removed from all copy (see section 6).",
          "**Competitors:** the first-draft list of five Los Angeles web-design shops came only from search snippets and assumed the wrong market. It has been removed as unsupported. Verified competitive pressure comes from AI website builders. Apex should name the agencies it actually loses deals to.",
          "**Social presence:** low visible activity (X dormant since 30 July 2026; Instagram @apex_web_design 10 posts). This supports a realistic ramp-up cadence rather than a high-volume calendar."]),
      VERIFY_LEGEND,
      H1("2. Methodology"),
      TB(["Step", "What we did", "Date"], [
          ["Client website", "Read all 34 sitemap URLs, the Terms and Privacy pages, CSS and logo files, and the pricing data", "2026-11-06"],
          ["Re-check", "Re-read the pricing, testimonials, UI/UX, homepage and web design pages for every fact used in content", "2026-11-07"],
          ["External sources", "Opened and read each cited article or report; recorded the publish date and a verbatim quote", "2026-11-07"],
          ["Social profiles", "One ordinary public page load per profile; no login, no workarounds", "2026-11-07"],
          ["Exclusions", "Anything only seen in search snippets, behind bot protection or not on the page is labelled UNVERIFIED and kept out of copy", "—"],
      ], [1800, 5700, 1500]),
      H1("3. Client brand findings (verified)"),
      TB(["Area", "Finding", "Label", "Source"], [
          ["Identity", "“Canada's trusted software development and marketing agency”; offices in Milton ON (head office), Los Angeles and Birmingham UK", "VERIFIED", "B01"],
          ["Offer", "13 services; six published web packages $599–$7,999; SEO, social and branding packages also priced publicly", "VERIFIED", "B01, B04"],
          ["Promise", "“No surprises. No radio silence. No hidden costs.”", "VERIFIED", "B02"],
          ["Process", "Discovery → Experience Design → Engineering & Development → Testing & Optimization → Release & Maintenance", "VERIFIED", "B03"],
          ["Accessibility", "“WCAG Compliance & Accessibility Standards” listed under UI/UX", "VERIFIED", "B03"],
          ["Tone", "Confident, punchy, contrast lines (“We Don't Just Build Digital Products – We Build Growth Engines”)", "OBSERVED", "B01"],
          ["Visual identity", "Dark theme; red accent #D23030; Inter / Urbanist / IBM Plex Mono", "OBSERVED (site code)", "B01"],
          ["Reviews", "Site claims Trustpilot 4.7 (200), Google 4.7 (55), Clutch 4.9 (25); themes are communication, flexibility, delivery; a price objection appears", "VERIFIED as on-site claims; platform pages UNVERIFIED (bot-blocked)", "B08"],
          ["Content assets", "Blog: 13 posts, newest 4 Nov 2025; no portfolio or case studies", "VERIFIED", "B09"],
          ["Inconsistencies", "100% vs 98% on-time delivery; +1K vs 45+ clients; Canada vs USA framing", "VERIFIED (conflict)", "B01, B03"],
      ], [1400, 4300, 1800, 1500]),
      H1("4. Social presence audit"),
      TB(["Channel", "URL", "What we could see", "Label"], [
          ["Instagram (linked from site)", "instagram.com/apexwebstudios", "Login wall; no public metrics", "UNVERIFIED"],
          ["Instagram (not linked)", "instagram.com/apex_web_design", "“471 Followers, 3 Following, 10 Posts”; bio “Crafting Websites that convert Visitors into Customers”; no link to apexwebstudios.net", "OBSERVED (ownership unconfirmed)"],
          ["Facebook", "facebook.com/apexwebstudios", "Login wall", "UNVERIFIED"],
          ["LinkedIn", "linkedin.com/company/apex-web-studios", "Bot challenge (403)", "UNVERIFIED"],
          ["X", "x.com/ApexWebStudios", "57 posts, 10 followers, joined Jan 2023; newest post 30 Jul 2026; recent themes: opinion posts on AI, logos, algorithms", "OBSERVED"],
          ["TikTok / YouTube", "—", "No accounts linked from the website", "OBSERVED"],
      ], [1700, 2200, 3700, 1400]),
      P("**Implication:** the brand's social channels are effectively restarting. The plan prioritises consistency (about 4 posts/week, or 2 on the Lite plan) over volume, and asks Apex for analytics to set real baselines."),
      H1("5. Competitor review"),
      H2("5.1 Removed: unsupported competitors"),
      P("The first draft listed the competitors below. They are removed from all deliverables because (a) their data came only from search-engine snippets that were never verified, and (b) they were chosen on the mistaken assumption that Apex is a Los Angeles web-design shop. Apex is a Canada-headquartered, full-service studio serving clients globally."),
      TB(["Removed entry", "Reason"], [
          ["LA Web Design Experts", "Snippet-only follower data; LA-only web shop; not a like-for-like competitor"],
          ["Sunlight Media LLC", "Snippet-only data; never verified"],
          ["67 Web Design", "Snippet-only data; subscription model not verified"],
          ["LAD Solutions", "No social data found; never verified"],
          ["Affordable Web Design Los Angeles", "No data; never verified"],
          ["The Futur / Flux Academy (aspirational)", "Audience is designers, not Apex's buyers; follower figures unverified"],
      ], [3000, 6000]),
      H2("5.2 Verified competitive pressure"),
      TB(["Alternative", "Evidence (verified)", "What it means for Apex content"], [
          ["AI website builders (e.g. Squarespace Blueprint AI)", "Squarespace: “the Blueprint AI website builder guides you through a few simple choices based on your description of what you do” (T50)", "Starter-tier buyers have a credible DIY option. Answer it honestly (P10) and emphasise custom features, ownership, project management and growth services."],
          ["Price-sensitive buyers", "Apex's own reviews include “Pricing is a little steep for me compared to others but Apex does great work” (B08)", "Price-transparency series (P08, P13) and value explanations; never compete on 'cheapest'."],
      ], [2400, 3600, 3000]),
      H2("5.3 What we still need"),
      P("Apex should name 3–5 agencies it competes with for deals in Canada, the US and the UK. With page access to their social profiles, the competitor benchmark (formats, cadence, engagement) can then be built on verified data. Until then, the strategy relies on the verified opportunities below rather than claims about specific rivals."),
      H2("5.4 Opportunities (based on Apex's verified assets)"),
      UL(["**Price transparency:** Apex publishes every price, which can be turned into a content series (Price Tag, Explained).",
          "**Accessibility expertise:** Apex lists WCAG standards, the date of the month (IDPD) supports it, and website-accessibility lawsuits are rising (T46).",
          "**AI fluency:** Apex builds AI agents, so it can explain AI search and AI builders honestly.",
          "**Human proof:** a large body of verbatim reviews naming individual team members.",
          "**Three-country footprint:** Milton, Los Angeles and Birmingham give a local angle in each market."]),
      H1("6. Trend & platform research (December 2026)"),
      TB(["Trend", "Platform", "Verified evidence", "Source", "Relevance to Apex", "Use"], [list(t) for t in TRENDS], [1600, 900, 2600, 800, 1900, 1200]),
      H2("Key dates"),
      TB(["Date", "Moment", "Status", "Use"], [
          ["Sat 28 Nov", "Small Business Saturday (US)", "VERIFIED (SBA)", "Before the December window; not used"],
          ["Mon 30 Nov", "Cyber Monday ($15.1B forecast)", "VERIFIED (T53)", "P01 (Dec 1)"],
          ["Thu 3 Dec", "International Day of Persons with Disabilities", "VERIFIED (T56)", "P03, P04"],
          ["Fri 4 – Sat 12 Dec", "Hanukkah (begins at sundown Dec 4)", "VERIFIED (T57)", "P05"],
          ["24–26 Dec", "Christmas Eve / Christmas / Boxing Day", "Fixed dates", "P16"],
          ["31 Dec – 1 Jan", "New Year", "Fixed dates", "P14, P17"],
      ], [1600, 3300, 1900, 2200]),
      H1("7. Claims excluded as unverified"),
      TB(["Claim (from the first draft)", "Why excluded"], [
          ["68.01% of US Google searches end without a click (Search Engine Land)", "The source site blocked automated verification; could not confirm the figure or its producer"],
          ["Google AI calls businesses to “check availability”", "The actual announcement is narrower: US only, select categories, rollout unconfirmed"],
          ["Wix Harmony launched 21 Jan 2026", "Press-release site blocked verification"],
          ["“Unlabelled AI content is what consumers most want brands to stop posting”", "Not on the cited Sprout Social pages"],
          ["Sprout reports declining LinkedIn document reach", "Not on the cited page"],
          ["BrightLocal: 45% use AI for local recommendations", "Figure not visible on the page"],
          ["Market size figures (IBISWorld, Ken Research)", "Paywalled or inconsistent definitions"],
          ["2017–18 Google page-speed bounce statistics", "Outdated"],
          ["Apex's own stats (+1K clients, 100% on-time, etc.)", "Contradicted elsewhere on the site; awaiting client confirmation"],
      ], [4500, 4500]),
     ]
RS += [H1("8. Source list")] + [UL([f"{k} — {t}: {u} ({s})" for k, (t, u, s) in SRC.items()])]
json.dump({"cover": cover("Competitor & Trend Research Report", "Verified brand, social, competitor and trend research"), "blocks": RS},
          open(os.path.join(SPECS, "research.json"), "w"), ensure_ascii=False)

print("posts", len(POSTS), "standard", len(STD), "lite", len(LITE), "ready", len(READY), "blocked", len(BLOCKED), dict(pill))
print("xlsx", xlsx_path)
