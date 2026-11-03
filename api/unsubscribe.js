// One-click unsubscribe from review requests and reorder reminders.
import { optOut, verify } from './_store.js';
import { esc } from './_mail.js';

const page = (title, body) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${esc(title)}</title><link rel="stylesheet" href="/assets/site.css"></head><body><main id="main"><div class="wrap prose"><h1>${esc(title)}</h1>${body}<p><a href="/">Back to Nuvera Form</a></p></div></main></body></html>`;

export default async function handler(req, res) {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  const q = req.query || {};
  const email = String(q.e || '').trim().toLowerCase();
  if (!email || !verify('u:' + email, q.s)) return res.status(403).send(page('Link not valid', '<p>Email info@nuveraform.com and we will remove you.</p>'));
  await optOut(email);
  return res.status(200).send(page('You are unsubscribed', `<p>${esc(email)} will no longer get review requests or reorder reminders. You will still get emails about orders you place.</p>`));
}
