#!/usr/bin/env python3
"""Builds every page of demo 2. Run from the repo root: python3 tools/build.py

Copy lives in this file. Before/after pairs live in assets/js/projects.js.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHONE = "802-PAINTER"
TEL = "+18027246837"
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
    return (f'<img class="{cls}" src="{p}-sm.jpg" srcset="{p}-sm.jpg 900w, {p}-lg.jpg 2000w" '
            f'sizes="{sizes}" alt="{alt}" {load} decoding="async">')


def head(title, desc, page):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f6f5f1">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/photos/dsc-0058-lg.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..700&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body data-page="{page}">
<a class="skip" href="#main">Skip to content</a>
"""


def header(page, over=False):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if page == h.split(".")[0] else ""}>{t}</a></li>'
        for h, t in NAV)
    return f"""<header class="hdr{' hdr--over' if over else ''}">
  <a class="hdr__logo" href="index.html" aria-label="Painting With Purpose, home"><img src="assets/logo.png" alt="Painting With Purpose" width="600" height="402"></a>
  <nav class="hdr__nav" id="nav" aria-label="Main">
    <ul>{links}</ul>
    <a class="hdr__cta" href="estimate.html">free estimate</a>
  </nav>
  <button class="hdr__menu" type="button" aria-expanded="false" aria-controls="nav"><span>menu</span></button>
</header>
"""


FOOTER = f"""<footer class="ftr">
  <div class="ftr__cta">
    <p class="label">(next)</p>
    <a class="ftr__big" href="estimate.html">let’s take a look <span aria-hidden="true">→</span></a>
    <p class="ftr__sub">Free walk-through and a written estimate. Or call <a href="tel:{TEL}">{PHONE}</a>.</p>
  </div>
  <div class="ftr__grid">
    <img class="ftr__logo" src="assets/logo.png" alt="Painting With Purpose" width="600" height="402" loading="lazy">
    <div><p class="label">studio</p><p>Residential &amp; commercial painting<br>Greater Burlington, Vermont</p></div>
    <div><p class="label">contact</p><p><a href="tel:{TEL}">{PHONE}</a><br><a href="{IG}">@paintingwithpurposevt</a></p></div>
    <div><p class="label">pages</p><p>{'<br>'.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<br><a href="estimate.html">free estimate</a></p></div>
  </div>
  <p class="ftr__fine"><span>© 2026 Painting With Purpose</span><span>A share of every job goes to CVOEO</span></p>
</footer>
<script src="assets/js/projects.js"></script>
<script src="assets/js/site.js"></script>
</body>
</html>
"""


def page_title(label, title, lede):
    return f"""<section class="ptitle wrap">
  <p class="label">{label}</p>
  <h1>{title}</h1>
  <p class="ptitle__lede">{lede}</p>
</section>
"""


def write(name, html):
    (ROOT / name).write_text(html)
    print("wrote", name)


# --------------------------------------------------------------------------
# Data

PROJECTS = [
    dict(id="sigma-phi", title="Sigma Phi House", where="Burlington, VT", kind="Columns, trim & entry",
         photos=["dsc-0179"],
         text="Four Corinthian columns, a full pediment and a fanlight entry, restored to read crisp against red brick."),
    dict(id="queen-anne", title="Queen Anne Victorian", where="Greater Burlington", kind="Exterior repaint",
         photos=["dsc-0058"],
         text="Spindles, brackets and fish-scale shingle, each one scraped, primed and cut in by hand, lead-safe from the first scrape."),
    dict(id="lake-cottage", title="Lake Cottage", where="Lake Champlain", kind="Full exterior & porch",
         photos=["dsc-0695", "dsc-0686", "dsc-0701"],
         text="A lakeside camp in deep lake blue, with white rails and a screened porch ready for another fifty summers."),
    dict(id="red-shingle", title="Red Shingle Colonial", where="Chittenden County", kind="Shingle & trim",
         photos=["dsc-0631"],
         text="Cedar shingle in barn red, black shutters and white trim, back-brushed course by course."),
    dict(id="library", title="Library & Community Hall", where="Greater Burlington", kind="Full interior",
         photos=["dsc-0856", "dsc-0995", "dsc-0951", "dsc-0735"],
         text="Bright, scrubbable walls against exposed timber, sequenced room by room so the building stayed open."),
    dict(id="dealership", title="Auto Dealership", where="Chittenden County", kind="Facade & canopy",
         photos=["dsc-1335"],
         text="Metal panel, canopy and soffit, prepped and coated off-hours so the lot never closed."),
    dict(id="built-ins", title="Built-ins & Porch", where="Greater Burlington", kind="Cabinetry & porch floor",
         photos=["dsc-1094", "dsc-1371"],
         text="A slate built-in with matching wainscot, and a porch floor laid out in a two-grey diamond."),
]

