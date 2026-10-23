"""Rebuild the results snapshot from the PUBLISHED view of each sheet:
exactly the rows and columns a reader saw (filters and hidden rows/columns respected)."""
import json, re, sys, html, time, urllib.request
from html.parser import HTMLParser

UA = {"User-Agent": "Mozilla/5.0"}
def get(url):
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception:
            time.sleep(2)
    return 0, ""

class Table(HTMLParser):
    """Reads Google's published grid: data cells only, keeps merges and links."""
    def __init__(s):
        super().__init__(); s.rows=[]; s.row=None; s.cell=None; s.intb=False; s.skip=0; s.frozen=0; s.sawfz=False
    def handle_starttag(s, t, a):
        a=dict(a); cls=a.get("class") or ""
        if t=="tbody": s.intb=True
        elif not s.intb: return
        elif t=="tr": s.row=[]
        elif t=="th": s.skip+=1
        elif t=="td" and s.row is not None and not s.skip:
            if "freezebar" in cls: s.skip+=1; s.fz=True; s.sawfz=True; return
            s.cell={"t":"", "c":int(a.get("colspan",1)), "r":int(a.get("rowspan",1)), "h":None}
        elif t=="br" and s.cell is not None: s.cell["t"]+="\n"
        elif t=="a" and s.cell is not None and a.get("href"): s.cell["h"]=a["href"]
    def handle_endtag(s, t):
        if t=="tbody": s.intb=False
        elif not s.intb: return
        elif t=="th": s.skip-=1
        elif t=="td":
            if getattr(s,"fz",False): s.skip-=1; s.fz=False; return
            if s.cell is not None: s.row.append(s.cell); s.cell=None
        elif t=="tr" and s.row is not None:
            if not s.row and s.sawfz: s.frozen=len(s.rows)
            else: s.rows.append(s.row)
            s.row=None; s.sawfz=False
    def handle_data(s, d):
        if s.cell is not None: s.cell["t"]+=d

def compact(rows):
    """Cell -> plain string, or [text, colspan, rowspan, link] only when needed.
    Drops nothing visible: trailing completely-empty rows/cells only."""
    out=[]
    for r in rows:
        cells=[]
        for c in r:
            t=c["t"].replace("\xa0"," ").strip("\n")
            # Google wraps link targets in a redirect; keep the real destination
            h=c["h"]
            if h and "google.com/url" in h:
                m=re.search(r"[?&]q=([^&]+)", h); h=urllib.parse.unquote(m.group(1)) if m else h
            cells.append(t if (c["c"],c["r"],h)==(1,1,None) else [t,c["c"],c["r"],h])
        while cells and cells[-1]=="": cells.pop()
        out.append(cells)
    while out and not out[-1]: out.pop()
    return out

import urllib.parse
old=json.load(open(sys.argv[1]))
snap={"taken":time.strftime("%Y-%m-%d"), "source":"Published Google Sheets embedded in belgraveharriers.com news articles, as readers saw them", "embeds":[]}
for e in old["embeds"]:
    src=e["embedSrc"]; m=re.search(r"/d/(e/)?([^/]+)/", src)
    base=f"https://docs.google.com/spreadsheets/d/{'e/' if m.group(1) else ''}{m.group(2)}"
    rec={k:e[k] for k in ("article","articleTitle","articleUrl","embedIndex","embedSrc")}
    rec["key"]=m.group(2)+"|"+(re.search(r"gid=(\d+)",src).group(1) if "single=true" in src and "gid=" in src else "all")
    rec["tabs"]=[]
    for t in e["tabs"]:
        if t["status"]!=200: rec["tabs"].append({"name":t["name"],"missing":True}); continue
        url=f"{base}/pubhtml/sheet?headers=false"+(f"&gid={t['gid']}" if t["gid"] else "")
        st,page=get(url); p=Table(); p.feed(page)
        rows=compact(p.rows)
        rec["tabs"].append({"name":t["name"],"head":p.frozen,"rows":rows})
        print(f"{e['article'][:38]:38} {str(t['name'])[:22]:22} csv={len(t['rows']):5} shown={len(rows):5}")
    snap["embeds"].append(rec)
json.dump(snap, open(sys.argv[2],"w"), ensure_ascii=False, separators=(",",":"))
