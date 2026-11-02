"""privsweep.py -- after privapply: replace every listed address/phone string in ALL string fields of 1976+ issues
(officers header, people notes, captions, summaries), then report anything that still looks like a phone number
or a house-number address, for a final look."""
import json,re,glob,sys
W='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
R=json.load(open(f'{W}/priv/redactions.json'))
LABEL={'address':'[address withheld]','phone':'[phone number withheld]','email':'[e-mail withheld]'}
subs=[]
for r in R:
    for v in {r['find'],r['find'].replace('\n',' '),r['find'].replace('\n',', ')}:
        if len(v)>=5: subs.append((v,LABEL[r['kind']]))
subs.sort(key=lambda x:-len(x[0]))
ST=r"(?:Road|Rd|Avenue|Ave|Gardens|Gdns|Close|Crescent|Street|Lane|Drive|Grove|Place|Terrace|Court|Rise|Walk|Mews|Square|Parade|Way|Hill|Green|Park|Vale|Pt)"
look=re.compile(r"\b\d{1,4}[A-Za-z]?,?\s+(?:[A-Z][\w'.]*\s+){1,3}"+ST+r"\b|\b0\d{1,4}[\s\-.]?\d{2,4}[\s\-.]?\d{3,4}\b|\(\s?0\d{3,5}\s?\)\s*\d{4,7}|\b(?:Tel|Telephone|phone|ring)\b\W{0,3}\d{2,4}[\s\-]?\d{3,5}",re.I)
keep=re.compile(r"Mile|Miles|Hours|Kilos|National Road|Belgrave Road|01.68[56].26 ?49|01.686.1866|997 3818|946.6859|Cherry Orchard|Kings Road|Pam St|Veronica St",re.I)
def fix(o):
    if isinstance(o,str):
        for a,b in subs:
            if a in o: o=o.replace(a,b)
        return o
    if isinstance(o,list): return [fix(x) for x in o]
    if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
    return o
ONLY=set(sys.argv[1:])  # optional issue numbers: only sweep these (other issues may be mid-edit by check jobs)
left=[]
for f in sorted(glob.glob(f'{W}/out/B*.json')):
    if f.split('/')[-1].count('.')>1: continue
    if ONLY and f.split('/B')[-1].split('.')[0] not in ONLY: continue
    d=json.load(open(f))
    if d.get('date','')<'1976': continue
    d2=fix(d)
    if d2!=d:  # write only when something changed, atomically
        tmp=f+'.tmp'; json.dump(d2,open(tmp,'w'),ensure_ascii=False,indent=1); import os; os.replace(tmp,f)
    d=d2
    def walk(o,path):
        if isinstance(o,str):
            for m in look.finditer(o):
                ctx=o[max(0,m.start()-40):m.end()+15]
                if not keep.search(ctx): left.append((d['issue'],path,ctx.replace('\n',' / ')))
        elif isinstance(o,dict):
            for k,v in o.items(): walk(v,path+'.'+k)
        elif isinstance(o,list):
            for i,v in enumerate(o): walk(v,path+f'[{i}]')
    walk(d,'')
for x in left: print(x)
print(len(left),'left to look at')
