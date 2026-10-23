"""Full build: every restorable story from the old belgraveharriers.com (2000-2013)."""
import sys, re, json, datetime, collections, html as htmllib
sys.path.insert(0, "/home/claude/tools")
from build import *

ix = index()
OLD = "https://www.belgraveharriers.com/"

SKIP_SECTIONS = {"rankings", "records", "statistics", "photo_gallery", "fixtures", "stories", "sot", "speed_gp", "2014"}
SKIP_FILES = re.compile(r"^(ix_|fix_|index|soon|fixtures|gpentry|archive\.htm)", re.I)
FEATURE_SECTIONS = {"obituary", "skippers_corner", "general", "articles", "back_track", "profiles",
                    "eHarrier", "off_the_track", "sutton"}
CUTOFF = datetime.date(2014, 1, 1)   # the WordPress era is already on the live site

# Pre-2014 stories already on the live News page (title, date) - checked 23 Oct 2026
LIVE = [("Belgrave Open 7 miles", "2003-11-22"), ("VAC 10000m Walk inc. Belgrave Championships", "2004-04-28"),
        ("Alex Wright wins RWA 10 miles", "2010-03-06"), ("IAAF Race Walking Challenge", "2010-05-01"),
        ("European Veterans' Championships", "2011-05-15"), ("European Race Walking Cup", "2011-05-21"),
        ("Bronze for Alex in another tough '20'", "2011-05-30"), ("Silver medals in RWA Ten Miles Championship", "2012-03-04"),
        ("Wright Wins 5km at UKA Championships", "2012-06-24"), ("A new era as five Belles race at Addington", "2012-10-06"),
        ("Belles triumph at Enfield", "2012-11-10"), ("Claret & Gold shines at Bexley", "2012-12-01"),
        ("Cambridge Harriers Winter League", "2013-02-09"), ("Grazina stars in Enfield League 5 miles", "2013-02-23"),
        ("A clean sweep for the Belles in individual Winter League results", "2013-03-02"),
        ("It's a National silver for Lauren", "2013-03-10"), ("Grazina is English Champion", "2013-04-28"),
        ("Another medal for Mo", "2013-06-08"), ("VAC, Belgrave, Surrey, Middlesex and Herts 10,000m Championships", "2003-04-23"),
        ("Belgrave Harriers 83rd Open 7 Miles Walk", "2002-11-23"), ("Belgrave 82nd Open 7 Miles", "2001-11-24"),
        ("Veterans' AC, Belgrave, Surrey, Middlesex and Herts 10,000m Champs", "2001-04-25")]
LIVE = [(set(re.findall(r"[a-z]{4,}", t.lower())), datetime.date.fromisoformat(d)) for t, d in LIVE]


def already_live(headline, date, text=""):
    words = set(re.findall(r"[a-z]{4,}", (headline + " " + text[:400]).lower()))
    for w, d in LIVE:
        if abs((date - d).days) <= 4 and len(w & words) >= 2:
            return True
    return False


ACRONYMS = {"AAA", "SEAA", "ERRA", "ECCA", "UKA", "BAL", "UK", "RWA", "VAC", "BUCS", "AFD", "IAAF", "EAA", "NAL",
            "BMC", "SCAA", "CSSC", "AC", "HH", "UKWAL", "YAL", "NYAL", "NJAL", "BUSA", "GP", "BMAF", "EVAA", "XC",
            "CC", "TV", "BBC", "USA", "GB", "RAF", "II", "III", "IV", "SLAN", "MAA", "SAL", "UKWL", "EAP", "UCL", "LICC"}


def tidy_title(h):
    h = re.sub(r"^[\s\-–:,.|]+", "", h or "")
    h = re.sub(r"[\s,(]+[a-g]\s*=\s*\d{1,2}(st|nd|rd|th)?\b.*$", "", h)   # 'a=2, b=3' day labels and anything after
    h = re.sub(r":?\s*Date of release$", "", h, flags=re.I)
    return h.strip()


