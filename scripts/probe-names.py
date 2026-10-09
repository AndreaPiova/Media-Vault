import importlib.util, time
sp = importlib.util.spec_from_file_location('u', 'scripts/upgrade-manga-covers-hires.py')
u = importlib.util.module_from_spec(sp); sp.loader.exec_module(u)
out = open('data/probe-names.txt', 'w')
for q in ['Orfani Bonelli', 'Orfani 1', 'Orfani Sergio Bonelli Editore vol. 5', 'MPD Psycho 12', 'MPD Psycho Planet Manga', 'Alice in Borderland 10',
          'Alice in Borderland 18', 'Vinland Saga 5', 'Aqualung 5', 'Aqualung Seth', '20th century boys ultimate deluxe 12', 'Imawa no kuni no alice']:
    out.write('== ' + q + '\n')
    for e, n in u.search(q)[:14]: out.write(f'   {e} {n}\n')
    out.flush(); time.sleep(1)
