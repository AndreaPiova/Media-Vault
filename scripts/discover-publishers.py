import requests,re,os,io
from PIL import Image
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"it-IT,it;q=0.9"}
os.makedirs("reports",exist_ok=True); out=open("reports/discover3.txt","w",encoding="utf8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n"); out.flush()
for u in ["https://www.starcomics.com/ricerca-fumetti/autocomplete?q=demon+slayer","https://www.starcomics.com/ricerca-fumetti/autocomplete?term=demon+slayer","https://www.starcomics.com/ricerca-fumetti?q=demon+slayer&shop=0","https://www.starcomics.com/sitemap.xml","https://www.starcomics.com/robots.txt"]:
    try:
        r=requests.get(u,headers=UA,timeout=30); w("\n##",u,r.status_code,r.headers.get("content-type"),len(r.text)); w(re.sub(r'\s+',' ',r.text[:1500]))
        w("slug /fumetto/ trovati:",len(re.findall(r'/fumetto/[a-z0-9\-]+',r.text)),re.findall(r'/fumetto/[a-z0-9\-]+',r.text)[:6])
    except Exception as e: w("ERRORE",u,e)
u="https://www.starcomics.com/files/immagini/fumetti-cover/detectiveconan-newedition-75-1200px"
r=requests.get(u,headers=UA,timeout=30); im=Image.open(io.BytesIO(r.content)); w("\nIMG",r.status_code,r.headers.get("content-type"),len(r.content),im.size,im.format)
out.close()
