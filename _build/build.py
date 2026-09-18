#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the ATOMAT LAB shop from content.py into out/.

    python3 _build/build.py           # regenerates the pages in the repo root
    python3 _build/build.py --check   # same, plus verifies every media path and link resolves
"""
from __future__ import annotations

import json
import math
import pathlib
import re
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import content as C  # noqa: E402

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
OUT = ROOT          # the pages are generated straight into the repo root
MEDIA = "media"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@400;500&display=swap">')

NAV = [("index.html", "Home"), ("shop.html", "Shop"), ("about.html", "About"),
       ("contact.html", "Contact")]


# ---------------------------------------------------------------- small helpers
def tag(text: str, kind: str = "") -> str:
    cls = "tag" + (" " + kind if kind else "")
    return f'<span class="{cls}">{text}</span>'


def sm(path: str) -> str:
    """The 800px variant that sits next to every imported photo."""
    p = pathlib.PurePosixPath(path)
    return str(p.with_suffix("")) + ".sm" + p.suffix


def media(path: str, small: bool = False) -> str:
    return f"{MEDIA}/{sm(path) if small else path}"


def ruler(lo: int = 10, hi: int = 17000, light: bool = False) -> str:
    """Logarithmic frequency axis used in place of a plain rule."""
    l0, l1 = math.log10(lo), math.log10(hi)
    parts = []
    labels = {10: "10 Hz", 100: "100", 1000: "1 k", 10000: "10 k"}
    dec = 1
    while True:
        f0 = 10 ** dec
        if f0 > hi:
            break
        for k in range(1, 10):
            f = k * f0
            if f > hi or f < lo:
                continue
            x = (math.log10(f) - l0) / (l1 - l0) * 100
            major = k == 1
            parts.append(f'<i class="{"maj" if major else ""}" style="left:{x:.2f}%"></i>')
            if major and f in labels and x < 88:
                parts.append(f'<b style="left:calc({x:.2f}% + 4px)">{labels[f]}</b>')
        dec += 1
    parts.append('<i class="maj" style="left:calc(100% - 1px)"></i>')
    khz = f"{hi / 1000:g} kHz"
    parts.append(f'<b class="end" style="left:calc(100% - 4px)">{khz}</b>')
    return f'<div class="ruler{" light" if light else ""}" aria-hidden="true">{"".join(parts)}</div>'


def stage(product: dict, cls: str = "", label: bool = True, lazy: bool = False) -> str:
    """Circular turntable: the rotation loop when there is one, otherwise a photo."""
    inner_cls = f"stage {cls}".strip()
    if product.get("loop"):
        poster = media(product["loop"] + ".jpg")
        body = (f'<video src="{media(product["loop"] + ".mp4")}" poster="{poster}" '
                f'autoplay muted loop playsinline preload="{"none" if lazy else "metadata"}" '
                f'aria-label="{product["name"]} rotating"></video>')
        chip = tag("360° ↻", "acc")
    else:
        inner_cls += " fill"
        lz = ' loading="lazy"' if lazy else ""
        body = f'<img src="{media(product["hero"], small=True)}" alt="{product["name"]}"{lz}>'
        chip = tag(product["serial"], "acc")
    tag_html = f'<span class="stage-tag">{chip}</span>' if label else ""
    return f'<div class="stage-wrap"><div class="{inner_cls}">{body}</div>{tag_html}</div>'


def thumb(product: dict) -> str:
    """Small circular thumb for index rows and cart lines."""
    if product.get("loop"):
        return (f'<video src="{media(product["loop"] + ".mp4")}" poster="{media(product["loop"] + ".jpg")}" '
                f'autoplay muted loop playsinline preload="none" aria-hidden="true"></video>')
    return f'<img src="{media(product["hero"], small=True)}" alt="" loading="lazy">'


def eur(cents: int) -> str:
    return f"€{cents / 100:.0f}" if cents % 100 == 0 else f"€{cents / 100:.2f}"


# ---------------------------------------------------------------- chrome
def head(title: str, desc: str, canonical: str, *, og_image: str, og_type: str = "website",
         extra: str = "") -> str:
    img = f"{C.SITE}/{og_image}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{C.SITE}/{canonical}">
<link rel="icon" href="{media('favicon.png')}">
<link rel="apple-touch-icon" href="{media('logo.png')}">
<meta name="theme-color" content="#e4e3dd">
<meta property="og:site_name" content="ATOMAT LAB">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{C.SITE}/{canonical}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
{FONTS}
<link rel="stylesheet" href="assets/shop.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active: str) -> str:
    cur = lambda h: ' aria-current="page"' if h == active else ""
    links = "".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in NAV)
    mlinks = "".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in NAV)
    return f"""<header class="head">
  <a class="brand" href="index.html" aria-label="ATOMAT LAB home">
    <img src="{media('logo-rotating.png', small=True)}" alt="" width="40" height="40">
    <span>Atomat Lab</span>
  </a>
  <nav class="nav" aria-label="Main">{links}</nav>
  <a class="cart-link" href="cart.html">
    <span>Cart</span><span class="badge zero" data-cart-count>0</span>
  </a>
  <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu">
    <span></span><span></span><span></span>
  </button>
