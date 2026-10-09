import base64, hashlib, json, os, requests
from cryptography.fernet import Fernet
U=os.environ["SB_URL"]; K=os.environ["SB_PUBKEY"]; V=os.environ["SB_VAULT_KEY"]
H={"apikey":K,"Authorization":"Bearer "+K,"x-vault-key":V,"Content-Type":"application/json"}
key=base64.urlsafe_b64encode(hashlib.sha256(V.encode()).digest())
rows=json.loads(Fernet(key).decrypt(open("scripts/merged-state.enc","rb").read()))
for r in rows: r["device"]="import-unione-pc-telefono"
rep={"righe_da_importare":len(rows)}
d=requests.delete(U+"/rest/v1/items?deleted=eq.false",headers={**H,"Prefer":"return=minimal"},timeout=90); rep["svuotamento"]=d.status_code
for i in range(0,len(rows),150):
    x=requests.post(U+"/rest/v1/items?on_conflict=id",headers={**H,"Prefer":"resolution=merge-duplicates,return=minimal"},json=rows[i:i+150],timeout=90)
    if x.status_code>=300: rep["errore"]=[x.status_code,x.text[:300]]; break
for tag,q in [("attive","deleted=eq.false"),("eliminate","deleted=eq.true")]:
    n=requests.get(U+"/rest/v1/items?select=id&"+q,headers={**H,"Prefer":"count=exact","Range":"0-0"},timeout=40); rep[tag]=n.headers.get("content-range")
c=requests.get(U+"/rest/v1/items?select=cat",headers={**H},timeout=60)
import collections; rep["per_categoria"]=dict(collections.Counter(x["cat"] for x in c.json() if True))
os.makedirs("data",exist_ok=True); json.dump(rep,open("data/supabase-import-merged-report.json","w"),indent=1,ensure_ascii=False); print(json.dumps(rep,ensure_ascii=False))
