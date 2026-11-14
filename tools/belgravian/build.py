"""Assemble the Belgravian archive data for the website.
python3 -I build.py WORKDIR REPO_BELGRAVIAN_DIR
Reads WORKDIR/out/B*.json, WORKDIR/crops, WORKDIR/pages, WORKDIR/people-index.json (optional, built by people.py)
and writes: issues/B*.json, index.json, search.json, people.json under the repo folder.
Images (WORKDIR/pages, WORKDIR/crops) go to the R2 bucket belgravian-archive under belgravian/: python3 -I r2up.py r2.env WORKDIR belgravian/ pages crops"""
import collections, json, os, sys, glob, shutil, re, unicodedata

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
# Steve, 7 Nov 2026: three London to Brighton races, each with its variants merged -- the road relay (National and
# Southern), the walk, and the 52-mile run. A plain "London to Brighton" tag is sorted by what the item says nearby.
BR_RELAY = re.compile(r"^(national |southern )?(london (to )?)?brighton (road )?relays?( \((national|southern|southern clubs)\))?$")
BR_WALK = re.compile(r"^(london (to )?)?brighton walk$")
BR_RUN = re.compile(r"^(r\.?r\.?c\.? )?london (to )?brighton ((road )?(run|race|running race)|52 miles)$")
def brighton_kind(it):
    h = (it.get('heading') or '').lower()
    for w, kind in (('relay', 'Relay'), ('walk', 'Walk'), ('run', 'Run')):
        if w in h and 'brighton' in h: return kind
    txt = ' '.join(str(it.get(x) or '') for x in ('heading', 'summary', 'text')).lower()
    sc = {'Relay': 0, 'Walk': 0, 'Run': 0}
    for m in re.finditer(r'brighton', txt):
        win = txt[max(0, m.start() - 120): m.end() + 120]
        sc['Relay'] += len(re.findall(r'relay|stage|\bleg\b', win))
        sc['Walk'] += len(re.findall(r'walk', win))
        sc['Run'] += len(re.findall(r'\brun\b|running race|road run|52 miles|runners? club|r\.r\.c', win))
    best = max(sc, key=sc.get)
    if sc[best] and list(sc.values()).count(sc[best]) == 1: return best
    for w, kind in (('relay', 'Relay'), ('walk', 'Walk'), ('road run', 'Run'), ('running', 'Run')):   # the column it sits in
        if w in h: return kind
    sc = {'Relay': len(re.findall(r'relay', txt)), 'Walk': len(re.findall(r'walk', txt)),
          'Run': len(re.findall(r'\brun\b|running race|road run', txt))}
    best = max(sc, key=sc.get)
    return best if sc[best] and list(sc.values()).count(sc[best]) == 1 else None
# Steve, 8 Nov 2026: the Surrey cross-country league under one name, whatever the page printed ("Surrey CC League",
# "Surrey Cross Country League", "Sweatshop Men's Surrey CC League", divisions, venues, youths and boys). The North
# Surrey League, the women's league and the young athletes' league stay separate; road, summer and winter leagues too.
SURREY_ALIASES = {'Surrey League': ['surrey league', 'surrey cross country league', 'surrey cross-country league',
                                    'surrey cc league', 'surrey c.c. league', 'surrey c. c. league', 'surrey xc league'],
                  "Surrey Women's Cross Country League": ["women's surrey league", "surrey women's league",
                                    "surrey women's cross country league", "women's surrey cc league",
                                    "surrey ladies cross country league"],
                  'North Surrey League': ['north surrey league']}
def surrey_tag(k):
    k = k.replace('\u2019', "'")
    if 'surrey' not in k or 'league' not in k or k.startswith('belgrave'): return None
    if re.search(r'road|summer|winter|championships|east surrey|mid surrey', k): return None
    if 'north surrey league' in k: return 'North Surrey League'
    m = re.match(r"^(sweatshop )?(men'?s |women'?s |ladies )?surrey (men'?s |women'?s'? |womens'? |ladies |youths?(/boys)? |junior |young athletes )?"
                 r"(cross country |c\.?c\.? |x\.?c\.? )?league\b(.*)$", k)
    if not m: return None
    who = (m.group(2) or '') + (m.group(3) or '') + (m.group(6) or '')
    if re.search(r"wom[ae]n|ladies", who): return "Surrey Women's Cross Country League"
    if re.search(r'young athletes|junior cross', who + ' ' + k): return 'Surrey Young Athletes Cross Country League'
    return 'Surrey League'
