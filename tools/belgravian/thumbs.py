"""thumbs.py -- small WebP thumbnails of every photo crop (max 360px on the long side) for galleries and photo rows.
crops/B<no>/<name>.jpg -> thumbs/B<no>/<name>.webp. Skips ones already made. Full crops stay for the lightbox."""
import os, glob
from PIL import Image
W='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
n=0
for f in glob.glob(f'{W}/crops/B*/*'):
    if f.endswith(('.orig','.tmp')): continue
    rel=os.path.relpath(f,f'{W}/crops'); out=f'{W}/thumbs/'+os.path.splitext(rel)[0]+'.webp'
    if os.path.exists(out) and os.path.getmtime(out)>=os.path.getmtime(f): continue
    os.makedirs(os.path.dirname(out),exist_ok=True)
    im=Image.open(f).convert('RGB'); im.thumbnail((360,360)); im.save(out,'WEBP',quality=72,method=6); n+=1
print(n,'thumbnails made')
