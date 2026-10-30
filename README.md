# Belgrave Harriers data

Frozen copies of results tables that appear in news articles on
[belgraveharriers.com](https://www.belgraveharriers.com/news).

Many older articles embedded a Google Sheet of results. Those sheets can be
edited or deleted at any time, and three have already disappeared. This
repository keeps a permanent copy of what readers saw, so the club site can
show the results in its own house style without depending on Google.

## Files

- `news-results.json` — every results table embedded in a news article, as
  published on 23 October 2026: 77 embeds in 64 articles (2019–2025), every tab,
  rows and columns exactly as readers saw them. Filtered tabs (for example
  "Belgrave finishers") keep only the rows the author's filter showed; hidden
  rows and columns stay hidden. Nothing has been edited.
  Entries with a `link` were added later: results an article linked to on a site that
  has since removed them, rebuilt from the official results (source given in each entry).
- `hero-framing.json` — where the eyes sit in each news article's featured photo (found by face
  detection), so the hero photo at the top of an article can be framed with the eyeline on the top third.
  For the 548 older articles whose featured image is only a blank placeholder, it records the
  first photo inside the article instead (or that there is none).
- `road-relays.json` — Belgrave men at the national 12-stage and 6-stage road relays: 12-stage
  winners by year, every Belgrave 12-stage leg, and every Belgrave 6-stage leg. Copied on
  23 October 2026 from Steve Gardner's "Bels at Sutton Park" sheet for
  belgraveharriers.com/national-road-relays. Nothing has been edited. Later
  additions (2025 and 2026 results, 6-stage winners from ERRA's official list, and one
  correction) are listed with their sources under `additions` in the file.
- `tools/snapshot_published.py` — the script that made the copy, kept for the
  record. `tools/eyes.py` and `tools/run_eyes.py` made the hero framing file.

## Rules

- Never edit results to change what they say. This is a historical record.
- To add results for a new article, add a new entry rather than changing old ones.

The file is published at
`https://stephengardner1.github.io/belgrave-harriers-data/news-results.json`
and read by code on the club website.

## Fonts

`fonts/` holds Castoro Belgrave, the club's headline typeface, used by the club
website's custom CSS:

- `CastoroBelgrave-Semibold` (weight 600) for headlines, subheads, news cards
  and navigation. 600 is the heaviest weight: `CastoroBelgrave-Bold` holds the
  same Semibold design, so anything styled at 700 gets 600 without a faux bold.
- `CastoroBelgraveTitlingLight-Regular` for large heritage capitals, such as the
  history page title.

Each comes as `.woff2` with a `.woff` fallback. Castoro Belgrave is a modified
version of [Castoro](https://github.com/TiroTypeworks/Castoro) by Tiro Typeworks,
redrawn after the 1960s Belgravian mastheads. It is released under the SIL Open
Font License 1.1, as the original requires; see `fonts/OFL.txt`.

## Archive: the old belgraveharriers.com, 2000–2013

Much of the club's news from about 2000 to 2013 was lost when the website moved to
WordPress and then to Squarespace. It has been recovered from the Internet Archive's
Wayback Machine and is being restored to the News page, tagged "Archive".

- `archive/photos/` — the 552 photos from the old site that the Wayback Machine kept
  (of 1,204 the old pages used), saved on 23 October 2026. Folder names follow the old
  site's, with file names tidied (lower case, hyphens). Nothing has been edited, cropped
  or resized.
- `archive/photos.json` — for each photo: its original address on the old site, the date
  of the Wayback Machine copy, and the old page it appeared on.
- `archive/stories/` — the 774 restored stories, one HTML file each, filed by year: 514 race
  reports, 192 features (Skipper's Corner, obituaries, club news, history pieces) and 68
  round-ups of the short results entries, one per old results page. Every paragraph is word for
  word as published on the old site; only the old layout code and menus were removed.
- `archive/stories.json` — the index: title, date, categories, tags, writer and original page
  for every story.
- `archive/bylines.json` — the 35 stories whose own text names their writer (e.g. "Charlie
  Dickinson writes"), read by the club website to show the byline. Others show "Belgrave archive".
- `archive/import/` — the same stories as WordPress export files, split by period, in the form
  Squarespace imports.
- `tools/archive/` — the scripts that collected the pages and photos from the Wayback Machine
  and turned them into the stories above, kept for the record.

The restored stories are imported into Squarespace from here, and this copy is kept
permanently so the history doesn't depend on any one website platform again.
