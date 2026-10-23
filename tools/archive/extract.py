"""Turn archived belgraveharriers.com (2000-2013) pages into clean posts.
Text is never reworded: we only remove the old site's layout code and menus."""
import re, csv, json, sys, datetime
from bs4 import BeautifulSoup, NavigableString, Comment
from html import escape as html_escape

ROOT = "/home/claude/archive_raw"
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
MON_SHORT = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"sept":9,"oct":10,"nov":11,"dec":12}
DATE_RE = re.compile(r"(\d{1,2})(?:st|nd|rd|th)?(?:\s*(?:[-–/&]|and|to)\s*\d{1,2}(?:st|nd|rd|th)?)?\s+(" + MONTHS + r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?,?\s+((?:19|20)\d\d)", re.I)
DATE_RE_US = re.compile(r"(" + MONTHS + r")\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+((?:19|20)\d\d)", re.I)

KEEP = {"p","br","b","strong","i","em","u","ul","ol","li","table","thead","tbody","tr","td","th","sup","sub","blockquote"}
DROP = {"script","style","img","hr","form","input","select","map","area","iframe","object","embed","noscript","head","title","meta","link"}


def index():
    return {r["page"]: r for r in csv.DictReader(open(f"{ROOT}/archive_index.csv"))}


def load(row):
    raw = open(f"{ROOT}/pages/{row['file'].strip()}", "rb").read()
    m = re.search(rb'charset=["\']?([\w-]+)', raw[:3000])
    enc = (m.group(1).decode().lower() if m else "windows-1252")
    if enc in ("iso-8859-1", "latin-1", "us-ascii", "ascii"):
        enc = "windows-1252"
    try:
        return raw.decode(enc, "replace")
    except LookupError:
        return raw.decode("windows-1252", "replace")


def parse_date(text):
    m = DATE_RE.search(text)
    if m:
        d, mon, y = int(m.group(1)), m.group(2).lower(), int(m.group(3))
    else:
        m = DATE_RE_US.search(text)
        if not m:
            return None, None
        mon, d, y = m.group(1).lower(), int(m.group(2)), int(m.group(3))
    mo = MON_SHORT.get(mon[:4] if mon[:4] == "sept" else mon[:3])
    try:
        return datetime.date(y, mo, d), m
    except (ValueError, TypeError):
        return None, None


# Set by the builder: a function taking an <img> src and returning the photo's public address
# (or None when the photo wasn't recovered). Without it, photos are left out.
PHOTO_RESOLVER = None
IMG_TOKEN = "\u27e6IMG{}\u27e7"


def clean(fragment_html):
    """Old layout HTML -> simple HTML (paragraphs, bold, italics, lists, tables, photos)."""
    soup = BeautifulSoup(fragment_html, "html.parser")
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    images = [i.get("src", "") for i in soup.find_all("img")]
    placed = []
    if PHOTO_RESOLVER:
        for img in soup.find_all("img"):
            url = PHOTO_RESOLVER(img.get("src", ""))
            if url:
                placed.append((url, (img.get("alt") or "").strip()))
                img.replace_with(IMG_TOKEN.format(len(placed) - 1))
    for t in soup.find_all(DROP):
        t.decompose()
    for t in soup.find_all(True):
        style = (t.get("style") or "").replace(" ", "").lower()
        if t.name in ("span", "font") and ("font-weight:700" in style or "font-weight:bold" in style):
            t.name = "strong"
            t.attrs = {}
            continue
        if t.name in ("span", "font") and "font-style:italic" in style:
            t.name = "em"
            t.attrs = {}
            continue
        if t.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            t.name = "p"
        if t.name == "div":
            t.name = "p" if not t.find(["p", "table", "div"]) else t.name
        if t.name not in KEEP:
            t.unwrap()
            continue
        t.attrs = {k: v for k, v in t.attrs.items() if k in ("colspan", "rowspan")}
    # bold done with a style attribute was lost above; that's fine, headings handled separately
    html = str(soup)
    html = html.replace("\xa0", " ")
    html = re.sub(r"[ \t\r\n]+", " ", html)
    html = re.sub(r"<(b|strong|i|em|u)>\s*</\1>", "", html)
    html = re.sub(r"<p>\s*(<br/?>\s*)*</p>", "", html)
    html = re.sub(r"\s*<br/?>\s*</p>", "</p>", html)
    html = re.sub(r"<(strong|b|em|i)>\s+", r"<\1>", html)
    html = re.sub(r"<p>\s+", "<p>", html)
    html = re.sub(r"<p>((?:<(?:b|strong|i|em)>)*)([A-Z])((?:</(?:b|strong|i|em)>)*) (?=[a-z]{2,})", r"<p>\1\2\3", html)  # drop capitals
    html = re.sub(r"\s+</p>", "</p>", html)
    html = re.sub(r"(</p>|</table>|</ul>|</ol>)\s*", r"\1\n", html)
    # photos: each on its own line, just before the block it sat in, caption underneath
    if placed:
        # rebuild: find each token's top-level block again on the original html
        doc = BeautifulSoup(html, "html.parser")
        for n, (url, alt) in enumerate(placed):
            tok = IMG_TOKEN.format(n)
            hit = doc.find(string=lambda s: s and tok in s)
            if hit is None:
                continue
            top = hit
            while top.parent is not None and top.parent is not doc:
                top = top.parent
            fresh = NavigableString(str(hit).replace(tok, ""))
            hit.replace_with(fresh)
            if top is hit:
                top = fresh
            fig = doc.new_tag("p")
            fig.append(doc.new_tag("img", src=url, alt=alt))
            cap = alt if alt and not re.search(r"\.(jpe?g|gif|png)$", alt, re.I) else ""
            if cap:
                fig.append(doc.new_tag("br"))
                fig.append(cap)
            top.insert_before(fig)
            top.insert_before("\n")
        html = str(doc)
        html = re.sub(r"<p>\s*</p>\n?", "", html)
        html = re.sub(r"<(b|strong|i|em|u)>\s*</\1>", "", html)
    html = html.strip()
    return html, images


def text_of(html):
    return re.sub(r"\s+", " ", BeautifulSoup(html, "html.parser").get_text(" ")).strip()


def split_season_page(page_html):
    """Season pages: one report per block between horizontal rules.
    Returns (page_title, [ {heading, date, body_html, words, images} ])."""
    soup = BeautifulSoup(page_html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    parts = re.split(r"<hr[^>]*>", page_html, flags=re.I)
    entries = []
    for part in parts:
        html, imgs = clean(part)
        paras = re.findall(r"<p>(.*?)</p>", html, re.S)
        if not paras:
            continue
        # the heading is the first paragraph that contains a date
        for i, p in enumerate(paras[:3]):
            ptxt = text_of(p)
            d, m = parse_date(ptxt)
            if d and len(ptxt) < 220:
                break
        else:
            continue
        heading = ptxt
        rest = paras[i + 1:]
        body = "".join(f"<p>{p}</p>\n" for p in rest)
        # tables after paragraphs
        tables = re.findall(r"<table>.*?</table>", html, re.S)
        if tables and "<table>" not in body:
            body += "\n".join(tables)
        entries.append(dict(heading=heading, date=d, body=body,
                            words=len(text_of(body).split()), images=imgs))
    return title, entries


def headline_from_heading(heading):
    """'AAA Men's 12-Stage Road Relay Championship, Sutton Coldfield, 23 April 2005.'
    -> 'AAA Men's 12-Stage Road Relay Championship, Sutton Coldfield' (words unchanged)."""
    d, m = parse_date(heading)
    h = heading
    if m:
        h = (heading[:m.start()] + heading[m.end():])
    h = re.sub(r"\s+", " ", h).strip()
    h = re.sub(r"^[\s,.;:–-]+|[\s,.;:–-]+$", "", h)
    return h


def main_cell(page_html):
    """The table cell (or body) holding the most text of its own: the article itself."""
    soup = BeautifulSoup(page_html, "html.parser")
    best, best_n = None, 0
    for td in soup.find_all(["td", "div", "body"]):
        own = 0
        for s in td.find_all(string=True):
            if isinstance(s, Comment):
                continue
            par = s.find_parent(["td", "div", "body"])
            if par is td:
                own += len(s.strip())
        if own > best_n:
            best, best_n = td, own
    return soup, best


def extract_feature(page_html):
    soup, cell = main_cell(page_html)
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    # gather the article: the best cell plus its sibling cells in the same table
    table = cell.find_parent("table") if cell and cell.name == "td" else None
    src = str(table) if table else str(cell)
    html, imgs = clean(src)
    html = re.sub(r"<strong>\s+", "<strong>", html)
    paras = re.findall(r"<p>(.*?)</p>", html, re.S)
    first = text_of(paras[0]) if paras else ""
    d, m = parse_date(first) if first else (None, None)
    heading = None
    if d and len(first) < 200:
        heading = first
        html = html.replace(f"<p>{paras[0]}</p>", "", 1).strip()
    else:
        d, m = parse_date(text_of(html)[:600])
    return dict(page_title=title, heading=heading, date=d, body=html,
                words=len(text_of(html).split()), images=imgs)


NAV = re.compile(r"^(www\.belgraveharriers\.com|home\b.{0,40}|top of page|back|index|.*\bindex|skipper'?s corner|obituary|obituaries|more pictures|\||.*back to top of page.*)$", re.I)


def is_data_table(t):
    rows = t.find_all("tr")
    cells = [len(r.find_all(["td", "th"])) for r in rows]
    return len(rows) >= 3 and sum(c >= 3 for c in cells) >= 3 and not t.find("table")


def extract_feature(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    body = soup.body or soup
    # layout tables -> plain blocks; keep genuine data tables
    for t in body.find_all("table"):
        if not is_data_table(t):
            for cell in t.find_all(["td", "th"]):
                cell.name = "div"
            for x in t.find_all(["tr", "tbody", "thead"]):
                x.unwrap()
            t.name = "div"
    html, imgs = clean(str(body))
    html = re.sub(r"<strong>\s+", "<strong>", html)
    html = re.sub(r"<b>\s+", "<b>", html)
    paras = re.findall(r"<p>(.*?)</p>|(<table>.*?</table>)", html, re.S)
    blocks = [(f"<p>{p}</p>" if p else t, text_of(p or t)) for p, t in paras]
    # drop menu lines at the start and end
    def junk(b):
        return "<img" not in b[0] and (NAV.match(b[1]) or len(b[1]) < 3)
    while blocks and junk(blocks[0]):
        blocks.pop(0)
    while blocks and junk(blocks[-1]):
        blocks.pop()
    heading, date = None, None
    for i, (b, tx) in enumerate(blocks[:6]):
        d, m = parse_date(tx)
        if d and len(tx) < 160 and m.end() >= len(tx.rstrip(". ")) - 1:
            heading, date = tx, d
            blocks.pop(i)
            break
    if not date:
        date, _ = parse_date(" ".join(tx for _, tx in blocks)[:800])
    out = "\n".join(b for b, _ in blocks)
    return dict(page_title=title, heading=heading, date=date, body=out, blocks=blocks,
                words=len(text_of(out).split()), images=imgs)
