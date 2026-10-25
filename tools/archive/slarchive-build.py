import json,os,re
M={(r['season'],r['match']):r['venue'] for r in json.load(open('data.json'))['races']}
W={(r['season'],r['match']):r['venue'] for r in json.load(open('dw.json'))['races']}
jobs=json.load(open('sl_jobs.json'))
out='/home/claude/belgrave-harriers-data/slarchive/'
n=0;miss=[]
for slug,rs in jobs.items():
    races=[]
    for r in rs:
        f='races/'+re.sub(r'\W+','_',r['url'])+'.json'
        if not os.path.exists(f): miss.append(r['url']);break
        d=json.load(open(f)); d['sex']=r['sex']
        if not d.get('venue'):
            m=re.search(r'race/(\d\d)(\d\d)-(\d)',r['url']);k=('20'+m.group(1)+'/'+m.group(2),int(m.group(3)))
            d['venue']=(W if r['sex']=='Women' else M)[k]
        races.append(d)
    else:
        if len(races)==1: obj=races[0]
        else:
            clubs={};[clubs.update(x['clubs']) for x in races]
            obj={'clubs':clubs,'blocks':[{'races':races}]}
        json.dump(obj,open(out+slug+'.json','w'),ensure_ascii=False,indent=1);n+=1
print('written',n,'missing',len(miss))
