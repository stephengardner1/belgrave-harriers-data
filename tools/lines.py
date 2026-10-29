"""lines.py PDF PAGE  -- prints each text line of the page's (rough) text layer with its box as page fractions:
   y0-y1  x0-x1  text     Use it to find item region boxes quickly; the text itself may be garbled."""
import sys, subprocess, re, html
pdf, page = sys.argv[1], sys.argv[2]
x = subprocess.run(['pdftotext','-bbox-layout','-f',page,'-l',page,pdf,'-'],capture_output=True,text=True).stdout
m = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', x)
W, H = float(m.group(1)), float(m.group(2))
for ln in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', x, re.S):
    x0,y0,x1,y1 = (float(ln.group(i)) for i in range(1,5))
    words = ' '.join(html.unescape(w) for w in re.findall(r'>([^<]*)</word>', ln.group(5)))
    print(f'{y0/H:.3f}-{y1/H:.3f}  {x0/W:.2f}-{x1/W:.2f}  {words}')
