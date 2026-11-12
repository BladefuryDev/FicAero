# FicAero

A FanFiction.net theme in the mid-2000s Frutiger Aero look: glossy accent surfaces, a
console-dashboard home, cartridge story cards and a plain reading column. Named
2026-11-12 (it was "FanFiction.net Refresh" until v0.15.2).

A Stylus userstyle for fanfiction.net. The site's markup has not changed in years
(Bootstrap 2 plus a thin layer of its own classes, no CSS custom properties), so the
theme works by stable ids and classes and should survive routine site updates.

## Install

1. Install the Stylus extension (Firefox or Chromium).
2. Open the raw file in the browser:
   `https://raw.githubusercontent.com/BladefuryDev/FicAero/main/ficaero.user.css`
   (or drag a local copy onto a tab). Stylus recognises the `.user.css` name and offers
   to install it. Stylus then checks the header's `@updateURL` (the same raw file) and
   offers each new `@version`, so bumping the version and pushing is how fixes reach
   readers; a local install from a file gets no updates.
3. Settings live in Stylus's style editor (the gear next to the style):

| Setting | Default | Notes |
|---|---|---|
| Colour scheme | Paper (light) | Slate (dark), or follow the system |
| Accent colour | #2f6fdb | links, title bar, selection gloss, focus ring, tagline rainbow (see Changing colours) |
| Page width | 1180 px | the site pins itself to 975 px; this makes it fluid up to the value |
| Reading column width | 820 px | 0 = full width; the site's own Full / 3/4 / 1/2 buttons still work |
| Reading font | Site setting | the site's Fonts panel keeps working when this stays on Site setting |
| Reading font size | 0 (site) | the site's A+ / A- buttons keep working at 0 |
| Reading line height | 1.6 | 0 hands line spacing back to the site's Expand / Tighten buttons |
| 2000s gloss on the blue surfaces | on | top bar, cookie bar, primary buttons, open menu button and menu-item highlight get a lighter-to-darker gradient, a hairline top highlight and the half-height glass band; off gives flat fills. The accent gradient is derived from the accent colour (16% lighter to 14% darker) |
| Keep the menu bar in view | on | sticky menu bar |
| Console-style motion | on | hover lift, press, caret turn, menu pop, search widen; never touches the story text; off under prefers-reduced-motion |
| Hide in-page ad slots too | on | the "Discover more" link units in the header, before the footer and the anchored pill are always hidden; this switch also hides the in-content AdSense slots |
| Allow selecting story text | off | lifts the site's `user-select: none` on the story body |

## Project rule: motion

Everything outside the reader moves like a console game menu: short (60 to 350 ms), eased
(`cubic-bezier(0.2, 0.8, 0.2, 1)`), one small cue per interaction (lift on hover, press on
click, caret turns, menu pops in, field widens on focus, story row nudges). Pleasing, never
busy. The story text itself never animates. All of it sits under the `motion` switch and is
disabled for users with reduced-motion set.

## Top bar tagline

"unleash your imagination" is a bare text node in the top bar, so CSS cannot select it.
The theme zeroes the bar's font size (hiding the node), gives every real child its size
back (the logo needs `!important` because its inline style is `1.1em`, the login span
gets 13 px), and re-renders the tagline as the separator's `::after` with the same words.
That box takes a hover underline: a three-colour gradient drawn at zero width that slides
in from the left to full width in 320 ms and leaves to the right (only the width
transitions; the anchor side flips instantly), whose hue rotates on a 7 s loop, so the colour you land on each
hover is effectively random. CSS has no randomness; this is the honest substitute. On
phones the separator (and with it the tagline) is hidden.

## Modals (Fontastic Panel, image preview, follow)

The site runs Bootstrap 2 modals with a "dynamic" option that nests the panel inside the
backdrop. On open it adds `in` to the backdrop and waits for `webkitTransitionEnd` on it
before showing the panel; on close it waits for the same event before removing the
backdrop. Two consequences for the theme:

