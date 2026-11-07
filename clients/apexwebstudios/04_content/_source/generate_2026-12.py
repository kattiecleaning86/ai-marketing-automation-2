#!/usr/bin/env python3
"""Generate Apex Web Studios 2026-12 calendar CSV, content doc and creative briefs from one source."""
import csv, os, sys

ROOT = sys.argv[1]
SLUG = "apexwebstudios"
MONTH = "2026-12"
TZ = "ET (America/Toronto)"

BRAND_DO = [
    "Dark background (#0A0A0A / #1A1A1A) with red #D23030 as the single accent",
    "Inter / Inter Display for copy, Urbanist for headlines, IBM Plex Mono for code/stat callouts",
    "Real team, real screens, Apex's own website or permitted client work only",
    "Minimum 4.5:1 text contrast; large type for mobile",
    "Apex logo (light version on dark) bottom-right or end card",
]
BRAND_DONT = [
    "No stock 'handshake' clichés or other studios' designs/screenshots",
    "No guarantee language (rankings, results) or unconfirmed self-reported stats",
    "No legal advice wording on accessibility topics",
    "No unlicensed music — Instagram/LinkedIn in-app library or licensed tracks only",
    "No purple outside small accents; no more than one accent colour per frame",
]

SPECS = {
    "Reel": "9:16, 1080x1920 px, MP4 (H.264), 30-45 s, burned-in captions; keep text inside the central safe area (avoid top ~250 px and bottom ~400 px for UI overlays); cover frame 1080x1920 with 4:5 crop-safe title",
    "Carousel": "4:5, 1080x1350 px per slide, PNG; slide count as listed; text ≤ ~25 words per slide",
    "Document carousel (PDF)": "4:5, 1080x1350 px pages exported as a single PDF (≤ 10 pages); document title as listed; text ≤ ~30 words per page",
    "Static image": "4:5, 1080x1350 px, PNG",
    "Text post + image": "1200x1200 px or 1080x1350 px PNG; image must be legible as a thumbnail",
    "Vertical video": "9:16 (or 4:5 fallback), 1080x1920 px, MP4, 45-60 s, burned-in captions + SRT file",
}

P = []  # posts

def post(**k):
    P.append(k)

# ---------------------------------------------------------------- posts
post(
    date="2026-12-01", time="10:00", platform="LinkedIn", pillar="Build Smarter (Educate)", objective="Engagement",
    funnel="Awareness", persona="P1, P3",
    topic="Post-Cyber Monday website health check: 6 things to review before the December rush peaks",
    rationale="Adobe forecasts a record US online holiday season ($275.1B) and $15.1B on Cyber Monday (T53 — forecast, search-located). SMB owners (P1/P3) are mid-season; practical checks are timely and save-worthy. LinkedIn PDF carousels test strongly (TR12, T21/T23).",
    hook="Cyber Monday is over. Your website's busiest month isn't.",
    alt_hooks=["6 website checks to do before December's traffic peaks.", "Did your website survive Cyber Monday? Here's how to tell."],
    caption="""Cyber Monday is over. Your website's busiest month isn't.

Adobe forecast a record US online holiday season this year — and December traffic doesn't wait for your to-do list. (Source: Adobe, Sept 2026 forecast.)

Here's a 15-minute health check we'd run on any small business site this week:

1. Load your homepage on mobile data — not office Wi-Fi
2. Submit your own contact form and confirm the email arrives
3. Click every button in your holiday promo
4. Check your hours and holiday closures on your site AND your Google Business Profile
5. Read your checkout or booking flow out loud — where would you hesitate?
6. Make sure your phone number is tap-to-call

Swipe through for what to look for at each step.

Need a second pair of eyes? Book a free call with our team — link in the comments.""",
    cta="Book a free call (link in first comment: /contact-us with UTM)",
    hashtags="#SmallBusiness #WebDevelopment #ApexWebStudios",
    format="Document carousel (PDF)",
    script=[
        "Cover: Cyber Monday is over. Your website's busiest month isn't. | 6 checks in 15 minutes",
        "1 — Test on mobile data: Load your homepage on 4G/5G, not office Wi-Fi. Slow? Note which page.",
        "2 — Submit your own form: Does the email arrive? Does the thank-you page load?",
        "3 — Click every promo button: Broken holiday links cost the most in December.",
        "4 — Match your hours everywhere: Website + Google Business Profile must say the same thing.",
        "5 — Walk your checkout or booking: Where would a first-time visitor hesitate?",
        "6 — Tap-to-call: Your phone number should dial with one tap on mobile.",
        "Source note: Holiday forecast — Adobe, Sept 2026 (news.adobe.com).",
        "CTA: Want us to run this check for you? Book a free call — apexwebstudios.net",
    ],
    visual="Dark (#0A0A0A) pages, numbered red (#D23030) IBM Plex Mono step numbers, phone-frame mock-ups of a generic (non-client) site; checklist icons.",
    brief_summary="9-page LinkedIn PDF: holiday website health checklist.",
    kpi="Engagement rate ≥ page's Nov average +10%; ≥ 5 website clicks",
    alt_text="Cover slide on a black background reading 'Cyber Monday is over. Your website's busiest month isn't.' with a red '6 checks in 15 minutes' label.",
    shots=None,
    audio="N/A (document)",
)

post(
    date="2026-12-02", time="12:00", platform="Instagram + Facebook (cross-post)", pillar="Behind the Build", objective="Engagement",
    funnel="Consideration", persona="P1, P2",
    topic="What happens in the first 48 hours of an Apex website project",
    rationale="Apex packages promise 'Initial Design Concepts within 48 Hours' and a 'Dedicated Project Manager' (B04). Testimonials praise communication (B08); the main objection is agency 'radio silence' (B02, audience_market §5). Instagram favours original footage (TR8).",
    hook="Here's what happens in the first 48 hours after you hire us.",
    alt_hooks=["Hired a web agency and heard nothing for weeks? Not here.", "Hour 0 to hour 48 of a new website project."],
    caption="""Here's what happens in the first 48 hours after you hire us. ⏱️

Hour 0 — You meet your dedicated project manager
Hour 1 — We go through your goals, pages and must-haves
Hour 24 — Our designers are sketching layouts
Hour 48 — You get your first design concepts

That's built into our website packages — first concepts within 48 hours, with one project manager as your point of contact from start to finish.

No surprises. No radio silence. 🖤

Thinking about a new site for 2027? Tap the link in bio to book a free call.""",
    cta="Book a free call — link in bio",
    hashtags="#WebDesign #SmallBusinessWebsite #WebDevelopment #SmallBusinessOwner #ApexWebStudios",
    format="Reel",
    script=[
        ("0-3s", "Close-up: laptop opening, timer graphic 00:00", "Hour 0 → Hour 48", "Here's what happens in the first 48 hours after you hire us.", "Upbeat, licensed in-app track, low under VO"),
        ("3-10s", "Project manager on a video call, smiling, notepad", "Hour 0: Meet your project manager", "First, you meet your dedicated project manager — one person, start to finish.", "—"),
        ("10-18s", "Screen recording: shared doc with goals/pages checklist", "Hour 1: Goals, pages, must-haves", "We map your goals, your pages and your must-haves.", "—"),
        ("18-28s", "Designer sketching wireframes; Figma timelapse", "Hour 24: Layouts in progress", "By the next day, our designers are working on layouts.", "Tempo lift"),
        ("28-36s", "Concept screens revealed on a monitor", "Hour 48: First concepts ✅", "And within 48 hours, you're looking at your first design concepts.", "Hit on reveal"),
        ("36-42s", "End card: logo on black, red underline", "No surprises. No radio silence. | Book a free call — link in bio", "Ready for 2027? Book a free call — link in bio.", "Fade out"),
    ],
    visual="Real Apex team and screens (no client work unless permission given). Warm natural light; dark UI overlays with red timer counter in IBM Plex Mono.",
    brief_summary="40 s behind-the-scenes Reel: Hour 0 → Hour 48 of a website project.",
    kpi="Shares + saves ≥ 2% of reach; ≥ 2 DMs",
    alt_text="Video: an Apex project manager on a video call, then designers sketching layouts, ending with website concepts on a monitor and the text 'Hour 48: First concepts'.",
    shots=["PM on camera (volunteer team member — confirm)", "Over-shoulder screen recording of a planning doc (dummy data)", "Designer hands sketching + Figma timelapse (non-client file)", "Monitor reveal of concept (Apex demo or permitted work)", "End card"],
    audio="Upbeat instrumental from Instagram's in-app library; VO recorded by PM or voice-over artist.",
    client_input="Confirm the hour-by-hour flow matches the real process; nominate on-camera PM.",
)

