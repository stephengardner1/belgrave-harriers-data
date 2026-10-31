# upsert.py ITEMSFILE : load W/out/B194.json, upsert items (by id) from ITEMSFILE (list), keep order, save
import json, sys
W='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
p=W+'/out/B194.json'
d=json.load(open(p)); new=json.load(open(sys.argv[1]))
ids={it['id']:i for i,it in enumerate(d['items'])}
for it in new:
    if it['id'] in ids: d['items'][ids[it['id']]]=it
    else: d['items'].append(it); ids[it['id']]=len(d['items'])-1
s=json.dumps(d,ensure_ascii=False,indent=1); json.loads(s)
open(p,'w').write(s); print('items',len(d['items']))
