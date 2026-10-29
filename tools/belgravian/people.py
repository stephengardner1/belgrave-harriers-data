"""Build the people index from the issue files.
python3 -I people.py WORKDIR   -> WORKDIR/people-index.json and WORKDIR/people-report.md

Rules (conservative; a person page must never mix two people):
- A name with a first name ("Gerry North", "CHARLIE DABBS") is a person key (case-normalised).
- An initials-only name ("G. North", "E.W. Hall") joins a full name only when exactly ONE full name in the
  archive has that surname and first initial. If two or more could fit (Gerry/Geoff North), it stays separate.
- Names listed in KEEP_APART never merge with anything else.
- Within one item, the reader already merged forms of one person (printedAs).
"""
import json, glob, re, sys, os, unicodedata, collections

W = sys.argv[1]
KEEP_APART = {'g north'}
# printed abbreviations that point to one person (the magazine's own convention)
ALIASES = {'gy north': 'gerald north', 'gf north': 'geoffrey north', 'gorry north': 'gerald north'}  # 'Gorry North' (B175, 1970) is Gerry: Steve, 29 Oct 2026        # Gerry North and Geoff North are different people (Steve, Oct 2026)

sl = json.load(open('/home/claude/stephengardner1/surrey-league/data.json'))
sl_names = set()
for r in sl['races']:
    for x in r.get('results', []):
        if x.get('c') == 'BEL' and x.get('n'):
            sl_names.add(x['n'].lower())

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
            'dennis denis', 'jacqueline jackie', 'frederick freddy', 'raymond raymund', 'leslie les',
            'lawrence laurence laurie larry', 'nicholas nicky', 'herbert herbie bert', 'arthur art', 'gordon gordie',
            'malcolm malc', 'barry barrie', 'sidney sydney syd sid', 'walter wally', 'stuart stewart stu', 'mervyn merv', 'percival percy']:
    ws = grp.split()
    for w in ws:
        NICK.setdefault(w, ws[0])

def canon_first(f):
    f = key(f)
    return NICK.get(f, f)

def key(n):
    return unicodedata.normalize('NFD', n).encode('ascii', 'ignore').decode().lower().replace('.', '').strip()

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', key(s)).strip('-')

mentions = []
PUB = set(int(x) for x in open(f'{W}/published.txt').read().split()) if os.path.exists(f'{W}/published.txt') else set()
for f in sorted(glob.glob(f'{W}/out/B*.json')):
    if re.search(r'\.(orig|firstpass)\.json$', f): continue
    d = json.load(open(f))
    if not (d['issue'] <= 172 or d['issue'] in PUB): continue
    for it in d['items']:
        for p in it.get('people') or []:
            raw = p.get('name') or p.get('printed')
            if not raw:
                continue
            n = clean(raw)
            sp = split(n)
            if not sp or len(sp[2]) < 2:
                continue
            mentions.append(dict(name=n, sp=sp, issue=d['issue'], date=d['date'], label=d['label'], item=it['id'],
                                 p=min(it['pages']) if it.get('pages') else 1, h=it.get('heading'), sum=it.get('summary'),
                                 note=p.get('note'), club=p.get('club'), role=p.get('role'),
                                 printed=[x for x in [p.get('printed')] + (p.get('printedAs') or []) if x],
                                 photos=[ph for ph in (it.get('photos') or []) if raw in (ph.get('people') or []) or n in (ph.get('people') or [])]))

# full-name keys
full = collections.defaultdict(list)
for m in mentions:
    first, inits, sur, has_first = m['sp']
    if has_first:
        if key(m['name']) not in ALIASES:
            full[canon_first(first) + ' ' + key(sur)].append(m)
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
# index full names by (surname, initial)
by_si = collections.defaultdict(set)
for k, ms in full.items():
    first, inits, sur, _ = ms[0]['sp']
    by_si[(key(sur), first[0].lower())].add(k)

