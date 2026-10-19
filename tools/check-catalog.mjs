// Verifies the P array in index.html matches api/_catalog.js (prices, variants, default stock).
import fs from 'node:fs';
import { PRODUCTS } from '../api/_catalog.js';
const html = fs.readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const block = html.match(/const P=\[([\s\S]*?)\];\nconst SLUG/)[1];
const P = eval('[' + block + ']');
let bad = 0;
for (const p of P) {
  const c = PRODUCTS[p.id]; if (!c) { console.log('missing server product', p.id); bad++; continue; }
  for (const [v, x] of Object.entries(p.v)) {
    const y = c.v[v]; if (!y || y.p !== x.p || (!c.parts && y.s !== x.s)) { console.log('mismatch', p.id, v, x, y); bad++; }
  }
  if (Object.keys(p.v).length !== Object.keys(c.v).length) { console.log('variant count', p.id); bad++; }
}
if (P.length !== Object.keys(PRODUCTS).length) { console.log('product count differs'); bad++; }
console.log(bad ? 'FAIL' : 'catalog in sync'); process.exit(bad ? 1 : 0);