def no_shouting(h):
    """House style: no all-caps headlines. Only the case of all-caps words changes; acronyms stay."""
    letters = re.sub(r"[^A-Za-z]", "", h)
    if not letters or sum(c.isupper() for c in letters) / len(letters) < 0.7:
        return h
    def fix(m):
        w = m.group(0)
        core = re.sub(r"[^A-Za-z]", "", w)
        if core.upper() in ACRONYMS or len(core) <= 2:
            return w
        return w[0] + w[1:].lower() if w[0].isalpha() else w[:1] + w[1:].lower()
    return re.sub(r"[A-Za-z][A-Za-z'’&.]*", fix, h)


NAME_RE = re.compile(r"^(?:by\s+|words(?: by)?:?\s+)?([A-Z][a-z]+(?:[ -][A-Z][a-zA-Z'’-]+){1,2})\.?$")
WRITES_RE = re.compile(r"^\s*(?:<[^>]+>)*\s*([A-Z][a-z]+(?: [A-Z][a-zA-Z'’-]+){1,2}) writes\b", re.M)


def find_writer(body_html):
    """The story's own words naming its writer: 'Charlie Dickinson writes:' or a closing sign-off line."""
    m = WRITES_RE.search(re.sub(r"<p>", "\n", body_html))
    if m:
        return m.group(1)
    paras = [p for p in re.findall(r"<p>(.*?)</p>", body_html, re.S) if "<img" not in p]
    NOT_A_NAME = {"Result", "Results", "League", "Women", "Men", "Senior", "Junior", "Team", "Final", "Match",
                  "Race", "Relay", "Road", "Cross", "Country", "Track", "Field", "Club", "Stage", "Belgrave", "Harriers", "Action", "Trust", "Foundation", "Committee", "Association", "Group"}
    start = int(len(paras) * 0.5)
    for p in reversed(paras[start:]):
        t = text_of(p)
        if "<b>" in p or "<strong>" in p:
            continue
        mm = NAME_RE.match(t)
        if not mm or set(mm.group(1).replace("-", " ").split()) & NOT_A_NAME:
            continue
        i = paras.index(p)
        prev = text_of(paras[i - 1]) if i > 0 else ""
        if len(prev.split()) >= 8 and not re.search(r"\d", prev[-80:]):
            return NAME_MAP.get(mm.group(1), mm.group(1))
    return None


def first_saved(page):
    ts = ix[page]["first_saved"]
    return datetime.date(int(ts[:4]), int(ts[4:6]), int(ts[6:8]))


def subject_of(title):
    t = re.sub(r"\s+", " ", title or "").strip()
    t = re.sub(r"^(Belgrave Har+iers?\s*(on-line)?\s*[-–:]*\s*)", "", t, flags=re.I)
    return t.strip(" -–:")


posts, skipped = [], collections.Counter()
seen = {}


def add(p, page, kind):
    p["page"], p["kind"] = page, kind
    if p["date"] >= CUTOFF:
        skipped["2014 or later (already live)"] += 1
        return
    if already_live(p["title"], p["date"], text_of(p["body"])):
        skipped["already on the live site"] += 1
        return
    key = (p["date"], re.sub(r"[^a-z0-9]", "", p["title"].lower())[:40])
    if key in seen:
        old = seen[key]
        skipped["same story on two pages"] += 1
        if len(p["body"]) > len(old["body"]):
            posts[posts.index(old)] = p
            seen[key] = p
        return
    p["page"], p["kind"] = page, kind
    seen[key] = p
    posts.append(p)


