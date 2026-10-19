// Local test of the order/stock/admin API against a fake Upstash REST server and a mocked Resend.
import http from 'node:http';
const hash = {}, kv = {}, lists = {};
const srv = http.createServer((req, res) => {
  let body = ''; req.on('data', d => body += d); req.on('end', () => {
    const cmds = JSON.parse(body);
    const out = cmds.map(([c, ...a]) => {
      const C = c.toUpperCase();
      if (C === 'HSETNX') { hash[a[0]] ??= {}; if (a[1] in hash[a[0]]) return { result: 0 }; hash[a[0]][a[1]] = Number(a[2]); return { result: 1 }; }
      if (C === 'HINCRBY') { hash[a[0]] ??= {}; hash[a[0]][a[1]] = (hash[a[0]][a[1]] || 0) + Number(a[2]); return { result: hash[a[0]][a[1]] }; }
      if (C === 'HSET') { hash[a[0]] ??= {}; hash[a[0]][a[1]] = Number(a[2]); return { result: 1 }; }
      if (C === 'HGETALL') return { result: Object.entries(hash[a[0]] || {}).flatMap(([k, v]) => [k, String(v)]) };
      if (C === 'SET') { if (a.map(String).includes('NX') && a[0] in kv) return { result: null }; kv[a[0]] = a[1]; return { result: 'OK' }; }
      if (C === 'GET') return { result: kv[a[0]] ?? null };
      if (C === 'LPUSH') { (lists[a[0]] ??= []).unshift(a[1]); return { result: 1 }; }
      if (C === 'LTRIM') return { result: 'OK' };
      if (C === 'LRANGE') return { result: (lists[a[0]] || []).slice(0, 50) };
      return { error: 'unknown ' + c };
    });
    res.setHeader('content-type', 'application/json'); res.end(JSON.stringify(out));
  });
});
await new Promise(r => srv.listen(0, r));
process.env.KV_REST_API_URL = 'http://127.0.0.1:' + srv.address().port; process.env.KV_REST_API_TOKEN = 't';
process.env.ADMIN_TOKEN = 'test-admin-token-123'; process.env.RESEND_API_KEY = 'x';
let mailFail = false; const mails = []; const realFetch = globalThis.fetch;
globalThis.fetch = async (u, o) => { if (String(u).startsWith('https://api.resend.com/')) { if (mailFail) return { ok: false, json: async () => ({}) }; mails.push(JSON.parse(o.body)); return { ok: true, json: async () => ({}) }; } return realFetch(u, o); };
const { default: order } = await import('../api/order.js'); const { default: stock } = await import('../api/stock.js'); const { default: admin } = await import('../api/admin.js');
const call = async (h, { method = 'POST', body, headers = {} } = {}) => { let code = 200, json; const res = { status(c) { code = c; return this; }, json(j) { json = j; return this; }, setHeader() {} }; await h({ method, body, headers: { origin: 'https://nuveraform.com', 'x-forwarded-for': '1.2.3.' + Math.floor(Math.random() * 250), ...headers } }, res); return { code, json }; };
const cust = n => ({ name: 'Ann Lee', email: `a${n}@b.co`, phone: '3055550000', street: '1 Main St', city: 'Miami', state: 'FL', zip: '33101' });
let fail = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fail++; };
let r = await call(stock, { method: 'GET' }); ok(r.json.tracked && r.json.stock['ret|5mg'] === 1 && r.json.stock['bn1|Bundle'] === 5 && r.json.stock['bn2|Bundle'] === 3, 'seeded stock + bundle min (bn2 = min(ret10=8, bac=3) = 3)');
// two buyers, last vial of ret 5mg, concurrently
const [a, b] = await Promise.all([1, 2].map(n => call(order, { body: { ...cust(n), items: [{ id: 'ret', v: '5mg', q: 1 }] } })));
ok([a.code, b.code].sort().join() === '200,409', `last vial sold once (got ${a.code},${b.code})`);
r = await call(stock, { method: 'GET' }); ok(r.json.stock['ret|5mg'] === 0, 'stock now 0 after sale');
// bundle consumes components
r = await call(order, { body: { ...cust(3), items: [{ id: 'bn2', v: 'Bundle', q: 1 }], promo: true } });
ok(r.code === 200 && r.json.total === 175.5 * 0.8 + 0 * 0 + (175.5 * 0.8 >= 200 ? 0 : 15), `bundle order priced server-side (${r.json.total})`);
r = await call(stock, { method: 'GET' }); ok(r.json.stock['ret|10mg'] === 7 && r.json.stock['bac|10ml'] === 2 && r.json.stock['bn2|Bundle'] === 2, 'bundle decremented parts; bundle stock follows');
// tampering: client cannot set price; invalid items rejected
r = await call(order, { body: { ...cust(4), items: [{ id: 'ret', v: '99mg', q: 1 }] } }); ok(r.code === 400, 'unknown variant rejected');
r = await call(order, { body: { ...cust(5), items: [{ id: 'ghk', v: '100mg', q: 11 }] } }); ok(r.code === 409, 'over-stock rejected');
r = await call(stock, { method: 'GET' }); ok(r.json.stock['ghk|100mg'] === 10, 'failed reservation rolled back');
// origin check
r = await call(order, { body: { ...cust(6), items: [{ id: 'ghk', v: '100mg', q: 1 }] }, headers: { origin: 'https://evil.example' } }); ok(r.code === 403, 'foreign origin blocked');
// admin
r = await call(admin, { body: { action: 'list' } }); ok(r.code === 401, 'admin needs token');
const H = { 'x-admin-token': process.env.ADMIN_TOKEN };
r = await call(admin, { body: { action: 'list' }, headers: H }); const o = r.json.orders.find(x => x.items[0].startsWith('Retatrutide 10mg + Bac')); ok(r.code === 200 && o && !('need' in o), 'admin lists orders without internals');
r = await call(admin, { body: { action: 'orderStatus', no: o.no, status: 'cancelled' }, headers: H }); ok(r.code === 200 && r.json.stock['ret|10mg'] === 8 && r.json.stock['bac|10ml'] === 3, 'cancel releases stock');
r = await call(admin, { body: { action: 'orderStatus', no: o.no, status: 'cancelled' }, headers: H }); ok(r.code === 409, 'cannot release twice');
r = await call(admin, { body: { action: 'setStock', stock: { 'ret|10mg': 38, 'kpv|10mg': 5 } }, headers: H }); ok(r.code === 400, 'unknown SKU rejected');
r = await call(admin, { body: { action: 'setStock', stock: { 'ret|10mg': 38 } }, headers: H }); ok(r.code === 200 && r.json.stock['ret|10mg'] === 38, 'restock sets level');
ok(mails.some(m => m.to[0] === 'info@nuveraform.com') && mails.some(m => m.to[0] === 'a1@b.co' || m.to[0] === 'a2@b.co'), 'owner + customer emails sent');

