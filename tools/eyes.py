import cv2,numpy as np,urllib.request,sys,json
det=None
def load(url,w=1000):
    data=urllib.request.urlopen(urllib.request.Request(url+'?format=%dw'%w,headers={"User-Agent":"Mozilla/5.0"}),timeout=60).read()
    return cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
def eyes(img):
    global det
    h,w=img.shape[:2]
    if det is None: det=cv2.FaceDetectorYN.create('models/yunet.onnx','',(w,h),0.75,0.3,50)
    det.setInputSize((w,h));_,f=det.detect(img)
    if f is None: return None
    f=[x for x in f if x[2]*x[3]>(w*h)*0.0015]           # ignore tiny background faces
    if not f: return None
    big=max(x[2]*x[3] for x in f); f=[x for x in f if x[2]*x[3]>=big*0.25]  # the main subjects
    ey=[(x[5]+x[7])/2/h for x in f]; ex=[(x[4]+x[6])/2/w for x in f]
    return {'x':round((min(ex)+max(ex))/2,3),'y':round(sum(ey)/len(ey),3),'n':len(f),'size':[w,h]}
if __name__=='__main__':
    print(eyes(load(sys.argv[1])))
