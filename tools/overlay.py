"""overlay.py ISSUE_JSON PAGE OUT.png  -- draws every item's region box on the page image, labelled with the item id,
so you can see at a glance whether boxes cover the right content."""
import sys, json, os
from PIL import Image, ImageDraw
d = json.load(open(sys.argv[1])); page = int(sys.argv[2])
W = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[1])))
im = Image.open(f"{W}/pages/B{d['issue']}/B{d['issue']}-p{page:02d}.webp").convert('RGB')
dr = ImageDraw.Draw(im); w, h = im.size
cols = [(200,0,40),(0,90,200),(0,140,60),(200,120,0),(120,0,160)]
for i, it in enumerate(d['items']):
    for r in it.get('regions') or []:
        if r.get('page') != page: continue
        x0,y0,x1,y1 = r['box']; c = cols[i % len(cols)]
        dr.rectangle([x0*w, y0*h, x1*w, y1*h], outline=c, width=3)
        dr.text((x0*w+4, y0*h+3), it['id'], fill=c)
im.save(sys.argv[3]); print(sys.argv[3])
