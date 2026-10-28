"""Assemble the Belgravian archive data for the website.
python3 -I build.py WORKDIR REPO_BELGRAVIAN_DIR
Reads WORKDIR/out/B*.json, WORKDIR/crops, WORKDIR/pages, WORKDIR/people-index.json (optional, built by people.py)
and writes: issues/B*.json, index.json, search.json, people.json, pages/, crops/ under the repo folder."""
import json, os, sys, glob, shutil, re, unicodedata

W, OUT = sys.argv[1], sys.argv[2]
man = json.load(open('/home/claude/stephengardner1/surrey-league/research/belgravian/manifest_raw.json'))
urls = {x['no']: x['url'].split('?')[0] for x in man if not x['eharrier']}
os.makedirs(f'{OUT}/issues', exist_ok=True)

def slug(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

issues, search = [], []
for f in sorted(glob.glob(f'{W}/out/B*.json')):
    if re.search(r'\.(orig|firstpass)\.json$', f): continue
    d = json.load(open(f))
    no = d['issue']
    d['pdfUrl'] = urls.get(no)
    for it in d['items']:
        it.setdefault('regions', [])
        for k in ('tables', 'scans', 'photos', 'people', 'events', 'clubs', 'places', 'sport'):
            it[k] = it.get(k) or []
    json.dump(d, open(f'{OUT}/issues/B{no}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    y = int(str(d['date'])[:4])
    issues.append({'issue': no, 'label': d['label'], 'date': d['date'], 'year': y,
                   'pageCount': d['pageCount'], 'items': len(d['items'])})
    for it in d['items']:
        ppl = []
        for p in it['people']:
            ppl += [p.get('name') or '', p.get('printed') or ''] + (p.get('printedAs') or [])
        cells = ' '.join(' '.join(map(str, r)) for t in it['tables'] for r in t.get('rows', []))
        caps = ' '.join((ph.get('caption') or '') for ph in it['photos'] + it['scans'])
        hay = ' '.join([it.get('heading') or '', it.get('summary') or '', it.get('text') or '', cells, caps,
                        ' '.join(ppl), ' '.join(it['events'] + it['places'] + it['clubs'])])
        p0 = min(it['pages']) if it.get('pages') else 1
        search.append({'id': it['id'], 'type': it['type'], 'label': d['label'], 'p': p0,
                       'h': it.get('heading'), 'sum': it.get('summary'),
                       's': re.sub(r'\s+', ' ', hay).strip()})
    # copy media
    for sub in ('pages', 'crops'):
        src = f'{W}/{sub}/B{no}'
        if os.path.isdir(src):
            shutil.copytree(src, f'{OUT}/{sub}/B{no}', dirs_exist_ok=True)

issues.sort(key=lambda x: x['date'])
idx = {'title': 'The Belgravian', 'issues': issues,
       'coming': ['1920s', '1930s', '1940s', '1950s', '1970s', '1980s', '1990s', '2000s'],
       'legends': json.load(open(f'{W}/legends-index.json')) if os.path.exists(f'{W}/legends-index.json') else []}

json.dump(idx, open(f'{OUT}/index.json', 'w'), ensure_ascii=False, indent=1)
json.dump({'items': search}, open(f'{OUT}/search.json', 'w'), ensure_ascii=False, separators=(',', ':'))

# people: light list (people.json) + per-surname-letter shards (people/<letter>.json) + legend profiles
import string
pi = json.load(open(f'{W}/people-index.json'))['people']
legends = idx['legends']
leg_ids = {l['id'] for l in legends}
os.makedirs(f'{OUT}/people', exist_ok=True); os.makedirs(f'{OUT}/legends', exist_ok=True)
shards = {}
light = []
for p in pi:
    letter = (p['sort'][:1] if p['sort'][:1] in string.ascii_lowercase else '_')
    for m in p['mentions']:
        for k in ('sum', 'label'): m.pop(k, None)
        if not m.get('note'): m.pop('note', None)
        if not m.get('h'): m.pop('h', None)
    p['legend'] = p['id'] in leg_ids
    shards.setdefault(letter, []).append(p)
    row = {'id': p['id'], 'name': p['name'], 'n': len(p['mentions']), 's': letter}
    if p['legend']: row['legend'] = True
    light.append(row)
for letter, ps in shards.items():
    json.dump({p['id']: p for p in ps}, open(f'{OUT}/people/{letter}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump({'people': light}, open(f'{OUT}/people.json', 'w'), ensure_ascii=False, separators=(',', ':'))
for l in legends:
    src = f"{W}/../legend/{l['id'][2:]}.json"
    if os.path.exists(src): shutil.copy(src, f"{OUT}/legends/{l['id'][2:]}.json")
print(len(issues), 'issues;', len(search), 'items;', 'search.json', os.path.getsize(f'{OUT}/search.json') // 1024, 'KB')
