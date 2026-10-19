// Places an order: validates it, prices it from the server catalog, reserves stock atomically, saves the order,
// emails the owner and sends the customer their Zelle payment instructions.
import { randomInt } from 'node:crypto';
import { guard, human, mailLimited, validEmail, esc, sendMail } from './_lib.js';
import { PRODUCTS, priceCents, lineName, TOTALS } from './_catalog.js';
import { configured, reserve, release, redis } from './_stock.js';

const OWNER = () => process.env.OWNER_EMAIL || 'info@nuveraform.com';
const money = c => '$' + (c / 100).toFixed(2);
const ALPHA = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const orderNo = () => { const d = new Date(); const p = n => String(n).padStart(2, '0'); return `NF-${p(d.getUTCFullYear() % 100)}${p(d.getUTCMonth() + 1)}${p(d.getUTCDate())}-${Array.from({ length: 4 }, () => ALPHA[randomInt(ALPHA.length)]).join('')}`; };
const clean = (v, max) => typeof v === 'string' ? v.replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, max) : '';

export default async function handler(req, res) {
  if (guard(req, res, { limit: 10, bucket: 'order' })) return;
  if (!(await human(req, res))) return;
  const b = req.body || {};
  const c = { name: clean(b.name, 80), email: clean(b.email, 254), phone: clean(b.phone, 30), street: clean(b.street, 120), city: clean(b.city, 60), state: clean(b.state, 2).toUpperCase(), zip: clean(b.zip, 10), notes: clean(b.notes, 300) };
  if (!/^[\p{L}\p{M} .'’-]{2,80}$/u.test(c.name) || !validEmail(c.email) || c.phone.replace(/\D/g, '').length < 7 || c.street.length < 3 || c.city.length < 2 || !/^[A-Z]{2}$/.test(c.state) || !/^\d{5}(-\d{4})?$/.test(c.zip)) return res.status(400).json({ error: 'Invalid details' });
  if (!Array.isArray(b.items) || !b.items.length || b.items.length > 20) return res.status(400).json({ error: 'Invalid items' });
  const merged = new Map();
  for (const i of b.items) {
    const q = Number(i && i.q);
    if (!i || !PRODUCTS[i.id] || !PRODUCTS[i.id].v[i.v] || !Number.isInteger(q) || q < 1 || q > 50) return res.status(400).json({ error: 'Invalid items' });
    const k = i.id + '|' + i.v; merged.set(k, { id: i.id, v: i.v, q: (merged.get(k)?.q || 0) + q });
  }
  const lines = [...merged.values()];
  if (mailLimited(res, 'order', c.email, 5)) return;
  const sub = lines.reduce((a, l) => a + priceCents(l.id, l.v) * l.q, 0);
  const t = TOTALS(sub, b.promo === true);

  let need = null, tracked = false;
  if (configured()) {
    try {
      const r = await reserve(lines);
      if (!r.ok) return res.status(409).json({ error: 'stock', sku: r.sku, available: r.available });
      need = r.need; tracked = true;
    } catch { return res.status(503).json({ error: 'Inventory unavailable' }); }
  }
  const no = orderNo();
  const rows = lines.map(l => `${lineName(l.id, l.v)} x${l.q} @ ${money(priceCents(l.id, l.v))}`);
  const rec = { no, ts: Date.now(), status: 'pending', customer: c, items: rows, promo: b.promo === true, ...t, need };
  const owner = await sendMail({ to: OWNER(), subject: `New order ${no} (${money(t.total)})`, html: `<div style="font-family:Arial,sans-serif"><h3>New order ${esc(no)}</h3><p><b>${esc(c.name)}</b><br>${esc(c.email)} · ${esc(c.phone)}<br>${esc(c.street)}, ${esc(c.city)}, ${esc(c.state)} ${esc(c.zip)}</p><ul>${rows.map(r => `<li>${esc(r)}</li>`).join('')}</ul><p>Discount: ${t.disc ? 'NUVERA20 −' + money(t.disc) + ' (first-order code: check this email has no earlier order)' : 'none'}<br>Shipping: ${t.ship ? money(t.ship) : 'Free'}<br><b>Total due: ${money(t.total)}</b> · Payment: Zelle (pending)</p>${c.notes ? `<p>Notes: ${esc(c.notes)}</p>` : ''}<p>Stock ${tracked ? 'was reserved automatically' : 'is NOT tracked (inventory store not connected)'}. Mark paid or cancel in /admin.</p></div>` });
  if (!owner || !owner.ok) { if (need) await release(need).catch(() => {}); return res.status(502).json({ error: 'Email provider error' }); }
  if (tracked) { try { await redis([['SET', 'order:' + no, JSON.stringify(rec), 'EX', 60 * 86400], ['LPUSH', 'orders', no], ['LTRIM', 'orders', 0, 199]]); } catch { /* order is already emailed to the owner */ } }

  const who = /^[\p{L}\p{M} .'’-]{1,80}$/u.test(c.name) ? c.name : '';
  const cust = await sendMail({ to: c.email, subject: `Nuvera Form order ${no}: payment instructions`, html: `<div style="font-family:Arial,sans-serif;background:#F7F0E3;color:#3A2816;padding:32px">
<h2 style="margin:0 0 12px">Thank you${who ? ', ' + esc(who) : ''}.</h2>
<p>We received your order <b>${esc(no)}</b>.</p><ul>${rows.map(r => `<li>${esc(r)}</li>`).join('')}</ul>
<p><b>Total due: ${money(t.total)}</b></p>
<p><b>Pay by Zelle:</b> send ${money(t.total)} to <b>(305) 457-3814</b> and put <b>${esc(no)}</b> in the memo. Please check the recipient name shown by your bank before sending.</p>
<p>We confirm payment by email and ship within 1–2 business days after that.</p>
<p>Questions? Reply to this email or call (305) 457-3814, Monday to Friday, 9 AM to 5 PM ET.</p>
<p style="font-size:12px">All products are for Research Use Only and are not for human or veterinary use.</p></div>` }).catch(() => null);
  return res.status(200).json({ ok: true, order_number: no, total: t.total / 100, tracked, emailed: Boolean(cust && cust.ok) });
}