</header>
<div class="menu" id="menu" hidden>
  <div class="menu-top">
    <span class="tag">Atomat Lab</span>
    <button class="menu-close" type="button">Close ×</button>
  </div>
  <nav aria-label="Mobile">{mlinks}<a href="cart.html">Cart <span class="badge zero" data-cart-count style="vertical-align:middle">0</span></a></nav>
  <div class="menu-foot">{ruler()}<p class="note" style="margin-top:14px">{C.TAGLINE} · {C.EMAIL}</p></div>
</div>
"""


def footer() -> str:
    shop = "".join(f'<li><a href="{p["slug"]}.html">{p["name"]}</a></li>' for p in C.PRODUCTS)
    legal = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in
                    [("termsofservice.html", "Terms of service"), ("privacypolicy.html", "Privacy policy"),
                     ("refundpolicy.html", "Refund policy")])
    social = "".join(f'<li><a href="{u}" rel="me noopener" target="_blank">{n} <span class="note">{h}</span></a></li>'
                     for n, h, u in C.SOCIALS[:4])
    return f"""<footer class="foot wrap">
{ruler()}
<div class="foot-grid">
  <div>
    <img class="mark-big" src="{media('textlogo.png', small=True)}" alt="ATOMAT LAB">
    <p class="note" style="margin-top:14px">Handmade in Bucharest<br>Ships to {len(C.SHIPPING)} countries</p>
  </div>
  <div><h3>Instruments</h3><ul>{shop}</ul></div>
  <div><h3>Elsewhere</h3><ul>{social}</ul></div>
  <div><h3>Legal</h3><ul>{legal}</ul>
    <p style="margin-top:14px"><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
  </div>
</div>
<div class="foot-note">
  <span class="note">© ATOMAT LAB — {C.TAGLINE}</span>
  <div class="pay">
    <span class="note">Secure checkout by Stripe</span>
    <img src="{media('pay-visa.png', small=True)}" alt="Visa">
    <img src="{media('pay-stripe.png', small=True)}" alt="Stripe">
    <img src="{media('pay-paypal.png', small=True)}" alt="PayPal">
  </div>
</div>
</footer>
<script src="assets/shop.js"></script>
</body>
</html>
"""


def lightbox() -> str:
    return """<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Photo">
  <button class="lb-close" type="button">Close ×</button>
  <button class="lb-prev" type="button" aria-label="Previous">←</button>
  <img src="" alt="">
  <button class="lb-next" type="button" aria-label="Next">→</button>
  <span class="lb-count"></span>
