import os,re,sys,io,json,gzip,csv,time,unicodedata,difflib,html,requests,hashlib
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
SEC=sys.argv[1]; SH=sys.argv[2] if len(sys.argv)>2 else '0/1'; si,sn=map(int,SH.split('/'))
K='2dca580c2a14b55200e784d157207b4d'; TB='https://api.themoviedb.org/3'; IMG='https://image.tmdb.org/t/p/w185'
D=json.load(open('data/v43.json')); S=requests.Session(); S.headers['User-Agent']='MediaVault-verify2/1.0'
os.makedirs('data/verify2',exist_ok=True)
def norm(s):
    s=unicodedata.normalize('NFKD',html.unescape(s or '')).encode('ascii','ignore').decode().lower()
    s=re.sub(r"\b(the|il|lo|la|le|i|gli|l|un|una|a|an)\b",' ',s)
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',s)).strip()
def sim(a,b): return difflib.SequenceMatcher(None,norm(a),norm(b)).ratio()
def tm(path,**q):
    q['api_key']=K
    for i in range(4):
        try:
            r=S.get(TB+path,params=q,timeout=40)
            if r.status_code==200: return r.json()
            if r.status_code==404: return None
        except Exception: pass
        time.sleep(1+i)
def getimg(u):
    for i in range(3):
        try:
            r=S.get(u,timeout=40)
            if r.status_code==200: return Image.open(io.BytesIO(r.content)).convert('L')
        except Exception: pass
        time.sleep(1)
def dh(im):
    im=im.resize((9,8)); p=list(im.getdata()); b=0
    for y in range(8):
        for x in range(8): b=(b<<1)|(1 if p[y*9+x]>p[y*9+x+1] else 0)
    return b
def dist(a,b): return bin(a^b).count('1')
def hash_url(u):
    im=getimg(u); return dh(im) if im else None
def toint(x):
    try: return int(x)
    except Exception: return None
def person_match(n,names):
    best=max([(sim(n,m),m) for m in names] or [(0,None)]); return best
def imdb_load(need,eps=False):
    basics={};cnt={}
    r=requests.get('https://datasets.imdbws.com/title.basics.tsv.gz',stream=True,timeout=300)
    with gzip.open(r.raw,'rt',encoding='utf8') as f:
        rd=csv.reader(f,delimiter='\t'); next(rd)
        for row in rd:
            if row[0] in need: basics[row[0]]=dict(year=toint(row[5]),end=toint(row[6]),runtime=toint(row[7]))
    if eps:
        r=requests.get('https://datasets.imdbws.com/title.episode.tsv.gz',stream=True,timeout=300)
        with gzip.open(r.raw,'rt',encoding='utf8') as f:
            rd=csv.reader(f,delimiter='\t'); next(rd)
            for row in rd:
                if row[1] in need: cnt[row[1]]=cnt.get(row[1],0)+1
    return basics,cnt
GENRE_IT={'Action':'Azione','Adventure':'Avventura','Animation':'Animazione','Comedy':'Commedia','Crime':'Crimine','Documentary':'Documentario','Drama':'Dramma','Family':'Famiglia','Fantasy':'Fantasy','History':'Storia','Horror':'Horror','Music':'Musica','Mystery':'Mistero','Romance':'Romantico','Science Fiction':'Fantascienza','Thriller':'Thriller','War':'Guerra','Western':'Western'}
def poster_check(ours_url,tm_imgs):
    """ritorna (min distanza, hash_cover)"""
    if not ours_url: return None,None
    hc=hash_url(re.sub(r'\?.*$','',ours_url)+'')
    if hc is None: return None,None
    hs=[]
    with ThreadPoolExecutor(8) as ex: hs=[h for h in ex.map(hash_url,tm_imgs) if h is not None]
    return (min(dist(hc,h) for h in hs) if hs else None),hc
def imgs_of(d,n=14):
    im=d.get('images') or {}; out=[]
    for k in ('posters','backdrops'):
        l=sorted(im.get(k,[]),key=lambda x:-(x.get('vote_count') or 0))[:n if k=='posters' else 8]
        out+=[IMG+x['file_path'] for x in l]
    return out