post(
    date="2026-12-03", time="09:00", platform="Instagram + Facebook (cross-post)", pillar="Build Smarter (Educate)", objective="Awareness",
    funnel="Awareness", persona="P1",
    topic="International Day of Persons with Disabilities: 3 website accessibility checks in 60 seconds",
    rationale="Dec 3 is the UN International Day of Persons with Disabilities; 2026 theme 'The CRPD at 20' (T56). Apex offers 'WCAG Compliance & Accessibility Standards' (B03, UI/UX page). No competitor seen owns this topic (competitors §2).",
    hook="Try this on your website right now: put your mouse away.",
    alt_hooks=["3 accessibility checks you can do in 60 seconds.", "Can everyone actually use your website?"],
    caption="""Try this on your website right now: put your mouse away. 🖱️❌

Today is the International Day of Persons with Disabilities. Here are 3 quick accessibility checks any business owner can do in 60 seconds:

1️⃣ Keyboard test — press Tab. Can you see where you are on the page at every step?
2️⃣ Image check — do your key images have alt text describing what they show?
3️⃣ Contrast check — is any text light grey on white? If it's hard for you to read, it's harder for others.

These are starting points, not a full audit — but they catch common issues.

Our team designs to WCAG accessibility standards. Want a hand? DM us "access" or tap the link in bio.

Save this and run the checks this week. 🖤""",
    cta="Save this + DM us to talk accessibility",
    hashtags="#WebAccessibility #IDPD #SmallBusinessWebsite #WebDesign #ApexWebStudios",
    format="Reel",
    script=[
        ("0-3s", "Hand pushes mouse off desk", "Put your mouse away.", "Try this on your website right now: put your mouse away.", "Clean, minimal licensed track"),
        ("3-8s", "Title card", "Dec 3 · International Day of Persons with Disabilities | 3 checks · 60 seconds", "It's the International Day of Persons with Disabilities. Here are three checks in sixty seconds.", "—"),
        ("8-22s", "Screen recording: tabbing through a demo site; focus outline visible vs. missing", "1. Press Tab — can you see where you are?", "One: press Tab. If you can't see where you are on the page, keyboard users can't either.", "—"),
        ("22-34s", "Screen recording: image with alt text shown in inspector / CMS field", "2. Do key images have alt text?", "Two: check your key images have alt text that describes what they show.", "—"),
        ("34-46s", "Split screen: light grey text on white vs. dark text on white", "3. Is your text easy to read?", "Three: if any text is light grey on white, fix the contrast.", "—"),
        ("46-55s", "Team member to camera", "Starting points — not a full audit.", "These catch common issues — they're not a full audit. We design to WCAG standards; DM us if you want help.", "—"),
        ("55-60s", "End card", "Save this · DM 'access' · apexwebstudios.net", "Save this and try it this week.", "Fade"),
    ],
    visual="Screen recordings on an Apex demo page (not a third-party site). High-contrast captions (white on black, ≥ 4.5:1). Large type.",
    brief_summary="60 s educational Reel: 3 quick website accessibility checks for IDPD.",
    kpi="Saves ≥ 3% of reach; non-follower reach ≥ 50% (publish as Trial Reel first if available)",
    alt_text="Video: a hand pushes a mouse aside, then screen recordings show keyboard focus outlines, an image alt-text field and a text contrast comparison, with captions listing three accessibility checks.",
    shots=["Mouse push-off (desk)", "Screen recordings x3 on Apex demo page", "Team member talking head (volunteer)", "End card"],
    audio="Calm licensed instrumental; full burned-in captions mandatory (accessibility post).",
)

post(
    date="2026-12-03", time="10:00", platform="LinkedIn", pillar="Build Smarter (Educate)", objective="Engagement",
    funnel="Awareness", persona="P1, P3",
    topic="International Day of Persons with Disabilities: 5 website accessibility fixes that help every visitor",
    rationale="IDPD Dec 3, theme 'The CRPD at 20' (T56). Seyfarth Shaw reports 5,006 federal ADA Title III filings in H1 2026, +9% YoY — all Title III, not only websites (T45). Apex offers WCAG-standard design (B03). LinkedIn documents perform strongly (TR12).",
    hook="Accessibility isn't a feature. It's whether people can use your website at all.",
    alt_hooks=["5 accessibility fixes that make your website better for everyone.", "Today is IDPD. Here's what that means for your website."],
    caption="""Accessibility isn't a feature. It's whether people can use your website at all.

Today is the UN's International Day of Persons with Disabilities. It's a good moment to look at your site through a different lens.

It's also a business issue: Seyfarth Shaw counted 5,006 federal ADA Title III lawsuits in the first half of 2026, up 9% year over year (these cover all Title III claims, not only websites).

5 fixes that help every visitor:
→ Visible keyboard focus
→ Descriptive alt text on meaningful images
→ Text contrast that's easy to read
→ Captions on video
→ Clear form labels and error messages

Our team designs to WCAG accessibility standards. If you'd like a second look at your site, our DMs are open.

(This is general information, not legal advice.)""",
    cta="Send us a message for an accessibility review conversation",
    hashtags="#WebAccessibility #WebDevelopment #ApexWebStudios",
    format="Document carousel (PDF)",
    script=[
        "Cover: Accessibility isn't a feature. | 5 website fixes for Dec 3 — International Day of Persons with Disabilities",
        "Why now: 5,006 federal ADA Title III lawsuits in H1 2026 (+9% YoY), all Title III claims — Seyfarth Shaw, Sept 2026.",
        "Fix 1 — Visible keyboard focus: Every link and button should show where you are when using Tab.",
        "Fix 2 — Meaningful alt text: Describe what the image shows and why it matters.",
        "Fix 3 — Readable contrast: Aim for at least 4.5:1 for body text (WCAG AA).",
        "Fix 4 — Captions on video: Burned-in or closed captions on every video with speech.",
        "Fix 5 — Clear forms: Visible labels and plain-language error messages.",
        "Note: General information only — not legal advice.",
        "CTA: Want a second look at your site? Message Apex Web Studios.",
    ],
    visual="Black pages with white type; red accent icon per fix; the deck itself must pass contrast (≥ 4.5:1) and use ≥ 24 px body type.",
    brief_summary="9-page LinkedIn PDF: 5 accessibility fixes for IDPD.",
    kpi="Engagement rate ≥ page's Nov average +10%; ≥ 3 inbound messages",
    alt_text="Cover slide on black: 'Accessibility isn't a feature.' with subtitle '5 website fixes for Dec 3 — International Day of Persons with Disabilities'.",
    shots=None,
    audio="N/A (document)",
)

