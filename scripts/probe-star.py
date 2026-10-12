import requests,re,json,os
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
os.makedirs('data/probe',exist_ok=True); out={}
for k,u in [('s1','https://www.starcomics.com/ricerca-fumetti?q=gantz'),('s2','https://www.starcomics.com/ricerca-fumetti?q=one+piece+new+edition+7'),('p1','https://www.starcomics.com/fumetto/gantz-new-edition-1'),('p2','https://www.starcomics.com/fumetto/one-piece-new-edition-7'),('j1','https://j-pop.it/search/suggest.json?resources[type]=product&q=dededemon+7'),('j2','https://j-pop.it/search?q=dededemon+7&type=product')]:
    try:
        r=requests.get(u,headers=UA,timeout=30); t=r.text
        out[k]=dict(status=r.status_code,len=len(t),links=sorted(set(re.findall(r'/fumetto/[a-z0-9\-]+',t)))[:25],og=re.findall(r'og:image"[^>]*content="([^"]+)"',t),title=re.findall(r'<title>(.*?)</title>',t,re.S)[:1])
        open(f'data/probe/{k}.txt','w',encoding='utf8').write(t[:40000])
    except Exception as e: out[k]=dict(err=str(e)[:200])
json.dump(out,open('data/probe/summary.json','w'),ensure_ascii=False,indent=1)
