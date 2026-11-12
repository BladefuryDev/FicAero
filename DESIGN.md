# FanFiction.net Refresh — design brief

**Theme: a retro game platform with modern touches.** The site was built in the
mid-2000s and still ships the Silk icon set from that era. Instead of hiding that, the
theme leans into it: the home page and menus feel like a game platform's dashboard of
that generation, rebuilt with today's spacing, type, dark mode and motion. Readers should
feel they are launching stories, not browsing a table.

Everything here is CSS only. No scripts, no external requests beyond the site's own
assets. Readers install a theme, not a toolchain.

## The two halves

| | Retro platform | Modern touches |
|---|---|---|
| Layout | panels and tiles, a "cursor" that highlights the thing you are on | fluid width, centred, 10 px radii, soft single shadow |
| Type | tracked small-caps section labels with the accent diamond | system Verdana / Segoe for everything readable; no pixel fonts (they would need an embedded font file) |
| Icons | Silk 16 px, served from the site's own `/static/ficons/`, drawn crisp | aligned to an 8 px grid, accent-tinted frames, never scaled smoothly |
| Colour | one accent, paper or slate surfaces, hard 1 px borders | CSS custom properties, follow-system scheme, colour-scheme set for native controls |
| Motion | stepped easing (`steps(n)`) for reveals and cursor moves, short and decisive | eased lifts and presses (`cubic-bezier(.2,.8,.2,1)`), all under 300 ms, off under reduced motion |
| Feedback | a press squashes, a selection fills with the accent, a caret turns | focus rings, hover states on every control, no layout shift |

## The cursor idea

Game menus do not have "hover"; they have a cursor. The theme treats hover and keyboard
focus the same way: the row or tile you are on gets the accent edge, the arrow marker, a
lift. Only one thing is "selected" at a time. Lists (categories, chapters, story rows,
dropdown entries) all use the same cursor treatment so the site feels like one platform.

## Motion language (outside the reader)

- **Stepped** for anything that reveals or switches content: the Fontastic preview
  (12 steps, 0.25 s), future chapter or tab switches. Reads as a machine doing work.
- **Eased** for anything the pointer does: lift on hover (-1 to -2 px), press on click
  (scale 0.97, 60 ms), menus popping in (160 ms), fields widening on focus.
- **Never** on the story text. The reader is a page, not a console.
- Reduced motion: animations off, transitions 10 ms (never none; modals depend on a
  transition ending).

## Components, in the platform language

- **Top bar**: the console's status strip. Logo with a hover shadow, icon buttons.
- **Menu bar**: centred row of 34 px buttons plus the search group; sticky.
- **Home**: the launcher. Two aligned columns (Fanfiction / Crossovers), each row a tile
  button with a Silk icon, name, arrow on cursor, FF / X tag. Tweets embed off by default.
- **Story lists**: rows as tiles with the cursor treatment; title, meta, cover.
- **Story page**: header card, reader toolbar as icon buttons, chapter select as a
  console selector; the reader itself stays plain.
- **Fontastic Panel**: the settings screen. Small-caps header, selector, scrollable list
  with each face previewed, stepped reveal on pick.
- **Modals**: dim fades both ways; panel drops in.
- **Footer**: one row at the end of the page, resting on the window edge on short pages.

## Icon mapping (Silk, all present on the site)

| Category | Icon | Category | Icon | Category | Icon |
|---|---|---|---|---|---|
| Anime/Manga | pencil | Books | book | Cartoons | emoticon_smile |
| Comics | newspaper | Games | controller | Misc | bricks |
| Movies | film | Plays | group | TV | television |

Icons are drawn at 16 px, or at 32 px with `image-rendering: pixelated` where a bigger
mark is wanted; never smoothly scaled. Silk is CC BY 2.5 by Mark James (famfamfam); the
credit line lives in the theme header.

## Decisions

- **Era anchor: 2000s console dashboard** (chosen 2026-11-11). Blades and big tiles over
  dense lists and window chrome. The launcher is two blades side by side, each a column
  of 52 px tile buttons; a tile holds the Silk icon in a square well, the name, and an
  arrow that slides in under the cursor.

- **Story cards: the cartridge** (chosen 2026-11-11 from four mockups in
  `mockups/story-cards.html`). The cover as a small book: cover plus mirrored spine,
  lying flat (the turn, the page edges and the navy column behind it were all dropped
  on 2026-11-12; the story page header keeps its column, its book lies flat too); title, latest-chapter button, author, summary, meta strip,
  reviews button bottom right.

- **Browse lists: the leaderboard** (chosen 2026-11-11 from four mockups in
  `mockups/browse.html`). Sticky toolbar (sort button, letter rail), two columns of
  ranked rows with a numbered badge, top three in the accent gloss, count as a mono tag.

- **Story page** (built 2026-11-11): header as a cartridge with the book, reader toolbar
  as 36 px icon buttons, chapter controls as one joined console selector above and below
  the text, review as a card. The reader text stays a plain page.

- **Account panel** (built 2026-11-12): the accordion sidebar as a sticky console menu
  (small-caps sections, cursor rows, the current item glossed), the story editing header
  as a glossy title bar with tab chips, label / value tables with small-caps labels, data
  tables with a small-caps head row. Same card language as the rest; no new motion beyond
  the row hover. Manage Stories (2026-11-12) reuses the cartridge card under a toolbar
  strip of sort chips with the filter box on the right.

## Open choices

- Whether section labels get a subtle "window title" treatment (a 1 px inner highlight
  under the header) to push the retro feel, or stay flat.
