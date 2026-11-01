"""privcand.py ISSUE... -- write priv/cand-<tag>.json: every item (and the issue header) of the given 1976+ issues whose
text/tables/captions hit an address, postcode or phone cue, with full text, for the privacy agent."""
import json,re,sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad')
W='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
STREET=r"(?:Road|Rd|Avenue|Ave|Gardens|Gdns|Close|Crescent|Cres|Street|St|Lane|Drive|Dr|Way|Grove|Place|Pl|Terrace|Court|Ct|Hill|Park|Rise|Walk|Mews|Square|Sq|Parade|Green|Vale|View|Mansions|House|Flats?)"
PC=r"(?:\b[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}\b|\b(?:S\.?\s?W|S\.?\s?E|N\.?\s?W|W\.?\s?C|E\.?\s?C)\.?\s?\d{1,2}\b)"
PHONE=r"(?:\b(?:Tel|Telephone|Phone|Tele|'Phone|Ring)\b[.:]?\s*(?:No\.?)?\s*[:\-]?\s*[\dA-Z(][\d\s\-/()A-Z]{4,}|\b0\d{2,4}[\s\-]\d{3}[\s\-]?\d{3,4}\b|\b01[\s\-]\d{3}[\s\-]\d{4}\b|\(0\d{3,5}\)\s?\d{4,6}|\b\d{3}[\s\-]\d{4}\b)"
HOUSE=r"\b\d{1,4}[A-Za-z]?,?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s+"+STREET+r"\b"
pat=re.compile("|".join(f"(?:{x})" for x in (HOUSE,PHONE,PC)))
out=[]
for no in sys.argv[1:]:
    d=json.load(open(f'{W}/out/B{no}.json'))
    hdr=json.dumps({k:v for k,v in d.items() if k!='items'},ensure_ascii=False)
    if pat.search(hdr): out.append({'id':f'B{no}-header','issue':int(no),'date':d.get('date'),'type':'issue header (officers etc.)','text':hdr,'cues':[m.group(0) for m in pat.finditer(hdr)][:8]})
    for it in d['items']:
        txt=it.get('text') or ''
        blob=txt+'\n'+'\n'.join(' | '.join(map(str,r)) for t in it.get('tables') or [] for r in t.get('rows',[]))+'\n'+json.dumps([it.get('summary'),it.get('photos'),it.get('scans'),it.get('people')],ensure_ascii=False)
        hits=[m.group(0) for m in pat.finditer(blob)]
        # time-like results (e.g. "336 1234"?) are rare; keep all hits, agent decides
        if hits: out.append({'id':it['id'],'issue':int(no),'date':d.get('date'),'type':it.get('type'),'heading':it.get('heading'),'text':txt,'tables':it.get('tables'),'summary':it.get('summary'),'captions':[p.get('caption') for p in (it.get('photos') or [])+(it.get('scans') or [])],'people_notes':[p.get('note') for p in it.get('people') or [] if p.get('note')],'cues':hits[:8]})
tag='-'.join(sys.argv[1:])
json.dump(out,open(f'{W}/priv/cand-{tag}.json','w'),ensure_ascii=False,indent=1)
print(tag,len(out),'candidate items')
