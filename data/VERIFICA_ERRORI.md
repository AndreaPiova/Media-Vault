# MediaVault – correzioni dati emerse dal controllo incrociato (10/10/2026)

## ISTRUZIONI PER LA CHAT
Lavora su `index.html` (array FILMS_RAW, SERIES_RAW, ANIME_RAW, MANGA_RAW). Regole del progetto: modifica SOLO le righe elencate, il resto resta identico; niente riscritture globali; file compatibile Android e PC; a fine lavoro consegna il file con present_files.
Formato righe: FILMS_RAW [id,titolo,stato,voto,durata_min] · SERIES_RAW [id,titolo,stato,voto,episodi_totali,minuti_medi,episodi_visti,nota] · ANIME_RAW [id,titolo,stato,voto,episodi_totali,episodi_visti,durata_min] · MANGA_RAW [id,titolo,stato,voto,nota,volumi_totali,prezzo,posseduti,letti,edizione,tipo,flag].
Prima di applicare ogni correzione ricontrolla su una seconda fonte (TMDB / IMDb / AniList / MyAnimeList / AnimeClick). Dove scritto «da decidere» chiedimi conferma.
Fonti usate nel controllo: TMDB, dataset IMDb, AniList, AnimeClick (edizioni italiane). Jikan/MAL non era raggiungibile in automatico.
Nota: nel file non sono salvati anno, cast, genere (Film/Serie/Anime) e le sezioni Libri e Film Infanzia sono vuote nel file, quindi non verificabili qui.
Controlli di coerenza interna (completato ma episodi/volumi non al massimo, visti>totali, posseduti>totali): nessuna anomalia trovata.

## 1. FILM – durata (TMDB e IMDb concordi, differenza >3 min)
Formato: id · titolo · durata attuale → proposta
- f10 · 3 uomini e una gamba · 92 → 100 min
- f55 · Un ponte per Terabithia · 111 → 96 min
- f77 · Pacific Rim · 111 → 131 min
- f79 · Ritorno al futuro 2 · 118 → 108 min  (2° film della saga)
- f92 · La banda dei babbi natale · 91 → 100 min
- f94 · Lady Vengeance · 120 → 112 min
- f104 · Tu la conosci Claudia? · 97 → 104 min
- f105 · La haine · 109 → 98 min
- f113 · Superman · 93 → 129 min
- f115 · Cercasi amore per la fine del mondo · 108 → 101 min
- f116 · Chiedimi se sono felice · 109 → 100 min
- f127 · Così è la vita · 92 → 108 min
- f132 · Viaggio al centro della terra · 84 → 90 min  (anno dedotto dalla durata più vicina tra omonimi)
- f139 · Sole a catinelle · 83 → 90 min
- f143 · Benvenuti al Nord · 90 → 110 min
- f144 · Che bella giornata · 90 → 97 min
- f145 · Cado dalle nubi · 88 → 95 min
- f147 · I pinguini di Mr. Popper · 88 → 94 min
- f150 · Mamma ho preso il morbillo · 95 → 102 min
- f169 · Coach Carter · 105 → 136 min
- f173 · Waiting · 103 → 94 min  (anno dedotto dalla durata più vicina tra omonimi)
- f179 · The Hunt · 105 → 115 min
- f186 · L'inquilino del terzo piano · 133 → 126 min
- f202 · Fallen · 117 → 124 min
- f208 · King of New York · 121 → 106 min
- f240 · God's Crooked Lines · 113 → 103 min  (anno dedotto dalla durata più vicina tra omonimi)
- f253 · La giuria · 133 → 127 min
- f257 · La leggenda di Al, John e Jack · 100 → 105 min
- f260 · Mad Max · 120 → 88 min  (anno dedotto dalla durata più vicina tra omonimi)
- f271 · Attitudini: Nessuna · 90 → 117 min
- f287 · The Call · 94 → 112 min
- f300 · The Double · 93 → 83 min
- f340 · Monster · 109 → 127 min
- f343 · No Mercy · 106 → 123 min
- f368 · Sympathy for Mr. Vengeance · 121 → 129 min
- f373 · The Truth Beneath · 108 → 102 min

