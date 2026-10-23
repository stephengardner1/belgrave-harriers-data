import json,cv2
from concurrent.futures import ThreadPoolExecutor
import eyes as E
items=json.load(open('all-news.json'))
def one(it):
    try:
        img=E.load(it['assetUrl'],800)
        h,w=img.shape[:2]
        det=cv2.FaceDetectorYN.create('models/yunet.onnx','',(w,h),0.75,0.3,50)
        E.det=None
        _,f=det.detect(img)
        r=None
        if f is not None:
            f=[x for x in f if x[2]*x[3]>(w*h)*0.0015]
            if f:
                big=max(x[2]*x[3] for x in f); f=[x for x in f if x[2]*x[3]>=big*0.25]
                ey=[(x[5]+x[7])/2/h for x in f]; ex=[(x[4]+x[6])/2/w for x in f]
                r={'m':'eyes','x':round(float((min(ex)+max(ex))/2),3),'y':round(float(sum(ey)/len(ey)),3)}
        if r is None:
            fp=it.get('mediaFocalPoint') or {}
            r={'m':'centre','x':round(fp.get('x',.5),3),'y':round(fp.get('y',.5),3)}
        r['a']=round(w/h,3)
        return it['urlId'],r
    except Exception as e:
        return it['urlId'],{'m':'error','e':str(e)[:60]}
with ThreadPoolExecutor(12) as ex: res=dict(ex.map(one,items))
json.dump(res,open('hero-framing.json','w'),separators=(',',':'))
import collections;print(collections.Counter(v['m'] for v in res.values()))
