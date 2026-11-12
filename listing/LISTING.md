# UserStyles.world listing

Field values for the FicAero listing, matched to the site's add/import form
(checked against the form templates on 2026-11-12). Use the **Import from URL**
route: it reads the UserCSS header, and "Mirror source code updates" then keeps
the listing's code in step with the repo whenever `@version` rises (the site
checks every four hours and only re-imports on a version change).

## Import form (`/add` → "Import userstyle")

| Field | Value |
|---|---|
| Import URL | `https://raw.githubusercontent.com/BladefuryDev/FicAero/main/ficaero.user.css` |
| Preview image | upload `listing/cover.png`, or paste `https://raw.githubusercontent.com/BladefuryDev/FicAero/main/listing/cover.png` |
| Category | `fanfiction.net` (the FAQ: domain plus TLD unless the TLD is .com or .org) |
| Mirror style metadata | off (that option is for USo-archive imports) |
| Mirror source code updates | **on** |
| Keep import URL private | off |
| Keep mirror URL private | off |

After the import, open the style's edit page and fill the fields below.

## Edit form

**Name** (max 50)

```
FicAero
```

**Description** (max 160, plain text, used for search and embeds)

```
FanFiction.net in the mid-2000s Frutiger Aero look: glossy accent bar, console-style home, cartridge story cards, clean reading column, light and dark.
```

**Homepage**

```
https://github.com/BladefuryDev/FicAero
```

**License**

```
MIT
```

**Notes** (Markdown)

```markdown
FanFiction.net in the mid-2000s Frutiger Aero look: a glossy title bar, a console-dashboard home, story lists as cartridge cards with the cover drawn as a small book, and a reading column left plain. Two colour schemes, Paper and Slate, and an accent colour that recolours the bar, the gloss, links and focus rings together. Everything outside the story text has small console-style motion: hover lift, press, caret turn, menu pop.

## What it restyles

- **Home**: the category table becomes two launcher blades of tile buttons with the site's own Silk icons.
- **Story lists** (search, browse, communities, profiles, Manage Stories): cartridge cards with the cover as a book, the meta line as a stat strip, Reviews as a button.
- **Browse lists**: a leaderboard with ranked rows, the top three glossed, and a sticky sort / letter toolbar.
- **Story page**: cartridge header, icon-button reader toolbar, one joined chapter selector above and below the text, the review form as a card. The site's own font, width, spacing and contrast buttons keep working; Story Contrast switches the page to Slate.
- **Communities, forums, the account panel** (sidebar menu, story editing header, Document Manager and the other tables) and **Manage Stories**.
- Nav bar, Fontastic Panel, footer and the site's modals.

## Settings (Stylus gear icon)

Colour scheme (Paper / Slate / follow system), accent colour, page width, reading column width, reading font, size and line height (all default to the site's own controls), 2000s gloss on/off, sticky menu bar, console-style motion on/off (off under reduced-motion), hide in-page ad slots, allow selecting story text.

## Notes

- Pure CSS: no scripts, no external requests beyond the site's own files. The Silk icons are served from fanfiction.net's own folder (Silk by Mark James, famfamfam.com, CC BY 2.5).
- The site's inline "Discover more" ad units are hidden by default; the anchored AdSense pill cannot be hidden by CSS alone, so a content blocker is still useful.
- Phone widths work but are not tuned.
- Bugs and requests: https://github.com/BladefuryDev/FicAero/issues

## Changelog

- 0.16.0 — renamed to FicAero; the title bar, gloss, links and focus rings follow the accent setting.
- 0.14 — Manage Stories; flat book covers with a mirrored spine on every card.
- 0.13 — the signed-in account panel.
- 0.12 — story page.
- 0.11 — communities and forums; home launcher; browse leaderboard; cartridge cards.
```

## Gallery

`listing/story-slate.png`, `listing/story-paper.png`, `listing/browse-paper.png`
(the site shows one preview image per style; the others can go in the Notes as
Markdown images once uploaded somewhere, or stay in the repo).