### 1b. FILM – da decidere (voce di saga/titolo ambiguo/abbinamento incerto)
- f160 · Avengers · Nostro 149 min; TMDB 143, IMDb 143 → proposta 143
- f162 · Star Wars · Nostro 125 min; TMDB 121, IMDb 121 → proposta 121
- f164 · Il Signore degli Anelli · Nostro 178 min; TMDB 132, IMDb 132 → proposta 132
- f165 · Lo Hobbit · Nostro 169 min; TMDB 77, IMDb 77 → proposta 77
- f11 · I guardiani della galassia 1 · NON_TROVATO: Nessun film TMDB corrisponde al titolo
- f20 · I guardiani della galassia 3 · NON_TROVATO: Nessun film TMDB corrisponde al titolo
- f27 · I guardiani della galassia 2 · NON_TROVATO: Nessun film TMDB corrisponde al titolo
- f61 · Zathura · NON_TROVATO: Nessun film TMDB corrisponde al titolo
- f70 · I pirati dei Caraibi 2 · DURATA?: Nostro 151 min; TMDB 141, IMDb 136 → proposta 141
- f80 · I pirati dei Caraibi 3 · DURATA?: Nostro 169 min; TMDB 141, IMDb 136 → proposta 141
- f128 · Enemy · DURATA?: Nostro 91 min; TMDB 130, IMDb None → proposta 130
- f140 · I pirati dei Caraibi 5 · DURATA?: Nostro 129 min; TMDB 141, IMDb 136 → proposta 141
- f184 · Rendezvous with Rama · DURATA?: Nostro 120 min; TMDB 4, IMDb 4 → proposta 4 (possibile film sbagliato/cortometraggio: controllare)
- f196 · Inside Men · DURATA?: Nostro 115 min; TMDB 181, IMDb 130 → proposta 181
- f217 · Arcane · DURATA?: Nostro 81 min; TMDB 15, IMDb None → proposta 15 (possibile film sbagliato/cortometraggio: controllare)
- f221 · The Secret Number · DURATA?: Nostro 90 min; TMDB 15, IMDb 15 → proposta 15 (possibile film sbagliato/cortometraggio: controllare)
- f270 · Wake Up Dead Man · DURATA?: Nostro 145 min; TMDB 97, IMDb None → proposta 97
- f304 · The Fall · ANNO: Anno copertina 2006 ≠ TMDB 2008
- f304 · The Fall · ANNO: TMDB 2008 ≠ IMDb 2006

## 2. SERIE TV – episodi totali
Alta confidenza (TMDB e IMDb concordi, serie conclusa):
- s27 · Elite · Nostro 40; TMDB 64, IMDb 64 → proposta 64
- s33 · Stranger Things · Nostro 34; TMDB 42, IMDb 42 → proposta 42
- s41 · Outer Banks · Nostro 40; TMDB 50, IMDb 50 → proposta 50
- s46 · The Good Place · Nostro 53; TMDB 50, IMDb 50 → proposta 50
- s48 · The Blacklist · Nostro 220; TMDB 218, IMDb 218 → proposta 218
- s65 · Battlestar Galactica · Nostro 75; TMDB 73, IMDb 74 → proposta 73 [Battlestar Galactica (2004); Battlestar Galactica (2003); Galactica (1978)]
- s92 · The Boys · Nostro 32; TMDB 40, IMDb 40 → proposta 40
- s105 · BoJack Horseman · Nostro 77; TMDB 76, IMDb 76 → proposta 76
- s110 · Ai confini della realtà (1985) · Nostro 156; TMDB 65, IMDb 66 → proposta 65