</div>
"""


def row(p: dict, first: bool = False) -> str:
    specs = "<br>".join(p["grid_specs"])
    return f"""<div class="row" data-cat="{p['cat']}">
  <span class="row-serial">{tag(p['serial'])}</span>
  <a class="row-thumb" href="{p['slug']}.html" aria-label="{p['name']}">{thumb(p)}</a>
  <div class="row-name">
    <a class="t" href="{p['slug']}.html">{p['name']}</a>
    <span class="d">{p['tagline']}</span>
  </div>
  <div class="row-specs">{specs}</div>
  <span class="row-price">{eur(p['price'])}</span>
  <span class="row-buy"><button class="btn{' solid' if first else ''}" type="button" data-add="{p['slug']}">Add to cart +</button></span>
</div>"""


# ---------------------------------------------------------------- pages
def page_home() -> str:
    rows = "".join(row(p, i == 0) for i, p in enumerate(C.PRODUCTS))
    f5 = C.BY_SLUG["field5"]
    reviews = [(p["review"][0], p["name"]) for p in C.PRODUCTS if p.get("review")][:3]
    quotes = "".join(f"""<figure class="card quote">
  <blockquote>“{text}”</blockquote>
  <figcaption>{name} — verified buyer</figcaption>
</figure>""" for text, name in reviews)
    org = json.dumps({
        "@context": "https://schema.org", "@type": "Organization", "name": "ATOMAT LAB",
        "url": C.SITE + "/", "logo": f"{C.SITE}/{media('logo.png')}", "email": C.EMAIL,
        "description": C.HOME_HERO,
        "sameAs": [u for _n, _h, u in C.SOCIALS],
    }, indent=1)
    return (head("ATOMAT LAB — Handmade Contact Microphones · Tools That Listen",
                 "ATOMAT LAB builds handmade contact microphones, EMF microphones and tools for field "
                 "recording, sound art and experimental music. Made to order in the EU, shipped worldwide.",
                 "", og_image=media("field5-shop.jpg"),
                 extra=f'<script type="application/ld+json">{org}</script>\n')
            + header("index.html") + f"""
<main id="main">
<div class="wrap">
  <section class="hero">
    <div class="hero-copy">
      <div class="tags">{tag('Handmade in Bucharest')}{tag(f'Ships to {len(C.SHIPPING)} countries')}</div>
      <h1>Tools<br>that <span class="mark">listen</span></h1>
      <p class="lead">{C.HOME_HERO}</p>
      <div class="hero-cta">
        <a class="btn big solid" href="#instruments">See the instruments ↓</a>
        <a class="btn big" href="{f5['slug']}.html">Start with FIELD5</a>
      </div>
    </div>
    <div class="hero-stage">{stage(f5)}</div>
  </section>

  <section class="sec" id="instruments">
    <div class="sec-head">
      <h2>Instruments</h2>
      <span class="m" data-rowcount>{len(C.PRODUCTS)} items</span>
    </div>
    <div class="rows">{rows}</div>
    <p class="note" style="margin-top:14px">{C.SHIP_NOTE}</p>
  </section>

  <section class="sec">
    <div class="sec-head"><h2>What they hear</h2><span class="m">Recorded with ATOMAT LAB mics</span></div>
    {ruler()}
    <div class="sc" style="margin-top:20px">
      <iframe title="FIELD5 sound samples on SoundCloud" loading="lazy" scrolling="no" frameborder="no"
        allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/soundcloud%253Aplaylists%253A{f5['playlist']}&color=%23151515&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false"></iframe>
      <p class="note" style="margin-top:10px"><a href="https://soundcloud.com/atomat-lab" target="_blank" rel="noopener">ATOMAT LAB on SoundCloud →</a></p>
    </div>
  </section>

  <section class="sec">
    <div class="sec-head"><h2>From the workbench</h2><span class="m">Trial, error, oscilloscopes</span></div>
    <div class="duo">
      <figure style="margin:0"><img src="{media('about-studio.jpg', small=True)}" alt="The ATOMAT LAB workbench" loading="lazy"></figure>
      <div class="card" style="justify-content:space-between">
        <div>
          <h3>Between artistic research and instrument making</h3>
          <p style="margin-top:12px">Every mic is soldered, sealed and tested by hand. Interactive programming,
          electronics, 3D printing and sound research all merge into the same practice.</p>
        </div>
        <a class="btn" href="about.html">Read the story →</a>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="sec-head"><h2>User feedback</h2><span class="m">★★★★★</span></div>
    <div class="trio">{quotes}</div>
  </section>
