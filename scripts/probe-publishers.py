import requests,re,json,os,urllib.parse as up
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
S=requests.Session(); S.headers.update(UA); out={}
def get(u):
    r=S.get(u,timeout=30)
    m=re.search(r"decodeURIComponent\('([^']+)'\)",r.text)
    if m and len(r.text)<5000:
        S.cookies.set('cookietest','1'); r=S.get(up.urljoin('https://www.panini.it',up.unquote(m.group(1))),timeout=30)
    return r
os.makedirs('data/probe',exist_ok=True)
for k,u in [('s_gantz','https://www.panini.it/shp_ita_it/catalogsearch/result/?q=gantz+1'),('s_vinland','https://www.panini.it/shp_ita_it/catalogsearch/result/?q=vinland+saga+3'),('s_real','https://www.panini.it/shp_ita_it/catalogsearch/result/?q=real+inoue+5')]:
    try:
        r=get(u); t=r.text
        links=sorted(set(re.findall(r'href="(https://www\.panini\.it/shp_ita_it/[^"#?]+\.html)"',t)))
        imgs=re.findall(r'https://www\.panini\.it/media/catalog/product/[^"\'\s)]+',t)
        out[k]=dict(status=r.status_code,len=len(t),links=links[:30],imgs=sorted(set(imgs))[:30],final=r.url)
        open(f'data/probe/{k}.html','w',encoding='utf8').write(t[:200000])
        if links:
            p=S.get(links[0],timeout=30).text
            out[k]['product']=dict(url=links[0],og=re.findall(r'og:image"[^>]*content="([^"]+)"',p),title=re.findall(r'<title>(.*?)</title>',p,re.S)[:1],isbn=re.findall(r'97[89]\d{10}',p)[:3])
    except Exception as e: out[k]=dict(err=str(e)[:300])
json.dump(out,open('data/probe/summary2.json','w'),ensure_ascii=False,indent=1)