# Steve, 8 Nov 2026: the Southern championships under their later names (SEAA, South of England) fold into the
# Southern Cross Country Championships; the inter-counties are split by discipline (sorted like London to Brighton).
SOUTHERN_MORE = re.compile(r"^((seaa|s\.e\.a\.a\.?|south of england)( aa)? (senior )?(cross country|c\.?c\.?) championships|"
                           r"southern counties (senior )?c\.? ?c\.?( ?championships)?|southern c\.?c\.?a\.?( race.*)?)$")
def ic_kind(it):
    h = (it.get('heading') or '').lower()
    if re.search(r'cross[- ]country|\bc\.? ?c\.?\b|x-?c\b', h): return 'xc'
    if re.search(r'\bwalk(s|ing)?\b', h): return 'walk'
    if re.search(r'track|field|athletic', h): return 'tf'
    txt = ' '.join(str(it.get(x) or '') for x in ('summary', 'text')).lower()
    sc = {'xc': 0, 'walk': 0, 'tf': 0}
    for m in re.finditer(r'inter[- ]?count', txt):
        win = txt[max(0, m.start() - 150): m.end() + 150]
        sc['xc'] += len(re.findall(r'cross[- ]country|\bc\.c\.|\bmud|\bcourse\b|parliament hill|\bcountry\b', win))
        sc['walk'] += len(re.findall(r'\bwalk(s|ing|ed)?\b', win))
        sc['tf'] += len(re.findall(r'\btrack\b|metres|\d+ ?m\b|yards|hurdles|steeplechase|jump|vault|shot|discus|javelin|hammer|sprint|relay', win))
    best = max(sc, key=sc.get)
    if best == 'walk' and sc['tf']: best = 'tf'   # the track championships had walks too
    if sc[best] and list(sc.values()).count(sc[best]) == 1: return best
    sp = set(it.get('sport') or [])
    if sp == {'cross country'}: return 'xc'
    if sp == {'race walking'}: return 'walk'
    if sp and sp <= {'track', 'field'}: return 'tf'
    return None
IC_NAMES = {'xc': 'Inter-Counties Cross Country Championships', 'walk': 'Inter-Counties Walks',
            'tf': 'Inter-Counties Track & Field'}
def ic_tag(k, it):
    if not re.search(r'inter[- ]?count(y|ies)', k): return None
    if re.search(r'\bmatch\b|\bmeet\b|meeting|vets|veteran|eastern|battle of britain|national and|aaa|\b10 ?k', k): return None
    if re.match(r'^(seaa|se |south of england|southern)', k): return 'Southern Inter-Counties'
    if 'school' in k: return 'Schools Inter-Counties'
    if re.search(r'\bu\d\d|under|youth|young|\bya\b', k): return None
    if '20 mile' in k: return 'Inter-Counties 20 Miles'
    if 'walk' in k: return 'Inter-Counties Walks'
    if re.search(r'cross country|\bc\.?c\.?\b|^junior inter', k): return IC_NAMES['xc']
    if re.match(r"^(cau )?inter[- ]?count(y|ies)( (championships?|champs\.?|race|track))?$", k):  # CAU ran both
        kind = ic_kind(it) if it is not None else None
        if 'track' in k and kind != 'walk': kind = 'tf'
        return IC_NAMES[kind] if kind else 'Inter-Counties'
    return None
# Steve, 8 Nov 2026: the Southern track and field championships (Southern Counties AAA, later SEAA / South of England AA)
# under one name, the partner of the Southern Cross Country Championships; the few plain "Southern Championships"
# that are really cross-country are sorted by the heading and the words nearby.
SOUTHERN_TF = re.compile(r"^(southern( counties)?( a\.?a\.?a\.?| aaa)?|s\.?c\.?a\.?a\.?a\.?|seaa|s\.e\.a\.a\.?|south of england( a\.?a\.?)?)"
                         r" (senior )?(championships?|champs\.?)$")
def southern_kind(it):
    h = (it.get('heading') or '').lower()
    if re.search(r'cross[- ]country|\bc\.? ?c\.?\b|x-?c\b', h): return 'xc'
    if re.search(r'track|field|athletic', h): return 'tf'
    sp = set(it.get('sport') or [])
    if 'cross country' not in sp and sp & {'track', 'field', 'race walking'}: return 'tf'
    if sp == {'cross country'}: return 'xc'
    txt = ' '.join(str(it.get(x) or '') for x in ('summary', 'text')).lower()
    xc = tf = 0
    for m in re.finditer(r'southern|s\.?e\.?a\.?a|south of england|s\.c\.a\.a', txt):
        win = txt[max(0, m.start() - 120): m.end() + 120]
        xc += len(re.findall(r'cross[- ]country|\bc\.c\.|\bmud|\bcourse\b|parliament hill|\bcountry\b', win))
        tf += len(re.findall(r'\btrack\b|metres|\d+ ?m\b|yards|hurdles|steeplechase|jump|vault|shot|discus|javelin|hammer|sprint|relay', win))
    if xc > tf: return 'xc'
    if tf > xc: return 'tf'
    sp = set(it.get('sport') or [])
    return 'xc' if sp == {'cross country'} else 'tf'
