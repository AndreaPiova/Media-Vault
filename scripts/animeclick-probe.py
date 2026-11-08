import json, re, requests
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36","Accept-Language":"it-IT,it;q=0.9","Accept":"text/html,application/xhtml+xml"}
out={}
for name,url in [("home","https://www.animeclick.it/"),("search1","https://www.animeclick.it/cerca?name=Death+Note"),("search2","https://www.animeclick.it/ricerca?query=Death+Note"),("page","https://www.animeclick.it/anime/1050/death-note"),("search3","https://www.animeclick.it/cerca/anime?name=Death+Note")]:
    try:
        r=requests.get(url,headers=UA,timeout=40,allow_redirects=True)
        out[name]={"status":r.status_code,"final":r.url,"len":len(r.text),"text":r.text[:1800]}
    except Exception as e: out[name]={"err":str(e)[:200]}
json.dump(out,open("data/animeclick-probe.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")
