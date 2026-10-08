import re, io, requests, traceback
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9'}
out=open('data/probe-hires.txt','w')
def w(*a): out.write(' '.join(str(x) for x in a)+'\n'); out.flush()
def img(u):
    try:
        r=requests.get(u,headers=UA,timeout=25); 
        try: s=Image.open(io.BytesIO(r.content)).size
        except Exception: s='non immagine'
        w('  ',r.status_code,r.headers.get('content-type'),len(r.content),'B',s)
        return r
    except Exception as e: w('  errore',e)
try:
    r=requests.get('https://www.animeclick.it/edizione/3089551/20th-century-boys-ultimate-deluxe',headers=UA,timeout=25); t=r.text
    w('## contesto immagine'); i=t.find('/immagini/manga/'); w(t[max(0,i-300):i+400])
    w('## og/href img'); [w(m) for m in re.findall(r'(?:og:image"[^>]*|href="[^"]*\.(?:jpg|jpeg|png|webp)[^"]*")',t)[:10]]
    txt=re.sub(r'<[^>]+>',' ',t); txt=re.sub(r'\s+',' ',txt)
    w('## ISBN'); [w(txt[max(0,m.start()-60):m.end()+80]) for m in list(re.finditer(r'(?i)isbn|barcode|\bEAN\b',txt))[:5]]
    m=re.search(r'97[89]\d{10}',txt); I=m.group(0) if m else None; w('isbn:',I)
    if I:
        for u in [f'https://covers.openlibrary.org/b/isbn/{I}-L.jpg?default=false',f'https://books.google.com/books/content?vid=ISBN:{I}&printsec=frontcover&img=1&zoom=1',f'https://books.google.com/books/content?vid=ISBN:{I}&printsec=frontcover&img=1&zoom=3',f'https://www.googleapis.com/books/v1/volumes?q=isbn:{I}']:
            w('==',u); img(u)
except Exception: w(traceback.format_exc())
for u in ['https://www.starcomics.com','https://www.panini.it','https://www.jpopmanga.com','https://www.amazon.it','https://www.lafeltrinelli.it','https://www.ibs.it','https://www.mangaworld.cx','https://mangavariant.com']:
    try: w('==',u,requests.get(u,headers=UA,timeout=20).status_code)
    except Exception as e: w('==',u,'errore',type(e).__name__)
