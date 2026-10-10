import os,re,sys,io,json,gzip,csv,time,unicodedata,difflib,html,requests
sys.path.insert(0,'scripts')
import importlib.util
sp=importlib.util.spec_from_file_location('ex','scripts/extract-raw.py'); ex=importlib.util.module_from_spec(sp); sp.loader.exec_module(ex)
SEC=sys.argv[1]; K=os.environ.get('TMDB_KEY','2dca580c2a14b55200e784d157207b4d'); TB='https://api.themoviedb.org/3'
S=requests.Session(); S.headers['User-Agent']='MediaVault-verify/1.0'
RAW=ex.extract(); os.makedirs('data/verify',exist_ok=True)
def norm(s):
    s=unicodedata.normalize('NFKD',html.unescape(s or '')).encode('ascii','ignore').decode().lower()
    s=re.sub(r'\b(the|il|lo|la|le|i|gli|l|un|una|a|an)\b',' ',s)
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',s)).strip()
def sim(a,b): return difflib.SequenceMatcher(None,norm(a),norm(b)).ratio()
def J(u,p=None,tries=4,wait=1.0):
    for i in range(tries):
        try:
            r=S.get(u,params=p,timeout=40)
            if r.status_code==200: return r.json()
            if r.status_code in (404,): return None
            time.sleep(wait*(i+2))
        except Exception: time.sleep(wait*(i+2))
def tm(path,**q):
    q['api_key']=K; return J(TB+path,q,wait=0.5)
def best(query,cands,get_titles,year=None,gy=None):
    sc=[]
    for c in cands:
        s=max([sim(query,t) for t in get_titles(c) if t] or [0])
        if year and gy and gy(c) and abs(gy(c)-year)<=1: s+=0.15
        sc.append((s,c))
    sc.sort(key=lambda x:-x[0]); return sc
def imdb_load(need_basic,need_eps=False):
    """stream IMDb datasets for needed tconsts"""
    basics={};eps={}
    r=requests.get('https://datasets.imdbws.com/title.basics.tsv.gz',stream=True,timeout=300)
    with gzip.open(r.raw,'rt',encoding='utf8') as f:
        rd=csv.reader(f,delimiter='\t'); next(rd)
        for row in rd:
            if row[0] in need_basic: basics[row[0]]=dict(type=row[1],title=row[2],year=row[5],end=row[6],runtime=row[7],genres=row[8])
    if need_eps:
        r=requests.get('https://datasets.imdbws.com/title.episode.tsv.gz',stream=True,timeout=300)
        with gzip.open(r.raw,'rt',encoding='utf8') as f:
            rd=csv.reader(f,delimiter='\t'); next(rd)
            for row in rd:
                if row[1] in need_basic:
                    e=eps.setdefault(row[1],dict(n=0,seasons=set())); e['n']+=1
                    if row[2]!='\\N': e['seasons'].add(row[2])
    for k,v in eps.items(): v['seasons']=len(v['seasons'])
    return basics,eps
def toint(x):
    try: return int(x)
    except Exception: return None
