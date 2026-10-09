import requests,re,json,os,urllib.parse as up
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
os.makedirs('data/probe',exist_ok=True); out={}
Q=['real 5','vinland saga 3','tegamibachi 4','letter bee 4','gantz new edition 5','mushishi 2','sun-ken rock 3']
for q in Q:
    d={}
    for site,u in [('ibs','https://www.ibs.it/search/?ts=as&query=%s'),('libraccio','https://www.libraccio.it/src/?FT=%s'),('mondadori','https://www.mondadoristore.it/search/?g=%s'),('unilibro','https://www.unilibro.it/find_buy/findresult?q=%s')]:
        try:
            r=requests.get(u%up.quote_plus(q),headers=UA,timeout=30); t=r.text
            names=re.findall(r'"item_name":"([^"]+)"',t)[:8] or re.findall(r'title="([^"]{5,80})"',t)[:8]
            eans=re.findall(r'97[89]\d{10}',t); d[site]=dict(s=r.status_code,len=len(t),names=names,eans=list(dict.fromkeys(eans))[:8])
        except Exception as e: d[site]=dict(err=str(e)[:100])
    out[q]=d
json.dump(out,open('data/probe/shops.json','w'),ensure_ascii=False,indent=1)
