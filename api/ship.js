// Store-owner page reached from the "Mark as shipped" link in each new-order email.
// GET shows a small form (carrier + tracking number); POST saves it and emails the customer.
import { getOrder, saveOrder, verify } from './_store.js';
import { send, layout, button, esc, SITE } from './_mail.js';

const CARRIERS = {
  usps: { name: 'USPS', url: t => `https://tools.usps.com/go/TrackConfirmAction?tLabels=${encodeURIComponent(t)}` },
  ups: { name: 'UPS', url: t => `https://www.ups.com/track?tracknum=${encodeURIComponent(t)}` },
  fedex: { name: 'FedEx', url: t => `https://www.fedex.com/fedextrack/?trknbr=${encodeURIComponent(t)}` }
};

const page = (title, body) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${esc(title)}</title><link rel="stylesheet" href="/assets/site.css"></head><body><main id="main"><div class="wrap prose"><h1>${esc(title)}</h1>${body}</div></main></body></html>`;

export default async function handler(req, res) {
  const q = req.method === 'POST' ? (req.body || {}) : (req.query || {});
  const order = String(q.o || '').toUpperCase();
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  if (!verify('ship:' + order, q.s)) return res.status(403).send(page('Link not valid', '<p>This link is not valid. Use the button in the order email.</p>'));

  const rec = await getOrder(order);
  if (!rec) return res.status(404).send(page('Order not found', `<p>No saved record for ${esc(order)}. Orders placed before November 3, 2026 are not stored; email tracking to the customer directly.</p>`));

  const items = rec.items.map(i => `${esc(i.name)}${i.v && !['Bundle', 'Blend'].includes(i.v) && !i.name.includes(i.v) ? ' · ' + esc(i.v) : ''} × ${i.q}`).join('<br>');

  if (req.method !== 'POST') {
    const done = rec.shippedAt ? `<div class="note">Already marked shipped on ${esc(rec.shippedAt.slice(0, 10))} (${esc(rec.carrier || '')} ${esc(rec.tracking || '')}). Sending again emails the customer again.</div>` : '';
    return res.status(200).send(page(`Ship ${order}`, `${done}<p><b>${esc(rec.first)} ${esc(rec.last)}</b> · ${esc(rec.email)}</p><p>${items}</p>
<form method="post" action="/api/ship"><input type="hidden" name="o" value="${esc(order)}"><input type="hidden" name="s" value="${esc(q.s)}">
<p><label>Carrier<br><select name="carrier" required style="padding:.5rem;border-radius:10px">${Object.entries(CARRIERS).map(([k, c]) => `<option value="${k}">${c.name}</option>`).join('')}</select></label></p>
<p><label>Tracking number<br><input name="tracking" required maxlength="40" style="padding:.5rem;border-radius:10px;width:100%;max-width:24rem"></label></p>
<p><button class="btn" type="submit">Mark shipped and email the customer</button></p></form>`));
  }

  const carrier = CARRIERS[q.carrier];
  const tracking = String(q.tracking || '').replace(/[^A-Za-z0-9]/g, '').slice(0, 40);
  if (!carrier || tracking.length < 8) return res.status(400).send(page('Check the details', '<p>Choose a carrier and enter a valid tracking number. Go back and try again.</p>'));

  const link = carrier.url(tracking);
  const ok = await send({
    to: [rec.email],
    subject: `Your Nuvera Form order ${order} has shipped`,
    html: layout(`<h2 style="margin:0 0 8px">Your order is on its way${rec.first ? ', ' + esc(rec.first) : ''}.</h2>
<p style="margin:0 0 6px">Order <b>${esc(order)}</b> shipped today by ${carrier.name}.</p>
<p style="margin:0 0 18px">Tracking number: <b>${esc(tracking)}</b></p>
<p style="margin:0 0 20px">${button(link, 'Track your package')}</p>
<p style="margin:0 0 6px">${items}</p>
<p style="margin:18px 0 0">Please store vials sealed, cold and away from light when they arrive, and see our <a href="${SITE}/learn/storing-lyophilized-peptides" style="color:#BF943C">storage guide</a>. If anything arrives damaged or incorrect, reply within 72 hours with a photo and we will replace it.</p>`)
  });
  if (!ok) return res.status(502).send(page('Email not sent', '<p>The shipping email could not be sent. Nothing was saved; go back and try again.</p>'));

  rec.shippedAt = new Date().toISOString(); rec.carrier = carrier.name; rec.tracking = tracking;
  await saveOrder(rec);
  return res.status(200).send(page('Marked as shipped', `<p>${esc(rec.first)} was emailed the ${carrier.name} tracking link for ${esc(order)}. A review request goes out automatically about a week from now.</p>`));
}
