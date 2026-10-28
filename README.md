# Painting With Purpose: website demo 2

A minimal, photo-led static site for [paintingwithpurpose.com](https://paintingwithpurpose.com). It follows the client's direction: a quiet home-design-studio feel, Gabe's own photos run large, the real logo, and very little "sales" UI.

No build step and no dependencies. Every page is plain HTML, CSS and JS.

## Run it locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Pages

| File | What's on it |
|---|---|
| `index.html` | Full-bleed photo hero, who we are, purpose, services list, one before/after, one review, closing line |
| `work.html` | Photo grid and the before/after slider with all 21 pairs |
| `services.html` | Five services as photo and text rows, how a job runs, service area, FAQ |
| `about.html` | Story, CVOEO, the crew |
| `careers.html` | Open roles and a short application form |
| `estimate.html` | Free estimate form (`?service=decks` preselects a service) |
| `404.html` | Not-found page |

## Design

- **Type:** Newsreader (upright only) for headings and body, Hanken Grotesk for nav and labels.
- **Color:** warm paper `#FAF8F4`, ink `#1C252C`, navy `#105677` from the logo plate, and brand sky blue `#68ABE4` for rules and hovers only.
- **Logo slot:** `.logo` in the header and footer, currently `assets/photos/pwp-logo.png`. Swap that file for the final logo.
- **Photos:** `assets/img/`, graded slightly (shadows lifted, skies 10% less saturated). Each has a full-size and `-sm` version, and the home, careers and services heroes have 4:5 crops for phones (`-m`).
- **Spacing:** one vertical rhythm, `--gap` in `site.css`, between every block on every page.

## Before going live

- [ ] Connect the estimate and careers forms (`[data-demo-form]` in `site.js`); they show a thank-you message but send nothing yet.
- [ ] Confirm photo captions and locations with Gabe.
- [ ] Confirm the service-area towns and the CVOEO total.
