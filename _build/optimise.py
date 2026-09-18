#!/usr/bin/env python3
"""Import the ATOMAT LAB shop photos from DRIVE-IMAGES into a committed media/ folder.

Full-size copies are capped at 1600px and a .sm.jpg variant at 800px is written next
to each one for grids and phones. Product rotation GIFs (15-25MB) become looping MP4s
with a JPEG poster. Re-runs skip files that are already up to date.
"""
import pathlib, subprocess, sys
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "DRIVE-IMAGES"
OUT = ROOT / "media"

# source (relative to DRIVE-IMAGES)  ->  name in media/
PHOTOS = {
    # FIELD5
    "FIELD5/FIELD51.jpg":               "field5-1.jpg",
    "FIELD5/FIELD5_1.JPG":              "field5-2.jpg",
    "FIELD5/FIELD5CLOSEUP.jpg":         "field5-closeup.jpg",
    "FIELD5/FIELD5_NUTCLOSEUP.jpg":     "field5-nut.jpg",
    "FIELD5/FIELD5BOX1.jpg":            "field5-box.jpg",
    "FIELD5/IMG_0060.JPG":              "field5-3.jpg",
    "FIELD5/IMG_0082.JPG":              "field5-4.jpg",
    "FIELD5/IMG_0083.JPG":              "field5-5.jpg",
    "SHOP SECTION/Copy of FIELD5_4.JPG":"field5-shop.jpg",
    # CRT2
    "CRT2/CRT2_FRONT.jpg":              "crt2-1.jpg",
    "CRT2/CRT2FRONT.jpg":               "crt2-2.jpg",
    "SHOP SECTION/CRT2.png":            "crt2-shop.jpg",
    # CRT1
    "CRT1/CRT1.jpg":                    "crt1-1.jpg",
    "CRT1/CRT1_BACK.jpg":               "crt1-2.jpg",
    "CRT1/CRT1_CASE FRONT.jpg":         "crt1-3.jpg",
    "SHOP SECTION/CRT1.png":            "crt1-shop.jpg",
    # ERT
    "ERT1/ERT1.jpg":                    "ert-1.jpg",
    "ERT1/IMG_1874.JPG":                "ert-2.jpg",
    "ERT1/IMG_1875.JPG":                "ert-3.jpg",
    "SHOP SECTION/ERT1.png":            "ert-shop.jpg",
    # RAINCATCHER
    "RAINCATCHER/1.JPG":                "raincatcher-1.jpg",
    "RAINCATCHER/1v2.JPG":              "raincatcher-2.jpg",
    "RAINCATCHER/2.JPG":                "raincatcher-3.jpg",
    "RAINCATCHER/4.JPG":                "raincatcher-4.jpg",
    # studio / about
    "ABOUT/ATOMATLAB.jpg":              "about-studio.jpg",
    "ABOUT/BeyondtheNoise.JPG":         "about-beyondthenoise.jpg",
    "HOME PAGE/Copy of SOUND10.JPG":    "about-sound.jpg",
    # brand marks (kept as PNG, transparency matters)
    "IMAGES/atomatlab.png":             "logo.png",
    "IMAGES/atomatlabrotating.png":     "logo-rotating.png",
    "IMAGES/atomatfavicon.png":         "favicon.png",
    "IMAGES/FIELD5.png":                "field5-cutout.png",
    "HOME PAGE/textlogo.png":           "textlogo.png",
    "HOME PAGE/textlogowhite.png":      "textlogo-white.png",
    "LOGOS/visa.png":                   "pay-visa.png",
    "LOGOS/stripe.png":                 "pay-stripe.png",
    "LOGOS/pypl.png":                   "pay-paypal.png",
    "MERCH/tricou negru.png":           "merch-tee.jpg",
}

# GIF -> looping MP4 (+ .jpg poster).
# square=True renders the portrait rotation onto a square canvas, filling the sides with a
# heavily blurred, desaturated copy of the same frame. The product is never cropped and the
# clip fills the circular stage on the site edge to edge, with no visible rectangle.
LOOPS = {
    "GIFS/FIELD5_GIF.gif":  ("loop-field5", True),
    "GIFS/CRT2_GIF.gif":    ("loop-crt2", True),
    "GIFS/CRT1_GIF.gif":    ("loop-crt1", True),
    "GIFS/ERT_GIF.gif":     ("loop-ert", True),
    "GIFS/OSC_PREAMP.gif":  ("loop-osc", False),   # shown as a plain rectangle on the about page
    "ABOUT/TRT_AURAL.gif":  ("loop-trt", False),
}
SQ = 800

MAXW, SMW, Q = 1600, 800, 82
# names that never render large: cap them tighter
CAPS = {"favicon.png": (134, 134), "pay-visa.png": (400, 400), "pay-stripe.png": (400, 400),
        "pay-paypal.png": (400, 400), "textlogo.png": (900, 600), "textlogo-white.png": (900, 600),
        "logo.png": (600, 400), "logo-rotating.png": (900, 600)}


def newer(src, dst):
    return not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime


def do_photo(src, name):
    dst = OUT / name
    sm = OUT / (dst.stem + ".sm" + (".png" if dst.suffix.lower() == ".png" else ".jpg"))
    if not newer(src, dst) and sm.exists():
        return "skip"
    im = ImageOps.exif_transpose(Image.open(src))
    keep_alpha = dst.suffix.lower() == ".png" and im.mode in ("RGBA", "LA", "P")
    if keep_alpha:
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    big, small = CAPS.get(name, (MAXW, SMW))
    for target, path in ((big, dst), (small, sm)):
        o = im.copy()
        if o.width > target:
            o = o.resize((target, round(o.height * target / o.width)), Image.LANCZOS)
        if path.suffix.lower() == ".png":
            o.save(path, "PNG", optimize=True)
        else:
            o.convert("RGB").save(path, "JPEG", quality=Q, optimize=True, progressive=True)
    return "ok"


def do_loop(src, stem, square):
    mp4, poster = OUT / (stem + ".mp4"), OUT / (stem + ".jpg")
    if not newer(src, mp4) and poster.exists():
        return "skip"
    if square:
        vf = (f"[0:v]fps=20,split=2[a][b];"
              f"[a]scale={SQ}:{SQ},gblur=sigma=44,eq=brightness=0.06:saturation=0.3:contrast=0.8[bg];"
              f"[b]scale=-2:{SQ}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:0,format=yuv420p")
        args = ["-filter_complex", vf]
    else:
        args = ["-vf", "scale='min(1000,iw)':-2:flags=lanczos,fps=20,format=yuv420p"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
                    "-movflags", "+faststart", "-an", *args,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "27",
                    str(mp4)], check=True)
    # the poster is the encoded video's own first frame, so it matches it exactly
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4),
                    "-frames:v", "1", "-q:v", "4", str(poster)], check=True)
    return "ok"


def main():
    OUT.mkdir(exist_ok=True)
    missing, done, skipped = [], 0, 0
    for rel, name in PHOTOS.items():
        src = SRC / rel
        if not src.exists():
            missing.append(rel); continue
        r = do_photo(src, name)
        done += r == "ok"; skipped += r == "skip"
        print(f"  {r:4}  {name}")
    for rel, (stem, square) in LOOPS.items():
        src = SRC / rel
        if not src.exists():
            missing.append(rel); continue
        r = do_loop(src, stem, square)
        done += r == "ok"; skipped += r == "skip"
        print(f"  {r:4}  {stem}.mp4")
    print(f"\n{done} written, {skipped} up to date")
    if missing:
        print("MISSING:", *missing, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
