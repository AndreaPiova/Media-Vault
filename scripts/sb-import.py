import json, os, re, requests
U=os.environ["SB_URL"]; K=os.environ["SB_PUBKEY"]; V=os.environ["SB_VAULT_KEY"]
SB={"apikey":K,"Authorization":"Bearer "+K,"x-vault-key":V,"Content-Type":"application/json"}
r=requests.get("https://api.jsonbin.io/v3/b/%s/latest"%os.environ["BIN_ID"],headers={"X-Master-Key":os.environ["JB_KEY"]},timeout=60); r.raise_for_status()
rec=r.json()["record"]
raw=json.load(open("scripts/raw-ids.json",encoding="utf-8")); rawids={a for rows in raw.values() for a,_ in rows}
CATS=["films","series","anime","manga","manga_variant","libri","film_infanzia"]
def cat_of(i):
    for p,c in [("mv","manga_variant"),("ab","manga_variant"),("f","films"),("s","series"),("a","anime"),("m","manga"),("b","libri")]:
        if re.match(r"^%s\d"%p,i): return c
    return "films"
STATIC=["mv1780800002","mv1780800003","mv1780800004","f394","ab2","mv1780800001"]
rows=[];ghosts=[];rep={"categorie":{}}
for c in CATS:
    L=rec.get(c) if isinstance(rec.get(c),list) else []
    keep=0;gh=0
    for x in L:
        if not isinstance(x,dict) or not x.get("id"): continue
        if x["id"] not in rawids and not x.get("title"): ghosts.append((x["id"],c)); gh+=1; continue
        rows.append({"id":x["id"],"cat":c,"data":x,"deleted":False,"device":"import-jsonbin"}); keep+=1
    rep["categorie"][c]={"nel_cloud":len(L),"importati":keep,"schede_scheletro_scartate":gh}
tomb={i:cat_of(i) for i in STATIC}
for i in (rec.get("_deleted") or []): tomb[i]=cat_of(i)
for i,c in ghosts: tomb[i]=c
for i,c in tomb.items():
    rows=[x for x in rows if x["id"]!=i]
    rows.append({"id":i,"cat":c,"data":{},"deleted":True,"device":"import-jsonbin"})
rep["eliminati_registrati"]=len(tomb); rep["righe_totali"]=len(rows)
H2={**SB,"Prefer":"resolution=merge-duplicates,return=minimal"}
for i in range(0,len(rows),150):
    x=requests.post(U+"/rest/v1/items?on_conflict=id",headers=H2,json=rows[i:i+150],timeout=90)
    if x.status_code>=300: rep["errore"]=[x.status_code,x.text[:300]]; break
n=requests.get(U+"/rest/v1/items?select=id",headers={**SB,"Prefer":"count=exact","Range":"0-0"},timeout=40)
rep["righe_nel_database"]=n.headers.get("content-range")
rep["ts_cloud"]=rec.get("_ts")
os.makedirs("data",exist_ok=True); json.dump(rep,open("data/supabase-import-report.json","w"),indent=1,ensure_ascii=False); print(json.dumps(rep,ensure_ascii=False))
