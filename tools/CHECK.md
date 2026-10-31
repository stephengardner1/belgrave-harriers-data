# The Belgravian archive — independent check

Another reader has digitised an issue of *The Belgravian* (Belgrave Harriers' club magazine) into a JSON file
following the brief at T/BRIEF.md (read it first — it defines the format and rules). You did NOT make this file.
Your job is to check it against the original scans and correct it, so the published archive is accurate.
It is a historical record: the text must match what was printed, including original spellings and errors.

W = /tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv
T = /tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bvtools
- Issue file: W/out/B<no>.json   — before changing anything, copy it once to W/out/B<no>.orig.json (if that doesn't exist yet).
- Page images: W/pages/B<no>/B<no>-p<NN>.webp (Read them), or render sharper: `sh T/page.sh W/pdf/<file>.pdf N W/work/<you>/x 180`
- Boxes drawn on a page: `python3 -I T/overlay.py W/out/B<no>.json N W/work/<you>/ov.png` then Read it.
- Crops: W/crops/B<no>/ ; crop tool `python3 -I T/crop.py ...` and line positions `python3 -I T/lines.py PDF PAGE` as in the brief.

## If page images stop being shown to you
Never fall back on the rough text layer for transcription or checking. If a page image doesn't display, try once more at a
lower resolution (e.g. 90 dpi, or crop the page into halves with crop.py and read each half). If images still don't show,
STOP: save what you have, and in your reply list exactly which pages were not read from images. Those pages will be redone.

## Check, page by page (one page at a time; save fixes as you go)
1. **Completeness**: everything printed on the page is in some item (headings, small notes, captions, adverts, lists).
2. **Names**: every personal name on the page is spelled exactly as printed in `text`/`tables`, and tagged in `people`
   with the right `printed`/`name`. No first names invented: "G. North" stays "G. North" unless the same item prints the
   first name. Gerry North and Geoff North are different people.
3. **Tables**: check every cell of every table against the image (positions, names, clubs, times). Where a cell can't be
   read with confidence, it must carry ` [?]` and the item must have a scan crop of the table.
4. **Text**: compare the text closely with the image for every item — at least every name, number, date and time, and
   read through the prose for dropped or invented words and lines. Original spelling stays.
5. **Photos and scans**: each crop is tight and complete, matches its caption, and the people tagged are the people named.
6. **Regions**: draw the overlay; every box covers its item within ~2% of the page; fix boxes that are off.
7. **Summaries**: one plain sentence, accurate, no claims the item doesn't support.

Fix problems directly in W/out/B<no>.json (keep it valid JSON). Keep a log at W/out/B<no>.check.md listing: pages checked,
each correction (item id, what was wrong, what it is now), and anything you could not resolve. Don't rewrite things that
are already right, and don't restyle the text.

Finish by validating the JSON and confirming every photo/scan file it names exists. Reply with a short summary:
corrections by kind (names, tables, text, crops, regions, missing items) and anything unresolved.