def is_bel(c):
    c = (c or '').lower()
    return (not c) or 'bel' in c or c in ('b.h.', 'bh')
# a full name used by a Belgrave member AND by someone printed with another club = two people
split_keys = {k for k, ms in full.items() if any(is_bel(m['club']) and m['club'] for m in ms) and any(not is_bel(m['club']) for m in ms)}

people = {}
def person_for(k, display):
    if k not in people:
        people[k] = {'name': display, 'ms': [], 'aka': set(), 'matched': 'name'}
    return people[k]

unresolved = collections.Counter()
for m in mentions:
    first, inits, sur, has_first = m['sp']
    if key(m['name']) in ALIASES:
        k = ALIASES[key(m['name'])]
        e = person_for(k, m['name']); e['ms'].append(m); e['aka'].update(m['printed'] or [m['name']])
        continue
    if has_first:
        k = canon_first(first) + ' ' + key(sur)
        k = fold.get(k, k)
        disp = f'{first} {sur}'
        if k in split_keys and not is_bel(m['club']):
            k += ' | ' + key(m['club']); disp = f"{first} {sur} ({m['club']})"
        if key(first) != canon_first(first) or len({key(x['sp'][0]) for x in full[k]}) > 1:
            person_for(k, disp)['matched'] = 'name (nickname forms)'
    else:
        ik = key(m['name'])
        cands = by_si.get((key(sur), inits[:1].lower()), set()) if inits else set()
        if ik not in KEEP_APART and len(cands) == 1:
            k = next(iter(cands)); disp = None
            person_for(k, full[k][0]['sp'][0] + ' ' + full[k][0]['sp'][2])['matched'] = 'name+initials'
        else:
            k = ik; disp = m['name']
            if len(cands) > 1:
                unresolved[(m['name'], tuple(sorted(cands)))] += 1
    e = person_for(k, disp or m['name'])
    e['ms'].append(m)
    e['aka'].update(m['printed'] or [m['name']])

# choose display name: most common full form
out = []
for k, e in people.items():
    forms = collections.Counter(m['name'] for m in e['ms'] if m['sp'][3])
    name = forms.most_common(1)[0][0] if forms else e['name']
    if ' | ' in k:
        name = e['name']
    pid = 'p-' + slug(name)
    seen = set(); ms = []
    for m in sorted(e['ms'], key=lambda m: (m['date'], m['item'])):
        if m['item'] in seen:
            continue
        seen.add(m['item'])
        ms.append({'id': m['item'], 'when': m['label'], 'label': f"No. {m['issue']}", 'p': m['p'], 'h': m['h'], 'sum': m['sum'], 'note': m['note']})
    photos = []
    for m in e['ms']:
        for ph in m['photos']:
            f = f"crops/B{m['issue']}/{ph['file']}"
            if f not in [x['file'] for x in photos]:
                photos.append({'file': f, 'caption': ph.get('caption'), 'source': m['item'], 'when': m['label']})
    clubs = collections.Counter(m['club'] for m in e['ms'] if m['club'])
    rec = {'id': pid, 'name': name, 'sort': split(name)[2].lower() + ' ' + name.lower(), 'aka': sorted(e['aka']),
           'club': clubs.most_common(1)[0][0] if clubs else None, 'matchedBy': e['matched'], 'mentions': ms}
    if photos:
        rec['photos'] = photos
        rec['photo'] = photos[0]
    if name.lower() in sl_names:
        rec['slarchive'] = 'https://slarchive.org/#athlete/' + re.sub(r'[^a-z0-9-]', '', name.lower().replace(' ', '-'))
    out.append(rec)

# id clashes (two keys -> same slug) get suffixes
ids = collections.Counter(r['id'] for r in out)
for r in out:
    if ids[r['id']] > 1:
        r['id'] += '-' + str(abs(hash(r['aka'][0])) % 1000)
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
