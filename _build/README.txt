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
