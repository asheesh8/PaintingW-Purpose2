# Painting With Purpose: website demo 2

A static, multi-page redesign concept for [paintingwithpurpose.com](https://paintingwithpurpose.com), styled after foundry-house.com: lowercase editorial headlines, generous white space, a warm paper palette and hand-painted Vermont watercolors, with the client's own photos doing the heavy lifting.

No build step and no dependencies. Every page is plain HTML, CSS and JS.

## Run it locally

```bash
cd demo2
python3 -m http.server 8000
# open http://localhost:8000
```

(Opening `index.html` directly also works.)

## Deploy

Push this folder to its own repo, then do either of these:
- **GitHub Pages:** Settings → Pages → Deploy from branch → `main` / root.
- **Netlify or Vercel:** import the repo, with no build command and the root as the publish directory.

## Pages

| File | What's on it |
|---|---|
| `index.html` | Watercolor hero with on-the-job photo, intro, CVOEO giving stats, 5 services, watercolor strip, before/after showcase (6 projects), reviews, call to action |
| `services.html` | Each service in detail, 4-step process, service area, FAQ |
| `work.html` | Full before/after showcase (all 21 pairs), filterable photo gallery with lightbox, reviews |
| `about.html` | Story, purpose and CVOEO, values, meet Gabe and Zach |
| `careers.html` | Why work here, open roles, application form |
| `estimate.html` | Free estimate request form (`?service=decks` preselects a service) |
| `404.html` | Not-found page |

## Structure

```
assets/
  css/site.css        all styles (design tokens at the top)
  js/site.js          interactions (no libraries)
  js/projects.js      before/after data: edit titles and captions here
  photos/             client photos (DSC_*) and photos from the current site
  before-after/       21 before/after pairs from the current site
  art/                watercolor illustrations (see image-prompts.md)
image-prompts.md      ChatGPT prompts to regenerate each watercolor at full size
```

## Design

- **Type:** Bricolage Grotesque (headlines, UI) with Newsreader (body, plus light upright accents). No italics anywhere. Both fonts load from Google Fonts.
- **Palette:** paper `#FBF8F2`, forest `#2A3F33`, maple red `#B5432A`, ochre `#DCA23A`, sage `#8B9A7A`. These are sampled from the hero watercolor.
- **Breakpoints:** phone (under 600px), tablet (600–1020px, two-column where it fits), laptop/desktop.
- **Motion:** line-by-line headline reveals, hero parallax, a slider that auto-sweeps the first time it's seen, and drifting watercolor and service marquees. All motion turns off for visitors with "reduce motion" set.
- **Accessibility:** skip link, labeled controls, a keyboard-operable before/after slider (it's a range input underneath), focus rings, alt text, `aria-live` on changing content, and Esc to close the menu and lightbox.

## Before going live

Some copy is placeholder or inferred and should be confirmed with Gabe and Zach:

- [ ] **Forms:** the estimate and careers forms show a thank-you message but don't send anything yet. Connect them to Formspree, Netlify Forms or the client's CRM (`[data-demo-form]` in `site.js`).
- [ ] **Service-area towns:** the list is a reasonable Greater Burlington guess.
- [ ] **"Next milestone: $20,000" progress bar** on the home page is illustrative.
- [ ] **Gabe and Zach bios** on About, plus the "co-founder" titles.
- [ ] **Before/after captions** in `assets/js/projects.js` describe what the photos show. The project locations aren't known, so all of them say "Greater Burlington" (one says "Vermont").
- [ ] **Brand mark:** the header uses a refreshed house-and-drip mark. The client's existing logo is in `assets/photos/pwp-logo.png` if they'd rather keep it.
- [ ] **Watercolors:** regenerate them at full size with `image-prompts.md`.
- [ ] **Phone link:** 802-PAINTER dials `+1 802-724-6837`.