post(
    date="2026-12-04", time="17:00", platform="Instagram + Facebook (cross-post)", pillar="Community & Moments", objective="Community",
    funnel="Loyalty", persona="All",
    topic="Hanukkah greeting (Hanukkah begins at sundown Dec 4, 2026)",
    rationale="Hanukkah runs from sundown Fri Dec 4 to Sat Dec 12, 2026 (T57, T58). Inclusive seasonal moment; supports the Community pillar (10%).",
    hook="Happy Hanukkah to everyone celebrating. 🕎",
    alt_hooks=["Wishing light and warmth this Hanukkah.", "To our clients and friends celebrating — Happy Hanukkah."],
    caption="""Happy Hanukkah to everyone celebrating. 🕎

Wishing you, your families and your teams eight nights of light and warmth.

— The Apex Web Studios team""",
    cta="None (goodwill post)",
    hashtags="#HappyHanukkah #ApexWebStudios",
    format="Static image",
    script="N/A",
    visual="Minimal: black background, eight small warm-light points in a row with a subtle red-to-gold glow; 'Happy Hanukkah' in Urbanist; small logo. Respectful, no novelty clip-art.",
    brief_summary="Minimal Hanukkah greeting graphic.",
    kpi="Engagement rate ≥ account average; zero negative sentiment",
    alt_text="Black graphic with a row of eight softly glowing lights and the words 'Happy Hanukkah' from Apex Web Studios.",
    shots=None,
    audio="N/A",
)

post(
    date="2026-12-08", time="10:00", platform="LinkedIn", pillar="Build Smarter (Educate)", objective="Engagement",
    funnel="Awareness", persona="P1, P3",
    topic="AI search is changing who gets the click — what small businesses can do",
    rationale="Ahrefs associates AI Overviews with ~58% lower click-through for the top result (T34); SparkToro data via Search Engine Land: 68.01% of US Google searches ended without a click, Jan–Apr 2026 (T35); Seer finds pages cited in AI Overviews earn more clicks than uncited ones (T37). Apex sells SEO + AI services (B03). All search-located — verify before approval.",
    hook="More of your customers are getting answers without ever clicking to your website.",
    alt_hooks=["AI search is changing who gets the click.", "Ranking #1 doesn't mean what it used to."],
    caption="""More of your customers are getting answers without ever clicking to your website.

A few data points from this year:
• SparkToro data reported by Search Engine Land found 68% of US Google searches ended without a click (Jan–Apr 2026).
• Ahrefs found AI Overviews were associated with ~58% lower click-through for the top-ranking page.
• Seer Interactive found pages cited inside AI Overviews earn more clicks than pages that aren't.

These are correlations, and the methods are debated — but the direction is clear: being the clearest answer matters more than ever.

What we're doing for clients:
1. Service pages that answer real questions in plain language
2. Accurate business info everywhere (website, Google Business Profile)
3. Clean structure search engines and AI tools can read

Nobody can promise an AI citation. But you can make your site easier to understand.

What's one question your customers always ask you? That's your next page.""",
    cta="Comment with the question your customers ask most",
    hashtags="#AISearch #SEO #ApexWebStudios",
    format="Text post + image",
    script="N/A",
    visual="Single 1080x1350 image: black background, three large IBM Plex Mono figures ('68%', '~58%', 'cited > uncited') each with a source line; red underline on 'be the clearest answer'.",
    brief_summary="Stat card image for an AI-search thought-leadership text post.",
    kpi="Comments ≥ 5; engagement rate ≥ page's Nov average",
    alt_text="Graphic with three data points: 68% of US Google searches ended without a click (SparkToro via Search Engine Land), about 58% lower click-through with AI Overviews (Ahrefs), and cited pages earn more clicks (Seer Interactive).",
    shots=None,
    audio="N/A",
)

post(
    date="2026-12-09", time="12:00", platform="Instagram + Facebook (cross-post)", pillar="Proof & Results", objective="Engagement",
    funnel="Consideration", persona="P1",
    topic="What clients say — 3 verbatim reviews",
    rationale="Customers praise communication and responsiveness (B08 testimonials; audience_market §5). Competitors seen don't use reviews on social (competitors §2). Quotes are verbatim from apexwebstudios.net/testimonials — permission for social reuse pending (brief Q5).",
    hook="We could tell you we're easy to work with. We'd rather let our clients do it.",
    alt_hooks=["3 things our clients say (in their own words).", "Real reviews. Real businesses. No edits."],
    caption="""We could tell you we're easy to work with. We'd rather let our clients do it. 💬

Swipe for three reviews, in their own words — from Body Rituals Spa, UpkeepX and Copy Smart.

What we hear most isn't about code. It's about communication: being reachable, responsive, and actually listening.

Thank you to every client who took the time to leave a review this year. 🖤

Want to see more? Tap the link in bio.""",
    cta="See all reviews — link in bio (/testimonials)",
    hashtags="#ClientLove #WebDesign #SmallBusinessWebsite #SmallBusinessOwner #ApexWebStudios",
    format="Carousel",
    script=[
        "Slide 1 (cover): We could tell you we're easy to work with. | We'd rather let our clients do it. →",
        "Slide 2: \"The website not only looks beautiful, but it's also intuitive and easy to navigate, which is exactly what we wanted.\" — Body Rituals Spa",
        "Slide 3: \"I am most impressed by how proactive and responsive they are.\" — Business Owner, UpkeepX",
        "Slide 4: \"Apex Web Studios is at the top of their game.\" — Owner, Copy Smart",
        "Slide 5 (CTA): Read more reviews → apexwebstudios.net/testimonials | Book a free call — link in bio",
    ],
    visual="Large quote marks in red; quotes in white Inter on black; attribution in IBM Plex Mono grey #F0F0F0. No client logos unless permission given.",
    brief_summary="5-slide testimonial carousel with verbatim quotes.",
    kpi="Profile visits ≥ 1.5% of reach; saves + shares ≥ 1%",
    alt_text="Carousel of client quotes in white text on black: Body Rituals Spa, UpkeepX and Copy Smart describing working with Apex Web Studios.",
    shots=None,
    audio="N/A",
    client_input="Confirm written permission from Body Rituals Spa, UpkeepX and Copy Smart to reuse their reviews on social. Hold post until confirmed.",
)

