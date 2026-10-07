#!/usr/bin/env python3
"""Confronta ogni poster film del repo con i poster TMDB dello stesso film (dHash) per scovare scambi/errori."""
import io, json, os, re, time, unicodedata
import requests
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
KEY=os.environ["TMDB_KEY"]; B="https://api.themoviedb.org/3"; S=requests.Session()
def tm(p,**q):
    q["api_key"]=KEY
    for i in range(4):
        try:
            r=S.get(B+p,params=q,timeout=30)
            if r.status_code==429: time.sleep(2); continue
            return r.json() if r.status_code==200 else None
        except Exception: time.sleep(1)
def dh(im):
    g=im.convert("L").resize((9,8),Image.LANCZOS); px=list(g.getdata()); bits=0
    for y in range(8):
        for x in range(8): bits=(bits<<1)|(px[y*9+x]>px[y*9+x+1])
    return bits
def ham(a,b): return bin(a^b).count("1")
def img(url):
    for i in range(3):
        try:
            r=S.get(url,timeout=40)
            if r.status_code==200: return Image.open(io.BytesIO(r.content))
        except Exception: time.sleep(1)
def work(f):
    out={"id":f["id"],"title":f["title"],"year":f["year"],"rating":f["rating"],"poster":f["poster"]}
    try:
        tid=f.get("tmdb")
        if not tid:
            d=tm("/search/movie",query=f["title"],year=f["year"] or "")
            res=(d or {}).get("results") or (tm("/search/movie",query=f["title"]) or {}).get("results") or []
            tid=res[0]["id"] if res else None
        out["tmdb"]=tid
        if not tid: out["err"]="tmdb non trovato"; return out
        d=tm("/movie/%d/images"%tid) or {}
        paths=[p["file_path"] for p in d.get("posters",[])][:30]
        mine=img(f["poster"]); 
        if not mine: out["err"]="poster non scaricabile"; return out
        h=dh(mine); best=64
        for p in paths:
            im=img("https://image.tmdb.org/t/p/w154"+p)
            if im: best=min(best,ham(h,dh(im)))
        out["dist"]=best; out["hash"]=h
    except Exception as e: out["err"]=str(e)
    return out
def main():
    films=json.load(open("scripts/film-poster-input.json",encoding="utf-8"))
    with ThreadPoolExecutor(8) as ex: res=list(ex.map(work,films))
    os.makedirs("data",exist_ok=True)
    json.dump(res,open("data/film-poster-check.json","w",encoding="utf-8"),ensure_ascii=False)
    ok=[r for r in res if "dist" in r]
    print("controllati",len(ok),"su",len(res),"| sospetti (dist>14):",sum(1 for r in ok if r["dist"]>14),"| errori:",sum(1 for r in res if "err" in r))
main()
