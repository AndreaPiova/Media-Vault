# MediaVault v43 — Errori da correggere (verifica multi-fonte)

Fonti: TMDB, IMDb datasets, AniList, AnimeClick/IBS (manga), Open Library. Poster/backdrop confrontati con hash percettivo per identificare omonimi.
Legenda: per ogni voce `id Titolo` → FLAG: dettaglio. Dove c'è `id_corretto` va sostituito l'id TMDB manuale.
Non verificabili automaticamente: Manga Variant/Artbook (211), Jikan non raggiungibile. FOTO_CAST = foto attore che non corrisponde al nome (controllo per somiglianza, rumoroso: verificare a campione).

## Correzioni id TMDB film (poster identificato)

- f82 The Illusionist → nuovo id TMDB 1491
- f127 Così è la vita → nuovo id TMDB 38396
- f456 The Hunger Games: Mockingjay - Part 1 → nuovo id TMDB 131631
- f194 Eyes Wide Shut → nuovo id TMDB 345
- f231 Chinatown → nuovo id TMDB 829
- f241 The Day After Tomorrow → nuovo id TMDB 435
- f263 JFK → nuovo id TMDB 820
- f270 Wake Up Dead Man → nuovo id TMDB 812583
- f279 Before Midnight → nuovo id TMDB 132344
- f312 The French Connection → nuovo id TMDB 1051
- f346 Oblivion → nuovo id TMDB 75612
- f352 Personal Shopper → nuovo id TMDB 340676
- f364 Society of the Snow → nuovo id TMDB 906126
- f417 Cube → nuovo id TMDB 431
- f419 Journey to the Mysterious Island → nuovo id TMDB 72545
- f440 Lost Highway → nuovo id TMDB 638
- f137 Stand by Me → nuovo id TMDB 235
- f457 The Hunger Games: Mockingjay - Part 2 → nuovo id TMDB 131634
- f168 Atonement → nuovo id TMDB 4347
- f212 Ted → nuovo id TMDB 72105
- f219 Source Code → nuovo id TMDB 45612
- f251 About Time → nuovo id TMDB 122906
- f258 Chronicle → nuovo id TMDB 76726
- f267 Collateral → nuovo id TMDB 1538
- f274 Aftersun → nuovo id TMDB 965150
- f292 Chungking Express → nuovo id TMDB 11104
- f301 The Elephant Man → nuovo id TMDB 1955
- f307 The Father → nuovo id TMDB 600354
- f329 The Insider → nuovo id TMDB 9008
- f347 Once Upon a Time in America → nuovo id TMDB 311
- f350 Paris, Texas → nuovo id TMDB 655
- f387 Dogville → nuovo id TMDB 553
- f393 Willy Wonka e la fabbrica di cioccolato → nuovo id TMDB 252
- f409 The Seventh Seal → nuovo id TMDB 490
- f428 Barry Lyndon → nuovo id TMDB 3175
- f90 The Untouchables → nuovo id TMDB 117
- f193 Moon → nuovo id TMDB 17431
- f213 Being John Malkovich → nuovo id TMDB 492
- f224 Big Fish → nuovo id TMDB 587
- f256 The Place Beyond the Pines → nuovo id TMDB 97367
- f265 First Man → nuovo id TMDB 369972
- f272 21 Jump Street → nuovo id TMDB 64688
- f296 Dial M for Murder → nuovo id TMDB 521
- f324 Her → nuovo id TMDB 152601
- f330 Into the Wild → nuovo id TMDB 5915
- f339 Minari → nuovo id TMDB 615643
- f351 Persona → nuovo id TMDB 797
- f357 Rear Window → nuovo id TMDB 567
- f363 Signs → nuovo id TMDB 2675
- f371 The Tree of Life → nuovo id TMDB 8967
- f374 Unbreakable → nuovo id TMDB 9741
- f407 Vanilla Sky → nuovo id TMDB 1903
- f413 Wind River → nuovo id TMDB 395834
- f416 Equilibrium → nuovo id TMDB 7299
- f185 Incendies → nuovo id TMDB 46738
- f285 Boyhood → nuovo id TMDB 85350
- f24 Mystic River → nuovo id TMDB 322
- f183 The Age of Adaline → nuovo id TMDB 293863
- f288 Carlito's Way → nuovo id TMDB 6075
- f310 The Fountain → nuovo id TMDB 1381

## FILM