</div>
</main>
""" + footer())


def page_shop() -> str:
    rows = "".join(row(p) for p in C.PRODUCTS)
    chips = "".join(f'<button type="button" data-filter="{k}" aria-pressed="false">{t}</button>'
                    for k, t in C.FILTERS)
    chips += '<button type="button" class="soon" disabled>Preamps — soon</button>'
    return (head("Shop — Contact Microphones &amp; EMF Mics | ATOMAT LAB",
                 "Shop handmade contact microphones, submersible piezo mics and EMF microphones for field "
                 "recording and experimental sound. Built to order, shipped from the EU.",
                 "shop.html", og_image=media("field5-shop.jpg"))
            + header("shop.html") + f"""
<main id="main">
<div class="wrap">
  <section style="padding:clamp(34px,5vw,72px) 0 0">
    <div class="tags" style="margin-bottom:18px">{tag('Built to order')}{tag('14-day EU returns')}</div>
    <h1 style="font-size:clamp(38px,6vw,84px)">Instruments</h1>
    <p class="lead" style="max-width:52ch;margin-top:18px">Handmade contact microphones and EMF microphones
    for field recording and experimental sound. Every unit is built after you order it, then tested before it ships.</p>
  </section>

  <section class="sec">
    <div class="sec-head">
      <div class="filters">{chips}</div>
      <span class="m" data-rowcount>{len(C.PRODUCTS)} items</span>
    </div>
    <div class="rows">{rows}</div>
    <p class="note" style="margin-top:14px">{C.SHIP_NOTE}</p>
  </section>

  <section class="sec">
    {ruler()}
    <div class="trio" style="margin-top:24px">
      <div class="card"><span class="m">01</span><h3>Pick a mic</h3><p>CRT1 to start, CRT2 for water and
      velcro, ERT for electronics, FIELD5 when you want phantom power and XLR.</p></div>
      <div class="card"><span class="m">02</span><h3>It gets built</h3><p>Soldered, epoxy-sealed and tested
      by hand in Bucharest, usually within a few days of the order.</p></div>
      <div class="card"><span class="m">03</span><h3>Plug in and listen</h3><p>Straight into any recorder or
      interface. No preamp needed unless the mic asks for phantom power.</p></div>
    </div>
  </section>
</div>
</main>
""" + footer())


def page_product(p: dict) -> str:
    specs = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in p["specs"])
    values = "".join(f'<div class="card"><span class="m">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>'
                     for i, (t, d) in enumerate(p["values"]))
    gal = "".join(f"""<figure><img src="{media(g, small=True)}" data-full="{media(g)}"
      alt="{p['name']} — photo {i + 1}" loading="lazy"></figure>""" for i, g in enumerate(p["gallery"]))
    thumbs = "".join(f"""<button type="button" data-thumb="{media(g)}" data-alt="{p['name']} — photo {i + 1}"
      aria-label="Show photo {i + 1}"><img src="{media(g, small=True)}" alt="" loading="lazy"></button>"""
                     for i, g in enumerate(p["gallery"][:4]))
    quote = ""
    if p.get("review"):
        quote = f"""<figure class="quote">
  <blockquote>“{p['review'][0]}”</blockquote><figcaption>{p['review'][1]}</figcaption></figure>"""
    if p.get("playlist"):
        samples = f"""<div class="sc">
  <iframe title="{p['name']} sound samples on SoundCloud" loading="lazy" scrolling="no" frameborder="no"
    allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/soundcloud%253Aplaylists%253A{p['playlist']}&color=%23151515&auto_play=false&hide_related=true&show_comments=false&show_user=true&show_reposts=false&show_teaser=false"></iframe>
  <p class="note" style="margin-top:10px"><a href="{p['playlist_url']}" target="_blank" rel="noopener">ATOMAT LAB · {p['playlist_name']} →</a></p>
