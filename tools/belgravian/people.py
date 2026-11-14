"""Build the people index from the issue files.
python3 -I people.py WORKDIR   -> WORKDIR/people-index.json and WORKDIR/people-report.md

Rules (conservative; a person page must never mix two people):
- A name with a first name ("Gerry North", "CHARLIE DABBS") is a person key (case-normalised).
- Forms differing only in punctuation, spacing, capitals or a man's title are one name (Steve, 14 Nov 2026).
- An initials-only name ("G. North", "E.W. Hall") joins a full name only when exactly ONE person fits: same surname
  and first initial, named in the same years, no clash of club, other initials or walking/running. If two or more
  could fit (Gerry/Geoff North), it stays separate unless name-merges.json (reviewed, with evidence) decides it.
- name-merges.json also holds nickname cases ("H. E. Footer" = Bert Footer) and per-period splits.
- Names listed in KEEP_APART never merge automatically (name-merges.json entries still apply).
- The Surrey League data (for slarchive links) is read from /home/claude/stephengardner1/surrey-league/data.json
  (a copy of https://slarchive.org/data.json); without it, profiles lose their slarchive links.
- Within one item, the reader already merged forms of one person (printedAs).
"""
import json, glob, re, sys, os, unicodedata, collections, zlib

W = sys.argv[1]
KEEP_APART = {'g north'}
# printed abbreviations that point to one person (the magazine's own convention)
ALIASES = {'gy north': 'gerald north', 'gf north': 'geoffrey north', 'gorry north': 'gerald north', 'a stroud': 'albert stroud', 'a ekoku': 'abi ekoku', 'c lawton': 'carl lawton', 'lawton': 'carl lawton', 'gerry adams': 'graham adams', "'gerry' adams": 'graham adams', 'g adams': 'graham adams', "'emu' lawton": 'carl lawton', 'p mead': 'patricia mead', 'pat mead': 'patricia mead', 'patricia mead': 'patricia mead', 'd mead': 'darren mead', 'sp8y': 'neil speaight', 'h e footer': 'albert footer', 'he footer': 'albert footer', 'h footer': 'albert footer', 'b footer': 'albert footer', 'he (bert) footer': 'albert footer', 'h e (bert) footer': 'albert footer', 'footer': 'albert footer', 'e footer': 'albert footer', '[illegible] e footer': 'albert footer', 'hefooter': 'albert footer', 'florrie footer': 'albert footer'}  # H. E. Footer is Bert Footer (printed "H.E. (Bert) Footer"): Steve, 8 Nov 2026; "little" Bertie Footer (a child, 1951) and Florrie Footer stay apart; a bare "Footer" is Bert too, the only other Footers being Bertie and Florrie: Steve, 8 Nov 2026; "Florrie Footer" (panto Princess Charming, B186) is Bert in costume: Steve, 8 Nov 2026  # Meads: Steve, 4 Nov 2026  # 'Gorry North' (B175, 1970) is Gerry; 'A. Stroud' is Bert Stroud: Steve, 29 Oct 2026; 'A. Ekoku' is Abi Ekoku, 'C. Lawton' and a bare male 'Lawton' are Carl Lawton: Steve, 1 Nov 2026; Gerry/'Gerry'/G. Adams (all 1985+) are Graham Adams: Steve, 2 Nov 2026        # Gerry North and Geoff North are different people (Steve, Oct 2026)

_sl = '/home/claude/stephengardner1/surrey-league/data.json'
if not os.path.exists(_sl): sys.exit('people.py needs ' + _sl + ' (download https://slarchive.org/data.json there)')
sl = json.load(open(_sl))
sl_names = collections.Counter()  # Belgrave runner name -> number of Surrey League races run for Belgrave
for r in sl['races']:
    for n in {x['n'].lower() for x in r.get('results', []) if x.get('c') == 'BEL' and x.get('n')}:
        sl_names[n] += 1