def identify(title,alts,year,hc,kind):
    """cerca tra i candidati TMDB quello il cui poster/backdrop assomiglia alla copertina"""
    seen={}
    for t in [title]+list(alts)[:3]:
        for lang in ('it-IT','en-US'):
            for c in (tm(f'/search/{kind}',query=t,language=lang) or {}).get('results',[])[:6]: seen[c['id']]=c
    best=[]
    for cid,c in list(seen.items())[:12]:
        d=tm(f'/{kind}/{cid}',append_to_response='images',include_image_language='it,en,null') or {}
        urls=imgs_of(d,8)
        with ThreadPoolExecutor(8) as ex: hs=[h for h in ex.map(hash_url,urls) if h is not None]
        if hs: best.append((min(dist(hc,h) for h in hs),cid,(d.get('title') or d.get('name')),((d.get('release_date') or d.get('first_air_date') or '')[:4])))
    best.sort(); return best[:3]
out=[]
if SEC=='films':
    rows=[r for i,r in enumerate(D['FILMS_RAW']) if i%sn==si]; 
    for r in rows:
        fid,title,st,rt,dur,year,trama,director,castS,genres=r; ids=D['MANUAL_TMDB_FILM_ID'].get(fid)
        rec=dict(id=fid,title=title,ours=dict(year=year,duration=dur,director=director,cast=castS,genres=genres,tmdb=ids),flags=[],src={})
        if not ids: rec['flags'].append(('NO_ID','Nessun id TMDB assegnato')); out.append(rec); continue
        d=tm(f'/movie/{ids}',language='it-IT',append_to_response='credits,external_ids,images',include_image_language='it,en,null')
        if not d: rec['flags'].append(('ID_TMDB_NON_VALIDO',f'id {ids} non esiste')); out.append(rec); continue
        ry=toint((d.get('release_date') or '0')[:4]); cr=d.get('credits') or {}
        directors=[x['name'] for x in cr.get('crew',[]) if x['job']=='Director']; cast=[x['name'] for x in cr.get('cast',[])[:25]]
        rec['src']['tmdb']=dict(title=d.get('title'),orig=d.get('original_title'),year=ry,runtime=d.get('runtime'),imdb=d['external_ids'].get('imdb_id'),directors=directors[:3],genres=[g['name'] for g in d.get('genres',[])],cast5=cast[:6])
        names=[d.get('title'),d.get('original_title')]+D['ALT_TITLES'].get(fid,[])
        if max(sim(title,n) for n in names if n)<0.6: rec['flags'].append(('TITOLO',f"'{title}' ≠ TMDB '{d.get('title')}' / '{d.get('original_title')}'"))
        if year and ry and abs(toint(year)-ry)>=1: rec['flags'].append(('ANNO',f"Nostro {year}; TMDB {ry}"))
        if director and directors and not any(sim(x.strip(),y)>=0.8 for x in re.split(r',|&| e ',director) for y in directors): rec['flags'].append(('REGISTA',f"Nostro '{director}'; TMDB {directors[:3]}"))
        al=D['FILM_CAST_ALIASES'].get(fid,{})
        miss=[]
        for n in [x.strip() for x in (castS or '').split(',') if x.strip()]:
            n2=al.get(n,n); s,m=person_match(n2,cast)
            if s<0.8: miss.append(n)
        if miss: rec['flags'].append(('CAST',f"Non nel cast TMDB (top25): {miss}; TMDB top: {cast[:6]}"))
        tg=[GENRE_IT.get(g['name'],g['name']) for g in d.get('genres',[])]; oursg=[g for g in (genres or [])]
        if oursg and tg and not (set(norm(x) for x in oursg)&set(norm(x) for x in tg)): rec['flags'].append(('GENERI',f"Nostri {oursg}; TMDB {tg}"))
        # foto cast
        prof={x['name']:x.get('profile_path') for x in cr.get('cast',[])}
        bad=[]
        for n,u in (D['FILM_CAST_PHOTOS'].get(fid) or {}).items():
            n2=al.get(n,n); s,m=person_match(n2,list(prof))
            if s<0.8: bad.append(f"{n}: non nel cast TMDB")
            else:
                pp=prof.get(m); 
                if not pp: continue
                if pp not in u: bad.append(f"{n}: foto diversa da TMDB")
        if bad: rec['flags'].append(('FOTO_CAST','; '.join(bad[:6])))
        # poster
        cover=D['MANUAL_COVERS_FILM'].get(fid); back=D['MANUAL_BACKDROPS_FILM'].get(fid)
        dm,hc=poster_check(cover,imgs_of(d))
        rec['src']['poster_dist']=dm
        if dm is not None and dm>16:
            idn=identify(title,names,year,hc,'movie') if hc is not None else []
            rec['flags'].append(('POSTER',f"Copertina non corrisponde ai poster TMDB id {ids} ({d.get('title')} {ry}), distanza {dm}. Candidati per somiglianza: {idn}"))
        out.append(rec)
    need={r['src']['tmdb']['imdb'] for r in out if r['src'].get('tmdb',{}).get('imdb')}
    basics,_=imdb_load(need)
    for r in out:
        t=r['src'].get('tmdb')
        if not t: continue
        b=basics.get(t['imdb']); 
        if b: r['src']['imdb']=b
        dur=r['ours']['duration']; vals=[v for v in (t.get('runtime'),(b or {}).get('runtime')) if v]
        if dur and vals and all(abs(dur-v)>3 for v in vals):
            agree=len(vals)==2 and abs(vals[0]-vals[1])<=2
            r['flags'].append(('DURATA' if agree else 'DURATA?',f"Nostro {dur} min; TMDB {t.get('runtime')}, IMDb {(b or {}).get('runtime')}"))
        y=toint(r['ours']['year'])
        if b and b.get('year') and t.get('year') and abs(b['year']-t['year'])>=1: r['flags'].append(('ANNO_FONTI',f"TMDB {t['year']} ≠ IMDb {b['year']} (nostro {y})"))
