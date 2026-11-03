// Store owner's Approve link from the review email. Publishes the review on the product page.
import { getPendingReview, approveReview, verify } from './_store.js';
import { REVIEWABLE } from './_catalog.js';
import { esc, SITE } from './_mail.js';

const page = (title, body) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${esc(title)}</title><link rel="stylesheet" href="/assets/site.css"></head><body><main id="main"><div class="wrap prose"><h1>${esc(title)}</h1>${body}</div></main></body></html>`;

export default async function handler(req, res) {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  const id = String((req.query || {}).id || '');
  if (!verify('rv:' + id, (req.query || {}).s)) return res.status(403).send(page('Link not valid', '<p>Use the Approve button in the review email.</p>'));
  const r = await getPendingReview(id);
  if (!r) return res.status(404).send(page('Already handled', '<p>This review was already approved, or it no longer exists.</p>'));
  await approveReview(id, r);
  const p = REVIEWABLE[r.product];
  return res.status(200).send(page('Review published', `<p>The review now shows on <a href="${SITE}/compounds/${p.page}">${esc(p.name)}</a> (it can take about a minute to appear).</p>`));
}