### f479 The Odyssey
- CAST: Non nel cast TMDB (top25): ['Zendaya']; TMDB top: ['Matt Damon', 'Tom Holland', 'Anne Hathaway', 'Robert Pattinson', 'Himesh Patel', 'Charlize Theron']
- FOTO_CAST: Tom Holland: foto diversa da TMDB
### f8 The Departed
- FOTO_CAST: Jack Nicholson: foto diversa da TMDB
### f11 Guardians of the Galaxy 1
- FOTO_CAST: Vin Diesel: foto diversa da TMDB; Bradley Cooper: foto diversa da TMDB
### f17 Memories of Murder
- CAST: Non nel cast TMDB (top25): ['Kim Sang-kyung']; TMDB top: ['Song Kang-ho', 'Song Jae-ho']
- FOTO_CAST: Kim Sang-kyung: persona non nel cast TMDB
### f20 Guardians of the Galaxy 3
- FOTO_CAST: Bradley Cooper: foto diversa da TMDB
### f29 The Social Network
- FOTO_CAST: Andrew Garfield: foto diversa da TMDB
### f38 Memento
- FOTO_CAST: Carrie-Anne Moss: foto diversa da TMDB
### f40 Training Day
- FOTO_CAST: Eva Mendes: foto diversa da TMDB
### f43 The Matrix
- FOTO_CAST: Carrie-Anne Moss: foto diversa da TMDB
### f46 Project Hail Mary
- FOTO_CAST: Sandra Hüller: foto diversa da TMDB
### f51 Drive
- FOTO_CAST: Bryan Cranston: foto diversa da TMDB
### f54 Knowing
- FOTO_CAST: Rose Byrne: foto diversa da TMDB
### f77 Pacific Rim
- DURATA: Nostro 111 min; TMDB 131, IMDb 131
### f80 Pirates of the Caribbean: At World's End
- FOTO_CAST: Keira Knightley: foto diversa da TMDB
### f82 The Illusionist [id_corretto: {'da': 1547, 'a': 1491}]
- FOTO_CAST: Jessica Biel: foto diversa da TMDB
### f85 La Fabbrica di Cioccolato
- FOTO_CAST: AnnaSophia Robb: foto diversa da TMDB
### f88 Men in Black 3
- POSTER?: Copertina poco simile ai poster TMDB id 41154 (Men in Black 3 2012), dist 27: verificare a vista. Candidati: [(27, 41154, 'Men in Black 3', '2012')]
### f100 The Redeem Team
- FOTO_CAST: LeBron James: foto diversa da TMDB
### f112 Now You See Me 2
- FOTO_CAST: Dave Franco: foto diversa da TMDB
### f115 Seeking a Friend for the End of the World
- FOTO_CAST: Steve Carell: foto diversa da TMDB; Keira Knightley: foto diversa da TMDB
- DURATA: Nostro 108 min; TMDB 101, IMDb 101
### f121 One Flew Over the Cuckoo's Nest
- FOTO_CAST: Jack Nicholson: foto diversa da TMDB
### f124 Inkheart
- FOTO_CAST: Paul Bettany: foto diversa da TMDB
### f136 Glass Onion
- FOTO_CAST: Janelle Monáe: foto diversa da TMDB
### f139 Sole a catinelle
- FOTO_CAST: Checco Zalone: foto diversa da TMDB
- DURATA?: Nostro 83 min; TMDB 90, IMDb 87
### f142 The Hangover
- FOTO_CAST: Bradley Cooper: foto diversa da TMDB; Zach Galifianakis: foto diversa da TMDB; Heather Graham: foto diversa da TMDB
### f145 Cado dalle nubi
- FOTO_CAST: Checco Zalone: foto diversa da TMDB
- DURATA: Nostro 88 min; TMDB 95, IMDb 95
### f154 Philadelphia
- FOTO_CAST: Antonio Banderas: foto diversa da TMDB
### f454 The Hobbit: The Battle of the Five Armies
- FOTO_CAST: Evangeline Lilly: foto diversa da TMDB
### f170 Snowden
- FOTO_CAST: Tom Wilkinson: foto diversa da TMDB
### f175 Next
- FOTO_CAST: Jessica Biel: foto diversa da TMDB
### f178 Schindler's List
- FOTO_CAST: Ralph Fiennes: foto diversa da TMDB
### f181 Rain Man
- FOTO_CAST: Tom Cruise: foto diversa da TMDB
### f185 Incendies [id_corretto: {'da': 45269, 'a': 46738}]
- FOTO_CAST: Mélissa Désormeaux-Poulin: foto diversa da TMDB
### f188 A Cure for Wellness
- ANNO: Nostro 2016; TMDB 2017
- FOTO_CAST: Dane DeHaan: foto diversa da TMDB
- ANNO_FONTI: TMDB 2017 ≠ IMDb 2016 (nostro 2016)
### f191 The Lives of Others
- FOTO_CAST: Ulrich Mühe: foto diversa da TMDB
### f194 Eyes Wide Shut [id_corretto: {'da': 919, 'a': 345}]
- FOTO_CAST: Tom Cruise: foto diversa da TMDB
### f206 Another Round
- ID_TMDB_SOSPETTO: 3 indizi concordi: l'id TMDB assegnato (581392) potrebbe riferirsi a un altro titolo/omonimo
- TITOLO: 'Another Round' ≠ TMDB 'Peninsula' / '반도'
- REGISTA: Nostro 'Thomas Vinterberg'; TMDB ['Yeon Sang-ho']
- CAST: Non nel cast TMDB (top25): ['Mads Mikkelsen', 'Thomas Bo Larsen', 'Magnus Millang', 'Lars Ranthe', 'Maria Bonnevie']; TMDB top: ['Kim Min-jae', 'Kim Do-yoon', 'Jang So-yeon', 'Joey Albright', 'Pierce Conran', 'John D. Michaels']
- GENERI: Nostri ['Commedia', 'Dramma']; TMDB ['Horror', 'Azione', 'Thriller', 'Avventura']
- FOTO_CAST: Mads Mikkelsen: persona non nel cast TMDB; Thomas Bo Larsen: persona non nel cast TMDB; Magnus Millang: persona non nel cast TMDB; Lars Ranthe: persona non nel cast TMDB; Maria Bonnevie: persona non nel cast TMDB
### f214 Oppenheimer
- FOTO_CAST: Florence Pugh: foto diversa da TMDB
### f225 Ex Machina
- ANNO: Nostro 2014; TMDB 2015
- ANNO_FONTI: TMDB 2015 ≠ IMDb 2014 (nostro 2014)
### f231 Chinatown [id_corretto: {'da': 664, 'a': 829}]
- FOTO_CAST: Jack Nicholson: foto diversa da TMDB
### f237 A Beautiful Mind
- FOTO_CAST: Russell Crowe: foto diversa da TMDB; Paul Bettany: foto diversa da TMDB
### f254 Nine Queens
- FOTO_CAST: Ricardo Darín: foto diversa da TMDB
### f257 La leggenda di Al, John e Jack
- DURATA: Nostro 100 min; TMDB 105, IMDb 105
### f260 Mad Max
- TITOLO: 'Mad Max' ≠ TMDB 'Mad Max: Fury Road' / 'Mad Max: Fury Road'
### f266 Sunshine
- FOTO_CAST: Rose Byrne: foto diversa da TMDB
### f276 All That Jazz
- FOTO_CAST: Jessica Lange: foto diversa da TMDB
### f297 Die Hard
- FOTO_CAST: Bonnie Bedelia: foto diversa da TMDB; Reginald VelJohnson: foto diversa da TMDB
### f300 The Double
- ANNO: Nostro 2013; TMDB 2014
- FOTO_CAST: Александр Ревва: persona non nel cast TMDB; Кристина Асмус: persona non nel cast TMDB; Дмитрий Хрусталев: persona non nel cast TMDB; Wallace Shawn: foto diversa da TMDB
- ANNO_FONTI: TMDB 2014 ≠ IMDb 2013 (nostro 2013)
### f303 Event Horizon
- FOTO_CAST: Joely Richardson: foto diversa da TMDB
### f325 Hitch
- FOTO_CAST: Eva Mendes: foto diversa da TMDB
### f334 The Last Samurai
- FOTO_CAST: Tom Cruise: foto diversa da TMDB
### f337 Love & Other Drugs
- FOTO_CAST: Hank Azaria: foto diversa da TMDB
### f346 Oblivion [id_corretto: {'da': 76757, 'a': 75612}]
- FOTO_CAST: Tom Cruise: foto diversa da TMDB
### f349 Pan's Labyrinth
- FOTO_CAST: Ivana Baquero: foto diversa da TMDB
### f361 Seven Pounds
- FOTO_CAST: Rosario Dawson: foto diversa da TMDB
### f368 Sympathy for Mr. Vengeance
- DURATA: Nostro 121 min; TMDB 129, IMDb 129
### f375 Unforgiven
- FOTO_CAST: Richard Harris: foto diversa da TMDB
- POSTER_ALTRO_TITOLO: La copertina assomiglia di più a WWE Unforgiven 2002 (2002, id 215921, dist 17) che a id assegnato 33 Gli spietati (1992, dist 24). Candidati: [(17, 215921, 'WWE Unforgiven 2002', '2002'), (22, 209855, 'WWE Unforgiven 2001', '2001'), (22, 1608445, 'Tarung: Unforgiven', '2026')]
### f378 Wild Tales
- ID_TMDB_SOSPETTO: 4 indizi concordi: l'id TMDB assegnato (325133) potrebbe riferirsi a un altro titolo/omonimo
- TITOLO: 'Wild Tales' ≠ TMDB 'Cattivi vicini 2' / 'Neighbors 2: Sorority Rising'
- ANNO: Nostro 2014; TMDB 2016
- REGISTA: Nostro 'Damián Szifron'; TMDB ['Nicholas Stoller']
- CAST: Non nel cast TMDB (top25): ['Ricardo Darín', 'Leonardo Sbaraglia', 'Érica Rivas', 'Oscar Martínez', 'Rita Cortese']; TMDB top: ['Seth Rogen', 'Zac Efron', 'Rose Byrne', 'Chloë Grace Moretz', 'Dave Franco', 'Ike Barinholtz']
- GENERI: Nostri ['Commedia nera', 'Dramma', 'Thriller']; TMDB ['Commedia']
- FOTO_CAST: Ricardo Darín: persona non nel cast TMDB; Leonardo Sbaraglia: persona non nel cast TMDB; Érica Rivas: persona non nel cast TMDB; Oscar Martínez: persona non nel cast TMDB; Rita Cortese: persona non nel cast TMDB
- DURATA: Nostro 122 min; TMDB 92, IMDb 92
### f381 Fracture
- FOTO_CAST: Anthony Hopkins: foto diversa da TMDB
### f386 A Separation
- CAST: Non nel cast TMDB (top25): ['Shahab Hosseini']; TMDB top: ['Sareh Bayat', 'Sarina Farhadi', 'Ali-Asghar Shahbazi', 'Kimia Hosseini', 'Armine Zeytounchian', 'Shirin Yazdanbakhsh']
- FOTO_CAST: Shahab Hosseini: persona non nel cast TMDB
### f396 Looper
- DURATA: Nostro 113 min; TMDB 119, IMDb 119
### f417 Cube [id_corretto: {'da': 9327, 'a': 431}]
- ANNO: Nostro 1997; TMDB 1998
- ANNO_FONTI: TMDB 1998 ≠ IMDb 1997 (nostro 1997)
### f427 Fury
- FOTO_CAST: Jon Bernthal: foto diversa da TMDB
### f430 Presumed Innocent
- FOTO_CAST: Bonnie Bedelia: foto diversa da TMDB
### f419 Journey to the Mysterious Island [id_corretto: {'da': 63076, 'a': 72545}]
- FOTO_CAST: Vanessa Hudgens: foto diversa da TMDB
### f447 Obsession
- ANNO: Nostro 2025; TMDB 2026
- ANNO_FONTI: TMDB 2026 ≠ IMDb 2025 (nostro 2025)
### f464 Harry Potter and the Half-Blood Prince
- FOTO_CAST: Rupert Grint: foto diversa da TMDB
### f470 The Amazing Spider-Man 2
- FOTO_CAST: Andrew Garfield: foto diversa da TMDB; Emma Stone: foto diversa da TMDB; Dane DeHaan: foto diversa da TMDB
### f473 Spider-Man: No Way Home
- FOTO_CAST: Tom Holland: foto diversa da TMDB; Zendaya: foto diversa da TMDB
### f476 Harry Potter and the Prisoner of Azkaban
- FOTO_CAST: Rupert Grint: foto diversa da TMDB
### f496 The Mandalorian and Grogu
- DURATA: Nostro 120 min; TMDB 133, IMDb 132
### f4 National Treasure
- FOTO_CAST: Jon Voight: foto diversa da TMDB
### f7 Se7en
- CAST: Non nel cast TMDB (top25): ['Kevin Spacey']; TMDB top: ['Morgan Freeman', 'Brad Pitt', 'Gwyneth Paltrow', 'John Cassini', 'Peter Crombie', 'Reg E. Cathey']
- FOTO_CAST: Gwyneth Paltrow: foto diversa da TMDB
### f9 L.A. Confidential
- FOTO_CAST: Russell Crowe: foto diversa da TMDB
### f15 The Prestige
- FOTO_CAST: Hugh Jackman: foto diversa da TMDB; Scarlett Johansson: foto diversa da TMDB
### f27 Guardians of the Galaxy 2
- FOTO_CAST: Vin Diesel: foto diversa da TMDB; Bradley Cooper: foto diversa da TMDB
### f30 Inception
- FOTO_CAST: Elliot Page: foto diversa da TMDB
### f39 Knives Out
- FOTO_CAST: Ana de Armas: foto diversa da TMDB
### f41 Maze Runner 1
- FOTO_CAST: Kaya Scodelario: foto diversa da TMDB
### f44 Rocky 1
- POSTER?: Copertina poco simile ai poster TMDB id 1366 (Rocky 1976), dist 26: verificare a vista. Candidati: [(23, 1367, 'Rocky II', '1979'), (23, 312221, 'Creed', '2015'), (26, 1366, 'Rocky', '1976')]
### f52 Now You See Me 1
- FOTO_CAST: Dave Franco: foto diversa da TMDB
### f55 Bridge to Terabithia
- FOTO_CAST: AnnaSophia Robb: foto diversa da TMDB
- DURATA: Nostro 111 min; TMDB 96, IMDb 96
### f58 V for Vendetta
- ANNO: Nostro 2005; TMDB 2006
- FOTO_CAST: Stephen Rea: foto diversa da TMDB
- ANNO_FONTI: TMDB 2006 ≠ IMDb 2005 (nostro 2005)
### f61 Zathura
- TITOLO: 'Zathura' ≠ TMDB 'Zathura - Un'avventura spaziale' / 'Zathura: A Space Adventure'
### f210 Heat
- FOTO_CAST: Val Kilmer: foto diversa da TMDB
### f72 Night at the Museum 1
- CAST: Non nel cast TMDB (top25): ['Owen Wilson']; TMDB top: ['Ben Stiller', 'Carla Gugino', 'Dick Van Dyke', 'Mickey Rooney', 'Bill Cobbs', 'Jake Cherry']
### f75 Lock, Stock & 2 Smoking Barrels
- FOTO_CAST: Jason Statham: foto diversa da TMDB
### f370 Thief
- FOTO_CAST: Tuesday Weld: foto diversa da TMDB
### f83 Mary Poppins
- FOTO_CAST: Julie Andrews: foto diversa da TMDB
### f98 Tenet
- FOTO_CAST: Elizabeth Debicki: foto diversa da TMDB
### f104 Tu la conosci Claudia?
- DURATA: Nostro 97 min; TMDB 104, IMDb 104
### f110 My Best Friend's Wedding
- FOTO_CAST: Cameron Diaz: foto diversa da TMDB
### f113 Superman
- FOTO_CAST: David Corenswet: foto diversa da TMDB
### f116 Chiedimi se sono felice
- DURATA: Nostro 109 min; TMDB 100, IMDb 100
### f119 The Grand Budapest Hotel
- FOTO_CAST: Ralph Fiennes: foto diversa da TMDB
### f125 Anatomy of a Fall
- FOTO_CAST: Sandra Hüller: foto diversa da TMDB
### f128 Enemy
- ANNO: Nostro 2013; TMDB 2014
- FOTO_CAST: Igor Samobor: persona non nel cast TMDB
- ANNO_FONTI: TMDB 2014 ≠ IMDb 2013 (nostro 2013)
### f131 Maze Runner 2
- FOTO_CAST: Kaya Scodelario: foto diversa da TMDB; Giancarlo Esposito: foto diversa da TMDB
### f140 Pirates of the Caribbean: Dead Men Tell No Tales
- FOTO_CAST: Kaya Scodelario: foto diversa da TMDB
### f143 Benvenuti al Nord
- DURATA: Nostro 90 min; TMDB 110, IMDb 110
### f146 Night at the Museum 2
- FOTO_CAST: Amy Adams: foto diversa da TMDB; Hank Azaria: foto diversa da TMDB
### f155 Trainspotting
- FOTO_CAST: Ewan McGregor: foto diversa da TMDB
### f166 The Hunger Games
- FOTO_CAST: Elizabeth Banks: foto diversa da TMDB
### f168 Atonement [id_corretto: {'da': 16995, 'a': 4347}]
- FOTO_CAST: Keira Knightley: foto diversa da TMDB
### f186 The Tenant
- FOTO_CAST: Jo Van Fleet: foto diversa da TMDB
### f192 I Am Mother
- FOTO_CAST: Rose Byrne: foto diversa da TMDB
### f219 Source Code [id_corretto: {'da': 20526, 'a': 45612}]
- FOTO_CAST: Jeffrey Wright: foto diversa da TMDB
### f223 The Sixth Sense
- FOTO_CAST: Olivia Williams: foto diversa da TMDB
### f226 Joker
- FOTO_CAST: Zazie Beetz: foto diversa da TMDB
### f255 The Theory of Everything
- FOTO_CAST: Charlie Cox: foto diversa da TMDB
### f258 Chronicle [id_corretto: {'da': 73873, 'a': 76726}]
- FOTO_CAST: Dane DeHaan: foto diversa da TMDB
### f264 Bad Times at the El Royale
- FOTO_CAST: Dakota Johnson: foto diversa da TMDB
### f267 Collateral [id_corretto: {'da': 2144, 'a': 1538}]
- FOTO_CAST: Tom Cruise: foto diversa da TMDB
### f292 Chungking Express [id_corretto: {'da': 9345, 'a': 11104}]
- FOTO_CAST: Tony Leung Chiu-wai: foto diversa da TMDB
### f295 The Descent
- POSTER_ALTRO_TITOLO: La copertina assomiglia di più a The Descent: Part 2 (2009, id 34480, dist 16) che a id assegnato 9392 The Descent - Discesa nelle tenebre (2005, dist 20). Candidati: [(16, 34480, 'The Descent: Part 2', '2009'), (20, 412605, 'The Last Descent', '2016'), (23, 9392, 'The Descent', '2005')]
### f298 Dog Day Afternoon
- FOTO_CAST: John Cazale: foto diversa da TMDB
### f301 The Elephant Man [id_corretto: {'da': 995, 'a': 1955}]
- FOTO_CAST: Anthony Hopkins: foto diversa da TMDB
### f304 The Fall
- ANNO: Nostro 2006; TMDB 2008
- ANNO_FONTI: TMDB 2008 ≠ IMDb 2006 (nostro 2006)
### f307 The Father [id_corretto: {'da': 632357, 'a': 600354}]
- FOTO_CAST: Anthony Hopkins: foto diversa da TMDB; Olivia Williams: foto diversa da TMDB
### f310 The Fountain [id_corretto: {'da': 44, 'a': 1381}]
- FOTO_CAST: Hugh Jackman: foto diversa da TMDB
### f326 In the Mood for Love
- FOTO_CAST: Tony Leung Chiu-wai: foto diversa da TMDB
- POSTER_ALTRO_TITOLO: La copertina assomiglia di più a Short Cuts: Wong Kar-wai's In the Mood for Love (, id 1209783, dist 20) che a id assegnato 843 In the Mood for Love (2000, dist 25). Candidati: [(20, 1209783, "Short Cuts: Wong Kar-wai's In the Mood for Love", ''), (25, 843, 'In the Mood for Love', '2000'), (25, 187548, 'Age of Bloom', '2001')]
### f329 The Insider [id_corretto: {'da': 331, 'a': 9008}]
- FOTO_CAST: Russell Crowe: foto diversa da TMDB
### f335 The Deer Hunter
- FOTO_CAST: Meryl Streep: foto diversa da TMDB; John Cazale: foto diversa da TMDB
### f338 The Master
- FOTO_CAST: Amy Adams: foto diversa da TMDB
### f347 Once Upon a Time in America [id_corretto: {'da': 271, 'a': 311}]
- FOTO_CAST: Tuesday Weld: foto diversa da TMDB
### f362 Sicario
- FOTO_CAST: Jon Bernthal: foto diversa da TMDB
### f365 Solaris
- ID_TMDB_SOSPETTO: 3 indizi concordi: l'id TMDB assegnato (63) potrebbe riferirsi a un altro titolo/omonimo
- TITOLO: 'Solaris' ≠ TMDB 'L'esercito delle 12 scimmie' / 'Twelve Monkeys'
- ANNO: Nostro 1972; TMDB 1995
- REGISTA: Nostro 'Andrei Tarkovsky'; TMDB ['Terry Gilliam']
- CAST: Non nel cast TMDB (top25): ['Natalya Bondarchuk', 'Donatas Banionis', 'Jüri Järvet', 'Vladislav Dvorzhetsky', 'Anatoliy Solonitsyn']; TMDB top: ['Bruce Willis', 'Madeleine Stowe', 'Brad Pitt', 'Christopher Plummer', 'David Morse', 'Jon Seda']
- FOTO_CAST: Donatas Banionis: persona non nel cast TMDB; Jüri Järvet: persona non nel cast TMDB; Natalya Bondarchuk: persona non nel cast TMDB; Vladislav Dvorzhetsky: persona non nel cast TMDB; Anatoliy Solonitsyn: persona non nel cast TMDB
- DURATA: Nostro 167 min; TMDB 129, IMDb 129
### f369 A Taxi Driver
- FOTO_CAST: 유해진: persona non nel cast TMDB; Yoo Hai-jin: foto diversa da TMDB
### f379 The Wizard of Lies
- FOTO_CAST: Hank Azaria: foto diversa da TMDB
### f387 Dogville [id_corretto: {'da': 112, 'a': 553}]
- FOTO_CAST: Paul Bettany: foto diversa da TMDB
### f393 Willy Wonka e la fabbrica di cioccolato [id_corretto: {'da': 12102, 'a': 252}]
- FOTO_CAST: Roy Kinnear: foto diversa da TMDB
### f400 Sentimental Value
- DURATA: Nostro 115 min; TMDB 133, IMDb 135
### f403 The Ghost Writer
- FOTO_CAST: Ewan McGregor: foto diversa da TMDB; Olivia Williams: foto diversa da TMDB
### f406 Gladiator
- FOTO_CAST: Russell Crowe: foto diversa da TMDB; Richard Harris: foto diversa da TMDB
### f412 Minority Report
- FOTO_CAST: Tom Cruise: foto diversa da TMDB; Samantha Morton: foto diversa da TMDB
### f431 Stonehearst Asylum
- FOTO_CAST: Kate Beckinsale: foto diversa da TMDB
### f438 Dune: Part Two
- FOTO_CAST: Zendaya: foto diversa da TMDB; Rebecca Ferguson: foto diversa da TMDB
### f442 The Secret in Their Eyes
- FOTO_CAST: Ricardo Darín: foto diversa da TMDB
### f445 Black Swan
- FOTO_CAST: Winona Ryder: foto diversa da TMDB
### f448 Marty Supreme
- FOTO_CAST: Gwyneth Paltrow: foto diversa da TMDB
### f465 Harry Potter and the Deathly Hallows: Part 1
- FOTO_CAST: Rupert Grint: foto diversa da TMDB; Ralph Fiennes: foto diversa da TMDB
### f468 Spider-Man 3
- FOTO_CAST: Topher Grace: foto diversa da TMDB
### f471 Spider-Man: Homecoming
- FOTO_CAST: Tom Holland: foto diversa da TMDB; Zendaya: foto diversa da TMDB
### f474 Spider-Man: Brand New Day
- FOTO_CAST: Tom Holland: foto diversa da TMDB; Zendaya: foto diversa da TMDB; Jon Bernthal: foto diversa da TMDB
### f477 Harry Potter and the Goblet of Fire
- FOTO_CAST: Rupert Grint: foto diversa da TMDB; Ralph Fiennes: foto diversa da TMDB
### f481 Harry Potter and the Philosopher's Stone
- FOTO_CAST: Rupert Grint: foto diversa da TMDB; Emma Watson: foto diversa da TMDB; Richard Harris: foto diversa da TMDB
### f2 Prisoners
- FOTO_CAST: Hugh Jackman: foto diversa da TMDB
### f10 Tre uomini e una gamba
- REGISTA: Nostro 'Aldo, Giovanni e Giacomo'; TMDB ['Aldo Baglio', 'Massimo Venier', 'Giacomo Poretti']
- DURATA: Nostro 92 min; TMDB 98, IMDb 100
### f13 Catch Me If You Can
- FOTO_CAST: Amy Adams: foto diversa da TMDB
### f25 Arrival
- FOTO_CAST: Amy Adams: foto diversa da TMDB
### f28 Pirates of the Caribbean: The Curse of the Black Pearl
- FOTO_CAST: Keira Knightley: foto diversa da TMDB
### f34 Hacksaw Ridge
- FOTO_CAST: Andrew Garfield: foto diversa da TMDB
### f53 Snatch
- FOTO_CAST: Jason Statham: foto diversa da TMDB
### f64 The Imitation Game
- FOTO_CAST: Keira Knightley: foto diversa da TMDB; Charles Dance: foto diversa da TMDB
### f70 Pirates of the Caribbean: Dead Man's Chest
- FOTO_CAST: Keira Knightley: foto diversa da TMDB
### f73 The Notebook
- FOTO_CAST: Gena Rowlands: foto diversa da TMDB
### f79 Back to the Future 2
- DURATA: Nostro 118 min; TMDB 108, IMDb 108
### f84 The Big Short
- FOTO_CAST: Steve Carell: foto diversa da TMDB
### f87 Blade Runner 2049
- FOTO_CAST: Ana de Armas: foto diversa da TMDB
### f90 The Untouchables [id_corretto: {'da': 754, 'a': 117}]
- FOTO_CAST: Sean Connery: foto diversa da TMDB
### f93 Real Steel
- FOTO_CAST: Hugh Jackman: foto diversa da TMDB; Evangeline Lilly: foto diversa da TMDB; Anthony Mackie: foto diversa da TMDB
### f102 Home Alone 1
- FOTO_CAST: Macaulay Culkin: foto diversa da TMDB
### f105 La haine
- CAST: Non nel cast TMDB (top25): ['Karim Belkhadra']; TMDB top: ['Vincent Cassel', 'Hubert Koundé', 'Saïd Taghmaoui', 'Abdel Ahmed Ghili', 'Solo', 'Joseph Momo']
- DURATA: Nostro 109 min; TMDB 98, IMDb 98
### f108 Coherence
- ANNO: Nostro 2013; TMDB 2014
- ANNO_FONTI: TMDB 2014 ≠ IMDb 2013 (nostro 2013)
### f111 Grease
- FOTO_CAST: Stockard Channing: foto diversa da TMDB
### f117 Maze Runner 3
- FOTO_CAST: Kaya Scodelario: foto diversa da TMDB; Giancarlo Esposito: foto diversa da TMDB
### f120 Donnie Darko
- FOTO_CAST: Drew Barrymore: foto diversa da TMDB
### f123 The Silence of the Lambs
- FOTO_CAST: Anthony Hopkins: foto diversa da TMDB
### f126 The Discovery
- FOTO_CAST: Robert Redford: foto diversa da TMDB; Riley Keough: foto diversa da TMDB
### f129 Home Alone 2
- TITOLO: 'Home Alone 2' ≠ TMDB 'Mamma, ho riperso l'aereo - Mi sono smarrito a New York' / 'Home Alone 2: Lost in New York'
- FOTO_CAST: Macaulay Culkin: foto diversa da TMDB
### f132 Journey to the Center of the Earth
- DURATA: Nostro 84 min; TMDB 93, IMDb 93
### f138 The Spiderwick Chronicles
- FOTO_CAST: Mary-Louise Parker: foto diversa da TMDB
### f141 Margin Call
- FOTO_CAST: Paul Bettany: foto diversa da TMDB
### f144 Che bella giornata
- FOTO_CAST: Checco Zalone: foto diversa da TMDB
- DURATA: Nostro 90 min; TMDB 97, IMDb 97
### f147 Mr. Popper's Penguins
- FOTO_CAST: Angela Lansbury: foto diversa da TMDB
- DURATA: Nostro 88 min; TMDB 94, IMDb 94
### f150 Home Alone 3
- FOTO_CAST: Scarlett Johansson: foto diversa da TMDB
- DURATA: Nostro 95 min; TMDB 102, IMDb 102
### f453 The Hobbit: The Desolation of Smaug
- FOTO_CAST: Evangeline Lilly: foto diversa da TMDB
### f458 The Hunger Games: The Ballad of Songbirds & Snakes
- FOTO_CAST: Rachel Zegler: foto diversa da TMDB; Hunter Schafer: foto diversa da TMDB
### f169 Coach Carter
- DURATA: Nostro 105 min; TMDB 136, IMDb 136
### f174 Synecdoche, New York
- FOTO_CAST: Samantha Morton: foto diversa da TMDB
### f187 Cape Fear
- FOTO_CAST: Jessica Lange: foto diversa da TMDB
### f190 Apocalypse Now
- FOTO_CAST: Frederic Forrest: foto diversa da TMDB; Dennis Hopper: foto diversa da TMDB
### f196 Inside Men
- CAST: Non nel cast TMDB (top25): ['Baek Yoon-sik']; TMDB top: ['Lee Byung-hun']
- FOTO_CAST: Baek Yoon-sik: persona non nel cast TMDB
### f199 The Pianist
- FOTO_CAST: Emilia Fox: foto diversa da TMDB
### f208 King of New York
- DURATA?: Nostro 121 min; TMDB 106, IMDb 103
### f213 Being John Malkovich [id_corretto: {'da': 15196, 'a': 492}]
- FOTO_CAST: Cameron Diaz: foto diversa da TMDB
### f216 Cold in July
- FOTO_CAST: Don Johnson: foto diversa da TMDB
### f224 Big Fish [id_corretto: {'da': 576, 'a': 587}]
- FOTO_CAST: Ewan McGregor: foto diversa da TMDB; Albert Finney: foto diversa da TMDB; Jessica Lange: foto diversa da TMDB
### f230 Dead Man's Shoes
- FOTO_CAST: Paddy Considine: foto diversa da TMDB
### f236 Pulp Fiction
- FOTO_CAST: Uma Thurman: foto diversa da TMDB; Ving Rhames: foto diversa da TMDB
### f243 Dune
- FOTO_CAST: Rebecca Ferguson: foto diversa da TMDB
### f256 The Place Beyond the Pines [id_corretto: {'da': 109410, 'a': 97367}]
- ANNO: Nostro 2012; TMDB 2013
- FOTO_CAST: Bradley Cooper: foto diversa da TMDB; Eva Mendes: foto diversa da TMDB; Rose Byrne: foto diversa da TMDB; Dane DeHaan: foto diversa da TMDB
- ANNO_FONTI: TMDB 2013 ≠ IMDb 2012 (nostro 2012)
### f262 Independence Day
- FOTO_CAST: Randy Quaid: foto diversa da TMDB
### f265 First Man [id_corretto: {'da': 359724, 'a': 369972}]
- FOTO_CAST: Claire Foy: foto diversa da TMDB
### f272 21 Jump Street [id_corretto: {'da': 60308, 'a': 64688}]
- FOTO_CAST: Dave Franco: foto diversa da TMDB
### f278 Battle Royale
- CAST: Non nel cast TMDB (top25): ['Tatsuya Fujiwara']; TMDB top: ['Takeshi Kitano', 'Masanobu Ando', 'Hirohito Honda', 'Ryou Nitta', 'Sayaka Ikeda', 'Yukari Kanasawa']
- FOTO_CAST: Tatsuya Fujiwara: persona non nel cast TMDB
### f284 Blue Velvet
- FOTO_CAST: Dennis Hopper: foto diversa da TMDB
### f287 The Call
- POSTER_ALTRO_TITOLO: La copertina assomiglia di più a The Call (2020, id 575604, dist 3) che a id assegnato 158011 The Call (2013, dist 26). Candidati: [(3, 575604, 'The Call', '2020'), (19, 20981, 'The Call of Cthulhu', '2006'), (21, 9694, 'One Missed Call', '2003')]
### f305 Falling Down
- FOTO_CAST: Tuesday Weld: foto diversa da TMDB
### f311 Frailty
- ANNO: Nostro 2001; TMDB 2002
- FOTO_CAST: Jeremy Sumpter: foto diversa da TMDB
- ANNO_FONTI: TMDB 2002 ≠ IMDb 2001 (nostro 2001)
### f324 Her [id_corretto: {'da': 113705, 'a': 152601}]
- FOTO_CAST: Scarlett Johansson: foto diversa da TMDB; Amy Adams: foto diversa da TMDB
### f333 La La Land
- FOTO_CAST: Emma Stone: foto diversa da TMDB
### f336 Lost in Translation
- FOTO_CAST: Scarlett Johansson: foto diversa da TMDB
### f339 Minari [id_corretto: {'da': 615457, 'a': 615643}]
- ANNO: Nostro 2020; TMDB 2021
- ANNO_FONTI: TMDB 2021 ≠ IMDb 2020 (nostro 2020)
### f345 Nocturnal Animals
- FOTO_CAST: Amy Adams: foto diversa da TMDB
### f354 Portrait of a Lady on Fire
- FOTO_CAST: Luàna Bajrami: foto diversa da TMDB
### f380 The Zone of Interest
- FOTO_CAST: Sandra Hüller: foto diversa da TMDB
### f384 The Invisible Guest
- ANNO: Nostro 2016; TMDB 2017
- ANNO_FONTI: TMDB 2017 ≠ IMDb 2016 (nostro 2016)
### f388 Twin Peaks
- ID_TMDB_SOSPETTO: 2 indizi concordi: l'id TMDB assegnato (1923) potrebbe riferirsi a un altro titolo/omonimo
- TITOLO: 'Twin Peaks' ≠ TMDB 'Twin Peaks: Fuoco cammina con me' / 'Twin Peaks: Fire Walk with Me'
- POSTER_ALTRO_TITOLO: La copertina assomiglia di più a Twin Peaks (1989, id 452522, dist 1) che a id assegnato 1923 Twin Peaks: Fuoco cammina con me (1992, dist 22). Candidati: [(1, 452522, 'Twin Peaks', '1989'), (23, 1923, 'Twin Peaks: Fire Walk with Me', '1992'), (23, 569865, "Return to 'Twin Peaks'", '2007')]
### f404 Under the Silver Lake
- FOTO_CAST: Andrew Garfield: foto diversa da TMDB; Riley Keough: foto diversa da TMDB; Topher Grace: foto diversa da TMDB
### f407 Vanilla Sky [id_corretto: {'da': 601, 'a': 1903}]
- FOTO_CAST: Tom Cruise: foto diversa da TMDB; Cameron Diaz: foto diversa da TMDB
### f413 Wind River [id_corretto: {'da': 391713, 'a': 395834}]
- FOTO_CAST: Elizabeth Olsen: foto diversa da TMDB; Jon Bernthal: foto diversa da TMDB
### f426 The Gentlemen
- ANNO: Nostro 2019; TMDB 2020
- ANNO_FONTI: TMDB 2020 ≠ IMDb 2019 (nostro 2019)
### f439 Dune: Part Three
- CAST: Non nel cast TMDB (top25): ['Austin Butler']; TMDB top: ['Timothée Chalamet', 'Zendaya', 'Jason Momoa', 'Florence Pugh', 'Rebecca Ferguson', 'Isaach de Bankolé']
- FOTO_CAST: Zendaya: foto diversa da TMDB; Florence Pugh: foto diversa da TMDB; Austin Butler: persona non nel cast TMDB
### f463 Harry Potter and the Order of the Phoenix
- FOTO_CAST: Rupert Grint: foto diversa da TMDB; Ralph Fiennes: foto diversa da TMDB
### f469 The Amazing Spider-Man
- FOTO_CAST: Andrew Garfield: foto diversa da TMDB; Emma Stone: foto diversa da TMDB
### f472 Spider-Man: Far From Home
- FOTO_CAST: Tom Holland: foto diversa da TMDB; Zendaya: foto diversa da TMDB
### f475 Harry Potter and the Chamber of Secrets
- FOTO_CAST: Rupert Grint: foto diversa da TMDB
### f478 Harry Potter and the Deathly Hallows: Part 2
- FOTO_CAST: Rupert Grint: foto diversa da TMDB; Ralph Fiennes: foto diversa da TMDB

