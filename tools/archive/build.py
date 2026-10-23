"""Build a WordPress (WXR) import file for Squarespace from restored stories."""
import re, json, html, datetime, sys
sys.path.insert(0, "/home/claude/tools")
from extract import *

NAME_MAP = json.load(open("/home/claude/name_map.json"))
import extract, urllib.parse
PAGES_BASE = "https://stephengardner1.github.io/belgrave-harriers-data/archive/photos/"
_PHOTOS = json.load(open("/home/claude/belgrave-harriers-data/archive/photos.json"))


def _key(url):
    p = urllib.parse.urlsplit(url)
    host = (p.hostname or "").lower()
    host = host[4:] if host.startswith("www.") else host
    return host + urllib.parse.unquote(p.path).lower()


_BY_ORIGINAL = {_key(v["original_url"]): k for k, v in _PHOTOS.items()}


def use_page(page):
    """Tell the extractor which old page we're on, so photo addresses resolve."""
    base = "http://www." + page
    def resolve(src):
        if not src:
            return None
        k = _BY_ORIGINAL.get(_key(urllib.parse.urljoin(base, src.strip())))
        return PAGES_BASE + urllib.parse.quote(k) if k else None
    extract.PHOTO_RESOLVER = resolve
NOTE = ('<p><em>Restored from the club\'s earlier website, belgraveharriers.com, '
        'and published here as originally written.</em></p>')

# Races, leagues and venues -> tag (matched on the headline and the text)
PLACES = [
    (r"surrey (cross[- ]country |xc |road and country )?league|surrey league", "Surrey League"),
    (r"south of (the )?thames", "South of the Thames"),
    (r"lloyd park", "Lloyd Park"), (r"wimbledon common", "Wimbledon Common"),
    (r"parliament hill", "Parliament Hill"), (r"sutton park|sutton coldfield", "Sutton Park"),
    (r"nonsuch", "Nonsuch Park"), (r"mitcham", "Mitcham Common"), (r"richmond park", "Richmond Park"),
    (r"battersea park", "Battersea Park"), (r"crystal palace", "Crystal Palace"),
    (r"wormwood scrubs", "Wormwood Scrubs"), (r"petersham", "Petersham"),
    (r"12[- ]stage", "12-Stage Road Relay"), (r"6[- ]stage", "6-Stage Road Relay"),
    (r"4[- ]stage", "4-Stage Road Relay"), (r"3[- ]stage", "3-Stage Road Relay"),
    (r"(ecca|english|national) (cross[- ]country|cc|xc)|\bthe national\b", "National Cross Country"),
    (r"(seaa|southern) (cross[- ]country|cc|xc)( champ)", "Southern Cross Country"),
    (r"inter[- ]counties", "Inter-Counties"), (r"london marathon", "London Marathon"),
    (r"british (athletics )?league|\bbal\b", "British Athletics League"),
    (r"women'?s southern league", "Women's Southern League"),
    (r"(?<!women's )(?<!womens )southern (athletics )?league", "Southern Athletics League"),
    (r"uk women'?s (athletics )?league|ukwal", "UK Women's Athletics League"),
    (r"rosenheim", "Rosenheim League"), (r"enfield league", "Enfield League"),
    (r"european clubs'? cup|european cup", "European Clubs' Cup"),
    (r"surrey (county )?(cross[- ]country |road )?(champ|relays)", "Surrey Championships"),
    (r"race ?walk|\brwa\b", "Race Walking"),
]


def categories_for(page, headline):
    sec = page.split("/")[1]
    f = page.split("/")[-1]
    cats = []
    if sec == "obituary" or sec in ("general", "skippers_corner", "sot"):
        cats = ["Club"]
    elif f.startswith(("rc_", "rr_", "cc_")) or sec == "road_country":
        cats = ["Road and Cross Country"]
    elif f.startswith(("tf_", "ya_", "rw_", "ve_")) or sec in ("track_field", "young_athletes", "race_walking"):
        cats = ["Track and Field"]
    elif f.startswith("tri"):
        cats = ["Club"]
    if "Road and Cross Country" in cats or sec == "skippers_corner":
        h = headline.lower()
        if re.search(r"\b(men'?s|men)\b", h):
            cats.append("Mens Road&XC")
        if re.search(r"\b(women'?s|women|ladies|belles)\b", h):
            cats.append("Womens Road&XC")
    return cats


def tags_for(headline, body_text, extra=()):
    """Race, league and venue tags come from the headline (what the story is about);
    athlete tags from full names anywhere in the story."""
    tags = ["Archive", *extra]
    hay = headline.lower()
    for pat, tag in PLACES:
        if re.search(pat, hay) and tag not in tags:
            tags.append(tag)
    for spelling, tag in NAME_MAP.items():
        if re.search(r"\b" + re.escape(spelling) + r"\b", body_text) and tag not in tags:
            tags.append(tag)
    return tags


def slugify(s):
    s = re.sub(r"[’'`]", "", s.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:80]


def tidy_headline(h, page_title=""):
    h = re.sub(r"\bfull results\b", "", h, flags=re.I)
    h = re.sub(r"\s*,\s*([,.]\s*)+", ", ", h)
    h = re.sub(r"\s+", " ", h).strip(" ,.;:–-")
    # bare 'Match 3, Tooting' style headings borrow their page's subject
    if re.match(r"^(match|round|semi-final|final|leg|race)\b", h, re.I) and page_title:
        subject = re.sub(r"^(Belgrave Harriers\s*|Track & Field\s*|Road Running & Cross Country\s*)", "", page_title).strip()
        h = f"{subject}: {h}"
    return h