Da verificare (serie in corso o fonti discordanti: spesso sono solo stagioni nuove uscite dopo l'inserimento):
- s4 · Friends · Nostro 235; TMDB 228, IMDb 234
- s16 · The Punisher · Nostro 26; TMDB 1, IMDb None (serie in corso: potrebbe essere solo aggiornamento)
- s28 · Rick and Morty · Nostro 110; TMDB 91, IMDb 94 (serie in corso: potrebbe essere solo aggiornamento)
- s37 · True Detective · Nostro 38; TMDB 30, IMDb 31 (serie in corso: potrebbe essere solo aggiornamento) → proposta 30
- s51 · Gli anelli del potere · Nostro 16; TMDB 24, IMDb 25 (serie in corso: potrebbe essere solo aggiornamento) → proposta 24
- s52 · The Last of Us · Nostro 9; TMDB 16, IMDb 17 (serie in corso: potrebbe essere solo aggiornamento) → proposta 16
- s54 · Invincible · Nostro 16; TMDB 32, IMDb 34 (serie in corso: potrebbe essere solo aggiornamento)
- s56 · A Knight of the Seven Kingdoms · Nostro 3; TMDB 6, IMDb 12 (serie in corso: potrebbe essere solo aggiornamento)
- s57 · House of the Dragon · Nostro 18; TMDB 26, IMDb 27 (serie in corso: potrebbe essere solo aggiornamento) → proposta 26
- s59 · Doctor Who · Nostro 293; TMDB 153, IMDb 175
- s63 · The Pitt · Nostro 15; TMDB 30, IMDb 45 (serie in corso: potrebbe essere solo aggiornamento)
- s64 · Black Mirror · Nostro 27; TMDB 33, IMDb 34 (serie in corso: potrebbe essere solo aggiornamento) → proposta 33
- s66 · From · Nostro 30; TMDB 40, IMDb 41 (serie in corso: potrebbe essere solo aggiornamento) → proposta 40
- s79 · Silo · Nostro 20; TMDB 31, IMDb 40 (serie in corso: potrebbe essere solo aggiornamento)
- s88 · Lupin · Nostro 17; TMDB 25, IMDb 25 (serie in corso: potrebbe essere solo aggiornamento) → proposta 25
- s102 · Fallout · Nostro 8; TMDB 16, IMDb 17 (serie in corso: potrebbe essere solo aggiornamento) → proposta 16

### 2b. SERIE TV – minuti per episodio (nostro vs TMDB media stagione 1 / ultimo episodio; differenza >8 min)
- s7 · La casa di carta · Nostro 45 min; TMDB stagione 1 media 72, ultimo episodio 77
- s13 · Squid Game · Nostro 33 min; TMDB stagione 1 media 55, ultimo episodio 56
- s17 · Lost in Space · Nostro 46 min; TMDB stagione 1 media 56, ultimo episodio 59
- s18 · Umbrella Academy · Nostro 46 min; TMDB stagione 1 media 56, ultimo episodio 70
- s26 · 13 Reasons Why · Nostro 47 min; TMDB stagione 1 media 56, ultimo episodio 99
- s32 · The Walking Dead · Nostro 22 min; TMDB stagione 1 media 49, ultimo episodio 65
- s51 · Gli anelli del potere · Nostro 60 min; TMDB stagione 1 media 71, ultimo episodio 74
- s54 · Invincible · Nostro 28 min; TMDB stagione 1 media 49, ultimo episodio 52
- s56 · A Knight of the Seven Kingdoms · Nostro 55 min; TMDB stagione 1 media 35, ultimo episodio 31
- s60 · Narcos Mexico · Nostro 45 min; TMDB stagione 1 media 61, ultimo episodio 69
- s75 · The Night Of · Nostro 55 min; TMDB stagione 1 media 66, ultimo episodio 96
- s77 · Scissione · Nostro 42 min; TMDB stagione 1 media 52, ultimo episodio 80
- s88 · Lupin · Nostro 28 min; TMDB stagione 1 media 46, ultimo episodio 52

### 2c. SERIE TV – non trovate
- s49 · Manhunt: Unabomber · Nessuna serie TMDB corrisponde (verifica a mano: titolo da correggere?)
- s109 · Eteros Ego · Nessuna serie TMDB corrisponde (verifica a mano: titolo da correggere?)

## 3. ANIME – episodi totali (le tue voci sono totali di franchise: confronto con TMDB, che somma le stagioni, e AniList, che è per singola stagione)
Probabili errori (TMDB ≥ AniList e diverso dal nostro):
- a1 · Attack on Titan · Nostro 94; TMDB (tutte le stagioni) 87, AniList (singola voce) 25
- a6 · Jujutsu Kaisen · Nostro 47; TMDB (tutte le stagioni) 59, AniList (singola voce) 24 – serie ancora in corso
- a7 · Dr. Stone · Nostro 53; TMDB (tutte le stagioni) 94, AniList (singola voce) 24
- a10 · Horimiya · Nostro 16; TMDB (tutte le stagioni) 13, AniList (singola voce) 13
- a11 · Kuroko no Basket · Nostro 75; TMDB (tutte le stagioni) 78, AniList (singola voce) 25
- a22 · Naruto · Nostro 720; TMDB (tutte le stagioni) 220, AniList (singola voce) 220
- a23 · JoJo's Bizarre Adventure · Nostro 190; TMDB (tutte le stagioni) 202, AniList (singola voce) 26 – serie ancora in corso
- a28 · Classroom of the Elite · Nostro 24; TMDB (tutte le stagioni) 54, AniList (singola voce) 12 – serie ancora in corso
- a30 · Tokyo Revengers · Nostro 37; TMDB (tutte le stagioni) 55, AniList (singola voce) 24 – serie ancora in corso
- a41 · One Punch Man · Nostro 24; TMDB (tutte le stagioni) 36, AniList (singola voce) 12 – serie ancora in corso
- a42 · My Hero Academia · Nostro 138; TMDB (tutte le stagioni) 170, AniList (singola voce) 13
- a73 · Angels of Death · Nostro 16; TMDB (tutte le stagioni) 12, AniList (singola voce) 12
- a87 · Bleach · Nostro 392; TMDB (tutte le stagioni) 416, AniList (singola voce) 366 – serie ancora in corso
- a89 · Bungou Stray Dogs · Nostro 47; TMDB (tutte le stagioni) 60, AniList (singola voce) 12 – serie ancora in corso
- a92 · Clannad · Nostro 47; TMDB (tutte le stagioni) 44, AniList (singola voce) 23
- a95 · D.Gray-man · Nostro 116; TMDB (tutte le stagioni) 103, AniList (singola voce) 103
- a106 · Gintama · Nostro 400; TMDB (tutte le stagioni) 367, AniList (singola voce) 201
- a123 · Kingdom · Nostro 130; TMDB (tutte le stagioni) 156, AniList (singola voce) 38 – serie ancora in corso
- a126 · Ghost in the Shell · Nostro 28; TMDB (tutte le stagioni) 10, AniList (singola voce) 1
- a130 · Magi · Nostro 63; TMDB (tutte le stagioni) 50, AniList (singola voce) 26
- a138 · Oshi no Ko · Nostro 23; TMDB (tutte le stagioni) 35, AniList (singola voce) 11 – serie ancora in corso
- a156 · Trigun · Nostro 38; TMDB (tutte le stagioni) 26, AniList (singola voce) 26
- a172 · Sword Art Online · Nostro 88; TMDB (tutte le stagioni) 96, AniList (singola voce) 25

Da controllare manualmente su MAL/AniList (TMDB non ha dato risultato, quindi sicura solo la singola stagione):
- a2 · One Piece · Nostro 1100; TMDB (tutte le stagioni) 1180, AniList (singola voce) None – serie ancora in corso
- a17 · Code Geass · Nostro 50; TMDB (tutte le stagioni) None, AniList (singola voce) 25
- a24 · Love is War · Nostro 37; TMDB (tutte le stagioni) None, AniList (singola voce) 12
- a35 · Spy x Family · Nostro 37; TMDB (tutte le stagioni) 50, AniList (singola voce) None
- a46 · Demon Slayer · Nostro 55; TMDB (tutte le stagioni) None, AniList (singola voce) 26
- a72 · Shinsekai Yori · Nostro 8; TMDB (tutte le stagioni) None, AniList (singola voce) 25
- a75 · 3-gatsu no Lion · Nostro 44; TMDB (tutte le stagioni) None, AniList (singola voce) 22
- a76 · 5-toubun no Hanayome · Nostro 26; TMDB (tutte le stagioni) None, AniList (singola voce) 12
- a80 · Ao no Exorcist · Nostro 37; TMDB (tutte le stagioni) None, AniList (singola voce) 25
- a81 · Ao no Hako · Nostro 25; TMDB (tutte le stagioni) None, AniList (singola voce) 12
- a82 · Ashita no Joe · Nostro 126; TMDB (tutte le stagioni) None, AniList (singola voce) 79
- a90 · 5 Centimeters Per Second · Nostro 1; TMDB (tutte le stagioni) None, AniList (singola voce) 3
- a99 · Enen no Shouboutai · Nostro 73; TMDB (tutte le stagioni) None, AniList (singola voce) 24
- a103 · Fumetsu no Anata e · Nostro 62; TMDB (tutte le stagioni) None, AniList (singola voce) 20
- a105 · Ginga Eiyuu Densetsu · Nostro 110; TMDB (tutte le stagioni) None, AniList (singola voce) 12
- a118 · Inazuma Eleven · Nostro 296; TMDB (tutte le stagioni) 268, AniList (singola voce) None
- a125 · Komi-san · Nostro 24; TMDB (tutte le stagioni) None, AniList (singola voce) 12
- a128 · Kusuriya no Hitorigoto · Nostro 48; TMDB (tutte le stagioni) None, AniList (singola voce) 24
- a134 · Mushoku Tensei · Nostro 35; TMDB (tutte le stagioni) None, AniList (singola voce) 11
- a136 · Nanatsu no Taizai · Nostro 96; TMDB (tutte le stagioni) None, AniList (singola voce) 24
- a144 · Re:Zero · Nostro 78; TMDB (tutte le stagioni) None, AniList (singola voce) 25
- a145 · Saiki Kusuo no Psi-nan · Nostro 144; TMDB (tutte le stagioni) None, AniList (singola voce) 24
- a146 · Seishun Buta Yarou · Nostro 14; TMDB (tutte le stagioni) None, AniList (singola voce) 13
- a152 · Sousou no Frieren · Nostro 38; TMDB (tutte le stagioni) None, AniList (singola voce) 28
- a154 · Tensei shitara Slime Datta Ken · Nostro 60; TMDB (tutte le stagioni) None, AniList (singola voce) 24
- a161 · Yahari Ore no Seishun Love Comedy · Nostro 38; TMDB (tutte le stagioni) None, AniList (singola voce) 1
- a171 · Dead Dead Demon's Dededede Destruction · Nostro 2; TMDB (tutte le stagioni) 17, AniList (singola voce) 18

### 3b. ANIME – durata episodio (min)
- a47 · Pluto · Nostro 45 min; AniList 60, TMDB [] / ultimo ep. 68
- a90 · 5 Centimeters Per Second · Nostro 63 min; AniList 22, TMDB None / ultimo ep. None
- a97 · Devilman: Crybaby · Nostro 30 min; AniList 25, TMDB [25] / ultimo ep. 25

### 3c. ANIME – non trovati
- a119 · Jibaku Shounen Hanako-kun · Nessuna fonte corrisponde (AniList/TMDB)
- a120 · Kage no Jitsuryokusha · Nessuna fonte corrisponde (AniList/TMDB)

## 4. MANGA – volumi (confronto con edizioni italiane AnimeClick e con l'originale AniList)
Formato: id · titolo · valore attuale → dato AnimeClick. Per le serie in corso la differenza di solito è solo l'uscita di nuovi volumi: se confermato aggiornare totalVols.
- m1 · Slam Dunk · Nostro 20; AnimeClick 'Slam Dunk' ultimo volume 24 (48 uscite)
- m2 · Solo Leveling · Nostro 27; AnimeClick 'Solo Leveling' ultimo volume 28 (28 uscite)
- m2 · Solo Leveling · Nostro 27 > volumi originali 15 (AniList, serie conclusa)
- m4 · 20th Century Boys · Nostro 12; AnimeClick '20th Century Boys Ultimate Deluxe Edition' ultimo volume 11 (11 uscite)
- m6 · Blue Lock · Nostro 32; AnimeClick 'Blue Lock' ultimo volume 35 (35 uscite)
- m10 · Chainsaw Man · Nostro 22; AnimeClick 'Chainsaw Man' ultimo volume 23 (32 uscite)
- m12 · All You Need Is Kill · Nostro 1; AnimeClick 'All You Need is Kill' ultimo volume 2 (2 uscite)
- m15 · One Piece · Nostro 109; AnimeClick 'One Piece New Edition' ultimo volume 112 (112 uscite)
- m16 · One Punch Man · Nostro 35; AnimeClick 'One-Punch Man' ultimo volume 36 (84 uscite)
- m18 · Shaman King · Nostro 35 > volumi originali 32 (AniList, serie conclusa)
- m25 · Alice in Borderland · Nostro 10; AnimeClick 'Alice in Borderland' ultimo volume 18 (27 uscite)
- m28 · Dandadan · Nostro 18; AnimeClick 'Dandadan' ultimo volume 23 (23 uscite)
- m29 · Tower of God · Nostro 500; AnimeClick 'Tower of God' ultimo volume 18 (18 uscite)
- m31 · Blue Period · Nostro 17; AnimeClick 'Blue Period' ultimo volume 18 (18 uscite)
- m47 · Kingdom · Nostro 74; AnimeClick 'Kingdom' ultimo volume 76 (76 uscite)
- m51 · Record of Ragnarok · Nostro 25; AnimeClick 'Record of Ragnarok' ultimo volume 26 (26 uscite)
- m52 · Spy x Family · Nostro 16; AnimeClick 'Spy X Family' ultimo volume 17 (31 uscite)
- m57 · Dededemon Dededestruction · Nostro 10; AnimeClick 'Dead Dead Demon’s Dededededestruction' ultimo volume 12 (19 uscite)
- m71 · Grand Blue · Nostro 3; AnimeClick 'Grand Blue' ultimo volume 4 (7 uscite)
- m94 · Radiant · Nostro 19; AnimeClick 'Radiant' ultimo volume 20 (29 uscite)

Note da non sovrascrivere (decisioni già prese da me): Alice in Borderland = 9 volumi (ultima edizione stampata; qui risulta 10 e AnimeClick ne indica 18: da allineare a 9 come deciso); 20th Century Boys Ultimate Deluxe: il vol. 12 è «21st Century Boys» (AnimeClick ne conta 11); Imawa no Kuni no Alice (m42) è un doppione da rimuovere. Tower of God: 500 sembra il numero di capitoli, non di volumi (AnimeClick: 18): da decidere.

### 4b. MANGA – edizione non riconosciuta su AnimeClick (controllare nome edizione/titolo italiano)
- m9 · Il prezzo di una vita · Nessun gruppo AnimeClick coincide con 'Il prezzo di una vita Box': Il prezzo di una vita - I sold my life for ten thousand yen per year: max vol 3, 3 uscite; Il prezzo di una vita - I sold my life for ten thousand yen per year Box: max vol 0, 1 uscite
- m18 · Shaman King · Nessun gruppo AnimeClick coincide con 'Shaman King Final edition': Le bizzarre avventure di JoJo: Steel Ball Run: max vol 24, 40 uscite
- m19 · Attack on Titan · Nessun gruppo AnimeClick coincide con 'Attack on Titan': L'Attacco dei Giganti - Discovery Edition: max vol 1, 1 uscite; L'Attacco dei Giganti: max vol 34, 125 uscite; L'Attacco dei Giganti Variant: max vol 33, 3 uscite; L'Attacco dei Giganti - Bundle con Shor
- m33 · Dorohedoro · Nessun gruppo AnimeClick coincide con 'Dorohedoro': Kappa - La scena dell'inferno: max vol 0, 1 uscite
- m40 · Houseki no Kuni · Nessun gruppo AnimeClick coincide con 'Houseki no Kuni': Land of the Lustrous: max vol 13, 13 uscite; Land of the Lustrous Jacket Variant Double-face: max vol 13, 1 uscite
- m43 · Jagaaaaaan · Nessun gruppo AnimeClick coincide con 'Jagaaaaaan': Jagan: max vol 14, 14 uscite; Jagan - Variant cover edition: max vol 1, 1 uscite
- m45 · Jujutsu Kaisen · Nessun gruppo AnimeClick coincide con 'Jujutsu Kaisen': Jujutsu Kaisen Official Fanbook: max vol 0, 1 uscite; Jujutsu Kaisen - Sorcery Fight - Edizione Early Access: max vol 1, 1 uscite; Jujutsu Kaisen - Sorcery Fight - Variant: max vol 30, 5 uscite; Jujutsu K
- m46 · Juujika no Rokunin · Nessun gruppo AnimeClick coincide con 'Juujika no Rokunin': X6 - Crucisix: max vol 15, 15 uscite
- m54 · Tegamibachi · Nessun gruppo AnimeClick coincide con 'Tegamibachi': Letter Bee: max vol 20, 22 uscite
- m59 · Gantz · Nessun gruppo AnimeClick coincide con 'Gantz New edition': Gantz: max vol 37, 38 uscite; Gantz - Nuova Edizione: max vol 37, 42 uscite
- m62 · Hanako-kun · Nessun gruppo AnimeClick coincide con 'Hanako-kun': Hanako kun - I sette misteri dell'Accademia Kamome: max vol 26, 26 uscite; Hanako kun - Art Work: max vol 0, 1 uscite; Hanako kun - Art Work 2: max vol 0, 1 uscite; Hanako kun - I sette misteri dell'Accademia
- m63 · Hell's Paradise · Nessun gruppo AnimeClick coincide con 'Hell's Paradise': Hell's Paradise – Jigokuraku: max vol 13, 13 uscite
- m65 · Komi-san · Nessun gruppo AnimeClick coincide con 'Komi-san': Komi Can't Communicate: max vol 37, 37 uscite; Komi Can't Communicate Variant Edition Games Academy: max vol 1, 1 uscite; Komi Can't Communicate - Graduation Variant: max vol 37, 1 uscite
- m66 · No Longer Human · Nessun gruppo AnimeClick coincide con 'No Longer Human Complete edition': Lo squalificato: max vol 3, 3 uscite; Lo squalificato - Complete Edition: max vol 0, 1 uscite
- m69 · Frieren · Nessun gruppo AnimeClick coincide con 'Frieren': Frieren - Oltre la fine del viaggio Variant: max vol 1, 1 uscite; Frieren - Oltre la fine del viaggio - Official Fanbook: max vol 0, 1 uscite; Frieren - Oltre la fine del viaggio Variant Popstore: max vol 1, 1 u
