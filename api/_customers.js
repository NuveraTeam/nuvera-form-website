// Remembers who has already ordered so the first-order code (NUVERA10) works only once.
// Each customer is stored as hashed keys (email, phone, street + ZIP) in a Vercel Blob store,
// so no readable personal data is kept here. Needs BLOB_READ_WRITE_TOKEN and CUSTOMER_SALT in Vercel.
import { createHash } from 'node:crypto';
import { head, put } from '@vercel/blob';

// CUSTOMER_SALT (Vercel env var) keeps these hashes from being matched by anyone who reads this public code.
const hash = s => createHash('sha256').update((process.env.CUSTOMER_SALT || '') + ':' + s).digest('hex').slice(0, 40);

export function customerKeys({ email = '', phone = '', addr1 = '', zip = '' }) {
  const keys = [];
  const e = email.trim().toLowerCase();
  if (e) keys.push('e:' + e);
  const p = phone.replace(/\D/g, '').slice(-10);
  if (p.length === 10) keys.push('p:' + p);
  const a = addr1.toLowerCase().replace(/[^a-z0-9]/g, '');
  const z = zip.slice(0, 5);
  if (a && z) keys.push('a:' + a + z);
  return keys.map(k => `customers/${hash(k)}.json`);
}

// Customers who ordered before this check existed (hashed; orders NF-261024-XR2E, NF-261031-8YO3).
const PAST = new Set(["customers/d722006cc7e160fb8c2c6ac87e5353f51554273a.json","customers/e60532002957794537a7b8101b59e9b8a2dd9cee.json","customers/e8e27b7e650d5a43310189e9172f79f850a9b8e6.json"]);

export const storageReady = () => Boolean(process.env.BLOB_READ_WRITE_TOKEN);

// True if any key matches an earlier order. Errors other than "not found" count as unknown (false).
export async function hasOrderedBefore(paths) {
  if (paths.some(p => PAST.has(p))) return true;
  if (!storageReady()) return false;
  const checks = await Promise.all(paths.map(p => head(p).then(() => true, () => false)));
  return checks.some(Boolean);
}

export async function rememberCustomer(paths, order) {
  if (!storageReady()) return;
  const body = JSON.stringify({ order, at: new Date().toISOString() });
  await Promise.allSettled(paths.map(p =>
    put(p, body, { access: 'public', contentType: 'application/json', addRandomSuffix: false, allowOverwrite: true })
  ));
}
