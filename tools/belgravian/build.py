"""Assemble the Belgravian archive data for the website.
python3 -I build.py WORKDIR REPO_BELGRAVIAN_DIR
Reads WORKDIR/out/B*.json, WORKDIR/crops, WORKDIR/pages, WORKDIR/people-index.json (optional, built by people.py)
and writes: issues/B*.json, index.json, search.json, people.json under the repo folder.
Images (WORKDIR/pages, WORKDIR/crops) go to the R2 bucket belgravian-archive under belgravian/: python3 -I r2up.py r2.env WORKDIR belgravian/ pages crops"""
import json, os, sys, glob, shutil, re, unicodedata

W, OUT = sys.argv[1], sys.argv[2]
man = json.load(open('/home/claude/stephengardner1/surrey-league/research/belgravian/manifest_raw.json'))
urls = {x['no']: x['url'].split('?')[0] for x in man if not x['eharrier']}
os.makedirs(f'{OUT}/issues', exist_ok=True)

def slug(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

# Event tags group the same race across years (Steve, 29 Oct 2026): drop the year/season from each tag.
YEAR = re.compile(r'(?<![\w.])(?:18[5-9]\d|19\d\d|20[0-2]\d)(?:\s*[-/\u2013]\s*\d{2,4})?(?![\w.])(?!\s*(?:m|metres?|meters?|yards?|yds|miles?|km|kilo\w*)\b)')
# Competitions that are one and the same, shown under one name (Steve's decisions). Keys are compared loosely:
# lower case, hyphens as spaces, "Championship" = "Championships".
EVENT_SAME = {'southern counties cross country championships': 'Southern Cross Country Championships',   # Steve, 2 Nov 2026
              'southern cross country championships': 'Southern Cross Country Championships'}
def ev_key(t):
    t = re.sub(r'\s+', ' ', t.lower().replace('-', ' ')).strip()
    return re.sub(r'\bchampionship\b', 'championships', t)
# Steve, 2 Nov 2026: the junior, youths, women's and veterans Southern championships (with or without "Counties")
# all fold into the one Southern Cross Country Championships. Leagues, inter-counties and association races stay apart.
SOUTHERN_XC = re.compile(r"^(veterans )?southern (counties )?((junior|juniors|youths?|women'?s|ladies|veterans|vets) )?"
                         r"(cross country|c\.?c\.?) championships( \(.*\))?$")
def event_tag(e):
    t = event_tag0(e)
    k = ev_key(t)
    if SOUTHERN_XC.match(k): return 'Southern Cross Country Championships'
    # Steve, 2 Nov 2026: "British League" and "BAL" are the British Athletics League (divisions and qualifying matches
    # included); its cup competitions keep their own names, with BAL / British League spelled out
    kb = re.sub(r'^(b\.?a\.?l\.?|british league)\b', 'british athletics league', k)
    if re.match(r'^british athletics league( (div(ision)?\.? ?\w+|premiership|qualifying match|match \w+))?$', kb):
        return 'British Athletics League'
    if kb != k and re.match(r'^british athletics league (gold )?cup$', kb):
        return 'British Athletics League ' + ('Gold Cup' if 'gold' in kb else 'Cup')
    return EVENT_SAME.get(k, t)
def event_tag0(e):
    t = YEAR.sub('', e)
    t = re.sub(r'\(\s*\)', '', t)                      # empty brackets left behind
    t = re.sub(r'\s+([,)])', r'\1', t); t = re.sub(r'\(\s+', '(', t)
    t = re.sub(r'\s{2,}', ' ', t).strip(' ,-\u2013')
    return t or e
# Publish only finished issues: the 1960s pilot, plus later issues listed in WORKDIR/published.txt once read AND checked.
PUB = set((int(x) if x.isdigit() else x) for x in open(f'{W}/published.txt').read().split()) if os.path.exists(f'{W}/published.txt') else set()
def published(no):
    return (isinstance(no, int) and no <= 172) or no in PUB

issues, search = [], []
for f in sorted(glob.glob(f'{W}/out/B*.json')):
    if re.search(r'\.(orig|firstpass)\.json$', f): continue
    d = json.load(open(f))
    no = d['issue']
    if not published(no): continue
    d['pdfUrl'] = d.get('pdfUrl') or urls.get(no)
    for it in d['items']:
        it.setdefault('regions', [])
        for k in ('tables', 'scans', 'photos', 'people', 'events', 'clubs', 'places', 'sport'):
            it[k] = it.get(k) or []
        it['events'] = list(dict.fromkeys(event_tag(e) for e in it['events']))
    json.dump(d, open(f'{OUT}/issues/B{no}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    y = int(str(d['date'])[:4])
    issues.append({'issue': no, 'label': d['label'], 'date': d['date'], 'year': y,
                   'pageCount': d['pageCount'], 'items': len(d['items'])})
    for it in d['items']:
        ppl = []
        for p in it['people']:
            ppl += [p.get('name') or '', p.get('printed') or '', p.get('note') or ''] + (p.get('printedAs') or [])
        cells = ' '.join(' '.join(map(str, r)) for t in it['tables'] for r in t.get('rows', []))
        caps = ' '.join((ph.get('caption') or '') for ph in it['photos'] + it['scans'])
        hay = ' '.join([it.get('heading') or '', it.get('summary') or '', it.get('text') or '', cells, caps,
                        ' '.join(ppl), ' '.join(it['events'] + it['places'] + it['clubs'])])
        p0 = min(it['pages']) if it.get('pages') else 1
        search.append({'decade': str(y)[:3] + '0s', 'id': it['id'], 'type': it['type'], 'label': d['label'], 'p': p0,
                       'h': it.get('heading'), 'sum': it.get('summary'),
                       's': re.sub(r'\s+', ' ', hay).strip()})
    # page images and crops are not copied: they live on Cloudflare R2 (upload with r2up.py from WORKDIR)

issues.sort(key=lambda x: x['date'])
idx = {'title': 'The Belgravian', 'issues': issues,
       # decades with nothing published yet; a decade only partly done (e.g. the 1980s) shows "(more to come)"
       'coming': [d + (' (more to come)' if d in {str(x['year'])[:3] + '0s' for x in issues} else '')
                  for d in ['1920s', '1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s', '2000s']
                  if d not in {str(x['year'])[:3] + '0s' for x in issues} or d in ('2000s',)],
       'legends': json.load(open(f'{W}/legends-index.json')) if os.path.exists(f'{W}/legends-index.json') else []}

json.dump(idx, open(f'{OUT}/index.json', 'w'), ensure_ascii=False, indent=1)
# one search file per decade, so a reader only downloads what exists (index.json lists them)
by_dec = {}
for x in search: by_dec.setdefault(x.pop('decade'), []).append(x)
idx['searchFiles'] = [f'search-{d}.json' for d in sorted(by_dec)]
json.dump(idx, open(f'{OUT}/index.json', 'w'), ensure_ascii=False, indent=1)
for d, xs in by_dec.items():
    json.dump({'items': xs}, open(f'{OUT}/search-{d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))

# people: light list (people.json) + per-surname-letter shards (people/<letter>.json) + legend profiles
import string
pi = json.load(open(f'{W}/people-index.json'))['people']
legends = idx['legends']
leg_ids = {l['id'] for l in legends}
os.makedirs(f'{OUT}/people', exist_ok=True); os.makedirs(f'{OUT}/legends', exist_ok=True)
shards = {}
light = []
# photos per item, so each person's page can open with the photos they are named in (captions only, as printed)
item_photos = {}
for f in sorted(glob.glob(f'{OUT}/issues/B*.json')):
    d = json.load(open(f))
    for it in d['items']:
        for ph in it.get('photos') or []:
            if ph.get('review') or not ph.get('people'): continue
            item_photos.setdefault(it['id'], []).append(
                {'f': f"crops/B{d['issue']}/{ph['file']}", 'c': ph.get('caption') or '', 'id': it['id'],
                 'w': d.get('label') or '', 'who': set(ph['people'])})
for p in pi:
    names = set(p.get('aka') or []) | {p['name']}
    seen, gal = set(), []
    for m in p['mentions'] + p.get('official', []) + p.get('wrote', []):
        for ph in item_photos.get(m['id'], []):
            if ph['f'] in seen or not (ph['who'] & names): continue
            seen.add(ph['f']); gal.append({k: v for k, v in ph.items() if k != 'who'})
    if gal: p['photos'] = gal
# athlete profiles: for each mention, the passage that names the person, so their page reads as a run of articles
# (people/x/<id>.json, only for people with 3+ mentions; loaded only on that person's page)
item_src = {}
for f in sorted(glob.glob(f'{OUT}/issues/B*.json')):
    d = json.load(open(f))
    for it in d['items']:
        item_src[it['id']] = it
os.makedirs(f'{OUT}/people/x', exist_ok=True)
for old in glob.glob(f'{OUT}/people/x/*.json'): os.remove(old)
SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z"\'(])|\n+')
def passage(it, forms, surname):
    """the sentence(s), table row or caption that names the person, trimmed to ~320 characters"""
    pats = [re.compile(r'(?<![A-Za-z])' + re.escape(f) + r'(?![a-z])') for f in forms] + \
           [re.compile(r'(?<![A-Za-z])' + re.escape(surname) + r'(?![a-z])', re.I)]
    text = it.get('text') or ''
    if it.get('heading'):  # skip the printed heading at the top of the text
        text = re.sub(r'^\s*' + re.escape(it['heading'].strip()) + r'\s*\n?', '', text)
    for pat in pats:
        m = pat.search(text)
        if m:
            parts = [s for s in SENT.split(text) if s.strip()]
            pos = 0
            for i, s in enumerate(parts):
                j = text.find(s, pos); pos = j + len(s)
                if j <= m.start() < pos:
                    out = s.strip()
                    if len(out) < 140 and i + 1 < len(parts) and len(parts[i + 1].strip()) > 40: out += ' ' + parts[i + 1].strip()
                    if len(out) < 140 and i > 0 and len(parts[i - 1].strip()) > 40: out = parts[i - 1].strip() + ' ' + out
                    out = re.sub(r'\s+', ' ', out)
                    if len(out) > 320:
                        k = max(0, out.find(m.group(0)) - 120); out = ('…' if k else '') + out[k:k + 300].rstrip() + '…'
                    return out
        for t in it.get('tables') or []:
            for r in (t.get('rows') or [])[1:]:
                row = ' · '.join(str(c) for c in r if str(c).strip())
                if pat.search(row): return row
        for ph in (it.get('photos') or []) + (it.get('scans') or []):
            if ph.get('caption') and pat.search(ph['caption']): return ph['caption']
    return ''
# a profile passage is a short excerpt: leave home addresses and phone numbers out of it, even from pre-1976 issues
# printed with them (the issue itself still shows them as printed)
_priv = f'{W}/priv/redactions.json'
PRIV = sorted({r['find'] for r in json.load(open(_priv)) if len(r['find']) > 5} |
              {r['find'].replace('\n', ' ') for r in json.load(open(_priv)) if len(r['find']) > 5}, key=len, reverse=True) if os.path.exists(_priv) else []
PHONE = re.compile(r'\(?\b0\d{1,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}\b|\b\d{3}[\s-]\d{4}\b')
def scrub(s):
    for a in PRIV:
        if a in s: s = s.replace(a, '…')
    return PHONE.sub('…', s) if re.search(r'(?i)\b(tel|telephone|phone|ring)\b', s) else s
nprof = 0
for p in pi:
    if len(p['mentions']) < 3: continue
    surname = re.sub(r'[^A-Za-z\'-]', '', p['name'].split()[-1]) or p['name']
    forms = sorted({a for a in (p.get('aka') or []) + [p['name']] if surname.lower() in a.lower() and len(a) > len(surname) + 1},
                   key=len, reverse=True)
    x = [scrub(passage(item_src.get(m['id'], {}), forms, surname)) for m in p['mentions']]
    if any(x):
        json.dump({'x': x}, open(f"{OUT}/people/x/{p['id']}.json", 'w'), ensure_ascii=False, separators=(',', ':'))
        p['x'] = 1; nprof += 1
print(nprof, 'profiles with passages')
for p in pi:
    letter = (p['sort'][:1] if p['sort'][:1] in string.ascii_lowercase else '_')
    for m in p['mentions']:
        for k in ('sum', 'label'): m.pop(k, None)
        if not m.get('note'): m.pop('note', None)
        if not m.get('h'): m.pop('h', None)
    p['legend'] = p['id'] in leg_ids
    shards.setdefault(letter, []).append(p)
    row = {'id': p['id'], 'name': p['name'], 'n': len(p['mentions']), 's': letter}
    # items where they appear only as author / photographer / official (not counted in n)
    o = {k: len(p[k]) for k in ('wrote', 'credits', 'official') if p.get(k)}
    if o: row['o'] = o
    if p['legend']: row['legend'] = True
    light.append(row)
for letter, ps in shards.items():
    json.dump({p['id']: p for p in ps}, open(f'{OUT}/people/{letter}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
# one small file per person, so a profile page loads only that person (people/p/<id>.json)
os.makedirs(f'{OUT}/people/p', exist_ok=True)
keep = set()
for ps in shards.values():
    for p in ps:
        fn = f"{OUT}/people/p/{p['id']}.json"; keep.add(fn)
        s_ = json.dumps(p, ensure_ascii=False, separators=(',', ':'))
        if not os.path.exists(fn) or open(fn).read() != s_: open(fn, 'w').write(s_)
for old in glob.glob(f'{OUT}/people/p/*.json'):
    if old not in keep: os.remove(old)
json.dump({'people': light}, open(f'{OUT}/people.json', 'w'), ensure_ascii=False, separators=(',', ':'))
for l in legends:
    src = f"{W}/../legend/{l['id'][2:]}.json"
    if os.path.exists(src): shutil.copy(src, f"{OUT}/legends/{l['id'][2:]}.json")
print(len(issues), 'issues;', len(search), 'items;', {d: os.path.getsize(f'{OUT}/search-{d}.json') // 1024 for d in by_dec}, 'KB')