for page in sorted(ix):
    if not page.startswith("belgraveharriers.com/"):
        continue
    parts = page.split("/")
    sec, fname = (parts[1] if len(parts) > 2 else "(top)"), parts[-1]
    if sec in SKIP_SECTIONS or sec == "(top)" or SKIP_FILES.match(fname) or sec == "Belgrave5k" and False:
        continue
    use_page(page)
    raw = load(ix[page])
    src = OLD + page.split("/", 1)[1]
    title, E = split_season_page(raw)
    dated = [e for e in E if e["date"]]
    is_feature = sec in FEATURE_SECTIONS or len(dated) <= 1

    if not is_feature:
        short = []
        for e in dated:
            h = tidy_title(no_shouting(tidy_headline(headline_from_heading(e["heading"]), title)))
            if re.fullmatch(r"(Date\s*:\s*)?(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day", h):
                own = re.sub(r"^Date\s*:\s*", "", e["heading"]).strip(" .")
                own = re.sub(r"\s+(19|20)\d\d$", "", own)
                h = f"{tidy_title(no_shouting(subject_of(title)))}: {own}"
            if e["words"] >= 150 and h:
                body = e["body"]
                writer = find_writer(body)
                add(dict(title=h, date=e["date"], body=body + "\n" + NOTE, cats=categories_for(page, h),
                         tags=tags_for(h, text_of(body)), source=src, writer=writer), page, "report")
            else:
                short.append(e)
        short = [e for e in short if e["date"] < CUTOFF]
        if short and "ix_" not in fname:
            rt = tidy_title(no_shouting(subject_of(title))) or f"Results {short[0]['date'].year}"
            body = "".join(f"<p><strong>{htmllib.escape(e['heading'])}</strong></p>\n{e['body']}" for e in short)
            add(dict(title=rt, date=max(e["date"] for e in short), body=body + "\n" + NOTE,
                     cats=categories_for(page, rt), tags=tags_for(" ".join(e["heading"] for e in short), text_of(body)),
                     source=src, writer=None), page, "round-up")
        continue

    f = extract_feature(raw)
    if f["words"] < 60:
        skipped["too little text to be a story"] += 1
        continue
    date = f["date"] or first_saved(page)
    if date.year < 2000 or (sec == "obituary" and date > first_saved(page)):
        date = first_saved(page)
    if f["heading"]:
        h = re.sub(r"\s*[-–:,]\s*$", "", headline_from_heading(f["heading"])).strip()
    else:
        h = ""
    if sec == "obituary" or not h or len(h) < 4:
        h = re.sub(r"^.*?Obituary\s*[-–]\s*", "", subject_of(f["page_title"])) or h
    if sec == "skippers_corner":
        h = re.sub(r"^Skipper'?s Corner\s*[-–:]?\s*", "", h, flags=re.I) or h
    h = tidy_title(no_shouting(tidy_headline(h)))
    if re.fullmatch(r"(Date\s*:\s*)?(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day", h or ""):
        h = tidy_title(no_shouting(subject_of(f["page_title"])))
    if not h:   # no title anywhere: use the article's own opening line if it is short
        first = next((t for b, t in f["blocks"] if t and len(t) < 90), "")
        h = tidy_title(no_shouting(first))
    kind = "feature"
    if sec in ("road_country", "track_field", "results", "race_walking", "veterans", "young_athletes", "triathlon") \
            and f["words"] > 2500 and subject_of(f["page_title"]):
        h, kind = tidy_title(no_shouting(subject_of(f["page_title"]))), "round-up"   # a whole results page
    byline = None
    m = re.match(r"^by\s+([A-Z][a-z]+ [A-Z][a-zA-Z'-]+)", h)
    if m:   # the only title is the author's credit: use the file's own name for the subject
        byline = m.group(1)
        h = fname.rsplit(".", 1)[0].replace("_", " ").title()
    blocks = f["blocks"]
    if blocks and h and re.sub(r"\W", "", blocks[0][1]).lower().endswith(re.sub(r"\W", "", h.split()[-1]).lower()) \
            and len(blocks[0][1]) < 120:
        blocks = blocks[1:]   # drop a repeated title line
    body = "\n".join(b for b, _ in blocks)
    cats = categories_for(page, h) or ["Club"]
    extra = ["Skipper's Corner"] if sec == "skippers_corner" else []
    if sec == "obituary":
        extra = [re.sub(r"\s*\d{4}\s*[-–]\s*\d{4}$", "", h)]
    add(dict(title=h, date=date, body=body + "\n" + NOTE, cats=cats,
             tags=tags_for(h, text_of(body), extra), source=src, writer=byline or find_writer(body)), page, kind)

posts.sort(key=lambda p: (p["date"], p["title"]))
json.dump([{**p, "date": p["date"].isoformat()} for p in posts], open("/home/claude/out/all_posts.json", "w"), ensure_ascii=False)
k = collections.Counter(p["kind"] for p in posts)
print("posts:", len(posts), dict(k))
print("skipped:", dict(skipped))
print("by year:", sorted(collections.Counter(p["date"].year for p in posts).items()))
print("with photos:", sum("<img" in p["body"] for p in posts), "| named writers:", sum(bool(p["writer"]) for p in posts))