ALT = {
    "dsc-0179": "Sigma Phi house with four white Corinthian columns and a pediment against red brick",
    "dsc-0058": "Cream Queen Anne Victorian with white porch spindles and trim",
    "dsc-0695": "Blue lake cottage with white porch railings",
    "dsc-0686": "Blue lake cottage with a screened porch above a stone beach",
    "dsc-0701": "Side of the blue lake cottage with white trim and fall flowers",
    "dsc-0631": "Red shingle colonial with black shutters and a painter on a ladder",
    "dsc-0856": "Library aisle with white walls and timber shelving",
    "dsc-0995": "Community hall with a black steel stair, timber and white walls",
    "dsc-0951": "Stairwell with white walls under a timber ceiling",
    "dsc-0735": "Freshly painted accessible restroom",
    "dsc-1335": "Car dealership with a white facade and red canopy",
    "dsc-1094": "Slate gray painted built-in cabinet with matching wainscot",
    "dsc-1371": "Covered porch with a painted diamond floor and white beadboard ceiling",
}


def load_pairs():
    src = (ROOT / "assets/js/projects.js").read_text()
    body = src[src.index("["): src.rindex("]") + 1]
    return json.loads(body)


SERVICES = [
    ("residential", "Residential painting", "dsc-0631",
     "Whole-house exteriors, single rooms, trim, doors, cabinets and porches. Prepped properly, finished cleanly.",
     ["Exterior siding, trim, doors and shutters", "Interior walls, ceilings and trim",
      "Cabinet and built-in refinishing", "Porches, railings and painted floors"]),
    ("commercial", "Commercial painting", "dsc-1335",
     "Offices, libraries, dealerships and multi-unit buildings, scheduled around your hours so the doors stay open.",
     ["Offices, retail, libraries and dealerships", "Property-management repaints",
      "Night and weekend scheduling", "Low-odor coatings for occupied spaces"]),
    ("decks", "Deck staining", "deck-painter",
     "Wash, sand, repair and stain, so decks and porches handle another Vermont winter.",
     ["Pressure washing and brightening", "Board repair and sanding",
      "Penetrating and solid stains", "Porch floors and stairs"]),
    ("lead", "Lead inspections", "lead-inspection",
     "Older Vermont homes often hide lead paint. Certified EMP work keeps families and crews safe.",
     ["Certified Essential Maintenance Practices", "Lead-safe prep and containment",
      "HEPA cleanup and verification", "Documentation for owners and landlords"]),
    ("gutters", "Gutter cleaning", "gutter-cleaning",
     "Leaves out, water flowing the right way. A small job that protects your siding and fresh paint.",
     ["Fall and spring cleanouts", "Downspout flushing",
      "Checks for leaks and loose hangers", "Debris hauled away"]),
]

SERVICE_ALT = {
    "dsc-0631": "Painter on a ladder at a red shingle colonial",
    "dsc-1335": "Dealership facade with a red canopy",
    "deck-painter": "Painter staining a deck by hand",
    "lead-inspection": "Inspector filling out a lead inspection checklist",
    "gutter-cleaning": "Gloved hand clearing leaves from a gutter",
}

STEPS = [
    ("walk & quote", "We visit, listen, measure and send a clear written estimate. Free, always."),
    ("prep & protect", "Furniture covered, floors and plants protected, surfaces scraped, sanded and primed."),
    ("paint & inspect", "Premium paint, steady hands, and painters who check their own work as they go."),
    ("clean & walk", "We clean up every day, then walk the finished job with you before we call it done."),
]

