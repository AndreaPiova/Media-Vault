#!/usr/bin/env python3
"""Collega ogni anime di MediaVault al suo id MAL (doppia verifica: AniList + lista MAL dell'utente)
e confronta personaggi, foto e generi con AniList. Sola lettura sul file dell'app."""
import json, re, time, sys, unicodedata, urllib.request, urllib.error
URL='https://graphql.anilist.co'
inp=json.load(open('data/anime-verify-input.json'))
USER=set(inp['user_mal_ids'])

def q(query, variables):
    body=json.dumps({'query':query,'variables':variables}).encode()
    for attempt in range(6):
        try:
            req=urllib.request.Request(URL,body,{'Content-Type':'application/json','Accept':'application/json'})
            with urllib.request.urlopen(req,timeout=30) as r:
                time.sleep(0.8); return json.load(r)['data']
        except urllib.error.HTTPError as e:
            if e.code==429:
                time.sleep(int(e.headers.get('Retry-After','30'))+2); continue
            if e.code==404: return None
            time.sleep(3)
        except Exception: time.sleep(3)
    return None

CHARS='characters(sort:[ROLE,FAVOURITES_DESC],perPage:25){edges{role node{id name{full} favourites image{large}}}}'
QID='query($m:Int){Media(idMal:$m,type:ANIME){id idMal format seasonYear episodes genres title{romaji english} description(asHtml:false) '+CHARS+'}}'
QSEARCH='query($s:String){Page(perPage:8){media(search:$s,type:ANIME,sort:SEARCH_MATCH){id idMal format seasonYear title{romaji english}}}}'

def norm(x): 
    x=unicodedata.normalize('NFD',str(x or '').lower()); x=re.sub(r'[\u0300-\u036f]','',x)
    return ' '.join(sorted(t for t in re.split(r'[^a-z0-9]+',x) if t))
def toks(x): return set(re.split(r'[^a-z0-9]+',unicodedata.normalize('NFD',str(x or '').lower()))) - {''}
def sim(a,b):
    A,B=toks(a),toks(b); 
    return len(A&B)/max(1,min(len(A),len(B)))
def tsim(title,m):
    t=m['title']; return max(sim(title,t.get('english')),sim(title,t.get('romaji')))

out_ids={}; rep=[]; dump={}
for it in inp['items']:
    k=it['id']; media=None; status=''; note=''
    cand=[]
    if it.get('hint_mal') and it['hint_mal'] in USER:
        d=q(QID,{'m':it['hint_mal']}); m=d and d.get('Media')
        if m and tsim(it['title'],m)>=0.5: media=m; status='confermato (id proposto + titolo + lista MAL)'
        elif m: note='id proposto non combacia col titolo: '+(m['title'].get('english') or m['title'].get('romaji') or '')
    if not media:
        d=q(QSEARCH,{'s':it['title']}); res=(d and d['Page']['media']) or []
        cand=[m for m in res if m.get('idMal') in USER]
        cand.sort(key=lambda m:(m.get('format') not in ('TV','MOVIE','ONA'), m.get('seasonYear') or 9999))
        if it.get('year'):
            ok=[m for m in cand if m.get('seasonYear') and abs(m['seasonYear']-it['year'])<=1]
            if ok: cand=ok
        good=[m for m in cand if tsim(it['title'],m)>=0.5]
        if len(good)>=1:
            m=good[0]; d=q(QID,{'m':m['idMal']}); media=d and d.get('Media')
            status='collegato per ricerca (in lista MAL)' if len(good)==1 else 'DA CONTROLLARE: più candidati'
            if len(good)>1: note='candidati: '+'; '.join('%s [%s] %s'%(x['idMal'],x.get('seasonYear'),x['title'].get('english') or x['title'].get('romaji')) for x in good[:4])
        else:
            status='NON RISOLTO'
            note=(note+' ' if note else '')+'; '.join('%s [%s] %s%s'%(x.get('idMal'),x.get('seasonYear'),x['title'].get('english') or x['title'].get('romaji'),'' if x.get('idMal') in USER else ' (non in lista)') for x in res[:3])
    entry={'status':status,'note':note}
    if media:
        entry.update({'mal':media['idMal'],'anilist':media['id'],'titolo_anilist':media['title'].get('english') or media['title'].get('romaji'),'anno':media.get('seasonYear'),'formato':media.get('format')})
        edges=media['characters']['edges']
        al=[{'id':e['node']['id'],'nome':e['node']['name']['full'],'ruolo':e['role'],'fav':e['node']['favourites'],'img':e['node']['image']['large']} for e in edges]
        dump[k]={'mal':media['idMal'],'generi':media['genres'],'episodi':media['episodes'],'trama':(media.get('description') or '')[:700],'personaggi':al}
        byname={norm(c['nome']):c for c in al}; byid={c['id']:c for c in al}
        issues=[]
        for name in it['chars']:
            c=byname.get(norm(name)); url=it['photos'].get(name)
            pid=None
            mm=re.search(r'/character/large/b?(\d+)-',url or '')
            if mm: pid=int(mm.group(1))
            if not c:
                issues.append('"%s": non trovato tra i primi 25 personaggi di AniList'%name)
            elif pid and pid!=c['id']:
                other=byid.get(pid); issues.append('"%s": la foto è di %s'%(name, other['nome'] if other else 'un altro personaggio (id %d)'%pid))
            elif not url: issues.append('"%s": senza foto'%name)
        have={norm(n) for n in it['chars']}
        main=[c for c in al if c['ruolo']=='MAIN']
        sup=[c for c in al if c['ruolo']!='MAIN'][:6]
        miss=[c['nome'] for c in main+sup[:3] if norm(c['nome']) not in have]
        entry['problemi_personaggi']=issues; entry['mancanti_importanti']=miss
        entry['generi_anilist']=media['genres']; entry['generi_file']=it['genres']
    out_ids[k]=entry
    rep.append((k,it['title'],entry))
    print(k,it['title'][:28],'|',status,entry.get('mal'),file=sys.stderr)

json.dump(out_ids,open('data/anime-verify-report.json','w'),ensure_ascii=False,indent=1)
json.dump(dump,open('data/anilist-anime-dump.json','w'),ensure_ascii=False)
json.dump({k:v['mal'] for k,v in out_ids.items() if v.get('mal') and v['status'].startswith(('confermato','collegato'))},open('data/anime-mal-ids.json','w'),indent=1)
with open('data/anime-verify-report.md','w',encoding='utf8') as f:
    n_ok=sum(1 for _,_,e in rep if e['status'].startswith(('confermato','collegato')))
    f.write('# Verifica anime\n\nCollegati con certezza: %d su %d\n\n'%(n_ok,len(rep)))
    for k,t,e in rep:
        f.write('## %s %s\n- stato: %s %s\n'%(k,t,e['status'],('(MAL %s - %s)'%(e.get('mal'),e.get('titolo_anilist'))) if e.get('mal') else ''))
        if e.get('note'): f.write('- nota: %s\n'%e['note'])
        for p in e.get('problemi_personaggi',[]): f.write('- ⚠ %s\n'%p)
        if e.get('mancanti_importanti'): f.write('- mancano personaggi importanti: %s\n'%', '.join(e['mancanti_importanti']))
        if e.get('generi_anilist'): f.write('- generi AniList: %s | file: %s\n'%(', '.join(e['generi_anilist']),', '.join(e['generi_file'])))
        f.write('\n')