- The backdrop must actually transition. The site's own CSS fades opacity but swaps the
  background from transparent to 80% black on `in`, which is why the dim used to pop. The
  theme gives the backdrop a constant colour and fades opacity only, both ways.
- Never set `transition: none` on the backdrop or the panel (for example in a
  reduced-motion block): the end event never fires and the modal never opens. The theme's
  reduced-motion rule shortens transitions to 10 ms instead.
- The close pop is the site's own bug: the panel's transitionend bubbles up to the
  backdrop (the panel is nested inside it) and hits the just-attached "remove backdrop"
  listener a millisecond later. The theme sidesteps it in CSS: the closing panel
  transition is visually done in ~150 ms but lasts 600 ms so nothing ends before the
  site's 500 ms fallback timer; the backdrop starts dimming via `:has()` as soon as the
  panel loses `.in` and settles at 0.02; the final 0.02 to 0 step after the fallback is a
  real transition whose end event lets the site remove the backdrop. Measured: panel 93%
  faded at 190 ms, backdrop dim gone by 400 ms, removed at ~735 ms, no leftovers.
  The project stays script-free on purpose: readers install a theme, not a toolchain.

## Home launcher

The home page's two category tables become two blades, Fanfiction and Crossovers, each a
column of 52 px tile buttons with a Silk icon in a square well, the name, and an arrow
that slides in under the cursor (hover or keyboard focus). The rules are scoped by
`#content_wrapper_inner:has(> .table-bordered > #gui_table1)`, which only the home page
matches. The tables are flattened with `display: contents` so the links stack; the two
5 px spacer divs are hidden; the tweets/ad table is hidden unless the "Show the
FictionPress tweets box" switch is on. Icons come from the site's own
`/static/ficons/<name>.png` (Silk, CC BY 2.5, Mark James), drawn pixelated, mapped by the
link's path (`a[href$="/anime/"]` matches both the plain and the crossover link). The
Stylus-language mixin builds the `url()` through `unquote` so it survives compilation.
See DESIGN.md for the direction (2000s console dashboard) and the icon table.

## Changing colours

Every colour lives in the PALETTE block at the top of the theme body: `paper-*` for the
light scheme, `slate-*` for the dark one, plus the shared `rainbow` (tagline underline)
and `ring` (focus rings and icon wells). The accent itself is the Stylus "Accent colour"
setting, and since v0.15.0 everything blue follows it: links, the gloss gradients, focus
rings, the tagline rainbow (accent first, then two stops 108° and 181° round the wheel)
and the title bar. The bar is a deep shade on the accent's own hue (v0.15.0 nudged it
18° towards indigo to keep the original navy `#262a5e`, but that read as purple beside
a blue accent, so v0.15.1 dropped the nudge and the default bar is now `#263b5e`), with
its saturation scaled from the accent's (60%), so a grey accent gives a grey bar; the
three gloss stops and the Slate bar take the original navy's lightness and saturation.
The selection gloss (active rows, primary buttons, glossed chips) is built on the accent
darkened by 15% (v0.15.2: a vivid green accent made active rows glow while the bar stayed
deep), so with the default blue it runs `#3373dc` to `#1c50a6`; links, markers, borders
and focus rings keep the accent itself. Stylus prints
the derived stops as `hsla()`, which is valid CSS. Nothing below the palette names a raw
colour except white/black overlays. Use `//` comments on palette lines: the Stylus
language keeps a `/* */` comment that sits on a value line as part of the value.

## Search page

The search form becomes one toolbar above the results: Story dropdown, the keyword field
stretched to fill, a glossy Search button and Options, all 36 px. The form's table is
flattened to blocks (table, body, rows and the cell, which carries a `width="1%"` hint
that has to be reset). The Options row that the site toggles with jQuery stays toggleable
and opens as a panel under the toolbar with capped labels. The Narrow Results box (the
word-count listbox) is a later sibling of the form, so it cannot be moved into the panel;
it is hidden while Options is closed and absolutely positioned over the panel's right-hand
side when open, with the panel padded to make room. "N found:" becomes a small-caps
status line; the results then run full width.