FAQ = [
    ("Is the estimate really free?", "Yes. We walk the project with you, answer questions and send a written estimate. There’s no charge and no obligation."),
    ("How far ahead do you book?", "Exterior season fills up fast in Vermont, so spring and early summer are best for booking outdoor work. Interiors and commercial jobs run year-round."),
    ("Do you help pick colors?", "Happily. We can bring samples, suggest combinations that suit the house and the light, and paint test swatches before you commit."),
    ("What about lead paint in an older home?", "Many Vermont homes built before 1978 have lead paint. We follow certified lead-safe (EMP) practices, contain the work area and clean with HEPA equipment."),
    ("How does the giving work?", "A share of every job goes to the Champlain Valley Office of Economic Opportunity (CVOEO), which helps Vermonters find and keep safe housing."),
    ("Do I need to move my furniture?", "We’ll move and cover what we can and protect everything else. Just put away anything fragile or personal before we arrive."),
]

TOWNS = ["Burlington", "South Burlington", "Winooski", "Essex", "Colchester", "Williston",
         "Shelburne", "Charlotte", "Richmond", "Jericho"]

REVIEWS = [
    ("Professional is not a large enough word to describe PWP’s craftsmanship and commitment.", "Pat Waterman"),
    ("This house is a Victorian and had deferred maintenance. We are so happy to see it restored.", "K Raz"),
    ("Our 16 year old kitchen cabinets were very worn and look like new again!", "Lara Militello"),
]


def slider(p, cls="", eager=False):
    load = "" if eager else ' loading="lazy"'
    t = p["title"]
    return f"""<figure class="ba {cls}">
  <div class="ba__frame" style="--p:50%">
    <img src="{p['before']}" alt="{t}, before"{load} decoding="async">
    <img class="ba__after" src="{p['after']}" alt="{t}, after"{load} decoding="async">
    <span class="ba__tag ba__tag--b">before</span><span class="ba__tag ba__tag--a">after</span>
    <span class="ba__handle" aria-hidden="true"></span>
    <input class="ba__range" type="range" min="0" max="100" value="50" aria-label="Compare before and after: {t}">
  </div>
  <figcaption><span>{t}</span><span class="meta">{p['what']}</span></figcaption>
</figure>"""


def num(i):
    return f"{i:02d}"


# --------------------------------------------------------------------------
# Pages

