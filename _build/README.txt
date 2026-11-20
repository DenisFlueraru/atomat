ATOMAT LAB shop — how this site is built
========================================

The pages in the repo root are GENERATED. Don't hand-edit them; edit the
sources here and re-run the build, or your change disappears next time.

    python3 _build/optimise.py     # DRIVE-IMAGES/  ->  media/   (photos + loops)
    python3 _build/build.py        # _build/        ->  the pages
    python3 _build/build.py --check   # same, plus verify every link and media path

Where things live
-----------------
_build/content.py   All copy, prices (in euro cents), specs, shipping table.
                    THIS is where you change a price or add a product.
_build/build.py     Turns content.py into the 14 pages + assets + the API function.
_build/shop.js.tpl  Cart / menu / filters / lightbox. The catalogue is injected.
_build/checkout.js.tpl  The Stripe function. The catalogue is injected here too.
_build/policy/      The three legal pages' body text (plain HTML, edit freely).
_build/optimise.py  Imports and resizes photos, and turns the rotation GIFs into
                    small square MP4 loops. DRIVE-IMAGES/ is gitignored.
assets/shop.css     Hand-written; edit directly, the build only copies it.

Why prices live in content.py
-----------------------------
The build writes the same price table into assets/shop.js (for display) and
into api/create-checkout-session.js (for charging). The browser only ever posts
{slug, qty} + a country code, so a tampered request can't change what a
customer pays. Change a price in content.py and re-run the build so both sides
stay in step.

Adding a product
----------------
1. Put its photos in DRIVE-IMAGES/<NAME>/ and add them to PHOTOS in optimise.py.
2. Add a dict to PRODUCTS in content.py (copy an existing one).
3. python3 _build/optimise.py && python3 _build/build.py --check

Fair kiosk (atomatlab.com/fair)
-------------------------------
An iPad page for fairs: start screen, recordings to play, how contact and EMF mics
work, the mics with prices, and QR codes. It is built with the rest of the site, so
prices and "sold out" always match the shop.

1. Put recordings in fair/sounds/ (.m4a or .mp3, 15–30 s). The file names, titles and
   which mic made each one are in FAIR_SOUNDS at the bottom of content.py; edit freely.
2. python3 _build/build.py --check. It lists any sound that is still missing; missing
   sounds are simply left off the page.
3. Push. On the iPad, open atomatlab.com/fair in Safari on good Wi-Fi, then Share →
   Add to Home Screen and open it from that icon (fullscreen, no browser bars).
4. Hold the spinning logo for 2 seconds to open Setup: it says whether every file is
   saved on the iPad for offline use, with a button to save them all.

fair/fair.css and fair/fair.js are hand-written. fair/index.html, fair/sw.js and
fair/manifest.webmanifest are generated. The offline cache name is a hash of every
file the page uses, so after changing anything just rebuild and push: the iPad picks
up the new version the next time it opens the page online.
