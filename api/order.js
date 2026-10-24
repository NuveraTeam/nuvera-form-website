// Vercel serverless function: receives a checkout, re-prices it from the server price list,
// emails the order to the store and a Zelle payment request to the customer via Resend.
import { PRICES, SHIPPING, PROMO } from './_catalog.js';

const hits = new Map();
const esc = (v = '') => String(v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const money = n => '$' + n.toFixed(2);
const str = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');
const STATES = 'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY PR'.split(' ');

function orderNumber() {
  const d = new Date();
  const ymd = String(d.getUTCFullYear()).slice(2) + String(d.getUTCMonth() + 1).padStart(2, '0') + String(d.getUTCDate()).padStart(2, '0');
  const rnd = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `NF-${ymd}-${rnd}`;
}

async function send(payload) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: process.env.MAIL_FROM || 'Nuvera Form <hello@nuveraform.com>', ...payload })
  });
  return r.ok;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const allowed = (process.env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  const origin = req.headers.origin || '';
  if (allowed.length && !allowed.includes(origin)) return res.status(403).json({ error: 'Forbidden' });

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0] || 'unknown';
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter(t => now - t < 3600e3);
  if (recent.length >= 10) return res.status(429).json({ error: 'Too many orders from this connection. Email info@nuveraform.com.' });
  hits.set(ip, [...recent, now]);

  const b = req.body || {};
  if (b.website) return res.status(200).json({ ok: true, order: 'NF-0' }); // honeypot

  const c = {
    first: str(b.first_name, 60), last: str(b.last_name, 60), email: str(b.email, 254).toLowerCase(), phone: str(b.phone, 30),
    addr1: str(b.address1, 120), addr2: str(b.address2, 120), city: str(b.city, 80), state: str(b.state, 2).toUpperCase(),
    zip: str(b.zip, 10), notes: str(b.notes, 500)
  };
  const missing = [];
  if (!c.first) missing.push('first name');
  if (!c.last) missing.push('last name');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c.email)) missing.push('a valid email');
  if (c.phone.replace(/\D/g, '').length < 10) missing.push('a valid phone number');
  if (!c.addr1) missing.push('street address');
  if (!c.city) missing.push('city');
  if (!STATES.includes(c.state)) missing.push('state');
  if (!/^\d{5}(-\d{4})?$/.test(c.zip)) missing.push('a valid ZIP code');
  if (b.ruo !== true) missing.push('the research-use confirmation');
  if (missing.length) return res.status(400).json({ error: 'Please add ' + missing.join(', ') + '.' });

  const ship = SHIPPING[b.shipping];
  if (!ship) return res.status(400).json({ error: 'Choose a shipping method.' });

  if (!Array.isArray(b.items) || !b.items.length || b.items.length > 30) return res.status(400).json({ error: 'Your cart is empty.' });
  const lines = [];
  for (const it of b.items) {
    const p = PRICES[it && it.id];
    const price = p && p.v[it.v];
    const q = Number(it && it.q);
    if (!price || !Number.isInteger(q) || q < 1 || q > 50) return res.status(400).json({ error: 'An item in your cart is no longer available. Refresh the page and try again.' });
    lines.push({ name: p.name, v: it.v, q, price, total: price * q });
  }

  const subtotal = lines.reduce((a, l) => a + l.total, 0);
  const code = str(b.promo, 20).toUpperCase();
  const rate = PROMO[code] || 0;
  const discount = Math.round(subtotal * rate * 100) / 100;
  const total = Math.round((subtotal - discount + ship.price) * 100) / 100;
  const order = orderNumber();

  const zelleTo = process.env.ZELLE_TO || '';
  const zelleName = process.env.ZELLE_NAME || 'Nuvera Form';
  const storeTo = (process.env.ORDER_NOTIFY_TO || 'info@nuveraform.com').split(',').map(s => s.trim()).filter(Boolean);

  const rows = lines.map(l => `<tr><td style="padding:6px 0">${esc(l.name)}${l.name.includes(l.v) || l.v === 'Bundle' || l.v === 'Blend' ? '' : ' · ' + esc(l.v)} × ${l.q}</td><td style="padding:6px 0;text-align:right">${money(l.total)}</td></tr>`).join('');
  const totalsHtml = `${rows}
<tr><td style="padding:6px 0;border-top:1px solid #E5D7BD">Subtotal</td><td style="padding:6px 0;text-align:right;border-top:1px solid #E5D7BD">${money(subtotal)}</td></tr>
${discount ? `<tr><td style="padding:6px 0">${esc(code)} (${Math.round(rate * 100)}%)</td><td style="padding:6px 0;text-align:right">−${money(discount)}</td></tr>` : ''}
<tr><td style="padding:6px 0">Shipping: ${esc(ship.label)}</td><td style="padding:6px 0;text-align:right">${money(ship.price)}</td></tr>
<tr><td style="padding:8px 0;font-weight:700;font-size:16px">Total due</td><td style="padding:8px 0;text-align:right;font-weight:700;font-size:16px">${money(total)}</td></tr>`;
  const addressHtml = `${esc(c.first)} ${esc(c.last)}<br>${esc(c.addr1)}${c.addr2 ? '<br>' + esc(c.addr2) : ''}<br>${esc(c.city)}, ${esc(c.state)} ${esc(c.zip)}`;

  const storeOk = await send({
    to: storeTo,
    reply_to: c.email,
    subject: `New order ${order}: ${money(total)} via Zelle (${ship.price === 60 ? 'OVERNIGHT' : 'Ground'})`,
    html: `<div style="font-family:Arial,sans-serif;color:#3A2816">
<h2 style="margin:0 0 8px">New order ${order}</h2>
<p style="margin:0 0 16px">Awaiting Zelle payment of <b>${money(total)}</b>. Customer was told to put <b>${order}</b> in the Zelle memo.</p>
<table style="width:100%;max-width:520px;border-collapse:collapse;font-size:14px">${totalsHtml}</table>
<h3 style="margin:20px 0 6px">Ship to</h3><p style="margin:0">${addressHtml}</p>
<h3 style="margin:20px 0 6px">Contact</h3><p style="margin:0">${esc(c.email)}<br>${esc(c.phone)}</p>
${c.notes ? `<h3 style="margin:20px 0 6px">Order notes</h3><p style="margin:0">${esc(c.notes)}</p>` : ''}
<p style="font-size:12px;color:#7a6650;margin-top:20px">Buyer confirmed 21+ and research use only at checkout.</p></div>`
  });
  if (!storeOk) return res.status(502).json({ error: 'Email provider error' });

  const payBlock = zelleTo
    ? `<p style="margin:0 0 6px">Send <b>${money(total)}</b> by Zelle to:</p>
<p style="font-size:18px;font-weight:700;margin:0 0 4px">${esc(zelleTo)}</p><p style="margin:0 0 10px">Name shown in Zelle: ${esc(zelleName)}</p>
<p style="margin:0">Put <b>${order}</b> in the Zelle memo so we can match your payment.</p>`
    : `<p style="margin:0">We will email you our Zelle details shortly. Total due: <b>${money(total)}</b>. Please put <b>${order}</b> in the Zelle memo.</p>`;

  const customerOk = await send({
    to: [c.email],
    reply_to: 'info@nuveraform.com',
    subject: `Order ${order} received: pay ${money(total)} by Zelle`,
    html: `<div style="font-family:Arial,sans-serif;background:#F7F0E3;color:#3A2816;padding:32px">
<img src="https://nuveraform.com/assets/nuvera-logo-hd-192.png" alt="Nuvera Form" width="64" height="64" style="display:block;width:64px;height:64px;border:0;margin:0 0 16px">
<h2 style="margin:0 0 8px">Thanks${c.first ? ', ' + esc(c.first) : ''}. Your order is reserved.</h2>
<p style="margin:0 0 18px">Order number <b>${order}</b>. It ships once your payment arrives.</p>
<div style="background:#fff;border:2px dashed #BF943C;border-radius:14px;padding:16px;margin:0 0 20px">${payBlock}</div>
<table style="width:100%;max-width:520px;border-collapse:collapse;font-size:14px">${totalsHtml}</table>
<h3 style="margin:20px 0 6px">Shipping to</h3><p style="margin:0">${addressHtml}</p>
<p style="margin:20px 0 0">Orders dispatch within 1–2 business days of payment, and we email tracking when yours leaves. Questions? Reply to this email or call 305-457-3814.</p>
<p style="font-size:12px;margin-top:20px">All products are for Research Use Only and are not for human or veterinary use.</p></div>`
  });

  return res.status(200).json({ ok: true, order, total, zelle: zelleTo ? { to: zelleTo, name: zelleName } : null, emailed: customerOk });
}
