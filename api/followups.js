// Runs once a day (Vercel Cron, see vercel.json). For shipped orders it sends:
//  - a review request REVIEW_REQUEST_DAYS after shipping
//  - a reorder reminder REORDER_WEEKS after shipping, only for products that have a number set
// Each email goes once per order, and never to someone who unsubscribed.
import { listOrders, saveOrder, isOptedOut, emailToken, storeReady } from './_store.js';
import { REVIEWABLE, REORDER_WEEKS, REVIEW_REQUEST_DAYS, reviewableIds, BUNDLE_PARTS } from './_catalog.js';
import { send, layout, button, esc, SITE } from './_mail.js';

const DAY = 864e5;
const unsub = email => `${SITE}/api/unsubscribe?e=${encodeURIComponent(email)}&s=${emailToken(email)}`;
const foot = email => `<p style="font-size:11px;margin-top:12px;color:#7a6650">You are getting this because you ordered from Nuvera Form. <a href="${unsub(email)}" style="color:#7a6650">Unsubscribe from follow-up emails</a>.</p>`;

function reorderWeeks(items) {
  const ids = [...new Set(items.flatMap(i => BUNDLE_PARTS[i.id] || [i.id]))];
  const weeks = ids.map(id => REORDER_WEEKS[id]).filter(n => Number.isFinite(n) && n > 0);
  return weeks.length ? Math.max(...weeks) : null;
}

export default async function handler(req, res) {
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.authorization !== `Bearer ${secret}`) return res.status(401).json({ error: 'Unauthorized' });
  if (!storeReady()) return res.status(200).json({ ok: true, skipped: 'store not configured' });

  const now = Date.now();
  const sent = { review: 0, reorder: 0 };
  for (const rec of await listOrders()) {
    if (!rec.shippedAt) continue;
    const age = now - Date.parse(rec.shippedAt);
    let changed = false;

    if (!rec.reviewSentAt && age >= REVIEW_REQUEST_DAYS * DAY && age < (REVIEW_REQUEST_DAYS + 21) * DAY) {
      if (await isOptedOut(rec.email)) { rec.reviewSentAt = 'opted-out'; changed = true; }
      else {
        const names = reviewableIds(rec.items).map(id => esc(REVIEWABLE[id].name)).join(', ');
        const ok = await send({
          to: [rec.email],
          subject: `How was your Nuvera Form order?`,
          html: layout(`<h2 style="margin:0 0 8px">How did we do${rec.first ? ', ' + esc(rec.first) : ''}?</h2>
<p style="margin:0 0 6px">Your order <b>${esc(rec.order)}</b> (${names}) should have arrived by now.</p>
<p style="margin:0 0 18px">A quick review of the order, packaging and shipping helps other researchers and helps a small business a lot. It takes under a minute.</p>
<p>${button(`${SITE}/review?o=${encodeURIComponent(rec.order)}`, 'Leave a review')}</p>`, foot(rec.email))
        });
        if (ok) { rec.reviewSentAt = new Date().toISOString(); changed = true; sent.review++; }
      }
    }

    const weeks = reorderWeeks(rec.items);
    if (weeks && !rec.reorderSentAt && age >= weeks * 7 * DAY && age < (weeks * 7 + 21) * DAY) {
      if (await isOptedOut(rec.email)) { rec.reorderSentAt = 'opted-out'; changed = true; }
      else {
        const names = reviewableIds(rec.items).map(id => esc(REVIEWABLE[id].name)).join(', ');
        const ok = await send({
          to: [rec.email],
          subject: `Time to restock? Your Nuvera Form order`,
          html: layout(`<h2 style="margin:0 0 8px">Ready for your next order${rec.first ? ', ' + esc(rec.first) : ''}?</h2>
<p style="margin:0 0 18px">It has been ${weeks} weeks since we shipped your order of ${names}. If your lab needs more, the catalog shows current stock, and orders still dispatch within 1–2 business days.</p>
<p>${button(`${SITE}/#catalog`, 'View the catalog')}</p>`, foot(rec.email))
        });
        if (ok) { rec.reorderSentAt = new Date().toISOString(); changed = true; sent.reorder++; }
      }
    }
    if (changed) await saveOrder(rec);
  }
  return res.status(200).json({ ok: true, sent });
}
