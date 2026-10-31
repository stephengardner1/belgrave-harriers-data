"""wordboxes.py ISSUE PAGE word [word...] -- print normalised boxes of OCR words containing the given fragments."""
import sys,subprocess,os
from PIL import Image
W='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
no,p=sys.argv[1],int(sys.argv[2]);frags=[f.lower() for f in sys.argv[3:]]
pdf=[f for f in os.listdir(f'{W}/pdf') if f.startswith(f'B{no}_')][0]
out=f'{W}/priv/blur/_wb'
subprocess.run(['pdftoppm','-r','300','-f',str(p),'-l',str(p),'-png','-singlefile',f'{W}/pdf/{pdf}',out],check=True)
im=Image.open(out+'.png');BW,BH=im.size
for psm in ('11','4'):
    for l in subprocess.run(['tesseract',out+'.png','-','--psm',psm,'tsv'],capture_output=True,text=True).stdout.splitlines()[1:]:
        c=l.split('\t')
        if len(c)>=12 and c[11].strip() and any(f in c[11].lower() for f in frags):
            x,y,w,h=map(int,c[6:10]);print(psm,repr(c[11]),round(x/BW,4),round(y/BH,4),round((x+w)/BW,4),round((y+h)/BH,4))
