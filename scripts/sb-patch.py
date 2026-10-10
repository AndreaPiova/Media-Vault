import base64, hashlib, json, os, requests
from cryptography.fernet import Fernet
U=os.environ["SB_URL"]; K=os.environ["SB_PUBKEY"]; V=os.environ["SB_VAULT_KEY"]
H={"apikey":K,"Authorization":"Bearer "+K,"x-vault-key":V,"Content-Type":"application/json","Prefer":"return=representation"}
patch=json.loads(Fernet(base64.urlsafe_b64encode(hashlib.sha256(V.encode()).digest())).decrypt(open("scripts/sb-patch.enc","rb").read()))
rep={"ok":0,"conflitti":0,"non_trovati":[],"creati":0}
for p in patch:
    for t in range(3):
        g=requests.get(U+"/rest/v1/items?id=eq.%s"%p["id"],headers=H,timeout=40).json()
        if not g:
            r=requests.post(U+"/rest/v1/items",headers=H,json={"id":p["id"],"cat":p["cat"],"data":{**p["set"]},"device":"patch"},timeout=40)
            rep["creati"]+= (r.status_code==201); break
        row=g[0]; data=dict(row["data"]); data.update(p["set"])
        for k in p["remove"]: data.pop(k,None)
        r=requests.patch(U+"/rest/v1/items?id=eq.%s&rev=eq.%d"%(p["id"],row["rev"]),headers=H,json={"data":data,"device":"patch"},timeout=40)
        if r.status_code==200 and r.json(): rep["ok"]+=1; break
        rep["conflitti"]+=1
os.makedirs("data",exist_ok=True); json.dump(rep,open("data/supabase-patch-report.json","w"),indent=1); print(json.dumps(rep))
