import requests,json,os,re,time,urllib.parse as up
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
os.makedirs('data/probe',exist_ok=True); out={}
for q in ['Real Inoue Takehiko Planet Manga','Tegamibachi Asada','Il killer dentro Hiroshi Sakurazaka','Gantz Oku Hiroya Star Comics','Dededemon Dededestruction Asano']:
    d={}
    try:
        r=requests.get('https://www.googleapis.com/books/v1/volumes',params={'q':q,'langRestrict':'it','maxResults':10,'printType':'books'},headers=UA,timeout=30)
        d['gb']=[r.status_code]+[(i['volumeInfo'].get('title'),i['volumeInfo'].get('publisher'),[x['identifier'] for x in i['volumeInfo'].get('industryIdentifiers',[])]) for i in r.json().get('items',[])][:8] if r.status_code==200 else [r.status_code,r.text[:100]]
    except Exception as e: d['gb']=str(e)[:80]
    try:
        r=requests.get('https://openlibrary.org/search.json',params={'q':q,'language':'ita','limit':8,'fields':'title,isbn,publisher'},headers=UA,timeout=30)
        d['ol']=[(x.get('title'),x.get('publisher',[])[:1],x.get('isbn',[])[:4]) for x in r.json().get('docs',[])]
    except Exception as e: d['ol']=str(e)[:80]
    out[q]=d; time.sleep(1)
json.dump(out,open('data/probe/src.json','w'),ensure_ascii=False,indent=1)
