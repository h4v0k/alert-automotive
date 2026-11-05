#!/usr/bin/env python3
"""Generates the Alert Automotive static pages into ../alert-automotive/."""
from pathlib import Path
import hashlib

OUT = Path(__file__).resolve().parent

def v(rel):
    """Cache-busting version from file contents."""
    return hashlib.md5((OUT / rel).read_bytes()).hexdigest()[:8]

BIZ = {
    "name": "Alert Automotive",
    "phone": "(352) 515-3660",
    "tel": "+13525153660",
    "email": "alertautomotive352@gmail.com",
    "street": "9824 Ideal Ln, Suite 103",
    "city": "Hudson, FL 34667",
    "fb": "https://www.facebook.com/AlertAutomotive",
    "hours": "Mon–Fri 8 AM–5 PM · Sat–Sun closed",
    "google": "https://share.google/eyMXdKkK0FIiKgoOZ",
}
MAP_Q = "9824+Ideal+Ln+Suite+103,+Hudson,+FL+34667"
DIRECTIONS = f"https://www.google.com/maps/dir/?api=1&destination={MAP_Q}"

ICONS = {
    "gear": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "scan": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2"/><path d="M7 12h3l2-4 2 8 2-4h1"/></svg>',
    "brake": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M5 6.5A9 9 0 0 0 5 17.5"/></svg>',
    "snow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.7S5 10 5 14.5a7 7 0 0 0 14 0C19 10 12 2.7 12 2.7z"/></svg>',
    "susp": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v3M12 19v3M8 5h8l-8 3 8 3-8 3 8 3H8"/></svg>',
    "engine": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 10h2V8h3V6h6v2h2l2 3h2v5h-2l-2 3H9l-3-3H4z"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    "clip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 2h6v4H9z"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16v16H4z"/><path d="m22 6-10 7L2 6"/></svg>',
    "family": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
    "tire": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="M12 2v6M12 16v6M2 12h6M16 12h6"/></svg>',
    "mower": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4l5 8M8 12h11v5H4v-5h4"/><circle cx="7" cy="19" r="2"/><circle cx="17" cy="19" r="2"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 22V3M4 3h14l-3 4 3 4H4"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "card": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/></svg>',
    "car": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17H3v-5l2-5h14l2 5v5h-2"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/><path d="M3 12h18"/></svg>',
}

LOGO = '''<svg viewBox="0 0 48 48" aria-hidden="true">
  <path d="M24 3 45 41H3z" fill="#e0221b"/>
  <path d="M24 5.5 42.7 39.5H5.3z" fill="none" stroke="#ffffff" stroke-width="2.2"/>
  <rect x="21.6" y="16" width="4.8" height="13" rx="2" fill="#ffffff"/>
  <circle cx="24" cy="34" r="2.7" fill="#ffffff"/>
</svg>'''

NAV = [
    ("index.html", "Home"),
    ("auto-repair.html", "Auto Repair"),
    ("fleet.html", "Fleet Services"),
    ("gallery.html", "Gallery"),
    ("contact.html", "Contact"),
]


def href(page):
    return "/" if page == "index.html" else "/" + page.replace(".html", "")


def header(current):
    links = "\n".join(
        f'<a href="{href(p)}"{" aria-current=\"page\"" if p == current else ""}>{label}</a>'
        for p, label in NAV
    )
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span>Family owned · Mon–Fri 8 AM–5 PM</span>
  <span><a href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a> <a class="addr" href="{DIRECTIONS}" target="_blank" rel="noopener">· {BIZ["street"]}, Hudson</a></span>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/" aria-label="Alert Automotive home">{LOGO}
    <span><span class="brand-name">Alert <span>Automotive</span></span><span class="brand-sub">HUDSON · FLORIDA</span></span>
  </a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav class="nav" id="site-nav" aria-label="Main">
{links}
    <a class="btn" href="/contact#schedule">Schedule Service</a>
  </nav>
