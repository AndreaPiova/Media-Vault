import requests,re,os,io,json
from PIL import Image
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"it-IT,it;q=0.9"}
os.makedirs("reports",exist_ok=True); out=open("reports/discover4.txt","w",encoding="utf8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n"); out.flush()
def isbn10(i13):
    d=[int(c) for c in i13[3:12]]; s=sum((10-k)*x for k,x in enumerate(d)); c=(11-s%11)%11; return "".join(map(str,d))+("X" if c==10 else str(c))
def img(u,name):
    try:
        r=requests.get(u,headers=UA,timeout=30); ct=r.headers.get("content-type","")
        try: im=Image.open(io.BytesIO(r.content)); w("IMG",name,r.status_code,ct,len(r.content),im.size)
        except Exception: w("IMG",name,r.status_code,ct,len(r.content),"non immagine")
    except Exception as e: w("IMG",name,"ERRORE",e)
# 1) Panini ricerca + prodotto
for u in ["https://www.panini.it/shp_ita_it/catalogsearch/result/?q=jujutsu+kaisen+1","https://www.panini.it/shp_ita_it/fumetti-e-manga.html"]:
    try:
        r=requests.get(u,headers=UA,timeout=40); t=r.text; w("\n## PANINI",u,r.status_code,r.url,len(t))
        prods=list(dict.fromkeys(re.findall(r'href="(https://www\.panini\.it/shp_ita_it/[a-z0-9\-]+\.html)"',t)))[:6]; w("prodotti:",prods)
        w("img catalog:",re.findall(r'(https://www\.panini\.it/media/catalog/product[^"\s]+)',t)[:5])
        if prods:
            p=requests.get(prods[0],headers=UA,timeout=40).text
            w("og:image:",re.findall(r'property="og:image"[^>]*content="([^"]+)"',p)[:2],"| ISBN:",re.findall(r'(97[89]\d{10})',p)[:3])
            for m in re.findall(r'(https://www\.panini\.it/media/catalog/product[^"\s]+)',p)[:3]: img(m,"panini-prodotto")
    except Exception as e: w("ERRORE",u,e)
# 2) Google Books
try:
    r=requests.get("https://www.googleapis.com/books/v1/volumes",params={"q":"jujutsu kaisen 1","langRestrict":"it","maxResults":5},headers=UA,timeout=30).json()
    for it in r.get("items",[])[:5]:
        v=it["volumeInfo"]; w("\nGB",it["id"],v.get("title"),v.get("publisher"),[i["identifier"] for i in v.get("industryIdentifiers",[])],list(v.get("imageLinks",{}).keys()))
    if r.get("items"):
        gid=r["items"][0]["id"]; img("https://books.google.com/books/content?id=%s&printsec=frontcover&img=1&zoom=0"%gid,"googlebooks-zoom0"); img("https://books.google.com/books/content?id=%s&printsec=frontcover&img=1&zoom=1"%gid,"googlebooks-zoom1")
except Exception as e: w("ERRORE googlebooks",e)
# 3) immagini per ISBN (JJK 1 Planet: 9788828754220)
I13="9788828754220"; I10=isbn10(I13); w("\nISBN13",I13,"ISBN10",I10)
img("https://covers.openlibrary.org/b/isbn/%s-L.jpg?default=false"%I13,"openlibrary-L")
img("https://images-eu.ssl-images-amazon.com/images/P/%s.01.LZZZZZZZ.jpg"%I10,"amazon-images-P")
img("https://m.media-amazon.com/images/P/%s.01._SCRMZZZZZZ_.jpg"%I10,"amazon-media-P")
for sz in ("0_0_536_0_75","0_0_1200_0_75","0_0_0_0_75"): img("https://www.lafeltrinelli.it/images/%s/%s.jpg"%(I13,sz),"feltrinelli-"+sz)
img("https://www.ibs.it/images/%s_0_0_536_0_75.jpg"%I13,"ibs-536"); img("https://www.ibs.it/images/%s_0_0_1200_0_75.jpg"%I13,"ibs-1200")
img("https://www.libraccio.it/images/%s_0_0_536_0_75.jpg"%I13,"libraccio-536")
out.close()