// --- review fixes ---
// prototype-chain ids/variants must not pass validation
r = await call(order, { body: { ...cust(7), items: [{ id: 'constructor', v: '5mg', q: 1 }] } }); ok(r.code === 400, 'id "constructor" rejected (400, no crash)');
r = await call(order, { body: { ...cust(7), items: [{ id: 'ret', v: 'constructor', q: 1 }] } }); ok(r.code === 400, 'variant "constructor" rejected');
r = await call(order, { body: { ...cust(7), items: [{ id: ['ghk'], v: '100mg', q: 1 }] } }); ok(r.code === 400, 'non-string id rejected');
r = await call(admin, { body: { action: 'setStock', stock: JSON.parse('{"constructor":5}') }, headers: H }); ok(r.code === 400, 'admin cannot write prototype-named stock fields');
r = await call(admin, { body: { action: 'setStock', stock: JSON.parse('{"__proto__":5}') }, headers: H }); ok(r.code === 400, 'admin rejects __proto__ stock field');
// transient negative counts are never published
hash.stock['ghk|100mg'] = -3; r = await call(stock, { method: 'GET' }); ok(r.json.stock['ghk|100mg'] === 0, 'public stock never negative'); hash.stock['ghk|100mg'] = 10;
// owner email failure gives stock back exactly once and the record cannot be released again
mailFail = true; r = await call(order, { body: { ...cust(8), items: [{ id: 'ghk', v: '100mg', q: 2 }] } }); mailFail = false;
ok(r.code === 502, 'email failure -> 502');
r = await call(stock, { method: 'GET' }); ok(r.json.stock['ghk|100mg'] === 10, 'stock restored after email failure');
r = await call(admin, { body: { action: 'list' }, headers: H }); const failed = r.json.orders.find(x => x.failed);
ok(failed && failed.status === 'cancelled', 'failed order recorded as cancelled');
r = await call(admin, { body: { action: 'orderStatus', no: failed.no, status: 'cancelled' }, headers: H }); ok(r.code === 409, 'failed order cannot be released again');
r = await call(stock, { method: 'GET' }); ok(r.json.stock['ghk|100mg'] === 10, 'no double release for failed order');
// concurrent cancels release once
r = await call(order, { body: { ...cust(9), items: [{ id: 'ghk', v: '100mg', q: 3 }] } }); ok(r.code === 200, 'order 3 ghk');
r = await call(admin, { body: { action: 'list' }, headers: H }); const o3 = r.json.orders.find(x => x.items[0].startsWith('GHK-Cu') && x.status === 'pending');
const cc = await Promise.all([1, 2, 3].map(() => call(admin, { body: { action: 'orderStatus', no: o3.no, status: 'cancelled' }, headers: H })));
ok(cc.filter(x => x.code === 200).length === 1, 'exactly one concurrent cancel succeeds (' + cc.map(x => x.code) + ')');
r = await call(stock, { method: 'GET' }); ok(r.json.stock['ghk|100mg'] === 10, 'stock released once, not three times');
// admin lockout applies before comparison: correct token is refused after 10 bad guesses from one IP
const ip = { 'x-forwarded-for': '9.9.9.9' };
for (let i = 0; i < 10; i++) await call(admin, { body: { action: 'list' }, headers: { ...ip, 'x-admin-token': 'wrong-wrong-wrong' + i } });
r = await call(admin, { body: { action: 'list' }, headers: { ...ip, ...H } }); ok(r.code === 429, 'correct token refused during lockout');
r = await call(admin, { body: { action: 'list' }, headers: H }); ok(r.code === 200, 'other IPs unaffected');
srv.close(); process.exit(fail ? 1 : 0);