</div></header>'''


def footer():
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div>
      <a class="brand" href="/" aria-label="Alert Automotive home">{LOGO}<span class="brand-name" style="color:#fff">Alert <span>Automotive</span></span></a>
      <p style="margin-top:1rem">Family owned and locally operated in Hudson, FL. Quality repairs, honest service, fair prices — and 20+ years of transmission expertise. Making vehicles run great again.</p>
    </div>
    <div>
      <h4>Visit</h4>
      <ul>
        <li><a href="{DIRECTIONS}" target="_blank" rel="noopener">{BIZ["street"]}<br>{BIZ["city"]}</a></li>
        <li>{BIZ["hours"]}</li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul>
        <li><a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a></li>
        <li><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></li>
        <li><a href="{BIZ["fb"]}" target="_blank" rel="noopener">Facebook</a></li>
      </ul>
    </div>
    <div>
      <h4>Services</h4>
      <ul>
        <li><a href="/auto-repair#transmissions">Transmission repair</a></li>
        <li><a href="/auto-repair">Auto repair &amp; maintenance</a></li>
        <li><a href="/auto-repair#classics">Classics &amp; performance</a></li>
        <li><a href="/auto-repair#small-engines">Small engine repair</a></li>
        <li><a href="/fleet">Fleet services</a></li>
        <li><a href="/contact#schedule">Request an appointment</a></li>
      </ul>
    </div>
  </div>
  <div class="legal"><span>© <span data-year></span> Alert Automotive · Hudson, Florida</span><span>Serving Hudson, Spring Hill, Port Richey &amp; the Nature Coast</span></div>
</div></footer>
<a class="btn call-fab" href="tel:{BIZ["tel"]}">{ICONS["phone"].replace('<svg', '<svg width="20" height="20"')} Call {BIZ["phone"]}</a>
<script src="/assets/config.js?v={v("assets/config.js")}"></script>
<script src="/assets/main.js?v={v("assets/main.js")}" defer></script>'''


SCHEMA = f'''<script type="application/ld+json">{{
  "@context": "https://schema.org", "@type": "AutoRepair",
  "name": "Alert Automotive", "telephone": "{BIZ["tel"]}", "email": "{BIZ["email"]}",
  "address": {{"@type": "PostalAddress", "streetAddress": "9824 Ideal Ln Suite 103",
    "addressLocality": "Hudson", "addressRegion": "FL", "postalCode": "34667", "addressCountry": "US"}},
  "sameAs": ["{BIZ["fb"]}"], "areaServed": ["Hudson, FL", "Spring Hill, FL", "Pasco County, FL", "Hernando County, FL"],
  "openingHours": "Mo-Fr 08:00-17:00", "slogan": "Making Vehicles Run Great Again"
}}</script>'''


