"""Apex Web Studios — December 2026 post data (v2, final). Single source of truth for all deliverables.
Only verified client facts (B-sources) and verified research (T-sources, see 01_research/sources.md) are used.
"""

SITE = "https://apexwebstudios.net"

def utm(platform, slug, path="/contact-us"):
    return f"{SITE}{path}?utm_source={platform}&utm_medium=organic_social&utm_campaign=2026-12_{slug}"

POSTS = [
dict(
    id="P01", date="2026-12-01", day="Tue", time="16:00", platform="LinkedIn", tier="Core (Lite + Standard)",
    pillar="Build Smarter (Educate)", series="Plain-English Web", objective="Engagement", funnel="Awareness", persona="P1 Local Service Owner; P3 Growing SMB Marketing Lead",
    format="Document carousel (PDF)",
    topic="Post-Cyber Monday website health check: 6 things to review before the December peak",
    rationale="Adobe forecast $15.1B in US online spending on Cyber Monday (Nov 30) and $275.1B for the Nov 1–Dec 31 season (T53, verified). December is still ahead for SMB sites. LinkedIn PDF carousels had the highest median engagement of any LinkedIn format in Buffer's 2026 study (21.77%, T21, verified).",
    sources=["T53", "T21"],
    hook="Your website just had its biggest weekend of the year. Did it pass?",
    alt_hooks=["Cyber Monday is over. December traffic isn't.", "6 checks to run on your website before the holiday peak."],
    caption="""Your website just had its biggest weekend of the year. Did it pass?

Adobe forecast $15.1B in US online spending on Cyber Monday alone, and $275.1B for the full holiday season (Nov 1 – Dec 31). December is still ahead.

Here's the 15-minute check we'd run on any small-business site this week:

1. Load your homepage on mobile data, not office Wi-Fi
2. Submit your own contact form and confirm the email arrives
3. Click every link in your holiday promotion
4. Make sure your hours match on your website and your Google Business Profile
5. Walk through checkout or booking as a first-time visitor
6. Tap your phone number on mobile. Does it dial?

Swipe for what to look for at each step.

Which one are you checking first?

Source: Adobe holiday forecast, Sept 28, 2026.""",
    cta="Comment which check you'll run first. Free-call link in the first comment.",
    first_comment="Want a second pair of eyes on your site before the holidays? Book a free call: " + utm("linkedin", "holiday-check"),
    hashtags="#SmallBusiness #WebDevelopment #ApexWebStudios",
    slides=[
        ("Cover", "Your website just had its biggest weekend of the year.", "Did it pass? 6 checks · 15 minutes"),
        ("Context", "December is still ahead.", "Adobe forecast $15.1B on Cyber Monday and $275.1B for the US holiday season (Nov 1–Dec 31). Source: Adobe, Sept 28, 2026."),
        ("Check 1", "Test on mobile data", "Not office Wi-Fi. If a page feels slow to you, it feels slower to a customer in a parking lot."),
        ("Check 2", "Submit your own form", "Does the email arrive? Does the thank-you page load? Check spam too."),
        ("Check 3", "Click every promo link", "Holiday banners, buttons and discount links. Broken links cost the most in December."),
        ("Check 4", "Match your hours everywhere", "Website and Google Business Profile should say the same thing, including holiday closures."),
        ("Check 5", "Walk your checkout or booking", "Go through it as a first-time visitor. Where would you hesitate?"),
        ("Check 6", "Tap to call", "Your phone number should dial with one tap on mobile."),
        ("CTA", "Want a second pair of eyes?", "Book a free call with Apex Web Studios · apexwebstudios.net"),
    ],
    visual="Black (#0A0A0A) pages; large red (#D23030) step numbers in IBM Plex Mono; white Urbanist headlines; simple phone-frame line illustrations (no third-party sites).",
    alt_text="Cover slide on a black background reading 'Your website just had its biggest weekend of the year. Did it pass?' with a red label '6 checks · 15 minutes'.",
    story="LinkedIn: n/a. Optional Instagram Story the same day: poll sticker 'Did your website get more traffic this weekend? Yes / Not sure', then a link sticker to the free-call page.",
    kpi="Engagement rate at or above the page's November average +10%; 5 or more link clicks from the first comment",
    readiness="Ready for review",
    client_input="",
),
dict(
    id="P02", date="2026-12-02", day="Wed", time="12:00", platform="Instagram + Facebook (cross-post)", tier="Standard",
    pillar="Behind the Build", series="Inside Apex", objective="Engagement", funnel="Consideration", persona="P1; P2 Startup Founder",
    format="Reel",
    topic="The 5 stages every Apex website goes through (from discovery to launch and beyond)",
    rationale="Apex's own web design page lists a 5-stage process: Product Discovery, Experience Design, Engineering & Development, Testing & Optimization, Release & Maintenance (B03, verified). Starter, Growth and Professional Business packages state first concepts within 48 hours (B04, verified). Instagram now restricts recommendations for accounts that repost others' content, so original footage is favoured (T03, verified).",
    sources=["B03", "B04", "T03"],
    hook="Most people only see the launch. Here's everything that happens before it.",
    alt_hooks=["What actually happens after you hire a web agency?", "5 stages. 1 website. The inside view."],
    caption="""Most people only see the launch. Here's everything that happens before it. 👀

Every website we build moves through 5 stages:

1️⃣ Product Discovery: your business, your customers, your goals
2️⃣ Experience Design: layouts and user journeys
3️⃣ Engineering & Development: the actual build
4️⃣ Testing & Optimization: checking it works everywhere
5️⃣ Release & Maintenance: launch, and what comes after

On our Starter, Growth and Professional Business packages, your first design concepts arrive within 48 hours.

Planning a new site for 2027? Tap the link in bio to book a free call.""",
    cta="Book a free call via the link in bio",
    first_comment="",
    link=utm("instagram", "inside-apex-process"),
    hashtags="#WebDesign #WebDevelopment #SmallBusinessWebsite #BehindTheScenes #ApexWebStudios",
    script=[
        ("0–3s", "Fast push-in on a laptop showing a live (Apex demo) website", "Most people only see the launch.", "Most people only see the launch. Here's everything before it.", "Licensed upbeat track from Instagram's library, low under VO"),
        ("3–9s", "Team member with notebook on a discovery video call (dummy client name)", "1 · Product Discovery", "Stage one: discovery. We learn your business, your customers and your goals.", "—"),
        ("9–15s", "Designer arranging wireframes in Figma (non-client file)", "2 · Experience Design", "Stage two: experience design: layouts and user journeys.", "—"),
        ("15–21s", "Developer's screen with code editor and browser preview", "3 · Engineering & Development", "Stage three: the build itself.", "Tempo lift"),
        ("21–27s", "Same page checked on phone, tablet and laptop side by side", "4 · Testing & Optimization", "Stage four: testing, so it works on every screen.", "—"),
        ("27–33s", "'Launch' click, then the live demo site on a phone", "5 · Release & Maintenance", "Stage five: launch, and the support that comes after.", "Hit on launch"),
        ("33–40s", "End card: logo on black, red underline", "First concepts in 48 hrs* · Book a free call: link in bio", "On our Starter, Growth and Professional packages, first concepts arrive within 48 hours. Book a free call.", "Fade"),
    ],
    end_note="*On-screen footnote: 'Starter, Growth & Professional Business packages'",
    visual="Real Apex team and screens only. Use Apex's own website or a purpose-made demo, never client work without written permission. Warm natural light; dark UI overlays; stage numbers as red IBM Plex Mono counters.",
    alt_text="Video: Apex team members move through five stages of building a website (discovery call, wireframes, coding, multi-device testing, launch), each labelled on screen, ending with the Apex logo.",
    story="Story: quiz sticker 'Which stage takes the longest?' (Discovery / Design / Build / Testing). Reveal the answer the next day from the team's real experience.",
    kpi="Shares and saves at 2% or more of reach; 2 or more DMs",
    readiness="Blocked: client input",
    client_input="Name 1–3 team members willing to appear on camera (written consent). Confirm the one-line description of each stage matches how Apex actually works.",
),
dict(
    id="P03", date="2026-12-03", day="Thu", time="09:00", platform="Instagram + Facebook (cross-post)", tier="Core (Lite + Standard)",
    pillar="Build Smarter (Educate)", series="60-Second Site Check", objective="Awareness", funnel="Awareness", persona="P1",
    format="Reel",
    topic="International Day of Persons with Disabilities: 3 accessibility checks any owner can do in 60 seconds",
    rationale="The UN observes the International Day of Persons with Disabilities on 3 December 2026, theme 'The CRPD at 20: Building on Progress, Advancing the Future' (T56, verified). Apex lists 'WCAG Compliance & Accessibility Standards' on its UI/UX page (B03, verified), so this is a real service, not borrowed authority.",
    sources=["T56", "B03"],
    hook="Unplug your mouse. Can you still use your own website?",
    alt_hooks=["3 accessibility checks you can do in 60 seconds.", "Can everyone actually use your website?"],
    caption="""Unplug your mouse. Can you still use your own website? 🖱️

Today is the International Day of Persons with Disabilities. Here are 3 checks any business owner can do in 60 seconds:

1️⃣ Keyboard test: press Tab. Can you always see where you are on the page?
2️⃣ Image check: do your important images have alt text describing what they show?
3️⃣ Contrast check: is any text light grey on white? If it's hard for you to read, it's harder for others.

These catch common issues. They're a starting point, not a full audit.

Our design team works to WCAG accessibility standards. Want a hand? Send us a DM.

Save this and run the checks this week.""",
    cta="Save this post. DM us for help with accessibility.",
    first_comment="",
    link=utm("instagram", "idpd-accessibility"),
    hashtags="#WebAccessibility #IDPD2026 #InclusiveDesign #SmallBusinessWebsite #ApexWebStudios",
    script=[
        ("0–3s", "Hand slides a mouse off the desk", "Unplug your mouse.", "Unplug your mouse. Can you still use your own website?", "Calm licensed instrumental"),
        ("3–8s", "Title card on black", "Dec 3 · International Day of Persons with Disabilities · 3 checks in 60 seconds", "It's the International Day of Persons with Disabilities. Three checks, sixty seconds.", "—"),
        ("8–22s", "Screen recording: pressing Tab through an Apex demo page; focus outline visible vs. missing (split screen)", "1 · Press Tab. Can you see where you are?", "One: press Tab. If you can't see where you are, keyboard users can't either.", "—"),
        ("22–34s", "Screen recording: image alt-text field in a CMS", "2 · Do key images have alt text?", "Two: give your important images alt text that describes what they show.", "—"),
        ("34–46s", "Split screen: light-grey text on white vs. dark text on white", "3 · Is your text easy to read?", "Three: if any text is light grey on white, fix the contrast.", "—"),
        ("46–55s", "Apex team member to camera", "A starting point, not a full audit.", "These catch common issues. They're not a full audit. We design to WCAG standards. DM us if you'd like help.", "—"),
        ("55–60s", "End card", "Save this · DM us · apexwebstudios.net", "Save this and try it this week.", "Fade"),
    ],
    visual="Screen recordings on an Apex demo page only (never a third-party site). Captions white on black, large type. This post must itself be accessible: full burned-in captions and no flashing.",
    alt_text="Video: a hand pushes a mouse aside, then screen recordings show keyboard focus outlines, an image alt-text field and a text-contrast comparison, with captions listing three accessibility checks.",
    story="Story: poll 'Did your site pass the Tab test? ✅ Yes / ❌ Not yet', with a link sticker to the free-call page for 'Not yet' voters (reply to each voter by DM).",
    kpi="Saves at 3% or more of reach; non-follower reach at 50% or more (publish as a Trial Reel first to test the hook)",
    readiness="Ready for review",
    client_input="",
),
dict(
    id="P04", date="2026-12-03", day="Thu", time="16:00", platform="LinkedIn", tier="Core (Lite + Standard)",
    pillar="Build Smarter (Educate)", series="Plain-English Web", objective="Engagement", funnel="Awareness", persona="P1; P3",
    format="Document carousel (PDF)",
    topic="IDPD: 5 accessibility fixes that make a website better for every visitor",
    rationale="IDPD on 3 Dec 2026 (T56, verified). Seyfarth Shaw: 'Plaintiffs filed 3,117 website accessibility lawsuits in federal court in 2025 – a 27% increase from 2024' (T46, verified, US federal courts only). Apex offers WCAG-standard design (B03, verified).",
    sources=["T56", "T46", "B03"],
    hook="If someone can't use a mouse, can they still contact your business?",
    alt_hooks=["Accessibility isn't a feature. It's whether people can use your website at all.", "5 accessibility fixes that help every visitor."],
    caption="""If someone can't use a mouse, can they still contact your business?

Today is the UN's International Day of Persons with Disabilities. It's a good day to look at your website through a different lens.

It's also a business risk. Seyfarth Shaw reports that 3,117 website accessibility lawsuits were filed in US federal court in 2025, a 27% increase from 2024.

5 fixes that help every visitor:
→ Visible keyboard focus on every link and button
→ Descriptive alt text on meaningful images
→ Strong contrast between text and background
→ Captions on every video with speech
→ Clear form labels and plain-language error messages

Our team designs to WCAG accessibility standards. If you'd like a second look at your site, send us a message.

General information only, not legal advice.""",
    cta="Send Apex a message for an accessibility conversation",
    first_comment="Source: Seyfarth Shaw, ADA Title III blog (Mar 2026): https://www.adatitleiii.com/2026/03/federal-court-website-accessibility-lawsuit-filings-bounce-back-in-2025/ · Talk to our team: " + utm("linkedin", "idpd-accessibility"),
    hashtags="#WebAccessibility #InclusiveDesign #ApexWebStudios",
    slides=[
        ("Cover", "If someone can't use a mouse, can they still contact your business?", "5 accessibility fixes · Dec 3 · International Day of Persons with Disabilities"),
        ("Why now", "3,117 website accessibility lawsuits", "were filed in US federal court in 2025, up 27% from 2024. Source: Seyfarth Shaw, Mar 2026."),
        ("Fix 1", "Visible keyboard focus", "Every link and button should show where you are when using Tab."),
        ("Fix 2", "Meaningful alt text", "Describe what the image shows and why it matters. Skip 'image1.jpg'."),
        ("Fix 3", "Strong contrast", "Light grey on white looks elegant and reads badly. Choose dark text on light backgrounds."),
        ("Fix 4", "Captions on video", "Every video with speech needs captions, burned in or closed."),
        ("Fix 5", "Clear forms", "Visible labels and plain-language error messages, not placeholder-only fields."),
        ("Note", "General information only.", "This is not legal advice. For compliance questions, speak to a qualified professional."),
        ("CTA", "Want a second look at your site?", "Message Apex Web Studios · apexwebstudios.net"),
    ],
    visual="Black pages, white type, one red icon per fix. The deck must itself be accessible: body text 24 px or larger and high contrast.",
    alt_text="Cover slide on black: 'If someone can't use a mouse, can they still contact your business?' with the subtitle '5 accessibility fixes, Dec 3, International Day of Persons with Disabilities'.",
    story="n/a (LinkedIn)",
    kpi="Engagement rate at or above the page's November average +10%; 3 or more inbound messages",
    readiness="Ready for review",
    client_input="",
),
dict(
    id="P05", date="2026-12-04", day="Fri", time="15:00", platform="Instagram + Facebook (cross-post)", tier="Standard",
    pillar="Community & Moments", series="Moments", objective="Community", funnel="Loyalty", persona="All",
    format="Static image",
    topic="Hanukkah greeting (begins at sundown, Fri Dec 4, 2026)",
    rationale="Hanukkah begins at sundown on Friday 4 December 2026 and ends at nightfall on Saturday 12 December 2026 (T57, verified). Posted before sundown. An inclusive seasonal moment for the Community pillar.",
    sources=["T57"],
    hook="Happy Hanukkah to everyone celebrating. 🕎",
    alt_hooks=["Wishing light and warmth this Hanukkah.", "To our clients and friends celebrating: Happy Hanukkah."],
    caption="""Happy Hanukkah to everyone celebrating. 🕎

Wishing you, your families and your teams eight nights of light and warmth.

The Apex Web Studios team""",
    cta="None (goodwill post)",
    first_comment="",
    link="",
    hashtags="#HappyHanukkah #ApexWebStudios",
    copy_on_image=["Happy Hanukkah", "Apex Web Studios (small logo)"],
    visual="Minimal and respectful: black background, a row of eight softly glowing points of light with a warm gold glow, and 'Happy Hanukkah' in Urbanist. No novelty clip-art and no religious imagery beyond the lights.",
    alt_text="Black graphic with a row of eight softly glowing lights and the words 'Happy Hanukkah' from Apex Web Studios.",
    story="Share the post to Stories with no stickers.",
    kpi="Engagement rate at or above the account average; no negative sentiment",
    readiness="Ready for review",
    client_input="",
),
dict(
    id="P06", date="2026-12-08", day="Tue", time="16:00", platform="LinkedIn", tier="Core (Lite + Standard)",
    pillar="Build Smarter (Educate)", series="Plain-English AI", objective="Engagement", funnel="Awareness", persona="P1; P3",
    format="Text post + image",
    topic="Is AI search killing website traffic? What the 2026 data actually shows",
    rationale="Ahrefs: 'the presence of an AI Overview now correlates with a 58% lower average clickthrough rate for the top-ranking page' (T34, Feb 2026, Dec 2025 data, verified). Seer Interactive: 'AIO organic click-through rates rebound 85% in the first two months of 2026' (T37, Apr 2026, verified). Presenting both is more credible than one-sided 'AI is killing clicks' content. Apex sells SEO and AI services (B03).",
    sources=["T34", "T37", "B03"],
    hook="Is AI search killing website traffic? The honest answer: it's complicated.",
    alt_hooks=["Two credible studies. Two different stories about AI search.", "Ranking #1 doesn't mean what it used to. But it still matters."],
    caption="""Is AI search killing website traffic? The honest answer: it's complicated.

Two credible data points from 2026:

📉 Ahrefs found that when an AI Overview appears, the top-ranking page's average click-through rate is 58% lower (December 2025 data; a correlation, not proof of cause).

📈 Seer Interactive found AI Overview click-through rates rebounded 85% in the first two months of 2026.

So the click isn't dead. It's harder to earn, and it goes to the clearest answer.

What we're doing for clients:
1. Service pages that answer real customer questions in plain language
2. Accurate business details everywhere (website, Google Business Profile, socials)
3. Clean page structure that search engines and AI tools can read

Nobody can promise you a spot in an AI answer. But you can make your website easier to understand.

What's the one question your customers always ask? That's your next page.""",
    cta="Comment with the question your customers ask most",
    first_comment="Sources: Ahrefs (Feb 2026) https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/ · Seer Interactive (Apr 2026) https://www.seerinteractive.com/news/search-engine-land-and-other-search-pubs-cite-seers-2026-ctr-research",
    hashtags="#AISearch #SEO #ApexWebStudios",
    copy_on_image=["Is AI search killing website traffic?", "📉 −58% top-result CTR when an AI Overview appears (Ahrefs, Dec 2025 data)", "📈 +85% AI Overview CTR rebound, Jan–Feb 2026 (Seer Interactive)", "The click isn't dead. It goes to the clearest answer."],
    visual="Single 1080×1350 image: black background, two large IBM Plex Mono figures (−58% in grey, +85% in red), each with a small source line, and the closing line in white Urbanist.",
    alt_text="Graphic asking 'Is AI search killing website traffic?' with two data points: 58% lower top-result click-through when an AI Overview appears (Ahrefs) and an 85% rebound in AI Overview click-through in early 2026 (Seer Interactive).",
    story="n/a (LinkedIn)",
    kpi="5 or more comments; engagement rate at or above the page's November average",
    readiness="Ready for review",
    client_input="",
),
dict(
    id="P07", date="2026-12-09", day="Wed", time="12:00", platform="Instagram + Facebook (cross-post)", tier="Standard",
    pillar="Proof & Results", series="In Their Words", objective="Engagement", funnel="Consideration", persona="P1",
    format="Carousel",
    topic="Three client reviews, word for word",
    rationale="These quotes are confirmed verbatim on apexwebstudios.net/testimonials (B08, re-checked 2026-11-07). Reviews praise communication and responsiveness, which answers the 'agency radio silence' objection that Apex itself addresses ('No surprises. No radio silence.', B02).",
    sources=["B08", "B02"],
    hook="We could tell you we're easy to work with. We'd rather our clients did.",
    alt_hooks=["3 reviews. Zero edits.", "What clients say when we're not in the room."],
    caption="""We could tell you we're easy to work with. We'd rather our clients did. 💬

Swipe for three reviews in their own words, from Body Rituals Spa, UpkeepX and Copy Smart.

The thing we hear most isn't about code. It's about communication: being reachable, responsive and actually listening.

Thank you to every client who took the time to leave a review this year. 🖤

Read more reviews via the link in bio.""",
    cta="Read more reviews via the link in bio (/testimonials)",
    first_comment="",
    link=utm("instagram", "reviews", "/testimonials"),
    hashtags="#ClientLove #WebDesign #SmallBusinessWebsite #Testimonials #ApexWebStudios",
    slides=[
        ("Cover", "We could tell you we're easy to work with.", "We'd rather our clients did. →"),
        ("Quote 1", "“The website not only looks beautiful, but it's also intuitive and easy to navigate, which is exactly what we wanted.”", "Body Rituals Spa"),
        ("Quote 2", "“I am most impressed by how proactive and responsive they are.”", "Business Owner, UpkeepX"),
        ("Quote 3", "“Apex Web Studios is at the top of their game.”", "Owner, Copy Smart"),
        ("CTA", "Read more reviews", "apexwebstudios.net/testimonials · Book a free call via the link in bio"),
    ],
    visual="Large red quotation marks; quotes in white Inter on black; attribution in IBM Plex Mono light grey. No client logos unless the client grants permission.",
    alt_text="Carousel of client quotes in white text on black from Body Rituals Spa, UpkeepX and Copy Smart describing working with Apex Web Studios.",
    story="Story: share slide 2 with a 'Read more' link sticker to /testimonials.",
    kpi="Profile visits at 1.5% or more of reach; saves plus shares at 1% or more",
    readiness="Blocked: client input",
    client_input="Written permission from Body Rituals Spa, UpkeepX and Copy Smart to feature their reviews and names on social media.",
),
dict(
    id="P08", date="2026-12-10", day="Thu", time="16:00", platform="LinkedIn", tier="Core (Lite + Standard)",
    pillar="Offers & Packages", series="Price Tag, Explained", objective="Leads", funnel="Conversion", persona="P1; P3",
    format="Document carousel (PDF)",
    topic="$599 to $7,999: what each Apex website package actually includes",
    rationale="Apex publishes full package prices and inclusions (B04, verified 2026-11-07), which is unusual in the category and supports the brand's 'No Hidden Cost' promise (B01). Price is a known objection in public reviews ('Pricing is a little steep for me compared to others', B08).",
    sources=["B04", "B01", "B08"],
    hook="“How much does a website cost?” Here's our actual price list.",
    alt_hooks=["We publish our prices. Here's exactly what each one buys.", "Website pricing, without the sales call."],
    caption="""“How much does a website cost?”

“It depends” frustrates everyone. So here's our actual price list and what each package includes:

• Starter: $599. 3-page custom website, mobile-responsive, contact form, CMS
• Growth: $1,199. 5-page custom website, 3 custom banners, CMS
• Professional Business: $1,999. Up to 10 pages, SEO-friendly structure, unlimited revisions
• Corporate Elite: $3,199. Up to 15 pages, lead capture, optional booking and ordering
• E-commerce Growth: $4,999. Custom store, up to 200 products, payment gateway integration
• Platinum Enterprise: $7,999. Up to 20 pages, advanced CMS, a dedicated team

Starter, Growth and Professional Business include first design concepts within 48 hours.

USD, one-time. CAD and GBP pricing is on our website.

Not sure which fits? Book a free call and we'll tell you honestly, even if it's the smallest one.""",
    cta="Book a free call (link in the first comment)",
    first_comment="Full package details: " + utm("linkedin", "price-list", "/pricing") + " · Book a free call: " + utm("linkedin", "price-list"),
    hashtags="#WebDevelopment #SmallBusiness #ApexWebStudios",
    slides=[
        ("Cover", "“How much does a website cost?”", "Our actual price list →"),
        ("Starter · $599", "3-page custom website", "Mobile-responsive · contact form · CMS · first concepts within 48 hours · dedicated project manager"),
        ("Growth · $1,199", "5-page custom website", "3 custom banners · CMS · first concepts within 48 hours · dedicated project manager"),
        ("Professional Business · $1,999", "Up to 10 pages", "SEO-friendly structure · CMS/admin panel · unlimited revisions · first concepts within 48 hours"),
        ("Corporate Elite · $3,199", "Up to 15 pages", "Lead capture and newsletter · optional booking, ordering and payments · dedicated project manager"),
        ("E-commerce Growth · $4,999", "Custom online store", "Up to 200 products · secure cart · payment gateway integration · dedicated project manager"),
        ("Platinum Enterprise · $7,999", "Up to 20 pages", "Advanced CMS · complex architecture · dedicated team of designers and developers"),
        ("Small print", "USD, one-time.", "CAD and GBP pricing at apexwebstudios.net/pricing. Prices as published in December 2026."),
        ("CTA", "Not sure which fits?", "Book a free call. We'll tell you honestly. apexwebstudios.net"),
    ],
    visual="One package per page; price in large red IBM Plex Mono; 3–5 white bullet inclusions; consistent grid; small 'Prices as published Dec 2026' footer on every page.",
    alt_text="Cover slide: '\"How much does a website cost?\" Our actual price list' in white on black with a red arrow.",
    story="n/a (LinkedIn)",
    kpi="10 or more link clicks to /pricing or /contact-us; 2 or more attributed inquiries",
    readiness="Ready for review (confirm prices are unchanged on publish day)",
    client_input="Confirm on the day of publishing that the prices on /pricing are unchanged.",
),
dict(
    id="P09", date="2026-12-11", day="Fri", time="12:00", platform="Instagram + Facebook (cross-post)", tier="Standard",
    pillar="Build Smarter (Educate)", series="60-Second Site Check", objective="Awareness", funnel="Awareness", persona="P1; P3",
    format="Reel",
    topic="Your Instagram is part of your SEO: 4 quick fixes",
    rationale="Hootsuite's 2026 trends report: 'Google has started indexing public Instagram content' and 'Social media content must adapt to multi-modal discovery' (T31, verified). Hootsuite: 'Social has become a search engine, not just a feed' (T32, verified). Apex sells both SEO and social media marketing (B04).",
    sources=["T31", "T32", "B04"],
    hook="Your next customer might find your Instagram post on Google.",
    alt_hooks=["Your Instagram is part of your SEO now.", "4 Instagram fixes that help people find you."],
    caption="""Your next customer might find your Instagram post on Google. 🔎

Hootsuite's 2026 trends report notes that Google has started indexing public Instagram content. Social is becoming a search engine.

4 quick fixes:
1️⃣ Put what you do and where in the first line of your caption ('Website design for Milton small businesses', not 'Big news!!')
2️⃣ Add on-screen text that says the same thing
3️⃣ Write alt text for your images (Advanced settings → Accessibility)
4️⃣ Make your name, bio and website link match your Google Business Profile

Small changes, findable posts.

Need help making your website and socials work together? Link in bio.""",
    cta="Save this post. Link in bio for help.",
    first_comment="",
    link=utm("instagram", "social-seo"),
    hashtags="#SocialSEO #InstagramTips #SmallBusinessTips #LocalSEO #ApexWebStudios",
    script=[
        ("0–3s", "Phone showing a Google results page with an Instagram post among the results (Apex's own post, mocked)", "Found on Google 👀", "Your next customer might find your Instagram post on Google.", "Light licensed beat"),
        ("3–9s", "Apex team member to camera", "Social = search", "Hootsuite's 2026 trends report says Google has started indexing public Instagram content.", "—"),
        ("9–18s", "Screen: rewriting a caption's first line", "1 · Say what you do and where, first", "One: put what you do, and where, in your first line.", "—"),
        ("18–26s", "Screen: adding a text overlay in the Reels editor", "2 · Match it with on-screen text", "Two: add on-screen text that says the same thing.", "—"),
        ("26–34s", "Screen: Advanced settings → Accessibility → alt text", "3 · Write alt text", "Three: write alt text for your images.", "—"),
        ("34–42s", "Side by side: Instagram bio and Google Business Profile", "4 · Make your name, bio and link match", "Four: make your name, bio and link match your Google profile.", "—"),
        ("42–45s", "End card", "Save this · Link in bio", "Save this one.", "Fade"),
    ],
    visual="All screens show Apex's own accounts or dummy accounts (no third-party businesses). Captions on throughout; red highlight boxes on the fields being edited.",
    alt_text="Video: a phone shows an Instagram post in Google search results, then screen recordings show a caption rewrite, an on-screen text overlay, the alt-text setting and matching bio and Google profile details.",
    story="Story: quiz 'Can Instagram posts show up on Google?' (Yes / No), with the answer and a link to the Reel.",
    kpi="Saves at 2% or more of reach; non-follower reach at 50% or more",
    readiness="Ready for review",
    client_input="",
),
dict(
    id="P10", date="2026-12-15", day="Tue", time="16:00", platform="LinkedIn", tier="Standard",
    pillar="Build Smarter (Educate)", series="Plain-English AI", objective="Engagement", funnel="Consideration", persona="P1; P2",
    format="Document carousel (PDF)",
    topic="AI website builder or agency? An honest guide to when each makes sense",
    rationale="AI website builders are mainstream. Squarespace promotes its 'Blueprint AI website builder' (T50, verified, updated Sept 2026). AI-built sites are a real alternative for Apex's Starter-tier buyers, and an honest comparison builds credibility. Apex's own AI Agent Development service (B03) shows it is pro-AI, not anti-AI.",
    sources=["T50", "B03", "B04"],
    hook="Sometimes an AI website builder is the right call. Here's when it isn't.",
    alt_hooks=["An agency telling you when NOT to hire an agency.", "AI builder vs. agency: the honest version."],
    caption="""Sometimes an AI website builder is the right call. Here's when it isn't.

AI builders are now mainstream. Squarespace, for example, offers a Blueprint AI builder that sets up a site from a description of your business. For some businesses, that's enough.

An AI builder probably makes sense if:
• You need a simple site live this week
• You're testing an idea before investing
• You're happy to maintain it yourself

An agency probably makes sense if:
• You need custom features like booking, portals or integrations
• Your site has to rank, convert and scale
• You'd rather spend your time running the business

We'd rather you choose the right tool than the wrong agency.

Which camp are you in for 2027?""",
    cta="Comment which camp you're in for 2027",
    first_comment="Weighing it up? Book a free, no-pressure call: " + utm("linkedin", "ai-builder-vs-agency"),
    hashtags="#AI #WebDevelopment #ApexWebStudios",
    slides=[
        ("Cover", "AI website builder or agency?", "An honest guide (from an agency)"),
        ("Context", "AI builders are mainstream.", "e.g. Squarespace's Blueprint AI builds a starting site from a short description of your business."),
        ("Choose an AI builder if…", "Speed and simplicity matter most", "You need a simple site this week · you're testing an idea · you'll maintain it yourself"),
        ("Choose an agency if…", "The website is a growth tool", "Custom features (booking, portals, integrations) · it must rank, convert and scale · you want your time back"),
        ("Ask yourself", "3 questions before you decide", "Who will update it? · What happens when you outgrow it? · Do you own the site and the code?"),
        ("Our take", "The right tool beats the wrong agency.", "We build custom sites and AI agents, so we're not anti-AI. We're pro-fit."),
        ("CTA", "Weighing it up for 2027?", "Book a free, no-pressure call · apexwebstudios.net"),
    ],
    visual="Two-column comparison pages (left grey 'AI builder', right red 'Agency'); neutral icons; no competitor logos or screenshots.",
    alt_text="Cover slide on black: 'AI website builder or agency? An honest guide (from an agency)'.",
    story="n/a (LinkedIn)",
    kpi="5 or more comments; engagement rate at or above the page's November average +10%",
    readiness="Ready for review",
    client_input="",
),
dict(
    id="P11", date="2026-12-16", day="Wed", time="12:00", platform="Instagram + Facebook (cross-post)", tier="Standard",
    pillar="Behind the Build", series="Inside Apex", objective="Engagement", funnel="Consideration", persona="P1; P2",
    format="Reel",
    topic="Meet the people behind your project",
    rationale="Public reviews name individual team members (Ahmed, Mark, Wade, Mo, Kais; B08, verified), showing that people drive trust. Sprout Social: 'Consumers say brands should make human-generated content their #1 priority' (T29, verified).",
    sources=["B08", "T29"],
    hook="Our clients mention our team by name in their reviews. Time you met them.",
    alt_hooks=["The people who'll actually build your website.", "Faces behind the reviews."],
    caption="""Our clients mention our team by name in their reviews. Time you met them. 👋

Meet [Name 1] ([Role 1]), [Name 2] ([Role 2]) and [Name 3] ([Role 3]), a few of the people behind the websites, apps and campaigns we build.

Got a question for them? Drop it in the comments. They'll answer. 👇""",
    cta="Ask the team a question in the comments",
    first_comment="",
    link=utm("instagram", "meet-the-team"),
    hashtags="#MeetTheTeam #WebDesign #AgencyLife #WebDevelopment #ApexWebStudios",
    script=[
        ("0–3s", "Quick cuts of three team members turning to camera", "Meet the team 👋", "Our clients mention our team by name. Time you met them.", "Upbeat licensed track"),
        ("3–13s", "Team member 1 at their desk", "[Name 1] · [Role 1]", "[Name 1]: 'I'm [Name 1], and I [what they do, in one line].'", "—"),
        ("13–23s", "Team member 2", "[Name 2] · [Role 2]", "[Name 2]: one-line intro in their own words", "—"),
        ("23–33s", "Team member 3", "[Name 3] · [Role 3]", "[Name 3]: one-line intro in their own words", "—"),
        ("33–40s", "Group shot or end card", "Ask us anything 👇", "Ask us anything in the comments.", "Fade"),
    ],
    visual="Natural office light, eye-level framing, team in their own clothes; name lower-thirds in Urbanist with a red bar.",
    alt_text="Video: three Apex Web Studios team members introduce themselves at their desks, with name and role captions.",
    story="Story: question sticker 'Ask our team anything', with answers posted the following week.",
    kpi="10 or more comments; profile visits at 1.5% or more of reach",
    readiness="Blocked: client input",
    client_input="Names, roles and signed on-camera consent for three team members. Each person writes their own one-line intro.",
),
dict(
    id="P12", date="2026-12-17", day="Thu", time="16:00", platform="LinkedIn", tier="Standard",
    pillar="Behind the Build", series="Inside Apex", objective="Engagement", funnel="Consideration", persona="P2; P3",
    format="Vertical video",
    topic="Why every Apex website project gets one dedicated project manager",
    rationale="Starter through E-commerce Growth packages list a 'Dedicated Project Manager' (B04, verified). The brand promise is 'No surprises. No radio silence. No hidden costs.' (B02, verified). LinkedIn advises spacing out similar video topics (T12, verified), so this is scheduled a day after the Instagram team Reel and is about a different subject.",
    sources=["B04", "B02", "T12"],
    hook="Ever chased an agency for an update? Here's how we make sure you never have to.",
    alt_hooks=["One project. One person to call.", "“Who do I even talk to?” Not a question our clients ask."],
    caption="""Ever chased an agency for an update? Here's how we make sure you never have to.

Every website package from Starter to E-commerce Growth comes with a dedicated project manager: one person who knows your project, answers your messages and keeps things moving.

In this short video, [PM name] explains what that looks like day to day.

No surprises. No radio silence. No hidden costs.

How do you prefer an agency to keep you updated: weekly calls, written updates or something else?""",
    cta="Comment your preferred update style",
    first_comment="See what's included in each package: " + utm("linkedin", "dedicated-pm", "/pricing"),
    hashtags="#ProjectManagement #WebDevelopment #ApexWebStudios",
    script=[
        ("0–4s", "PM to camera, office background", "Ever chased an agency for an update?", "Ever chased an agency for an update? Let me tell you how we avoid that.", "No music, or a very low bed"),
        ("4–20s", "PM to camera", "One project. One point of contact.", "Every website project here gets a dedicated project manager. For a lot of our clients, that's me.", "—"),
        ("20–40s", "Cutaways: PM sending an update, task board, video call (dummy data)", "What that means for you", "[PM explains in their own words how updates are shared and how quickly they reply. This must match real practice.]", "—"),
        ("40–55s", "PM to camera", "No surprises. No radio silence.", "No surprises. No radio silence. That's the deal.", "—"),
        ("55–60s", "End card", "apexwebstudios.net", "—", "—"),
    ],
    visual="Talking head, 9:16 vertical, mid-shot, lapel mic; IBM Plex Mono lower-thirds; red accent bar.",
    alt_text="Video: an Apex Web Studios project manager speaks to camera about being a single point of contact for clients.",
    story="n/a (LinkedIn)",
    kpi="Average watch time of 15 s or more; 5 or more comments",
    readiness="Blocked: client input",
    client_input="Nominate the project manager and get on-camera consent. Confirm that the update cadence described matches real practice.",
),
dict(
    id="P13", date="2026-12-18", day="Fri", time="12:00", platform="Instagram + Facebook (cross-post)", tier="Core (Lite + Standard)",
    pillar="Offers & Packages", series="Price Tag, Explained", objective="Leads", funnel="Conversion", persona="P1",
    format="Carousel",
    topic="Starting a business in 2027? What the $599 Starter website includes",
    rationale="Starter Web Package: $599 one-time, 3-page custom website, mobile-responsive, contact form, CMS, first concepts within 48 hours, dedicated project manager, '100% Ownership Rights', '100% Satisfaction Guarantee' (B04, verified). The January new-business planning window is timely. A different angle and platform from P08 (one package, for new businesses).",
    sources=["B04", "B06"],
    hook="Starting a business in 2027? Here's what $599 gets you.",
    alt_hooks=["Your first website doesn't have to cost thousands.", "$599. 3 pages. 100% yours."],
    caption="""Starting a business in 2027? Here's what $599 gets you. 🚀

Our Starter Web Package includes:
✔️ A 3-page custom website with a tailored layout
✔️ A mobile-responsive design for every device
✔️ A contact and inquiry form
✔️ A CMS so you can edit it yourself
✔️ First design concepts within 48 hours
✔️ A dedicated project manager
✔️ 100% ownership rights

A one-time price in USD. CAD and GBP pricing is on our website.

Want to start January with a website? Tap the link in bio to book a free call.""",
    cta="Book a free call via the link in bio",
    first_comment="",
    link=utm("instagram", "starter-599", "/pricing"),
    hashtags="#SmallBusinessWebsite #NewBusiness #WebDesign #SmallBusinessOwner #ApexWebStudios",
    slides=[
        ("Cover", "Starting a business in 2027?", "Here's what $599 gets you →"),
        ("Slide 2", "3-page custom website", "A tailored layout for your business"),
        ("Slide 3", "Works everywhere", "Mobile-responsive · contact form · CMS you can edit"),
        ("Slide 4", "Fast and looked after", "First design concepts within 48 hours · a dedicated project manager"),
        ("Slide 5", "It's yours", "100% ownership rights · 100% satisfaction guarantee*"),
        ("CTA", "Start January with a website.", "Book a free call via the link in bio · USD, one-time · *See terms at apexwebstudios.net"),
    ],
    visual="A phone mock-up of a generic 3-page demo site (Apex-made); '$599' in large red IBM Plex Mono on the cover; red checkmarks.",
    alt_text="Carousel cover: 'Starting a business in 2027? Here's what $599 gets you' next to a phone showing a simple website.",
    story="Story: slider sticker 'How ready is your 2027 website plan?', then a link sticker to /pricing.",
    kpi="15 or more link-in-bio clicks; 2 or more DMs or inquiries",
    readiness="Ready for review (confirm prices are unchanged on publish day)",
    client_input="Confirm on the day of publishing that the price, inclusions and satisfaction-guarantee wording are unchanged.",
),
dict(
    id="P14", date="2026-12-22", day="Tue", time="12:00", platform="Instagram + Facebook (cross-post)", tier="Core (Lite + Standard)",
    pillar="Build Smarter (Educate)", series="60-Second Site Check", objective="Engagement", funnel="Awareness", persona="P1; P2",
    format="Carousel",
    topic="Your 2027 website checklist (made to be saved)",
    rationale="A year-end planning carousel that rolls the month's educational themes into one checklist: holiday checks (P01, T53), accessibility (P03/P04, T56), and social search and business details (P09, T31). Built to be saved.",
    sources=["T53", "T56", "T31"],
    hook="Before you plan anything else for 2027, check your website.",
    alt_hooks=["Your 2027 website checklist. Save it.", "Screenshot this before January."],
    caption="""Before you plan anything else for 2027, check your website. ✅

Swipe for an 8-point checklist and save it for your first week back in January.

How many can you tick off already? Tell us your score in the comments 👇""",
    cta="Save this post and comment your score",
    first_comment="",
    link=utm("instagram", "2027-checklist"),
    hashtags="#SmallBusinessTips #WebsiteChecklist #SmallBusinessWebsite #NewYearPlanning #ApexWebStudios",
    slides=[
        ("Cover", "Your 2027 website checklist ✅", "Save this for January"),
        ("Slide 2", "☐ Loads fast on mobile data", "☐ Phone number is tap-to-call"),
        ("Slide 3", "☐ Contact form tested", "…and the emails actually arrive"),
        ("Slide 4", "☐ Hours, services and phone match", "on your website AND your Google Business Profile"),
        ("Slide 5", "☐ Keyboard focus visible", "☐ Alt text on key images ☐ Text easy to read"),
        ("Slide 6", "☐ Service pages answer real questions", "the ones customers ask you every week"),
        ("Slide 7", "☐ You own your domain, site and logins", "not your old web person"),
        ("CTA", "Scored under 6?", "Book a free website call via the link in bio"),
    ],
    visual="Checklist look: white checkboxes on black, red ticks, one idea per slide, slide numbers in IBM Plex Mono.",
    alt_text="Carousel cover: 'Your 2027 website checklist, save this for January' with empty checkboxes on a black background.",
    story="Story: emoji slider 'How ready is your website for 2027?' and a link sticker to the free-call page.",
    kpi="Saves at 3% or more of reach; 5 or more comments",
    readiness="Ready for review",
    client_input="",
),
dict(
    id="P15", date="2026-12-23", day="Wed", time="16:00", platform="LinkedIn", tier="Standard",
    pillar="Proof & Results", series="In Their Words", objective="Engagement", funnel="Consideration", persona="P1; P3",
    format="Text post + image",
    topic="Client story: a full rebrand and a new website against a fixed deadline",
    rationale="Jamar Root's public review on apexwebstudios.net/testimonials (Aug 16, 2024; B08, verified) describes needing 'a full rebrand and website by a certain deadline' and praises communication. Apex has no published case studies yet, so verbatim reviews are its strongest proof asset.",
    sources=["B08"],
    hook="A full rebrand and a new website, on a fixed deadline.",
    alt_hooks=["Deadlines don't scare us. Silence does.", "What a client said after a deadline-driven rebrand."],
    caption="""A full rebrand and a new website, on a fixed deadline.

That was the brief from client Jamar Root. In Jamar's words:

“Communication was AMAZING and they did a great job of taking my ideas and turning them into something even better than I could have imagined.”

Deadlines don't scare us. Silence does, which is why we don't do it.

Thank you, Jamar. 🖤

Planning a rebrand or a new site for 2027? Let's talk.""",
    cta="Message Apex to plan a 2027 rebrand or website",
    first_comment="Branding and website packages: " + utm("linkedin", "client-story", "/pricing"),
    hashtags="#Branding #WebDesign #ApexWebStudios",
    copy_on_image=["“Communication was AMAZING and they did a great job of taking my ideas and turning them into something even better than I could have imagined.”", "Jamar Root, Apex client"],
    visual="Quote card: black background, large red quotation marks, the quote in white Inter, attribution in IBM Plex Mono.",
    alt_text="Quote card on black: 'Communication was AMAZING and they did a great job of taking my ideas and turning them into something even better than I could have imagined.' Jamar Root, Apex Web Studios client.",
    story="n/a (LinkedIn)",
    kpi="Engagement rate at or above the page's November average; 2 or more inbound messages",
    readiness="Blocked: client input",
    client_input="Written permission from Jamar Root to feature the review and name on social media.",
),
dict(
    id="P16", date="2026-12-24", day="Thu", time="10:00", platform="Instagram + Facebook (cross-post)", tier="Standard",
    pillar="Community & Moments", series="Moments", objective="Community", funnel="Loyalty", persona="All",
    format="Static image",
    topic="Season's greetings and holiday office hours",
    rationale="Christmas Eve. Clients need to know holiday availability. The post reflects Apex's three offices (Milton ON, Los Angeles, Birmingham UK; B01, verified).",
    sources=["B01"],
    hook="From all of us at Apex: happy holidays. 🖤",
    alt_hooks=["Thank you for building with us this year.", "Season's greetings from Milton, Los Angeles and Birmingham."],
    caption="""From all of us at Apex: happy holidays. 🖤

Thank you to every client, partner and follower who built something with us this year.

Holiday hours:
[Dates and hours to be confirmed by Apex]

Wishing you a restful break and a great start to 2027.

The Apex Web Studios team, from Canada, the USA and the UK""",
    cta="None (goodwill and information)",
    first_comment="",
    link="",
    hashtags="#HappyHolidays #SeasonsGreetings #ApexWebStudios",
    copy_on_image=["Happy holidays", "Milton · Los Angeles · Birmingham", "Apex Web Studios"],
    visual="A team photo if available (with consent), or a minimal black card with red-and-white festive line art. The three city names set in IBM Plex Mono.",
    alt_text="Holiday card from Apex Web Studios on a black background with festive line art and the city names Milton, Los Angeles and Birmingham.",
    story="Story: holiday hours as plain text, saved to a 'Contact' Highlight.",
    kpi="Engagement rate at or above the account average",
    readiness="Blocked: client input",
    client_input="Holiday office hours for Dec 24 – Jan 1. Optional: a team photo with consent.",
),
dict(
    id="P17", date="2026-12-30", day="Wed", time="12:00", platform="Instagram + Facebook (cross-post)", tier="Core (Lite + Standard)",
    pillar="Offers & Packages", series="Price Tag, Explained", objective="Leads", funnel="Conversion", persona="P1; P2",
    format="Reel",
    topic="If your website were an employee, would you rehire it for 2027?",
    rationale="The free call is Apex's primary call to action ('Book a Free Call', B01, verified), and the brand promise is 'No Confusing Proposals / No Lengthy Contracts / No Hidden Cost' (B01, verified). The new year is a natural decision point. This closes the month's sequence after the checklist (P14) and the package posts (P08, P13).",
    sources=["B01"],
    hook="If your website were an employee, would you rehire it for 2027?",
    alt_hooks=["New year. Same website? 👀", "Your website's annual review is due."],
    caption="""If your website were an employee, would you rehire it for 2027? 🤔

Did it bring in leads? Show up on Google? Work on mobile? Answer customers' questions?

If the answer is “not really”, January is the time to fix it.

Book a free call and we'll:
→ Look at your current site (or your idea)
→ Tell you honestly what it needs and what it doesn't
→ Show you which package fits, with the price up front

No confusing proposals. No lengthy contracts. No hidden costs.

Tap the link in bio to grab a January slot.""",
    cta="Book a free call via the link in bio",
    first_comment="",
    link=utm("instagram", "rehire-your-website"),
    hashtags="#SmallBusinessWebsite #WebDesign #NewYearNewWebsite #SmallBusinessOwner #ApexWebStudios",
    script=[
        ("0–3s", "Mock 'performance review' form on a desk titled 'Employee: Your Website'", "Would you rehire your website for 2027?", "If your website were an employee, would you rehire it?", "Light, playful licensed track"),
        ("3–12s", "Pen ticks boxes: 'Brings in leads? ☐  Works on mobile? ☐  Shows up on Google? ☐'", "Annual review time 📋", "Did it bring in leads? Work on mobile? Show up on Google?", "—"),
        ("12–24s", "Apex team member to camera", "Not really? Fix it in January.", "If the answer's 'not really', January's the time to fix it. Book a free call. We'll look at your site and tell you honestly what it needs.", "—"),
        ("24–32s", "Text-only frames, one line each", "No confusing proposals. · No lengthy contracts. · No hidden costs.", "No confusing proposals. No lengthy contracts. No hidden costs.", "Beat hits on each line"),
        ("32–38s", "End card", "Grab a January slot: link in bio", "Grab a January slot via the link in bio.", "Fade"),
    ],
    visual="Props: a printed 'performance review' form (Apex-designed), desk setting. Red-and-black end card. Light humour, no mocking of any real business's website.",
    alt_text="Video: a mock employee performance review titled 'Your Website' with unticked boxes, then an Apex team member inviting viewers to book a free call, ending with the text 'No confusing proposals. No lengthy contracts. No hidden costs.'",
    story="Story: poll 'Would you rehire your website? 👍 / 👎', with a link sticker for 👎 voters.",
    kpi="20 or more link-in-bio clicks; 3 or more attributed free-call bookings",
    readiness="Ready for review (confirm January call availability)",
    client_input="Confirm free-call availability in the first two weeks of January.",
),
dict(
    id="P18", date="2026-12-29", day="Tue", time="16:00", platform="LinkedIn", tier="Reserve (optional)",
    pillar="Behind the Build", series="Inside Apex", objective="Engagement", funnel="Loyalty", persona="P2; P3; P4 Agency Partner",
    format="Document carousel (PDF)",
    topic="What 2026 taught our team about building for clients",
    rationale="A year-end reflection window. Sprout Social reports consumers want human-generated content prioritised (T29, verified). This must use real team input; no results are invented. Optional: publish only if capacity allows and the inputs arrive.",
    sources=["T29"],
    hook="We asked our team: what's one thing 2026 taught you about building for clients?",
    alt_hooks=["3 lessons from a year of building websites, apps and AI tools.", "What 2026 taught us."],
    caption="""We asked our team: what's one thing 2026 taught you about building for clients?

[Team member 1, role]: “[Lesson, in their words]”

[Team member 2, role]: “[Lesson, in their words]”

[Team member 3, role]: “[Lesson, in their words]”

Our shared takeaway: the best projects start with the clearest conversations.

What did 2026 teach you about your business?""",
    cta="Comment your 2026 lesson",
    first_comment="Here's to building in 2027: " + utm("linkedin", "2026-lessons"),
    hashtags="#Leadership #WebDevelopment #ApexWebStudios",
    slides=[
        ("Cover", "What 2026 taught our team", "Lessons from a year of building"),
        ("Page 2", "[Team member 1 photo + quote]", "[Name, role]"),
        ("Page 3", "[Team member 2 photo + quote]", "[Name, role]"),
        ("Page 4", "[Team member 3 photo + quote]", "[Name, role]"),
        ("Page 5", "Our takeaway", "The best projects start with the clearest conversations."),
        ("CTA", "Here's to building in 2027.", "apexwebstudios.net"),
    ],
    visual="A portrait photo per page (team, with consent) on black; quote in white; name and role in red IBM Plex Mono.",
    alt_text="Cover slide: 'What 2026 taught our team, lessons from a year of building' on a black background.",
    story="n/a (LinkedIn)",
    kpi="5 or more comments; engagement rate at or above the page's November average",
    readiness="Blocked: client input (reserve)",
    client_input="Three real team quotes, with names, roles, photos and consent. Skip this post if they aren't available by Dec 22.",
),
]

POSTS.sort(key=lambda p: (p["date"], p["time"]))
for i, p in enumerate(POSTS, 1):
    p["cb"] = f"CB-2026-12-{i:02d}"
