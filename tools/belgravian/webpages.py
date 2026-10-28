import sys, subprocess, tempfile, os, glob
from PIL import Image
pdf, outdir = sys.argv[1], sys.argv[2]
no = os.path.basename(pdf).split('_')[0]
os.makedirs(outdir, exist_ok=True)
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['pdftoppm','-r','170','-png',pdf,os.path.join(d,'p')],check=True)
    for f in sorted(glob.glob(os.path.join(d,'p-*.png'))):
        n = int(f.rsplit('-',1)[1].split('.')[0])
        im = Image.open(f).convert('RGB')
        im.save(os.path.join(outdir, f'{no}-p{n:02d}.webp'), quality=60)
print(no)