def clean(n):
    n = re.sub(r'\s+', ' ', (n or '').replace('’', "'")).strip(' .,;:')
    if n.isupper() or (len(n) > 3 and sum(c.isupper() for c in n) > len(n) * .7):
        n = ' '.join(w.capitalize() if not re.fullmatch(r'[A-Z]\.?', w) else w for w in n.split())
        n = re.sub(r"\bMc([a-z])", lambda m: 'Mc' + m.group(1).upper(), n)
        n = re.sub(r"\bO'([a-z])", lambda m: "O'" + m.group(1).upper(), n)
    # tidy initials: "E.W.Hall" -> "E.W. Hall"
    n = re.sub(r'^((?:[A-Z]\.)+)(?=[A-Z][a-z])', r'\1 ', n)
    return n

def split(n):
    """-> (first, initials, surname, has_first_name)"""
    parts = n.replace('.', '. ').split()
    parts = [p for p in parts if p not in ('Mr.', 'Mrs.', 'Miss', 'Dr.', 'Mr', 'Mrs', 'Dr', 'Capt.', 'Lt.', 'Sgt.')]
    if not parts:
        return None
    sur = parts[-1].strip('.')
    rest = parts[:-1]
    inits = ''.join(p[0].upper() for p in rest if p)
    has_first = any(len(p.strip('.')) > 1 for p in rest)
    first = next((p for p in rest if len(p.strip('.')) > 1), '')
    return first, inits, sur, has_first

NICK = {}
for grp in ['charles charlie chas chaz', 'malcolm mal', 'robert bob bobby rob', 'richard dick rick ricky rich ritchie', 'william bill billy',
            'james jim jimmy jimi', 'anthony tony', 'michael mike mick micky', 'david dave', 'ronald ron ronnie', 'edward ted eddie',
            'thomas tom tommy', 'peter pete', 'stanley stan', 'frederick fred freddie', 'alfred alf', 'albert bert',
            'kenneth ken kenny', 'leonard len lenny lennie', 'raymond ray', 'douglas doug', 'donald don', 'harold harry',
            'patrick pat paddy', 'joseph joe', 'samuel sam', 'stephen steve stevie', 'steven steve', 'nicholas nick',
            'christopher chris cris', 'timothy tim', 'andrew andy', 'gerald gerry', 'geoffrey geoff', 'terence terry', 'derek del',
            'alan allan allen', 'philip phillip phil', 'reginald reg', 'victor vic', 'clifford cliff', 'edward ed eddy',
            'dennis denis', 'jacqueline jackie jacqui jacky', 'frederick freddy', 'raymond raymund', 'leslie les',
            'lawrence laurence laurie larry', 'nicholas nicky', 'herbert herbie bert', 'arthur art', 'gordon gordie',
            'malcolm malc', 'barry barrie', 'john johnny johnnie', 'oliver olly ollie', 'cynthia cindy', 'alistair alister alastair alasdair', 'darrell darryl daryl darrel', 'sidney sydney syd sid', 'walter wally', 'stuart stewart stu', 'mervyn merv', 'percival percy']:
    ws = grp.split()
    for w in ws:
        NICK.setdefault(w, ws[0])

def canon_first(f):
    f = key(f)
    return NICK.get(f, f)

def key(n):
    # hyphen vs space is a spacing slip, not a different name (McLean-Foreman = McLean Foreman)
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFD', n).encode('ascii', 'ignore').decode().lower().replace('.', '').replace('-', ' ')).strip()

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', key(s)).strip('-')