elif SEC=='series':
    for r in D['SERIES_RAW']:
        sid,title,st,rt,te,am,ew,note,y0,y1,seasons=r[:11]; castS=r[11] if len(r)>11 else ''; ids=D['MANUAL_TMDB_SERIES_ID'].get(sid)
        ov=D['SERIES_MANUAL_OVERRIDES'].get(sid,{}); cred=D['SERIES_CREDITS'].get(sid,{})
        rec=dict(id=sid,title=title,ours=dict(totalEps=te,avgMin=am,epsWatched=ew,y0=y0,y1=y1,seasons=seasons,tmdb=ids,creators=cred.get('creators')),flags=[],src={})
        if st=='completed' and te and ew!=te: rec['flags'].append(('COERENZA',f"Completata ma visti {ew}/{te}"))
        if seasons and te and sum(seasons)!=te: rec['flags'].append(('COERENZA',f"Somma episodi stagioni {sum(seasons)} ≠ totale {te}"))
        if not ids: rec['flags'].append(('NO_ID','Nessun id TMDB')); out.append(rec); continue
        d=tm(f'/tv/{ids}',language='it-IT',append_to_response='aggregate_credits,external_ids,images',include_image_language='it,en,null')
        if not d: rec['flags'].append(('ID_TMDB_NON_VALIDO',f'id {ids}')); out.append(rec); continue
        fy=toint((d.get('first_air_date') or '0')[:4]); ly=toint((d.get('last_air_date') or '0')[:4]); ended=d.get('status') in ('Ended','Canceled')
        sc=[(s['season_number'],s['episode_count']) for s in d.get('seasons',[]) if s['season_number']>0]
        rec['src']['tmdb']=dict(name=d.get('name'),orig=d.get('original_name'),first=fy,last=ly,status=d.get('status'),eps=d.get('number_of_episodes'),seasons=[c for _,c in sc],creators=[x['name'] for x in d.get('created_by',[])],imdb=d['external_ids'].get('imdb_id'))
        if max(sim(title,n) for n in (d.get('name'),d.get('original_name')) if n)<0.6: rec['flags'].append(('TITOLO',f"'{title}' ≠ '{d.get('name')}'/'{d.get('original_name')}'"))
        if y0 and fy and abs(toint(y0)-fy)>=1: rec['flags'].append(('ANNO_INIZIO',f"Nostro {y0}; TMDB {fy}"))
        if y1 and ly and ended and abs(toint(y1)-ly)>=1: rec['flags'].append(('ANNO_FINE',f"Nostro {y1}; TMDB {ly} (serie {d.get('status')})"))
        if seasons and sc and [c for _,c in sc]!=seasons: rec['flags'].append(('EPISODI_STAGIONE',f"Nostro {seasons}; TMDB {[c for _,c in sc]}"+('' if ended else ' (serie in corso)')))
        elif te and d.get('number_of_episodes') and te!=d['number_of_episodes']: rec['flags'].append(('EPISODI',f"Nostro {te}; TMDB {d['number_of_episodes']}"))
        if cred.get('creators') and rec['src']['tmdb']['creators'] and not any(sim(a,b)>=0.8 for a in cred['creators'] for b in rec['src']['tmdb']['creators']): rec['flags'].append(('CREATORI',f"Nostri {cred['creators']}; TMDB {rec['src']['tmdb']['creators']}"))
        tg=[GENRE_IT.get(g['name'],g['name']) for g in d.get('genres',[])]; og=ov.get('genres') or []
        if og and tg and not (set(norm(x) for x in og)&set(norm(x) for x in tg)): rec['flags'].append(('GENERI',f"Nostri {og}; TMDB {tg}"))
        ac=(d.get('aggregate_credits') or {}).get('cast',[])[:30]; an=[x['name'] for x in ac]; pr={x['name']:x.get('profile_path') for x in ac}
        miss=[];badp=[];badc=[]
        for c in ov.get('cast',[]):
            s,m=person_match(c['name'],an)
            if s<0.8: miss.append(c['name']); continue
            pp=pr.get(m)
            if pp and c.get('img') and pp not in c['img']: badp.append(c['name'])
            roles=[x['character'] for x in ac if x['name']==m for x in x.get('roles',[])] if False else [rl['character'] for x0 in ac if x0['name']==m for rl in x0.get('roles',[])]
            if c.get('character') and roles and not any(sim(c['character'],q)>=0.6 or norm(c['character']) in norm(q) or norm(q) in norm(c['character']) for q in roles): badc.append(f"{c['name']}: '{c['character']}' vs {roles[:3]}")
        if miss: rec['flags'].append(('CAST',f"Non nel cast TMDB: {miss}; TMDB top: {an[:8]}"))
        if badp: rec['flags'].append(('FOTO_CAST',f"Foto diversa da TMDB: {badp}"))
        if badc: rec['flags'].append(('PERSONAGGIO',f"{badc[:5]}"))
        cover=D['MANUAL_COVERS_SERIE'].get(sid); dm,hc=poster_check(cover,imgs_of(d)); rec['src']['poster_dist']=dm
        if dm is not None and dm>16:
            idn=identify(title,[d.get('name')],y0,hc,'tv') if hc is not None else []
            rec['flags'].append(('POSTER',f"Copertina non corrisponde ai poster TMDB id {ids} ({d.get('name')} {fy}), distanza {dm}. Candidati: {idn}"))
        out.append(rec)
    need={r['src']['tmdb']['imdb'] for r in out if r['src'].get('tmdb',{}).get('imdb')}
    basics,cnt=imdb_load(need,True)
    for r in out:
        t=r['src'].get('tmdb')
        if not t: continue
        b=basics.get(t['imdb']); c=cnt.get(t['imdb']); r['src']['imdb']=dict(year=(b or {}).get('year'),end=(b or {}).get('end'),eps=c)
        te=r['ours']['totalEps']
        if te and t.get('eps') and c and te!=t['eps'] and te!=c and not any(f[0]=='EPISODI' for f in r['flags']) : r['flags'].append(('EPISODI?',f"Nostro {te}; TMDB {t['eps']}, IMDb {c}"))
        y0=toint(r['ours']['y0'])
        if b and b.get('year') and y0 and abs(b['year']-y0)>=1 and t.get('first') and abs(b['year']-t['first'])>=1: r['flags'].append(('ANNO_FONTI',f"Nostro {y0}; TMDB {t['first']}; IMDb {b['year']}"))
json.dump(out,open(f'data/verify2/{SEC}_{si}.json','w'),ensure_ascii=False,indent=1,default=list)
print(SEC,si,len(out),'con flag',sum(1 for r in out if r['flags']))
