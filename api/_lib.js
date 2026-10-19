// Shared helpers for serverless functions (underscore prefix = not routed).
const hits = new Map();
export const esc = (v = '') => String(v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
export const validEmail = e => typeof e === 'string' && e.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
export const FROM = () => process.env.MAIL_FROM || 'Nuvera Form <hello@nuveraform.com>';
export const SEGMENT = () => process.env.RESEND_SEGMENT_ID || 'df0df756-7c4c-45b5-b0e6-ecbd0e0cc8a8';

/** Returns an error response (and true) if the request should be rejected. */
export function guard(req, res, { limit = 5, bucket = 'x' } = {}) {
  if (req.method !== 'POST') { res.status(405).json({ error: 'Method not allowed' }); return true; }
  const allowed = (process.env.ALLOWED_ORIGINS || 'https://nuveraform.com,https://www.nuveraform.com').split(',').map(s => s.trim()).filter(Boolean);
  if (allowed.length && !allowed.includes(req.headers.origin || '')) { res.status(403).json({ error: 'Forbidden' }); return true; }
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (throttle(bucket + ':ip:' + ip, limit)) { res.status(429).json({ error: 'Too many requests' }); return true; }
  return false;
}

/** Best-effort sliding-window limiter (per warm instance; use a shared store or Vercel Firewall rate limits for hard limits). Returns true if over the limit. */
export function throttle(key, limit, windowMs = 3600e3) {
  const now = Date.now();
  if (hits.size > 5000) for (const [k, v] of hits) if (!v.some(t => now - t < windowMs)) hits.delete(k);
  const recent = (hits.get(key) || []).filter(t => now - t < windowMs);
  if (recent.length >= limit) { hits.set(key, recent); return true; }
  hits.set(key, [...recent, now]);
  return false;
}

/** Limits how many mails one recipient can be sent per hour, so the API cannot be used to spam a third party. */
export function mailLimited(res, bucket, email, limit = 2) {
  if (throttle(bucket + ':to:' + email.toLowerCase(), limit)) { res.status(429).json({ error: 'Too many requests' }); return true; }
  return false;
}

/** Adds (or updates) a contact in the Resend segment. Never throws. */
export async function addContact(email, first_name) {
  try {
    const r = await fetch('https://api.resend.com/contacts', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, first_name: first_name || undefined, segments: [{ id: SEGMENT() }] }) // no `unsubscribed` flag: never re-subscribe someone who opted out
    });
    return r.ok;
  } catch { return false; }
}

export async function sendMail({ to, subject, html }) {
  try { return await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM(), to: [to], reply_to: 'info@nuveraform.com', subject, html })
  }); } catch { return { ok: false }; }
}

/** Fires a Resend automation event for a contact. Never throws. */
export async function sendEvent(event, email) {
  try {
    const r = await fetch('https://api.resend.com/events/send', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ event, email })
    });
    return r.ok;
  } catch { return false; }
}
