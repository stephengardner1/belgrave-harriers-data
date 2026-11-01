"""Build plain, search-engine-readable pages for The Belgravian archive.

  python3 tools/belgravian/build_pages.py [--index]

Reads belgravian/issues/*.json, belgravian/people.json and belgravian/people/*.json (already privacy-cleaned) and writes
belgravian/read/: index.html, one page per issue (issues/B171.html), one per named person (people/<slug>.html) and
sitemap.xml. Every page links into the full reader on the club site at the matching item.

Pages carry <meta name="robots" content="noindex"> unless --index is given. Switch it on only once the pages live at
their own address (archive.belgraveharriers.com) and belgravian@belgraveharriers.com forwards to someone, because every
person page tells readers to email that address to correct or remove an entry.
"""
import json, os, re, sys, glob, html, shutil

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'belgravian')
OUT = os.path.join(ROOT, 'read')
SITE = 'https://archive.belgraveharriers.com/'          # where these pages will live
READER = 'https://www.belgraveharriers.com/belgravian#'  # the full reader on the club site
CONTACT = 'belgravian@belgraveharriers.com'
INDEX = '--index' in sys.argv

TYPE = {'cover': 'Cover', 'masthead': 'Masthead', 'editorial': 'Editorial', 'report': 'Report', 'results': 'Results',
        'notice': 'Notice', 'letter': 'Letter', 'obituary': 'Obituary', 'members': 'New members', 'feature': 'Feature',
        'column': 'Column', 'records': 'Records', 'photo': 'Photograph', 'advert': 'Advertisement', 'poem': 'Poem',
        'cartoon': 'Cartoon', 'other': 'Item'}
e = lambda s: html.escape(str(s or ''), quote=True)

