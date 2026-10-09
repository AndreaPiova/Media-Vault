import os, re, io, json, time, importlib.util, subprocess, requests
from PIL import Image
sp = importlib.util.spec_from_file_location('u', 'scripts/upgrade-manga-covers-hires.py')
u = importlib.util.module_from_spec(sp); sp.loader.exec_module(u)
OUT = 'covers/manga'; LOG = 'data/manga-missing-log2.json'; log = {}

def img_any(ean):
    im = u.fetch_img(ean)
    if im: return im
    r = u.get(f'https://img.ibs.it/images/{ean}_0_0_536_0_75.jpg', tries=1)
    if not r: return None
    try: im = Image.open(io.BytesIO(r.content)).convert('RGB')
    except Exception: return None
    return im if im.width >= 250 and im.height >= 300 and im.size != (1200, 1200) else None

def save(base, n, im): im.thumbnail((540, 800)); im.save(f'{OUT}/{base}_vol{n}.jpg', 'JPEG', quality=88)

def run(mid, title, base, vols, queries, ok):
    rec = log[mid] = dict(title=title, found=[], missing=[])
    for n in vols:
        fn = f'{OUT}/{base}_vol{n}.jpg'
        if os.path.exists(fn) and Image.open(fn).width >= 400: continue
        got = False
        for q in queries(n):
            for ean, name in u.search(q):
                if ok(name, n):
                    im = img_any(ean)
                    if im: save(base, n, im); rec['found'].append([n, name]); got = True; break
            time.sleep(0.8)
            if got: break
        if not got: rec['missing'].append(n)
    print(title, rec['found'].__len__(), 'trovati; mancanti', rec['missing'], flush=True)

orf = lambda name, n: re.search(r'(?i)\.\s*orfani\.\s*vol\.\s*0*%d\s*$' % n, name) is not None
run('m96', 'Orfani', 'manga_orfani', range(1, 17), lambda n: [f'Orfani Sergio Bonelli Editore vol. {n}', f'Orfani vol. {n}', f'Orfani {n}'], orf)
vin = lambda name, n: re.fullmatch(r'(?i)vinland saga[.\s]+vol\.\s*0*%d' % n, name.strip()) is not None or name.strip().lower() == f'vinland saga {n}'
run('m22', 'Vinland Saga', 'manga_vinland_saga', [5], lambda n: ['Vinland Saga 5', 'Vinland Saga vol. 5'], vin)
ali = lambda name, n: re.fullmatch(r'(?i)alice in borderland[.\s]+vol\.\s*0*%d' % n, name.strip()) is not None
run('m25', 'Alice in Borderland', 'manga_alice_in_borderland', [10], lambda n: ['Alice in Borderland 10', 'Alice in borderland vol. 10', 'Haro Aso Alice in Borderland 10'], ali)
aq = lambda name, n: re.fullmatch(r'(?i)aqualung[.\s]+vol\.\s*0*%d' % n, name.strip()) is not None
run('m95', 'Aqualung', 'manga_aqualung', [5], lambda n: ['Aqualung 5 Paliaga', 'Aqualung BAO vol. 5', 'Aqualung Paliaga Carlomagno'], aq)
json.dump(log, open(LOG, 'w'), ensure_ascii=False, indent=1)
subprocess.run(['git', 'add', OUT, LOG], check=False)
if subprocess.run(['git', 'diff', '--staged', '--quiet']).returncode:
    subprocess.run(['git', 'commit', '-q', '-m', 'Copertine mancanti (2): Orfani, Vinland Saga, Alice, Aqualung'], check=False)
    subprocess.run(['git', 'pull', '-q', '--rebase', '-X', 'theirs'], check=False); subprocess.run(['git', 'push', '-q'], check=False)
