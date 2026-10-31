"""privmanual.py -- apply hand-set blur boxes (priv/manual_boxes.json) after privblur.py."""
import json,os,shutil
from PIL import Image,ImageFilter
W='/tmp/claude-0/-home-claude/7418dbbe-23b1-5767-91a3-214502410ce0/scratchpad/bv'
for m in json.load(open(f'{W}/priv/manual_boxes.json')):
    pth=f"{W}/pages/B{m['issue']}/B{m['issue']}-p{m['page']:02d}.webp"
    if not os.path.exists(pth+'.orig'): shutil.copy(pth,pth+'.orig')
    im=Image.open(pth).convert('RGB');IW,IH=im.size;a,b,c,d=m['box']
    L,T,R,B=int(a*IW),int(b*IH),int(c*IW)+1,int(d*IH)+1
    reg=im.crop((L,T,R,B));reg=reg.resize((max(1,reg.width//6),max(1,reg.height//6)),Image.BILINEAR).resize(reg.size,Image.NEAREST).filter(ImageFilter.GaussianBlur(3))
    im.paste(reg,(L,T));im.save(pth,'WEBP',quality=82)
    pv=Image.open(pth+'.orig').convert('RGB');top,bot=max(0,T-60),min(IH,B+60)
    out=Image.new('RGB',(IW*2+10,bot-top),'white');out.paste(pv.crop((0,top,IW,bot)),(0,0));out.paste(im.crop((0,top,IW,bot)),(IW+10,0))
    out.save(f"{W}/priv/blur/manual-B{m['issue']}-p{m['page']:02d}.jpg",quality=80);print('blurred',m['issue'],m['page'],m['why'])
