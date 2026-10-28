#!/usr/bin/env python3
"""Builds every page of demo 2. Run from the repo root: python3 tools/build.py

Copy lives in this file. Before/after pairs live in assets/js/projects.js.
Every page opens on a full-bleed clip or photo (phero), then short sections, then the night footer.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHONE = "802-PAINTER"
TEL = "+18027246837"
EMAIL = "office@pwpvt.com"
IG = "https://www.instagram.com/paintingwithpurposevt/"

NAV = [
    ("work.html", "work"),
    ("services.html", "services"),
    ("about.html", "purpose"),
    ("careers.html", "careers"),
]


def photo(name, alt, cls="", sizes="100vw", eager=False):
    """Client photo with both sizes in srcset."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    p = f"assets/photos/{name}"
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{p}-sm.jpg" srcset="{p}-sm.jpg 900w, {p}-lg.jpg 2000w" '
            f'sizes="{sizes}" alt="{alt}" {load} decoding="async">')


def clip(name, alt, eager=False):
    """Looping drone clip. Muted until the visitor turns sound on. The video source is only
    written once the file exists in assets/video, so the poster still shows until then."""
    src = ROOT / f"assets/video/{name}.mp4"
    source = f'<source src="assets/video/{name}.mp4" type="video/mp4">' if src.exists() else ""
    small = ROOT / f"assets/video/{name}-720.mp4"
    if src.exists() and small.exists():
        source = f'<source src="assets/video/{name}-720.mp4" type="video/mp4" media="(max-width: 900px)">' + source
    return (f'<video class="clip" muted loop playsinline preload="{"auto" if eager else "none"}" '
            f'poster="assets/video/{name}.jpg" aria-label="{alt}">{source}</video>')


def logo(cls=""):
    return f'<span class="logo {cls}" aria-hidden="true"></span>'


def phero(media, label, title, lede="", cls="", cap="", extra=""):
    """Page hero: media fills the screen, the title sits bottom left over a scrim."""
    lede = f'<p class="phero__lede">{lede}</p>' if lede else ""
    cap = f'<p class="label phero__cap">{cap}</p>' if cap else ""
    return f"""<section class="phero {cls}">
  {media}
  <div class="phero__txt">
    <p class="label">{label}</p>
    <h1>{title}</h1>
    {lede}{extra}
  </div>
  {cap}
</section>
"""


def still(name, alt, pos="50% 50%"):
    """Photo hero media, cropped around pos."""
    img = photo(name, alt, eager=True).replace("<img", f'<img style="object-position:{pos}"', 1)
    return f'<div class="media">{img}</div>'


def head(title, desc, page):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0b151c">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/photos/dsc-0179-lg.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="assets/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&family=Inter+Tight:wght@400;500&display=swap">
<link rel="preload" href="assets/logo.svg" as="image" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/main.css">
</head>
<body data-page="{page}">
<a class="skip" href="#main">Skip to content</a>
"""


def header(page):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if page == h.split(".")[0] else ""}>{t}</a></li>'
        for h, t in NAV)
    return f"""<header class="hdr is-dark">
  <a class="hdr__logo" href="index.html" aria-label="Painting With Purpose, home">{logo()}</a>
  <nav class="hdr__nav" id="nav" aria-label="Main">
    <ul>{links}</ul>
    <a class="hdr__cta" href="estimate.html">free estimate</a>
  </nav>
  <button class="hdr__menu" type="button" aria-expanded="false" aria-controls="nav"><span>menu</span></button>
