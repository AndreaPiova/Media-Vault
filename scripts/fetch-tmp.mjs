import { writeFileSync, mkdirSync } from 'fs';
mkdirSync('data/tmp', { recursive: true });
const H = { apikey: 'sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', Authorization: 'Bearer sb_publishable_Grif0vaKG2WpPehNog4uMQ_GqpSmUJx', 'x-vault-key': 'xZ0qWUo6S3wgD2R7qLJJ1T_hc_C75-8eZTUZGWkfJU0' };
const lb = await fetch('https://znfopdihrmfgweqabeqm.supabase.co/rest/v1/items?select=id,data,rev&cat=eq.libri&order=id.asc', { headers: H });
writeFileSync('data/tmp/audit.json', JSON.stringify(await lb.json()));
console.log('fatto');