mentions = []
PRINTED = json.load(open(f'{W}/printed.json')) if os.path.exists(f'{W}/printed.json') else {}   # as each issue prints its number
PUB = set((int(x) if x.isdigit() else x) for x in open(f'{W}/published.txt').read().split()) if os.path.exists(f'{W}/published.txt') else set()
for f in sorted(glob.glob(f'{W}/out/B*.json')):
    if re.search(r'\.(orig|firstpass)\.json$', f): continue
    d = json.load(open(f))
    if not ((isinstance(d['issue'], int) and d['issue'] <= 172) or d['issue'] in PUB): continue
    for it in d['items']:
        for p in it.get('people') or []:
            raw = p.get('name') or p.get('printed')
            if not raw or '[illegible]' in raw or '[?]' in raw:
                continue   # unreadable letters: kept in the item, not indexed as a person (the note stays searchable)
            n = clean(raw)
            sp = split(n)
            if not sp or len(sp[2]) < 2:
                continue
            mentions.append(dict(name=n, sp=sp, issue=d['issue'], date=d['date'], label=d['label'], item=it['id'],
                                 p=min(it['pages']) if it.get('pages') else 1, h=it.get('heading'), sum=it.get('summary'),
                                 note=p.get('note'), club=p.get('club'), role=p.get('role'), sport=it.get('sport'), type=it.get('type'),
                                 printed=[x for x in [p.get('printed')] + (p.get('printedAs') or []) if x],
                                 photos=[ph for ph in (it.get('photos') or []) if raw in (ph.get('people') or []) or n in (ph.get('people') or [])]))

# ---- name tidy-up (Steve, 14 Nov 2026: replaces "people are not merged across different initials or spellings") ----
# 1. Forms that differ only in punctuation, spacing or capitals are one name ("W.H.Hare" = "W. H. Hare", '"Bert" Footer'
#    = "Bert Footer"). A man's title (Mr., Capt., Sgt. ...) is dropped too; Mrs./Miss are kept (a wife or daughter).
# 2. An initials-only name joins a full-name person when exactly ONE person fits: same surname, same first initial, no
#    clash of other initials, mentioned within 2 years of that person's own named mentions, no club clash and no
#    walking/running clash. A shorter form ("T. Green") joins a longer one ("T. W. Green") the same way.
# 3./4. Nicknames whose letter differs from the initials ("H. E. Footer" = Bert Footer) and hard cases (J. Wilson) are
#    decided one by one, with evidence, in name-merges.json beside this script. Only entries marked "apply": true act.
MALE_TITLES = {'mr', 'capt', 'captain', 'sgt', 'sergeant', 'lt', 'cpl', 'pte', 'dr', 'rev', 'l/cpl', 'col', 'major', 'sir'}
FEMALE_TITLES = {'mrs', 'miss', 'ms', 'madame', 'mme', 'lady'}
def loose(n):
    """one key for forms that differ only in punctuation, spacing, capitals or a man's title"""
    k = key(n.replace('\u2019', "'").replace('.', ' ')).replace("'", '').replace('"', '').replace('\u201c', '').replace('\u201d', '')
    w = [x for x in k.replace(',', ' ').split() if x]
    while len(w) > 1 and w[0] in MALE_TITLES: w = w[1:]
    out, buf = [], ''
    for x in w[:-1]:
        if len(x) == 1: buf += x
        else:
            if buf: out.append(buf); buf = ''
            out.append(x)
    if buf: out.append(buf)
    return ' '.join(out + w[-1:])
def title_of(n):
    w = key(n).split()
    return w[0] if w and (w[0] in FEMALE_TITLES or w[0] in MALE_TITLES) else ''
def year(m): return int(str(m['date'])[:4])

# the reviewed table (steps 3 and 4); an entry's optional 'printed' list moves only mentions printed in one of those forms
MERGES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'name-merges.json')))['merges'] \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'name-merges.json')) else []
TABLE = collections.defaultdict(list)    # loose form -> [(from, to, items, target key)]
for x in MERGES:
    if not x.get('apply'): continue
    for f in x['forms']:
        TABLE[loose(f)].append((x.get('from') or 0, x.get('to') or 9999, set(x.get('items') or []), x.get('exceptItems') or [], x.get('intoKey') or x['into'],
                                {loose(q) for q in x.get('printed') or []}))