</header>
"""


FOOTER = f"""<footer class="ftr">
  {logo("wm")}
  <div class="ftr__in">
    <div class="ftr__cta">
      <p class="label">(inquire)</p>
      <a class="ftr__big" href="estimate.html">let’s take a <span style="white-space:nowrap">look <span aria-hidden="true">→</span></span></a>
      <p class="ftr__sub">A free walkthrough and a written estimate. Or call <a href="tel:{TEL}">{PHONE}</a>.</p>
    </div>
    <div class="ftr__grid">
      <a href="index.html" aria-label="Painting With Purpose, home">{logo("ftr__logo")}</a>
      <div><p class="label">studio</p><p>Residential &amp; commercial painting<br>Greater Burlington, Vermont</p></div>
      <div><p class="label">contact</p><p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{IG}">@paintingwithpurposevt</a></p></div>
      <div><p class="label">pages</p><p>{'<br>'.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<br><a href="estimate.html">free estimate</a></p></div>
    </div>
    <p class="ftr__fine"><span>© 2026 Painting With Purpose LLC</span><span>Part of every job goes to CVOEO.</span></p>
  </div>
</footer>
<button class="snd" type="button" aria-pressed="false" hidden><span class="snd__bars" aria-hidden="true"><i></i><i></i><i></i></span><span class="snd__t">sound off</span></button>
<script src="assets/js/site.js"></script>
<script src="assets/js/cine.js"></script>
</body>
</html>
"""


def sechead(label, title, hid, aside=""):
    aside = f'<p class="aside">{aside}</p>' if aside else ""
    return f'<div class="head"><p class="label">{label}</p><h2 id="{hid}">{title}</h2>{aside}</div>'


def write(name, html):
    (ROOT / name).write_text(html)
    print("wrote", name)


# --------------------------------------------------------------------------
# Data

PROJECTS = [
    dict(id="queen-anne", title="Queen Anne Victorian", where="Burlington", kind="Full exterior", photo="hero-0058", size="wide",
         text="Spindles, brackets and fish-scale shingle, scraped, primed and cut in by hand, lead-safe from the first scrape."),
    dict(id="lake-cottage", title="Lake Cottage", where="Lake Champlain", kind="Exterior & porch", photo="dsc-0695", size="",
         text="A lakeside camp in deep lake blue, with white rails and a screened porch."),
    dict(id="red-shingle", title="Red Shingle Colonial", where="Chittenden County", kind="Shingle & trim", photo="dsc-0631", size="",
         text="Cedar shingle in barn red, black shutters and white trim, brushed course by course."),
    dict(id="library", title="Library & Community Hall", where="Greater Burlington", kind="Full interior", photo="dsc-0995", size="wide",
         text="Clean white walls against timber and stone, finished room by room so the building stayed open."),
    dict(id="built-ins", title="Built-ins & Porch", where="Greater Burlington", kind="Cabinetry", photo="dsc-1094", size="tall",
         text="A slate built-in with matching wainscot."),
    dict(id="porch-floor", title="Porch Floor", where="Greater Burlington", kind="Painted floor", photo="dsc-1371", size="tall",
         text="A porch floor laid out in a two-grey diamond under a white beadboard ceiling."),
    dict(id="dealership", title="Auto Dealership", where="Chittenden County", kind="Facade & canopy", photo="dsc-1335", size="wide",
         text="Metal panel, canopy and soffit, painted in sections so the lot stayed open."),
]

ALT = {
    "hero-0058": "Cream Queen Anne Victorian with white porch spindles and trim",
    "dsc-0695": "Blue lake cottage with white porch railings",
    "dsc-0631": "Red shingle colonial with black shutters and a painter on a ladder",
    "dsc-0995": "Community hall with a black steel stair, timber and white walls",
    "dsc-1335": "Car dealership with a white facade and red canopy",
    "dsc-1094": "Slate gray painted built-in cabinet with matching wainscot",
    "dsc-1371": "Covered porch with a painted diamond floor and white beadboard ceiling",
}


def load_pairs():
    src = (ROOT / "assets/js/projects.js").read_text()
    body = src[src.index("["): src.rindex("]") + 1]
    return json.loads(body)


SERVICES = [
    ("residential", "residential painting", "dsc-0631",
     "Whole exteriors, single rooms, trim, doors, cabinets and porches. Prepped properly, finished cleanly.",
     ["Exterior siding, trim, doors and shutters", "Interior walls, ceilings and trim",
      "Cabinets and built-ins", "Rot repair before paint"]),
    ("commercial", "commercial painting", "dsc-1335",
     "Offices, storefronts, libraries and multi-unit buildings, inside and out, phased around your hours.",
     ["Offices, retail and public buildings", "Property-management repaints",
      "Lift work at height", "Scheduling around open hours"]),
    ("decks", "deck staining", "assets/before-after/deck-pair01-after.jpg",
     "Wash, repair and stain, so decks and porches are ready for another Vermont winter.",
     ["Pressure washing", "Board repair and sanding",
      "Stain or paint for wood, composite and metal", "Porch floors and stairs"]),
    ("lead", "lead inspections", "dsc-0951",
     "Many older Vermont homes still carry lead paint. We are EPA lead certified and offer EMP inspections for owners and property managers.",
     ["Essential Maintenance Practices inspections", "Lead-safe prep and containment",
      "Careful cleanup", "Paperwork for owners and landlords"]),
    ("gutters", "gutter cleaning", "dsc-0701",
     "Spring and fall cleanouts that keep water moving through the winter and off fresh paint.",
     ["Spring and fall cleanouts", "Downspouts flushed",
      "Loose hangers flagged", "Debris hauled away"]),
]

SERVICE_ALT = {
    "dsc-0631": "Painter on a ladder at a red shingle colonial",
    "dsc-1335": "Dealership facade with a red canopy",
    "assets/before-after/deck-pair01-after.jpg": "A freshly stained back deck",
    "dsc-0951": "Stairwell with white walls and original trim under a timber ceiling",
    "dsc-0701": "Eaves and trim along the side of a blue lake cottage",
}

STEPS = [
    ("walk & quote", "We visit, listen, measure and send a written estimate. Always free."),
    ("prep & protect", "Furniture, floors and plants covered. Surfaces scraped, sanded and primed."),
    ("paint & check", "Good paint, steady hands, and painters who check their own work as they go."),
    ("clean & walk", "We clean up every day, then walk the finished job with you."),
]

FAQ = [
    ("Is the estimate really free?", "Yes. We walk the project with you, answer questions and send a written estimate. No cost, no obligation."),
    ("How far ahead should I book?", "Exterior work books up early in Vermont, so reach out in the spring for summer jobs. Interiors are easier to fit in."),
    ("Do you help with color?", "Yes. Color consulting is part of the job. We can suggest combinations that suit the house and the light, and paint test swatches before you decide."),
    ("What about lead paint in an older home?", "We are EPA lead certified and work lead-safe on older homes from the first scrape. We also offer EMP lead inspections."),
    ("How does the giving work?", "A portion of the profit from every job goes to CVOEO, which helps people in shelters move into permanent housing. It adds nothing to your price."),
    ("Do I need to move my furniture?", "We move and cover what we can and protect the rest. Put away anything fragile or personal before we arrive."),
]

KIND = [
    ("Professional is not a large enough word to describe PWP’s craftsmanship and commitment.", "Pat Waterman"),
    ("This house is a Victorian and had deferred maintenance. We are so happy to see it restored.", "K Raz"),
    ("Our 16 year old kitchen cabinets were very worn and look like new again.", "Lara Militello"),
]

QUOTE = ("The best experience we’ve ever had with painters. They showed up on time with everything, were clean and tidy, "
         "and did the job expertly and within the time frame they estimated.", "Barbara Boutsikaris")


def slider(p):
    t = p["title"]
    return f"""<figure class="ba">
  <div class="ba__frame" style="--p:50%">
    <img src="{p['before']}" alt="{t}, before" loading="lazy" decoding="async">
    <img class="ba__after" src="{p['after']}" alt="{t}, after" loading="lazy" decoding="async">
    <span class="ba__tag ba__tag--b">before</span><span class="ba__tag ba__tag--a">after</span>
    <span class="ba__handle" aria-hidden="true"></span>
    <input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Compare before and after: {t}">
  </div>
  <figcaption><span>{t}</span><span class="meta">{p['what']}</span></figcaption>
</figure>"""


def simg(ph):
    """Service photo: a client photo name, or a direct path to a before/after image."""
    if ph.endswith(".jpg"):
        return f'<img src="{ph}" alt="{SERVICE_ALT[ph]}" loading="lazy" decoding="async">'
    return photo(ph, SERVICE_ALT[ph], sizes="(min-width: 1020px) 18vw, 26vw")


def num(i):
    return f"{i:02d}"


# --------------------------------------------------------------------------
# Pages

def build_index():
    html = head("Painting With Purpose · House painters in Burlington, Vermont",
                "Residential and commercial painting in Greater Burlington. Part of every job helps a Vermont neighbor find a home.",
                "home")
    html += header("index")
    html += f"""<main id="main">
<section class="vs vs--hero" aria-label="Sigma Phi House">
  {clip("sigma", "Sigma Phi House on a fall afternoon, students on the lawn", eager=True)}
  <div class="vs__txt">
    <h1 class="beat">Whether it’s a frat house on the hill,</h1>
    <p class="label vs__cap">Sigma Phi House · Burlington</p>
  </div>
</section>
<section class="vs vs--vic" aria-label="Queen Anne Victorian">
  {clip("victorian", "A Queen Anne Victorian on a quiet street, a neighbor walking a dog past")}
  <div class="vs__txt"><p class="beat">a Victorian on a quiet street,</p><p class="label vs__cap">Queen Anne Victorian · Burlington</p></div>
</section>
<section class="vs" aria-label="Library">
  {clip("library", "A library atrium with readers, timber ceilings and a black steel stair")}
  <div class="vs__txt"><p class="beat">a library in the middle of town,</p><p class="label vs__cap">Library &amp; community hall · Greater Burlington</p></div>
</section>
<section class="porch">
  <div class="porch__arch">{clip("porch-tall", "A freshly painted covered porch with a diamond pattern in the floor")}</div>
  <div class="porch__txt">
    <p class="beat">or the porch you come home to,</p>
    <h2>we paint with purpose.</h2>
    <p class="lead">A Greater Burlington crew that preps by hand, cleans up every day and walks the finished job with you. Part of every job helps a Vermont neighbor move into a home.</p>
    <a class="btn btn--light" href="estimate.html">free estimate <span aria-hidden="true">→</span></a>
  </div>
</section>
</main>
"""
    html += FOOTER
    write("index.html", html)


def build_work(pairs):
    cards = "".join(f"""<article class="pcard{f' pcard--{p["size"]}' if p["size"] else ''}" id="{p['id']}">
  <div class="pcard__img">{photo(p['photo'], ALT[p['photo']], sizes="(min-width: 760px) 50vw, 100vw" if p['size'] != 'wide' else "100vw")}</div>
  <div class="pcard__cap"><span class="n">{num(i)}</span><h3>{p['title']}</h3><p class="meta">{p['where']} · {p['kind']}</p><p>{p['text']}</p></div>
</article>""" for i, p in enumerate(PROJECTS, 1))
    lead = ["Green Victorian", "Navy Shingle Cottage", "Porch Floor Revival", "Dining Room Color Change", "Townhouse Refresh", "Two-Tone Foursquare"]
    pairs = sorted(pairs, key=lambda p: lead.index(p["title"]) if p["title"] in lead else len(lead))
    sliders = "\n".join(slider(p) for p in pairs)
    html = head("Work · Painting With Purpose", "Seven projects and twenty-one before and afters from around Greater Burlington.", "work")
    html += header("work")
    html += f"""<main id="main">
{phero(clip("sigma", "Sigma Phi House on a fall afternoon, students on the lawn", eager=True), "(work)", "the work",
       "Houses, halls and storefronts around Greater Burlington. Most of these photos were taken by Gabe on the last day of the job.",
       cap="Sigma Phi House · Burlington")}
<section class="sec wrap" aria-labelledby="p-h">
  {sechead("(selected projects)", "recent work", "p-h", f"{len(PROJECTS)} projects")}
  <div class="pgrid">{cards}</div>
</section>
<section class="sec wrap" id="before-after" aria-labelledby="ba-h">
  {sechead("(before &amp; after)", f"{len(pairs)} transformations", "ba-h", "drag across each photo to compare")}
  <div class="bagrid">
{sliders}
  </div>
  <div class="more"><button class="btn btn--ghost" type="button" data-more>show all {len(pairs)} <span aria-hidden="true">↓</span></button></div>
</section>
<section class="sec wrap" aria-label="What clients say">
  <figure class="quote">
    <blockquote><p>“{QUOTE[0]}”</p></blockquote>
    <figcaption class="label">{QUOTE[1]} · Google review</figcaption>
  </figure>
</section>
</main>
"""
    html += FOOTER
    write("work.html", html)


def build_services():
    rows = "".join(f"""<li class="srow" id="{sid}">
  <span class="n">{num(i)} / {num(len(SERVICES))}</span>
  <h3>{name}</h3>
  <div class="srow__txt"><p>{blurb}</p><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div>
  <div class="srow__img">{simg(ph)}</div>
</li>""" for i, (sid, name, ph, blurb, items) in enumerate(SERVICES, 1))
    steps = "".join(f'<li><span class="n">{num(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS, 1))
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    html = head("Services · Painting With Purpose", "Residential and commercial painting, deck staining, EMP lead inspections and gutter cleaning in northern Vermont.", "services")
    html += header("services")
    html += f"""<main id="main">
{phero(clip("library", "A library atrium with readers, timber ceilings and a black steel stair", eager=True), "(services)", "what we do",
       "Five services, one standard: careful prep, daily cleanup and painters who check their own work.",
       cap="Library &amp; community hall · Greater Burlington")}
<section class="sec wrap" aria-labelledby="s-h">
  {sechead("(services)", "five ways we help", "s-h")}
  <ol class="slist">{rows}</ol>
</section>
<section class="sec wrap" aria-labelledby="steps-h">
  {sechead("(process)", "four steps, no surprises", "steps-h")}
  <ol class="cols">{steps}</ol>
</section>
<section class="sec wrap faq" aria-labelledby="faq-h">
  <div class="faqgrid">
    <div>
      <p class="label">(questions)</p>
      <h2 id="faq-h" style="font-size:var(--t-h2);margin-top:14px">good to know</h2>
      <p class="area">We cover Addison, Chittenden, Franklin, Grand Isle, Lamoille, Orange and Washington counties. Not sure if you’re in range? Call <a href="tel:{TEL}">{PHONE}</a>.</p>
    </div>
    <div>{faq}</div>
  </div>
</section>
</main>
"""
    html += FOOTER
    write("services.html", html)


def build_about():
    html = head("Purpose · Painting With Purpose", "How part of every job goes to CVOEO to help Vermonters move from shelter into a home.", "about")
    html += header("about")
    html += f"""<main id="main">
{phero(clip("victorian", "A Queen Anne Victorian on a quiet street, a neighbor walking a dog past", eager=True), "(purpose)", "good work should do good",
       "A Greater Burlington painting company with one larger goal: helping end homelessness in Vermont.",
       cls="phero--vic", cap="Queen Anne Victorian · Burlington")}
<section class="sec wrap story">
  <p class="label">(story)</p>
  <div class="story__txt">
    <p class="story__big">Painting is honest work. You can see it from the street. We wanted the reason behind it to be just as easy to see.</p>
    <div class="story__cols">
      <p>Painting With Purpose opened in February 2022 with a simple idea: do excellent work for our neighbors, and use the business to help the neighbors who have no home at all.</p>
      <p>The plan took first place at the Joy and Jerry Meyers Cup at UVM. More than a hundred jobs later, it still sets how we work. On time, fully equipped, your home protected, and the site cleaned every day.</p>
    </div>
  </div>
</section>
<section class="band" aria-labelledby="cvoeo-h">
  <div class="wrap band__in">
    <div>
      <p class="label">(cvoeo)</p>
      <h2 id="cvoeo-h">part of every job goes to housing.</h2>
      <p>CVOEO, the Champlain Valley Office of Economic Opportunity, helps people in shelters move into permanent homes. Our share covers the costs that stand in the way: a security deposit, a first month’s rent, the utilities.</p>
      <div class="nums"><div><b>$15k+</b><span>given to CVOEO</span></div><div><b>12+</b><span>people housed</span></div><div><b>100+</b><span>jobs finished</span></div></div>
      <ol class="flow"><li>You book a job</li><li>We do it right</li><li>A share goes to CVOEO</li><li>A neighbor moves in</li></ol>
    </div>
    <div class="band__img">{photo("crew-three", "Three painters on the job", sizes="(min-width: 760px) 50vw, 100vw")}</div>
  </div>
</section>
<section class="sec wrap" aria-labelledby="kw-h">
  {sechead("(kind words)", "in their words", "kw-h")}
  <div class="kind">{''.join(f'<figure><blockquote><p>“{q}”</p></blockquote><figcaption class="label">{w}</figcaption></figure>' for q, w in KIND)}</div>
</section>
<section class="sec wrap" aria-labelledby="f-h">
  {sechead("(founders)", "gabe &amp; zach", "f-h")}
  <div class="people">
    <figure>{photo("crew-portrait-1", "Gabe Dunn in a Painting With Purpose cap", sizes="(min-width: 860px) 30vw, 50vw")}<figcaption><span>Gabe Dunn</span><span class="meta">co-founder</span></figcaption></figure>
    <figure>{photo("crew-portrait-2", "Zach Dunn laughing in a Painting With Purpose cap", sizes="(min-width: 860px) 30vw, 50vw")}<figcaption><span>Zach Dunn</span><span class="meta">co-founder</span></figcaption></figure>
    <p class="people__txt">Brothers Gabe and Zach Dunn started Painting With Purpose to prove a painting company could be very good at the work and good for the place it works. Gabe takes most of the photographs on this site.</p>
  </div>
</section>
</main>
"""
    html += FOOTER
    write("about.html", html)


def field(label, name, kind="text", req=True, auto=""):
    r = " required" if req else ""
    a = f' autocomplete="{auto}"' if auto else ""
    return f'<label class="fld"><span>{label}</span><input type="{kind}" name="{name}"{r}{a}></label>'


def choices(name, opts, kind="radio"):
    return "".join(
        f'<label class="chip"><input type="{kind}" name="{name}" value="{v}"{" required" if kind == "radio" and i == 0 else ""}><span>{t}</span></label>'
        for i, (v, t) in enumerate(opts))


def build_estimate():
    svc = [("residential", "Residential painting"), ("commercial", "Commercial painting"), ("decks", "Deck staining"),
           ("lead", "Lead inspection"), ("gutters", "Gutter cleaning")]
    html = head("Free estimate · Painting With Purpose", "Tell us about your project and we’ll set up a free walkthrough.", "estimate")
    html += header("estimate")
    html += f"""<main id="main">
{phero(still("dsc-1247", "The Painting With Purpose tent on a Vermont town street", "50% 60%"), "(free estimate)", "let’s take a look",
       "Tell us a little about the project and we’ll set up a time to walk it with you.", cls="phero--short")}
<section class="sec wrap formwrap">
  <form class="form" data-demo-form novalidate>
    <fieldset><legend><span class="n">01</span>What do you need?</legend><div class="chips">{choices("service", svc)}</div></fieldset>
    <fieldset><legend><span class="n">02</span>Inside, outside, or both?</legend><div class="chips">{choices("where", [("interior", "Interior"), ("exterior", "Exterior"), ("both", "Both")])}</div></fieldset>
    <fieldset><legend><span class="n">03</span>When are you hoping to start?</legend><div class="chips">{choices("when", [("asap", "As soon as possible"), ("soon", "In the next few months"), ("next", "Next season"), ("planning", "Just planning")])}</div></fieldset>
    <fieldset><legend><span class="n">04</span>How do we reach you?</legend>
      <div class="flds">{field("Full name", "name", auto="name")}{field("Phone", "phone", "tel", auto="tel")}{field("Email", "email", "email", auto="email")}{field("Town", "town", req=False, auto="address-level2")}</div>
      <label class="fld fld--wide"><span>Tell us about the project</span><textarea name="details" rows="4"></textarea></label>
    </fieldset>
    <p class="form__err" role="alert" hidden>Please fill in the highlighted fields.</p>
    <button class="btn" type="submit">request my estimate <span aria-hidden="true">→</span></button>
    <p class="form__fine">Free, with no obligation. We don’t share your details.</p>
  </form>
  <div class="form__done" hidden tabindex="-1"><h2>you’re on the list.</h2><p>Thanks. We’ll be in touch soon to find a time to walk the project.</p></div>
  <aside class="formside">
    <p class="label">rather talk?</p><p>Call or text and a person on our team will pick up.<br><a href="tel:{TEL}">{PHONE}</a></p>
    <small>133 Elm Street, Office B, Winooski · 8:00 to 5:00 daily</small>
    <p class="label">every job gives back</p><p>Part of your project goes to CVOEO to help Vermonters move into a home.</p>
  </aside>
</section>
</main>
"""
    html += FOOTER
    write("estimate.html", html)


def build_careers():
    perks = [("fair, steady pay", "$18 to $30 an hour based on experience, with paid lunch, paid uniforms and paid drives over 30 minutes."),
             ("learn the trade", "Residential, commercial, staining, pressure washing, specialty finishes and color consulting. Room to grow as your skills do."),
             ("work that matters", "Every job you finish helps a Vermont neighbor find a home.")]
    pk = "".join(f'<li><span class="n">{num(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(perks, 1))
    html = head("Careers · Painting With Purpose", "Painter jobs in Greater Burlington. $18 to $30 an hour and room to grow.", "careers")
    html += header("careers")
    html += f"""<main id="main">
{phero(still("crew", "The Painting With Purpose crew beside their truck", "50% 30%"), "(careers)", "paint with us",
       "We are looking for reliable, careful people who take pride in their work. Experience helps. Attitude matters more.")}
<section class="sec wrap" aria-labelledby="why-h">
  {sechead("(why here)", "a crew, not just a job", "why-h")}
  <ol class="cols cols--3">{pk}</ol>
  <p class="cols__note">Short and long term disability, life insurance and flexible vacation.</p>
</section>
<section class="sec wrap" aria-labelledby="roles-h">
  {sechead("(open roles)", "hiring now", "roles-h")}
  <ul class="roles"><li><span class="n">01</span><span class="t">Painter</span><span class="d">Full-time · $18 to $30 an hour</span><span class="meta">Greater Burlington</span></li></ul>
</section>
<section class="sec wrap formwrap" aria-labelledby="apply-h">
  <form class="form" data-demo-form novalidate>
    <h2 id="apply-h" class="form__h">apply</h2>
    <fieldset><legend><span class="n">01</span>About you</legend>
      <div class="flds">{field("Full name", "name", auto="name")}{field("Phone", "phone", "tel", auto="tel")}{field("Email", "email", "email", auto="email")}{field("Where you live", "town", req=False, auto="address-level2")}</div>
      <label class="fld fld--wide"><span>Experience (a sentence or two is fine)</span><textarea name="experience" rows="3"></textarea></label>
    </fieldset>
    <p class="form__err" role="alert" hidden>Please fill in the highlighted fields.</p>
    <button class="btn" type="submit">send application <span aria-hidden="true">→</span></button>
    <p class="form__fine">We read every application.</p>
  </form>
  <div class="form__done" hidden tabindex="-1"><h2>got it.</h2><p>Thanks. We’ll be in touch soon.</p></div>
  <aside class="formside">
    <p class="label">what we look for</p><p>Shows up on time. Cares about the details. Treats every home like their own. We can teach the rest.</p>
    <p class="label">prefer to call?</p><p><a href="tel:{TEL}">{PHONE}</a></p>
  </aside>
</section>
</main>
"""
    html += FOOTER
    write("careers.html", html)


def build_404():
    html = head("Page not found · Painting With Purpose", "That page isn’t here.", "404")
    html += header("404")
    btns = f'<div class="btns"><a class="btn btn--light" href="index.html">back home <span aria-hidden="true">→</span></a><a class="btn btn--ghost" href="work.html">see the work</a></div>'
    html += f"""<main id="main">
{phero(clip("porch-tall", "A freshly painted covered porch with a diamond pattern in the floor", eager=True), "(404)", "missed a spot",
       "That page isn’t here. It may have moved, or the link has a typo.", extra=btns)}
</main>
"""
    html += FOOTER
    write("404.html", html)


if __name__ == "__main__":
    pairs = load_pairs()
    build_index()
    build_work(pairs)
    build_services()
    build_about()
    build_estimate()
    build_careers()
    build_404()
