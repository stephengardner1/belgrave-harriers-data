"""Front page of the Belgravian reader: the numbers and lists behind the timeline, the decade panels and the
browse sections (Nov 2026, direction E).

Reads (read only): belgravian/index.json, belgravian/issues/*.json, belgravian/people.json, belgravian/people/*.json
and tools/belgravian/home_picks.json (hand-picked photos, discipline pictures and portraits).
Writes: belgravian/home.json   - totals, articles per year, and per decade: first issue of each year, the most
                                 mentioned athletes, the most reported competitions and six photographs
        belgravian/browse.json - item ids per discipline (track, field, ...), for the discipline pages
Run after the archive is rebuilt:  python3 tools/belgravian/build_home.py
"""
import collections, glob, json, os, re

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, '..', '..', 'belgravian')
SPORTS = ['track', 'field', 'race walking', 'cross country', 'road', 'club life']
KINDS = ['results', 'photo', 'records', 'obituary', 'letter', 'cartoon', 'poem']


def load(p):
    return json.load(open(p, encoding='utf-8'))


def key(no):
    return re.sub(r'^B', '', str(no))


idx = load(os.path.join(ROOT, 'index.json'))
picks = load(os.path.join(HERE, 'home_picks.json'))
issues = sorted(idx['issues'], key=lambda x: (x['date'], str(x['issue'])))
year_of = {key(i['issue']): i['year'] for i in issues}

per_year = collections.Counter()
dec = collections.defaultdict(lambda: {'issues': 0, 'articles': 0, 'nphotos': 0})
ev_forms = collections.defaultdict(collections.Counter)
ev_dec = collections.defaultdict(collections.Counter)
sport_ids = collections.defaultdict(list)
sport_n, kind_n = collections.Counter(), collections.Counter()
photo_item = {}
auto = collections.defaultdict(list)
tot_items = tot_photos = 0

for i in issues:
    d = str(i['year'] // 10 * 10)
    dec[d]['issues'] += 1
    data = load(os.path.join(ROOT, 'issues', 'B%s.json' % key(i['issue'])))
    for it in data.get('items', []):
        tot_items += 1
        per_year[i['year']] += 1
        dec[d]['articles'] += 1
        kind_n[it.get('type')] += 1
        for s in set(it.get('sport') or []):
            sport_n[s] += 1
            sport_ids[s].append(it['id'])
        for e in set((x or '').strip() for x in it.get('events') or []):
            if e:
                ev_forms[e.lower()][e] += 1
                ev_dec[d][e.lower()] += 1
        for ph in it.get('photos') or []:
            if ph.get('review'):
                continue
            tot_photos += 1
            dec[d]['nphotos'] += 1
            photo_item[ph['file']] = (it['id'], ph.get('caption') or '', i['label'])
            c = ph.get('caption') or ''
            if ph.get('people') and 25 <= len(c) <= 170 and 'cover' not in ph['file'].lower():
                auto[d].append({'f': 'crops/B%s/%s' % (key(i['issue']), ph['file']), 'r': 0.75, 'c': c})

# athletes: mentions per decade, named people only (no bare initials or surnames)
P = load(os.path.join(ROOT, 'people.json'))['people']
real = {p['id']: p for p in P if len(p['name'].split()) > 1 and not re.match(r'^[A-Z]\.', p['name'])}
ath = collections.defaultdict(collections.Counter)
for f in glob.glob(os.path.join(ROOT, 'people', '*.json')):
    for pid, v in load(f).items():
        if pid not in real or not isinstance(v, dict):
            continue
        for m in v.get('mentions') or []:
            y = year_of.get(key(str(m['id']).split('-')[0]))
            if y:
                ath[str(y // 10 * 10)][pid] += 1

faces = picks.get('faces', {})
decades = {}
for d in sorted(dec):
    first = {}
    for i in issues:
        # No. 1 is W. H. Hare's one-page covering letter, so 1925 shows No. 2, the first gazette
        if str(i['year'] // 10 * 10) == d and i['year'] not in first and i['issue'] != 1:
            first[i['year']] = {'y': i['year'], 'no': i['issue'], 'label': i['label']}
    photos = []
    for p in picks.get('photos', {}).get(d) or auto[d][:6]:
        fn = p['f'].split('/')[-1]
        iid, cap, lab = photo_item.get(fn, ('', p['c'], ''))
        photos.append({'f': p['f'], 'r': p['r'], 'c': p['c'], 'cap': cap, 'id': iid, 'w': lab})
    decades[d] = dict(dec[d],
                      covers=[first[y] for y in sorted(first)],
                      athletes=[{'id': pid, 'name': real[pid]['name'], 'n': n, 'face': faces.get(pid, '')}
                                for pid, n in ath[d].most_common(6)],
                      comps=[[ev_forms[e].most_common(1)[0][0], n] for e, n in ev_dec[d].most_common(6)],
                      photos=photos)

years = [i['year'] for i in issues]
home = {
    'totals': {'issues': len(issues), 'articles': tot_items, 'photos': tot_photos, 'names': sum(1 for p in P if not p.get('to'))},
    'span': [min(years), max(years)],
    'years': {str(y): per_year[y] for y in sorted(per_year)},
    'decades': decades,
    'disc': [[s, sport_n[s], picks.get('disc', {}).get(s, '')] for s in SPORTS],
    'kinds': [[k, kind_n[k]] for k in KINDS],
    'comps': len([e for e in ev_forms if sum(ev_forms[e].values()) >= 5]),
}
json.dump(home, open(os.path.join(ROOT, 'home.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump({'sport': {s: sport_ids[s] for s in SPORTS}}, open(os.path.join(ROOT, 'browse.json'), 'w', encoding='utf-8'),
          separators=(',', ':'))
print('home.json: %d issues, %d decades; browse.json: %d discipline lists' % (len(issues), len(decades), len(SPORTS)))