</div>"""
    else:
        samples = '<div class="soon-box"><span class="m">Sound samples — coming soon</span></div>'
    schema = json.dumps({
        "@context": "https://schema.org", "@type": "Product", "name": p["name"],
        "sku": p["serial"], "image": f"{C.SITE}/{media(p['gallery'][0])}",
        "description": p["schema_desc"], "brand": {"@type": "Brand", "name": "ATOMAT LAB"},
        "url": f"{C.SITE}/{p['slug']}.html",
        "offers": {
            "@type": "Offer", "url": f"{C.SITE}/{p['slug']}.html", "priceCurrency": "EUR",
            "price": f"{p['price'] / 100:.2f}", "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
            "shippingDetails": {"@type": "OfferShippingDetails",
                                "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "EU"}},
        },
    }, indent=1)
    spec_ruler = ruler(*p["freq"]) if p.get("freq") else ""
    return (head(p["seo_title"], p["seo_desc"], f"{p['slug']}.html",
                 og_image=media(p["gallery"][0]), og_type="product",
                 extra=f'<script type="application/ld+json">{schema}</script>\n')
            + header("shop.html") + f"""
<main id="main">
<div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb">
    <a href="shop.html">Instruments</a><span>/</span><span>{p['name']}</span>
    <span style="margin-left:auto">{tag(p['serial'])}</span>
  </nav>

  <section class="prod">
    <div class="prod-media">
      <div data-main-media>{stage(p, label=True)}</div>
      <div class="prod-thumbs">{thumbs}</div>
    </div>
    <div class="prod-copy">
      <div class="tags">{tag(p['tagline'])}</div>
      <h1>{p['name']}</h1>
      <p class="lead">{p['claim']}</p>
      <p>{p['body']}</p>
      <div class="buy">
        <span class="price">{eur(p['price'])}</span>
        <button class="btn big solid" type="button" data-add="{p['slug']}">Add to cart +</button>
        <a class="btn big" href="cart.html">Cart →</a>
      </div>
      <p class="note">{C.SHIP_NOTE}</p>
      {quote}
    </div>
  </section>

  <section class="sec">
    <div class="duo">
      <div>
        <div class="sec-head"><h2>Specifications</h2></div>
        {spec_ruler}
        <table class="spec-table">{specs}</table>
        <h3 style="margin-top:28px">What’s included</h3>
        <p style="margin-top:8px">{p['included']}</p>
      </div>
      <div>
        <div class="sec-head"><h2>Sound samples</h2></div>
        {samples}
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="trio">{values}</div>
  </section>

  <section class="sec">
    <div class="sec-head"><h2>Gallery</h2><span class="m">{len(p['gallery'])} photos · click to enlarge</span></div>
    <div class="gal">{gal}</div>
  </section>

  <section class="sec">
    {ruler()}
    <div class="sec-head" style="margin-top:18px"><h2>More instruments</h2><a class="btn" href="shop.html">All →</a></div>
    <div class="rows">{"".join(row(o) for o in C.PRODUCTS if o['slug'] != p['slug'])}</div>
  </section>
</div>
</main>
""" + lightbox() + footer())


def page_cart() -> str:
    opts = "".join(f'<option value="{c}">{n} — {eur(f)}</option>' for c, n, f in C.SHIPPING)
    return (head("Cart — ATOMAT LAB", "Your ATOMAT LAB cart: handmade contact and EMF microphones, "
                                      "built to order and shipped from Romania.",
                 "cart.html", og_image=media("field5-shop.jpg"))
            + header("cart.html") + f"""
