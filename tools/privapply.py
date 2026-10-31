"""privapply.py REDACTIONS.json -- hide personal addresses/phone numbers (issues 1976+) in W/out/B*.json.
Keeps an untouched copy as out/B<no>.json.prered (local only, never published). Replaces every occurrence of each
listed string in the item's text, summary and table cells; records what was hidden in it['redacted']."""
import json, sys, os, shutil, collections
W='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
R=json.load(open(sys.argv[1]))
LABEL={'address':'[address withheld]','phone':'[phone number withheld]'}
by=collections.defaultdict(list)
for r in R: by[r['id']].append(r)
done=missed=0
for no in sorted({i.split('-')[0][1:] for i in by}):
    f=f'{W}/out/B{no}.json'
    if not os.path.exists(f+'.prered'): shutil.copy(f,f+'.prered')
    d=json.load(open(f))
    for it in d['items']:
        for r in sorted(by.get(it['id'],[]),key=lambda r:-len(r['find'])):
            s,lab=r['find'],LABEL[r['kind']]
            hit=False
            for k in ('text','summary'):
                if it.get(k) and s in it[k]: it[k]=it[k].replace(s,lab); hit=True
            for t in it.get('tables') or []:
                t['rows']=[[c.replace(s,lab) if isinstance(c,str) else c for c in row] for row in t.get('rows',[])]
            if hit or any(lab in str(t) for t in it.get('tables') or []):
                done+=1; red=it.setdefault('redacted',{}); red[r['kind']]=red.get(r['kind'],0)+1
            elif any(lab in (it.get(k) or '') for k in ('text','summary')): done+=1  # already applied
            else: missed+=1; print('NOT FOUND',it['id'],repr(s[:50]))
    json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
print('applied',done,'missed',missed)