def table_target(m):
    for y0, y1, items, exc, into, pr in TABLE.get(loose(m['name']), []):
        if m['item'] in exc: continue
        if pr and not any(loose(q) in pr for q in (m['printed'] or [m['name']])): continue   # only these printed forms
        if (items and m['item'] in items) or (not items and y0 <= year(m) <= y1):
            return into
    return None
def alias_of(n):
    return ALIASES.get(key(n)) or ALIASES.get(loose(n))

def into_key(t):
    if ' ' in t and t == t.lower(): return t          # already a key ("william kerr")
    sp = split(clean(t)); k = full_key(sp[0], sp[2])
    return fold.get(k, k)
def full_key(first, sur):
    return canon_first(first.strip('\'"\u201c\u201d')) + ' ' + key(sur).replace("'", '')

# full-name keys
full = collections.defaultdict(list)
for m in mentions:
    first, inits, sur, has_first = m['sp']
    if has_first and not alias_of(m['name']) and not table_target(m):
        full[full_key(first, sur)].append(m)
# fold one-letter misprints of first names (>=5 letters) into the commoner spelling with the same surname
def ed1(a, b):
    if abs(len(a)-len(b)) > 1: return False
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b): a, b = b, a
    return any(b[:i] + b[i+1:] == a for i in range(len(b)))
bysur = collections.defaultdict(list)
for k in full: bysur[k.split(' ',1)[1] if ' ' in k else k].append(k)
fold = {}
for sur, ks in bysur.items():
    ks.sort(key=lambda k: -len(full[k]))
    for i, k in enumerate(ks):
        f1 = k.split(' ')[0]
        for big in ks[:i]:
            f2 = big.split(' ')[0]
            if len(f1) >= 5 and len(f2) >= 5 and f1[0] == f2[0] and ed1(f1, f2) and len(full[big]) >= 2 * len(full[k]):
                fold[k] = fold.get(big, big); break
for k, big in fold.items():
    full[big].extend(full.pop(k))

def is_bel(c):
    c = (c or '').lower()
    return (not c) or 'bel' in c or c in ('b.h.', 'bh')
# a full name used by a Belgrave member AND by someone printed with another club = two people
split_keys = {k for k, ms in full.items() if any(is_bel(m['club']) and m['club'] for m in ms) and any(not is_bel(m['club']) for m in ms)}

# what is known about each full-name person: years, initials printed for them, walking or running
WALK = 'race walking'; RUN = {'cross country', 'road', 'track'}
def sport_kind(m):
    s = set(m.get('sport') or [])
    if WALK in s and not (s & RUN): return 'walk'
    if (s & RUN) and WALK not in s: return 'run'
    return ''
ONE_NAME = re.compile(r"^(?:[A-Z][a-z]+\.? )?(?:[A-Z]\.\s?){1,3}\s?[A-Z][A-Za-z'-]+$|^(?:[A-Z]\.\s?){2,3}\s?[A-Z][A-Za-z'-]+$")
finfo = {}
by_sur_full = collections.defaultdict(list)
for k, ms in full.items():
    first, inits, sur, _ = ms[0]['sp']
    # a look back (obituary, history piece) names someone in full long after they ran: kept apart from their own years
    retro = [year(m) for m in ms if m.get('type') == 'obituary' or 'history' in (m.get('sport') or [])]
    ys = [year(m) for m in ms if not (m.get('type') == 'obituary' or 'history' in (m.get('sport') or []))] or [None]
    ini = collections.Counter()
    for m in ms:
        for f in [m['name']] + (m['printed'] or []):
            if not ONE_NAME.match(clean(f)): continue   # "E., A. and A. Bishop" is three people, not initials
            sp = split(clean(f))
            if sp and sp[1] and len(sp[1]) >= 2 and sp[1].isalpha() and sp[1][0] == first[:1].upper() and key(sp[2]).replace("'", '') == key(sur).replace("'", ''): ini[sp[1]] += 1
    kinds = collections.Counter(sport_kind(m) for m in ms if (m.get('role') or 'athlete') == 'athlete')
    finfo[k] = dict(y0=min(ys) if ys[0] else None, y1=max(ys) if ys[0] else None, retro=retro, ini=ini, walk=kinds['walk'], run=kinds['run'], first=k.split(' ')[0])
    by_sur_full[key(sur).replace("'", '')].append(k)