## Story cards (the cartridge)

Every `.z-list` row (search results, category listings, profiles) is a cartridge card: the
cover drawn as a small book on the left, the title with the latest-chapter chevron as a
square button at the right, author, summary, and the meta line as a dashed-off stat strip
with the "reviews" link seated bottom right as a button. The glossy navy column that
first sat behind the book was dropped on 2026-11-12 (user's call); the row's hover rule
still sets `background-image: none !important`, because the site paints its own hover
gradient there. Mechanics, since the markup is fixed: the cover image, which the site
floats inside the title link, is absolutely placed and lies flat with a drop shadow (the
six-degree turn and the page-edge shadows were dropped on 2026-11-12, user's call; the
`book-turn` variable now only centres it vertically) and is centred in the card's 112 px
left padding, 18 px clear each side; the spine strip is the title link's
`::before`, and the mirrored slice is the image's box reflection. Rows without a cover get
a blank book from the row's `::before`. On hover the card lifts. The "Reviews: N" in the meta line is plain text in
listings, so it cannot be made clickable; only the story page links the number. Under
600 px the column and book are dropped.

## Browse lists (the leaderboard)

Category lists such as `/crossovers/game/` (1,399 entries) become a leaderboard. The site's
"Sort by Popularity / Filter by name: All . # . A … Z" line is a `center` whose links
re-render the list through the site's script; the theme zeroes its font size to drop the
text nodes and separators, restyles the sort link as a button with a sort glyph and the
letters as a chip rail, and sticks the bar under the menu. The list is a three-column
table of `div > a + span.gray`; the table parts are flattened with `display: contents`
and the container becomes a two-column grid of 40 px rows. Ranks come from a CSS
counter in document order, which is the popularity order (first column first), so
reading order equals rank; the first three entries of the first column get the accent
gloss on their badge. Counts keep the site's parentheses (text nodes cannot be
trimmed). Under the Name sort the badges show alphabetical positions, since the theme
cannot tell which sort is active. One column under 760 px. Plain category pages
(`/game/`) carry the letters in a `.lc-wrapper` with no sort link and put the heading image
inside a small table; both shapes get the same bar and chips. The heading image (the
generic script or arrow-switch icon) is swapped for the category's Silk icon through nine
URL-scoped `@-moz-document url-prefix()` sections at the end of the theme, one per
category covering `/x/` and `/crossovers/x/`, using `content: url()` on the image; the
markup names no category, so only the URL can.

## Community pages

`/community/Name/id/` pages share the story-row markup but open with a breadcrumb, a
bordered header card (`div.tcat` title, `table#gui_table1` with the community image,
Follow link, focus and founder lines), a filter form named `myform` with six selects and
a Go button, then the rows and a `center` pager. The header card gets a glossy navy
title bar; its single table cell becomes a grid (image down the left; Follow as a button
and the feed link as an icon button on the first row; the focus line and the founder /
stories / followers / id line as two stat rows; the description, which is the cell's last
div, across the bottom in its own labelled area). The form becomes a toolbar with a
glossy Go, and the pager becomes chips with the current page (a `b`) in the accent gloss.
Three Stylus-language traps met here: a `//` comment on a declaration line inside braces
broke the parse; a `grid-template-areas` value split over several lines does too, so each
areas value sits on one line; and `{name}` is not interpolated inside a quoted string, so
a selector variable built from another (`ccell`) is concatenated (`community + ' > …'`),
not written as `'{community} > …'`. The last one compiled silently and shipped rules the
browser dropped; `tools/build.js` now fails on any unexpanded `{placeholder}`. Two scoping traps
fixed here: the home launcher used to key on "a bordered div holding `#gui_table1`",
which this header card also is, so the whole page was laid out as the launcher; the
launcher now requires both home tables. And the category pages' Filters modal also
carries a form named `myform`, so the community scope excludes modals.