def build_index(pairs):
    sel = [PROJECTS[0], PROJECTS[2], PROJECTS[3], PROJECTS[4], PROJECTS[6], PROJECTS[5]]
    layout = ["w-7", "w-5 tall", "w-5", "w-7", "w-6 tall", "w-6"]
    imgs = {"lake-cottage": "dsc-0686", "library": "dsc-0995", "built-ins": "dsc-1094"}
    tiles = []
    for i, (p, lay) in enumerate(zip(sel, layout), 1):
        ph = imgs.get(p["id"], p["photos"][0])
        tiles.append(f"""<a class="tile {lay}" href="work.html#{p['id']}">
    <div class="tile__img">{photo(ph, ALT[ph], sizes="(min-width: 900px) 60vw, 100vw")}</div>
    <p class="tile__cap"><span class="n">{num(i)}</span><span class="t">{p['title']}</span><span class="meta">{p['where']}</span></p>
  </a>""")
    services = "".join(
        f'<li><a href="services.html#{sid}"><span class="n">{num(i)}</span><span class="t">{name}</span>'
        f'<span class="d">{blurb}</span><span class="arr" aria-hidden="true">→</span></a></li>'
        for i, (sid, name, _, blurb, _) in enumerate(SERVICES, 1))
    thumbs = "".join(
        f'<a class="bathumb" href="work.html#before-after"><img src="{p["after"]}" alt="{p["title"]}, after" loading="lazy">'
        f'<span>{p["title"]}</span></a>' for p in pairs[1:4])
    q, who = REVIEWS[0]
    html = head("Painting With Purpose | House painters in Burlington, Vermont",
                "Residential and commercial painting across Greater Burlington, Vermont. A share of every job helps Vermonters find housing.",
                "home")
    html += header("index", over=True)
    html += f"""<main id="main">
<section class="hero">
  {photo("dsc-0058", ALT["dsc-0058"], "hero__img", eager=True)}
  <div class="hero__txt">
    <h1>good work,<br>for good.</h1>
    <div class="hero__meta">
      <p>House painters in Burlington, Vermont.<br>A share of every job goes to ending homelessness.</p>
      <a class="btn btn--light" href="estimate.html">free estimate <span aria-hidden="true">→</span></a>
    </div>
  </div>
  <p class="hero__credit">Queen Anne Victorian · Greater Burlington</p>
</section>

<section class="intro wrap">
  <p class="label">(01) studio</p>
  <p class="intro__big">Painting With Purpose is a Burlington crew that preps carefully, paints cleanly and walks every job with you at the end. <span class="mute">Then we send part of what you paid to CVOEO, to help a Vermont neighbor find a home.</span></p>
</section>

<section class="work wrap" aria-labelledby="work-h">
  <div class="sechead"><p class="label">(02) selected work</p><h2 id="work-h">recent projects</h2><a class="more" href="work.html">all work →</a></div>
  <div class="tiles">
  {''.join(tiles)}
  </div>
</section>

<section class="bafeature wrap" aria-labelledby="ba-h">
  <div class="sechead"><p class="label">(03) before &amp; after</p><h2 id="ba-h">drag to compare</h2><a class="more" href="work.html#before-after">all {len(pairs)} →</a></div>
  <div class="bafeature__grid">
    {slider(pairs[0], "ba--big")}
    <div class="bafeature__side">
      <p class="bafeature__desc">{pairs[0]['desc']}</p>
      <div class="bathumbs">{thumbs}</div>
    </div>
  </div>
</section>

<section class="purpose" aria-labelledby="purpose-h">
  <div class="wrap purpose__in">
    <div class="purpose__txt">
      <p class="label">(04) purpose</p>
      <h2 id="purpose-h">every job helps a neighbor find a home.</h2>
      <p>We partner with the Champlain Valley Office of Economic Opportunity. A share of every project goes to their housing work, built into the price, never added on top.</p>
      <dl class="stats">
        <div><dt>100+</dt><dd>jobs finished</dd></div>
        <div><dt>12+</dt><dd>neighbors housed</dd></div>
        <div><dt>$0</dt><dd>extra to you</dd></div>
      </dl>
      <a class="btn btn--light" href="about.html">our purpose <span aria-hidden="true">→</span></a>
    </div>
    <div class="purpose__img">{photo("crew", "The Painting With Purpose crew in white painter’s clothes beside their truck", sizes="(min-width: 900px) 50vw, 100vw")}</div>
  </div>
</section>

<section class="svc wrap" aria-labelledby="svc-h">
  <div class="sechead"><p class="label">(05) services</p><h2 id="svc-h">what we do</h2><a class="more" href="services.html">details →</a></div>
  <ul class="svclist">{services}</ul>
</section>

<section class="quote wrap">
  <p class="label">(06) word of mouth</p>
  <blockquote><p>“{q}”</p><footer>{who} · Google review ★★★★★</footer></blockquote>
</section>
</main>
"""
    html += FOOTER
    write("index.html", html)


def build_work(pairs):
    projects = []
    for i, p in enumerate(PROJECTS, 1):
        main, rest = p["photos"][0], p["photos"][1:]
        extras = "".join(f'<div class="proj__x">{photo(ph, ALT[ph], sizes="(min-width: 900px) 33vw, 100vw")}</div>' for ph in rest)
        projects.append(f"""<article class="proj" id="{p['id']}">
  <div class="proj__main">{photo(main, ALT[main], sizes="(min-width: 900px) 66vw, 100vw")}</div>
  <div class="proj__info">
    <p class="n">{num(i)}</p>
    <h3>{p['title']}</h3>
    <p class="meta">{p['where']} · {p['kind']}</p>
    <p>{p['text']}</p>
  </div>
  {f'<div class="proj__extras n{len(rest)}">{extras}</div>' if rest else ''}
</article>""")
    sliders = "\n".join(slider(p) for p in pairs)
    html = head("Work | Painting With Purpose", "Recent painting projects and 21 before-and-after transformations from around Greater Burlington, Vermont.", "work")
    html += header("work")
    html += f"""<main id="main">
{page_title("(work)", "the work", "Houses, halls and storefronts around Greater Burlington. Most of these photos were taken by Gabe on the last day of the job.")}
<nav class="jump wrap" aria-label="Projects">{''.join(f'<a href="#{p["id"]}">{p["title"]}</a>' for p in PROJECTS)}<a href="#before-after">Before &amp; after</a></nav>
<section class="projects wrap">
{''.join(projects)}
</section>
<section class="balist wrap" id="before-after" aria-labelledby="ba-h">
  <div class="sechead"><p class="label">(before &amp; after)</p><h2 id="ba-h">{len(pairs)} transformations</h2><p class="more">drag each photo to compare</p></div>
  <div class="bagrid">
{sliders}
  </div>
</section>
<section class="crew wrap" aria-labelledby="crew-h">
  <div class="sechead"><p class="label">(on the job)</p><h2 id="crew-h">the crew at work</h2></div>
  <div class="crew__grid">
    <div class="w-a">{photo("green-house-crew", "Painters on ladders at a green house", sizes="(min-width: 900px) 33vw, 100vw")}</div>
    <div class="w-b">{photo("townhouse-crew", "Painters on ladders at a townhouse", sizes="(min-width: 900px) 66vw, 100vw")}</div>
    <div class="w-c">{photo("crew-three", "Three painters taking a break beside a ladder", sizes="(min-width: 900px) 66vw, 100vw")}</div>
    <div class="w-d">{photo("yellow-colonial", "Finished yellow colonial with a red door", sizes="(min-width: 900px) 33vw, 100vw")}</div>
  </div>
</section>
</main>
"""
    html += FOOTER
    write("work.html", html)