def event_tag(e, it=None):
    t = event_tag0(e)
    k = ev_key(t)
    if BR_RELAY.match(k): return 'London to Brighton Relay'
    if BR_WALK.match(k): return 'London to Brighton Walk'
    if BR_RUN.match(k): return 'London to Brighton Run'
    if re.match(r"^stock exchange (london (to )?)?brighton( walk)?$", k): return 'Stock Exchange London to Brighton Walk'
    if re.match(r"^london (to )?brighton and back( walk)?$", k): return 'London to Brighton and Back Walk'
    if k in ('london to brighton', 'london brighton') and it is not None:
        kind = brighton_kind(it)
        if kind: return 'London to Brighton ' + kind
    st = surrey_tag(k)
    if st: return st
    if SOUTHERN_XC.match(k) or SOUTHERN_MORE.match(k): return 'Southern Cross Country Championships'
    if SOUTHERN_TF.match(k):
        return 'Southern Cross Country Championships' if it is not None and southern_kind(it) == 'xc' else 'Southern Track & Field Championships'
    ic = ic_tag(k, it)
    if ic: return ic
    # Steve, 2 Nov 2026: "British League" and "BAL" are the British Athletics League (divisions and qualifying matches
    # included); its cup competitions keep their own names, with BAL / British League spelled out
    kb = re.sub(r'^(b\.?a\.?l\.?|british league|british athletic league)\b', 'british athletics league', k)
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
# Publish only finished issues: the 1960s pilot (Nos. 141-172), plus later issues listed in WORKDIR/published.txt once read AND checked.
PUB = set((int(x) if x.isdigit() else x) for x in open(f'{W}/published.txt').read().split()) if os.path.exists(f'{W}/published.txt') else set()
def published(no):
    return (isinstance(no, int) and 141 <= no <= 172) or no in PUB   # 1960s pilot only; everything else must be listed

# printed numbering, checked against the mastheads 14 Nov 2026 (Steve: 'match the number to what the print edition calls itself')
PRINTED = json.load(open(f'{W}/printed.json')) if os.path.exists(f'{W}/printed.json') else {}
issues, search = [], []
VARIANTS = {}
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
        fin = []
        for e in it['events']:
            t = event_tag(e, it); fin.append(t)
            raw = re.sub(r'\s*\(.*?\)', '', event_tag0(e)).strip().lower().replace('\u2019', "'")
            if raw and raw != t.lower(): VARIANTS.setdefault(t, set()).add(raw)
        it['events'] = list(dict.fromkeys(fin))
    if str(no) in PRINTED: d['printed'] = PRINTED[str(no)]   # what the issue calls itself ('No. 1', '3rd Edition, 1929', or '' if nothing printed)
    json.dump(d, open(f'{OUT}/issues/B{no}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    y = int(str(d['date'])[:4])
    issues.append({'issue': no, 'label': d['label'], 'date': d['date'], 'year': y,
                   'pageCount': d['pageCount'], 'items': len(d['items'])})
    if 'printed' in d: issues[-1]['printed'] = d['printed']
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
                       'h': it.get('heading'), 'sum': it.get('summary'), 'd': d['date'], 'e': it['events'],
                       's': re.sub(r'\s+', ' ', hay).strip()})
    # page images and crops are not copied: they live on Cloudflare R2 (upload with r2up.py from WORKDIR)

issues.sort(key=lambda x: x['date'])
idx = {'title': 'The Belgravian', 'issues': issues,
       # decades with nothing published yet; a decade only partly done (e.g. the 1980s) shows "(more to come)"
       'coming': [d + (' (more to come)' if d in {str(x['year'])[:3] + '0s' for x in issues} else '')
                  for d in ['1920s', '1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s', '2000s']
                  if d not in {str(x['year'])[:3] + '0s' for x in issues}],
       'legends': json.load(open(f'{W}/legends-index.json')) if os.path.exists(f'{W}/legends-index.json') else []}

json.dump(idx, open(f'{OUT}/index.json', 'w'), ensure_ascii=False, indent=1)
# one search file per decade, so a reader only downloads what exists (index.json lists them)
by_dec = {}
for x in search: by_dec.setdefault(x.pop('decade'), []).append(x)
idx['searchFiles'] = [f'search-{d}.json' for d in sorted(by_dec)]
json.dump(idx, open(f'{OUT}/index.json', 'w'), ensure_ascii=False, indent=1)
for d, xs in by_dec.items():
    json.dump({'items': xs}, open(f'{OUT}/search-{d}.json', 'w'), ensure_ascii=False, separators=(',', ':'))