def page(filename, title, desc, body, current=None, extra_head=""):
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#111214">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css?v={v("assets/styles.css")}">
{SCHEMA}
{extra_head}
</head>
<body>
{header(current or filename)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    (OUT / filename).write_text(html)


def card(icon, title, text, cls="card", anchor=None):
    a = f' id="{anchor}"' if anchor else ""
    return f'<article class="{cls}"{a}><div class="icon">{ICONS[icon]}</div><h3>{title}</h3><p>{text}</p></article>'


CTA = f'''<section class="cta-band"><div class="wrap">
  <h2>Warning light on?<br>Let's take a look.</h2>
  <div class="btn-row"><a class="btn dark" href="/contact#schedule">Request an Appointment</a><a class="btn dark" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a></div>
</div></section>'''

# ---------------- HOME ----------------
home = f'''
<section class="hero"><div class="wrap">
  <span class="eyebrow">Family owned · Hudson, FL</span>
  <h1>Making vehicles <em>run great</em> again.</h1>
  <p class="lede">Daily drivers, brand-new vehicles, work trucks, cool classics and even your lawn mower — Alert Automotive does it all. Family owned and locally operated, with 20+ years of transmission expertise and newly doubled bays to get you back on the road faster.</p>
  <div class="btn-row">
    <a class="btn" href="/contact#schedule">Request an Appointment</a>
    <a class="btn ghost" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a>
  </div>
  <ul class="trust">
    <li>5.0★ on Google · 160+ reviews</li>
    <li>24-month / 24,000-mile warranty</li>
    <li>Free second opinions</li>
  </ul>
</div></section>

<section data-until="2026-11-30" style="padding-bottom:0"><div class="wrap">
  <div class="special">
    <div>
      <span class="tag">November special · through Nov 30</span>
      <h2 style="margin:0">Brake special</h2>
      <p style="margin:.3rem 0 0">Pads &amp; hardware, <strong>labor included</strong>. Applies to most vehicles; additional parts and labor may be required.</p>
    </div>
    <div style="display:flex;flex-wrap:wrap;align-items:center;gap:1rem">
      <span class="price">$149.99</span>
      <a class="btn" href="/contact#schedule">Book brakes</a>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head">
    <span class="kicker">Big or small, we do it all</span>
    <h2>What we work on</h2>
  </div>
  <div class="grid">
    {card("car", "Daily drivers &amp; new vehicles", "Foreign and domestic cars, SUVs and minivans — routine maintenance to full engine overhauls.")}
    {card("truck", "Trucks &amp; fleets", "Work trucks and company vehicles kept on the road, plus upfitting: wheels, tires, lighting, bumpers and canopies.")}
    {card("flag", "Classics &amp; custom", "Classic cars are our passion — restoration and repair, performance upgrades and custom modifications.")}
    {card("mower", "Small engines", "Lawn mowers, generators, chainsaws and trimmers — tune-ups, carb cleaning, fuel systems and more.")}
  </div>
</div></section>

<section class="section-dark"><div class="wrap">
  <div class="section-head">
    <span class="kicker">Full service</span>
    <h2>Most-requested services</h2>
    <p>Not sure what's wrong? Tell us what you're hearing, feeling or seeing — we diagnose it before we fix anything.</p>
  </div>
  <div class="grid">
    {card("gear", "Transmission service", "20+ years of transmission work — diagnosis, repair, rebuilds and replacements.")}
    {card("engine", "Engine repair", "From misfires and leaks to full engine overhauls.")}
    {card("brake", "Brakes &amp; safety", "Pads, rotors, calipers, lines and ABS so you stop straight and quiet.")}
    {card("tire", "Tire sales", "Now offering Cosmo tires — all-season, all-terrain and mud-terrain options.")}
    {card("drop", "Oil changes &amp; maintenance", "Preventative maintenance that keeps your vehicle running longer.")}
    {card("snow", "A/C &amp; heating", "Florida-proof A/C service and repair.")}
    {card("bolt", "Electrical diagnostics", "Warning lights, batteries, charging and wiring traced to the real cause.")}
    {card("mower", "Small engine repair", "Mowers, generators and outdoor equipment tuned up and running strong.")}
  </div>
  <p style="margin-top:2rem"><a class="btn" href="/auto-repair">See all services</a></p>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="kicker">Peace of mind</span><h2>Why drivers choose Alert</h2></div>
  <div class="promo-grid">
    <div class="promo"><span class="big">Free 2nd opinion</span><p>Got an estimate somewhere else? Bring it in and get a free second opinion from our certified shop.</p><a class="btn dark" href="/contact#schedule">Get a second opinion</a></div>
    <div class="promo"><span class="big">24 mo / 24K mi</span><p>Our repairs are backed by a 24-month / 24,000-mile warranty. We stand behind our work.</p></div>
    <div class="promo"><span class="big">6 months financing</span><p>Promotional financing on purchases of $199 or more with the Synchrony Car Care™ credit card.</p><small>Subject to credit approval. Minimum monthly payments required. See store for details.</small></div>
  </div>
</div></section>

<section class="section-dark"><div class="wrap">
  <div class="grid two">
    <div>
      <span class="kicker">Locally owned &amp; operated</span>
      <h2>Bigger shop. Same family.</h2>
      <p>We just doubled our bays — more room and faster turnaround. What hasn't changed is how we treat people: like family, with honest recommendations and no surprises.</p>
      <ul class="ticks">
        <li>Experienced, skilled technicians</li>
        <li>All makes &amp; models — foreign, domestic, trucks, SUVs</li>
        <li>Quality parts and state-of-the-art diagnostic equipment</li>
        <li>Fair, honest pricing — nothing done without your OK</li>
      </ul>
      <ul class="badges">
        <li>CARFAX 2025 Top-Rated Service Center</li>
        <li>BusinessRate Best of 2026</li>
        <li>2026 Best of Florida Regional Winner</li>
      </ul>
      <p style="margin-top:1.4rem"><a class="btn" href="{BIZ["google"]}" target="_blank" rel="noopener">Read our Google reviews</a></p>
    </div>
    <div>
      <span class="kicker">How it works</span>
      <h2>Getting your vehicle in</h2>
      <ol class="steps" style="color:var(--ink)">
        <li><strong>Request a time</strong>Pick a preferred day online or give us a call.</li>
        <li><strong>We confirm</strong>We'll call or text to lock in your drop-off.</li>
        <li><strong>Diagnose &amp; approve</strong>You get a clear explanation and estimate first.</li>
      </ol>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:1rem;max-width:none">
    <div><span class="kicker">From the shop</span><h2 style="margin:0">Recent work</h2></div>
    <a class="btn dark" href="/gallery">View the gallery</a>
  </div>
  <div class="gallery-grid" data-gallery data-limit="6"></div>
</div></section>

{CTA}
'''
page("index.html", "Alert Automotive | Auto Repair in Hudson, FL — Making Vehicles Run Great Again",
     "Family-owned auto repair in Hudson, FL: transmissions, engine, brakes, tires, A/C, classics, fleets and small engines. 5.0★ on Google. Free second opinions. Call (352) 515-3660.",
     home)

# ---------------- AUTO REPAIR ----------------
repair = f'''
<section class="hero small"><div class="wrap">
  <span class="eyebrow">Consumer auto repair</span>
  <h1>Big or small, we do it all</h1>
  <p class="lede">Everyday repairs and maintenance, transmissions, tires, classics, custom work and small engines — all makes and models, foreign and domestic.</p>
  <div class="btn-row"><a class="btn" href="/contact#schedule">Request an Appointment</a><a class="btn ghost" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a></div>
</div></section>

<section id="transmissions"><div class="wrap">
  <div class="grid two">
    <div>
      <span class="kicker">20+ years of experience</span>
      <h2>Transmission repair &amp; rebuilds</h2>
      <p>We've been working on transmissions for over 20 years. Before you're told you need a replacement, let us take a look — sometimes the fix is a sensor, a solenoid, a leak, or a software issue rather than the whole unit.</p>
      <ul class="ticks">
        <li>Automatic and manual transmission diagnosis</li>
        <li>Rebuilds, repairs, and replacement units</li>
        <li>Fluid and filter service</li>
        <li>Leaks, slipping, harsh or delayed shifting</li>
        <li>Clutches, CV axles, and driveline work</li>
      </ul>
      <a class="btn" href="/contact#schedule">Get it checked</a>
    </div>
    <div class="card feature" data-badge="20+ YEARS">
      <h3>Signs your transmission needs attention</h3>
      <ul class="ticks">
        <li>Engine revs but the vehicle doesn't accelerate</li>
        <li>Clunks, jerks or hesitation when shifting</li>
        <li>Delay when putting it in Drive or Reverse</li>
        <li>Red or brown fluid spots under the vehicle</li>
        <li>Burning smell or a transmission warning light</li>
      </ul>
      <p>Catching these early is usually the difference between a repair and a rebuild.</p>
    </div>
  </div>
</div></section>

<section class="section-dark"><div class="wrap">
  <div class="section-head"><span class="kicker">Full service</span><h2>Everything else under the hood</h2></div>
  <div class="grid">
    {card("scan", "Diagnostics &amp; check-engine", "Computer diagnostics plus hands-on testing to find the cause, not just the code.")}
    {card("engine", "Engine repair", "Misfires, leaks, timing components, gaskets, and performance problems.")}
    {card("brake", "Brakes", "Pads, rotors, calipers, hoses, fluid flushes and ABS diagnosis.")}
    {card("snow", "A/C &amp; heating", "Recharge, leak detection, compressors and blend-door issues.")}
    {card("drop", "Cooling system", "Radiators, hoses, water pumps, thermostats and overheating.")}
    {card("susp", "Suspension &amp; steering", "Shocks, struts, ball joints, tie rods, and that clunk over bumps.")}
    {card("bolt", "Electrical", "Batteries, alternators, starters, wiring and lighting.")}
    {card("clip", "Oil changes &amp; maintenance", "Oil changes, fluids, belts, filters and preventative maintenance.")}
    {card("tire", "Tire sales &amp; service", "Now offering Cosmo tires — all-season, all-terrain and mud-terrain, mounted and balanced.")}
  </div>
</div></section>

<section id="classics"><div class="wrap">
  <div class="grid two">
    <div>
      <span class="kicker">We love classics</span>
      <h2>Classics, performance &amp; custom</h2>
      <p>Classic cars are our passion. Whether you're bringing a classic back to life or building something completely custom, we're ready to get to work.</p>
      <ul class="ticks">
        <li>Classic car restoration &amp; repair</li>
        <li>Performance upgrades</li>
        <li>Custom modifications</li>
        <li>Upfitting — wheels, tires, lighting, bumpers &amp; canopies</li>
      </ul>
      <a class="btn" href="/contact#schedule">Talk about your build</a>
    </div>
    <div id="small-engines" class="card feature">
      <h3>Small engine repair &amp; maintenance</h3>
      <p>Mowers, generators, chainsaws, trimmers and more — don't wait until your equipment leaves you stranded.</p>
      <ul class="ticks">
        <li>Tune-ups &amp; oil changes</li>
        <li>Spark plug replacement</li>
        <li>Carburetor cleaning &amp; repair</li>
        <li>Fuel system service</li>
        <li>Lawn mower blade sharpening</li>
        <li>Seasonal maintenance</li>
      </ul>
    </div>
  </div>
</div></section>

<section class="section-dark"><div class="wrap">
  <div class="promo-grid" style="color:var(--ink)">
    <div class="promo"><span class="big">Free 2nd opinion</span><p>Received an estimate elsewhere? Bring it in for a free second opinion.</p></div>
    <div class="promo"><span class="big">24 mo / 24K mi</span><p>Warranty on our repairs.</p></div>
    <div class="promo"><span class="big">Financing</span><p>6 months promotional financing on $199+ with the Synchrony Car Care™ credit card.</p><small>Subject to credit approval. Minimum monthly payments required. See store for details.</small></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="kicker">What to expect</span><h2>No surprises</h2></div>
  <ol class="steps">
    <li><strong>Tell us the symptoms</strong>Use the request form or call — the more detail, the faster the diagnosis.</li>
    <li><strong>We inspect &amp; diagnose</strong>We find the cause and walk you through what we found.</li>
    <li><strong>You approve the estimate</strong>No work starts until you say go.</li>
    <li><strong>Back on the road</strong>We'll call when it's ready and explain what was done.</li>
  </ol>
</div></section>

{CTA}
'''
page("auto-repair.html", "Auto & Transmission Repair in Hudson, FL | Alert Automotive",
     "Transmission, engine, brake, tire, A/C and electrical repair, classic car restoration, performance upgrades and small engine repair in Hudson, FL.",
     repair)

# ---------------- FLEET ----------------
fleet = f'''
<section class="hero small"><div class="wrap">
  <span class="eyebrow">Commercial &amp; fleet</span>
  <h1>Keep your fleet earning, not sitting</h1>
  <p class="lede">Local businesses rely on Alert Automotive to keep work trucks, vans and company cars on the road — with planned maintenance, fast turnaround on repairs, and a shop that knows your vehicles.</p>
  <div class="btn-row"><a class="btn" href="#fleet-form">Set up a fleet account</a><a class="btn ghost" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a></div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="kicker">Built for business</span><h2>What fleet customers get</h2></div>
  <div class="grid">
    {card("clip", "Preventive maintenance", "Mileage- or interval-based service plans so problems get caught before a breakdown.")}
    {card("clock", "Priority scheduling", "We work with your schedule to minimize downtime and get vehicles back to work.")}
    {card("gear", "Drivetrain expertise", "Twenty years of transmission work — the part that takes a hard-working vehicle off the road.")}
    {card("truck", "Mixed fleets welcome", "Pickups, service vans, SUVs and company cars — one shop for the whole lineup.")}
    {card("scan", "Clear reporting", "Straightforward estimates and service records for every vehicle.")}
    {card("tire", "Tires &amp; upfitting", "Cosmo tires plus wheels, lighting, bumpers and canopies to get work trucks job-ready.")}
    {card("shield", "24 mo / 24K mi warranty", "Repairs backed by our 24-month / 24,000-mile warranty.")}
  </div>
</div></section>

<section class="section-dark"><div class="wrap">
  <div class="grid two">
    <div>
      <span class="kicker">Who we work with</span>
      <h2>Fleets of every size</h2>
      <p>Whether you run two work trucks or a few dozen vehicles, we'll set up a maintenance rhythm that fits how hard your vehicles work.</p>
      <ul class="ticks">
        <li>Contractors &amp; trades</li>
        <li>Delivery and service vans</li>
        <li>Landscaping, tree service, pool &amp; pest control — including your mowers and outdoor equipment</li>
        <li>Real estate, sales &amp; company cars</li>
        <li>Municipal and nonprofit vehicles</li>
      </ul>
    </div>
    <div class="form-card" id="fleet-form" style="color:var(--ink)">
      <form name="fleet-inquiry" method="POST" action="/thank-you" data-netlify="true" netlify-honeypot="bot-field" data-ajax>
        <input type="hidden" name="form-name" value="fleet-inquiry">
        <input type="hidden" name="subject" value="New fleet inquiry — Alert Automotive website">
        <p class="hidden-field"><label>Don't fill this out: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
        <fieldset>
          <legend>Fleet inquiry</legend>
          <div class="form-grid">
            <div class="full"><label for="f-company">Company name <span class="req">*</span></label><input id="f-company" type="text" name="company" required autocomplete="organization"></div>
            <div><label for="f-name">Your name <span class="req">*</span></label><input id="f-name" type="text" name="name" required autocomplete="name"></div>
            <div><label for="f-phone">Phone <span class="req">*</span></label><input id="f-phone" type="tel" name="phone" required autocomplete="tel"></div>
            <div><label for="f-email">Email <span class="req">*</span></label><input id="f-email" type="email" name="email" required autocomplete="email"></div>
            <div><label for="f-size">Number of vehicles</label>
              <select id="f-size" name="fleet_size"><option value="">Choose…</option><option>1–5</option><option>6–15</option><option>16–40</option><option>40+</option></select></div>
            <div class="full"><label for="f-types">Vehicle types</label><input id="f-types" type="text" name="vehicle_types" placeholder="e.g. 4 F-250s, 2 Transit vans"></div>
            <div class="full"><label for="f-msg">What do you need?</label><textarea id="f-msg" name="message" placeholder="Maintenance plan, a specific repair, billing setup…"></textarea></div>
          </div>
        </fieldset>
        <button class="btn" type="submit">Send fleet inquiry</button>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
</div></section>

{CTA}
'''
page("fleet.html", "Fleet Vehicle Maintenance & Repair in Hudson, FL | Alert Automotive",
     "Fleet maintenance and repair for work trucks, vans and company vehicles in Hudson and Pasco County, FL. Transmission specialists.",
     fleet)

# ---------------- GALLERY ----------------
gallery = '''
<section class="hero small"><div class="wrap">
  <span class="eyebrow">Gallery</span>
  <h1>Inside the shop</h1>
  <p class="lede">Recent jobs, rebuilds, and the vehicles that come through our bays.</p>
</div></section>
<section><div class="wrap">
  <div class="gallery-grid" data-gallery></div>
</div></section>
<dialog class="lightbox" aria-label="Photo viewer">
  <img alt="">
  <div class="lb-bar"><span class="lb-caption"></span><div class="lb-nav"><button data-lb="prev" aria-label="Previous photo">‹ Prev</button><button data-lb="next" aria-label="Next photo">Next ›</button><button data-lb="close">Close</button></div></div>
</dialog>
''' + CTA
page("gallery.html", "Photo Gallery | Alert Automotive, Hudson FL",
     "Photos of recent repairs, transmission rebuilds and vehicles at Alert Automotive in Hudson, FL.",
     gallery)

# ---------------- CONTACT ----------------
def chk(name, value):
    return f'<label class="choice"><input type="checkbox" name="{name}" value="{value}"> {value}</label>'

services = ["Transmission problem", "Check-engine / warning light", "Brakes", "Tires",
            "A/C or heating", "Oil change / maintenance", "Engine / overheating", "Electrical / battery",
            "Classic / performance / custom", "Small engine (mower, generator…)", "Free second opinion", "Something else"]

contact = f'''
<section class="hero small"><div class="wrap">
  <span class="eyebrow">Contact &amp; scheduling</span>
  <h1>Request an appointment</h1>
  <p class="lede">Tell us about your vehicle and pick a preferred time. We'll call or text to confirm — usually the same business day.</p>
</div></section>

<section id="schedule"><div class="wrap">
  <div class="grid two">
    <div class="form-card">
      <div class="form-note"><strong>This is a request, not a confirmed booking.</strong> Have an estimate from another shop? Choose "Free second opinion" below. We'll reach out to confirm your time. Need it today? Call <a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a>.</div>
      <form name="appointment-request" method="POST" action="/thank-you" data-netlify="true" netlify-honeypot="bot-field" data-ajax>
        <input type="hidden" name="form-name" value="appointment-request">
        <input type="hidden" name="subject" value="New appointment request — Alert Automotive website">
        <p class="hidden-field"><label>Don't fill this out: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

        <fieldset>
          <legend>Your info</legend>
          <div class="form-grid">
            <div><label for="c-name">Full name <span class="req">*</span></label><input id="c-name" type="text" name="name" required autocomplete="name"></div>
            <div><label for="c-phone">Phone <span class="req">*</span></label><input id="c-phone" type="tel" name="phone" required autocomplete="tel"></div>
            <div><label for="c-email">Email</label><input id="c-email" type="email" name="email" autocomplete="email"></div>
            <div><label for="c-contact">Best way to reach you</label>
              <select id="c-contact" name="contact_method"><option>Call</option><option>Text</option><option>Email</option></select></div>
            <div class="full"><label>This vehicle is…</label>
              <div class="choices">
                <label class="choice"><input type="radio" name="customer_type" value="Personal vehicle" checked> Personal vehicle</label>
                <label class="choice"><input type="radio" name="customer_type" value="Fleet / business vehicle"> Fleet / business vehicle</label>
              </div></div>
          </div>
        </fieldset>

        <fieldset>
          <legend>Your vehicle</legend>
          <div class="form-grid">
            <div><label for="v-year">Year <span class="req">*</span></label><input id="v-year" type="text" inputmode="numeric" name="vehicle_year" required maxlength="4" placeholder="2018"></div>
            <div><label for="v-make">Make <span class="req">*</span></label><input id="v-make" type="text" name="vehicle_make" required placeholder="Ford"></div>
            <div><label for="v-model">Model <span class="req">*</span></label><input id="v-model" type="text" name="vehicle_model" required placeholder="F-150"></div>
            <div><label for="v-miles">Approx. mileage</label><input id="v-miles" type="text" inputmode="numeric" name="mileage" placeholder="98,000"></div>
          </div>
        </fieldset>

        <fieldset>
          <legend>What's going on?</legend>
          <div class="choices">{"".join(chk("services", s) for s in services)}</div>
          <div style="margin-top:1rem"><label for="c-msg">Describe the problem</label><textarea id="c-msg" name="message" placeholder="What are you hearing, feeling or seeing? When does it happen?"></textarea></div>
        </fieldset>

        <fieldset>
          <legend>Preferred time</legend>
          <div class="form-grid">
            <div><label for="d-1">Preferred date <span class="req">*</span></label><input id="d-1" type="date" name="preferred_date" required data-min-today></div>
            <div><label for="t-1">Time of day</label>
              <select id="t-1" name="preferred_time"><option>Morning drop-off</option><option>Midday</option><option>Afternoon</option><option>Any time</option></select></div>
            <div><label for="d-2">Backup date</label><input id="d-2" type="date" name="backup_date" data-min-today></div>
            <div><label for="c-wait">Drop off or wait?</label>
              <select id="c-wait" name="drop_or_wait"><option>Drop off</option><option>Wait (quick services)</option><option>Need a ride / not sure</option></select></div>
          </div>
          <p class="hint">We'll confirm the exact time when we contact you.</p>
        </fieldset>

        <button class="btn" type="submit">Send appointment request</button>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>

    <aside>
      <span class="kicker">Find us</span>
      <h2>Visit the shop</h2>
      <ul class="info-list" style="margin-bottom:1.6rem">
        <li><span class="icon">{ICONS["pin"]}</span><div><strong>Address</strong><a href="{DIRECTIONS}" target="_blank" rel="noopener">{BIZ["street"]}<br>{BIZ["city"]}</a></div></li>
        <li><span class="icon">{ICONS["phone"]}</span><div><strong>Phone</strong><a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a></div></li>
        <li><span class="icon">{ICONS["mail"]}</span><div><strong>Email</strong><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></div></li>
        <li><span class="icon">{ICONS["clock"]}</span><div><strong>Hours</strong><table class="hours"><tr><td>Monday–Friday</td><td>8 AM – 5 PM</td></tr><tr><td>Saturday–Sunday</td><td>Closed</td></tr></table></div></li>
      </ul>
      <iframe class="map" title="Map to Alert Automotive" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q={MAP_Q}&output=embed"></iframe>
      <p style="margin-top:1rem"><a class="btn dark" href="{DIRECTIONS}" target="_blank" rel="noopener">Get directions</a></p>
    </aside>
  </div>
</div></section>
'''
page("contact.html", "Contact & Schedule Service | Alert Automotive, Hudson FL",
     "Request an auto repair appointment at Alert Automotive, 9824 Ideal Ln Suite 103, Hudson, FL. Call (352) 515-3660.",
     contact)

# ---------------- THANK YOU ----------------
thanks = f'''
<section class="hero small"><div class="wrap">
  <span class="eyebrow">Request received</span>
  <h1>Thanks — we've got it.</h1>
  <p class="lede">We'll reach out to confirm, usually the same business day. If it's urgent, give us a call.</p>
  <div class="btn-row"><a class="btn" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a><a class="btn ghost" href="/">Back to home</a></div>
</div></section>
'''
page("thank-you.html", "Thank You | Alert Automotive", "Your request was received.", thanks, current="")

# 404
notfound = '''
<section class="hero small"><div class="wrap">
  <span class="eyebrow">Error 404</span>
  <h1>Wrong turn.</h1>
  <p class="lede">That page doesn't exist. Let's get you back on the road.</p>
  <div class="btn-row"><a class="btn" href="/">Home</a><a class="btn ghost" href="/contact">Contact us</a></div>
</div></section>
'''
page("404.html", "Page not found | Alert Automotive", "Page not found.", notfound, current="")

(OUT / "assets" / "favicon.svg").write_text(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
print("built", sorted(p.name for p in OUT.glob("*.html")))
