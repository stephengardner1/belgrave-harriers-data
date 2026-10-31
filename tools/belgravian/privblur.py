"""privblur.py [ISSUE ...] -- blur the hidden addresses/phone numbers on the published page scans (1976+).
Reads priv/redactions.json + the .prered item regions, OCRs each affected PDF page at 250 dpi (tesseract), finds each
hidden string inside its item's region, and blurs those words (padded) on pages/B<no>/B<no>-pNN.webp.
Untouched originals kept as pages/B<no>/B<no>-pNN.webp.orig (local only). Writes priv/blur/report.json and
before/after previews priv/blur/B<no>-pNN.jpg for checking."""
import json, re, sys, os, subprocess, difflib, shutil, collections
from PIL import Image, ImageFilter, ImageDraw
W='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
R=[r for r in json.load(open(f'{W}/priv/redactions.json')) if r['id'].split('-')[1].isdigit()]
only=set(sys.argv[1:])
SKIP=json.load(open(f'{W}/priv/skip.json')) if os.path.exists(f'{W}/priv/skip.json') else []
R=[r for r in R if not any(r['id']==k['id'] and r['find'].startswith(k['find']) for k in SKIP)]
def norm(t):
    t=t.lower().replace('|','l')
    return re.sub(r'[^a-z0-9]','',t)
def toks(s): return [norm(x) for x in re.split(r'[\s,./()\-:;]+',s) if norm(x)]
def sim(a,b):
    if a==b: return 1
    tr=str.maketrans('ilo','110')
    if a.translate(tr)==b.translate(tr): return 0.95
    return difflib.SequenceMatcher(None,a,b).ratio()
issues=collections.defaultdict(lambda: collections.defaultdict(list))
for r in R:
    no=r['id'].split('-')[0][1:]
    if only and no not in only: continue
    d=json.load(open(f'{W}/out/B{no}.json.prered'))
    it=[i for i in d['items'] if i['id']==r['id']]
    if not it: continue
    for g in it[0].get('regions',[]):
        if g.get('box'): issues[no][g['page']].append((r,g['box']))