by_si_all = collections.defaultdict(set)
for k2, ms2 in full.items():
    by_si_all[(k2.split(' ', 1)[1] if ' ' in k2 else k2, ms2[0]['sp'][0].strip('\'"\u201c\u201d')[:1].upper())].add(k2)
def fits(k, m, inits, span=None):
    """can full-name person k be the initials-only mention m? (span: judge the years by the whole run of that form)"""
    fi = finfo[k]
    r0, r1 = span or (year(m), year(m))
    named_then = fi['y0'] is not None and not (r1 < fi['y0'] - 3 or r0 > fi['y1'] + 3)
    # or named in full only in a later look back, and the only one of that surname and first initial in the archive
    # (never when they were also named in full as a runner of some other era: that is a different man)
    looked_back = fi['y0'] is None and any(y >= r0 for y in fi['retro']) and len(by_si_all[(k.split(' ', 1)[1], inits[:1])]) == 1
    if not (named_then or looked_back): return False
    fl = full[k][0]['sp'][0].strip('\'"\u201c\u201d')[:1].upper()
    if inits[:1] != fl: return False
    if len(inits) >= 2:   # other initials printed for them (three times or more) must not clash
        ok = sum(v for i, v in fi['ini'].items() if i.startswith(inits) or inits.startswith(i))
        if not ok and sum(fi['ini'].values()) >= 3: return False
    if not is_bel(m['club']) and (k in split_keys or any(is_bel(x['club']) and x['club'] for x in full[k])): return False
    sk = sport_kind(m)
    if sk == 'run' and fi['walk'] >= 5 and fi['walk'] >= 6 * fi['run']: return False
    if sk == 'walk' and fi['run'] >= 5 and fi['run'] >= 6 * fi['walk']: return False
    return True

people = {}
def person_for(k, display):
    if k not in people:
        people[k] = {'name': display, 'ms': [], 'aka': set(), 'matched': 'name'}
    return people[k]

unresolved = collections.Counter()
auto = collections.Counter()   # (form, person) -> mentions joined by rule 2
def add(k, disp, m, how=None):
    e = person_for(k, disp); e['ms'].append(m); e['aka'].update(m['printed'] or [m['name']])
    if how and e['matched'] == 'name': e['matched'] = how

# initials-only mentions, grouped by form; longer forms first so "T. Green" can follow "T. W. Green"
init_ms = collections.defaultdict(list)
for m in mentions:
    first, inits, sur, has_first = m['sp']
    a = alias_of(m['name']); t = table_target(m)
    if a or t:
        k = a or into_key(t)
        add(k, m['name'], m, 'name (Steve)' if a else 'name-merges.json')
        continue
    if has_first:
        k = fold.get(full_key(first, sur), full_key(first, sur))
        disp = f'{first} {sur}'
        if k in split_keys and not is_bel(m['club']):
            k += ' | ' + key(m['club']); disp = f"{first} {sur} ({m['club']})"
        add(k, disp, m)
        if key(first) != canon_first(first) or len({key(x['sp'][0]) for x in full.get(k, [])}) > 1:
            people[k]['matched'] = 'name (nickname forms)'
        continue
    init_ms[loose(m['name'])].append(m)