## Forums

`/forum/Name/id/` pages get a light pass only: rounded header image and larger forum
name, the pager as chips, the topics table as a card with the breadcrumb strip and
small-caps column heads, filter badges as chips (active one glossed), count badges in a
mono face, accent pin icons, rounded avatars. Scoped by the striped topics table having a
`thead`. The forum page also carries a `#gui_table1` and a `#gui_table2` in bordered divs,
which used to satisfy the home launcher test; the launcher now keys on the home tables
holding the category links (`a[href="/anime/"]`, `a[href="/crossovers/anime/"]`), which
no other page has.

## Story page

Scoped by the page holding `#storytextp`. The header `#profile_top` becomes a cartridge:
navy spine column with the cover as the book (the cover sits in a clickable span whose
`::before` is the spine strip; the image carries the page edges and the mirrored slice),
Follow/Fav as a glossy button top right, the title at 22 px, a muted by-line, the summary,
and the meta line as a dashed-off strip. The reader toolbar's spans become 36 px icon
buttons; the width and spacing sub-rows keep the site's hidden state (they start with
`.hide` and no inline display, and the site's script writes an inline display to open and
close them, so the rule that hides them keys on exactly those two states) and show as
chips when open. The chapter controls above and below the text become one joined
selector: Prev, the chapter select centred and 320 px wide, Next, each 38 px; on the last
chapter there is no Next and the select takes the right radius. The review form becomes
a card with its empty 336 px spacer cell hidden. The story text itself is untouched beyond
the reading settings. Under 700 px the spine column and book are dropped. The site's
Story Contrast button writes inline colours the palette overrides, so on its own it does
nothing; the theme reads the `.xlight` class it adds to the story text and switches the
page to Slate while it is set (a no-op when Slate is already on). The site's cookie keeps
the state, so a dark-marked story opens in Slate on later visits.

## Account panel

The signed-in area (`/account/`, `/story/`, `/docs/`, `/alert/`, `/pm2/` …) shares one
layout: a two-row table whose second row holds a `ul.topnav` accordion on the left and the
page's cards on the right. Scoped by that table (`#content_wrapper_inner > table > tbody >
tr > td > ul.topnav`). The table becomes blocks and the second row a flex row (sidebar
220 px, content fills the rest, stacked under 760 px); the cells keep their default
stretch so the sticky sidebar has room to travel. The notice row (`div.panel_normal`)
becomes a quiet strip.

The sidebar is a console menu: section headers small-caps with the site's +/- marker in
the mono face on the right, items as cursor rows (bar and marker on hover, the current one
glossed). The site writes "- " into every item's text, and Chrome's `::first-letter` takes
the dash, the space and the first letter together, so hiding it that way loses a letter.
Instead the anchor gets a negative `text-indent` of 1.3ch (the width of "- " in Verdana)
and a `clip-path` that cuts off the first 22 px; the row background, cursor bar and marker
therefore live on the `li`, which is not clipped.

Cards come in three shapes, told apart by structure:

- The story editing header (one row of tab links ending in a right-aligned Delete link):
  glossy navy title bar, the links as 32 px chips, Delete in the reviews colour. The
  cells carry `width="1%"`, which would shrink them to nothing as flex items, so they get
  `flex: none; width: auto`. Keyed on the right-aligned single-link cell, not
  `:first-child`, because the cell opens with script tags.
- Label / value tables (no `thead`; Info, Account Settings, the properties form): label
  cells carry `width="1%"` and become small-caps muted labels, with the `div.gray` /
  `span.xgray` hint under them in a smaller plain face. In forms the labels sit at the top
  of the row.
- Data tables with a `thead` (Document Manager, Story Chapters, Alert Settings): the
  header row goes small-caps; the `width="1%"` cells are left alone, since there they are
  data, not labels.

Form controls follow the site-wide styling; text inputs and the summary fill the row up to
560 px, the Save button (`button[type=submit].btn`) is the accent gloss. Checked on the
story properties page; the other pages were only inspected by structure.

### Manage Stories

`/story/story_tab_list.php` has no cards: a bold "Published Stories" heading, the bare text
": click on story to edit", an `hr`, then `#story-list`, a List.js block holding the
filter input, the bare text "Sort by:", the sort spans separated by bare " - " text, an
`hr`, and `div.sort-list` of `div.z-list` story entries. The entries are the listing cards
with two differences, so the cartridge rules were widened rather than copied: the title
link is `a.l-title` (added beside `a.stitle`) and the cover image is a direct child of the
card (the spine strip now also draws for `.z-list:has(> img.cimage)`). The block becomes a
panel: a toolbar strip (Sort label, the spans as chips with the active one glossed and a
▲/▼ from List.js's `l-asc` / `l-desc` class, the filter box on the right, growing to fill
its row when it wraps) with the card list below it in a lighter well that escapes the
strip's padding with negative margins. The bare text nodes are hidden by zeroing the font
size on the cell and the block and restoring it on their children.