# Steve, 8 Nov 2026: what each competition tag was printed as, so a competition search also finds and highlights
# the wording inside long results round-ups. Only tags with variants are listed.
for t, al in SURREY_ALIASES.items(): VARIANTS.setdefault(t, set()).update(al)
_cnt = collections.Counter(x for v in VARIANTS.values() for x in v)
_names = {t.lower() for t in VARIANTS} | {e.lower() for it in search for e in it.get('e', [])}
VARIANTS = {t: {x for x in v if _cnt[x] == 1 and x not in _names and len(x) > 6} | (set(SURREY_ALIASES.get(t, [])) - {t.lower()})
            for t, v in VARIANTS.items()}
json.dump({t: sorted(v, key=len)[:40] for t, v in VARIANTS.items() if v},
          open(f'{OUT}/tag-variants.json', 'w'), ensure_ascii=False, separators=(',', ':'))

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
# a street address ending in a postcode ("60 Green Acres, Park Hill, Croydon CR0 5UX")
POSTAL = re.compile(r'\b\d{1,4}[A-Za-z]?,? [A-Z][^.;:"]{2,80}?\b[A-Z]{1,2}[\dO][A-Z\d]? ?[\dO][A-Z]{2}\b')
def scrub(s):
    for a in PRIV:
        if a in s: s = s.replace(a, '…')
    s = POSTAL.sub('…', s)
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
# share card text and picture for each person (Steve, 5 Nov 2026): used for link previews (read/share/<id>.html)
# and the page title / description in the reader. Built only from what the archive holds.
MEDIA = 'https://belgravian-images.stephendgardner.workers.dev/belgravian/'
PAGES = 'https://stephengardner1.github.io/belgrave-harriers-data/belgravian/'
RESULTISH = re.compile(r'\b\d{1,2}[:.]\d{2}\b|\b\d+(st|nd|rd|th)\b|^\s*=?\d+\b', re.I)
def n_names(c):
    return len(re.findall(r"\b[A-Z][a-z'’]+(?:[ -][A-Z][a-z'’]+)+", c or ''))
def plural(n, w, ws=None): return f"{n:,} {w if n == 1 else (ws or w + 's')}"
for p in pi:
    ms = p['mentions']
    yrs = sorted({int(y.group(0)) for m in ms for y in [re.search(r'(18|19|20)\d\d', m.get('when') or '')] if y})
    span = (f"{yrs[0]}–{yrs[-1]}" if yrs and yrs[0] != yrs[-1] else str(yrs[0])) if yrs else ''
    nis = len({m['id'].split('-')[0] for m in ms})
    res = sum(1 for m in ms if (item_src.get(m['id'], {}).get('type') in ('results', 'records')) or RESULTISH.search(m.get('note') or ''))
    ph = p.get('photos') or []
    lead = f"{p['name']} in The Belgravian, the Belgrave Harriers club gazette"
    if ms:
        parts = [plural(len(ms), 'mention') + f" in {plural(nis, 'issue')}"]
        if res: parts.append(plural(res, 'race result'))
        if ph: parts.append(plural(len(ph), 'photograph'))
        desc = lead + (f", {span}" if span else '') + ': ' + (', '.join(parts[:-1]) + ' and ' + parts[-1] if len(parts) > 1 else parts[0]) + '.'
    else:
        desc = lead + '.'
        if ph: desc += f" In {plural(len(ph), 'photograph')}."
    if p.get('wrote'): desc += f" Wrote or reported {plural(len(p['wrote']), 'item')}."
    if p.get('official') and not ms: desc += f" Listed as a club official in {plural(len(p['official']), 'item')}."
    # picture: a hand-picked portrait if there is one, else the photo naming the fewest people (a caption that starts
    # with their name wins a tie), else none
    img = ''
    if os.path.exists(f"{OUT}/home/faces/{p['id']}.jpg"): img = f"{PAGES}home/faces/{p['id']}.jpg"
    elif ph:
        sur = p['name'].split()[-1]
        best = min(ph, key=lambda f: (n_names(f.get('c') or f.get('caption')), 0 if (f.get('c') or f.get('caption') or '').lstrip().startswith(p['name'].split()[0]) else 1))
        img = MEDIA + (best.get('f') or best.get('file'))
    p['share'] = {'d': desc, 'img': img, 'u': f"{PAGES}read/share/{p['id']}.html"}

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
