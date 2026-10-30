# -*- coding: utf-8 -*-
"""All copy, prices and media references for the ATOMAT LAB shop.

Prices are in euro cents and are the single source of truth: build.py writes them
into the pages AND into api/create-checkout-session.js, so the server never has to
trust a price that came from a browser.
"""

SITE = "https://atomatlab.com"
EMAIL = "contact@atomatlab.com"
TAGLINE = "tools that listen"

SOCIALS = [
    ("Instagram", "@atomatlab", "https://instagram.com/atomatlab"),
    ("YouTube", "@atomatlab", "https://youtube.com/@atomatlab"),
    ("SoundCloud", "atomat-lab", "https://soundcloud.com/atomat-lab"),
    ("TikTok", "@atomatlab", "https://tiktok.com/@atomatlab"),
    ("Personal page", "denisflueraru.com", "https://denisflueraru.com"),
]

SHIP_NOTE = "Handmade in Romania · in stock, ships within a few days · 14-day EU returns"

# ---------------------------------------------------------------- products
# price: euro cents.  freq: (low, high) in Hz for the spec ruler.
PRODUCTS = [
    dict(
        slug="field5", name="FIELD5", serial="AL-F5", price=15000, cat="mic",
        tagline="48V phantom-powered contact microphone",
        seo_title="FIELD5 — 48V Phantom Powered Contact Microphone | ATOMAT LAB",
        seo_desc=("FIELD5 is a submersible 48V phantom-powered contact microphone with Neutrik XLR "
                  "output for field recording and sound design. Includes magnet, suction cup and "
                  "velcro mounts. Handmade in the EU."),
        schema_desc=("Submersible 48V phantom-powered contact microphone with Neutrik XLR output, "
                     "epoxy-sealed and copper-shielded, for field recording and sound design. "
                     "Includes magnet, suction cup, probe and velcro mounts."),
        claim=("FIELD5 is a 48V phantom-powered contact microphone designed to listen in any "
               "circumstance. With the included accessories it fits most structures and objects."),
        body=("Use it for field recording, sound design and experimental music: attach it to metal, "
              "wood, glass or ice with the included magnet, suction cup or velcro mounts, submerge it "
              "for underwater recording, and capture the vibrations travelling inside materials "
              "directly into any recorder or audio interface with 48V phantom power. Epoxy-sealed and "
              "copper-shielded, with a male Neutrik XLR, it is built for both field and studio work — "
              "no external preamp required."),
        short="Submersible · 48V phantom · Neutrik XLR",
        grid_specs=["Frequency 10 Hz – 17 kHz", "48V phantom powered · 87 g",
                    "2 m cable · mounting kit included", "Submersible"],
        specs=[("Frequency", "10 Hz – 17 kHz"), ("Power", "48V phantom"),
               ("Output", "Male Neutrik XLR"), ("Cable", "2 m"), ("Weight", "87 g"),
               ("Build", "Epoxy-sealed, copper-shielded")],
        freq=(10, 17000),
        included="Microphone, magnet, suction cup, probe, velcro support, extra weight",
        values=[("Waterproof", "Epoxy-coated PCB, submersible for underwater recording."),
                ("Field &amp; studio", "Copper shielding and a male Neutrik XLR output."),
                ("Phantom powered", "Runs on 48V from any recorder — no external preamp.")],
        review=("Very good, as described! Quality and sound top notch!", "Verified buyer"),
        loop="loop-field5", hero="field5-shop.jpg",
        gallery=["field5-1.jpg", "field5-closeup.jpg", "field5-2.jpg", "field5-nut.jpg",
                 "field5-3.jpg", "field5-4.jpg", "field5-5.jpg", "field5-box.jpg"],
        playlist="2189812859", playlist_name="FIELD5 MIC SAMPLES",
        playlist_url="https://soundcloud.com/atomat-lab/sets/field5-mic-samples",
    ),
    dict(
        slug="crt2", name="CRT2", serial="AL-C2", price=6000, cat="mic",
        tagline="Submersible contact microphone",
        seo_title="CRT2 — Submersible Contact Microphone | ATOMAT LAB",
        seo_desc=("CRT2 is a submersible contact microphone with copper shielding and velcro mounting "
                  "for surface and underwater recording. Handmade by ATOMAT LAB, ships from the EU."),
        schema_desc=("Submersible contact microphone with copper shielding, internal capacitor and "
                     "velcro mounting, for surface and underwater recording."),
        claim=("CRT2 is a rugged, multi-purpose contact microphone designed for surface and underwater "
               "sound exploration. A refined version of the CRT1."),
        body=("Sink it in creeks, aquariums and rain barrels as a compact alternative to a hydrophone, "
              "or strap it to pipes, trees, machines and instruments with the velcro strap and textured "
              "mounting base. The copper shielding and internal capacitor tame harsh upper frequencies "
              "for a smoother, more musical tone — a rugged contact microphone for field recording on "
              "land and underwater."),
        short="Copper shielded · velcro mount",
        grid_specs=["Frequency 10 Hz – 15 kHz", "Copper shielding · tamed highs",
                    "1.5 m cable · 55 g", "Submersible"],
        specs=[("Frequency", "10 Hz – 15 kHz"), ("Output", "6.3 mm mono TS jack"),
               ("Cable", "1.5 m"), ("Weight", "55 g"),
               ("Build", "Copper-shielded, velcro hole, textured base")],
        freq=(10, 15000),
        included="CRT2 mic, 1.5 m cable, 6.3 mm mono TS jack, 40 cm velcro strap",
        values=[("Surface &amp; underwater", "Designed for both dry and submerged environments."),
                ("Flexible mounting", "Textured base for Blu Tack and a velcro hole.")
                , ("Refined sound", "Copper shielding and an internal capacitor tame the harsh highs.")],
        review=("Excellent microphone and excellent service by Dennis!", "Verified buyer"),
        loop="loop-crt2", hero="crt2-shop.jpg",
        gallery=["crt2-1.jpg", "crt2-2.jpg", "crt2-shop.jpg"],
        playlist=None, playlist_name=None, playlist_url=None,
    ),
    dict(
        slug="crt1", name="CRT1", serial="AL-C1", price=4500, cat="mic",
        tagline="Entry contact microphone",
        seo_title="CRT1 — Entry Contact Microphone for Experimental Recording | ATOMAT LAB",
        seo_desc=("CRT1 is an affordable waterproof piezo contact microphone — the entry point to "
                  "experimental recording. Capture vibrations inside objects and liquids. Handmade to "
                  "order, ships from the EU."),
        schema_desc=("Waterproof piezo contact microphone for experimental recording, capturing "
                     "vibrations inside solid objects and liquids. 1 m cable, 6.3 mm mono jack."),
        claim=("CRT1 is our entry point into the world of experimental recording. It captures the "
               "vibration hidden inside solid objects and liquids, revealing sound where microphones "
               "normally fail."),
        body=("A piezo contact mic picks up vibration travelling inside materials instead of sound "
              "moving through air — press it against fences, radiators, strings, machines or ice and "
              "record what is happening inside the object. CRT1 is waterproof, weighs only 13 grams, "
              "and plugs straight into any recorder or audio interface with a 6.3 mm jack, making it an "
              "ideal first microphone for experimental field recording."),
        short="Waterproof piezo · 1 m cable",
        grid_specs=["Frequency 10 Hz – 17 kHz", "All-rounder · entry point",
                    "1 m cable · 13 g", "Waterproof"],
        specs=[("Frequency", "10 Hz – 17 kHz"), ("Output", "6.3 mm mono TS jack"),
               ("Cable", "1 m"), ("Weight", "13 g"), ("Build", "Waterproof piezo")],
        freq=(10, 17000),
        included="CRT1, rubber band",
        values=[("Capture the unseen", "Internal vibration, not air pressure."),
                ("Built to explore", "Hands-on, robust and intuitive."),
                ("Entry point", "A good way to break the ice of experimental recording.")],
        review=("Great Mic. I really like it and ordered one more.", "Verified buyer"),
        loop="loop-crt1", hero="crt1-shop.jpg",
        gallery=["crt1-1.jpg", "crt1-2.jpg", "crt1-3.jpg", "crt1-shop.jpg"],
        playlist=None, playlist_name=None, playlist_url=None,
    ),
    dict(
        slug="ert", name="ERT", serial="AL-E1", price=4000, cat="mic",
        tagline="Electromagnetic (EMF) microphone",
        seo_title="ERT — EMF Microphone for Listening to Electronics | ATOMAT LAB",
        seo_desc=("ERT is an electromagnetic (EMF) microphone that makes the hidden fields of "
                  "electronics audible: screens, chargers, routers, motors. For sound design and sonic "
                  "exploration. Handmade in the EU."),
        schema_desc=("Electromagnetic (EMF) microphone with double inductors that makes the "
                     "electromagnetic fields of electronics audible. 1 m cable, 6.3 mm jack."),
        claim=("ERT is an electromagnetic field microphone that reveals the hidden soundscape of "
               "electronic devices — clocks, screens, chargers and invisible ambient hum."),
        body=("Sweep it over laptops, phone screens, chargers, routers, LED signs and motors to record "
              "glitchy tones, data-like pulses and hidden electrical hums. An EMF microphone (inductive "
              "coil pickup) is a staple tool for sound designers, electroacoustic composers and sonic "
              "explorers — plug and play with any recorder or audio interface via 6.3 mm jack."),
        short="Hear screens, chargers, motors",
        grid_specs=["Frequency 10 Hz – 18 kHz", "Clocks, phones, displays, TVs",
                    "Double inductors · 1 m cable", "Plug and play"],
        specs=[("Frequency", "10 Hz – 18 kHz"), ("Pickup", "Double inductors"),
               ("Output", "6.3 mm male jack"), ("Cable", "1 m")],
        freq=(10, 18000),
        included="ERT mic",
        values=[("Electrical fields", "Listens to EMF emissions, not acoustic sound."),
                ("Mobile exploration", "Walk, scan and discover electronic environments."),
                ("Immediate feedback", "Direct connection to recorders and interfaces.")],
        review=("Amazing mic, picks up loads of sounds", "Verified buyer"),
        loop="loop-ert", hero="ert-shop.jpg",
        gallery=["ert-1.jpg", "ert-2.jpg", "ert-3.jpg", "ert-shop.jpg"],
        playlist="2190450968", playlist_name="ERT1 Microphone",
        playlist_url="https://soundcloud.com/atomat-lab",
    ),
    dict(
        slug="raincatcher", name="RAINCATCHER", serial="AL-RC", price=4500, cat="acc",
        tagline="Rain plate for FIELD5",
        seo_title="RAINCATCHER — Rain Recording Attachment for FIELD5 | ATOMAT LAB",
        seo_desc=("Raincatcher is a 30cm resonant plate attachment for the FIELD5 contact microphone, "
                  "built for recording rain and other transient sounds. Handmade by ATOMAT LAB."),
        schema_desc=("30 cm engraved plexiglass resonant plate attachment for the FIELD5 contact "
                     "microphone, built for recording rain and other transients."),
        claim=("A FIELD5 attachment built to isolate and capture transients — rain, birds and similar "
               "sounds."),
        body=("Raindrops strike the 30 cm engraved plexiglass disc and the FIELD5 picks up every impact "
              "directly from the material — a percussion instrument played by the weather. Beyond rain, "
              "the resonant plate isolates other transient sources for close, detailed field recording "
              "of environmental micro-events."),
        short="30 cm resonant plate",
        grid_specs=["Isolates rain and similar transients", "3D-printed support · 4 mm plexi board",
                    "30 cm diameter", "FIELD5 attachment"],
        specs=[("Plate", "30 cm engraved 4 mm plexiglass"), ("Mount", "3D-printed support, M4 knob"),
               ("Fits", "FIELD5 contact microphone"), ("Built for", "Transients and micro-detail")],
        freq=None,
        included="Raincatcher attachment module, support, M4 knob, 4 mm engraved plexi board",
        values=[("Rain as percussion", "Every drop is an impact read straight from the material."),
                ("Isolates transients", "Close, detailed recording of environmental micro-events."),
                ("FIELD5 attachment", "Mounts to the FIELD5 with an M4 knob — no tools needed.")],
        review=None,
        loop=None, hero="raincatcher-2.jpg",
        gallery=["raincatcher-1.jpg", "raincatcher-2.jpg", "raincatcher-3.jpg", "raincatcher-4.jpg"],
        playlist="2189812859", playlist_name="FIELD5 MIC SAMPLES",
        playlist_url="https://soundcloud.com/atomat-lab/sets/field5-mic-samples",
    ),
]