## Fontastic Panel

Restyled as a console menu: small-caps header with an accent diamond, a full-width
selector button, a scrollable font list (each entry in its own face, accent marker on
hover), a preview card, and a Close / Save footer. Width and margin are left to the site:
in its "dynamic" mode the panel is `position: static` inside a `.modal-wrapper` that
centres it with `left: 50%; width: 560px; margin-left: -280px`, so overriding the panel's
own width or margin shifts it off centre.

Reveal on font change, CSS only: the site's pick handler sets the preview's font and
removes `.open` from the list in one step, so the preview's reveal animation is parked
with `animation: none` while `.modal-body:has(.btn-group.open)` matches and restarts the
moment the list closes. A `::before` cover the colour of the card sits over the text and
slides off left to right in twelve steps over 0.25 s (`steps(12, end)`), so the new text
appears in chunks that read as words. CSS cannot wrap words, so the steps are by width,
not by word boundary; a true word-by-word reveal would need a script, which this project
avoids. Nothing runs while the list is open. (0.5 s was tried first; the user asked for
twice the speed.)

## Footer

One 40 px row at the end of the page: the five links and the X icon, centred. The body is
a flex column at least one viewport tall and the footer takes `margin-top: auto`, so on a
short page (the home page) it rests on the bottom edge of the window with the free space
above it, and on a long page (a chapter) it simply follows the last element. Not fixed:
it never covers content. The markup is five stacked divs (links, spacer, icon, spacer,
"ray id"); the spacers and the ray id are hidden, and the " . " separators between the
links are bare text nodes that vanish under `font-size: 0` on their row while the links
get their size back. (A fixed bar was tried first and rejected.)

## Nav bar

The menu is a two-cell table in the markup. The theme flattens it with `display: contents`
on the row and cells and lays it out as a centred flex row. Menu buttons, the Story
dropdown button and the search field are all 34 px tall. The open menu button fills with
the accent colour and takes the focus ring.

## What CSS cannot hide

The anchored Google pill at the bottom right (`#google-anno-sa`, hung directly off the html
element) sets every CSS property inline with `!important`, which beats any stylesheet rule.
A content blocker such as uBlock Origin removes it; the theme does not try to cover it.

## How the site's reader controls work (so the theme cooperates)

Found by reading the page's own functions in a browser (`_fontastic_*`, `toggleTheme`):

- Font size: inline `font-size: <n>em` on `#storytext` (default 1em from `.storytext`).
- Width: inline `width: <n>%` on `#storytext`.
- Line height: inline `line-height` on `#storytext` (default 1.25).
- Font: inline `font-family` on `#storytext` from the Fonts modal.
- Contrast: inline `background-color` on `.xcontrast`, `.xcontrast_outer`, `.lc*` and the
  class `xlight` on `.xcontrast_txt`. All saved in the `xcookie2` cookie.