<main id="main">
<div class="wrap">
  <section style="padding:clamp(34px,5vw,64px) 0 0">
    <h1 style="font-size:clamp(38px,6vw,78px)">Cart</h1>
  </section>
  <section class="sec">
    <div class="cart-grid">
      <div>
        <div class="rows" id="cartList"></div>
        <p class="note" style="margin-top:16px">{C.SHIP_NOTE}</p>
      </div>
      <aside class="totals">
        <div class="field">
          <label for="country">Shipping country</label>
          <select id="country" name="country">
            <option value="">Select a country…</option>
            {opts}
          </select>
          <p class="err" id="shipErr" hidden>Please choose a shipping country.</p>
        </div>
        <dl>
          <dt>Subtotal</dt><dd id="sub">€0.00</dd>
          <dt>Shipping</dt><dd id="fee">—</dd>
        </dl>
        <div class="grand"><span class="m">Total</span><b id="grand">€0.00</b></div>
        <button class="btn big solid block" type="button" id="checkout" disabled>Checkout →</button>
        <p class="note">Payments handled by Stripe. Prices and shipping are confirmed on the
        server, so what you see here is what you pay.</p>
      </aside>
    </div>
  </section>
</div>
</main>
""" + footer())


def page_about() -> str:
    paras = "".join(f"<p>{t}</p>" for t in C.ABOUT)
    return (head("About — ATOMAT LAB | Handmade Listening Tools",
                 "The story of ATOMAT LAB: handmade microphones and listening tools born from interactive "
                 "sound installations, texture recording and DIY electronics.",
                 "about.html", og_image=media("about-studio.jpg"))
            + header("about.html") + f"""
<main id="main">
<div class="wrap">
  <section style="padding:clamp(34px,5vw,72px) 0 0">
    <div class="tags" style="margin-bottom:18px">{tag('Since 2020')}{tag('Bucharest')}</div>
    <h1 style="font-size:clamp(38px,6vw,84px)">Listening to<br>what <span class="mark">vibrates</span></h1>
  </section>

  <section class="sec">
    <div class="duo">
      <div class="prose">{paras}</div>
      <div style="display:flex;flex-direction:column;gap:var(--gap)">
        <figure style="margin:0">
          <img src="{media('about-studio.jpg', small=True)}" alt="Hand-stencilled ATOMAT LAB FIELD5 sign" loading="lazy">
          <figcaption class="note" style="margin-top:8px">Stencilled by hand</figcaption>
        </figure>
        <figure style="margin:0">
          <video src="{media('loop-trt.mp4')}" poster="{media('loop-trt.jpg')}" autoplay muted loop playsinline
            preload="none" aria-label="TRT aural prototype"></video>
          <figcaption class="note" style="margin-top:8px">TRT — recording texture rather than sound</figcaption>
        </figure>
        <figure style="margin:0">
          <video src="{media('loop-osc.mp4')}" poster="{media('loop-osc.jpg')}" autoplay muted loop playsinline
            preload="none" aria-label="Oscilloscope reading a preamp"></video>
          <figcaption class="note" style="margin-top:8px">Seeing the signal before hearing it</figcaption>
        </figure>
        <figure style="margin:0">
          <img src="{media('about-beyondthenoise.jpg', small=True)}" alt="Beyond the Noise" loading="lazy">
          <figcaption class="note" style="margin-top:8px">Beyond the Noise</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="sec">
    {ruler()}
    <div class="sec-head" style="margin-top:18px"><h2>The instruments</h2><a class="btn" href="shop.html">Shop →</a></div>
    <div class="rows">{"".join(row(p) for p in C.PRODUCTS)}</div>
  </section>
