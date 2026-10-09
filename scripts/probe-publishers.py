import requests,re,json,os
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
T=[('panini','https://www.panini.it/shp_ita_it/catalogsearch/result/?q=gantz'),
('panini2','https://www.panini.it/shp_ita_it/search?q=vinland+saga'),
('star','https://www.starcomics.com/search?q=gantz'),
('star2','https://www.starcomics.com/ricerca?keyword=gantz'),
('jpop','https://www.j-pop.it/?s=real'),
('jpop2','https://j-pop.it/catalogo?search=real'),
('planet','https://www.panini.it/shp_ita_it/planet-manga.html'),
('amazon','https://www.amazon.it/s?k=gantz+new+edition+1+star+comics')]
os.makedirs('data/probe',exist_ok=True); out={}
for k,u in T:
    try:
        r=requests.get(u,headers=UA,timeout=25); t=r.text
        imgs=re.findall(r'https?://[^"\'\s)]+\.(?:jpg|jpeg|png|webp)[^"\'\s)]*',t)
        out[k]=dict(url=u,status=r.status_code,len=len(t),final=r.url,imgs=imgs[:15],title=re.findall(r'<title>(.*?)</title>',t,re.S)[:1])
        open(f'data/probe/{k}.html','w',encoding='utf8').write(t[:60000])
    except Exception as e: out[k]=dict(url=u,err=str(e)[:200])
json.dump(out,open('data/probe/summary.json','w'),ensure_ascii=False,indent=1)