## SERIE TV

### s121 The Penguin
- CAST: Non nel cast TMDB: ['Eugene Solfanelli']; TMDB top: ['Colin Farrell', 'Cristin Milioti', 'Rhenzy Feliz', "Deirdre O'Connell", 'Clancy Brown', 'Carmen Ejogo', 'Shohreh Aghdashloo', 'Theo Rossi']
### s123 His Dark Materials
- ANNO_FINE: Nostro 2022; TMDB 2023 (serie Ended)
- GENERI: Nostri ['Fantasy', 'Avventura', 'Mistero']; TMDB ['Fantascienza', 'Dramma', 'Azione']
### s120 The Mentalist
- CAST: Non nel cast TMDB: ['Adrianne Palicki', 'Jared Padalecki', 'Fredric Lehne', 'Jensen Ackles', 'Amanda Tapping', 'Misha Collins', 'Mark Sheppard', 'Loretta Devine', 'Julian Richings', 'Sebastian Spence', 'Amber Benson', 'Richard Libertini']; TMDB top: ['Simon Baker', 'Robin Tunney', 'Tim Kang', 'Owain Yeoman', 'Amanda Righetti', 'Joe Adler', 'Aunjanue Ellis-Taylor', 'Michael Gaston']
### s1 Breaking Bad
- CAST: Non nel cast TMDB: ['Aaron Hill', 'Harry Groener']; TMDB top: ['Bryan Cranston', 'Aaron Paul', 'Anna Gunn', 'RJ Mitte', 'Dean Norris', 'Betsy Brandt', 'Bob Odenkirk', 'Jonathan Banks']
- FOTO_CAST: Foto diversa da TMDB: ['Giancarlo Esposito']
### s3 Prison Break
- COERENZA: Completata ma visti 90/89
- EPISODI_STAGIONE: Nostro [22, 22, 13, 23, 9]; TMDB [22, 22, 13, 22, 9]
- EPISODI?: Nostro 89; TMDB 88, IMDb 90
### s4 Friends
- COERENZA: Completata ma visti 235/234
- EPISODI_STAGIONE: Nostro [24, 24, 25, 24, 24, 25, 24, 24, 23, 17]; TMDB [24, 24, 25, 23, 23, 23, 23, 23, 23, 17]
- CAST: Non nel cast TMDB: ['Steve Zahn', 'Michael McKean', 'Jana Marie Hupp', 'Carlo Imperato', 'Brittney Powell', 'Lea Thompson']; TMDB top: ['Jennifer Aniston', 'Courteney Cox', 'Lisa Kudrow', 'Matt LeBlanc', 'Matthew Perry', 'David Schwimmer', 'James Michael Tyler', 'Elliott Gould']
### s5 The Last Dance
- CREATORI: Nostri ['Jason Hehir']; TMDB ['Michael Tollin']
### s6 Game of Thrones
- COERENZA: Completata ma visti 74/73
- CAST: Non nel cast TMDB: ['Sean Bean', 'Mark Addy']; TMDB top: ['Peter Dinklage', 'Kit Harington', 'Nikolaj Coster-Waldau', 'Lena Headey', 'Emilia Clarke', 'Maisie Williams', 'Isaac Hempstead Wright', 'Sophie Turner']
### s7 La casa di carta
- EPISODI_STAGIONE: Nostro [9, 6, 8, 8, 10]; TMDB [15, 16, 10]
- FOTO_CAST: Foto diversa da TMDB: ['Rodrigo de la Serna']
### s8 Better Call Saul
- CAST: Non nel cast TMDB: ['Alex Désert', 'Elisha Yaffe', 'Chris Mulkey', 'Jim Beaver']; TMDB top: ['Bob Odenkirk', 'Jonathan Banks', 'Rhea Seehorn', 'Patrick Fabian', 'Michael Mando', 'Giancarlo Esposito', 'Michael McKean', 'Tony Dalton']
- FOTO_CAST: Foto diversa da TMDB: ['Giancarlo Esposito']
### s10 Lost
- COERENZA: Completata ma visti 121/115
- EPISODI_STAGIONE: Nostro [24, 23, 22, 13, 16, 17]; TMDB [24, 24, 23, 13, 17, 17]
- FOTO_CAST: Foto diversa da TMDB: ['Evangeline Lilly']
- EPISODI?: Nostro 115; TMDB 118, IMDb 121
### s11 Band of Brothers
- CAST: Non nel cast TMDB: ['Andrew-Lee Potts', 'Paul Herzberg', 'William Armstrong']; TMDB top: ['Michael Cudlitz', 'Rick Gomez', 'Scott Grimes', 'Damian Lewis', 'Ron Livingston', 'James Madio', 'Neal McDonough', 'Donnie Wahlberg']
### s13 Squid Game
- COERENZA: Completata ma visti 22/15
- EPISODI_STAGIONE: Nostro [9, 6]; TMDB [9, 7, 6]
- CAST: Non nel cast TMDB: ['임시완']; TMDB top: ['Lee Jung-jae', 'Lee Byung-hun', 'Kang Ae-sim', 'Kang Ha-neul', 'David Lee', 'Anupam Tripathi', 'Lee Doo-seok', 'John Choi']
- EPISODI?: Nostro 15; TMDB 22, IMDb 22
### s14 Peaky Blinders
- CAST: Non nel cast TMDB: ['Dave Simon']; TMDB top: ['Cillian Murphy', 'Paul Anderson', 'Sophie Rundle', 'Helen McCrory', 'Finn Cole', 'Ian Peck', 'Ned Dennehy', "Natasha O'Keeffe"]
### s15 The Expanse
- CAST: Non nel cast TMDB: ['Paulo Costanzo', 'Sara Mitich']; TMDB top: ['Steven Strait', 'Dominique Tipper', 'Wes Chatham', 'Shohreh Aghdashloo', 'Cas Anvar', 'Frankie Adams', 'Cara Gee', 'Shawn Doyle']
### s17 Lost in Space
- CREATORI: Nostri ['Zack Estrin', 'Matt Sazama', 'Burk Sharpless']; TMDB ['Irwin Allen']
### s19 The Office
- EPISODI_STAGIONE: Nostro [6, 22, 25, 14, 28, 26, 26, 24, 25]; TMDB [6, 22, 23, 14, 26, 24, 24, 24, 23]
- EPISODI?: Nostro 196; TMDB 186, IMDb 191
### s20 Happy Days
- COERENZA: Completata ma visti 255/247
- EPISODI_STAGIONE: Nostro [16, 23, 23, 23, 27, 27, 25, 22, 22, 22, 17]; TMDB [16, 23, 23, 24, 26, 27, 25, 22, 22, 22, 22]
- EPISODI?: Nostro 247; TMDB 252, IMDb 255
### s21 I Robinson
- COERENZA: Completata ma visti 197/201
- EPISODI_STAGIONE: Nostro [24, 25, 25, 24, 26, 26, 26, 25]; TMDB [24, 25, 25, 23, 25, 26, 25, 24]
- CREATORI: Nostri ['Matt Groening']; TMDB ['Bill Cosby', 'Michael J. Leeson', 'Ed. Weinberger']
- EPISODI?: Nostro 201; TMDB 197, IMDb 197
### s22 Vis a Vis
- ANNO_FINE: Nostro 2020; TMDB 2019 (serie Ended)
- EPISODI_STAGIONE: Nostro [11, 13, 8, 8, 8]; TMDB [11, 13, 8, 8]
- POSTER_ALTRO_TITOLO: La copertina assomiglia di più a Dream Productions (2024, id 255868, dist 20) che a id 62455 Vis a vis - Il prezzo del riscatto (2015, dist 24)
### s23 Sex Education
- FOTO_CAST: Foto diversa da TMDB: ['Mimi Keene', 'Tanya Reynolds']
### s24 Succession
- FOTO_CAST: Foto diversa da TMDB: ['Dagmara Dominczyk']
### s27 Elite
- CAST: Non nel cast TMDB: ['María Pedraza', 'Miguel Herrán']; TMDB top: ['Omar Ayuso', 'Itzan Escamilla', 'Valentina Zenere', 'André Lamoglia', 'Miguel Bernardeau', 'Arón Piper', 'Georgina Amorós', 'Claudia Salas']
- FOTO_CAST: Foto diversa da TMDB: ['Ester Expósito']
### s28 Rick and Morty
- EPISODI_STAGIONE: Nostro [11, 10, 10, 10, 10, 10, 10, 10]; TMDB [11, 10, 10, 10, 10, 10, 10, 10, 10] (serie in corso)
- CAST: Non nel cast TMDB: ['Lil Pump', 'Dana Carvey', 'John Oliver', 'Werner Herzog', 'Stephen Colbert', 'Nathan Fillion']; TMDB top: ['Chris Parnell', 'Spencer Grammer', 'Sarah Chalke', 'Justin Roiland', 'Kari Wahlgren', 'Tom Kenny', 'Ryan Ridley', 'Dan Harmon']
- EPISODI?: Nostro 81; TMDB 91, IMDb 94
### s29 Lucifer
- EPISODI_STAGIONE: Nostro [13, 18, 24, 10, 16, 10]; TMDB [13, 18, 26, 10, 16, 10]
- CAST: Non nel cast TMDB: ['Jon Sklaroff']; TMDB top: ['Tom Ellis', 'Lauren German', 'Kevin Alejandro', 'D. B. Woodside', 'Lesley-Ann Brandt', 'Rachael Harris', 'Aimee Garcia', 'Scarlett Estevez']
- FOTO_CAST: Foto diversa da TMDB: ['Tom Welling']
- EPISODI?: Nostro 91; TMDB 93, IMDb 93
### s31 How I Met Your Mother
- EPISODI_STAGIONE: Nostro [22, 22, 20, 24, 24, 24, 23, 23, 23]; TMDB [22, 22, 20, 24, 24, 24, 24, 24, 24]
- CAST: Non nel cast TMDB: ['Abby Elliott']; TMDB top: ['Josh Radnor', 'Neil Patrick Harris', 'Jason Segel', 'Alyson Hannigan', 'Cobie Smulders', 'Lyndsy Fonseca', 'David Henrie', 'Cristin Milioti']
- EPISODI?: Nostro 205; TMDB 208, IMDb 208
### s32 The Walking Dead
- CAST: Non nel cast TMDB: ['Jon Bernthal', 'Jeffrey DeMunn']; TMDB top: ['Norman Reedus', 'Melissa McBride', 'Lauren Cohan', 'Danai Gurira', 'Andrew Lincoln', 'Christian Serratos', 'Josh McDermitt', 'Chandler Riggs']
### s34 WandaVision
- FOTO_CAST: Foto diversa da TMDB: ['Elizabeth Olsen', 'Randall Park']
### s36 Mad Men
- EPISODI_STAGIONE: Nostro [13, 13, 13, 13, 12, 12, 14]; TMDB [13, 13, 13, 13, 13, 13, 14]
- EPISODI?: Nostro 90; TMDB 92, IMDb 92
### s38 The Leftovers
- FOTO_CAST: Foto diversa da TMDB: ['Margaret Qualley']
### s39 Suits
- CAST: Non nel cast TMDB: ['Laura Allen']; TMDB top: ['Gabriel Macht', 'Rick Hoffman', 'Sarah Rafferty', 'Patrick J. Adams', 'Meghan, Duchess of Sussex', 'Gina Torres', 'Amanda Schull', 'Wendell Pierce']
### s41 Outer Banks
- FOTO_CAST: Foto diversa da TMDB: ['Madison Bailey']
### s42 Barry
- CAST: Non nel cast TMDB: ['Nicholas Sean Johnny', 'Tyler Jacob Moore']; TMDB top: ['Bill Hader', 'Sarah Goldberg', 'Anthony Carrigan', 'Henry Winkler', 'Stephen Root', "D'Arcy Carden", 'Michael Irby', 'Darrell Britt-Gibson']
### s43 Person of Interest
- FOTO_CAST: Foto diversa da TMDB: ['Sarah Shahi']
### s45 Vikings
- CAST: Non nel cast TMDB: ['Gabriel Byrne']; TMDB top: ['Katheryn Winnick', 'Gustaf Skarsgård', 'Alexander Ludwig', 'Georgia Hirst', 'Peter Franzén', 'Alex Høgh Andersen', 'Jordan Patrick Smith', 'Clive Standen']
### s46 The Good Place
- CAST: Non nel cast TMDB: ['Emily Arlook', 'Jill Remez', 'Paulina Lule', 'Hayden Szeto', 'George Basil']; TMDB top: ['Kristen Bell', 'Ted Danson', 'William Jackson Harper', 'Jameela Jamil', 'Manny Jacinto', "D'Arcy Carden", 'Marc Evan Jackson', 'Tiya Sircar']
### s49 Manhunt
- CREATORI: Nostri ['Andrew Zinnes', 'David Coggeshall']; TMDB ['Andrew Sodroski', 'Jim Clemente', 'Tony Gittelson']
- CAST: Non nel cast TMDB: ['Trieste Kelly Dunn', 'Mike Pniewski']; TMDB top: ['Gethin Anthony', 'Arliss Howard', 'Kelly Jenrette', 'Cameron Britton', 'Sam Worthington', 'Ness Bautista', 'Jeremy Bobb', 'Ben Weber']
### s51 Gli anelli del potere
- EPISODI_STAGIONE: Nostro [8, 8]; TMDB [8, 8, 8] (serie in corso)
- EPISODI?: Nostro 16; TMDB 24, IMDb 25
### s52 The Last of Us
- CAST: Non nel cast TMDB: ['Jerry Wasserman']; TMDB top: ['Bella Ramsey', 'Pedro Pascal', 'Gabriel Luna', 'Isabela Merced', 'Young Mazino', 'Rutina Wesley', 'Samuel Hoeksema', 'Danny Ramirez']
### s54 Invincible
- EPISODI_STAGIONE: Nostro [8, 8, 8, 8]; TMDB [8, 8, 8, 8, 0] (serie in corso)
- CAST: Non nel cast TMDB: ['Jon Hamm', 'Mahershala Ali', 'Max Burkholder', 'Lauren Cohan', 'Micah Aliling', 'Scoot McNairy']; TMDB top: ['Steven Yeun', 'Sandra Oh', 'J.K. Simmons', 'Gillian Jacobs', 'Walton Goggins', 'Grey DeLisle', 'Chris Diamantopoulos', 'Ross Marquand']
### s57 House of the Dragon
- EPISODI_STAGIONE: Nostro [10, 8]; TMDB [10, 8, 8] (serie in corso)
- EPISODI?: Nostro 18; TMDB 26, IMDb 27
### s58 Fringe
- EPISODI_STAGIONE: Nostro [20, 22, 22, 22, 13]; TMDB [20, 23, 22, 22, 13]
- CAST: Non nel cast TMDB: ['David Caruso', 'Emily Procter', 'Eddie Cibrian', 'Omar Benson Miller', 'Rory Cochrane', 'Jonathan Togo', 'Adam Rodriguez', 'Khandi Alexander', 'Sofia Milos', 'Rex Linn', 'Eva LaRue', 'Josh Hopkins']; TMDB top: ['Anna Torv', 'Joshua Jackson', 'Jasika Nicole', 'John Noble', 'Lance Reddick', 'Blair Brown', 'Leonard Nimoy', 'Seth Gabel']
- EPISODI?: Nostro 99; TMDB 100, IMDb 100
### s59 Doctor Who
- ANNO_FINE: Nostro 2022; TMDB 2021 (serie Ended)
### s62 Mindhunter
- CAST: Non nel cast TMDB: ['David H. Holmes', 'Julia Crockett', 'Jordan Gelber', "Thomas Philip O'Neill", 'Lee Sellars']; TMDB top: ['Jonathan Groff', 'Holt McCallany', 'Anna Torv', 'Sonny Valicenti', 'Stacey Roca', 'Cotter Smith', 'Hannah Gross', 'Joe Tuttle']
- FOTO_CAST: Foto diversa da TMDB: ['Anna Torv']
### s63 The Pitt
- EPISODI_STAGIONE: Nostro [15, 15]; TMDB [15, 15, 0] (serie in corso)
- FOTO_CAST: Foto diversa da TMDB: ['Supriya Ganesh', 'Fiona Dourif']
### s64 Black Mirror
- EPISODI_STAGIONE: Nostro [3, 3, 6, 6, 3, 5, 6]; TMDB [3, 4, 6, 6, 3, 5, 6] (serie in corso)
- EPISODI?: Nostro 32; TMDB 33, IMDb 34
### s65 Battlestar Galactica
- FOTO_CAST: Foto diversa da TMDB: ['Edward James Olmos']
### s67 Boardwalk Empire
- CAST: Non nel cast TMDB: ['Mark Harmon', 'Sean Murray', 'Michael Weatherly', 'Wilmer Valderrama', 'Katrina Law', 'Cote De Pablo', 'Brian Dietzen', 'Sasha Alexander', 'David McCallum', 'Pauley Perrette', 'Emily Wickersham', 'Lauren Holly']; TMDB top: ['Steve Buscemi', 'Kelly Macdonald', 'Michael Shannon', 'Shea Whigham', 'Stephen Graham', 'Vincent Piazza', 'Michael Kenneth Williams', 'Paul Sparks']
### s68 Gotham
- CAST: Non nel cast TMDB: ['Victoria Cartagena']; TMDB top: ['Ben McKenzie', 'Donal Logue', 'David Mazouz', 'Sean Pertwee', 'Robin Lord Taylor', 'Erin Richards', 'Camren Bicondova', 'Cory Michael Smith']
- POSTER_ALTRO_TITOLO: La copertina assomiglia di più a Gotham Tonight (2008, id 110419, dist 16) che a id 60708 Gotham (2014, dist 20)
### s69 Sons of Anarchy
- CAST: Non nel cast TMDB: ['Rupert Degas', 'Lorraine Pilkington', 'Mark DeCarlo', 'Charlie Schlatter', 'Tara Strong', '伊川東吾', 'Megan Cavanagh']; TMDB top: ['Charlie Hunnam', 'Katey Sagal', 'Tommy Flanagan', 'Mark Boone Junior', 'Kim Coates', 'Theo Rossi', 'Dayton Callie', 'Ron Perlman']
### s70 Oz
- CAST: Non nel cast TMDB: ['Ryan Ryno Templeton']; TMDB top: ['Lee Tergesen', 'Harold Perrineau', 'Dean Winters', 'Eamonn Walker', 'Ernie Hudson', 'Terry Kinney', 'Rita Moreno', 'J.K. Simmons']
### s71 The End of the F***ing World
- CREATORI: Nostri ['Charlie Covell']; TMDB ['Jonathan Entwistle']
### s75 The Night Of
- CAST: Non nel cast TMDB: ['Carter Hudson', 'Eleasha Gamble', 'Racquel Palmer', 'Chris Perfetti']; TMDB top: ['Riz Ahmed', 'John Turturro', 'Bill Camp', 'Jeannie Berlin', 'Poorna Jagannathan', 'Amara Karan', 'Syam M. Lafi', 'Paul Sparks']
### s76 Six Feet Under
- CAST: Non nel cast TMDB: ['Nicholas Burns', 'Julian Barratt', 'Claire Keelan', 'Richard Ayoade', 'Spencer Brown', 'Benedict Cumberbatch', 'Julia Davis', 'Stephen Mangan', 'Peter Sullivan', 'Ramon Tikaram', 'Mathew Horne', 'Montserrat Lombard']; TMDB top: ['Peter Krause', 'Michael C. Hall', 'Frances Conroy', 'Lauren Ambrose', 'Freddy Rodríguez', 'Mathew St. Patrick', 'Rachel Griffiths', 'Justina Machado']
### s77 Severance
- EPISODI_STAGIONE: Nostro [9, 10]; TMDB [9, 10, 0] (serie in corso)
- CAST: Non nel cast TMDB: ['Jeff McCarthy']; TMDB top: ['Adam Scott', 'Britt Lower', 'Tramell Tillman', 'Zach Cherry', 'Patricia Arquette', 'Jen Tullock', 'Dichen Lachman', 'John Turturro']
### s78 Banshee
- CAST: Non nel cast TMDB: ['James Purefoy', 'Dervla Kirwan', 'Nathaniel Parker', 'Sasha Behar', 'Charlie Creed-Miles', 'Obi Abili', 'Lisa Diveney', 'Stephen Hagan', 'Elijah Baker', 'Ivan Kaye', 'Ivanno Jeremiah', 'Clifford Barry']; TMDB top: ['Antony Starr', 'Ivana Miličević', 'Hoon Lee', 'Frankie Faison', 'Ulrich Thomsen', 'Matt Servitto', 'Lili Simmons', 'Ryann Shane']
### s79 Silo
- EPISODI_STAGIONE: Nostro [10, 10]; TMDB [10, 10, 10, 1] (serie in corso)
- FOTO_CAST: Foto diversa da TMDB: ['Jessica Brown Findlay']
- EPISODI?: Nostro 20; TMDB 31, IMDb 40
### s80 The OA
- CAST: Non nel cast TMDB: ['Anson Mount', 'Serinda Swan', 'Iwan Rheon', 'Isabelle Cornish', 'Ken Leung', 'Eme Ikwuakor', 'Sonya Balmores', 'Ellen Woglom', 'Henry Ian Cusick', 'Aidan Fiske', 'Bridger Zadina', 'Garret Sato']; TMDB top: ['Brit Marling', 'Jason Isaacs', 'Emory Cohen', 'Phyllis Smith', 'Patrick Gibson', 'Brendan Meyer', 'Brandon Perea', 'Will Brill']
### s81 Daredevil
- CAST: Non nel cast TMDB: ['Nikolai Nikolaeff', 'Gideon Emery', 'Kevin Nagle', 'Wendy Moniz', 'Adriane Lenox', 'Alex Falberg']; TMDB top: ['Charlie Cox', 'Deborah Ann Woll', 'Elden Henson', "Vincent D'Onofrio", 'Royce Johnson', 'Geoffrey Cantor', 'Jon Bernthal', 'Jay Ali']
### s82 Deadwood
- CAST: Non nel cast TMDB: ['Reece Dinsdale', 'Elizabeth Bennett', 'Clare Clifford', 'Frank Mills', 'Sheila Hancock', 'Charles Kay', 'Erika Hoffman', 'Ken Campbell', 'Susan Jameson', 'Reginald Marsh', 'Hugh Walters']; TMDB top: ['Timothy Olyphant', 'Ian McShane', 'Molly Parker', 'Jim Beaver', 'W. Earl Brown', 'Dayton Callie', 'Brad Dourif', 'John Hawkes']
- FOTO_CAST: Foto diversa da TMDB: ['John Thaw']
- PERSONAGGIO: ["John Thaw: 'Henry Willows' vs ['Sol Star']"]
### s83 The Shield
- CAST: Non nel cast TMDB: ['Ivan Sergei', 'Amanda Peet', 'Justin Kirk', 'Sarah Paulson', 'Jaime Pressly', 'Simon Rex', 'Bill Macy', 'Chad Willett', 'Elisa Donovan', 'Clayton Rohner', 'Kathryn Harrold', 'Lindsay Price']; TMDB top: ['Michael Chiklis', 'Catherine Dent', 'Walton Goggins', 'Michael Jace', 'Jay Karnes', 'Benito Martinez', 'CCH Pounder', 'Cathy Cahlin Ryan']
### s84 Utopia
- CREATORI: Nostri ['Gillian Flynn']; TMDB ['Dennis Kelly']
### s85 Atlanta
- CAST: Non nel cast TMDB: ['Will Forte', 'Kristen Schaal', 'January Jones', 'Cleopatra Coleman', 'Mel Rodriguez', 'Mary Steenburgen', 'Boris Kodjoe', 'Kenneth Choi', 'Leighton Meester', 'Alexandra Daddario', 'Fred Armisen']; TMDB top: ['Donald Glover', 'Brian Tyree Henry', 'LaKeith Stanfield', 'Zazie Beetz', 'Khris Davis', 'Katt Williams', 'Diane Sellers', 'Rick Holmes']
- FOTO_CAST: Foto diversa da TMDB: ['Keith L. Williams']
- PERSONAGGIO: ["Keith L. Williams: 'Jasper' vs ['Uncle Willy']"]
### s86 Fargo
- FOTO_CAST: Foto diversa da TMDB: ['Ewan McGregor']
### s88 Lupin
- EPISODI_STAGIONE: Nostro [5, 5, 7]; TMDB [10, 7, 8] (serie in corso)
- CAST: Non nel cast TMDB: ['Kamel Guenfoud', 'Grégoire Colin', 'Arthur Choisnet', 'Saïd Benchnafa', 'Mohamed Nouar', 'Ary Gabison', 'Xavier Gojo', 'Linda Massoz', 'Karim Lasmi', 'François Créton', 'Laurent Maurel']; TMDB top: ['Omar Sy', 'Ludivine Sagnier', 'Soufiane Guerrab', 'Shirine Boutella', 'Etan Simon', 'Antoine Gouy', 'Mamadou Haïdara', 'Hervé Pierre']
- EPISODI?: Nostro 17; TMDB 25, IMDb 25
### s89 The Last Kingdom
- CREATORI: Nostri ['Jack Bender', 'Michele Fazekas', 'Tara Butters']; TMDB ['Stephen Butchard']
- CAST: Non nel cast TMDB: ['찬열', '문가영', '도경수', '백현', '세훈', '장유상', '전수진', '김희정', '윤주상', '카이', '수호', '张艺兴']; TMDB top: ['Alexander Dreymon', 'Eliza Butterworth', 'Arnas Fedaravičius', 'Mark Rowley', 'Emily Cox', 'James Northcote', 'Millie Brady', 'Timothy Innes']
### s91 The Sopranos
- CAST: Non nel cast TMDB: ['Victor Spinetti', 'Roy Kinnear', 'Melvyn Hayes', 'Sheila Steafel', 'Jon Pertwee', 'Myfanwy Talog', 'Derek Griffiths', 'Christopher Plummer', 'Peter Hawkins', 'Mel Blanc']; TMDB top: ['James Gandolfini', 'Edie Falco', 'Jamie-Lynn Sigler', 'Robert Iler', 'Lorraine Bracco', 'Michael Imperioli', 'Steven Van Zandt', 'Tony Sirico']
### s93 24
- ANNO_FINE: Nostro 2010; TMDB 2014 (serie Ended)
- EPISODI_STAGIONE: Nostro [24, 24, 24, 24, 24, 24, 24, 24]; TMDB [24, 24, 24, 24, 24, 24, 24, 24, 12]
- CAST: Non nel cast TMDB: ['Yvonne Strahovski', 'Tate Donovan', 'John Terry']; TMDB top: ['Kiefer Sutherland', 'Mary Lynn Rajskub', 'Carlos Bernard', 'Dennis Haysbert', 'Elisha Cuthbert', 'Sarah Clarke', 'Kim Raver', 'James Morrison']
### s94 Brooklyn 99
- EPISODI_STAGIONE: Nostro [22, 23, 23, 21, 22, 18, 13, 9]; TMDB [22, 23, 23, 22, 22, 18, 13, 9]
- CAST: Non nel cast TMDB: ['Adam Sandler', 'Joe Theismann', 'Anthony Azizi']; TMDB top: ['Andy Samberg', 'Melissa Fumero', 'Terry Crews', 'Joe Lo Truglio', 'Stephanie Beatriz', 'Andre Braugher', 'Dirk Blocker', 'Joel McKinnon Miller']
- EPISODI?: Nostro 151; TMDB 152, IMDb 153
### s95 12 Monkeys
- CAST: Non nel cast TMDB: ['Wolfgang Kieling', 'Andrea Rau', 'Gernot Endemann', 'Karlheinz Lemken', 'Horst Hesslein', 'Paul Edwin Roth', 'Ferdinand Dux', 'Michael Gempart', 'Herbert Fleischmann', 'Gert Schaefer', 'Gerhard Olschewski', 'Rudolf Beiswanger']; TMDB top: ['Aaron Stanford', 'Amanda Schull', 'Barbara Sukowa', 'Emily Hampshire', 'Todd Stashwick', 'Andrew Gillies', 'Kirk Acevedo', 'Alisen Richmond-Peck']
### s100 The Americans
- CAST: Non nel cast TMDB: ['Charlie Hunnam', 'Johnny Lewis', 'Katey Sagal', 'Ron Perlman', 'Tommy Flanagan', 'Mark Boone Junior', 'Ryan Hurst', 'Kim Coates', 'Maggie Siff', 'Theo Rossi', 'Dayton Callie', 'David Labrava']; TMDB top: ['Keri Russell', 'Matthew Rhys', 'Holly Taylor', 'Keidrich Sellati', 'Noah Emmerich', 'Costa Ronin', 'Lev Gorn', 'Alison Wright']
### s102 Fallout
- EPISODI_STAGIONE: Nostro [8]; TMDB [8, 8] (serie in corso)
- CAST: Non nel cast TMDB: ['Sam Elliott', 'Tim McGraw', 'Faith Hill', 'Isabel May', 'LaMonica Garrett', 'Marc Rissmann', 'Audie Rick', 'James Landry Hébert', 'Dan Pfau', 'Dean Gosdin', 'Natalie Dickinson', 'Kamen Casey']; TMDB top: ['Ella Purnell', 'Aaron Moten', 'Moisés Arias', 'Walton Goggins', 'Frances Turner', 'Kyle MacLachlan', 'Dave Register', 'Leslie Uggams']
- EPISODI?: Nostro 8; TMDB 16, IMDb 17
### s103 Limitless
- GENERI: Nostri ['Crimine', 'Fantascienza', 'Thriller']; TMDB ['Dramma', 'Commedia', 'Azione']
### s104 Hannibal
- CAST: Non nel cast TMDB: ['Lance Henriksen', 'Tom Wisdom']; TMDB top: ['Mads Mikkelsen', 'Hugh Dancy', 'Laurence Fishburne', 'Caroline Dhavernas', 'Aaron Abrams', 'Scott Thompson', 'Gillian Anderson', 'Kacey Rohl']
### s105 BoJack Horseman
- CAST: Non nel cast TMDB: ['Jon Daly', 'Fred Tatasciore', 'Judy Greer', 'Minae Noji']; TMDB top: ['Will Arnett', 'Aaron Paul', 'Alison Brie', 'Amy Sedaris', 'Paul F. Tompkins', 'Adam Conover', 'Keith Olbermann', 'Patton Oswalt']
- FOTO_CAST: Foto diversa da TMDB: ['Alison Brie']
### s106 Gravity Falls
- EPISODI_STAGIONE: Nostro [20, 22]; TMDB [20, 20]
- EPISODI?: Nostro 42; TMDB 40, IMDb 41
### s107 Avatar: The Last Airbender
- CAST: Non nel cast TMDB: ['Jodi Carlisle']; TMDB top: ['Zach Tyler Eisen', 'Mae Whitman', 'Jack De Sena', 'Dante Basco', 'Dee Bradley Baker', 'Michaela Jill Murphy', 'Mako', 'Cricket Leigh']
### s108 Over the Garden Wall
- CAST: Non nel cast TMDB: ['Baz Ashmawy', 'Nancy Ashmawy']; TMDB top: ['Elijah Wood', 'Collin Dean', 'Melanie Lynskey', 'Samuel Ramey', 'Christopher Lloyd', 'Jack Jones', 'John Cleese', 'Sam Marin']
### s109 Eteros Ego
- ID_TMDB_SOSPETTO: 2 indizi concordi: l'id TMDB assegnato (90621) potrebbe riferirsi a un altro titolo/omonimo
- TITOLO: 'Eteros Ego' ≠ 'Έτερος Εγώ'/'Έτερος Εγώ'
- GENERI: Nostri ['Commedia', 'Romance']; TMDB ['Mistero', 'Crimine']
- CAST: Non nel cast TMDB: ['Μαριάννα Τουμασάτου']; TMDB top: ['Samuel Akinola', 'Kris Radanov', 'Polydoros Vogiatzis']
### s111 Aspirants
- CREATORI: Nostri ['Apoorv Singh Karki']; TMDB ['Arunabh Kumar', 'Shreyansh Pandey', 'Deepesh Sumitra Jagdish']
### s113 Persona
- ANNO_INIZIO: Nostro 2018; TMDB 2019
- EPISODI_STAGIONE: Nostro [4, 5]; TMDB [4] (serie in corso)
- EPISODI?: Nostro 9; TMDB 4, IMDb 4
### s114 Twin Peaks
- CAST: Non nel cast TMDB: ['Candy Clark']; TMDB top: ['Kyle MacLachlan', 'Michael Horse', 'Harry Goaz', 'Kimmy Robertson', 'Dana Ashbrook', 'Richard Beymer', 'Mädchen Amick', 'Peggy Lipton']
- FOTO_CAST: Foto diversa da TMDB: ['Harry Goaz']
### s116 Stranger Things
- FOTO_CAST: Foto diversa da TMDB: ['Winona Ryder', 'Millie Bobby Brown', 'Caleb McLaughlin', 'Charlie Heaton']
### s117 Black Sails
- CAST: Non nel cast TMDB: ['Mai Nakahara', '近藤孝行', 'Mamiko Noto', '皆川純子', 'Aya Hisakawa', '清水香里', 'Akeno Watanabe', 'かかずゆみ', 'Nobuyuki Hiyama', '山口太郎', '小谷津央典', '堀川仁']; TMDB top: ['Toby Stephens', 'Luke Arnold', 'Hannah New', 'Jessica Parker Kennedy', 'Toby Schmitz', 'Tom Hopper', 'Clara Paget', 'Zach McGowan']
### s118 The Queen's Gambit
- CAST: Non nel cast TMDB: ["Jonjo O'Neill", 'Madeline Holliday', 'Jenny Galloway', 'Steffen Mennekes', 'Johannes Franke']; TMDB top: ['Anya Taylor-Joy', 'Chloe Pirrie', 'Marcin Dorociński', 'Matthew Dennis Lewis', 'Russell Dennis Lewis', 'Dolores Carbonari', 'Janina Elkin', 'Harry Melling']
### s119 When They See Us
- CAST: Non nel cast TMDB: ['Josh Brener', 'Mary Elizabeth Winstead', 'Topher Grace', 'Helen Sadler', 'Hayley McLaughlin', 'Omid Abtahi', 'Christine Adams', 'Hakeem Kae-Kazim', 'Anastasia Foster', 'Neil Kaplan', 'G.K. Bowes', 'Courtenay Taylor']; TMDB top: ['Asante Blackk', 'Jharrel Jerome', 'Ethan Herisse', 'Marquis Rodriguez', 'Caleel Harris', 'Marsha Stephanie Blake', 'Michael Kenneth Williams', 'John Leguizamo']
### s126 The Mandalorian
- CAST: Non nel cast TMDB: ['John Beasley', 'Dmitrious Bistrevsky', 'Brian Posehn', 'Ryan Watson', 'Julia Jones', 'Isla Farris', 'Eugene Cordero', 'Aydrea Walden']; TMDB top: ['Pedro Pascal', 'Katee Sackhoff', 'Misty Rosas', 'Chris Bartlett', 'Carl Weathers', 'Emily Swallow', 'Brendan Wayne', 'Giancarlo Esposito']
### s127 Star Wars: The Clone Wars
- CAST: Non nel cast TMDB: ['David Tennant', 'Liam Neeson', 'Tom Kenny', 'George Takei']; TMDB top: ['Tom Kane', 'Matt Lanter', 'James Arnold Taylor', 'Dee Bradley Baker', 'Ashley Eckstein', 'Matthew Wood', "Terrence 'T.C.' Carson", 'Ian Abercrombie']
- FOTO_CAST: Foto diversa da TMDB: ['James Arnold Taylor']
### s128 And Then There Were None
- FOTO_CAST: Foto diversa da TMDB: ['Charles Dance']

