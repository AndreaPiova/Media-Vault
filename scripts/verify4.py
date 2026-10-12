import os,re,sys,io,json,glob,time,unicodedata,difflib,html,requests
SEC=sys.argv[1]
K='2dca580c2a14b55200e784d157207b4d'; TB='https://api.themoviedb.org/3'; IMG='https://image.tmdb.org/t/p/w185'
D=json.load(open('data/v43.json')); S=requests.Session(); S.headers['User-Agent']='MediaVault-verify4/1.0'
os.makedirs('data/verify4',exist_ok=True)
GI={'Action':'Azione','Adventure':'Avventura','Animation':'Animazione','Comedy':'Commedia','Crime':'Crimine','Documentary':'Documentario','Drama':'Dramma','Family':'Famiglia','Fantasy':'Fantasy','History':'Storico','Horror':'Horror','Music':'Musica','Mystery':'Mistero','Romance':'Romance','Science Fiction':'Fantascienza','TV Movie':'Film TV','Thriller':'Thriller','War':'Guerra','Western':'Western','Action & Adventure':'Azione, Avventura','Sci-Fi & Fantasy':'Fantascienza, Fantasy','War & Politics':'Guerra','Kids':'Bambini','Reality':'Reality','Soap':'Soap','Talk':'Talk'}
def norm(s):
    s=unicodedata.normalize('NFKD',html.unescape(s or '')).encode('ascii','ignore').decode().lower()
    return re.sub(r'\s+',' ',re.sub(r'[^a-z0-9 ]+',' ',s)).strip()
def sim(a,b): return difflib.SequenceMatcher(None,norm(a),norm(b)).ratio()
def latin(n): return bool(n) and all(ord(c)<0x250 for c in n)
def tm(path,**q):
    q['api_key']=K
    for i in range(4):
        try:
            r=S.get(TB+path,params=q,timeout=40)
            if r.status_code==200: return r.json()
            if r.status_code==404: return None
        except Exception: pass
        time.sleep(1+i)
def load(p):
    r=[]
    for f in sorted(glob.glob(p)): r+=json.load(open(f))
    return r
LAST=[0]
def AL(q,v):
    for i in range(6):
        w=0.9-(time.time()-LAST[0])
        if w>0: time.sleep(w)
        LAST[0]=time.time()
        try:
            r=S.post('https://graphql.anilist.co',json=dict(query=q,variables=v),timeout=40)
            if r.status_code==200: return r.json().get('data')
            if r.status_code==404: return None
            time.sleep(int(r.headers.get('Retry-After','8')) if r.status_code==429 else 4)
        except Exception: time.sleep(4)
out=[]
if SEC=='films':
    fix={x['id']:x for x in load('data/verify2/films_fix_*.json')}
    for x in [fix.get(x['id'],x) for x in load('data/verify2/films_[0-9].json')]:
        fl=[f[0] for f in x['flags']]
        if not set(fl)&{'CAST','GENERI','FOTO_CAST'}: continue
        tid=x['ours'].get('tmdb'); d=tm(f'/movie/{tid}',append_to_response='credits',language='it-IT') if tid else None
        if not d: continue
        cast=[c for c in d['credits']['cast'][:30] if latin(c['name'])][:6]
        rec=dict(id=x['id'],title=x['title'],tmdb=tid,flags=x['flags'],cast_nostro=x['ours'].get('cast'),
                 cast_tmdb=[dict(nome=c['name'],personaggio=c.get('character'),foto=(IMG+c['profile_path']) if c.get('profile_path') else None) for c in cast],
                 generi_tmdb=[GI.get(g['name'],g['name']) for g in d.get('genres',[])],generi_nostri=x['ours'].get('genres'))
        ph=D['FILM_CAST_PHOTOS'].get(x['id']) or {}; rec['foto_nostre']=ph
        out.append(rec)
