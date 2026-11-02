# Belgravian reading job (small, one page range) — 1970s

W = /tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv
T = /tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bvtools

Read T/BRIEF.md first: it has every rule for transcription, tables, scans, photos, people, tags and regions.
Then read ONLY your assigned page range of one issue. Other jobs read the other ranges of the same issue, one after
another, so you add to a shared file.

Differences from BRIEF.md for these jobs:
- Spelling aid for names: W/slarchive-belgrave-names-1969-80.txt (Belgrave Surrey League runners 1969–80; for 1980s issues use W/slarchive-belgrave-names-1979-90.txt; for 1990s and 2000s issues use W/slarchive-belgrave-names-1990-2009.txt). Use it to
  confirm a reading, never to change what is printed.
- Output: W/out/B<no>.json. If it doesn't exist (you have the first range), create it with the issue header
  (issue, label, date "YYYY-MM", pdf, pageCount, officers if printed on your pages) and "items": [].
  If it exists, load it just before writing and append; never rewrite it from memory.
- Item ids: use "B<no>-tmp-<page>-<n>" (n = 1, 2… on that page). They are renumbered after the whole issue is read.
- An item that runs past your last page: write what's on your pages and set "continues": true on it.
  If the piece jumps ("continued on page 39"), also set "continuedOn": 39.
  Before you start, look at EVERY item in the file with "continues": true. If one carries on in your pages (the next
  page, or its "continuedOn" page), continue THAT item (append text, tables, people, pages, regions) and remove
  "continues"/"continuedOn" when it ends. If an item without "continuedOn" doesn't carry on onto your first page, remove
  its flag. Leave flags whose "continuedOn" page is beyond your range.
- Save after every page (load, append/update, write) so nothing is lost.
- Crops go to W/crops/B<no>/ exactly as BRIEF.md says.

- Event tags: the competition name only, no year or season ("Inter-Counties", not "Inter-Counties 1971").

Lessons from the 1960s checks (follow them now, so checking finds less):
- Words running off the edge of the scan: transcribe only the visible part and mark the rest [illegible]; never complete
  words by guesswork.
- Faint or overtyped letters: never fill them in by guesswork or from a names list; if you can't see a letter, mark it
  [illegible]. A worn or clogged letter may be read as the letter it is only when it matches that letter elsewhere on the page.
- Typewriter stand-ins for digits (capital I or l for 1, o or O for 0 inside numbers, e.g. "I97I", "3o9") are
  written as the digits they stand for, so dates and times stay searchable. Everything else stays as typed.
- Fix word-spacing slips only; keep spelling, punctuation and capitals exactly as printed.
- Ditto marks in tables stay as printed ("), never filled in.
- Never merge differently printed surnames or initials into one person (Carton ≠ Carter, G. Dance ≠ W. Dance); a likely
  misprint goes in a note.
- NAMES AS PRINTED (Steve, 2 Nov 2026), in every people entry, photo tag and note:
  - `name` is the printed form; only capitals and hyphen/space may be tidied ("T benjamin" → "T Benjamin").
  - Never expand an initial or nickname ("K Sempers" stays "K Sempers" even if "Kevin Sempers" is printed nearby).
  - Never give a surname to a first-name-only mention, or a first name to a surname-only mention.
  - Never use the spelling aid, other items or your own knowledge to complete or "correct" a name.
  - No entry for a name that refers to no one (a wrong name someone was called) or a pen-name you can't place.
  - Before saving, re-read your people entries: each `name` must appear on the page with the same letters.
- Don't add header rows or bracketed labels of your own inside text or tables.
- Be economical: one page image at a time at 110 dpi; zoom (160–200 dpi or a crop) only for small print, tables and names.
- Read every page from its own image, even if it repeats a page from another issue (officers, winners lists); never
  copy text from another issue's file.
- A common word with one partly printed letter that can only be that word (e.g. "for_idable" = formidable) is written
  in full; keep [illegible] for genuinely uncertain letters, and for names and numbers.
- Never use the rough text layer as a source. If page images stop displaying, save, stop and list the pages not read.

Reply in under 80 words: pages read, items, photos, scans, anything doubtful.
- 1990s photo-set print, "rn" that looks like "m" (Steve's rule, 1 Nov 2026): write "rn" wherever the r+n reading is a
  real word or name and the shapes fit touching letters (Herne Hill, Southern, turned, Turner, morning, Barnet,
  Osbourne). Don't zoom past 300 dpi for this, and add no note. Keep "m" with a note only where the r+n reading would
  not be a real word or name.
- Disk: put scratch renders in W/work/<your-job>/ and delete that folder's large images when you finish.
- Rankings or results kept as scans because the print is too small: still tag in "people" every Belgrave name you can
  read clearly (their profile pages depend on it).
