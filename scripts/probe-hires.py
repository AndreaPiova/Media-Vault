import re, io, requests, traceback, urllib.parse as up
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
out=open('data/probe-hires.txt','w')
def w(*a): out.write(' '.join(str(x) for x in a)+'\n'); out.flush()
def get(u):
    try: return requests.get(u,headers=UA,timeout=25)
    except Exception as e: w('  errore',u,type(e).__name__); return None
def isz(u):
    r=get(u)
    if r is None: return
    try: s=Image.open(io.BytesIO(r.content)).size
    except Exception: s='non immagine'
    w('  IMG',r.status_code,len(r.content),'B',s,u)
q='20th Century Boys Ultimate Deluxe Edition 1'
for name,u in [('IBS','https://www.ibs.it/search/?ts=as&query='+up.quote_plus(q)),
               ('Feltrinelli','https://www.lafeltrinelli.it/search?q='+up.quote_plus(q)),
               ('Panini','https://www.panini.it/shp_ita_it/catalogsearch/result/?q='+up.quote_plus(q)),
               ('StarComics','https://www.starcomics.com/search?q='+up.quote_plus('slam dunk 1'))]:
    try:
        r=get(u); w('=====',name,r.status_code if r else None,len(r.text) if r else 0,u)
        if not r: continue
        t=r.text
        w(' titles/links:'); [w('   ',m) for m in re.findall(r'href="([^"]*(?:/libri/|/manga|/prodotto|/product|/fumetto|/e/|\.html)[^"]*)"',t)[:12]]
        eans=re.findall(r'97[89]\d{10}',t); w(' EAN trovati:',list(dict.fromkeys(eans))[:8])
        imgs=re.findall(r'(?:src|data-src)="([^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"',t); w(' img:'); [w('   ',x) for x in imgs[:8]]
        if eans:
            e=eans[0]
            for iu in [f'https://img.ibs.it/images/{e}_0_0_536_0_75.jpg',f'https://img.ibs.it/images/{e}_0_0_1200_0_75.jpg',f'https://www.lafeltrinelli.it/images/{e}_0_0_536_0_75.jpg',f'https://books.google.com/books/content?vid=ISBN:{e}&printsec=frontcover&img=1&zoom=1',f'https://covers.openlibrary.org/b/isbn/{e}-L.jpg?default=false']: isz(iu)
    except Exception: w(traceback.format_exc())
