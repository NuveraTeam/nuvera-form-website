// Order records, reviews and email opt-outs, kept in the Vercel Blob store.
// Order records hold customer contact details, so they are encrypted with ORDER_KEY
// (AES-256-GCM) and stored under hashed, unguessable paths. Approved reviews are public by design.
// Needs BLOB_READ_WRITE_TOKEN, ORDER_KEY and CUSTOMER_SALT in Vercel.
import { createHash, createHmac, createCipheriv, createDecipheriv, randomBytes, timingSafeEqual } from 'node:crypto';
import { head, put, list, del } from '@vercel/blob';
import { SEED_ORDERS } from './_seed.js';

const SECRET = () => process.env.ORDER_KEY || '';
export const storeReady = () => Boolean(process.env.BLOB_READ_WRITE_TOKEN && SECRET());

const key = () => createHash('sha256').update('nf-enc:' + SECRET()).digest();
const h = s => createHash('sha256').update((process.env.CUSTOMER_SALT || '') + ':' + s).digest('hex').slice(0, 40);

export function encrypt(obj) {
  const iv = randomBytes(12);
  const c = createCipheriv('aes-256-gcm', key(), iv);
  const ct = Buffer.concat([c.update(JSON.stringify(obj), 'utf8'), c.final()]);
  return Buffer.concat([iv, c.getAuthTag(), ct]).toString('base64');
}
export function decrypt(b64) {
  const buf = Buffer.from(b64, 'base64');
  const d = createDecipheriv('aes-256-gcm', key(), buf.subarray(0, 12));
  d.setAuthTag(buf.subarray(12, 28));
  return JSON.parse(Buffer.concat([d.update(buf.subarray(28)), d.final()]).toString('utf8'));
}

// Signed links (mark as shipped, approve review, unsubscribe) so only the store owner or the
// customer the email was sent to can use them.
export const sign = s => createHmac('sha256', 'nf-sig:' + SECRET()).update(String(s)).digest('hex').slice(0, 32);
export function verify(s, sig) {
  const a = Buffer.from(sign(s)), b = Buffer.from(String(sig || ''));
  return a.length === b.length && timingSafeEqual(a, b);
}

async function readBlob(pathname) {
  try {
    const m = await head(pathname);
    const r = await fetch(m.url + '?v=' + Date.now(), { cache: 'no-store' });
    return r.ok ? await r.text() : null;
  } catch { return null; }
}
const writeBlob = (pathname, body) =>
  put(pathname, body, { access: 'public', contentType: 'application/json', addRandomSuffix: false, allowOverwrite: true, cacheControlMaxAge: 60 });

// ---- orders ----
const orderPath = order => `orders/${h('o:' + order)}.json`;

export async function getOrder(order) {
  order = String(order || '').trim().toUpperCase();
  if (!/^NF-\d{6}-[A-Z0-9]{4}$/.test(order)) return null;
  if (storeReady()) {
    const raw = await readBlob(orderPath(order));
    if (raw) { try { return decrypt(raw); } catch { /* fall through */ } }
  }
  const seed = SEED_ORDERS[h('o:' + order)];
  if (seed && SECRET()) { try { return decrypt(seed); } catch { return null; } }
  return null;
}

export async function saveOrder(rec) {
  if (!storeReady()) return false;
  await writeBlob(orderPath(rec.order), encrypt(rec));
  return true;
}

export async function listOrders() {
  if (!storeReady()) return [];
  const out = [];
  let cursor;
  do {
    const page = await list({ prefix: 'orders/', cursor, limit: 1000 });
    for (const b of page.blobs) {
      const raw = await readBlob(b.pathname);
      if (raw) { try { out.push(decrypt(raw)); } catch { /* skip unreadable */ } }
    }
    cursor = page.hasMore ? page.cursor : undefined;
  } while (cursor);
  return out;
}

// ---- email opt-outs ----
const optPath = email => `optout/${h('e:' + String(email).trim().toLowerCase())}.json`;
export const emailToken = email => sign('u:' + String(email).trim().toLowerCase());
export async function isOptedOut(email) {
  if (!storeReady()) return false;
  return (await readBlob(optPath(email))) !== null;
}
export async function optOut(email) {
  if (!storeReady()) return false;
  await writeBlob(optPath(email), JSON.stringify({ at: new Date().toISOString() }));
  return true;
}

// ---- reviews ----
// Pending reviews wait for approval; approved ones are listed per catalog product id.
export async function savePendingReview(r) {
  const id = randomBytes(9).toString('base64url');
  await writeBlob(`reviews/pending/${id}.json`, encrypt(r));
  return id;
}
export async function getPendingReview(id) {
  if (!/^[A-Za-z0-9_-]{12}$/.test(String(id))) return null;
  const raw = await readBlob(`reviews/pending/${id}.json`);
  if (!raw) return null;
  try { return decrypt(raw); } catch { return null; }
}
export async function approveReview(id, r) {
  const pub = { name: r.name, rating: r.rating, text: r.text, product: r.product, date: r.date, verified: true };
  await writeBlob(`reviews/approved/${r.product}/${id}.json`, JSON.stringify(pub));
  try { await del(`reviews/pending/${id}.json`); } catch { /* already gone */ }
}
export async function reviewKeyUsed(order, product) {
  return (await readBlob(`reviews/used/${h('r:' + order + ':' + product)}.json`)) !== null;
}
export async function markReviewKeyUsed(order, product) {
  await writeBlob(`reviews/used/${h('r:' + order + ':' + product)}.json`, JSON.stringify({ at: new Date().toISOString() }));
}
export async function listApprovedReviews(product) {
  if (!process.env.BLOB_READ_WRITE_TOKEN) return [];
  const page = await list({ prefix: `reviews/approved/${product}/`, limit: 200 });
  const out = [];
  for (const b of page.blobs) {
    const raw = await readBlob(b.pathname);
    if (raw) { try { out.push(JSON.parse(raw)); } catch { /* skip */ } }
  }
  return out.sort((a, b) => String(b.date).localeCompare(String(a.date)));
}
