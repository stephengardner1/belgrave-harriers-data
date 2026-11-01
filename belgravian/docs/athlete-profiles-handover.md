# Athlete profile pages: design handover (1 Nov 2026)

This is for a separate design session. It covers the layout and design of the person / athlete profile pages in
The Belgravian reader. The original session keeps doing the reading, checking, privacy work and indexing. Its
priorities are integrity and quality. This session owns the look and behaviour of the profile pages only.

## Who you're working with
- Steve: Belgrave Harriers, and a brand and creative director by trade. He has strong design and content judgement
  but no coding background. Explain anything technical in plain words, show him screenshots rather than code, and
  ask his decisions one at a time.
- House style: the club site uses the claret and gold palette and the titling face already defined as CSS variables
  in the reader (`--claret`, `--gold`, `--ink`, `--body`, `--slate`, `--rule`, `--titling`, `--text`). Keep to them.

## Where it lives
- Repo (PUBLIC): `stephengardner1/belgrave-harriers-data`, branch `main`. GitHub Pages serves it.
- Live page: https://www.belgraveharriers.com/belgravian (unlinked Squarespace page). It loads the reader script
  from the repo, so a push updates the live site within a minute or two. Person pages are at `#p-<slug>`,
  e.g. `#p-john-thresher`.
- Preview without the club site:
  https://stephengardner1.github.io/belgrave-harriers-data/belgravian/index.html#p-john-thresher
- Reader source: `site/belgravian-block.html` (one file: CSS + HTML + JS). After editing, run
  `python3 tools/belgravian/build_loader.py` (writes `site/belgravian.js`, which is what the live page loads) and
  `python3 tools/belgravian/make_preview.py site/belgravian-block.html belgravian/index.html` (the preview page).
- Person page code: `personShow()` and `arts()` / `fullArt()` in the block. Styles: `.bv-person*`, `.bv-gallery*`,
  `.bv-arts*`, `.bv-art*`. Full-screen photo: `lightbox(src, cap, href, w)`.
- Images: `https://belgravian-images.stephendgardner.workers.dev/belgravian/` + `crops/B<no>/<file>` (photos) or
  `pages/B<no>/B<no>-pNN.webp` (page scans). The constant `MEDIA` in the reader holds the base.

## What's there now (prototype, commit 99e0e7e)
These are Steve's spec from 1 Nov:
1. The name at the top, with a line like "388 mentions from 1960 to 1988 · Surrey League record: slarchive.org".
2. A row of every photo the person is named in, with the year under each. The caption appears only when a photo is
   tapped (full-screen view), along with a link to the article it appears in.
3. Then every mention as an article, grouped by year: date, page, headline, and the passage that names them
   (their surname is highlighted when expanded). "Read the whole article" expands the full item in place, with a
   link to open it in the issue beside the page scan.
4. Legends (only Gerry North so far) also get a written profile with numbered source links, plus a facts panel.

Test people: John Thresher `p-john-thresher` (388 mentions, 34 photos), Laurie O'Hara `p-laurie-o-hara`
(671 mentions), Gerry North `p-gerry-north` (legend profile, 465 mentions).

## The data you can display
Coverage today: 77 issues, from the 1960s to December 1991. More decades will arrive, and the files grow as they do.
- `belgravian/people.json`: the light list of everyone (11,131 people): `{id, name, n (mentions), s (shard
  letter), legend?}`.
- `belgravian/people/<letter>.json`: full records keyed by id:
  - `name`, `aka` (every printed form of the name, e.g. "J. Thresher", "JOHN THRESHER"), `club`, `matchedBy`
  - `mentions`: in date order, `{id (item id e.g. "B145-25"), when ("July 1961"), p (page), h (headline),
    note?}`. The `note` is what the issue says about them in that item, often a race result such as "6th, 19:18",
    "114th" or "3rd in the GRE final at Gateshead".
  - `photos`: about 1,200 people have them. Each is `{f (crop path), c (printed caption), id (item id), w ("July
    1961")}`.
  - `photo`: a single fallback picture. `slarchive`: link to their Surrey League record if there is one.
  - `legend`: true or false. `x: 1` means a passages file exists.
- `belgravian/people/x/<id>.json`: `{x: [...]}`, one passage per mention, in the same order (3,536 people with 3
  or more mentions). Each passage is the sentence(s), results-table row ("10/ · J. Thresher · 43:41") or photo
  caption that names them. An empty string means none was found.
- `belgravian/legends/<slug>.json`: `name`, `standfirst`, `facts` ([label, value] pairs), `sections` (heading +
  paragraphs; `[[B155-01]]` marks are citations to items, `[[slarchive]]` to the Surrey League),
  `photos` (`file, caption, source, when`), `refs`, `sources`. `index.json` → `legends` lists them with a one-line
  `line` and a `photo`.
- `belgravian/issues/B<no>.json`: each whole issue (load only on demand, ~0.5 MB each): `issue, label, date,
  pageCount, pdfUrl, items[]`. Each item has:
  - `id, type` (cover, masthead, editorial, report, results, notice, letter, obituary, members, feature, column,
    records, photo, advert, poem, cartoon, other), `heading, byline, summary, text`
  - `tables[{caption, rows}]` (the first row is the header), `photos` and `scans` (`{file, caption, people[],
    credit, review}`)
  - `people[{printed, name, club, role (athlete/official/author/photographer/other), note, printedAs}]`
  - `events` (race tags with no year, so the same race groups across editions), `places, clubs, sport`
  - `pages`, `regions` (boxes on the page scans, as fractions of the page)
- `belgravian/search-<decade>.json`: the search index. `belgravian/index.json`: the issue list, `legends`, and
  `coming`.

### Worth exploring with Steve (derivable from the above without new reading)
- Career span and mentions per year (a small timeline or sparkline). The races they ran (`events` of their
  items), and positions and times (from `note`). Their clubs and roles (official, author, photographer as well as
  athlete). The people most often in the same items ("ran with").
- Where a summary needs new computed fields, prefer computing them in the browser from the files above. If they
  would be better precomputed, write the request down for Steve to pass to the reading/indexing session, which
  owns the data build (`tools/belgravian/build.py`, `people.py`).

## Rules the design must respect (data integrity)
- Everything is printed as it was: spelling, capitals and punctuation stay. Never tidy names or add facts that
  aren't printed. No invented first names, clubs, events or years.
- People are not merged across different initials or spellings. "Thresher" (surname only) is a separate entry from
  "John Thresher", deliberately. Don't present them as one.
- A person is tagged in a photo only when the caption names them. Photos marked `review: true` stay hidden.
- Privacy: from 1976 on, private addresses and phone numbers show as "[address withheld]" / "[phone number
  withheld]" and are blurred on scans. Never surface them by other means.
- Legend profiles cite an item for every fact. Any new written summary must do the same and must be checked
  against the items.

## Working rules for this session
- Touch only the reader: `site/belgravian-block.html` and the two files it generates (`site/belgravian.js`,
  `belgravian/index.html`). Possibly also the person-page template in `tools/belgravian/build_pages.py` (plain pages
  for search engines), but only after telling Steve. Do NOT edit `belgravian/issues/`, `belgravian/people/`,
  `tools/belgravian/build.py`, `people.py` or any privacy tool. The other session rebuilds those files and would
  overwrite your changes.
- Both sessions push to `main`: always `git pull --rebase` before pushing, and keep commits small.
- The repo is public: no secrets, keys or private details in commits.
- Check on a phone width (390px) and on desktop (1280px). Playwright with Chromium is the easy way. Show Steve
  screenshots.
- Speed matters on phones: don't load whole issues for a profile until the reader asks for an article.