post(
    date="2026-12-09", time="16:00", platform="LinkedIn", pillar="Offers & Packages", objective="Leads",
    funnel="Conversion", persona="P1, P3",
    topic="$599 to $7,999: what each Apex website package actually includes",
    rationale="Apex publishes full package pricing and inclusions (B04) — rare in the category (competitors §2). Price is a known objection in public reviews (B08). Pricing transparency supports the 'No Hidden Cost' message (B01). Wednesday ~16:00 tests Buffer's LinkedIn window (T25).",
    hook="\"How much does a website cost?\" Here's our actual answer — with the price list.",
    alt_hooks=["What does $599 get you vs $7,999? We'll show you.", "Website pricing, without the sales call."],
    caption=""""How much does a website cost?"

It depends — but that answer frustrates everyone. So here's our actual price list, and what each package includes.

• Starter — $599: 3-page custom site, mobile-responsive, contact form, CMS
• Growth — $1,199: 5 pages, 3 custom banners, CMS
• Professional Business — $1,999: up to 10 pages, SEO-friendly structure, unlimited revisions
• Corporate Elite — $3,199: up to 15 pages, lead capture, optional booking/ordering
• E-commerce Growth — $4,999: custom store, up to 200 products, payment gateway
• Platinum Enterprise — $7,999: up to 20 pages, advanced CMS, enterprise-level build

Every package includes first design concepts within 48 hours and a dedicated project manager.

Prices in USD, one-time. Full details (and CAD/GBP) on our pricing page.

Not sure which fits? Book a free call and we'll tell you honestly — even if it's the smallest one.""",
    cta="Book a free call / view pricing (link in first comment)",
    hashtags="#WebDevelopment #SmallBusiness #ApexWebStudios",
    format="Document carousel (PDF)",
    script=[
        "Cover: How much does a website cost? | Our actual price list →",
        "Starter — $599: 3-page custom site · mobile-responsive · contact form · CMS · first concepts in 48 h",
        "Growth — $1,199: 5-page custom site · 3 custom banners · CMS · performance-focused build",
        "Professional Business — $1,999: up to 10 pages · SEO-friendly structure · CMS/admin panel · unlimited revisions",
        "Corporate Elite — $3,199: up to 15 pages · lead capture & newsletter · optional booking/ordering/payments",
        "E-commerce Growth — $4,999: custom store · up to 200 products · secure cart & payment gateway",
        "Platinum Enterprise — $7,999: up to 20 pages · advanced CMS · complex architecture",
        "Every package: dedicated project manager · first concepts within 48 hours. USD, one-time. CAD/GBP on site.",
        "CTA: Not sure which fits? Book a free call — apexwebstudios.net/pricing",
    ],
    visual="One package per page; price in large IBM Plex Mono red; inclusions as 3-5 white bullets; consistent grid; small 'Prices as of Dec 2026' footer.",
    brief_summary="9-page LinkedIn PDF: website package price list and inclusions.",
    kpi="Link clicks to /pricing or /contact-us ≥ 10; ≥ 2 inquiries attributed",
    alt_text="Cover slide: 'How much does a website cost? Our actual price list' on black with a red arrow.",
    shots=None,
    audio="N/A (document)",
    client_input="Confirm prices and inclusions unchanged for December 2026.",
)

post(
    date="2026-12-10", time="09:00", platform="Instagram + Facebook (cross-post)", pillar="Build Smarter (Educate)", objective="Awareness",
    funnel="Awareness", persona="P1",
    topic="Your Google Business Profile is starting to talk to AI — 3 things to update",
    rationale="Google announced agentic AI Mode features at I/O 2026, including AI calling local businesses for some categories (T38, May 2026, search-located — availability varies by country). Hours/services accuracy is a quick win for SMB owners (P1). Keyword-led on-screen text supports social search (TR10).",
    hook="Google's AI may soon call your business for a customer. Is your info right?",
    alt_hooks=["3 things to update on your Google Business Profile this week.", "AI is reading your business listing. Here's what it sees."],
    caption="""Google's AI may soon call your business for a customer. Is your info right? 🤖📞

At Google I/O 2026, Google announced AI Mode features that can check availability with local businesses for some categories (availability varies by country).

Whether AI or a human is looking, these 3 things should match everywhere — your website AND your Google Business Profile:

1️⃣ Opening hours (including holiday hours!)
2️⃣ Your services, in plain language
3️⃣ Your phone number and booking link

Takes 10 minutes. Do it before the holidays.

Need help making your website and listings work together? Link in bio.""",
    cta="Save + update your listing this week; link in bio for help",
    hashtags="#GoogleBusinessProfile #LocalSEO #AISearch #SmallBusinessTips #ApexWebStudios",
    format="Reel",
    script=[
        ("0-3s", "Phone ringing on a shop counter, caller ID 'Google'", "Google's AI might call you.", "Google's AI may soon call your business for a customer.", "Ringtone SFX then licensed beat"),
        ("3-10s", "Team member to camera", "Announced at Google I/O 2026", "Google announced AI features that can check availability with local businesses — in some categories and countries.", "—"),
        ("10-20s", "Screen recording: editing hours in a demo Google Business Profile", "1. Hours — incl. holidays", "One: your hours. Including holiday hours.", "—"),
        ("20-30s", "Screen recording: services list", "2. Services in plain language", "Two: your services, in words customers actually use.", "—"),
        ("30-38s", "Screen recording: phone + booking link", "3. Phone + booking link", "Three: your phone number and booking link — matching your website.", "—"),
        ("38-45s", "End card", "10 minutes. Do it this week. | Link in bio", "Ten minutes. Do it before the holidays.", "Fade"),
    ],
    visual="Demo listing with dummy business data (never a real third-party listing). Red highlight boxes on fields. Captions on throughout.",
    brief_summary="45 s Reel: update your Google Business Profile for AI search.",
    kpi="Non-follower reach ≥ 50%; saves ≥ 2% of reach",
    alt_text="Video: a phone rings on a counter, then a screen recording shows hours, services and phone number being updated on a demo Google Business Profile.",
    shots=["Phone-on-counter prop shot", "Talking head (volunteer)", "3 screen recordings on dummy listing", "End card"],
    audio="Ringtone SFX (royalty-free) + in-app licensed beat.",
)