## ANIME

### a1 Attack on Titan
- COERENZA: Somma episodi stagioni 89 ≠ totale 94
- PERSONAGGI: Non trovati su AniList: ['Levi Ackerman', 'Historia Reiss']. AniList main: ['Eren Yeager', 'Mikasa Ackerman', 'Armin Arlert']
### a5 Your Name
- POSTER?: Copertina poco simile a AniList (dist 29): verificare a vista
### a9 Made in Abyss
- PERSONAGGI: Non trovati su AniList: ['Prushka', 'Vueko']. AniList main: ['Reg', 'Riko']
### a21 Heavenly Delusion
- TITOLO: 'Heavenly Delusion' ≠ AniList 'Tengoku Daimakyou' / 'Tengoku Daimakyo' (MAL 53393)
### a25 Assassination Classroom
- PERSONAGGI: Non trovati su AniList: ['Karasuma', "Nagisa's madre"]. AniList main: ['Koro-sensei', 'Nagisa Shiota']
### a29 Hell's Paradise
- PERSONAGGI: Non trovati su AniList: ['Toma Sagiri']. AniList main: ['Gabimaru', 'Sagiri']
### a33 Blue Lock
- STUDIO: Nostri ['Eightbit']; AniList ['8-bit']
### a37 Tower of God
- PERSONAGGI: Non trovati su AniList: ['Evankhell', 'Prince Hansung Yu', 'Novick']. AniList main: ['Aguero Agnis Khun', 'Twenty-Fifth Baam', 'Rak Wraithraiser', 'Rachel']
### a41 One Punch Man
- COERENZA: Completato ma visti 24/36
- NUMERO_STAGIONI: Nostre 3 stagioni TV; AniList 4: [(2015, 12), (2019, 12), (2025, 12), (2027, None)]
- POSTER?: Copertina poco simile a AniList (dist 28): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Garou']
### a45 The Promised Neverland
- PERSONAGGI: Non trovati su AniList: ['Mujika', 'Sonju', 'Peter Ratri']. AniList main: ['Ray', 'Norman', 'Emma']
### a49 I Want to Eat Your Pancreas
- PERSONAGGI: Non trovati su AniList: ['Kyoko Yamauchi']. AniList main: ['Sakura Yamauchi', 'Haruki Shiga']
### a57 Sakamoto desu ga
- PERSONAGGI: Non trovati su AniList: ['Kubota', 'Fumihiko Hayabusa', 'Souma Aoyama']. AniList main: ['Sakamoto']
- FOTO_MANCANTE: Senza foto: ['Sakamoto']
### a61 Wonder Egg Priority
- PERSONAGGI: Non trovati su AniList: ['Kaoru', 'Fuku']. AniList main: ['Ai Ooto', 'Rika Kawai', 'Momoe Sawaki', 'Neiru Aonuma']
### a77 86
- TITOLO: '86' ≠ AniList '86: Eighty Six' / '86 EIGHTY-SIX' (MAL 41457)
### a81 Ao no Hako
- STUDIO: Nostri ['TMS Entertainment']; AniList ['Electric Circus']
- POSTER?: Copertina poco simile a AniList (dist 33): verificare a vista
- PERSONAGGI: Non trovati su AniList: ['Haruka Ninomiya']. AniList main: ['Chinatsu Kano', 'Taiki Inomata']
### a85 Banana Fish
- PERSONAGGI: Non trovati su AniList: ['Ibe']. AniList main: ['Ash Lynx', 'Eiji Okumura']
### a89 Bungou Stray Dogs
- EPISODI_STAGIONI: Nostre stagioni TV: [(2016, 12), (2016, 12), (2019, 12), (2023, 11), (2023, 11)] (tot 58); AniList catena TV: [(2016, 12), (2016, 12), (2019, 12), (2023, 13), (2023, 11)] (tot 60)
- PERSONAGGI: Non trovati su AniList: ['Odasaku', 'Fyodor Dostoevsky']. AniList main: ['Osamu Dazai', 'Ryuunosuke Akutagawa', 'Atsushi Nakajima', 'Doppo Kunikida']
### a93 Claymore
- POSTER?: Copertina poco simile a AniList (dist 29): verificare a vista
### a97 Devilman: Crybaby
- DURATA: Nostro 30; AniList 25
- POSTER?: Copertina poco simile a AniList (dist 29): verificare a vista
### a101 Fate/Zero
- EPISODI_STAGIONI: Nostre stagioni TV: [(2011, 13), (2012, 12)] (tot 25); AniList catena TV: [(2006, 24), (2011, 13), (2012, 12), (2014, 13), (2015, 13)] (tot 75)
- PERSONAGGI: Non trovati su AniList: ['Cu Chulainn']. AniList main: ['Artoria Pendragon', 'Gilgamesh', 'Kiritsugu Emiya', 'Iskandar', 'Kirei Kotomine', 'Waver Velvet', 'Irisviel von Einzbern', 'Diarmuid  Ua Duibhne']
### a105 Ginga Eiyuu Densetsu
- STUDIO: Nostri ['Artland']; AniList ['Production I.G']
### a113 Hajime no Ippo
- PERSONAGGI: Non trovati su AniList: ['Yuusuke Kimura']. AniList main: ['Ippo Makunouchi', 'Mamoru Takamura', 'Ichirou Miyata', 'Genji Kamogawa', 'Tatsuya Kimura', 'Masaru Aoki']
### a125 Komi-san
- TITOLO: 'Komi-san' ≠ AniList 'Komi-san wa, Komyushou desu.' / 'Komi Can’t Communicate' (MAL 48926)
- FOTO_PERSONAGGIO: Makeru Yamai (foto di AniList id 130874, personaggio id 130871)
### a128 Kusuriya no Hitorigoto
- EPISODI_STAGIONI: Nostre stagioni TV: [(2023, 24), (2024, 24)] (tot 48); AniList catena TV: [(2023, 24), (2025, 24), (2026, 12), (2027, 12)] (tot 72)
### a132 Monster
- PERSONAGGI: Non trovati su AniList: ['Inspector Lunge', 'Milch']. AniList main: ['Johan Liebert', 'Kenzou Tenma', 'Heinrich Runge', 'Anna Liebert', 'Eva Heinemann']
### a136 Nanatsu no Taizai
- EPISODI_STAGIONI: Nostre stagioni TV: [(2014, 24), (2018, 24), (2019, 24), (2021, 24), (2023, 24), (2024, 12)] (tot 132); AniList catena TV: [(2014, 24), (2016, 4), (2018, 24), (2019, 24), (2021, 24), (2023, 24), (2024, 12)] (tot 136)
- PERSONAGGI: Non trovati su AniList: ['Escanor', 'Zeldris', 'Estarossa']. AniList main: ['Ban', 'Meliodas', 'King', 'Diane', 'Elizabeth Liones', 'Gowther', 'Hawk']
### a140 Perfect Blue
- POSTER?: Copertina poco simile a AniList (dist 34): verificare a vista
- PERSONAGGI: Non trovati su AniList: ['Rei Todoroki']. AniList main: ['Mima Kirigoe']
### a144 Re:Zero
- TITOLO: 'Re:Zero' ≠ AniList 'Re:Zero kara Hajimeru Isekai Seikatsu' / 'Re:ZERO -Starting Life in Another World-' (MAL 31240)
### a148 Shangri-La Frontier
- PERSONAGGI: Non trovati su AniList: ['Kyouka Uto', 'Bella Wilhelmina Nono', 'Shiden Kunai', 'Elru']. AniList main: ['Rakurou Hizutome']
### a152 Sousou no Frieren
- NUMERO_STAGIONI: Nostre 2 stagioni TV; AniList 3: [(2023, 28), (2026, 10), (2027, None)]
### a156 Trigun
- EPISODI_STAGIONI: Nostre stagioni TV: [(1998, 26), (2023, 12), (2026, 12)] (tot 50); AniList catena TV: [(1998, 26)] (tot 26)
### a172 Sword Art Online
- PERSONAGGI: Non trovati su AniList: ['Sinon', 'Heathcliff', 'Alice Synthesis Thirty']. AniList main: ['Asuna Yuuki', 'Kazuto Kirigaya', 'Suguha Kirigaya']
- FOTO_MANCANTE: Senza foto: ['Eugeo']
### a2 One Piece
- COERENZA: Completato ma visti 1100/1172
- EPISODI_STAGIONI: Nostre stagioni TV: [(1999, 61), (2001, 8), (2001, 8), (2001, 14), (2001, 44), (2003, 17), (2003, 54), (2004, 57), (2006, 62), (2008, 59), (2008, 23), (2009, 14), (2009, 35), (2010, 60), (2011, 58), (2013, 54), (2014, 118), (2016, 36), (2017, 95), (2019, 12), (2019, 196), (2024, 70), (2026, 17)] (tot 1172); AniList catena TV: [(1999, None), (2024, 1)] (tot 1)
- POSTER?: Copertina poco simile a AniList (dist 28): verificare a vista
### a6 Jujutsu Kaisen
- COERENZA: Completato ma visti 47/59
- FOTO_MANCANTE: Senza foto: ['Yuta Okkotsu']
### a10 Horimiya
- POSTER?: Copertina poco simile a AniList (dist 27): verificare a vista
- FOTO_PERSONAGGIO: Sota Hori (foto di AniList id 66171, personaggio id 66969)
### a14 Fullmetal Alchemist Brotherhood
- FOTO_MANCANTE: Senza foto: ['Father']
### a18 Chainsaw Man
- PERSONAGGI: Non trovati su AniList: ['Quanxi', 'Nayuta']. AniList main: ['Makima', 'Denji', 'Power', 'Aki Hayakawa']
- FOTO_MANCANTE: Senza foto: ['Reze']
### a22 Naruto
- EPISODI_STAGIONI: Nostre stagioni TV: [(2002, 220), (2007, 500)] (tot 720); AniList catena TV: [(2002, 220), (2007, 500), (2017, 293), (None, None)] (tot 1013)
- PERSONAGGI: Non trovati su AniList: ['Tsunade', 'Minato Namikaze']. AniList main: ['Kakashi Hatake', 'Naruto Uzumaki', 'Sasuke Uchiha', 'Sakura Haruno']
- FOTO_PERSONAGGIO: Obito Uchiha (foto di AniList id 13, personaggio id 21122)
### a26 My Dress-Up Darling
- PERSONAGGI: Non trovati su AniList: ['Kaoruko Iikawa']. AniList main: ['Marin Kitagawa', 'Wakana Gojou']
### a30 Tokyo Revengers
- COERENZA: Completato ma visti 37/50
- EPISODI_STAGIONI: Nostre stagioni TV: [(2021, 24), (2023, 13), (2023, 13)] (tot 50); AniList catena TV: [(2021, 24), (2023, 13), (2023, 13), (2026, 13)] (tot 63)
- POSTER?: Copertina poco simile a AniList (dist 27): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Manjiro Sano (Mikey)', 'Ken Ryuguji (Draken)']
### a34 Terror in Resonance
- POSTER?: Copertina poco simile a AniList (dist 30): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Shibazaki']
### a38 Tomodachi Game
- STUDIO: Nostri ['LIDENFILMS']; AniList ['Okuruto Noboru']
- PERSONAGGI: Non trovati su AniList: ['Tenji Sanada', 'Chidubem Michael Ichinose', 'Manabu Yamamoto', 'Reko Kirifuda']. AniList main: ['Yuuichi Katagiri', 'Shiho Sawaragi', 'Tenji Mikasa', 'Yutori Kokorogi', 'Makoto Shibe']
### a42 My Hero Academia
- COERENZA: Completato ma visti 138/171
### a46 Demon Slayer
- COERENZA: Completato ma visti 55/64
- PERSONAGGI: Non trovati su AniList: ['Akaza']. AniList main: ['Tanjirou Kamado', 'Nezuko Kamado', 'Inosuke Hashibira', 'Zenitsu Agatsuma']
### a50 Mob Psycho 100
- POSTER?: Copertina poco simile a AniList (dist 28): verificare a vista
### a54 Deca-Dence
- PERSONAGGI: Non trovati su AniList: ['Fara', 'Minato Bell']. AniList main: ['Natsume', 'Kaburagi']
### a58 Inuyashiki
- FOTO_MANCANTE: Senza foto: ['Ichiro Inuyashiki', 'Hiro Shishigami', 'Shion Watanabe', 'Andou']
### a62 Death Parade
- PERSONAGGI: Non trovati su AniList: ['Chiyuki']. AniList main: ['Decim', 'Kurokami no Onna', 'Nona', 'Ginti']
### a70 Nanbaka
- CREATORI: Nostri ['Yokkaichi']; AniList staff ['Shou Futamata', 'Shinji Takamatsu', 'Mitsutaka Hirota', 'Takayuki Noguchi', 'Tomokazu Seki', 'Tetsuya Kakihara']
- EPISODI_STAGIONI: Nostre stagioni TV: [(2016, 13), (2017, 13)] (tot 26); AniList catena TV: [(2016, 13), (2017, 12)] (tot 25)
### a74 Yu-Gi-Oh ZEXAL
- STUDIO: Nostri ['Gallop']; AniList ['Studio Gallop']
- POSTER?: Copertina poco simile a AniList (dist 28): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Dr. Faker']
### a78 Angel Beats!
- PERSONAGGI: Non trovati su AniList: ['Iwasawa', 'Yui']. AniList main: ['Kanade Tachibana', 'Yuri Nakamura', 'Yui Yoshioka', 'Yuzuru Otonashi', 'Hideki Hinata', 'Ayato Naoi']
### a82 Ashita no Joe
- PERSONAGGI: Non trovati su AniList: ['Jose Mendoza']. AniList main: ['Joe Yabuki', 'Tooru Rikiishi', 'Danpei Tange', 'Youko Shiraki']
### a86 Black Clover
- STUDIO: Nostri ['Pierrot']; AniList ['Studio Pierrot']
- FOTO_MANCANTE: Senza foto: ['Klaus Lunettes']
### a90 5 Centimeters Per Second
- EPISODI: Nostro 1; AniList 3
- DURATA: Nostro 63; AniList 22
### a98 Edens Zero
- FOTO_MANCANTE: Senza foto: ['Pino']
### a102 Fruits Basket
- ANNO: Nostro prima stagione 2019; AniList 2001
- STUDIO: Nostri ['TMS Entertainment']; AniList ['Studio DEEN']
- EPISODI_STAGIONI: Nostre stagioni TV: [(2019, 25), (2020, 25), (2021, 13)] (tot 63); AniList catena TV: [(2001, 26)] (tot 26)
- FOTO_PERSONAGGIO: Yuki Sohma (foto di AniList id 209, personaggio id 208); Shigure Sohma (foto di AniList id 209, personaggio id 206); Kagura Sohma (foto di AniList id 209, personaggio id 366); Hatsuharu Sohma (foto di AniList id 209, personaggio id 369); Momiji Sohma (foto di AniList id 209, personaggio id 367); Hatori Sohma (foto di AniList id 209, personaggio id 368)
### a106 Gintama
- FOTO_PERSONAGGIO: Otae Shimura (foto di AniList id 673, personaggio id 2944)
### a110 Kaiji
- TITOLO: 'Kaiji' ≠ AniList 'Gyakkyou Burai Kaiji: Ultimate Survivor' / 'Kaiji - Ultimate Survivor' (MAL 3002)
- PERSONAGGI: Non trovati su AniList: ['Sakazaki', 'Endo']. AniList main: ['Kaiji Itou']
### a114 Hellsing Ultimate
- PERSONAGGI: Non trovati su AniList: ['Integra Hellsing']. AniList main: ['Alucard', 'Seras Victoria', 'Integra Fairbrook Wingates Hellsing']
### a118 Inazuma Eleven
- CREATORI: Nostri ['Level-5']; AniList staff ['Akihiro Hino', 'Takuzou Nagano', 'Katsuhito Akiyama', 'Atsuhiro Tomioka', 'Yuuji Ikeda', 'Masafumi Mima']
- PERSONAGGI: Non trovati su AniList: ['Judou Domon']. AniList main: ['Mamoru Endou', 'Shuuya Gouenji', 'Yuuto Kidou']
- FOTO_MANCANTE: Senza foto: ['Ryugo Someoka']
### a122 Katekyou Hitman Reborn!
- FOTO_PERSONAGGIO: Kyoko Sasagawa (foto di AniList id 1861, personaggio id 1857)
- FOTO_MANCANTE: Senza foto: ['Basil']
### a126 Ghost in the Shell
- POSTER?: Copertina poco simile a AniList (dist 30): verificare a vista
- PERSONAGGI: Non trovati su AniList: ['Saito']. AniList main: ['Motoko Kusanagi', 'Batou', 'Togusa']
### a133 Mushishi
- NUMERO_STAGIONI: Nostre 2 stagioni TV; AniList 3: [(2005, 26), (2014, 10), (2014, 10)]
- POSTER?: Copertina poco simile a AniList (dist 31): verificare a vista
### a137 Noragami
- PERSONAGGI: Non trovati su AniList: ['Kofuku']. AniList main: ['Yato', 'Hiyori Iki', 'Yukine']
### a141 Plastic Memories
- PERSONAGGI: Non trovati su AniList: ['Michiru', 'Kazuki']. AniList main: ['Isla', 'Tsukasa Mizugaki']
### a145 Saiki Kusuo no Psi-nan
- POSTER?: Copertina poco simile a AniList (dist 30): verificare a vista
### a149 Shigatsu wa Kimi no Uso
- POSTER?: Copertina poco simile a AniList (dist 33): verificare a vista
### a153 Tenkuu no Shiro Laputa
- PERSONAGGI: Non trovati su AniList: ['Zio Pom']. AniList main: ['Pazu', 'Sheeta', 'Dola', 'Muska']
### a157 Uchuu Kyoudai
- PERSONAGGI: Non trovati su AniList: ['Kenji Matsuo']. AniList main: ['Mutta Nanba', 'Hibito Nanba']
### a161 Yahari Ore no Seishun Love Comedy
- TITOLO: 'Yahari Ore no Seishun Love Comedy' ≠ AniList 'Yahari Ore no Seishun Love Come wa Machigatteiru. Zoku: Kitto, Onnanoko wa Osatou to Spice to Suteki na Nanika de Dekiteiru' / 'My Teen Romantic Comedy SNAFU TOO! OVA' (MAL 33161)
- ANNO: Nostro prima stagione 2013; AniList 2016
- PERSONAGGI: Non trovati su AniList: ['Saika Totsuka']. AniList main: ['Hachiman Hikigaya', 'Iroha Isshiki']
### a165 Kenpuu Denki Berserk
- PERSONAGGI: Non trovati su AniList: ['Femto']. AniList main: ['Guts', 'Griffith', 'Casca']
- FOTO_MANCANTE: Senza foto: ['Guts', 'Griffith', 'Casca', 'Judeau', 'Pippin', 'Corkus', 'Rickert']
### a169 Kaoru Hana wa Rin to Saku
- STUDIO: Nostri ['Bibury Animation Studio']; AniList ['CloverWorks']
- PERSONAGGI: Non trovati su AniList: ['Wako Uehara', 'Kotaro Kanetsugu', 'Rui Kishi']. AniList main: ['Kaoruko Waguri', 'Rintarou Tsumugi']
### a173 Fate/stay night: Unlimited Blade Works
- EPISODI_STAGIONI: Nostre stagioni TV: [(2014, 12), (2015, 13)] (tot 25); AniList catena TV: [(2006, 24), (2011, 13), (2012, 12), (2014, 13), (2015, 13)] (tot 75)
### a3 Hunter x Hunter
- STUDIO: Nostri ['Madhouse']; AniList ['Nippon Animation']
- PERSONAGGI: Non trovati su AniList: ['Meruem', 'Biscuit Krueger']. AniList main: ['Killua Zoldyck', 'Kurapika', 'Gon Freecss', 'Leorio Paradinight']
### a7 Dr. Stone
- COERENZA: Completato ma visti 53/95
- PERSONAGGI: Non trovati su AniList: ['Ryusui Nanami']. AniList main: ['Senkuu Ishigami', 'Kohaku', 'Chrome', 'Tsukasa Shishiou', 'Taiju Ooki', 'Yuzuriha Ogawa']
- FOTO_MANCANTE: Senza foto: ['Ukyo Saionji']
### a19 Gurren Lagann
- PERSONAGGI: Non trovati su AniList: ['Gimmy', 'Darry']. AniList main: ['Kamina', 'Simon', 'Youko Littner', 'Nia Teppelin']
### a23 JoJo's Bizarre Adventure
- COERENZA: Completato ma visti 190/191
- EPISODI_STAGIONI: Nostre stagioni TV: [(2012, 26), (2014, 48), (2016, 39), (2018, 39), (2022, 38), (2026, 1)] (tot 191); AniList catena TV: [(2012, 26), (2014, 24), (2015, 24), (2016, 39), (2018, 39), (2021, 12), (2022, 26), (2026, 1), (2026, 11)] (tot 202)
- PERSONAGGI: Non trovati su AniList: ['Josuke Higashikata', 'Giorno Giovanna', 'Jolyne Cujoh', 'Kakyoin Noriaki', 'Polnareff', 'Iggy', 'Killer Queen (Kira)', 'Bruno Bucciarati']. AniList main: ['Joseph Joestar', 'Dio Brando', 'Jonathan Joestar', 'Caesar Zeppeli']
- FOTO_MANCANTE: Senza foto: ['Jotaro Kujo']
### a27 Summertime Rendering
- PERSONAGGI: Non trovati su AniList: ['Ryunosuke Ushijima', 'Doi']. AniList main: ['Mio Kofune', 'Shinpei Ajiro', 'Hizuru Minakata', 'Ushio Kofune']
### a31 Kanata no Astra
- FOTO_PERSONAGGIO: Yunhua Lu (foto di AniList id 157848, personaggio id 139436)
### a35 Spy x Family
- COERENZA: Completato ma visti 37/50
- STAGIONE: 'Spy x Family Part 2': nostro 2022/12 ep; AniList 'SPY×FAMILY Part 2' 2022/13 ep
- STAGIONE: 'Spy x Family Season 2': nostro 2023/13 ep; AniList 'SPY×FAMILY Season 2' 2023/12 ep
- PERSONAGGI: Non trovati su AniList: ['Fiona Frost', 'Melinda Desmond']. AniList main: ['Yor Forger', 'Anya Forger', 'Loid Forger']
- FOTO_PERSONAGGIO: Bond Forger (foto di AniList id 138102, personaggio id 138101)
### a39 Btooom!
- PERSONAGGI: Non trovati su AniList: ['Natsu Kiyomizu', 'Kira', 'Zaji Kira']. AniList main: ['Himiko', 'Ryouta Sakamoto']
- FOTO_PERSONAGGIO: Himiko Kinoshita (foto di AniList id 52941, personaggio id 74431)
### a43 God Eater
- CREATORI: Nostri ['Bandai Namco']; AniList staff ['Takayuki Hirao', 'Kentarou Waki', 'Takayuki Hirao', 'Gou Shiina', 'OLDCODEX', 'Masato Nagamori']
- PERSONAGGI: Non trovati su AniList: ['Erina Yumizuru']. AniList main: ['Alisa Ilichina Amiella', 'Lenka Utsugi']
### a47 Pluto
- DURATA: Nostro 45; AniList 60
- POSTER?: Copertina poco simile a AniList (dist 34): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Brau1589']
### a51 No Game No Life
- PERSONAGGI: Non trovati su AniList: ['Kurami Zell']. AniList main: ['Shiro', 'Sora', 'Jibril', 'Stephanie Dola']
### a55 Prison School
- PERSONAGGI: Non trovati su AniList: ['Gakuto Sudo']. AniList main: ['Takehito Morokuzu', 'Kiyoshi Fujino', 'Jouji Nezu', 'Reiji Andou', 'Shingo Wakamoto']
### a59 Toradora
- POSTER?: Copertina poco simile a AniList (dist 27): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Ryuji Takasu', 'Taiga Aisaka', 'Minori Kushieda', 'Yusaku Kitamura', 'Ami Kawashima']
### a63 Charlotte
- POSTER?: Copertina poco simile a AniList (dist 28): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Jojiro Takajo']
### a67 Overlord
- COERENZA: Completato ma visti 52/53
### a75 3-gatsu no Lion
- FOTO_MANCANTE: Senza foto: ['Kyoko Kubo']
### a79 Ao Ashi
- PERSONAGGI: Non trovati su AniList: ['Yu Aoi', 'Gabriel Ichijo', 'Yukichi Otomo']. AniList main: ['Ashito  Aoi']
- FOTO_PERSONAGGIO: Kuroda Junnosuke (foto di AniList id 253947, personaggio id 280424)
### a83 Baccano!
- POSTER?: Copertina poco simile a AniList (dist 31): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Czeslaw Meyer']
### a87 Bleach
- EPISODI_STAGIONI: Nostre stagioni TV: [(2004, 366), (2022, 13), (2023, 13), (2024, 14), (2026, 3)] (tot 409); AniList catena TV: [(2004, 366), (2022, 13), (2023, 13), (2024, 14), (2026, 10)] (tot 416)
- POSTER?: Copertina poco simile a AniList (dist 35): verificare a vista
### a91 Chi. Chikyuu no Undou ni Tsuite
- PERSONAGGI: Non trovati su AniList: ['Fuiba', 'Albert', 'Nastazja']. AniList main: ['Rafał', 'Badeni', 'Nowak', 'Oczy', 'Jolenta', 'Draka', 'Schmitt']
- FOTO_MANCANTE: Senza foto: ['Yosaf']
### a99 Enen no Shouboutai
- STAGIONE: 'Stagione 3 Parte 1': nostro 2023/12 ep; AniList 'Enen no Shouboutai: San no Shou' 2025/12 ep
- STAGIONE: 'Stagione 3 Parte 2': nostro 2023/13 ep; AniList 'Enen no Shouboutai: San no Shou Part 2' 2026/13 ep
- PERSONAGGI: Non trovati su AniList: ['Shuya Kanamori']. AniList main: ['Iris', 'Shinra Kusakabe', 'Arthur Boyle', 'Maki Oze', 'Tamaki Kotatsu', 'Akitaru Oubi', 'Takehisa Hinawa']
### a103 Fumetsu no Anata e
- STAGIONE: 'Stagione 3': nostro 2023/22 ep; AniList 'Fumetsu no Anata e Season 3' 2025/22 ep
- PERSONAGGI: Non trovati su AniList: ['Bon', 'Rean']. AniList main: ['Fushi']
### a107 Golden Kamuy
- PERSONAGGI: Non trovati su AniList: ['Otonoshin Koito']. AniList main: ['Saichi Sugimoto', 'Asirpa', 'Yoshitake Shiraishi']
### a123 Kingdom
- EPISODI_STAGIONI: Nostre stagioni TV: [(2012, 38), (2013, 39), (2020, 26), (2022, 27)] (tot 130); AniList catena TV: [(2012, 38), (2013, 39), (2020, 26), (2022, 26), (2024, 13), (2025, 13), (None, None)] (tot 155)
- PERSONAGGI: Non trovati su AniList: ['Xin', 'Wang Ben']. AniList main: ['Xin Li', 'Lei Qiang', 'Zheng Ying', 'Liao Diao He']
- FOTO_PERSONAGGIO: Wang Jian (foto di AniList id 65443, personaggio id 132056)
### a174 Innocence: Ghost in the Shell 2
- POSTER?: Copertina poco simile a AniList (dist 30): verificare a vista
### a130 Magi
- TITOLO: 'Magi' ≠ AniList 'Mahou Sensei Negima!' / 'Negima!' (MAL 157)
- ANNO: Nostro prima stagione 2012; AniList 2005
- CREATORI: Nostri ['Shinobu Ohtaka']; AniList staff ['Ken Akamatsu', 'Youta Tsuruoka', 'Shinkichi Mitsumune', 'Hiroaki Sakurai', 'Miku Ooshima', 'Yui Horie']
- STUDIO: Nostri ['A-1 Pictures', 'LAY-DUCE']; AniList ['Xebec']
- EPISODI_STAGIONI: Nostre stagioni TV: [(2012, 25), (2013, 25), (2016, 13)] (tot 63); AniList catena TV: [(2005, 26), (2006, 26), (2017, 12)] (tot 64)
- PERSONAGGI: Non trovati su AniList: ['Alibaba Saluja', 'Aladdin', 'Morgiana', 'Sinbad', "Ja'far", 'Kougyoku Ren', 'Judal', 'Hakuryuu Ren']. AniList main: ['Negi Springfield', 'Asuna Kagurazaka', 'Nodoka Miyazaki', 'Yue Ayase', 'Konoka Konoe']
### a134 Mushoku Tensei
- EPISODI_STAGIONI: Nostre stagioni TV: [(2021, 11), (2021, 12), (2023, 12)] (tot 35); AniList catena TV: [(2021, 11), (2021, 12), (2023, 13), (2024, 12), (2026, 14), (2027, None)] (tot 62)
### a138 Oshi no Ko
- EPISODI_STAGIONI: Nostre stagioni TV: [(2023, 11), (2024, 12), (2026, 11)] (tot 34); AniList catena TV: [(2023, 11), (2024, 13), (2026, 11), (None, None)] (tot 35)
- PERSONAGGI: Non trovati su AniList: ['Gorou']. AniList main: ['Kana Arima', 'Aquamarine Hoshino', 'Ruby Hoshino']
### a142 Psycho-Pass
- EPISODI_STAGIONI: Nostre stagioni TV: [(2012, 22), (2014, 11), (2019, 8)] (tot 41); AniList catena TV: [(2012, 22), (2014, 11), (2019, 8), (2020, 3)] (tot 44)
### a146 Seishun Buta Yarou
- TITOLO: 'Seishun Buta Yarou' ≠ AniList 'Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo Minai' / 'Rascal Does Not Dream of Bunny Girl Senpai' (MAL 37450)
### a150 Slam Dunk
- PERSONAGGI: Non trovati su AniList: ['Eiji Sawakita']. AniList main: ['Hanamichi Sakuragi', 'Ryouta Miyagi', 'Hisashi Mitsui', 'Kaede Rukawa', 'Takenori Akagi']
### a154 Tensei shitara Slime Datta Ken
- STUDIO: Nostri ['Eight Bit']; AniList ['8-bit']
- EPISODI_STAGIONI: Nostre stagioni TV: [(2018, 24), (2021, 12), (2021, 12), (2024, 12)] (tot 60); AniList catena TV: [(2018, 24), (2021, 12), (2021, 12), (2024, 24), (2026, 24), (2027, None)] (tot 96)
- FOTO_MANCANTE: Senza foto: ['Hakuro']
### a162 Yuu☆Yuu☆Hakusho
- FOTO_PERSONAGGIO: Toguro (foto di AniList id 7176, personaggio id 8716)
### a166 Usagi Drop
- FOTO_MANCANTE: Senza foto: ['Daikichi Kawachi', 'Rin Kaga']
### a170 Tongari Boushi no Atelier
- STUDIO: Nostri ['Studio non ancora confermato']; AniList ['BUG FILMS']
- POSTER?: Copertina poco simile a AniList (dist 29): verificare a vista
- PERSONAGGI: Non trovati su AniList: ['Agott']. AniList main: ['Qifrey', 'Coco']
### a8 Vinland Saga
- PERSONAGGI: Non trovati su AniList: ['Thorfinn', 'Arnheid', 'Gudrid', 'Sverkel']. AniList main: ['Thorfinn Karlsefni', 'Askeladd', 'Canute Svenson']
- FOTO_PERSONAGGIO: Thors (foto di AniList id 13021, personaggio id 10138)
- FOTO_MANCANTE: Senza foto: ['Einar']
### a12 Parasyte
- PERSONAGGI: Non trovati su AniList: ["Shinichi's madre"]. AniList main: ['Shinichi Izumi', 'Migi']
### a16 Death Note
- FOTO_PERSONAGGIO: L (foto di AniList id 71, personaggio id 36309); Soichiro Yagami (foto di AniList id 80, personaggio id 1927)
### a20 Cyberpunk: Edgerunners
- STUDIO: Nostri ['Studio Trigger']; AniList ['TRIGGER']
### a24 Love is War
- COERENZA: Completato ma visti 37/40
- EPISODI_STAGIONI: Nostre stagioni TV: [(2019, 12), (2020, 12), (2022, 13)] (tot 37); AniList catena TV: [(2019, 12), (2020, 12), (2022, 13), (2023, 4)] (tot 41)
- PERSONAGGI: Non trovati su AniList: ['Nagisa Kaguya (madre)']. AniList main: ['Kaguya Shinomiya', 'Chika Fujiwara', 'Yuu Ishigami', 'Miyuki Shirogane']
### a28 Classroom of the Elite
- COERENZA: Completato ma visti 24/54
- NUMERO_STAGIONI: Nostre 4 stagioni TV; AniList 5: [(2017, 12), (2022, 13), (2024, 13), (2026, 16), (None, None)]
### a32 Solo Leveling
- PERSONAGGI: Non trovati su AniList: ['Thomas Andre', 'Liu Zhigang', 'Christopher Reed', 'Beru']. AniList main: ['Jin-U Seong']
- FOTO_MANCANTE: Senza foto: ['Sung Jinwoo', 'Go Gunhee', 'Woo Jinchul', 'Yoo Jinho', 'Baek Yoonho', 'Sung Jinah', 'Sung Il-Hwan']
### a36 Dororo
- PERSONAGGI: Non trovati su AniList: ['Tahomaru']. AniList main: ['Hyakkimaru', 'Dororo']
- FOTO_MANCANTE: Senza foto: ['Nui no Kata', 'Itachi']
### a40 Grand Blue
- PERSONAGGI: Non trovati su AniList: ['Motoharu Kotobuki']. AniList main: ['Chisa Kotegawa', 'Iori Kitahara', 'Kouhei Imamura', 'Aina Yoshiwara']
### a44 Ao Haru Ride
- PERSONAGGI: Non trovati su AniList: ['Aya Murao']. AniList main: ['Kou Mabuchi', 'Futaba Yoshioka']
### a48 Josee to Tora to Sakana-tachi
- POSTER?: Copertina poco simile a AniList (dist 33): verificare a vista
- PERSONAGGI: Non trovati su AniList: ['Mai']. AniList main: ['Josee', 'Tsuneo Suzukawa']
### a52 Anohana
- TITOLO: 'Anohana' ≠ AniList 'Ano Hi Mita Hana no Namae wo Bokutachi wa Mada Shiranai.' / 'Anohana: The Flower We Saw That Day' (MAL 9989)
- CREATORI: Nostri ['Mari Okada']; AniList staff ['Chouheiwa Busters', 'Tatsuyuki Nagai', 'Masayoshi Tanaka', 'Yukie Hiyamizu', 'Kaori Kuroki', 'Takayoshi Fukushima']
### a56 Howl's Moving Castle
- POSTER?: Copertina poco simile a AniList (dist 32): verificare a vista
- PERSONAGGI: Non trovati su AniList: ['Strega delle Lande', 'Principe Justin']. AniList main: ['Howl', 'Sophie Hatter']
- FOTO_MANCANTE: Senza foto: ['Sophie Hatter', 'Howl', 'Calcifer', 'Markl', 'Madame Suliman']
### a60 Odd Taxi
- PERSONAGGI: Non trovati su AniList: ['Odokawa']. AniList main: ['Hiroshi Odokawa']
### a64 Evangelion
- POSTER?: Copertina poco simile a AniList (dist 34): verificare a vista
- FOTO_PERSONAGGIO: Gendo Ikari (foto di AniList id 89, personaggio id 1257)
### a80 Ao no Exorcist
- NUMERO_STAGIONI: Nostre 4 stagioni TV; AniList 5: [(2011, 25), (2017, 12), (2024, 12), (2024, 12), (2025, 12)]
### a88 Boruto
- TITOLO: 'Boruto' ≠ AniList 'BORUTO: NARUTO NEXT GENERATIONS' / 'Boruto: Naruto Next Generations' (MAL 34566)
- CREATORI: Nostri ['Masashi Kishimoto']; AniList staff ['Ukyou Kodachi', 'Mikio Ikemoto', 'Noriyuki Abe', 'Hiroyuki Yamashita', 'Toshirou Fujii', 'Masayuki Kouda']
- POSTER?: Copertina poco simile a AniList (dist 31): verificare a vista
- FOTO_PERSONAGGIO: Shikadai Nara (foto di AniList id 2007, personaggio id 121442)
- FOTO_MANCANTE: Senza foto: ['Konohamaru Sarutobi', 'Sumire Kakei', 'Delta', 'Jigen']
### a92 Clannad
- PERSONAGGI: Non trovati su AniList: ['Ushio Okazaki']. AniList main: ['Tomoya Okazaki', 'Nagisa Furukawa', 'Tomoyo Sakagami', 'Fuuko Ibuki', 'Kyou Fujibayashi', 'Kotomi Ichinose', 'Youhei Sunohara', 'Ryou Fujibayashi']
### a96 Dandadan
- POSTER?: Copertina poco simile a AniList (dist 28): verificare a vista
### a100 Fairy Tail
- PERSONAGGI: Non trovati su AniList: ['Zeref Dragneel']. AniList main: ['Erza Scarlet', 'Natsu Dragneel', 'Lucy Heartfilia', 'Gray Fullbuster', 'Happy', 'Wendy Marvell', 'Charlés']
### a104 Gachiakuta
- STUDIO: Nostri ['Bones']; AniList ['bones film']
- PERSONAGGI: Non trovati su AniList: ['Zanka', 'Guy']. AniList main: ['Enjin', 'Rudo', 'Riyou Reaper', 'Zanka Nijiku']
### a108 Great Pretender
- CREATORI: Nostri ['Hirotaka Adachi']; AniList staff ['Hiro Kaburagi', 'Ryouji Masuyama', 'Ryouta Kosawa', 'Yoshiyuki Sadamoto', 'Hirotaka Katou', 'Keita Shimizu']
- PERSONAGGI: Non trovati su AniList: ['Dorothy MacKaren']. AniList main: ['Laurent Thierry', 'Abigail Jones', 'Makoto Edamura', 'Cynthia Moore']
### a112 Haikyuu!!
- PERSONAGGI: Non trovati su AniList: ['Kotaro Bokuto']. AniList main: ['Shouyou Hinata', 'Tobio Kageyama']
### a116 Houseki no Kuni
- PERSONAGGI: Non trovati su AniList: ['Kongo Sensei']. AniList main: ['Phosphophyllite']
### a127 Koutetsujou no Kabaneri
- PERSONAGGI: Non trovati su AniList: ['Ayame']. AniList main: ['Mumei', 'Ikoma']
### a131 Mahou Shoujo Madoka Magica
- FOTO_MANCANTE: Senza foto: ['Kyubey']
### a143 Rainbow: Nisha Rokubou no Shichinin
- PERSONAGGI: Non trovati su AniList: ['Kunihiro Ishihara', 'Mario Anjou', 'Joe Wakabayashi', 'Heitai Suzuki', 'Ryuji Hyodo', 'Denkichi Maeda']. AniList main: ['Rokurouta Sakuragi', 'Mario Minakami', 'Jou Yokosuka', 'Noboru Maeda', 'Tadayoshi Tooyama', 'Ryuuji Nomoto', 'Mansaku Matsuura']
### a147 Sen to Chihiro no Kamikakushi
- POSTER?: Copertina poco simile a AniList (dist 31): verificare a vista
- FOTO_MANCANTE: Senza foto: ['Kamaji']
### a151 Soul Eater
- PERSONAGGI: Non trovati su AniList: ['Medusa']. AniList main: ['Death the Kid', 'Maka Albarn', 'Soul Eater Evans', 'Black☆Star', 'Tsubaki Nakatsukasa', 'Patricia Thompson', 'Elizabeth Thompson']
- FOTO_PERSONAGGIO: Liz Thompson (foto di AniList id 8444, personaggio id 8445)
### a155 Tonari no Totoro
- FOTO_MANCANTE: Senza foto: ['Nekobus']
### a159 Vivy: Fluorite Eye's Song
- CREATORI: Nostri ['Wit Studio']; AniList staff ['Tappei Nagatsuki', 'Eiji Umehara', 'loundraw', 'Shinpei Ezaki', 'Yuusuke Kubo', 'Eiji Umehara']
- PERSONAGGI: Non trovati su AniList: ['Momoka']. AniList main: ['Vivy', 'Matsumoto']
### a163 Zom 100
- TITOLO: 'Zom 100' ≠ AniList 'Zom 100: Zombie ni Naru Made ni Shitai 100 no Koto' / 'Zom 100: Bucket List of the Dead' (MAL 54112)
- PERSONAGGI: Non trovati su AniList: ['Himeko Souya', 'Kencho Yamada']. AniList main: ['Shizuka Mikazuki', 'Akira Tendou', 'Beatrix Amerhauser', 'Kenichirou Ryuuzaki']
### a167 Mononoke Hime
- PERSONAGGI: Non trovati su AniList: ['Moro']. AniList main: ['San', 'Ashitaka']
### a171 Dead Dead Demon's Dededede Destruction
- STUDIO: Nostri ['Science SARU']; AniList ['Production +h']
- PERSONAGGI: Non trovati su AniList: ['Kaname Furube']. AniList main: ['Ouran Nakagawa', 'Kadode Koyama', 'Keita Ooba']

