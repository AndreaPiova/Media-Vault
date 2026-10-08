import re, io, json, requests, traceback, urllib.parse as up
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
out=open('data/probe-hires.txt','w')
def w(*a): out.write(' '.join(str(x) for x in a)+'\n'); out.flush()
def get(u,**k):
    try: return requests.get(u,headers=UA,timeout=25,**k)
    except Exception as e: w('  errore',u,type(e).__name__); return None
q='20th century boys ultimate deluxe edition'
for name,u in [('IBS-lista','https://www.ibs.it/libri/?query='+up.quote_plus(q)),
               ('IBS-search','https://www.ibs.it/search/?ts=as&query='+up.quote_plus(q)),
               ('Felt-search','https://www.lafeltrinelli.it/search?q='+up.quote_plus(q))]:
    r=get(u)
    if not r: continue
    t=r.text; w('=====',name,r.status_code,len(t),'Urasawa' in t,'Ultimate' in t, 'ultimate' in t.lower())
    for m in list(re.finditer(r'(?i)ultimate deluxe',t))[:3]: w('  ctx:',re.sub(r'\s+',' ',t[max(0,m.start()-250):m.end()+250]))
    # JSON API hints
    for m in list(re.finditer(r'(?:https?:)?//[^"\']*(?:api|search|solr|algolia|elastic)[^"\']*',t))[:8]: w('  api?',m.group(0)[:200])
for name,u in [('GBooks-feed','https://www.google.com/books/feeds/volumes?q='+up.quote_plus(q)+'&max-results=3'),
               ('GBooks-api','https://www.googleapis.com/books/v1/volumes?q='+up.quote_plus(q)+'&maxResults=3'),
               ('OpenLibrary','https://openlibrary.org/search.json?q='+up.quote_plus(q)+'&limit=3'),
               ('Amazon','https://www.amazon.it/s?k='+up.quote_plus(q)),
               ('Panini-new','https://www.panini.it/shp_ita_it/catalogsearch/result/index/?q=20th+century+boys')]:
    r=get(u)
    if r is not None: w('=====',name,r.status_code,len(r.text)); w('  ',re.sub(r'\s+',' ',r.text[:500]))
