// Owner-only inventory and order management. Protected by the ADMIN_TOKEN environment variable.
import { timingSafeEqual } from 'node:crypto';
import { guard, throttle } from './_lib.js';
import { DEFAULT_STOCK } from './_catalog.js';
import { configured, redis, readStock, release } from './_stock.js';

const same = (a, b) => { const x = Buffer.from(String(a)), y = Buffer.from(String(b)); return x.length === y.length && timingSafeEqual(x, y); };

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (guard(req, res, { limit: 200, bucket: 'adminreq' })) return;
  const expected = process.env.ADMIN_TOKEN;
  if (!expected || expected.length < 12) return res.status(503).json({ error: 'Admin is not configured' });
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (!same(req.headers['x-admin-token'] || '', expected)) { if (throttle('adminfail:' + ip, 10)) return res.status(429).json({ error: 'Too many attempts' }); return res.status(401).json({ error: 'Unauthorized' }); }
  if (!configured()) return res.status(503).json({ error: 'Inventory store is not connected' });
  const b = req.body || {};
  try {
    if (b.action === 'setStock') {
      const cmds = [];
      for (const [k, v] of Object.entries(b.stock || {})) {
        if (!(k in DEFAULT_STOCK) || !Number.isInteger(v) || v < 0 || v > 99999) return res.status(400).json({ error: 'Invalid stock value for ' + k });
        cmds.push(['HSET', 'stock', k, v]);
      }
      if (cmds.length) await redis(cmds);
    } else if (b.action === 'orderStatus') {
      if (typeof b.no !== 'string' || !/^NF-\d{6}-[A-Z0-9]{4}$/.test(b.no) || !['paid', 'cancelled'].includes(b.status)) return res.status(400).json({ error: 'Invalid request' });
      const [raw] = await redis([['GET', 'order:' + b.no]]);
      if (!raw) return res.status(404).json({ error: 'Order not found' });
      const rec = JSON.parse(raw);
      if (rec.status === 'cancelled') return res.status(409).json({ error: 'Already cancelled' });
      if (b.status === 'cancelled' && rec.need) await release(rec.need);
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