def post(title, date, body_html, cats, tags, source_url):
    return dict(title=title, date=date, body=body_html + "\n" + NOTE, cats=cats, tags=tags,
                slug=f"{date:%Y-%m-%d}-{slugify(title)}", source=source_url)


def wxr(posts, path):
    """Write a file laid out exactly like a real WordPress export (WXR 1.2)."""
    base = "https://www.belgraveharriers.com"
    def cdata(s):
        return "<![CDATA[" + s.replace("]]>", "]]]]><![CDATA[>") + "]]>"
    # unique, letter-first web addresses: 'hats-off-to-thames-2005'
    seen = set(p["slug"] for p in posts if p.get("fixed_slug"))
    for p in posts:
        if p.get("fixed_slug"):
            continue
        slug = slugify(p["title"])[:70].strip("-")
        if not re.search(r"(19|20)\d\d", slug):
            slug += f"-{p['date'].year}"
        n, s0 = 2, slug
        while slug in seen:
            slug, n = f"{s0}-{n}", n + 1
        seen.add(slug)
        p["slug"] = slug
    all_cats = sorted({c for p in posts for c in p["cats"]})
    all_tags = sorted({t for p in posts for t in p["tags"]})
    terms = []
    for i, c in enumerate(all_cats, 1):
        terms.append(f"  <wp:category><wp:term_id>{i}</wp:term_id><wp:category_nicename>{cdata(slugify(c))}</wp:category_nicename>"
                     f"<wp:category_parent>{cdata('')}</wp:category_parent><wp:cat_name>{cdata(c)}</wp:cat_name></wp:category>")
    for i, t in enumerate(all_tags, len(all_cats) + 1):
        terms.append(f"  <wp:tag><wp:term_id>{i}</wp:term_id><wp:tag_slug>{cdata(slugify(t))}</wp:tag_slug>"
                     f"<wp:tag_name>{cdata(t)}</wp:tag_name></wp:tag>")
    items = []
    for i, p in enumerate(posts, 1):
        dt = datetime.datetime.combine(p["date"], datetime.time(12, 0))
        cats = "".join(f'\n    <category domain="category" nicename="{slugify(c)}">{cdata(c)}</category>' for c in p["cats"])
        tags = "".join(f'\n    <category domain="post_tag" nicename="{slugify(t)}">{cdata(t)}</category>' for t in p["tags"])
        items.append(f"""
  <item>
    <title>{cdata(p['title'])}</title>
    <link>{base}/{p['slug']}/</link>
    <pubDate>{dt.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    <dc:creator>{cdata('belgravearchive')}</dc:creator>
    <guid isPermaLink="false">{base}/?p={p.get('id', i)}</guid>
    <description></description>
    <content:encoded>{cdata(p['body'])}</content:encoded>
    <excerpt:encoded>{cdata('')}</excerpt:encoded>
    <wp:post_id>{p.get('id', i)}</wp:post_id>
    <wp:post_date>{cdata(dt.strftime('%Y-%m-%d %H:%M:%S'))}</wp:post_date>
    <wp:post_date_gmt>{cdata(dt.strftime('%Y-%m-%d %H:%M:%S'))}</wp:post_date_gmt>
    <wp:comment_status>{cdata('closed')}</wp:comment_status>
    <wp:ping_status>{cdata('closed')}</wp:ping_status>
    <wp:post_name>{cdata(p['slug'])}</wp:post_name>
    <wp:status>{cdata('publish')}</wp:status>
    <wp:post_parent>0</wp:post_parent>
    <wp:menu_order>0</wp:menu_order>
    <wp:post_type>{cdata('post')}</wp:post_type>
    <wp:post_password>{cdata('')}</wp:post_password>
    <wp:is_sticky>0</wp:is_sticky>{cats}{tags}
  </item>""")
    doc = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
\txmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
\txmlns:content="http://purl.org/rss/1.0/modules/content/"
\txmlns:wfw="http://wellformedweb.org/CommentAPI/"
\txmlns:dc="http://purl.org/dc/elements/1.1/"
\txmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
  <title>Belgrave Harriers archive</title>
  <link>{base}</link>
  <description>Stories restored from belgraveharriers.com, 2000-2013</description>
  <pubDate>{datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
  <language>en-GB</language>
  <wp:wxr_version>1.2</wp:wxr_version>
  <wp:base_site_url>{base}</wp:base_site_url>
  <wp:base_blog_url>{base}</wp:base_blog_url>
  <wp:author><wp:author_id>1</wp:author_id><wp:author_login>{cdata('belgravearchive')}</wp:author_login><wp:author_email>{cdata('')}</wp:author_email><wp:author_display_name>{cdata('Belgrave archive')}</wp:author_display_name><wp:author_first_name>{cdata('Belgrave')}</wp:author_first_name><wp:author_last_name>{cdata('archive')}</wp:author_last_name></wp:author>
{chr(10).join(terms)}
  <generator>https://wordpress.org/?v=6.4</generator>
{''.join(items)}
</channel>
</rss>
"""
    open(path, "w", encoding="utf-8").write(doc)
