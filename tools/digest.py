"""digest.py WORKDIR PERSON_ID OUTFILE -- every mention of one person: date, item, heading, the person's note, item summary,
and the sentences of the item text that mention them (by any printed form)."""
import json, sys, re, glob
W, pid, out = sys.argv[1:4]
P = {p['id']: p for p in json.load(open(f'{W}/people-index.json'))['people']}[pid]
forms = sorted({a for a in P['aka'] if len(a) > 3} | {P['name']}, key=len, reverse=True)
items = {}
for f in glob.glob(f'{W}/out/B1*.json'):
    if re.search(r'\.(orig|firstpass)\.json$', f): continue
    d = json.load(open(f))
    for it in d['items']: items[it['id']] = (d, it)
lines = [f"# {P['name']} — {len(P['mentions'])} items; printed as: {', '.join(P['aka'])}\n"]
for m in P['mentions']:
    d, it = items[m['id']]
    sents = re.split(r'(?<=[.!?])\s+', (it.get('text') or '').replace('\n', ' '))
    hit = [s.strip() for s in sents if any(f.lower() in s.lower() for f in forms)][:4]
    rows = [' | '.join(map(str, r)) for t in it.get('tables') or [] for r in t.get('rows', []) if any(f.lower() in ' '.join(map(str, r)).lower() for f in forms)][:4]
    ph = [p.get('caption') for p in (it.get('photos') or []) if any(f in (p.get('people') or []) for f in forms + [P['name']])]
    lines.append(f"## {m['id']} · {d['label']} · p{m['p']} · {it['type']} · {it.get('heading') or ''}\n"
                 f"note: {m.get('note') or '-'}\nsummary: {it.get('summary')}\n" +
                 ''.join(f"> {s}\n" for s in hit) + ''.join(f"| {r}\n" for r in rows) + ''.join(f"[photo] {c}\n" for c in ph))
open(out, 'w').write('\n'.join(lines))
print(out, len(''.join(lines)) // 1000, 'k chars')
