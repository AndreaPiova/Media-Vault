import json, time, requests, re
UA={"User-Agent":"MediaVault-plot-check/1.0 (personal project)"}
out={}
for it in json.load(open("scripts/plots-aml-input.json",encoding="utf-8"))["libri"]:
    o={"google":[],"wiki":None,"err":None}
    try:
        r=requests.get("https://www.googleapis.com/books/v1/volumes",params={"q":"%s %s"%(it["title"],it["author"]),"maxResults":10,"printType":"books"},headers=UA,timeout=40)
        o["status"]=r.status_code
        for v in r.json().get("items",[]):
            i=v.get("volumeInfo",{}); d=i.get("description","")
            if len(d)>150: o["google"].append({"title":i.get("title"),"authors":i.get("authors"),"lang":i.get("language"),"date":i.get("publishedDate"),"desc":d[:1500]})
    except Exception as e: o["err"]=str(e)[:200]
    try:
        q=requests.get("https://it.wikipedia.org/w/api.php",params={"action":"query","list":"search","srsearch":"%s %s"%(it["title"],it["author"]),"srlimit":2,"format":"json"},headers=UA,timeout=40).json()["query"]["search"]
        for h in q[:1]:
            ex=requests.get("https://it.wikipedia.org/w/api.php",params={"action":"query","prop":"extracts","explaintext":1,"exsectionformat":"wiki","pageids":h["pageid"],"format":"json"},headers=UA,timeout=40).json()["query"]["pages"]
            t=list(ex.values())[0].get("extract","")
            m=re.search(r"==\s*Trama\s*==\n(.*?)(?:\n==[^=]|\Z)",t,re.S)
            o["wiki"]={"page":h["title"],"lead":t[:700],"plot":(m.group(1).strip()[:1200] if m else "")}
    except Exception as e: o["err"]=(o["err"] or "")+" wiki:"+str(e)[:150]
    out[it["id"]]=o; time.sleep(1.2)
json.dump(out,open("data/plots-books.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")