def build_services():
    rows = []
    for i, (sid, name, ph, blurb, items) in enumerate(SERVICES, 1):
        lis = "".join(f"<li>{x}</li>" for x in items)
        rows.append(f"""<article class="srv" id="{sid}">
  <div class="srv__img">{photo(ph, SERVICE_ALT[ph], sizes="(min-width: 900px) 45vw, 100vw")}</div>
  <div class="srv__txt">
    <p class="n">{num(i)} / {num(len(SERVICES))}</p>
    <h2>{name.lower()}</h2>
    <p>{blurb}</p>
    <ul>{lis}</ul>
    <a class="link" href="estimate.html?service={sid}">get an estimate →</a>
  </div>
</article>""")
    steps = "".join(f'<li><span class="n">{num(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS, 1))
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    towns = "".join(f"<li>{t}</li>" for t in TOWNS)
    html = head("Services | Painting With Purpose", "Residential and commercial painting, deck staining, lead inspections and gutter cleaning in Greater Burlington, Vermont.", "services")
    html += header("services")
    html += f"""<main id="main">
{page_title("(services)", "what we do", "Five services, one standard: careful prep, daily cleanup and painters who check their own work.")}
<section class="srvs wrap">
{''.join(rows)}
</section>
<section class="steps wrap" aria-labelledby="steps-h">
  <div class="sechead"><p class="label">(process)</p><h2 id="steps-h">four steps, no surprises</h2></div>
  <ol class="steplist">{steps}</ol>
</section>
<section class="area wrap" aria-labelledby="area-h">
  <div class="sechead"><p class="label">(area)</p><h2 id="area-h">greater burlington &amp; beyond</h2></div>
  <div class="area__grid">
    <ul class="towns">{towns}</ul>
    <p>Not on the list? Call <a href="tel:{TEL}">{PHONE}</a>. If we can get there, we’ll come take a look.</p>
  </div>
</section>
<section class="faq wrap" aria-labelledby="faq-h">
  <div class="sechead"><p class="label">(questions)</p><h2 id="faq-h">good to know</h2></div>
  <div class="faq__list">{faq}</div>
</section>
</main>
"""
    html += FOOTER
    write("services.html", html)


def build_about():
    values = [
        ("Quality you can see", "Every painter inspects their own work before anyone else does. If it isn’t right, we make it right."),
        ("Trust & respect", "We treat your home like it’s ours. Things covered, nothing left behind."),
        ("Clean, every day", "Brushes washed, drop cloths folded and walkways clear before we leave each afternoon."),
        ("Straight talk", "Step-by-step communication, so you always know what’s happening next and when."),
    ]
    vals = "".join(f'<li><span class="n">{num(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(values, 1))
    html = head("Purpose | Painting With Purpose", "Painting With Purpose is a Greater Burlington painting company working to help end homelessness in Vermont.", "about")
    html += header("about")
    html += f"""<main id="main">
{page_title("(purpose)", "good work should do good", "A Greater Burlington painting company with one big goal: helping end homelessness in Vermont.")}
<section class="full">{photo("dsc-1247", "The Painting With Purpose tent at a Vermont town event", sizes="100vw")}</section>
<section class="split wrap">
  <p class="label">(story)</p>
  <div class="split__txt">
    <p class="big">Painting is honest work. You can see it from the street. We wanted the why behind it to be just as visible.</p>
    <p>Painting With Purpose started with a crew, a van and a promise: do excellent work for our neighbors, and use the business to help the neighbors who don’t have a home at all.</p>
    <p>More than a hundred jobs later, that promise still sets how we work. We show up on time with everything we need, protect your home, clean up daily and talk you through each step. Along the way we were honored with the Joy and Jerry Meyers Cup.</p>
  </div>
</section>
<section class="purpose" aria-labelledby="cvoeo-h">
  <div class="wrap purpose__in">
    <div class="purpose__txt">
      <p class="label">(cvoeo)</p>
      <h2 id="cvoeo-h">part of every job goes to housing.</h2>
      <p>The Champlain Valley Office of Economic Opportunity helps Vermonters find and keep safe, stable housing. When you hire us, a share of what you pay goes to that work, at no extra cost to you.</p>
      <ol class="flow"><li>You book a job</li><li>We do it right</li><li>A share goes to CVOEO</li><li>A neighbor finds a home</li></ol>
    </div>
    <div class="purpose__img">{photo("crew-three", "Three painters on the job", sizes="(min-width: 900px) 50vw, 100vw")}</div>
  </div>
</section>
<section class="values wrap" aria-labelledby="values-h">
  <div class="sechead"><p class="label">(how we work)</p><h2 id="values-h">what you can count on</h2></div>
  <ol class="steplist">{vals}</ol>
</section>
<section class="founders wrap" aria-labelledby="f-h">
  <div class="sechead"><p class="label">(founders)</p><h2 id="f-h">gabe &amp; zach</h2></div>
  <div class="founders__grid">
    <figure>{photo("crew-portrait-1", "Gabe Dunn in a Painting With Purpose cap", sizes="(min-width: 900px) 30vw, 50vw")}<figcaption><span>Gabe Dunn</span><span class="meta">co-founder</span></figcaption></figure>
    <figure>{photo("crew-portrait-2", "Zach Dunn laughing in a Painting With Purpose cap", sizes="(min-width: 900px) 30vw, 50vw")}<figcaption><span>Zach Dunn</span><span class="meta">co-founder</span></figcaption></figure>
    <p class="founders__txt">Brothers Gabe and Zach Dunn started Painting With Purpose to prove a painting company could be really good at the work and really good for the community. One of them is on nearly every job, walking the estimate or checking the prep. Gabe also shoots most of the project photos on this site.</p>
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
    svc = [(s[0], s[1]) for s in SERVICES]
    html = head("Free estimate | Painting With Purpose", "Request a free painting estimate in Greater Burlington, Vermont.", "estimate")
    html += header("estimate")
    html += f"""<main id="main">
{page_title("(free estimate)", "let’s take a look", "Tell us a little about the project. We’ll be in touch within one business day to set up a walk-through.")}
<section class="formwrap wrap">
  <form class="form" data-demo-form novalidate>
    <fieldset><legend><span class="n">01</span>What do you need?</legend><div class="chips">{choices("service", svc)}</div></fieldset>
    <fieldset><legend><span class="n">02</span>Inside, outside, or both?</legend><div class="chips">{choices("where", [("interior", "Interior"), ("exterior", "Exterior"), ("both", "Both")])}</div></fieldset>
    <fieldset><legend><span class="n">03</span>When are you hoping to start?</legend><div class="chips">{choices("when", [("asap", "As soon as possible"), ("1-3", "1–3 months"), ("next", "Next season"), ("exploring", "Just exploring")])}</div></fieldset>
    <fieldset><legend><span class="n">04</span>How do we reach you?</legend>
      <div class="flds">{field("Full name", "name", auto="name")}{field("Phone", "phone", "tel", auto="tel")}{field("Email", "email", "email", auto="email")}{field("Town", "town", req=False, auto="address-level2")}</div>
      <label class="fld fld--wide"><span>Tell us about the project</span><textarea name="details" rows="4"></textarea></label>
    </fieldset>
    <p class="form__err" role="alert" hidden>Please fill in the highlighted fields.</p>
    <button class="btn" type="submit">Request my estimate <span aria-hidden="true">→</span></button>
    <p class="form__fine">Free and no obligation. We never share your info.</p>
  </form>
  <div class="form__done" hidden tabindex="-1"><h2>you’re on the list.</h2><p>Thanks. We’ll reach out within one business day to set up a time to walk the project.</p></div>
  <aside class="formside">
    {photo("interior-entry", "Freshly painted entry with a wood door and white trim", sizes="(min-width: 900px) 30vw, 100vw")}
    <p class="label">rather talk?</p><p>Call or text and a real person will pick up.<br><a href="tel:{TEL}">{PHONE}</a></p>
    <p class="label">every job gives back</p><p>A share of your project goes to CVOEO to help Vermonters find housing.</p>
  </aside>
</section>
</main>
"""
    html += FOOTER
    write("estimate.html", html)


def build_careers():
    roles = [("Painter", "Full-time · seasonal"), ("Crew lead", "Full-time"), ("Apprentice painter", "Full-time · no experience needed")]
    rl = "".join(f'<li><span class="n">{num(i)}</span><span class="t">{t}</span><span class="d">{d}</span><span class="meta">Greater Burlington</span></li>' for i, (t, d) in enumerate(roles, 1))
    perks = [("Fair, steady pay", "Competitive hourly pay with room to grow as your skills do."),
             ("Learn the trade", "Prep, spraying, cabinets, lead-safe work. We train painters, not just hire them."),
             ("Work that matters", "Every job you finish helps a Vermont neighbor find housing.")]
    pk = "".join(f'<li><span class="n">{num(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(perks, 1))
    html = head("Careers | Painting With Purpose", "Join the Painting With Purpose crew in Greater Burlington, Vermont.", "careers")
    html += header("careers")
    html += f"""<main id="main">
{page_title("(careers)", "paint with us", "We’re always looking for reliable, careful people who take pride in their work. Experience helps, attitude matters more.")}
<section class="full">{photo("crew", "The Painting With Purpose crew beside their truck", sizes="100vw")}</section>
<section class="values wrap" aria-labelledby="why-h">
  <div class="sechead"><p class="label">(why here)</p><h2 id="why-h">a crew, not a job</h2></div>
  <ol class="steplist steplist--3">{pk}</ol>
</section>
<section class="roles wrap" aria-labelledby="roles-h">
  <div class="sechead"><p class="label">(open roles)</p><h2 id="roles-h">hiring now</h2></div>
  <ul class="rolelist">{rl}</ul>
</section>
<section class="formwrap wrap" aria-labelledby="apply-h">
  <form class="form" data-demo-form novalidate>
    <h2 id="apply-h" class="form__h">apply</h2>
    <fieldset><legend><span class="n">01</span>Which role?</legend><div class="chips">{choices("role", [("painter", "Painter"), ("lead", "Crew lead"), ("apprentice", "Apprentice")])}</div></fieldset>
    <fieldset><legend><span class="n">02</span>About you</legend>
      <div class="flds">{field("Full name", "name", auto="name")}{field("Phone", "phone", "tel", auto="tel")}{field("Email", "email", "email", auto="email")}</div>
      <label class="fld fld--wide"><span>Experience (a sentence or two is fine)</span><textarea name="experience" rows="3"></textarea></label>
    </fieldset>
    <p class="form__err" role="alert" hidden>Please fill in the highlighted fields.</p>
    <button class="btn" type="submit">Send application <span aria-hidden="true">→</span></button>
    <p class="form__fine">We reply to every application within a few days.</p>
  </form>
  <div class="form__done" hidden tabindex="-1"><h2>thanks!</h2><p>We’ve got your application and will be in touch soon.</p></div>
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
    html = head("Page not found | Painting With Purpose", "That page doesn’t exist.", "404")
    html += header("404")
    html += f"""<main id="main">
{page_title("(404)", "missed a spot", "That page doesn’t exist. It may have moved, or the link has a typo.")}
<section class="wrap nf"><a class="btn" href="index.html">back home <span aria-hidden="true">→</span></a> <a class="link" href="work.html">see the work</a></section>
</main>
"""
    html += FOOTER
    write("404.html", html)


if __name__ == "__main__":
    pairs = load_pairs()
    build_index(pairs)
    build_work(pairs)
    build_services()
    build_about()
    build_estimate()
    build_careers()
    build_404()
