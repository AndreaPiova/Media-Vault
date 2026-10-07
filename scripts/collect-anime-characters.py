#!/usr/bin/env python3
"""Foto personaggi anime da AniList -> data/anime-character-photos.json  {id:{nome_nel_file:url}}"""
import json, re, time, unicodedata, requests
S=requests.Session()
Q="""query($mal:Int,$q:String){Media(idMal:$mal,search:$q,type:ANIME){id title{romaji}
 characters(sort:[ROLE,FAVOURITES_DESC],perPage:40){edges{node{name{full alternative} image{large}}}}}}"""
def gql(v):
    for i in range(6):
        try:
            r=S.post("https://graphql.anilist.co",json={"query":Q,"variables":v},timeout=40)
            if r.status_code==429: time.sleep(int(r.headers.get("Retry-After",30))); continue
            if r.status_code>=500: time.sleep(3*(i+1)); continue
            j=r.json(); return (j.get("data") or {}).get("Media")
        except Exception: time.sleep(3*(i+1))
def norm(s):
    s=unicodedata.normalize("NFD",(s or "").lower()); s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+"," ",s).split()
def score(a,b):
    A,B=set(a),set(b)
    if not A or not B: return 0
    return len(A&B)/max(len(A),len(B)) if A!=B else 1.0
def main():
    items=json.load(open("scripts/anime-chars-input.json",encoding="utf-8")); out={}; miss=[]; nofound=[]
    for it in items:
        m=gql({"mal":it["mal"]}) if it["mal"] else None
        if not m: m=gql({"q":it["title"]})
        if not m: nofound.append(it["title"]); continue
        cands=[]
        for e in m["characters"]["edges"]:
            n=e["node"]; img=(n["image"] or {}).get("large")
            if not img or "default" in img: continue
            for nm in [n["name"]["full"]]+(n["name"].get("alternative") or []): cands.append((norm(nm),img))
        res={}
        for name in it["names"]:
            t=norm(name); best=(0,None)
            for c,img in cands:
                sc=score(t,c)
                if sc>best[0]: best=(sc,img)
            if best[0]>=0.5: res[name]=best[1]
            else: miss.append(it["title"]+": "+name)
        out[it["id"]]=res; time.sleep(0.8)
        print(it["id"],it["title"],len(res),"/",len(it["names"]),flush=True)
    import os; os.makedirs("data",exist_ok=True)
    json.dump(out,open("data/anime-character-photos.json","w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
    print("TOTALE foto",sum(len(v) for v in out.values()),"| senza foto",len(miss),"| anime non trovati",nofound); print("MISS",miss[:60])
main()