post(
    date="2026-12-15", time="10:00", platform="LinkedIn", pillar="Build Smarter (Educate)", objective="Engagement",
    funnel="Consideration", persona="P1, P2",
    topic="AI website builder or agency? An honest guide to when each makes sense",
    rationale="AI builders are mainstream (Wix Harmony launched 2026-01-21, T49; Squarespace Blueprint AI, T50). Low-price builder offers anchor prices down (competitors §3). An honest comparison positions Apex credibly without disparaging competitors.",
    hook="Sometimes an AI website builder is the right call. Here's when it isn't.",
    alt_hooks=["AI builder vs. agency: an honest guide from an agency.", "Should you just use an AI website builder? Sometimes, yes."],
    caption="""Sometimes an AI website builder is the right call. Here's when it isn't.

AI builders went mainstream this year — Wix launched Wix Harmony in January, and Squarespace has Blueprint AI. They're genuinely useful.

An AI builder probably makes sense if:
• You need a simple site live this week
• You're testing an idea before investing
• You're happy to maintain it yourself

An agency probably makes sense if:
• You need custom features (booking, portals, integrations)
• Your site has to rank, convert and scale
• You'd rather spend your time running the business

We'd rather you choose the right tool than the wrong agency.

Which camp are you in for 2027?""",
    cta="Comment: which camp are you in for 2027?",
    hashtags="#WebDevelopment #SmallBusiness #ApexWebStudios",
    format="Document carousel (PDF)",
    script=[
        "Cover: AI website builder or agency? | An honest guide (from an agency)",
        "AI builders are mainstream: e.g. Wix Harmony (launched Jan 2026), Squarespace Blueprint AI.",
        "Choose an AI builder if… you need a simple site fast · you're testing an idea · you'll maintain it yourself",
        "Choose an agency if… you need custom features · the site must rank, convert & scale · you want your time back",
        "Questions to ask yourself: Who updates it? What happens when you outgrow it? Do you own it?",
        "Our take: the right tool beats the wrong agency.",
        "CTA: Weighing it up for 2027? Book a free, no-pressure call — apexwebstudios.net",
    ],
    visual="Two-column comparison pages (left grey 'AI builder', right red 'Agency'); neutral icons; no competitor logos or screenshots.",
    brief_summary="7-page LinkedIn PDF: honest AI builder vs agency comparison.",
    kpi="Comments ≥ 5; engagement rate ≥ page's Nov average +10%",
    alt_text="Cover slide on black: 'AI website builder or agency? An honest guide (from an agency)'.",
    shots=None,
    audio="N/A (document)",
)

post(
    date="2026-12-16", time="12:00", platform="Instagram + Facebook (cross-post)", pillar="Behind the Build", objective="Engagement",
    funnel="Consideration", persona="P1, P2",
    topic="Meet the people behind your project",
    rationale="Testimonials repeatedly name individual team members (Ahmed, Mark, Wade, Mo, Kais — B08), showing people drive trust. Sprout Social reports consumers want human, not unlabelled AI, content (TR14, T29).",
    hook="Our clients mention our team by name in their reviews. Time you met them.",
    alt_hooks=["Meet the people who'll actually build your website.", "Behind every Apex project: these faces."],
    caption="""Our clients mention our team by name in their reviews. Time you met them. 👋

Meet [Name 1], [Role 1], [Name 2], [Role 2] and [Name 3], [Role 3] — a few of the people behind the websites, apps and campaigns we build.

Ask them anything in the comments — they'll answer. 👇""",
    cta="Ask the team a question in the comments",
    hashtags="#MeetTheTeam #WebDesign #WebDevelopment #AgencyLife #ApexWebStudios",
    format="Reel",
    script=[
        ("0-3s", "Quick cuts of three team members turning to camera", "Meet the team", "Our clients mention our team by name. Time you met them.", "Upbeat licensed track"),
        ("3-13s", "Team member 1 at desk", "[Name 1] · [Role 1]", "[Name 1]: \"I'm [Name 1], and I [what they do — 1 line].\"", "—"),
        ("13-23s", "Team member 2", "[Name 2] · [Role 2]", "[Name 2]: one-line intro", "—"),
        ("23-33s", "Team member 3", "[Name 3] · [Role 3]", "[Name 3]: one-line intro", "—"),
        ("33-40s", "Group shot / end card", "Ask us anything 👇", "Ask us anything in the comments.", "Fade"),
    ],
    visual="Natural office light, eye-level framing, team in own clothes; name lower-thirds in Urbanist with red bar.",
    brief_summary="40 s 'meet the team' Reel with three volunteer team members.",
    kpi="Comments ≥ 10; profile visits ≥ 1.5% of reach",
    alt_text="Video: three Apex Web Studios team members introduce themselves at their desks, with name and role captions.",
    shots=["3 volunteer team members (signed consent to appear)", "Desk B-roll", "Group shot"],
    audio="In-app licensed track; captions burned-in.",
    client_input="Names, roles and on-camera consent for 3 team members.",
)

post(
    date="2026-12-17", time="10:00", platform="LinkedIn", pillar="Behind the Build", objective="Engagement",
    funnel="Consideration", persona="P2, P3",
    topic="Why every Apex project gets one dedicated project manager",
    rationale="Every web package includes a 'Dedicated Project Manager' (B04); brand promise 'No surprises. No radio silence. No hidden costs.' (B02). Responsiveness is the top praise theme (B08). LinkedIn vertical video is expanding (TR13); spaced from the Dec 16 IG team Reel.",
    hook="The most common complaint about agencies isn't the work. It's the silence.",
    alt_hooks=["Why we give every project one person to call.", "\"Who do I even talk to?\" — never again."],
    caption="""The most common complaint about agencies isn't the work. It's the silence.

That's why every website project at Apex gets one dedicated project manager — one person who knows your project, answers your messages and keeps things moving.

In this short video, [PM name] explains what that looks like day to day.

No surprises. No radio silence. No hidden costs.

How do you prefer agencies to keep you updated — weekly calls, async updates, or something else?""",
    cta="Comment your preferred update style",
    hashtags="#ProjectManagement #WebDevelopment #ApexWebStudios",
    format="Vertical video",
    script=[
        ("0-4s", "PM to camera, office background", "The silence is the problem.", "The most common complaint about agencies isn't the work — it's the silence.", "No music / very low bed"),
        ("4-20s", "PM to camera", "One project. One point of contact.", "Every project here gets one dedicated project manager. That's me, for a lot of our clients.", "—"),
        ("20-40s", "Cutaways: PM messaging, checklist board, call", "What that means for you", "[PM explains in own words: how updates are shared, response expectations — must match real practice.]", "—"),
        ("40-55s", "PM to camera", "No surprises. No radio silence.", "No surprises. No radio silence. That's the deal.", "—"),
        ("55-60s", "End card", "apexwebstudios.net", "—", "—"),
    ],
    visual="Talking head, 9:16, mid-shot, lapel mic; IBM Plex Mono lower-thirds; red accent bar.",
    brief_summary="60 s LinkedIn talking-head video from a project manager.",
    kpi="Average watch time ≥ 15 s; comments ≥ 5",
    alt_text="Video: an Apex Web Studios project manager speaks to camera about being a single point of contact for clients.",
    shots=["PM talking head (volunteer, consent)", "Cutaways: messaging, task board, video call (dummy data)"],
    audio="Clean dialogue; optional low licensed bed; SRT captions.",
    client_input="Nominate PM; confirm described update cadence reflects actual practice.",
)