report=[]
for no,pages in sorted(issues.items()):
    pdf=[f for f in os.listdir(f'{W}/pdf') if f.startswith(f'B{no}_')][0]
    for p,lst in sorted(pages.items()):
        png=f'/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv/priv/blur/_p'
        subprocess.run(['pdftoppm','-r','250','-f',str(p),'-l',str(p),'-png','-singlefile',f'{W}/pdf/{pdf}',png],check=True)
        big=Image.open(png+'.png'); BW,BH=big.size
        cache={}
        def ocr_box(box):
            key=tuple(box)
            if key in cache: return cache[key]
            pad=0.02
            x0,y0,x1,y1=max(0,box[0]-pad),max(0,box[1]-pad),min(1,box[2]+pad),min(1,box[3]+pad)
            L,T0=int(x0*BW),int(y0*BH)
            big.crop((L,T0,int(x1*BW),int(y1*BH))).save(png+'c.png')
            ws=[]
            for psm in ('6','4','11'):
                tsv=subprocess.run(['tesseract',png+'c.png','-','--psm',psm,'tsv'],capture_output=True,text=True).stdout.splitlines()
                for line in tsv[1:]:
                    c=line.split('\t')
                    if len(c)<12 or not c[11].strip(): continue
                    ws.append(dict(t=norm(c[11]),raw=c[11],x=(L+int(c[6]))/BW,y=(T0+int(c[7]))/BH,w=int(c[8])/BW,h=int(c[9])/BH,key=(psm,c[2],c[3],c[4])))
                ws.append(dict(t='',raw='',x=0,y=0,w=0,h=0,key=('sep',)))
            cache[key]=ws; return ws
        boxes=[]
        for r,box in lst:
            x0,y0,x1,y1=box; pad=0.02
            cand=[w for w in ocr_box(box) if w['t'] or w['key']==('sep',)]
            parts=[x for x in r['find'].split('\n') if toks(x)]
            if len(parts)>1:
                sp=[w for w in ocr_box(box) if w['key'][0]=='11' and w['t']]
                # geometric lines -> segments split at wide gaps (columns)
                sp.sort(key=lambda w:(w['y']+w['h']/2,w['x']))
                lines=[]
                for w in sp:
                    yc=w['y']+w['h']/2
                    for L_ in lines:
                        if abs(L_['yc']-yc)<0.6*max(w['h'],L_['h']): L_['ws'].append(w); break
                    else: lines.append(dict(yc=yc,h=w['h'],ws=[w]))
                segs=[]
                for L_ in lines:
                    ws=sorted(L_['ws'],key=lambda w:w['x']); cur=[ws[0]]
                    for w in ws[1:]:
                        if w['x']-(cur[-1]['x']+cur[-1]['w'])>2.2*L_['h']: segs.append(cur); cur=[w]
                        else: cur.append(w)
                    segs.append(cur)
                def bestwin(target,pool):
                    bw=(0,None)
                    for si,sg in enumerate(pool):
                        for st in range(len(sg)):
                            acc=''
                            for en in range(st,len(sg)):
                                acc+=sg[en]['t'].translate(tr)
                                if len(acc)>len(target)*1.4+3: break
                                sc=difflib.SequenceMatcher(None,target,acc).ratio()
                                if sc>bw[0]: bw=(sc,(si,sg[st:en+1]))
                    return bw
                tr=str.maketrans('ilo','110')
                tg=[''.join(toks(x)).translate(tr) for x in parts]
                # anchor: the longest part
                ai=max(range(len(parts)),key=lambda i:len(tg[i]))
                sc,hit=bestwin(tg[ai],segs)
                got={}
                if sc>=0.7:
                    got[ai]=hit
                    for direction in (1,-1):
                        prev=hit; i=ai+direction
                        while 0<=i<len(parts):
                            px0=min(w['x'] for w in prev[1]); px1=max(w['x']+w['w'] for w in prev[1])
                            py=sum(w['y']+w['h']/2 for w in prev[1])/len(prev[1]); ph=max(w['h'] for w in prev[1])
                            near=[sg for sg in segs if 0<(direction*((sum(w['y']+w['h']/2 for w in sg)/len(sg))-py))<3.2*ph
                                  and min(w['x'] for w in sg)<px1+0.05 and max(w['x']+w['w'] for w in sg)>px0-0.05]
                            s2,h2=bestwin(tg[i],near)
                            if s2<0.55: break
                            h2=(segs.index(near[h2[0]]),h2[1]); got[i]=h2; prev=h2; i+=direction
                found_words=[w for k,v in got.items() for w in v[1]]
                best=(len(got)/len(parts) if got else 0,found_words)
            else:
                target=''.join(toks(r['find'])); tr=str.maketrans('ilo','110')
                target=target.translate(tr)
                best=(0,[])
                for st in range(len(cand)):
                    acc=''
                    for en in range(st,min(len(cand),st+40)):
                        if cand[en]['key']==('sep',): break
                        acc+=cand[en]['t'].translate(tr)
                        if len(acc)>len(target)*1.4+4: break
                        if len(acc)<len(target)*0.6: continue
                        sc=difflib.SequenceMatcher(None,target,acc).ratio()
                        if sc>best[0]: best=(sc,cand[st:en+1])
            ok=best[0]>0 if len(parts)>1 else best[0]>=0.65
            complete=best[0]>=0.99 if len(parts)>1 else ok
            report.append(dict(issue=no,page=p,id=r['id'],kind=r['kind'],find=r['find'][:60],score=round(best[0],2),complete=complete,matched=[w['raw'] for w in best[1]] if ok else []))
            if ok:
                # one box per OCR line: from first to last matched word on that line
                byl=collections.defaultdict(list)
                for w in best[1]: byl[(round((w['y']+w['h']/2)*200),w['key'][0])].append(w)
                for ws in byl.values():
                    boxes.append((min(w['x'] for w in ws),min(w['y'] for w in ws),max(w['x']+w['w'] for w in ws),max(w['y']+w['h'] for w in ws)))
        if not boxes: continue
        pth=f'{W}/pages/B{no}/B{no}-p{p:02d}.webp'
        if not os.path.exists(pth+'.orig'): shutil.copy(pth,pth+'.orig')
        im=Image.open(pth+'.orig').convert('RGB'); IW,IH=im.size; out=im.copy()
        for (a,b,c,d) in boxes:
            px,py=0.006,0.004
            L,T_,Rr,B=int((a-px)*IW),int((b-py)*IH),int((c+px)*IW)+1,int((d+py)*IH)+1
            reg=out.crop((L,T_,Rr,B))
            sw,sh=max(1,reg.width//6),max(1,reg.height//6)
            reg=reg.resize((sw,sh),Image.BILINEAR).resize(reg.size,Image.NEAREST).filter(ImageFilter.GaussianBlur(3))
            out.paste(reg,(L,T_))
        out.save(pth,'WEBP',quality=82)
        # preview: before | after, cropped to the affected band
        ys=[b for _,b,_,_ in boxes]+[d for _,_,_,d in boxes]
        top,bot=max(0,int((min(ys)-0.03)*IH)),min(IH,int((max(ys)+0.03)*IH))
        pv=Image.new('RGB',(IW*2+10,bot-top),'white'); pv.paste(im.crop((0,top,IW,bot)),(0,0)); pv.paste(out.crop((0,top,IW,bot)),(IW+10,0))
        pv.save(f'{W}/priv/blur/B{no}-p{p:02d}.jpg',quality=80)
json.dump(report,open(f'{W}/priv/blur/report.json','w'),indent=1)
agg=collections.defaultdict(list)
for x in report: agg[(x['issue'],x['id'],x['find'])].append(x)
bad=[k for k,v in agg.items() if not any(x['complete'] for x in v)]
print(len(agg),'hidden details;',len(agg)-len(bad),'blurred on the scan;',len(bad),'not found')
for k in bad: print('  NOT FOUND',k, max(x['score'] for x in agg[k]))
