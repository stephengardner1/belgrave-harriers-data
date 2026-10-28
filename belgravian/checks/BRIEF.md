# The Belgravian archive — reading brief (1960s pilot)

You are digitising issues of *The Belgravian*, the club magazine of Belgrave Harriers (athletics club,
founded 1887). The goal is a searchable online archive on belgraveharriers.com: every item readable as
clean text, tagged, with photos cropped from the scans, and later "legend" profiles of great athletes.
This is a historical record: **transcribe what is printed, never improve, summarise away or invent.**

Folders (W = /tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv,
T = /tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bvtools):
- PDFs: W/pdf/B<no>_<year>.pdf     Rough machine text (garbled names!): W/txt/B<no>_<year>.txt (pages split by form feed)
- Render a page to look at: `sh T/page.sh W/pdf/B159_1966.pdf 5 W/work/<you>/B159-p05` then Read the PNG.
  Default 110 dpi is fine for typed text; use 160–200 dpi (4th arg) for small print, tables and names.
- Crop a photo or a scanned table: `python3 -I T/crop.py PDF PAGE X0 Y0 X1 Y1 OUT.jpg` (fractions of page width/height).
  After cropping, Read the jpg to confirm it is tight and complete; redo if not.
- Known Belgrave cross-country names 1962–73 from slarchive (for spelling checks only): W/slarchive-belgrave-names-1962-73.txt
- Write output to W/out/B<no>.json and crops to W/crops/B<no>/ . Your work dir: W/work/<your agent id>/

- Find where text sits on a page (for region boxes): `python3 -I T/lines.py PDF PAGE` prints every line of the rough text
  layer with its box as page fractions (y0-y1, x0-x1). The words may be garbled but the positions are accurate.

## Working rhythm (important — your context drops old images)
Work **one page at a time**: render it, read it, write that page's items, then move on. Keep a running file
W/work/<you>/B<no>.partial.json (list of items so far) and save after every page, so nothing is lost if early page
images drop out of your view. Assemble W/out/B<no>.json from it at the end of the issue.

## If page images stop being shown to you
Never fall back on the rough text layer for transcription or checking. If a page image doesn't display, try once more at a
lower resolution (e.g. 90 dpi, or crop the page into halves with crop.py and read each half). If images still don't show,
STOP: save what you have, and in your reply list exactly which pages were not read from images. Those pages will be redone.

