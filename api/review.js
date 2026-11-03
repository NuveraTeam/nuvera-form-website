// Verified-buyer reviews. POST with order number + order email + product + rating + text.
// The review is held for approval and the store owner gets an email with an Approve link.
import { getOrder, savePendingReview, reviewKeyUsed, markReviewKeyUsed, sign, storeReady } from './_store.js';
import { REVIEWABLE, reviewableIds } from './_catalog.js';
import { send, layout, button, esc, SITE } from './_mail.js';

const hits = new Map();
const str = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  if (!storeReady()) return res.status(503).json({ error: 'Reviews are not available right now. Email info@nuveraform.com.' });

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0] || 'unknown';
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter(t => now - t < 3600e3);
  if (recent.length >= 8) return res.status(429).json({ error: 'Too many attempts. Try again later.' });
  hits.set(ip, [...recent, now]);

  const b = req.body || {};
  if (b.website) return res.status(200).json({ ok: true }); // honeypot
  const order = str(b.order, 20).toUpperCase();
  const email = str(b.email, 254).toLowerCase();
  const product = str(b.product, 8);
  const rating = Number(b.rating);
  const text = str(b.text, 1200);
  const name = str(b.name, 40).replace(/[<>]/g, '');

  const rec = await getOrder(order);
  if (!rec || rec.email.toLowerCase() !== email)
    return res.status(400).json({ error: 'We could not match that order number and email. Use the email you ordered with.' });

  const ids = reviewableIds(rec.items);
  if (b.lookup) return res.status(200).json({ ok: true, products: ids.map(id => ({ id, name: REVIEWABLE[id].name })) });

  if (!ids.includes(product)) return res.status(400).json({ error: 'Choose a product from this order.' });
  if (!Number.isInteger(rating) || rating < 1 || rating > 5) return res.status(400).json({ error: 'Choose a rating from 1 to 5 stars.' });
  if (text.length < 10) return res.status(400).json({ error: 'Please write a few words about your order.' });
  if (await reviewKeyUsed(order, product)) return res.status(409).json({ error: 'You have already reviewed this product for this order. Thank you!' });

  const shown = name || `${rec.first || 'Verified'} ${rec.last ? rec.last[0] + '.' : 'buyer'}`;
  const review = { order, product, rating, text, name: shown, date: new Date().toISOString().slice(0, 10) };
  const id = await savePendingReview(review);
  await markReviewKeyUsed(order, product);

  const approve = `${SITE}/api/review-approve?id=${id}&s=${sign('rv:' + id)}`;
  await send({
    to: (process.env.ORDER_NOTIFY_TO || 'info@nuveraform.com').split(',').map(s => s.trim()).filter(Boolean),
    reply_to: rec.email,
    subject: `New ${rating}★ review for ${REVIEWABLE[product].name} (${order})`,
    html: layout(`<h2 style="margin:0 0 8px">New review waiting for approval</h2>
<p style="margin:0 0 4px"><b>${'★'.repeat(rating)}${'☆'.repeat(5 - rating)}</b> · ${esc(REVIEWABLE[product].name)}</p>
<p style="margin:0 0 4px">Shown as: <b>${esc(shown)}</b> · Order ${esc(order)}</p>
<blockquote style="margin:12px 0;padding:12px 16px;background:#fff;border-left:4px solid #BF943C">${esc(text).replace(/\n/g, '<br>')}</blockquote>
<p style="margin:0 0 16px;font-size:13px">Only approve reviews that talk about the order, shipping, packaging, labelling or service. Do not approve reviews that describe effects, dosing or use in people or animals; just ignore this email and it stays hidden.</p>
<p>${button(approve, 'Approve and publish')}</p>`)
  });
  return res.status(200).json({ ok: true });
}
