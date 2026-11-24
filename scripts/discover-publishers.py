import requests,re,os
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36","Accept-Language":"it-IT,it;q=0.9"}
os.makedirs("reports",exist_ok=True); out=open("reports/discover5.txt","w",encoding="utf8")
def w(*a): out.write(" ".join(str(x) for x in a)+"\n"); out.flush()
tests=[("ibs","https://www.ibs.it/search/?ts=as&query=jujutsu+kaisen+1",r'href="(/[^"]*/e/(97[89]\d{10}))"'),
("ibs2","https://www.ibs.it/search/?ts=as&query=20th+century+boys+deluxe+1",r'href="(/[^"]*/e/(97[89]\d{10}))"'),
("libraccio","https://www.libraccio.it/src/?FT=jujutsu+kaisen+1",r'href="(/libro/(97[89]\d{10})[^"]*)"'),
("libraccio2","https://www.libraccio.it/cerca/?FT=jujutsu+kaisen+1",r'href="(/libro/(97[89]\d{10})[^"]*)"'),
("mondadori","https://www.mondadoristore.it/search/?g=jujutsu+kaisen+1",r'href="(/[^"]*/ean/(97[89]\d{10})[^"]*)"'),
("amazon-search","https://www.amazon.it/s?k=jujutsu+kaisen+1+planet+manga&i=stripbooks",r'/dp/([0-9X]{10})')]
for name,u,rx in tests:
    try:
        r=requests.get(u,headers=UA,timeout=40); t=r.text; res=re.findall(rx,t)
        w("\n##",name,r.status_code,r.url[:90],len(t),"| captcha/robot:",bool(re.search(r"captcha|robot check|Access Denied|queue-it",t,re.I)))
        w("risultati:",len(res)); [w("  ",x if isinstance(x,str) else x[0][:90],"" if isinstance(x,str) else x[1]) for x in list(dict.fromkeys(res))[:8]]
    except Exception as e: w("ERRORE",name,e)
out.close()
