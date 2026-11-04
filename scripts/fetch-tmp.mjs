import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const H = { apikey: 'sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', Authorization: 'Bearer sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', 'x-vault-key': 'xZ0qWUo6S3wgD2R7qLJJ1T_hc_C75-8eZTUZGWkfJU0', 'Content-Type': 'application/json', Prefer: 'return=representation' };
const VP = {"b1": {"0": 15.2}, "b2": {"0": 22}, "b3": {"0": 38, "1": 48, "2": 48, "3": 48, "4": 48, "5": 48, "6": 48, "7": 48, "8": 48, "9": 48, "10": 48, "11": 48, "12": 48, "13": 48, "14": 48}, "b4": {"0": 16}, "b5": {"0": 35}, "b6": {"0": 26, "1": 26}, "b7": {}, "b8": {"0": 26, "1": 28, "2": 26, "3": 26, "4": 26}, "b9": {"0": 12}, "b10": {"0": 16, "1": 19, "2": 19, "3": 17}, "b11": {"0": 27, "1": 27, "2": 27, "3": 27, "4": 27, "5": 27, "6": 27, "7": 27, "8": 27, "9": 27, "10": 27, "11": 27, "12": 5.9, "13": 5.9, "14": 5.9, "15": 5.9, "16": 5.9, "17": 5.9, "18": 5.9, "19": 5.9, "20": 5.9, "21": 5.9, "22": 5.9, "23": 5.9, "24": 5.9, "25": 5.9, "26": 5.9, "27": 23, "28": 28}, "b12": {"0": 18, "1": 18, "2": 16}}; const TI = {"b4": "I 4 Pilastri dell'Indipendenza Finanziaria", "b7": "La Torre Nera", "b8": "Il Trono di Spade", "b9": "Padre Ricco Padre Povero"};
const out = {};
for (const id of Object.keys(VP)) {
  for (let t = 0; t < 3; t++) {
    const r = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?id=eq.' + id + '&select=id,data,rev', { headers: H });
    const row = (await r.json())[0]; if (!row) { out[id] = 'riga mancante'; break; }
    const d = Object.assign({}, row.data, { volPrices: VP[id] }); if (TI[id]) d.title = TI[id]; delete d.pricePerVol;
    const u = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?id=eq.' + id + '&rev=eq.' + row.rev, { method: 'PATCH', headers: H, body: JSON.stringify({ data: d, device: 'claude' }) });
    const j = await u.json();
    if (u.ok && j[0]) { out[id] = { ok: true, title: j[0].data.title, n: Object.keys(j[0].data.volPrices || {}).length }; break; }
    out[id] = 'tentativo ' + t + ' HTTP ' + u.status;
  }
}
writeFileSync('data/tmp/audit.json', JSON.stringify(out));
console.log('fatto');
