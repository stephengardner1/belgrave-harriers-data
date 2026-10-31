import json, sys
# usage: append.py OUT.json NEWITEMS.json  -> appends items (replacing same id)
out, new = sys.argv[1], sys.argv[2]
d = json.load(open(out))
items = json.load(open(new))
ids = {it['id'] for it in items}
d['items'] = [it for it in d['items'] if it['id'] not in ids] + items
json.dump(d, open(out, 'w'), indent=1, ensure_ascii=False)
json.load(open(out))
print(len(d['items']), 'items')