def slug(s):
    import unicodedata
    s = unicodedata.normalize('NFD', str(s)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

CSS = """@font-face{font-family:"Castoro Belgrave";src:url(../../fonts/CastoroBelgrave-Semibold.woff2) format("woff2");font-weight:600;font-display:swap}
:root{--ink:#1e1a1a;--body:#4a4343;--slate:#5c5555;--claret:#7a001d;--gold:#d6b97a;--gold-ink:#7a5e1c;--rule:#e6dfd3;--cream:#f5efe4}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font:400 17px/28px "Public Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:760px;margin:0 auto;padding:24px 16px 64px}a{color:var(--claret)}
.top{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font:500 14px/20px "Public Sans",sans-serif;border-bottom:3px double var(--gold);padding-bottom:12px;margin-bottom:24px}
.top a{color:var(--slate);text-decoration:none}.top a:hover{color:var(--claret)}
.label{font:600 12px/16px "Public Sans",sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink)}
h1{font:600 36px/42px "Castoro Belgrave",Castoro,Georgia,serif;margin:6px 0 8px}h2{font:600 24px/30px "Castoro Belgrave",Castoro,Georgia,serif;margin:6px 0}
h3{font:600 20px/26px "Libre Franklin",sans-serif;margin:28px 0 8px}
.meta,.by,.sum{color:var(--slate);font-size:15px;line-height:22px;margin:0 0 8px}
article{border-top:1px solid var(--rule);padding:22px 0}article p{margin:0 0 12px;white-space:pre-line;color:var(--body)}
.read{display:inline-block;margin-top:6px;font:500 15px/20px "Public Sans",sans-serif}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}.chips a,.chips span{font-size:13px;line-height:18px;background:var(--cream);border-radius:99px;padding:3px 10px;color:var(--ink);text-decoration:none}
table{border-collapse:collapse;width:100%;font-size:15px;line-height:20px;margin:8px 0 14px;font-variant-numeric:tabular-nums}
th{text-align:left;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--slate);border-bottom:3px solid var(--gold);padding:0 8px 6px 0}
td{border-bottom:1px solid var(--rule);padding:6px 8px 6px 0;vertical-align:top}.tw{overflow-x:auto}
figure{margin:10px 0}figure img{max-width:100%;height:auto;border:1px solid var(--rule)}figcaption{font-size:14px;color:var(--slate)}
ul.list{list-style:none;padding:0;margin:0}ul.list li{border-bottom:1px solid var(--rule);padding:10px 0}
.note{margin-top:40px;padding:14px 16px;background:var(--cream);border-radius:8px;font-size:15px;line-height:22px;color:var(--body)}
.az{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 18px}.az a{font-weight:600;text-decoration:none;padding:2px 8px;border:1px solid var(--rule);border-radius:6px}"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600&family=Libre+Franklin:wght@600&display=swap">'

def page(path, title, desc, body, canonical):
    robots = '' if INDEX else '<meta name="robots" content="noindex">'
    doc = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{e(title)}</title><meta name="description" content="{e(desc)}">{robots}'
           f'<link rel="canonical" href="{e(SITE + canonical)}">{FONTS}<link rel="stylesheet" href="' + ('../' if '/' in canonical else '') + 'style.css"></head><body><div class="wrap">'
           '<nav class="top"><a href="' + ('../' if '/' in canonical else '') + 'index.html">The Belgravian archive</a>'
           '<a href="https://www.belgraveharriers.com/belgravian">Read with the original pages →</a></nav>'
           + body +
           '<p class="note">The Belgravian was Belgrave Harriers’ club gazette (1925–2009). Scans by Alan Mead, club historian '
           '(<a href="https://www.belgraveharriers.info/thebelgravian">belgraveharriers.info</a>). Text transcribed exactly as printed; '
           'from 1976 onwards private addresses and phone numbers are withheld. Spotted a mistake, or want an entry removed? '
           f'Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p></div></body></html>')
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(doc)

def paras(text):
    return ''.join(f'<p>{e(p.strip())}</p>' for p in re.split(r'\n\s*\n', text or '') if p.strip())

def table(t):
    rows = t.get('rows') or []
    if not rows: return ''
    h = '<div class="tw"><table>' + (f'<caption>{e(t.get("caption"))}</caption>' if t.get('caption') else '')
    h += '<thead><tr>' + ''.join(f'<th>{e(c)}</th>' for c in rows[0]) + '</tr></thead><tbody>'
    h += ''.join('<tr>' + ''.join(f'<td>{e(c)}</td>' for c in r) + '</tr>' for r in rows[1:])
    return h + '</tbody></table></div>'

# ---- people (only real names: skip bare initials like "G. North", which can't be pinned to one person) ----
people = json.load(open(os.path.join(ROOT, 'people.json')))['people']
detail = {}
for f in glob.glob(os.path.join(ROOT, 'people', '*.json')):
    detail.update(json.load(open(f)))
def real_name(n):
    first = n.split()[0] if n.split() else ''
    # a first name, not initials ("G.", "G.A.", "GA")
    return bool(re.match(r"^[A-Z][a-z][A-Za-z'\-]*$", first.strip(',')))
PAGE = {}
for p in people:
    if p['id'] in detail and real_name(p['name']):
        PAGE[p['id']] = 'people/' + slug(p['id'][2:]) + '.html'
def person_link(name, prefix):
    pid = 'p-' + slug(name)
    return f'<a href="{prefix}{PAGE[pid]}">{e(name)}</a>' if pid in PAGE else f'<span>{e(name)}</span>'

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT); open(os.path.join(OUT, 'style.css'), 'w').write(CSS)
urls = []

# ---- issues ----
issues = []
for f in sorted(glob.glob(os.path.join(ROOT, 'issues', 'B*.json'))):
    d = json.load(open(f)); no = d['issue']; issues.append(d)
    body = f'<span class="label">No. {no}</span><h1>The Belgravian, {e(d["label"])}</h1>'
    body += f'<p class="meta">{len(d["items"])} items · {d["pageCount"]} pages · <a href="{READER}B{no}">Read beside the original pages</a></p>'
    for it in d['items']:
        body += f'<article id="{e(it["id"])}"><span class="label">{e(TYPE.get(it.get("type"), "Item"))} · page {min(it.get("pages") or [1])}</span>'
        if it.get('heading'): body += f'<h2>{e(it["heading"])}</h2>'
        if it.get('byline'): body += f'<p class="by">{e(it["byline"])}</p>'
        if it.get('summary') and not it.get('text'): body += f'<p class="sum">{e(it["summary"])}</p>'
        body += paras(it.get('text'))
        for t in it.get('tables') or []: body += table(t)
        for ph in [x for x in (it.get('photos') or []) if not x.get('review')]:
            if ph.get('caption'): body += f'<figure><figcaption>Photograph: {e(ph["caption"])}{(" (" + e(ph["credit"]) + ")") if ph.get("credit") else ""}</figcaption></figure>'
        names = []
        for pp in it.get('people') or []:
            n = pp.get('name') or pp.get('printed')
            if n and n not in names: names.append(n)
        if names: body += '<div class="chips">' + ''.join(person_link(n, '../') for n in names) + '</div>'
        body += f'<a class="read" href="{READER}{e(it["id"])}">See it on the printed page →</a></article>'
    title = f'The Belgravian, {d["label"]} (No. {no}) · Belgrave Harriers'
    desc = f'Belgrave Harriers club gazette, {d["label"]}: ' + '; '.join(x.get('heading') for x in d['items'] if x.get('heading'))[:150]
    page(f'issues/B{no}.html', title, desc, body, f'issues/B{no}.html'); urls.append(f'issues/B{no}.html')

when = {d['issue']: d['label'] for d in issues}
# ---- people pages ----
for p in people:
    if p['id'] not in PAGE: continue
    x = detail[p['id']]
    body = f'<span class="label">In The Belgravian</span><h1>{e(x["name"])}</h1>'
    aka = [a for a in (x.get('aka') or []) if a != x['name']]
    if aka: body += f'<p class="meta">Also printed as {e(", ".join(aka[:12]))}</p>'
    body += f'<p class="meta">{len(x["mentions"])} mention{"s" if len(x["mentions"]) != 1 else ""}</p><ul class="list">'
    for m in x['mentions']:
        no = m['id'].split('-')[0][1:]; no = int(no) if no.isdigit() else no
        body += (f'<li><a href="../issues/B{no}.html#{e(m["id"])}">{e(m.get("when") or when.get(no, ""))}, page {e(m.get("p"))}</a>'
                 + (f' — {e(m["note"])}' if m.get('note') else '') + f' · <a href="{READER}{e(m["id"])}">printed page</a></li>')
    body += '</ul>'
    page(PAGE[p['id']], f'{x["name"]} in The Belgravian · Belgrave Harriers archive',
         f'Every mention of {x["name"]} in The Belgravian, the Belgrave Harriers club gazette.', body, PAGE[p['id']])
    urls.append(PAGE[p['id']])

# ---- index ----
by = {}
for d in issues: by.setdefault(str(d['date'])[:3] + '0s', []).append(d)
body = '<span class="label">Belgrave Harriers · Founded 1887</span><h1>The Belgravian archive</h1>'
body += f'<p>The club’s gazette, transcribed issue by issue. {len(issues)} issues so far; more decades are being added. '
body += f'Read them beside the original printed pages on <a href="https://www.belgraveharriers.com/belgravian">belgraveharriers.com</a>.</p>'
for dec in sorted(by):
    body += f'<h3>{dec}</h3><ul class="list">' + ''.join(
        f'<li><a href="issues/B{d["issue"]}.html">{e(d["label"])}</a> · No. {d["issue"]} · {len(d["items"])} items</li>'
        for d in sorted(by[dec], key=lambda d: d['date'])) + '</ul>'
named = sorted([p for p in people if p['id'] in PAGE], key=lambda p: detail[p['id']].get('sort') or p['name'].lower())
letters = sorted({(p.get('s') or p['name'][-1:]).upper()[:1] for p in named if (p.get('s') or '').isalpha()})
body += '<h3>People</h3><div class="az">' + ''.join(f'<a href="people/index-{l.lower()}.html">{l}</a>' for l in letters) + '</div>'
page('index.html', 'The Belgravian archive · Belgrave Harriers', 'Every issue of The Belgravian, the Belgrave Harriers club gazette, transcribed and searchable.', body, 'index.html')
urls.append('index.html')
for l in letters:
    group = [p for p in named if (p.get('s') or '').upper() == l]
    body = f'<span class="label">People · {l}</span><h1>Names in The Belgravian: {l}</h1><ul class="list">' + ''.join(
        f'<li><a href="{PAGE[p["id"]].split("/",1)[1]}">{e(p["name"])}</a> · {p.get("n", "")}</li>' for p in group) + '</ul>'
    page(f'people/index-{l.lower()}.html', f'Names in The Belgravian: {l} · Belgrave Harriers', f'People named in The Belgravian, surnames {l}.', body, f'people/index-{l.lower()}.html')
    urls.append(f'people/index-{l.lower()}.html')

open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'<url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(('User-agent: *\nAllow: /\n' if INDEX else 'User-agent: *\nDisallow: /\n') + f'Sitemap: {SITE}sitemap.xml\n')
print(len(issues), 'issue pages,', len(PAGE), 'person pages,', len(letters), 'A-Z pages; indexing', 'ON' if INDEX else 'OFF (noindex)')
