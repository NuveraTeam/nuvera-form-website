// Public list of approved reviews for one product: /api/reviews?product=ret
import { listApprovedReviews } from './_store.js';
import { REVIEWABLE } from './_catalog.js';

export default async function handler(req, res) {
  const ids = String((req.query || {}).product || '').split(',').filter(id => REVIEWABLE[id]).slice(0, 3);
  if (!ids.length) return res.status(400).json({ error: 'Unknown product' });
  let reviews = [];
  try { for (const id of ids) reviews = reviews.concat(await listApprovedReviews(id)); } catch { reviews = []; }
  reviews.sort((a, b) => String(b.date).localeCompare(String(a.date)));
  const count = reviews.length;
  const avg = count ? Math.round((reviews.reduce((a, r) => a + r.rating, 0) / count) * 10) / 10 : null;
  res.setHeader('Cache-Control', 'public, s-maxage=120, stale-while-revalidate=600');
  return res.status(200).json({ count, avg, reviews: reviews.slice(0, 50) });
}
