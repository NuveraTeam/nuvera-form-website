// Adds a newsletter subscriber to the Resend segment.
import { guard, mailLimited, validEmail, addContact } from './_lib.js';
export default async function handler(req, res) {
  if (guard(req, res, { limit: 10, bucket: 'sub' })) return;
  const { email, first_name } = req.body || {};
  if (!validEmail(email)) return res.status(400).json({ error: 'Invalid email' });
  if (mailLimited(res, 'sub', email, 3)) return;
  const ok = await addContact(email, typeof first_name === 'string' ? first_name.slice(0, 80) : undefined);
  return ok ? res.status(200).json({ ok: true }) : res.status(502).json({ error: 'Provider error' });
}
