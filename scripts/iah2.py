import re,json,time,requests,urllib.parse as up
S=requests.Session(); S.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'; S.headers['Accept-Language']='it-IT,it;q=0.9'
out={}
def tryget(name,u):
    try:
        r=S.get(u,timeout=30); out[name]=dict(status=r.status_code,len=len(r.text),isbns=sorted(set(re.findall(r'97888\d{8}',r.text)))[:60],head=r.text[:200].replace('\n',' '))
    except Exception as e: out[name]=dict(err=str(e))
for n in (3,9,19):
    q=f'I am a hero nuova edizione {n}'; qq=up.quote_plus(q)
    tryget(f'amazon{n}',f'https://www.amazon.it/s?k={qq}')
    tryget(f'feltrinelli{n}',f'https://www.lafeltrinelli.it/cerca?query={qq}')
    tryget(f'libraccio{n}',f'https://www.libraccio.it/src/?FT={qq}')
    tryget(f'mondadori{n}',f'https://www.mondadoristore.it/search/?g={qq}')
    tryget(f'ol{n}',f'https://openlibrary.org/search.json?q={qq}&limit=20')
    tryget(f'ibs_ediz{n}',f'https://www.ibs.it/search/?ts=as&query={up.quote_plus("I am a hero. Nuova ediz. "+str(n))}')
tryget('whakoom','https://www.whakoom.com/ediciones/378578/i_am_a_hero-rustica')
tryget('animeclick','https://www.animeclick.it/manga/')
json.dump(out,open('data/iah-probe.json','w'),ensure_ascii=False,indent=1)
