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
- `tools/snapshot_published.py` — the script that made the copy, kept for the
  record.

## Rules

- Never edit results to change what they say. This is a historical record.
- To add results for a new article, add a new entry rather than changing old ones.

The file is published at
`https://stephengardner1.github.io/belgrave-harriers-data/news-results.json`
and read by code on the club website.