</div>
</main>
""" + footer())


def page_contact() -> str:
    items = "".join(f"""<div class="card">
  <span class="m">{n}</span>
  <a class="x" style="font-size:22px" href="{u}" target="_blank" rel="noopener">{h}</a>
</div>""" for n, h, u in C.SOCIALS)
    return (head("Contact — ATOMAT LAB",
                 "Contact ATOMAT LAB about handmade contact microphones, EMF mics, custom builds and workshops.",
                 "contact.html", og_image=media("about-studio.jpg"))
            + header("contact.html") + f"""
<main id="main">
<div class="wrap">
  <section style="padding:clamp(34px,5vw,72px) 0 0">
    <h1 style="font-size:clamp(38px,6vw,84px)">Say <span class="mark">hello</span></h1>
    <p class="lead" style="max-width:48ch;margin-top:20px">{C.CONTACT_INTRO}</p>
    <p style="margin-top:24px"><a class="btn big solid" href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
  </section>
  <section class="sec">
    {ruler()}
    <div class="trio" style="margin-top:24px">{items}</div>
  </section>
</div>
</main>
""" + footer())


def page_success() -> str:
    return (head("Order confirmed — ATOMAT LAB", "Your ATOMAT LAB order is confirmed.",
                 "success.html", og_image=media("field5-shop.jpg"))
            + header("index.html") + f"""
<main id="main">
<div class="wrap">
  <section style="padding:clamp(40px,7vw,110px) 0 0;max-width:62ch">
    <div class="tags" style="margin-bottom:18px">{tag('Paid', 'acc')}</div>
    <h1 style="font-size:clamp(38px,6vw,84px)">Thank <span class="mark">you</span></h1>
    <p class="lead" style="margin-top:22px">Your order is in. A confirmation is on its way to your inbox from
    Stripe, and your instrument goes on the bench next — handmade to order, usually shipped within a few days.</p>
    <p style="margin-top:8px">If anything looks wrong, or you want to add to the order before it ships,
    write to <a href="mailto:{C.EMAIL}" style="text-decoration:underline">{C.EMAIL}</a>.</p>
    <div class="hero-cta" style="margin-top:28px">
      <a class="btn big solid" href="shop.html">Back to the instruments</a>
      <a class="btn big" href="index.html">Home</a>
    </div>
  </section>
  <section class="sec">{ruler()}</section>
</div>
</main>
""" + '<script>try { localStorage.removeItem("atomat_cart"); } catch (e) {}</script>\n' + footer())


POLICIES = [("privacypolicy.html", "Privacy policy", "Privacy Policy — ATOMAT LAB",
             "How ATOMAT LAB collects, uses and protects your personal information."),
            ("refundpolicy.html", "Refund policy", "Refund Policy — ATOMAT LAB",
             "Returns, refunds and the 14-day EU withdrawal period for ATOMAT LAB orders."),
            ("termsofservice.html", "Terms of service", "Terms of Service — ATOMAT LAB",
             "The terms that apply when you buy from ATOMAT LAB.")]


def page_policy(fname: str, label: str, title: str, desc: str) -> str:
    src = HERE / "policy" / fname
    body = src.read_text(encoding="utf-8").strip() if src.exists() else "<p>—</p>"
    # the extracted body carries its own <h1>; drop it, the page supplies one
    body = re.sub(r"<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    return (head(title, desc, fname, og_image=media("field5-shop.jpg"))
            + header("index.html") + f"""
<main id="main">
<div class="wrap">
  <section style="padding:clamp(34px,5vw,64px) 0 0">
    <div class="tags" style="margin-bottom:16px">{tag('Legal')}</div>
    <h1 style="font-size:clamp(32px,4.6vw,60px)">{label}</h1>
  </section>
  <section class="sec">
    {ruler()}
    <div class="prose" style="margin-top:28px">{body}</div>
  </section>
