// Owner-only inventory and order management. Protected by the ADMIN_TOKEN environment variable.
import { timingSafeEqual, createHash } from 'node:crypto';
import { guard, throttle, over } from './_lib.js';
import { DEFAULT_STOCK } from './_catalog.js';
import { configured, redis, readStock, release } from './_stock.js';

const h = v => createHash('sha256').update(String(v)).digest();
const same = (a, b) => timingSafeEqual(h(a), h(b));

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (guard(req, res, { limit: 200, bucket: 'adminreq' })) return;
  const expected = process.env.ADMIN_TOKEN;
  if (!expected || expected.length < 12) return res.status(503).json({ error: 'Admin is not configured' });
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  // Lock out BEFORE comparing, otherwise a correct guess after the limit would still succeed and the limit would not slow guessing at all.
  if (over('adminfail:' + ip, 10)) return res.status(429).json({ error: 'Too many attempts' });
  if (!same(req.headers['x-admin-token'] || '', expected)) { throttle('adminfail:' + ip, 10); return res.status(401).json({ error: 'Unauthorized' }); }
  if (!configured()) return res.status(503).json({ error: 'Inventory store is not connected' });
  const b = req.body || {};
  try {
    if (b.action === 'setStock') {
      const cmds = [];
      for (const [k, v] of Object.entries(b.stock || {})) {
        if (!Object.hasOwn(DEFAULT_STOCK, k) || !Number.isInteger(v) || v < 0 || v > 99999) return res.status(400).json({ error: 'Invalid stock value for ' + k });
        cmds.push(['HSET', 'stock', k, v]);
      }
      if (cmds.length) await redis(cmds);
    } else if (b.action === 'orderStatus') {
      if (typeof b.no !== 'string' || !/^NF-\d{6}-[A-Z0-9]{4}$/.test(b.no) || !['paid', 'cancelled'].includes(b.status)) return res.status(400).json({ error: 'Invalid request' });
      const [raw] = await redis([['GET', 'order:' + b.no]]);
      if (!raw) return res.status(404).json({ error: 'Order not found' });
      const rec = JSON.parse(raw);
      if (rec.status === 'cancelled') return res.status(409).json({ error: 'Already cancelled' });
      if (b.status === 'cancelled' && rec.need) {
        // Atomic one-time claim: two concurrent cancels (double click, two tabs) must not both give the stock back.
        const [got] = await redis([['SET', 'released:' + b.no, '1', 'NX', 'EX', 90 * 86400]]);
        if (got !== 'OK') return res.status(409).json({ error: 'Already cancelled' });
        await release(rec.need);
      }
      rec.status = b.status; rec.updated = Date.now();
      await redis([['SET', 'order:' + b.no, JSON.stringify(rec), 'EX', 60 * 86400]]);
    } else if (b.action !== 'list') return res.status(400).json({ error: 'Unknown action' });
    const stock = await readStock();
    const [nos] = await redis([['LRANGE', 'orders', 0, 49]]);
    const recs = nos.length ? await redis(nos.map(n => ['GET', 'order:' + n])) : [];
    const orders = recs.filter(Boolean).map(r => { const o = JSON.parse(r); delete o.need; return o; });
    return res.status(200).json({ ok: true, stock, orders, skus: Object.keys(DEFAULT_STOCK) });
  } catch { return res.status(502).json({ error: 'Inventory error' }); }
}
