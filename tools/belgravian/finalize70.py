"""finalize70.py ISSUE -- after all read jobs: validate, order items by page and position, renumber ids, mark ready."""
import json, sys, os, re
B = '/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
no = sys.argv[1]; f = f'{B}/out/B{no}.json'
d = json.load(open(f))
def pos(it):
    p = min(it.get('pages') or [999])
    ys = [r['box'][1] for r in it.get('regions', []) if r.get('page') == p and r.get('box')]
    xs = [r['box'][0] for r in it.get('regions', []) if r.get('page') == p and r.get('box')]
    return (p, round(min(ys or [0]), 2), min(xs or [0]))
d['items'].sort(key=pos)
probs = []
for i, it in enumerate(d['items'], 1):
    it['id'] = f'B{no}-{i:02d}'
    if it.pop('continues', None): probs.append(f'{it["id"]} still marked continues')
    for k in ('pages', 'regions', 'type', 'summary'):
        if not it.get(k): probs.append(f'{it["id"]} missing {k}')
    for ph in (it.get('photos') or []) + (it.get('scans') or []):
        if not os.path.exists(f'{B}/crops/B{no}/{ph.get("file")}'): probs.append(f'{it["id"]} crop missing {ph.get("file")}')
seen = set(p for it in d['items'] for p in it.get('pages', []))
missing = [p for p in range(1, d['pageCount'] + 1) if p not in seen]
if missing: probs.append(f'pages with no item: {missing}')
json.dump(d, open(f, 'w'), ensure_ascii=False, indent=1)
q = json.load(open(f'{B}/queue70.json')); q['issues'][no]['state'] = 'ready'; json.dump(q, open(f'{B}/queue70.json', 'w'), indent=0)
print(f'B{no}: {len(d["items"])} items', '; '.join(probs) or 'ok')