post(
    date="2026-12-18", time="09:00", platform="Instagram + Facebook (cross-post)", pillar="Offers & Packages", objective="Leads",
    funnel="Conversion", persona="P1",
    topic="Launching a business in 2027? What our $599 Starter website includes",
    rationale="Starter Web Package $599 is aimed at 'individuals and small businesses' (B04); new-year planning window (TR16). Different angle/platform from the Dec 9 LinkedIn price list (focus on one package for new businesses).",
    hook="Starting a business in 2027? Here's what $599 gets you.",
    alt_hooks=["Your first website doesn't have to cost thousands.", "A custom website for $599 — here's exactly what's included."],
    caption="""Starting a business in 2027? Here's what $599 gets you. 🚀

Our Starter Web Package includes:
✔️ 3-page custom website with a tailored layout
✔️ Mobile-responsive on every device
✔️ Contact / inquiry form
✔️ CMS so you can edit it yourself
✔️ First design concepts within 48 hours
✔️ A dedicated project manager
✔️ 100% ownership of your site

One-time price, USD. CAD and GBP pricing on our site.

Want to start January with a website? Tap the link in bio to book a free call.""",
    cta="Book a free call — link in bio",
    hashtags="#SmallBusinessWebsite #NewBusiness #WebDesign #SmallBusinessOwner #ApexWebStudios",
    format="Carousel",
    script=[
        "Slide 1 (cover): Starting a business in 2027? | Here's what $599 gets you →",
        "Slide 2: 3-page custom website — tailored layout design",
        "Slide 3: Mobile-responsive + contact form + CMS you can edit",
        "Slide 4: First concepts in 48 hours · dedicated project manager",
        "Slide 5: 100% ownership rights · 100% satisfaction guarantee",
        "Slide 6 (CTA): Start January with a website. Book a free call — link in bio | One-time, USD",
    ],
    visual="Phone mock-up of a generic 3-page site; '$599' in large red IBM Plex Mono on cover; checkmarks in red.",
    brief_summary="6-slide Starter package carousel for new businesses.",
    kpi="Link-in-bio clicks ≥ 15; ≥ 2 DMs or inquiries",
    alt_text="Carousel cover: 'Starting a business in 2027? Here's what $599 gets you' with a phone showing a simple website.",
    shots=None,
    audio="N/A",
    client_input="Confirm Starter price/inclusions and the satisfaction-guarantee wording are current; confirm refund terms are linked where needed.",
)

post(
    date="2026-12-22", time="10:00", platform="LinkedIn", pillar="Proof & Results", objective="Engagement",
    funnel="Consideration", persona="P1, P3",
    topic="Client story: a full rebrand and website against a deadline (Jamar Root review)",
    rationale="Verbatim public review on apexwebstudios.net/testimonials (Jamar Root, Aug 16, 2024 — B08) describes a deadline-driven rebrand + website and praises communication. Proof pillar (15%); no case studies exist yet (brand_analysis §6). Permission pending (brief Q5).",
    hook="A full rebrand and a new website — on a fixed deadline.",
    alt_hooks=["What a client said after a deadline-driven rebrand.", "Deadlines don't scare us. Silence does."],
    caption="""A full rebrand and a new website — on a fixed deadline.

That was the brief from client Jamar Root. In Jamar's words:

\"Communication was AMAZING and they did a great job of taking my ideas and turning them into something even better than I could have imagined.\"

Deadlines don't scare us. Silence does — which is why we don't do it.

Thank you, Jamar. 🖤

Planning a rebrand or a new site for 2027? Let's talk.""",
    cta="Message us to plan a 2027 rebrand or website",
    hashtags="#Branding #WebDesign #ApexWebStudios",
    format="Text post + image",
    script="N/A",
    visual="Quote card: black background, large red quote marks, quote 'Communication was AMAZING…' in white Inter, attribution 'Jamar Root — Apex client' in IBM Plex Mono.",
    brief_summary="Quote card for client-story text post.",
    kpi="Engagement rate ≥ page's Nov average; ≥ 2 inbound messages",
    alt_text="Quote card on black: 'Communication was AMAZING and they did a great job of taking my ideas and turning them into something even better than I could have imagined.' — Jamar Root, Apex Web Studios client.",
    shots=None,
    audio="N/A",
    client_input="Written permission from Jamar Root to feature the review and name on social.",
)

post(
    date="2026-12-22", time="12:00", platform="Instagram + Facebook (cross-post)", pillar="Build Smarter (Educate)", objective="Engagement",
    funnel="Awareness", persona="P1, P2",
    topic="Your 2027 website checklist (save-worthy carousel)",
    rationale="Year-end planning window (TR16); budgets reset in January (audience_market §3, hypothesis). Combines verified themes from the month: accessibility (TR1), AI search (TR4/TR5), mobile and forms. Save-worthy format for Instagram.",
    hook="Before you plan anything else for 2027, check your website.",
    alt_hooks=["Your 2027 website checklist. Save it.", "10 minutes now saves you a year of lost leads."],
    caption="""Before you plan anything else for 2027, check your website. ✅

Swipe for an 8-point checklist — save it for your first week back in January.

How many can you tick off already? Tell us in the comments 👇""",
    cta="Save this + comment your score",
    hashtags="#SmallBusinessTips #SmallBusinessWebsite #WebDesign #NewYearPlanning #ApexWebStudios",
    format="Carousel",
    script=[
        "Slide 1 (cover): Your 2027 website checklist ✅ | Save this for January",
        "Slide 2: ☐ Loads fast on mobile data  ☐ Tap-to-call phone number",
        "Slide 3: ☐ Contact form tested — and the emails arrive",
        "Slide 4: ☐ Hours, services & phone match your Google Business Profile",
        "Slide 5: ☐ Keyboard focus visible  ☐ Alt text on key images  ☐ Readable contrast",
        "Slide 6: ☐ Service pages answer the questions customers actually ask",
        "Slide 7: ☐ You own your domain, site and logins",
        "Slide 8 (CTA): Score under 6? Book a free website call — link in bio",
    ],
    visual="Checklist aesthetic: white checkboxes on black, red ticks; one idea per slide; slide numbers in IBM Plex Mono.",
    brief_summary="8-slide 2027 website checklist carousel.",
    kpi="Saves ≥ 3% of reach; comments ≥ 5",
    alt_text="Carousel cover: 'Your 2027 website checklist — save this for January' with empty checkboxes on a black background.",
    shots=None,
    audio="N/A",
)

post(
    date="2026-12-24", time="10:00", platform="Instagram + Facebook (cross-post)", pillar="Community & Moments", objective="Community",
    funnel="Loyalty", persona="All",
    topic="Season's greetings + holiday office hours",
    rationale="Christmas Eve; clients need holiday availability (brief Q8). Inclusive seasonal greeting supports the Community pillar.",
    hook="From all of us at Apex: happy holidays. 🖤",
    alt_hooks=["Thank you for building with us this year.", "Season's greetings from Milton, Los Angeles and Birmingham."],
    caption="""From all of us at Apex: happy holidays. 🖤

Thank you to every client, partner and follower who built something with us this year.

Holiday hours:
[Dates/hours — to be confirmed by Apex]

Wishing you a restful break and a great start to 2027.

— The Apex Web Studios team in Canada, the USA and the UK""",
    cta="None (goodwill + information)",
    hashtags="#HappyHolidays #SeasonsGreetings #ApexWebStudios",
    format="Static image",
    script="N/A",
    visual="Team photo (if available, with consent) or minimal black card with red/white festive line art; three city names (Milton · Los Angeles · Birmingham) in IBM Plex Mono.",
    brief_summary="Holiday greeting card with office hours.",
    kpi="Engagement rate ≥ account average",
    alt_text="Holiday card from Apex Web Studios on a black background with festive line art and the city names Milton, Los Angeles and Birmingham.",
    shots=None,
    audio="N/A",
    client_input="Holiday office hours; team photo + consent (optional).",
)