out=[]
# ---------------- FILMS ----------------
if SEC=='films':
    years={}
    for fn in os.listdir('covers/film'):
        m=re.match(r'^film_(.+?)_(\d{4})\.jpg$',fn)
        if m: years[m.group(1)]=int(m.group(2))
    def slug(s): return re.sub(r'[^a-z0-9]+','_',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('_')
    for fid,title,st,rt,dur in RAW['FILMS_RAW']:
        y=years.get(slug(title)); rec=dict(id=fid,title=title,ours=dict(duration=dur,cover_year=y),flags=[],src={})
        res=None
        for lang in ('it-IT','en-US'):
            q=dict(query=title,language=lang,include_adult='false')
            if y: q['year']=y
            res=tm('/search/movie',**q)
            if res and res.get('results'): break
            if y: 
                q.pop('year'); res=tm('/search/movie',**q)
                if res and res.get('results'): break
        cands=(res or {}).get('results',[])[:8]
        sc=best(title,cands,lambda c:[c.get('title'),c.get('original_title')],y,lambda c:toint((c.get('release_date') or '0')[:4]))
        if not sc or sc[0][0]<0.6: rec['flags'].append(('NON_TROVATO','Nessun film TMDB corrisponde al titolo')); out.append(rec); continue
        c=sc[0][1]; d=tm(f"/movie/{c['id']}",language='it-IT',append_to_response='external_ids,credits')
        if not d: out.append(rec); continue
        ry=toint((d.get('release_date') or '0')[:4])
        rec['src']['tmdb']=dict(id=d['id'],title=d.get('title'),orig=d.get('original_title'),year=ry,runtime=d.get('runtime'),imdb=d['external_ids'].get('imdb_id'),genres=[g['name'] for g in d.get('genres',[])],director=[x['name'] for x in d.get('credits',{}).get('crew',[]) if x['job']=='Director'][:3])
        rec['match_score']=round(sc[0][0],2)
        if len(sc)>1 and sc[1][0]>=sc[0][0]-0.02 and not y: rec['flags'].append(('AMBIGUO','Più film con lo stesso titolo: '+', '.join(f"{x[1].get('title')} ({(x[1].get('release_date') or '')[:4]})" for x in sc[:3])))
        if y and ry and abs(y-ry)>1: rec['flags'].append(('ANNO',f"Anno copertina {y} ≠ TMDB {ry}"))
        out.append(rec); time.sleep(0.05)
    need={r['src']['tmdb']['imdb'] for r in out if r['src'].get('tmdb',{}).get('imdb')}
    basics,_=imdb_load(need)
    for r in out:
        t=r['src'].get('tmdb')
        if not t: continue
        b=basics.get(t['imdb'])
        if b: r['src']['imdb']=dict(id=t['imdb'],title=b['title'],year=toint(b['year']),runtime=toint(b['runtime']),genres=b['genres'])
        d=r['ours']['duration']; tr=t.get('runtime'); ir=(r['src'].get('imdb') or {}).get('runtime')
        vals=[v for v in (tr,ir) if v]
        if d and vals:
            if all(abs(d-v)>3 for v in vals):
                good=ir if (tr and ir and abs(tr-ir)<=2) else tr or ir
                r['flags'].append(('DURATA',f"Nostro {d} min; TMDB {tr}, IMDb {ir} → proposta {good}"))
        if b and t['year'] and toint(b['year']) and abs(toint(b['year'])-t['year'])>1: r['flags'].append(('ANNO',f"TMDB {t['year']} ≠ IMDb {b['year']}"))
# ---------------- SERIES ----------------
elif SEC=='series':
    for sid,title,st,rt,te,am,ew,note in RAW['SERIES_RAW']:
        rec=dict(id=sid,title=title,ours=dict(totalEps=te,avgMin=am,epsWatched=ew,status=st,note=note),flags=[],src={})
        if st=='completed' and ew is not None and te and ew!=te: rec['flags'].append(('COERENZA',f"Completata ma guardati {ew}/{te} episodi"))
        if ew and te and ew>te: rec['flags'].append(('COERENZA',f"Episodi guardati {ew} > totali {te}"))
        res=tm('/search/tv',query=title,language='it-IT') or {}
        cands=res.get('results',[])[:8]
        sc=best(title,cands,lambda c:[c.get('name'),c.get('original_name')])
        if not sc or sc[0][0]<0.6: rec['flags'].append(('NON_TROVATO','Nessuna serie TMDB corrisponde')); out.append(rec); continue
        c=sc[0][1]; d=tm(f"/tv/{c['id']}",language='it-IT',append_to_response='external_ids') or {}
        rec['src']['tmdb']=dict(id=c['id'],name=d.get('name'),year=toint((d.get('first_air_date') or '0')[:4]),eps=d.get('number_of_episodes'),seasons=d.get('number_of_seasons'),runtime=d.get('episode_run_time'),status=d.get('status'),imdb=(d.get('external_ids') or {}).get('imdb_id'),genres=[g['name'] for g in d.get('genres',[])])
        if len(sc)>1 and sc[1][0]>=sc[0][0]-0.02: rec['flags'].append(('AMBIGUO','Più serie simili: '+', '.join(f"{x[1].get('name')} ({(x[1].get('first_air_date') or '')[:4]})" for x in sc[:3])))
        out.append(rec); time.sleep(0.05)
    need={r['src']['tmdb']['imdb'] for r in out if r['src'].get('tmdb',{}).get('imdb')}
    basics,eps=imdb_load(need,True)
    for r in out:
        t=r['src'].get('tmdb')
        if not t: continue
        i=t['imdb']; b=basics.get(i); e=eps.get(i)
        r['src']['imdb']=dict(id=i,runtime=toint(b['runtime']) if b else None,eps=e['n'] if e else None,seasons=e['seasons'] if e else None,year=b and b['year'],end=b and b['end'])
        te=r['ours']['totalEps']; vals=[v for v in (t.get('eps'),(e or {}).get('n')) if v]
        ongoing=(t.get('status') or '') in ('Returning Series','In Production')
        if te and vals and all(abs(te-v)>0 for v in vals):
            agree=len(vals)==2 and vals[0]==vals[1]
            r['flags'].append(('EPISODI',f"Nostro {te}; TMDB {t.get('eps')}, IMDb {(e or {}).get('n')}"+(' (serie in corso: può essere solo aggiornamento)' if ongoing else '')+(f" → proposta {vals[0]}" if agree else '')))
        am=r['ours']['avgMin']; rts=(t.get('runtime') or [])+([toint(b['runtime'])] if b and toint(b['runtime']) else [])
        if am and rts and all(abs(am-v)>5 for v in rts): r['flags'].append(('MINUTAGGIO',f"Nostro {am} min; TMDB {t.get('runtime')}, IMDb {b and b['runtime']}"))
# ---------------- ANIME ----------------
elif SEC=='anime':
    man=json.load(open('covers/anime/_manifest.json'))
    for aid,title,st,rt,te,ew,dur in RAW['ANIME_RAW']:
        rec=dict(id=aid,title=title,ours=dict(totalEps=te,epsWatched=ew,duration=dur,status=st),flags=[],src={})
        if st=='completed' and ew is not None and te and ew!=te: rec['flags'].append(('COERENZA',f"Completato ma guardati {ew}/{te}"))
        if ew and te and ew>te: rec['flags'].append(('COERENZA',f"Guardati {ew} > totali {te}"))
        mal=(man.get(aid) or {}).get('mal')
        if mal:
            time.sleep(0.5); j=(J(f'https://api.jikan.moe/v4/anime/{mal}') or {}).get('data')
            if j:
                m=re.search(r'(\d+)\s*min',j.get('duration') or ''); h=re.search(r'(\d+)\s*hr',j.get('duration') or '')
                dmin=(int(h.group(1))*60 if h else 0)+(int(m.group(1)) if m else 0) or None
                rec['src']['jikan']=dict(mal=mal,title=j['title'],type=j.get('type'),eps=j.get('episodes'),duration=dmin,year=j.get('year') or (j.get('aired',{}).get('prop',{}).get('from',{}) or {}).get('year'),status=j.get('status'),genres=[g['name'] for g in j.get('genres',[])])
        q='''query($s:String){Page(perPage:6){media(search:$s,type:ANIME){id idMal title{romaji english native} episodes duration startDate{year} format status}}}'''
        try:
            r=S.post('https://graphql.anilist.co',json=dict(query=q,variables=dict(s=title)),timeout=40); ms=r.json()['data']['Page']['media'] if r.status_code==200 else []
        except Exception: ms=[]
        pick=next((x for x in ms if mal and x.get('idMal')==mal),None)
        if not pick and ms:
            sc=best(title,ms,lambda c:[c['title'].get('romaji'),c['title'].get('english')]); pick=sc[0][1] if sc[0][0]>=0.6 else None
        if pick: rec['src']['anilist']=dict(id=pick['id'],title=pick['title'].get('romaji'),eps=pick.get('episodes'),duration=pick.get('duration'),year=(pick.get('startDate') or {}).get('year'),format=pick.get('format'),status=pick.get('status'))
        j=rec['src'].get('jikan'); a=rec['src'].get('anilist')
        if not j and not a: rec['flags'].append(('NON_TROVATO','Nessuna fonte corrisponde'))
        vals=[v for v in ((j or {}).get('eps'),(a or {}).get('eps')) if v]
        if te and vals and all(te!=v for v in vals):
            rec['flags'].append(('EPISODI',f"Nostro {te}; Jikan {(j or {}).get('eps')}, AniList {(a or {}).get('eps')} (può essere voce franchise/più stagioni)"))
        dv=[v for v in ((j or {}).get('duration'),(a or {}).get('duration')) if v]
        if dur and dv and all(abs(dur-v)>4 for v in dv): rec['flags'].append(('DURATA',f"Nostro {dur} min; Jikan {(j or {}).get('duration')}, AniList {(a or {}).get('duration')}"))
        out.append(rec); time.sleep(0.6)
# ---------------- MANGA ----------------
elif SEC=='manga':
    clog=json.load(open('data/manga-covers-log.json'))
    for mid,title,st,rt,note,tv,ppv,vo,vr,ed,vt,sp in RAW['MANGA_RAW']:
        rec=dict(id=mid,title=title,ours=dict(totalVols=tv,volsOwned=vo,volsRead=vr,edition=ed,volType=vt,price=ppv,status=st),flags=[],src={})
        if tv:
            if vo and vo>tv: rec['flags'].append(('COERENZA',f"Posseduti {vo} > totali {tv}"))
            if vr and vr>tv: rec['flags'].append(('COERENZA',f"Letti {vr} > totali {tv}"))
            if st=='completed' and vr is not None and vr!=tv: rec['flags'].append(('COERENZA',f"Completato ma letti {vr}/{tv}"))
        cl=clog.get(mid)
        if cl: rec['src']['animeclick']=dict(groups=cl.get('groups'),chosen=cl.get('chosen'),expected=cl.get('expected'))
        time.sleep(0.5); res=(J('https://api.jikan.moe/v4/manga',dict(q=title,limit=6)) or {}).get('data',[])
        sc=best(title,res,lambda c:[c.get('title'),c.get('title_english')]+[t['title'] for t in c.get('titles',[])])
        if sc and sc[0][0]>=0.75:
            c=sc[0][1]; rec['src']['jikan']=dict(mal=c['mal_id'],title=c['title'],volumes=c.get('volumes'),chapters=c.get('chapters'),status=c.get('status'),year=(c.get('published',{}).get('prop',{}).get('from',{}) or {}).get('year'))
        q='''query($s:String){Page(perPage:5){media(search:$s,type:MANGA){id title{romaji english} volumes chapters startDate{year} status}}}'''
        try:
            r=S.post('https://graphql.anilist.co',json=dict(query=q,variables=dict(s=title)),timeout=40); ms=r.json()['data']['Page']['media'] if r.status_code==200 else []
        except Exception: ms=[]
        sa=best(title,ms,lambda c:[c['title'].get('romaji'),c['title'].get('english')]) if ms else []
        if sa and sa[0][0]>=0.75:
            c=sa[0][1]; rec['src']['anilist']=dict(id=c['id'],title=c['title'].get('romaji'),volumes=c.get('volumes'),chapters=c.get('chapters'),status=c.get('status'),year=(c.get('startDate') or {}).get('year'))
        j=rec['src'].get('jikan'); a=rec['src'].get('anilist'); ac=rec['src'].get('animeclick')
        if not j and not a: rec['flags'].append(('NON_TROVATO','Nessuna fonte giapponese (titolo italiano?) — verificare con AnimeClick/editore'))
        jv=[v for v in ((j or {}).get('volumes'),(a or {}).get('volumes')) if v]
        if tv and jv and all(tv!=v for v in jv) and not ed:
            rec['flags'].append(('VOLUMI',f"Nostro {tv}; Jikan {(j or {}).get('volumes')}, AniList {(a or {}).get('volumes')}"+(f", AnimeClick edizione scelta {ac['expected']}" if ac else '')))
        if tv and ac and ac.get('expected') and ac['expected']!=tv: rec['flags'].append(('VOLUMI_IT',f"Nostro {tv}; AnimeClick edizione '{ac['chosen']}' indica {ac['expected']}"+(' — verificare' )))
        out.append(rec)
json.dump(out,open(f'data/verify/{SEC}.json','w'),ensure_ascii=False,indent=1,default=list)
print(SEC,len(out),'con flag:',sum(1 for r in out if r['flags']))
