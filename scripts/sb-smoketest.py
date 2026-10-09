import os, json, requests
U=os.environ["SB_URL"]; K=os.environ["SB_PUBKEY"]; V=os.environ["SB_VAULT_KEY"]
H={"apikey":K,"Authorization":"Bearer "+K,"x-vault-key":V,"Content-Type":"application/json","Prefer":"return=representation"}
B={"apikey":K,"Authorization":"Bearer "+K,"Content-Type":"application/json"}
def rq(m,p,h=H,**kw): return requests.request(m,U+"/rest/v1/"+p,headers=h,timeout=40,**kw)
res={}
try:
    # prova: chi non ha la chiave privata non deve vedere/scrivere
    x=rq("POST","items",B,json={"id":"zz_intruso","cat":"test","data":{}}); res["senza_chiave_scrittura_bloccata"]=x.status_code in (401,403)
    rq("DELETE","items?id=eq.zz_test",H); rq("DELETE","items?id=eq.zz_intruso",H)
    # inserimento con chiave
    x=rq("POST","items",json={"id":"zz_test","cat":"test","data":{"qty":1},"device":"smoketest"}); res["inserimento"]=x.status_code==201 and x.json()[0]["rev"]==1
    y=rq("GET","items?id=eq.zz_test"); res["lettura"]=y.status_code==200 and len(y.json())==1
    z=rq("GET","items?id=eq.zz_test",B); res["senza_chiave_lettura_vuota"]=z.status_code==200 and z.json()==[]
    # aggiornamento con controllo di revisione
    u=rq("PATCH","items?id=eq.zz_test&rev=eq.1",json={"data":{"qty":6}}); res["aggiornamento_rev1"]=u.status_code==200 and len(u.json())==1 and u.json()[0]["rev"]==2
    c=rq("PATCH","items?id=eq.zz_test&rev=eq.1",json={"data":{"qty":99}}); res["conflitto_rilevato"]=c.status_code==200 and c.json()==[]
    v=rq("GET","items?id=eq.zz_test"); res["valore_finale"]=v.json()[0]["data"]=={"qty":6}
    h=rq("GET","items_history?id=eq.zz_test"); res["storico_salvato"]=h.status_code==200 and len(h.json())>=1
    # impostazioni
    k=rq("POST","kv?on_conflict=key",json={"key":"zz_test","value":{"ok":True}},h={**H,"Prefer":"return=representation,resolution=merge-duplicates"}); res["kv_scrittura"]=k.status_code in (200,201)
    # pulizia
    rq("DELETE","items?id=eq.zz_test"); rq("DELETE","kv?key=eq.zz_test"); rq("DELETE","items_history?id=eq.zz_test")
    res["pulizia"]=len(rq("GET","items?id=eq.zz_test").json())==0
except Exception as e:
    res["errore"]=str(e)[:200]
os.makedirs("data",exist_ok=True); json.dump(res,open("data/supabase-smoketest.json","w"),indent=1)
print(json.dumps(res)); 
