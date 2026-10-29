# Belgravian check job (small, one page range)

W = /tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv
T = /tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bvtools

Read T/CHECK.md (and the parts of T/BRIEF.md it relies on), then check ONLY your assigned page range of one issue.
Be economical: concentrate on words, names, numbers, table cells, crops and boxes that matter to a reader; don't spend
effort on trivial punctuation differences unless they change meaning. view one page at a time, crop/zoom only where print is small or doubtful, don't re-read other pages.
- If W/out/B<no>.orig.json doesn't exist, copy W/out/B<no>.json to it first.
- Items that run onto pages outside your range: check only the part on your pages.
- HEAVY mode (when your job says so): earlier work on these pages was partly typed from the rough text layer, so verify
  EVERY word, name, number and table cell against the image, and redraw boxes as needed. Otherwise do the normal check.
- Edit W/out/B<no>.json in place with a short python read-modify-write (another job may have edited other pages of
  this issue earlier, so always load the current file just before writing; never rewrite it from memory).
- Append to W/out/B<no>.check.md: a line exactly "Pages checked: A-B" then your corrections (item id: was → now) and
  anything unresolved.
- Words running off the edge of the scan: transcribe only the visible part and mark the rest [illegible]; never complete words by guesswork.
- Spacing: fix typing slips in WORD SPACING only (words run together like "canloan" → "can loan", words split like "bi gguns" → "big guns", line-break hyphens). Keep spelling, punctuation and capitals exactly as printed (misspellings stay). Log spacing fixes briefly.
- Ditto marks in tables stay as printed ("), never filled in with the repeated value.
- Never merge differently printed surnames into one person (Carton ≠ Carter); a likely misprint goes in a note, not a merge.
- Faint or overtyped letters: keep a letter only if you can see it in the image (a worn/clogged letter may be read as the
  letter it matches elsewhere on the page); otherwise [illegible], with the likely reading in the person's note.
- Typewriter stand-ins for digits (capital I or l for 1, o/O for 0 inside numbers, e.g. "I97I", "3o9") are written as the
  digits they stand for; don't change them back to letters.
- A common word with one partly printed letter that can only be that word (e.g. "for_idable" = formidable) is written
  in full; keep [illegible] for genuinely uncertain letters, and for names and numbers.
- Never use the rough text layer as a source. If page images stop displaying, stop and say which pages are left.
Reply in under 100 words: corrections by kind (text, names, tables, crops, boxes, missing items) and anything unresolved.
