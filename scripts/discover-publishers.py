import requests,re,os
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"it-IT,it;q=0.9"}
URLS=["https://www.starcomics.com/","https://www.starcomics.com/search/node?keys=demon+slayer","https://www.starcomics.com/cerca?keys=demon+slayer",
"https://www.j-pop.it/","https://www.j-pop.it/?s=dandadan","https://www.j-pop.it/search?q=dandadan",
"https://www.panini.it/shp_ita_it/catalogsearch/result/?q=jujutsu+kaisen","https://www.edizionibd.it/"]
os.makedirs("reports",exist_ok=True); out=open("reports/discover.txt","w",encoding="utf8")
for u in URLS:
    out.write("\n\n######## %s\n"%u)
    try:
        r=requests.get(u,headers=UA,timeout=25,allow_redirects=True)
        t=r.text
        out.write("final=%s status=%s ctype=%s len=%d\n"%(r.url,r.status_code,r.headers.get("content-type"),len(t)))
        out.write("forms: %s\n"%re.findall(r'<form[^>]{0,200}',t)[:4])
        imgs=re.findall(r'(?:src|data-src|content)="([^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"',t)
        out.write("img: %s\n"%imgs[:8])
        links=[l for l in re.findall(r'href="([^"]+)"',t) if re.search(r'fumett|manga|volum|serie|catalog|prodott',l)]
        out.write("links: %s\n"%links[:12])
        out.write("html head: %s\n"%re.sub(r'\s+',' ',t[:700]))
    except Exception as e: out.write("ERRORE %s\n"%e)
out.close()
