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
- `hero-framing.json` — where the eyes sit in each news article's featured photo (found by face
  detection), so the hero photo at the top of an article can be framed with the eyeline on the top third.
  For the 548 older articles whose featured image is only a blank placeholder, it records the
  first photo inside the article instead (or that there is none).
- `road-relays.json` — Belgrave men at the national 12-stage and 6-stage road relays: 12-stage
  winners by year, every Belgrave 12-stage leg, and every Belgrave 6-stage leg. Copied on
  23 October 2026 from Steve Gardner's "Bels at Sutton Park" sheet for
  belgraveharriers.com/national-road-relays. Nothing has been edited.
- `tools/snapshot_published.py` — the script that made the copy, kept for the
  record. `tools/eyes.py` and `tools/run_eyes.py` made the hero framing file.

## Rules

- Never edit results to change what they say. This is a historical record.
- To add results for a new article, add a new entry rather than changing old ones.

The file is published at
`https://stephengardner1.github.io/belgrave-harriers-data/news-results.json`
and read by code on the club website.
