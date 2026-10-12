import json, os, re, time, unicodedata, requests
S=requests.Session()
Q="""query($q:String,$m:Int){Media(search:$q,idMal:$m,type:ANIME){id idMal format status episodes startDate{year month} endDate{year month} title{romaji english}}}"""
def al(**v):
    v={k:x for k,x in v.items() if x}
    for i in range(6):
        try:
            r=S.post("https://graphql.anilist.co",json={"query":Q,"variables":v},timeout=40)
            if r.status_code==429: time.sleep(int(r.headers.get("Retry-After",30))); continue
            if r.status_code>=500: time.sleep(3*(i+1)); continue
            return (r.json().get("data") or {}).get("Media")
        except Exception: time.sleep(3*(i+1))
out=[]
for x in json.load(open("scripts/anime-years-input.json",encoding="utf-8")):
    o={"id":x["id"],"title":x["title"],"seasons":[]}
    if x["seasons"]:
        for s in x["seasons"]:
            m=al(q=s["name"]) if s.get("name") else None; time.sleep(0.8)
            o["seasons"].append({"k":s["k"],"label":s["label"],"type":s["type"],"file_year":s["year"],"file_eps":s["eps"],"al":m and {"title":m["title"]["romaji"],"fmt":m["format"],"start":m["startDate"]["year"],"end":(m["endDate"] or {}).get("year"),"eps":m["episodes"],"status":m["status"]}})
    else:
        m=al(m=x["mal"]) if x["mal"] else (al(q=x["first_name"] or x["title"])); time.sleep(0.8)
        o["single"]=m and {"title":m["title"]["romaji"],"fmt":m["format"],"start":m["startDate"]["year"],"end":(m["endDate"] or {}).get("year"),"eps":m["episodes"],"status":m["status"]}
    out.append(o); print(x["id"],flush=True)
os.makedirs("data",exist_ok=True); json.dump(out,open("data/anime-years.json","w",encoding="utf-8"),ensure_ascii=False); print(len(out))