elif SEC=='series':
    for x in load('data/verify2/series_*.json'):
        fl=[f[0] for f in x['flags']]
        if not set(fl)&{'CAST','GENERI','FOTO_CAST','PERSONAGGIO'}: continue
        tid=x['ours'].get('tmdb'); d=tm(f'/tv/{tid}',append_to_response='aggregate_credits',language='it-IT') if tid else None
        if not d: continue
        ac=[c for c in d['aggregate_credits']['cast'][:30] if latin(c['name'])][:8]
        out.append(dict(id=x['id'],title=x['title'],tmdb=tid,flags=x['flags'],
            cast_tmdb=[dict(nome=c['name'],personaggio=(c.get('roles') or [{}])[0].get('character'),foto=(IMG+c['profile_path']) if c.get('profile_path') else None) for c in ac],
            generi_tmdb=[GI.get(g['name'],g['name']) for g in d.get('genres',[])],generi_nostri=x['ours'].get('genres'),
            cast_nostro=D['SERIES_CREDITS'].get(x['id'])))
elif SEC=='anime':
    Q='query($s:String,$p:Int){Media(search:$s,type:ANIME){id characters(perPage:25,page:$p,sort:[ROLE,RELEVANCE]){pageInfo{hasNextPage} nodes{id name{full native} image{large}}}}}'
    for x in load('data/verify3/anime_*.json'):
        miss=[]
        for f in x['flags']:
            if f[0]=='FOTO_MANCANTE': miss+=re.findall(r"'([^']+)'",f[1])
            if f[0]=='FOTO_PERSONAGGIO': miss+=[m.strip() for m in re.findall(r'(?:^|;\s*)([^;(]+?) \(foto',f[1])]
        if not miss: continue
        al=x['src'].get('anilist') or {}; s=al.get('title') or x['title']; nodes=[]
        for p in (1,2,3,4):
            r=AL(Q,dict(s=s,p=p)); m=(r or {}).get('Media')
            if not m: break
            nodes+=m['characters']['nodes']
            if not m['characters']['pageInfo']['hasNextPage']: break
        res=[]
        for n in miss:
            best=max(nodes,key=lambda c:sim(n,c['name']['full']),default=None)
            ok=best and sim(n,best['name']['full'])>=0.7
            res.append(dict(personaggio=n,anilist_nome=best['name']['full'] if ok else None,foto=best['image']['large'] if ok else None,anilist_char_id=best['id'] if ok else None))
        out.append(dict(id=x['id'],title=x['title'],proposte=res))
elif SEC=='manga':
    Q='query($s:String){Media(search:$s,type:MANGA){id title{romaji english} chapters volumes staff(perPage:12){edges{role node{name{full}}}}}}'
    def mdx(title):
        try:
            r=S.get('https://api.mangadex.org/manga',params={'title':title,'limit':5},timeout=40).json().get('data',[])
        except Exception: return None
        for m in r:
            names=list(m['attributes']['title'].values())+[v for a in m['attributes'].get('altTitles',[]) for v in a.values()]
            if max(sim(title,n) for n in names)>=0.85: return m['id']
    for x in load('data/verify3/manga_*.json'):
        keys={f[0] for f in x['flags']}
        if not keys&{'CAPITOLI','CAPITOLI?','CAPITOLI_SOSPETTI','CAPITOLI_MANCANTI','AUTORI','VOLUMI_INTERNI'}: continue
        al=x['src'].get('anilist') or {}; t=al.get('title') or x['title']
        rec=dict(id=x['id'],title=x['title'],flags=x['flags'],nostro=x['ours'])
        r=AL(Q,dict(s=t)); m=(r or {}).get('Media')
        if m: rec['anilist']=dict(capitoli=m['chapters'],volumi=m['volumes'],autori=[f"{e['node']['name']['full']} ({e['role']})" for e in m['staff']['edges']])
        mid=mdx(t) or mdx(x['title'])
        if mid:
            try:
                ag=S.get(f'https://api.mangadex.org/manga/{mid}/aggregate',timeout=40).json().get('volumes',{})
                vols={}
                for v,dv in ag.items():
                    vols[v]=len(dv['chapters'])
                rec['mangadex_capitoli_per_volume']={k:vols[k] for k in sorted(vols,key=lambda z:(z=='none',float(z) if z!='none' else 0))}
            except Exception as e: rec['mangadex_err']=str(e)
        out.append(rec)
json.dump(out,open(f'data/verify4/{SEC}.json','w'),ensure_ascii=False,indent=1)
print(SEC,len(out))
