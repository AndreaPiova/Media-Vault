import json, re, time, unicodedata, requests
UA={"User-Agent":"MediaVault-plot-check/1.0 (personal project)"}
def norm(x):
    x=unicodedata.normalize("NFD",(x or "").lower()); x="".join(c for c in x if unicodedata.category(c)!="Mn")
    return re.sub(r"[^a-z0-9]","",x)
def wiki(params):
    p={"format":"json",**params}
    for _ in range(3):
        try: return requests.get("https://it.wikipedia.org/w/api.php",params=p,headers=UA,timeout=40).json()
        except Exception: time.sleep(2)
    return {}
out={}
for it in json.load(open("scripts/anime-wiki-input.json",encoding="utf-8")):
    res=wiki({"action":"query","list":"search","srsearch":it["title"]+" anime","srlimit":3}).get("query",{}).get("search",[])
    got=None
    for r in res:
        pg=wiki({"action":"query","prop":"extracts","explaintext":1,"exsectionformat":"wiki","pageids":r["pageid"]}).get("query",{}).get("pages",{})
        txt=list(pg.values())[0].get("extract","") if pg else ""
        if "anime" not in txt[:500].lower(): continue
        if norm(it["title"]) not in norm(r["title"]) and norm(r["title"]) not in norm(it["title"]): continue
        m=re.search(r"==\s*Trama\s*==\n(.*?)(?:\n==[^=]|\Z)",txt,re.S)
        plot=m.group(1).strip() if m else ""
        paras=[p for p in plot.split("\n") if p.strip() and not p.startswith("=")]
        got={"page":r["title"],"plot":" ".join(paras[:2])[:1400],"lead":txt[:400]}; break
    out[it["id"]]=got or {"page":None}; time.sleep(0.15)
json.dump(out,open("data/anime-wiki.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")
