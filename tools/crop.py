"""crop.py PDF PAGE X0 Y0 X1 Y1 OUT.jpg  -- coordinates are fractions (0-1) of the page width/height.
Renders the page at 220 dpi, crops, saves a JPEG (longest side max 1800px)."""
import sys, subprocess, tempfile, os
from PIL import Image
pdf, page = sys.argv[1], int(sys.argv[2]); x0,y0,x1,y1 = map(float, sys.argv[3:7]); out = sys.argv[7]
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['pdftoppm','-r','220','-f',str(page),'-l',str(page),'-png','-singlefile',pdf,os.path.join(d,'p')],check=True)
    im = Image.open(os.path.join(d,'p.png')).convert('RGB')
w,h = im.size
c = im.crop((int(x0*w),int(y0*h),int(x1*w),int(y1*h)))
c.thumbnail((1800,1800))
c.save(out, quality=85)
print(out, c.size)
