import json, sys
# usage: add.py OUTJSON PAGEITEMS.json  -- appends items (or updates items with same id)
out, new = sys.argv[1], sys.argv[2]
d = json.load(open(out))
items = json.load(open(new))
ids = {i['id']: n for n, i in enumerate(d['items'])}
for it in items:
    if it['id'] in ids:
        d['items'][ids[it['id']]] = it
    else:
        d['items'].append(it)
json.dump(d, open(out, 'w'), ensure_ascii=False, indent=1)
json.load(open(out))
print('ok', len(d['items']))
