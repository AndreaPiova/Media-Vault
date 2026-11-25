import os,io,csv,subprocess,time,requests
import numpy as np
from PIL import Image,ImageOps
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
START=int(os.environ.get("START","0")); COUNT=int(os.environ.get("COUNT","1000"))
EXC={l.strip()+".jpg" for l in open("scripts/manga-exclude.txt") if l.strip()}
rows=[r for r in csv.DictReader(open("reports/manga-upgrade/dry-merged.csv",encoding="utf8")) if r["esito"]=="MIGLIORATA"]
rows=rows[START:START+COUNT]
def sig(im):
    a=np.asarray(ImageOps.grayscale(im).resize((24,36)),dtype=float); return (a-a.mean())/(a.std()+1e-6)
def push():
    subprocess.run(["git","config","user.name","mediavault-bot"]); subprocess.run(["git","config","user.email","bot@users.noreply.github.com"])
    subprocess.run(["git","add","covers/manga"]); 
    if subprocess.run(["git","diff","--cached","--quiet"]).returncode==0: return
    subprocess.run(["git","commit","-m","Manga: copertine migliorate (Star Comics/J-POP/Amazon/IBS), 2:3 q100"])
    for i in range(5):
        if subprocess.run("git pull --rebase && git push",shell=True).returncode==0: break
        time.sleep(8)
rep=[]; n=0
for r in rows:
    f=r["file"]; path="covers/manga/"+f; cur=Image.open(path).convert("RGB")
    if f in EXC:
        W,H=cur.size
        if abs((W/H)/(2/3)-1)>0.012:
            cur.resize((W,round(W*1.5)),Image.LANCZOS).save(path,"JPEG",quality=100,subsampling=0,optimize=True); rep.append([f,"ESCLUSA_portata_a_2:3",""]); n+=1
        else: rep.append([f,"ESCLUSA_invariata",""])
    else:
        try:
            im=Image.open(io.BytesIO(requests.get(r["url_o_motivo"],headers=UA,timeout=60).content)).convert("RGB")
            s=float((sig(cur)*sig(im)).mean())
            if im.size[0]<cur.size[0]*1.15 or s<0.80: rep.append([f,"SALTATA_controllo_finale","%dpx sim %.2f"%(im.size[0],s)]); continue
            W,H=im.size
            if W>2400: im=im.resize((2400,round(H*2400/W)),Image.LANCZOS); W,H=im.size
            im.resize((W,round(W*1.5)),Image.LANCZOS).save(path,"JPEG",quality=100,subsampling=0,optimize=True); rep.append([f,"SOSTITUITA","%dx%d sim %.2f %s"%(W,round(W*1.5),s,r["fonte"])]); n+=1
        except Exception as e: rep.append([f,"ERRORE",str(e)[:80]])
        time.sleep(0.25)
    if n and n%70==0: push(); print("push",n,flush=True)
push()
os.makedirs("reports/manga-upgrade",exist_ok=True)
with open("reports/manga-upgrade/applied-%d-%d.csv"%(START,START+COUNT),"w",newline="",encoding="utf8") as fh:
    w=csv.writer(fh); w.writerow(["file","esito","dettaglio"]); w.writerows(rep)
subprocess.run(["git","add","reports/manga-upgrade"]); subprocess.run(["git","commit","-m","report sostituzione manga"])
for i in range(5):
    if subprocess.run("git pull --rebase && git push",shell=True).returncode==0: break
    time.sleep(8)
import collections; print(collections.Counter(x[1] for x in rep))