BY_SLUG = {p["slug"]: p for p in PRODUCTS}

FILTERS = [("all", "All"), ("mic", "Microphones"), ("acc", "Accessories")]

# ---------------------------------------------------------------- shipping
# (code, label, cents).  The same table is emitted into the serverless function,
# so a tampered browser request can never change what a customer is charged.
SHIPPING = [
    ("RO", "Romania", 500),
    ("BG", "Bulgaria", 1000),
    ("CZ", "Czech Republic", 1000),
    ("HR", "Croatia", 1000),
    ("CY", "Cyprus", 1000),
    ("GR", "Greece", 1000),
    ("SK", "Slovakia", 1000),
    ("SI", "Slovenia", 1000),
    ("DE", "Germany", 1200),
    ("HU", "Hungary", 1200),
    ("PL", "Poland", 1200),
    ("AT", "Austria", 1300),
    ("FR", "France", 1400),
    ("IT", "Italy", 1400),
    ("PT", "Portugal", 1400),
    ("ES", "Spain", 1500),
    ("EE", "Estonia", 1500),
    ("LV", "Latvia", 1500),
    ("LT", "Lithuania", 1500),
    ("NL", "Netherlands", 1700),
    ("IE", "Ireland", 1800),
    ("LU", "Luxembourg", 2000),
    ("DK", "Denmark", 2000),
    ("BE", "Belgium", 2200),
    ("SE", "Sweden", 2500),
    ("CH", "Switzerland", 2500),
    ("US", "USA", 3000),
    ("GB", "United Kingdom", 2600),
    ("FI", "Finland", 4000),
]

