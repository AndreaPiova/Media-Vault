import requests,re,json,os
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
S=requests.Session(); S.headers.update(UA); out={}; os.makedirs('data/probe',exist_ok=True)
for k,u in [('azione','https://www.panini.it/shp_ita_it/fumetti-libri-riviste/planet-manga/genere/azione.html'),('azione2','https://www.panini.it/shp_ita_it/fumetti-libri-riviste/planet-manga/genere/azione.html?p=2&product_list_limit=36'),('all','https://www.panini.it/shp_ita_it/fumetti-libri-riviste/planet-manga.html?product_list_limit=36')]:
    try:
        r=S.get(u,timeout=40); t=r.text
        prods=re.findall(r'<a[^>]+class="product-item-link"[^>]*href="([^"]+)"[^>]*>\s*([^<]+?)\s*</a>',t) or re.findall(r'href="(https://www\.panini\.it/shp_ita_it/[a-z0-9\-]+\.html)"[^>]*>\s*([^<]{3,80}?)\s*<',t)
        i=t.find('product-item-info'); 
        out[k]=dict(status=r.status_code,len=len(t),final=r.url[:200],n=len(prods),prods=prods[:12],pager=re.findall(r'(?:toolbar-number|Articoli|risultati)[^<]{0,60}',t)[:6],sample=t[i-100:i+1800] if i>0 else t[:300])
    except Exception as e: out[k]=dict(err=str(e)[:200])
json.dump(out,open('data/probe/panini.json','w'),ensure_ascii=False,indent=1)