The theme's palette rules use `!important`, so they beat those inline backgrounds in both
schemes. Reader settings are only emitted when their Stylus value is non-zero / not "Site
setting", so the site's buttons keep working otherwise.

## Repository layout

The folder is its own git repository (initialised 2026-11-12), meant to live at
`github.com/BladefuryDev/FicAero` on `main`; the header's `@updateURL`,
`@homepageURL` and `@supportURL` point there, so the repository name and branch are
part of the install link and should not change once readers have installed from it.
`build/` and `node_modules/` are ignored.

- `ficaero.user.css` — the theme (Stylus-language preprocessor).
- `tools/build.js` — compiles the theme the way the Stylus extension does, with the
  header defaults or overrides, into `build/`. Needs the `stylus` npm package:
  `npm install stylus@0.63.0` in some folder, then
  `node tools/build.js <that folder> [theme=dark readsize=18px ...]`.
  Every branch should be compiled before a release: default, `theme=slate readfont=georgia
  readsize=18px hideads=1 allowselect=1`, and `theme=auto stickymenu=0 readwidth=0px readlh=0`.
  Stylus injects option values bare (`theme=slate;`), so select values are short idents that
  the body maps; never use `light` or `dark` as values, they are Stylus-language colour
  functions and the comparison goes wrong silently. Select option values in the header must
  be JSON strings or the whole header fails to parse and Stylus lints the body as plain CSS.
- `listing/cover.png` — the UserStyles.world cover (1600×900): the home page cut into
  seven diagonal shards, one per accent colour, Slate last, each seam glowing in the
  accent of the shard to its left, the FicAero wordmark on a glass plate bottom-left.
  Built by `tools/cover.py` from full-window screenshots of the home page (chrome cropped
  at 82 px; the accent is sampled from the diamond beside "FANFICTION"), with the
  wordmark from `tools/wordmark.py` (three treatments; `aero` is the one in use).
  `python tools/cover.py <shots dir> listing/cover.png <shot ...>` in display order.
  The other files in `listing/` are gallery screenshots for the listing (story page in
  Slate and Paper, a browse listing), made by `tools/shots.py` from the same kind of
  full-window shots: chrome cropped, scaled to 1600 wide. `listing/LISTING.md` holds
  the field values for the UserStyles.world form (import from the raw URL with code
  mirroring on; category `fanfiction.net`; description, notes, licence).
- `tools/unwrap.js` — strips the `@-moz-document` wrapper from a compiled build so the
  CSS can be pasted into a page as a `<style>` for preview (Chromium drops
  `@-moz-document` blocks in inline styles, and the desktop app's browser pane blocks
  localhost subresources on https pages, so serving the file does not work either).
- `tools/mcp_drive.py` — drives the Craft Anything MCP server over stdio for one job
  (used for the first capture attempt).
- `captures/` — `xss26.css` (the site's stylesheet, with a pretty-printed copy) and
  DOM skeletons of a category listing and a story page.

## Known gaps

- The mockup's stat bubbles (rating, chapters, words as chips, rating coloured) cannot
  be built: the meta line is one run of text with only the two date spans as elements,
  and listings carry no data attributes (checked on a category listing, a search result
  and Manage Stories, 2026-11-12). They would need a script, which this theme rules out;
  parked by the user.

- Phone widths are usable but not tuned (the menu table and ad slots still force some
  horizontal overflow).
- Of the account panel only the story properties and Manage Stories pages have been
  looked at in the browser; the PM inbox
  (`.bubbledNNormal` rows), the Traffic Stats page (a different wrapper) and the thead
  tables (Document Manager, Story Chapters) were checked by structure only. Profiles and
  the login page have not been looked at.
- Craft Anything's private headless browser is stopped by the site's Cloudflare
  interstitial, so its site capture and pixel compare could not be used on the live
  site. Observation was done in the Claude desktop app's browser instead.