# ---------------------------------------------------------------- pages
HOME_HERO = ("Contact and electromagnetic microphones for field recording, sound design and "
             "experimental music — soldered, sealed and tested by hand in Bucharest.")

ABOUT = [
    ("It all started around 2020, when I began learning about microcontrollers, the MIDI protocol and "
     "software like Max MSP to build interactive sound installations. I was interested in sound not only "
     "as something to be heard, but as something that could react, respond, and exist physically in space."),
    ("While working with interactive systems, I became increasingly curious about what happens before "
     "sound reaches a speaker. Signals, voltages, and vibrations felt more interesting than the final "
     "audio output. Instead of shaping sound digitally, I started looking for ways to listen directly to "
     "physical phenomena, such as movement, friction, resonance, and electrical activity."),
    ("This approach became central during my dissertation, where I developed an early version of what "
     "later became the TRT. It wasn’t designed as a finished product, but as an experiment, a way to "
     "record texture rather than sound in the traditional sense. Many recordings failed, others revealed "
     "unexpected rhythms and structures hidden inside materials. That unpredictability became part of the "
     "process."),
    ("From that point on, the work evolved through trial and error. I began experimenting with different "
     "contact microphones, electromagnetic pickups, materials, and enclosures. I learned to use tools like "
     "oscilloscopes not from an engineering background, but as a way to visually understand sound, "
     "connecting what I heard with what was physically happening."),
    ("ATOMAT LAB sits somewhere between artistic research and instrument making. Interactive programming, "
     "electronics, 3D printing, and sound research all merge into the same practice."),
    ("The first instrument I started selling was the CRT1. What began as a small, self-built tool quickly "
     "received a lot of support and encouraging feedback, which made it clear that this way of listening "
     "resonated with others as well. That response pushed the work forward."),
    ("I started developing other instruments, refining both the electronics and the physical design, while "
     "keeping the same experimental, hands-on approach. This process eventually led to FIELD5, ATOMAT LAB’s "
     "top-of-the-line recording instrument: a phantom-powered contact microphone designed to work reliably "
     "across different environments, while still revealing the subtle textures and vibrations that "
     "conventional microphones often miss."),
]

CONTACT_INTRO = ("We love hearing from collaborators, users and experimental audio enthusiasts. "
                 "Custom builds, workshops, repairs, or just a question about which mic to start with — "
                 "write to us.")