## Method
Read **every page as an image** (don't trust the text layer; use it only as a typing aid). For each page,
split the content into items. An item is one self-contained piece: an article/report, an editorial, a
results table, a notice, a letter, an obituary, a list of new members, a column ("From the Belgravian 25
years ago", "Walking notes", "Club records"), a standalone photo, an advert, the cover, the masthead.
An article that runs across pages is ONE item (list all its pages). Short paragraphs under one heading on a page
(e.g. a run of club gossip notes separated by dots) are one item.

## Rules
1. **Text**: transcribe exactly as printed, from the image — original spelling, punctuation, abbreviations,
   capitalisation of names as printed. Fix only machine-reading errors. Paragraphs separated by a blank line.
   Unreadable word → `[illegible]`. Don't add your own words inside `text`.
2. **Results tables**: if you can read EVERY cell confidently, transcribe into `tables` (header row + rows, cells as printed).
   **If any part is hard to read, do not guess: crop the table as an image into `scans`** (Steve's rule: host the
   scanned jpg of difficult results). You can still put a short printed heading in `text`. Either way, tag the
   people you can read with confidence in `people`.
3. **Photos**: crop every photograph (not decorative drawings or crests unless notable) with its caption.
   Record caption exactly, photographer credit if printed, and the people named. File name:
   `B<no>-p<page>-<short-slug>.jpg`. Include the caption text in the crop only if it's part of the photo block — better
   to crop the photo alone and keep the caption as text.
4. **People**: tag every named person in the item. `printed` = exactly as printed ("G. North", "Gerry North",
   "R.Middleton"); `name` = the fullest name THIS item supports (expand "G. North" only if the same item gives the
   first name; otherwise leave the initial). Don't merge across items — a later step builds the people index.
   **Geoff North and Gerry North are two different Belgrave runners of the 1960s** — never assume one is the other;
   if only "G. North" is printed, keep "G. North". Add `club` if stated or clearly Belgrave, and `role`:
   athlete | official | author | photographer | other. Note notable facts in `note` (e.g. "won Inter-Counties 3 miles").
5. **Tags**: `events` (named competitions with year if clear, e.g. "AAA Championships 1966", "Inter-Counties 1966",
   "National Cross Country Championships 1966", "Surrey League (North Surrey League)", "Nijmegen march"),
   `clubs` (other clubs named), `places` (venues/towns), `sport` (one or more of: cross country, road, track, field,
   race walking, club life, administration, social, history).
6. **Privacy**: these issues are over 50 years old, so addresses may stay as printed.
7. `summary`: ONE plain sentence in your own words saying what the item is (this is the only place for your words).
8. Keep going to the end of each issue. Don't skip adverts or lists — they're short items.
10. **Decisions from the test run**:
   - Results tables: fully legible → `tables`. Legible except a few doubtful cells → still `tables`, write the doubtful
     cell as printed with ` [?]` after it, AND add a crop of the table to `scans`. Hard to read overall → `scans` only.
   - Short results written as a run-on line inside a report ("Result: 1/ A. Harris (Mitcham) 18:23 5/ M. Heck…") stay in
     `text`. Set results laid out in columns/rows become `tables`.
   - Same person printed several ways in one item → ONE people entry (fullest form in `name`), every printed form in
     `printedAs` (list), e.g. {"printed":"Charlie Dabbs","printedAs":["Charlie Dabbs","C. Dabbs"],"name":"Charlie Dabbs"}.
   - Clubs: list them in `clubs` exactly as printed ("H.H.H.", "Herne Hill"); don't expand abbreviations — the index step does that.
   - Photos: attach a photo to the article it illustrates (caption or placement ties it); otherwise make it its own `photo` item.
     A credit or caption printed on another page goes with the photo's item, adding a region on that page.
   - Masthead `officers`: keys as printed. Season events (e.g. Southern 1959-60): use the year the race was held.
   - When the issue contradicts itself (dates, positions), keep both as printed and say so in `summary`.
9. **Regions (important)**: readers will see the original scan beside the clean text, with the item highlighted.
   For every item give `regions`: one entry per page it occupies, `{"page": 3, "box": [x0, y0, x1, y1]}` as fractions
   of page width/height (0–1), covering the item's heading, text, tables and photos on that page. Be reasonably
   accurate (within ~2% of the page) — check a box by cropping it once with crop.py if unsure. Items in two columns or
   wrapping around another item may have two boxes on the same page (two entries with the same page).

## Output: W/out/B<no>.json
```json
{
  "issue": 159, "label": "August 1966", "date": "1966-08", "pdf": "B159_1966.pdf", "pageCount": 40,
  "officers": {"President": "R.T.Taylor", "Gen.Hon.Sec.": "A.A.Harley", "...": "..."},
  "items": [
    {
      "id": "B159-01", "pages": [3], "regions": [{"page": 3, "box": [0.27, 0.14, 0.94, 0.62]}], "type": "editorial",
      "heading": "Editorial", "byline": null,
      "summary": "Editorial congratulating Ray Middleton on his Commonwealth Games walking silver and praising Geoff North's season.",
      "text": "Congratulations! Ray Middleton. Our leading walker continued the tradition ...\n\nWhilst appreciating Middleton's grand performance, ...",
      "tables": [], "scans": [],
      "photos": [],
      "people": [
        {"printed": "Ray Middleton", "name": "Ray Middleton", "club": "Belgrave Harriers", "role": "athlete", "note": "silver, 20 miles walk, British Empire and Commonwealth Games, Jamaica"},
        {"printed": "Geoff North", "name": "Geoff North", "club": "Belgrave Harriers", "role": "athlete", "note": "won Inter-Counties 3 miles in Championship Best 13:18.8"}
      ],
      "events": ["British Empire and Commonwealth Games 1966", "Inter-Counties 1966", "European Championships 1966"],
      "clubs": [], "places": ["Jamaica", "Budapest"], "sport": ["race walking", "track"]
    },
    {
      "id": "B159-07", "pages": [5], "type": "results", "heading": "Oxfordshire County Championships", "byline": null,
      "summary": "One-mile result from the Oxfordshire County Championships with R. Bhatia third.",
      "text": "", "tables": [{"caption": "1 mile", "rows": [["Pos","Name","Club","Time"],["1","N.Barton","Oxford C","4:16.1"]]}],
      "scans": [], "photos": [], "people": [{"printed": "R.Bhatia", "name": "R. Bhatia", "club": "Belgrave Harriers / OUAC", "role": "athlete"}],
      "events": ["Oxfordshire County Championships 1966"], "clubs": ["Oxford City","Thames Valley Harriers"], "places": [], "sport": ["track"]
    }
  ]
}
```
`type` ∈ cover, masthead, editorial, report, results, notice, letter, obituary, members, feature, column, records,
photo, advert, poem, cartoon, other. `scans` and `photos` entries: {"file": "B159-p05-oxon-results.jpg", "page": 5,
"caption": "... as printed or null", "credit": null, "people": ["Geoff North"]}. Item ids: B<no>-01, -02 ... in page order.

Write each issue's JSON as soon as it's finished (valid JSON — check with `python3 -I -c "import json;json.load(open(...))"`).
When all your issues are done, reply with a short summary: issues, item counts, photos, scans, problems.
