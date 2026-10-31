import json,sys
out='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv/out/B178.json'
new=json.load(open(sys.argv[1]))
d=json.load(open(out))
ids={i['id'] for i in d['items']}
for it in new:
    if it['id'] in ids:
        d['items']=[it if x['id']==it['id'] else x for x in d['items']]
    else: d['items'].append(it)
json.dump(d,open(out,'w'),indent=1,ensure_ascii=False)
json.load(open(out)); print(len(d['items']))