gyears = {ik: [year(x) for x in ms] for ik, ms in init_ms.items()}
init_by_sur = collections.defaultdict(list)
for ik in init_ms: init_by_sur[ik.split(' ')[-1]].append(ik)
group_target = {}   # initials form -> the person most of its mentions joined (for shorter forms to follow)
# a form's "runs": its mentions split wherever 8+ years pass without one (one form, used by different men in
# different eras, is judged era by era)
runs = {}
for ik, ys in gyears.items():
    yy = sorted(set(ys)); cur = [yy[0], yy[0]]; out = []
    for y in yy[1:]:
        if y - cur[1] >= 8: out.append(tuple(cur)); cur = [y, y]
        else: cur[1] = y
    out.append(tuple(cur)); runs[ik] = out
def run_of(ik, y):
    return next(r for r in runs[ik] if r[0] <= y <= r[1])

def resolve(m, ik):
    first, inits, sur, _ = m['sp']
    if not inits or ik in KEEP_APART or title_of(m['name']) in FEMALE_TITLES: return None, []
    skey = key(sur).replace("'", '')
    y = year(m); r = run_of(ik, y)
    def rivals(lo, hi):
        out = set()
        for ik2 in init_by_sur[ik.split(' ')[-1]]:
            if ik2 == ik: continue
            ms2 = init_ms[ik2]; i2 = ms2[0]['sp'][1]
            if len(i2) <= len(inits) or not i2.startswith(inits): continue
            if title_of(ms2[0]['name']) in FEMALE_TITLES: continue
            # a rival only if printed at least twice in that time (a lone odd form is usually a slip)
            if sum(1 for y2 in gyears[ik2] if lo <= y2 <= hi) >= 2:
                out.add(group_target.get(ik2) or ('=' + ik2))
        return out
    # the whole run first: exactly one person who fits and was named in those years
    cands = {k for k in by_sur_full.get(skey, []) if fits(k, m, inits, r)} | rivals(r[0] - 2, r[1] + 2)
    if len(cands) == 1: return next(iter(cands)), cands
    # else this mention's own year
    cands = {k for k in by_sur_full.get(skey, []) if fits(k, m, inits)} | rivals(y - 5, y + 5)
    return (next(iter(cands)) if len(cands) == 1 else None), cands

for ik in sorted(init_ms, key=lambda k: -len(init_ms[k][0]['sp'][1])):
    got = collections.Counter()
    for m in init_ms[ik]:
        k, cands = resolve(m, ik)
        if k and not k.startswith('='):
            add(k, m['name'], m, 'name+initials'); got[k] += 1; auto[(ik, k)] += 1
        elif k:
            m['_follow'] = k[1:]; got[k[1:]] += 0
        else:
            m['_follow'] = None
            if len(cands) > 1: unresolved[(m['name'], tuple(sorted(cands)))] += 1
    if got and sum(got.values()) >= len(init_ms[ik]) / 2:
        group_target[ik] = got.most_common(1)[0][0]
for ik, ms in init_ms.items():
    for m in ms:
        if '_follow' not in m: continue
        f = m.pop('_follow')
        k = (group_target.get(f) or f) if f else ik
        if f and group_target.get(f): auto[(ik, k)] += 1
        add(k, None, m, 'name+initials' if f else None)

