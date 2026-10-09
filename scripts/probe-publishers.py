import requests,re,json,os
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
S=requests.Session(); S.headers.update(UA); out={}
os.makedirs('data/probe',exist_ok=True)
def rec(k,u,pat=None):
    try:
        r=S.get(u,timeout=30); t=r.text
        out[k]=dict(status=r.status_code,len=len(t),final=r.url,forms=re.findall(r'<form[^>]+action="([^"]*)"',t)[:5],
          links=sorted(set(re.findall(r'href="([^"]*(?:manga|volume|prodotto|fumetto|serie|titolo)[^"]*)"',t)))[:25],
          imgs=sorted(set(re.findall(r'(?:src|data-src|content)="(https?://[^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"',t)))[:25])
        open(f'data/probe/{k}.html','w',encoding='utf8').write(t[:150000]); return t
    except Exception as e: out[k]=dict(err=str(e)[:300])
rec('jpop_s','https://www.j-pop.it/?s=real')
rec('star_home','https://www.starcomics.com/')
rec('star_s','https://www.starcomics.com/search?keyword=gantz')
rec('planet_cat','https://www.panini.it/shp_ita_it/planet-manga.html')
json.dump(out,open('data/probe/summary3.json','w'),ensure_ascii=False,indent=1)
