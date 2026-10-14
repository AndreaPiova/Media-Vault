#!/usr/bin/env python3
import os, io, json, time, subprocess, requests, urllib.parse as up
from PIL import Image
OUT='data/lowfix2'; os.makedirs(OUT,exist_ok=True)
B='https://www.animeclick.it/images/Manga_Cover/'
U={}
for n,f in {12:'MPDPsycho12',13:'MPDPsycho13',14:'MPDPsycho14',15:'MPDPsycho15',16:'MPDPsycho16',17:'MPDPsycho17',18:'MPDPsycho18',19:'MPDPsycho19',20:'MPDPsycho20',21:'MPDPsycho21',22:'mpdpsycho22c'}.items(): U[('mpd_psycho',n)]=B+f+'.jpg'
U[('mpd_psycho',23)]='https://www.animeclick.it/immagini/manga/MPD_Psycho/edizioni/MPD%20Psycho-edizione-3071616.jpg'
U[('mpd_psycho',24)]='https://www.animeclick.it/immagini/manga/MPD_Psycho/edizioni/MPD%20Psycho-edizione-3071869.jpg'
for n in (1,3,4,8,9): U[('mushishi',n)]=B+('Mushishi1' if n==1 else f'Mushishi{n:02d}')+'.jpg'
for n in (2,3,4,5,6,7,8,10,11,12,13,14,15,19): U[('tegamibachi',n)]=B+('letterbee19x' if n==19 else f'LetterBee{n:02d}')+'.jpg'
S=requests.Session(); S.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
log={}
for (k,n),u in U.items():
    try:
        r=S.get(u,timeout=30); ok=r.status_code==200 and len(r.content)>3000
        if ok:
            im=Image.open(io.BytesIO(r.content)).convert('RGB'); open(f'{OUT}/{k}_vol{n}.jpg','wb').write(r.content)
            log[f'{k}_{n}']=[u,list(im.size)]
        else: log[f'{k}_{n}']=[u,r.status_code]
    except Exception as e: log[f'{k}_{n}']=[u,str(e)]
    print(k,n,log[f'{k}_{n}'][1],flush=True); time.sleep(0.5)
json.dump(log,open('data/lowfix2-log.json','w'),indent=1)
subprocess.run(['git','add','data/lowfix2','data/lowfix2-log.json']); subprocess.run(['git','commit','-q','-m','lowfix2'])
for _ in range(12):
    subprocess.run(['git','fetch','origin','manga-publisher']); subprocess.run(['git','rebase','-X','theirs','origin/manga-publisher'])
    if subprocess.run(['git','push','origin','HEAD:manga-publisher']).returncode==0: break
    time.sleep(5)