post(
    date="2026-12-29", time="10:00", platform="LinkedIn", pillar="Behind the Build", objective="Engagement",
    funnel="Loyalty", persona="P2, P3, P4",
    topic="What our team learned building in 2026 (team reflections)",
    rationale="Year-end reflection window (TR16). Human, first-person content performs with audiences wary of AI-generated posts (TR14). Content must come from real team input — no invented results.",
    hook="We asked our team: what's one thing 2026 taught you about building for clients?",
    alt_hooks=["3 lessons from a year of building websites, apps and AI tools.", "What 2026 taught our team."],
    caption="""We asked our team: what's one thing 2026 taught you about building for clients?

[Team member 1, role]: "[Lesson — in their words]"

[Team member 2, role]: "[Lesson — in their words]"

[Team member 3, role]: "[Lesson — in their words]"

Our own takeaway: the best projects start with the clearest conversations.

What did 2026 teach you about your business?""",
    cta="Comment your 2026 lesson",
    hashtags="#Leadership #WebDevelopment #ApexWebStudios",
    format="Document carousel (PDF)",
    script=[
        "Cover: What 2026 taught our team | Lessons from a year of building",
        "Page 2: [Team member 1 photo + quote]",
        "Page 3: [Team member 2 photo + quote]",
        "Page 4: [Team member 3 photo + quote]",
        "Page 5: Our takeaway: the best projects start with the clearest conversations.",
        "Page 6 (CTA): Here's to building in 2027 — apexwebstudios.net",
    ],
    visual="Portrait photo per page (team, with consent) on black; quote in white; name/role in IBM Plex Mono red.",
    brief_summary="6-page team reflections PDF.",
    kpi="Comments ≥ 5; engagement rate ≥ page's Nov average",
    alt_text="Cover slide: 'What 2026 taught our team — lessons from a year of building' on a black background.",
    shots=None,
    audio="N/A (document)",
    client_input="Three real team quotes, names, roles, photos and consent.",
)

post(
    date="2026-12-30", time="12:00", platform="Instagram + Facebook (cross-post)", pillar="Offers & Packages", objective="Leads",
    funnel="Conversion", persona="P1, P2",
    topic="Plan your 2027 build — book a free call in the first week of January",
    rationale="Free call is Apex's primary offer (B01); new-year budget window (TR16, hypothesis). Closes the month's funnel after the checklist (Dec 22) and package posts (Dec 9, Dec 18).",
    hook="New year. Same website? 👀",
    alt_hooks=["Your 2027 website starts with one free call.", "Make January the month your website finally gets fixed."],
    caption="""New year. Same website? 👀

If your site didn't pull its weight in 2026, January is the time to fix it.

Book a free call and we'll:
→ Look at your current site (or your idea)
→ Tell you honestly what it needs — and what it doesn't
→ Show you which package fits, with the price up front

No confusing proposals. No lengthy contracts. No hidden costs.

Tap the link in bio to grab a January slot.""",
    cta="Book a free call — link in bio",
    hashtags="#SmallBusinessWebsite #WebDesign #NewYearNewWebsite #SmallBusinessOwner #ApexWebStudios",
    format="Reel",
    script=[
        ("0-3s", "Old laptop with a dated-looking demo site; party popper goes off", "New year. Same website? 👀", "New year. Same website?", "Light licensed track"),
        ("3-12s", "Team member to camera", "January = fix it", "If your website didn't pull its weight this year, January's the time to fix it.", "—"),
        ("12-26s", "B-roll: video call, screen share of site review (Apex demo)", "Free call: honest look · what it needs · price up front", "Book a free call — we'll look at your site, tell you honestly what it needs, and show you the price up front.", "—"),
        ("26-34s", "Text-only frame", "No confusing proposals. No lengthy contracts. No hidden costs.", "No confusing proposals. No lengthy contracts. No hidden costs.", "—"),
        ("34-40s", "End card", "Book a January slot — link in bio", "Grab a January slot — link in bio.", "Fade"),
    ],
    visual="Before: an obviously dated demo site (Apex-made mock, not a real business). After: modern Apex demo. Red/black end card.",
    brief_summary="40 s new-year free-call Reel.",
    kpi="Link-in-bio clicks ≥ 20; ≥ 3 free-call bookings attributed",
    alt_text="Video: a dated website on an old laptop, then an Apex team member inviting viewers to book a free call, ending with the text 'No confusing proposals. No lengthy contracts. No hidden costs.'",
    shots=["Dated demo site mock (made by Apex)", "Team member talking head", "Video-call B-roll with dummy data", "End card"],
    audio="Licensed in-app track; burned-in captions.",
    client_input="Confirm January call availability.",
)

# ---------------------------------------------------------------- build
P.sort(key=lambda p: (p["date"], p["time"]))
for i, p in enumerate(P, 1):
    p["cb"] = f"CB-{MONTH}-{i:02d}"


def script_text(p):
    s = p["script"]
    if isinstance(s, str):
        return s
    if s and isinstance(s[0], tuple):
        return " | ".join(f"[{t}] VISUAL: {v} / ON-SCREEN: {o} / VO: {vo} / AUDIO: {a}" for t, v, o, vo, a in s)
    return " | ".join(s)

HEADER = ["Date", "Platform", "Content Pillar", "Objective", "Topic", "Research Rationale", "Hook", "Caption", "CTA",
          "Hashtags", "Format", "Reel Script / Carousel Slide Copy", "Visual Direction", "Creative Brief", "KPI Objective", "Approval Status"]

