import re,json,os,sys,time,urllib.parse as up,importlib.util,requests
sp=importlib.util.spec_from_file_location('m','scripts/isbn-covers.py'); src=open('scripts/isbn-covers.py').read().replace('\nmain()\n','\n'); ns={'__name__':'m'}; exec(src,ns)
os.makedirs('data/probe',exist_ok=True); out={}
for q in ['Real 5','Real Inoue 5','Real. Vol. 5','Letter Bee 4','Tegamibachi 4','Il killer dentro 3','The Killer Inside 3','Gantz new edition 5','Gantz 5','Dededemon Dededestruction 5','Dededemon 5']:
    r=ns['get']('https://www.ibs.it/search/?ts=as&query='+up.quote_plus(q)); t=r.text if r else ''
    out[q]=dict(len=len(t),items=re.findall(r'"item_id":"(\d{13})","item_name":"([^"]+)"',t)[:10],raw=re.findall(r'"item_name":"[^"]+"',t)[:6])
    time.sleep(1)
json.dump(out,open('data/probe/ibs.json','w'),ensure_ascii=False,indent=1)
