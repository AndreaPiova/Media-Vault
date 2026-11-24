import requests,re,os,json
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"it-IT,it;q=0.9"}
os.makedirs("reports",exist_ok=True); out=open("reports/discover2.txt","w",encoding="utf8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n")
def get(u,**k):
    try: return requests.get(u,headers=UA,timeout=30,**k)
    except Exception as e: w("ERRORE",u,e); return None
# --- Star Comics: pagina prodotto
r=get("https://www.starcomics.com/fumetto/detective-conan-new-edition-75")
if r:
    t=r.text; w("STAR prodotto",r.status_code,len(t))
    w("og:image:",re.findall(r'property="og:image"[^>]*',t)[:3])
    w("img prodotto:",[i for i in re.findall(r'(?:src|data-src|href|content)="([^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"',t) if "cover" in i.lower() or "copertin" in i.lower() or "fumett" in i.lower()][:10])
    w("input ricerca:",re.findall(r'<input[^>]{0,160}',t)[:5])
for u in ["https://www.starcomics.com/sitemap.xml","https://www.starcomics.com/robots.txt","https://www.starcomics.com/ricerca-fumetti?titolo=conan","https://www.starcomics.com/ricerca-fumetti?search=conan","https://www.starcomics.com/catalogo-fumetti"]:
    r=get(u)
    if r: w("\nSTAR",u,r.status_code,r.headers.get("content-type"),len(r.text)); w(re.sub(r'\s+',' ',r.text[:900])); w("links /fumetto/:",len(re.findall(r'href="/fumetto/',r.text)),"| paginazione:",re.findall(r'href="([^"]*(?:page|pagina|p)=\d+[^"]*)"',r.text)[:4])
# --- J-POP Shopify
r=get("https://j-pop.it/collections/manga/products.json?limit=2")
if r:
    w("\nJPOP products.json",r.status_code); w(r.text[:1800])
r=get("https://j-pop.it/search/suggest.json?q=dandadan&resources[type]=product&resources[limit]=3")
if r: w("\nJPOP suggest",r.status_code,r.text[:900])
r=get("https://j-pop.it/sitemap.xml")
if r: w("\nJPOP sitemap",r.status_code,r.text[:700])
out.close()
