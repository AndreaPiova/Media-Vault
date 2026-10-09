import requests,io,json,os,hashlib
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
def i10(e):
    b=e[3:12]; s=sum((10-i)*int(c) for i,c in enumerate(b)); c=(11-s%11)%11; return b+('X' if c==10 else str(c))
os.makedirs('data/probe',exist_ok=True); out={}
for e in ['9788864200750','9788864200477','9788806233341','9788861231665','9788822606341']:
    i=i10(e); U={'feltrinelli':f'https://www.lafeltrinelli.it/images/{e}_0_0_536_0_75.jpg','ibs':f'https://img.ibs.it/images/{e}_0_0_536_0_75.jpg',
    'amazon':f'https://images-na.ssl-images-amazon.com/images/P/{i}.01.LZZZZZZZ.jpg','amazon2':f'https://m.media-amazon.com/images/P/{i}.01._SCRM_.jpg',
    'ol':f'https://covers.openlibrary.org/b/isbn/{e}-L.jpg?default=false','gb':f'https://books.google.com/books/content?vid=ISBN:{e}&printsec=frontcover&img=1&zoom=3',
    'mondadori':f'https://www.mondadoristore.it/img/x/ean/{e}.jpg','libraccio':f'https://www.libraccio.it/images/{e}_0_0_536_0_75.jpg'}
    d={}
    for k,u in U.items():
        try:
            r=requests.get(u,headers=UA,timeout=30)
            try: im=Image.open(io.BytesIO(r.content)); d[k]=[r.status_code,im.size,hashlib.md5(r.content).hexdigest()[:6]]
            except Exception: d[k]=[r.status_code,'noimg',len(r.content)]
        except Exception as ex: d[k]=str(ex)[:60]
    out[e]=d
json.dump(out,open('data/probe/cdn.json','w'),indent=1)