# choose display name: most common full form
out = []
for k, e in people.items():
    forms = collections.Counter(m['name'] for m in e['ms'] if m['sp'][3] and not title_of(m['name']) and '"' not in m['name'])
    if not forms: forms = collections.Counter(m['name'] for m in e['ms'] if m['sp'][3])
    if not forms:   # initials only: the fullest form ("A. E. Smith" over "A. Smith") if printed at least a third as often
        allf = collections.Counter(m['name'] for m in e['ms'] if not title_of(m['name']))
        allf = allf or collections.Counter(m['name'] for m in e['ms'])
        top = allf.most_common(1)[0][1]
        forms = collections.Counter({f: (len(split(f)[1]) if split(f) else 0, n) for f, n in allf.items() if n * 3 >= top})
    name = forms.most_common(1)[0][0] if forms else e['name']
    if ' | ' in k:
        name = e['name']
    pid = 'p-' + slug(name)
    seen = set(); ms = []
    # Steve, 2 Nov 2026: bylines, photo credits and officer listings are not athletic mentions. An item counts as a
    # mention only if the person appears there as an athlete (or is otherwise written about); items where they appear
    # only as author / photographer / official go to separate lists ('wrote', 'credits', 'official').
    byitem = collections.defaultdict(list)
    for m in e['ms']: byitem[m['item']].append(m)
    side = {'wrote': [], 'credits': [], 'official': []}
    ROLE_LIST = {'author': 'wrote', 'photographer': 'credits', 'official': 'official'}
    for m in sorted(e['ms'], key=lambda m: (m['date'], m['item'])):
        if m['item'] in seen:
            continue
        seen.add(m['item'])
        roles = {x.get('role') or 'athlete' for x in byitem[m['item']]}
        if roles & set(ROLE_LIST) and not roles - set(ROLE_LIST):
            for r in sorted(roles):
                side[ROLE_LIST[r]].append({'id': m['item'], 'when': m['label'], 'p': m['p'], 'h': m['h']})
            continue
        ath = [x for x in byitem[m['item']] if (x.get('role') or 'athlete') not in ROLE_LIST]
        ms.append({'id': m['item'], 'when': m['label'], 'label': PRINTED.get(str(m['issue']), f"No. {m['issue']}"), 'p': m['p'], 'h': m['h'], 'sum': m['sum'], 'note': (ath or [m])[0]['note']})
    photos = []
    for m in e['ms']:
        for ph in m['photos']:
            f = f"crops/B{m['issue']}/{ph['file']}"
            if f not in [x['file'] for x in photos]:
                photos.append({'file': f, 'caption': ph.get('caption'), 'source': m['item'], 'when': m['label']})
    clubs = collections.Counter(m['club'] for m in e['ms'] if m['club'])
    rec = {'id': pid, 'name': name, 'sort': split(name)[2].lower() + ' ' + name.lower(), 'aka': sorted(e['aka']),
           'club': clubs.most_common(1)[0][0] if clubs else None, 'matchedBy': e['matched'], 'mentions': ms}
    for k2, v in side.items():
        if v: rec[k2] = v
    if photos:
        rec['photos'] = photos
        rec['photo'] = photos[0]
    if name.lower() in sl_names:
        rec['slarchive'] = 'https://slarchive.org/#athlete/' + re.sub(r'[^a-z0-9-]', '', name.lower().replace(' ', '-'))
        rec['slRaces'] = sl_names[name.lower()]
    out.append(rec)

# id clashes (two keys -> same slug) get suffixes
ids = collections.Counter(r['id'] for r in out)
for r in out:
    if ids[r['id']] > 1:
        r['id'] += '-' + str(zlib.crc32((r['name'] + '|' + r['aka'][0]).encode()) % 1000)  # stable across rebuilds (hash() is not)
legends = json.load(open(f'{W}/legends-index.json')) if os.path.exists(f'{W}/legends-index.json') else []
for r in out:
    if any(l['id'] == r['id'] for l in legends):
        r['legend'] = True
json.dump({'people': out}, open(f'{W}/people-index.json', 'w'), ensure_ascii=False, separators=(',', ':'))
with open(f'{W}/people-report.md', 'w') as fh:
    fh.write(f'# People index\n\n{len(out)} people from {len(mentions)} mentions.\n\n## Initials left unmatched because more than one person fits\n\n')
    for (n, c), v in unresolved.most_common():
        fh.write(f'- {n} ({v}×): could be ' + ', '.join(c) + '\n')
print(len(out), 'people;', len(mentions), 'mentions;', sum(unresolved.values()), 'ambiguous initials')
