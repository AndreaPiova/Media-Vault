import json, re, time, requests
UA={"User-Agent":"Mozilla/5.0 (compatible; MediaVault-personal/1.0)","Accept-Language":"it-IT,it;q=0.9"}
out={}
tests=[("anime","Death Note"),("anime","Monster"),("manga","Berserk")]
for kind,t in tests:
    o={}
    try:
        r=requests.get("https://www.animeclick.it/cerca",params={"name":t,"tipo":kind},headers=UA,timeout=40)
        o["search_status"]=r.status_code; o["search_len"]=len(r.text)
        links=re.findall(r'href="(/(?:anime|manga)/\d+/[^"#?]+)"',r.text)
        o["links"]=list(dict.fromkeys(links))[:6]
        o["search_head"]=r.text[:300]
        if links:
            p=requests.get("https://www.animeclick.it"+links[0],headers=UA,timeout=40)
            o["page_status"]=p.status_code; o["page_len"]=len(p.text)
            i=p.text.find("Trama"); o["trama_idx"]=i
            o["trama_snip"]=p.text[max(0,i-200):i+1500] if i>=0 else p.text[:500]
            o["has_cf"]="cloudflare" in p.text.lower()[:3000]
    except Exception as e: o["err"]=str(e)[:200]
    out[kind+":"+t]=o; time.sleep(2)
json.dump(out,open("data/animeclick-probe.json","w",encoding="utf-8"),ensure_ascii=False); print("ok")