</div>
</main>
""" + footer())


# ---------------------------------------------------------------- assets
def js_catalog() -> str:
    return json.dumps({p["slug"]: {"name": p["name"], "serial": p["serial"], "price": p["price"],
                                   "thumb": media(p["hero"], small=True)}
                       for p in C.PRODUCTS}, indent=2)


def js_shipping() -> str:
    return json.dumps({c: f for c, _n, f in C.SHIPPING}, indent=2)


def api_catalog() -> str:
    return json.dumps({p["slug"]: {"name": p["name"], "tagline": p["tagline"], "serial": p["serial"],
                                   "price": p["price"], "image": media(p["gallery"][0], small=True)}
                       for p in C.PRODUCTS}, indent=2)


def api_shipping() -> str:
    return json.dumps({c: {"name": n, "amount": f} for c, n, f in C.SHIPPING}, indent=2)


def sitemap() -> str:
    urls = [""] + ["shop.html", "about.html", "contact.html"] + [f"{p['slug']}.html" for p in C.PRODUCTS] \
           + ["termsofservice.html", "privacypolicy.html", "refundpolicy.html"]
    body = "".join(f"  <url><loc>{C.SITE}/{u}</loc></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


# ---------------------------------------------------------------- driver
def build() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "api").mkdir(exist_ok=True)

    pages = {
        "index.html": page_home(),
        "shop.html": page_shop(),
        "cart.html": page_cart(),
        "about.html": page_about(),
        "contact.html": page_contact(),
        "success.html": page_success(),
    }
    for p in C.PRODUCTS:
        pages[f"{p['slug']}.html"] = page_product(p)
    for fname, label, title, desc in POLICIES:
        pages[fname] = page_policy(fname, label, title, desc)

    for name, html in pages.items():
        (OUT / name).write_text(html, encoding="utf-8")

    js = (HERE / "shop.js.tpl").read_text(encoding="utf-8")
    js = js.replace("__CATALOG__", js_catalog()).replace("__SHIPPING__", js_shipping())
    (OUT / "assets" / "shop.js").write_text(js, encoding="utf-8")

    api = (HERE / "checkout.js.tpl").read_text(encoding="utf-8")
    api = api.replace("__CATALOG__", api_catalog()).replace("__SHIPPING__", api_shipping())
    (OUT / "api" / "create-checkout-session.js").write_text(api, encoding="utf-8")

    (OUT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {C.SITE}/sitemap.xml\n", encoding="utf-8")

    print(f"{len(pages)} pages + assets/shop.css, assets/shop.js, api/create-checkout-session.js")
    return pages


def check(pages: dict, media_dir: pathlib.Path | None) -> int:
    """Verify every local href/src resolves, and every media file exists if we can see them."""
    bad = 0
    names = set(pages) | {"assets/shop.css", "assets/shop.js", "sitemap.xml", "robots.txt"}
    for name, html in pages.items():
        refs = re.findall(r'(?:href|src|data-full|data-thumb)="([^"]+)"', html)
        for r in refs:
            if r.startswith(("http", "mailto:", "#", "data:", "/api/")):
                continue
            target, _, frag = r.partition("#")
            if not target:
                continue
            if target.startswith(MEDIA + "/"):
                if media_dir is None:
                    continue
                if not (media_dir / target[len(MEDIA) + 1:]).exists():
                    print(f"  MISSING MEDIA  {name} -> {target}")
                    bad += 1
                continue
            if target not in names:
                print(f"  DEAD LINK      {name} -> {target}")
                bad += 1
        for frag in re.findall(r'href="#([^"]+)"', html):
            if f'id="{frag}"' not in html:
                print(f"  DEAD ANCHOR    {name} -> #{frag}")
                bad += 1
    print("check: " + ("ok" if not bad else f"{bad} problem(s)"))
    return bad


if __name__ == "__main__":
    pages = build()
    if "--check" in sys.argv:
        md = OUT / MEDIA
        sys.exit(1 if check(pages, md if md.exists() else None) else 0)
