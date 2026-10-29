# The Belgravian archive (pilot: the 1960s)

The club gazette, readable and searchable on belgraveharriers.com, with the original page scans beside the text.
Scans of every issue are by Alan Mead, the club historian (belgraveharriers.info/thebelgravian).

**Preview:** https://stephengardner1.github.io/belgrave-harriers-data/belgravian/ (not indexed by search engines).
The same reader goes on the club site as a code block: `site/belgravian-block.html`.
It reads the text data from here (`BV_BASE`) and the images from Cloudflare R2 (`BV_MEDIA`).

## What's here (32 issues, March 1960 to December 1969)

- `issues/B<no>.json` — every item in an issue: clean text transcribed from the scans, results tables, photo and scan
  crops, the people, events and places named, and where the item sits on each page (for the highlight on the scan).
- Images are not stored here (the full archive would pass GitHub Pages' 1 GB limit). They live in Cloudflare R2,
  bucket `belgravian-archive`, public at https://pub-16e146f74e014d32bd956564b0563306.r2.dev/belgravian/ :
  `pages/B<no>/` — every page as an image (1,112 pages); `crops/B<no>/` — 514 photographs and 146 scans of results
  that were hard to read. Upload with `tools/belgravian/r2up.py` (needs a short-lived R2 token; never commit it).
- `search.json` — the search index. `people.json` + `people/<letter>.json` — everyone named (about 4,500 people).
- `legends/` — legend profiles (so far: Gerry North), every fact linked to the item it comes from.
- `checks/` — the reading brief, the checking rules and a log of every correction made to each issue.

## How it was made

1. Each page was read as an image and transcribed exactly as printed, misprints included.
   Results that couldn't be read with confidence were kept as scans, and doubtful figures are marked `[?]`.
2. Every page was then checked a second time against the scan by a separate reader: every name, every table cell,
   the text, the photo crops and the highlight boxes. Corrections are logged in `checks/B<no>.check.md`.
3. People are matched across issues conservatively: an initial is only joined to a full name when just one person fits.
   Gerry and Geoff North are kept apart; a bare "G. North" stays unassigned.

## Rules

- This is a historical record: never edit text to change what was printed. Corrections go in the check logs.
- Spacing slips (words run together) are fixed; spelling, punctuation and capitals stay as printed.
- No people tags for names that aren't printed. Different initials or surname spellings are never merged.

Tools: `tools/belgravian/`.