## MANGA

### m1 Slam Dunk
- CAPITOLI: Somma nostri capitoli 188; AniList 276
### m2 Solo Leveling
- CAPITOLI_SOSPETTI: 28/28 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI: Somma nostri capitoli 28; AniList 201
### m3 La ragazza in riva al mare
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m4 20th Century Boys
- CAPITOLI?: Edizione 'Deluxe edition': somma capitoli 265; originale 249
### m5 Blame
- CAPITOLI?: Edizione 'Master edition': somma capitoli 67; originale 1
### m6 Blue Lock
- VOLUMI_INTERNI: totalVols 34 ma elenco volumi con capitoli ne ha 42
### m7 The Killer Inside
- CAPITOLI_SOSPETTI: 11/11 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m8 La fine del mondo e prima dell'alba
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m9 Il prezzo di una vita
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m10 Chainsaw Man
- CAPITOLI: Somma nostri capitoli 208; AniList 232
### m18 Shaman King
- CAPITOLI_SOSPETTI: 35/35 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI?: Edizione 'Final edition': somma capitoli 35; originale 288
### m21 Tokyo Revengers
- VOLUMI_INTERNI: totalVols 31 ma elenco volumi con capitoli ne ha 37
- CAPITOLI: Somma nostri capitoli 319; AniList 279
### m23 Alita
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m29 Tower of God
- VOLUMI_INTERNI: totalVols 500 ma elenco volumi con capitoli ne ha 17
- CAPITOLI_SOSPETTI: 16/17 volumi con 1 solo capitolo (probabile segnaposto): [11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
### m30 Ashita no Joe
- CAPITOLI_SOSPETTI: 13/13 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI?: Edizione 'Perfect edition': somma capitoli 13; originale 171
### m31 Blue Period
- CAPITOLI_SOSPETTI: 11/18 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 5, 5]
### m36 Fullmetal Alchemist
- CAPITOLI?: Edizione 'Ultimate deluxe': somma capitoli 108; originale 116
### m38 Homunculus
- CAPITOLI_SOSPETTI: 15/15 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI: Somma nostri capitoli 15; AniList 166
### m40 Houseki no Kuni
- CAPITOLI: Somma nostri capitoli 108; AniList 120
### m41 I Am Hero
- CAPITOLI_SOSPETTI: 22/22 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI: Somma nostri capitoli 22; AniList 265
### m43 Jagaaaaaan
- CAPITOLI_SOSPETTI: 13/14 volumi con 1 solo capitolo (probabile segnaposto): [7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI: Somma nostri capitoli 20; AniList 163
### m45 Jujutsu Kaisen
- VOLUMI_INTERNI: totalVols 30 ma elenco volumi con capitoli ne ha 33
- CAPITOLI: Somma nostri capitoli 297; AniList 272
### m46 Juujika no Rokunin
- CAPITOLI_SOSPETTI: 14/14 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI: Somma nostri capitoli 14; AniList 234
- AUTORI: Nostri ['Autore non confermato']; AniList ['Shiryuu  Nakatake', 'Frederic Malet']
### m48 Mushishi
- CAPITOLI: Somma nostri capitoli 50; AniList 1
- GENERI: Nostri ['Fantasy', 'Mistero', 'Slice of Life']; AniList ['Horror']
- AUTORI: Nostri ['Yuki Urushibara']; AniList ['Kurage Asazuke']
### m49 Real
- CAPITOLI_SOSPETTI: 16/16 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
### m50 Sekai no Owari no Hajimari ni
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Autore non confermato']; AniList ['Kei Tanaka']
### m51 Record of Ragnarok
- CAPITOLI_SOSPETTI: 26/26 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
### m53 Sun-Ken Rock
- CAPITOLI_SOSPETTI: 25/25 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI: Somma nostri capitoli 25; AniList 181
### m55 The Horizon
- CAPITOLI_SOSPETTI: 3/3 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1]
- CAPITOLI?: Edizione 'Box': somma capitoli 3; originale 21
- AUTORI: Nostri ['Autore non confermato']; AniList ['Ji-Hun Jeong', 'Abigail Blackman']
### m57 Dededemon Dededestruction
- CAPITOLI_SOSPETTI: 12/12 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m62 Hanako-kun
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m65 Komi-san
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m68 Rurouni Kenshin
- CAPITOLI_SOSPETTI: 22/22 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI?: Edizione 'Perfect edition': somma capitoli 22; originale 259
### m69 Frieren
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m70 MPD Psycho
- CAPITOLI_SOSPETTI: 24/24 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- CAPITOLI: Somma nostri capitoli 24; AniList 147
### m72 Utsuro no Hako to Zero no Maria
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Autore non confermato']; AniList ['Eiji Mikage', 'Tetsuo', 'Luke Baker', 'Thien Thanh', 'Thuy Tram', 'Maarubi']
### m73 Classroom of the Elite
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
### m74 Your Talent Is Mine
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Autore non confermato']; AniList ['Hao Fan', 'Wei CC', 'Jian Shen Wu Di']
### m75 The Beginning After the End
- CAPITOLI_SOSPETTI: 6/6 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1]
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m76 Leveling Up with the Gods
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m77 Poison Dragon
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m78 Return of the Crazy Demon
- AUTORI: Nostri ['Autore non confermato']; AniList ['JP', 'Hi Lee', 'Jin-Seong Yu', 'Ra-Gi Yun', 'Ra-Gi Yun']
### m79 Return of the Unrivaled Spear Knight
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m80 Solo Max-Level Newbie
- AUTORI: Nostri ['Sadoyeon']; AniList ['WAN.Z', 'Swing Bat', 'Maslow']
### m81 A Returner's Magic Should Be Special
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
### m82 Great Mage Returns After 4000 Years
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Autore non confermato']; AniList ['Barnicle', 'Deok-Yong Kim', 'Nakhasan']
### m83 Nano Machine
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Han Jung Hoon', 'Bak Jong Hee']; AniList ['Geobalhan', 'Geumgangbulgoe', 'Hanjung Worya', 'Alexandra Dickmann']
### m84 Legend of the Northern Blade
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Autore non confermato']; AniList ['Hae-Min', 'U-Gak', 'Son']
### m85 Omniscient Reader's Viewpoint
- CAPITOLI_SOSPETTI: 4/4 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1]
### m86 Mercenary Enrollment
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m87 God Game
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Autore non confermato']; AniList ['Shuu Miyazaki', 'Nanakusa']
### m88 Her Summon
- VOLUMI_INTERNI: totalVols 117 ma elenco volumi con capitoli ne ha 1
- AUTORI: Nostri ['Autore non confermato']; AniList ['Jin-Jun Park']
### m89 Reverend Insanity
- CAPITOLI: Somma nostri capitoli 22; AniList 96 (serie in corso)
### m90 Lord of Mysteries
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Cuttlefish That Loves Diving']; AniList ['Chun Ba', 'Yuanyan de Qiqiu', 'Ai Qianshui de Wuzei']
### m91 Age of Adepts
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m92 House of Horrors
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- AUTORI: Nostri ['Autore non confermato']; AniList ['Miyako Cojima']
### m93 Warlock of the Magus World
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m94 Radiant
- CAPITOLI: Somma nostri capitoli 148; AniList 1
- GENERI: Nostri ['Fantasy', 'Azione', 'Avventura']; AniList ['Hentai', 'Romance']
- AUTORI: Nostri ['Tony Valente']; AniList ['Niiro Ikuhana']
### m98 Birth of the Demonic Sword
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m99 Galaxias
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- GENERI: Nostri ['Sci-Fi']; AniList ['Action', 'Adventure', 'Fantasy']
- AUTORI: Nostri ['Autore non confermato']; AniList ['Ao Hatezaka', 'Nate Derr', 'Jan Ivan Concepcion', 'Katherine Tran']
### m95 Aqualung
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m96 Orfani
- CAPITOLI_SOSPETTI: 16/16 volumi con 1 solo capitolo (probabile segnaposto): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)
### m97 Qwest
- CAPITOLI_MANCANTI: Nessun dato capitoli per volume
- NON_TROVATO: AniList: titolo non riconosciuto (titolo italiano/alternativo?)

## LIBRI

### b1 Il Piccolo Libro dell'Investimento
- NON_TROVATO: Open Library: nessun risultato
### b2 Il Cigno Nero
- GENERE: Genere mancante
- NON_TROVATO: Open Library: nessun risultato
### b3 The Wheel of Time
- PAGINE: Numero pagine mancante
- GENERE: Genere mancante
- NON_TROVATO: Open Library: nessun risultato
### b10 Aqualung
- AUTORE: Autore mancante/non confermato: 'Autore non confermato'
- PAGINE: Numero pagine mancante
### b11 Orfani
- PAGINE: Numero pagine mancante
### b12 Qwest
- PAGINE: Numero pagine mancante
- NON_TROVATO: Open Library: nessun risultato