os.makedirs(f"{ROOT}/03_calendar", exist_ok=True)
with open(f"{ROOT}/03_calendar/{SLUG}_calendar_{MONTH}_v1.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(HEADER)
    for p in P:
        w.writerow([f"{p['date']} {p['time']} {TZ}", p["platform"], p["pillar"], p["objective"], p["topic"], p["rationale"],
                    p["hook"], p["caption"], p["cta"], p["hashtags"], p["format"], script_text(p), p["visual"],
                    f"{p['cb']} — {p['brief_summary']}", p["kpi"], "Pending Review"])

# ---------------------------------------------------------------- content doc
from collections import Counter
pill = Counter(p["pillar"] for p in P)
plat = Counter("LinkedIn" if p["platform"] == "LinkedIn" else "Instagram + Facebook" for p in P)
fmt = Counter(p["format"] for p in P)
n = len(P)
L = []
L.append(f"# Apex Web Studios — Content for December 2026 (v1)\n")
L.append(f"- **Status:** all {n} posts **Pending Review**. Nothing is scheduled or published.")
L.append(f"- **Time zone:** {TZ}. Posting times are test hypotheses based on Buffer studies (T25, T26).")
L.append("- **Source IDs** refer to `01_research/sources.md`. Trend IDs (TR#) refer to `01_research/trends_2026-12.md`.")
L.append("- Posts marked **Needs client input** contain `[bracketed]` placeholders or need permissions. They cannot be approved until the operator supplies them.\n")
L.append("## Calendar overview\n")
L.append("| Pillar | Posts | Share | Strategy target |\n|---|---|---|---|")
targets = {"Build Smarter (Educate)": "40%", "Proof & Results": "15%", "Behind the Build": "20%", "Offers & Packages": "15%", "Community & Moments": "10%"}
for k, t in targets.items():
    L.append(f"| {k} | {pill[k]} | {pill[k]*100/n:.0f}% | {t} |")
L.append("")
L.append("| Platform | Posts |\n|---|---|")
for k, v in plat.items():
    L.append(f"| {k} | {v} |")
L.append("")
L.append("| Format | Posts |\n|---|---|")
for k, v in fmt.items():
    L.append(f"| {k} | {v} |")
L.append("""
**Key dates and trends covered**
- Post-Cyber Monday check (Dec 1, T53)
- International Day of Persons with Disabilities (Dec 3, T56; T45)
- Hanukkah (Dec 4, T57)
- AI search and Google AI Mode (Dec 8, Dec 10; T34, T35, T37, T38)
- AI builders vs agency (Dec 15, T49, T50)
- Holidays (Dec 24)
- 2027 planning (Dec 22, Dec 29, Dec 30)

| # | Date | Platform | Pillar | Format | Topic | Brief |
|---|---|---|---|---|---|---|""")
for i, p in enumerate(P, 1):
    L.append(f"| {i} | {p['date']} {p['time']} | {p['platform']} | {p['pillar']} | {p['format']} | {p['topic']} | {p['cb']} |")
L.append("\n---\n")

for i, p in enumerate(P, 1):
    L.append(f"## {i}. {p['date']} {p['time']} ET — {p['platform']} — {p['format']}\n")
    if p.get("client_input"):
        L.append(f"> **Needs client input:** {p['client_input']}\n")
    L.append(f"- **Topic:** {p['topic']}")
    L.append(f"- **Pillar / Objective / Funnel:** {p['pillar']} / {p['objective']} / {p['funnel']}")
    L.append(f"- **Persona:** {p['persona']}")
    L.append(f"- **Research rationale:** {p['rationale']}")
    L.append(f"- **KPI:** {p['kpi']}")
    L.append(f"- **Creative brief:** {p['cb']} — {p['brief_summary']}")
    L.append(f"- **Approval status:** Pending Review\n")
    L.append("**Hooks**")
    L.append(f"- Primary: {p['hook']}")
    for a in p["alt_hooks"]:
        L.append(f"- Alternate: {a}")
    L.append("\n**Caption**\n")
    L.append("```text\n" + p["caption"] + "\n```\n")
    L.append(f"**CTA:** {p['cta']}  ")
    L.append(f"**Hashtags:** {p['hashtags']}\n")
    s = p["script"]
    if isinstance(s, list) and s and isinstance(s[0], tuple):
        L.append("**Reel / video script**\n")
        L.append("| Time | Shot / visual | On-screen text | Voiceover / dialogue | Audio |\n|---|---|---|---|---|")
        for t, v, o, vo, a in s:
            L.append(f"| {t} | {v} | {o} | {vo} | {a} |")
        L.append("\n*Subtitles:* burned-in captions for the full VO, plus an uploaded caption file where the platform supports it.\n")
    elif isinstance(s, list):
        L.append("**Slide copy**\n")
        for j, sl in enumerate(s, 1):
            L.append(f"{j}. {sl}")
        L.append("")
    else:
        L.append("**Script / slides:** N/A (single-image format)\n")
    L.append(f"**Visual direction:** {p['visual']}  ")
    L.append(f"**Alt text:** {p['alt_text']}\n")
    L.append("---\n")

os.makedirs(f"{ROOT}/04_content", exist_ok=True)
open(f"{ROOT}/04_content/{SLUG}_content_{MONTH}_v1.md", "w", encoding="utf-8").write("\n".join(L))

# ---------------------------------------------------------------- briefs
B = [f"# Apex Web Studios — Creative Briefs, December 2026 (v1)\n",
     "**For:** designers and video editors.",
     "**Reviewer:** the operator (Apex marketing team).",
     "**Deadline rule:** final assets are due **3 business days before** each publish date, for review.",
     "**Canva:** no brand kit or template link yet (brief Q10). Build from the brand system below.\n",
     "## Shared brand system\n",
     "**Do**"] + [f"- {d}" for d in BRAND_DO] + ["\n**Don't**"] + [f"- {d}" for d in BRAND_DONT] + [
     "\n**Accessibility (all assets)**",
     "- Burned-in captions on all video.",
     "- Alt text supplied (see each brief).",
     "- Text contrast of at least 4.5:1.",
     "- No information conveyed by colour alone.",
     "\n---\n"]

from datetime import date, timedelta
def due(d):
    y, m, dd = map(int, d.split("-")); x = date(y, m, dd); k = 0
    while k < 3:
        x -= timedelta(days=1)
        if x.weekday() < 5: k += 1
    return x.isoformat()

for p in P:
    fk = p["format"]
    B.append(f"## {p['cb']} — {p['topic']}\n")
    B.append(f"- **Post:** {p['date']} {p['time']} ET · {p['platform']} · {fk}")
    B.append(f"- **Objective / KPI:** {p['objective']} — {p['kpi']}")
    B.append(f"- **Deliverable specs:** {SPECS[fk]}")
    B.append(f"- **Key message / hook:** {p['hook']}")
    B.append(f"- **Deadline:** {due(p['date'])} (for review) · **Reviewer:** Operator (Apex marketing)")
    if p.get("client_input"):
        B.append(f"- **Blocked until:** {p['client_input']}")
    s = p["script"]
    if isinstance(s, list) and s and isinstance(s[0], tuple):
        B.append("\n**On-screen copy & script**\n")
        B.append("| Time | Shot / visual | On-screen text | VO | Audio |\n|---|---|---|---|---|")
        for t, v, o, vo, a in s:
            B.append(f"| {t} | {v} | {o} | {vo} | {a} |")
    elif isinstance(s, list):
        B.append("\n**Slide / page copy**\n")
        for j, sl in enumerate(s, 1):
            B.append(f"{j}. {sl}")
    else:
        B.append("\n**Copy on image:** headline = hook (shortened if needed) + logo.")
    B.append(f"\n**Visual direction:** {p['visual']}")
    B.append("**Palette:** #0A0A0A, #1A1A1A, #383838, #F0F0F0, #FFFFFF, accent #D23030 (logo red #FF0000).")
    B.append("**Typography:** Urbanist (headlines), Inter (body), IBM Plex Mono (numbers and labels).")
    if p.get("shots"):
        B.append("\n**Shot list:** " + "; ".join(p["shots"]))
    B.append(f"\n**Audio:** {p['audio']}")
    B.append(f"\n**Alt text:** {p['alt_text']}")
    B.append("\n---\n")

os.makedirs(f"{ROOT}/05_creative_briefs", exist_ok=True)
open(f"{ROOT}/05_creative_briefs/{SLUG}_briefs_{MONTH}_v1.md", "w", encoding="utf-8").write("\n".join(B))
print(n, dict(pill), dict(plat))
