"""Free automatic checks. Flags pages where the readable text looks copied from the rough text layer
(machine-reading garbles such as digits inside words, stray symbols) and pages with no items."""
import json, glob, re, sys, os
W = sys.argv[1]
GARBLE = re.compile(r"\b(?=\w*[A-Za-z])(?=\w*\d)[A-Za-z]{2,}\d\w*\b|\b\d[a-z]{2,}\b|[{}$|\\~^]")
rows = []
for f in sorted(glob.glob(f'{W}/out/B*.json')):
    if re.search(r'\.(orig|firstpass)\.json$', f): continue
    d = json.load(open(f)); n = d['issue']
    checked = os.path.exists(f'{W}/out/B{n}.check.md')
    perpage = {}
    for it in d['items']:
        txt = (it.get('text') or '') + ' ' + ' '.join(' '.join(map(str, r)) for t in it.get('tables') or [] for r in t.get('rows', []))
        hits = [m.group(0) for m in GARBLE.finditer(txt) if not re.fullmatch(r"\d+(st|nd|rd|th|s|lb|lbs|yds|ins|ft|m|km|mins?|secs?|pts)", m.group(0), re.I)]
        for p in it.get('pages') or []:
            perpage.setdefault(p, []).extend(hits)
    empty = [p for p in range(1, d['pageCount'] + 1) if p not in perpage]
    sus = {p: h for p, h in perpage.items() if len(h) >= 3}
    rows.append((n, d['label'], checked, empty, sus))
for n, lab, ch, empty, sus in rows:
    print(f"B{n} {lab:16} {'checked' if ch else '-------'}  empty pages: {empty or '-'}  suspect pages: " +
          (', '.join(f"p{p}({len(h)}: {' '.join(h[:3])})" for p, h in sorted(sus.items())) or '-'))
