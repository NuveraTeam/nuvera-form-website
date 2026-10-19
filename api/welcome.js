// Sends the welcome email with the NUVERA20 code and saves the contact in Resend.
// The API key lives in Vercel environment variables, never in the browser.
import { human, guard, mailLimited, validEmail, esc, addContact, sendMail, sendEvent } from './_lib.js';

export default async function handler(req, res) {
  if (guard(req, res, { limit: 5, bucket: 'welcome' })) return;
  if (!(await human(req, res))) return;
  const { email, first_name } = req.body || {};
  if (!validEmail(email)) return res.status(400).json({ error: 'Invalid email' });
  if (mailLimited(res, 'welcome', email)) return;
  const name = typeof first_name === 'string' ? first_name.trim().slice(0, 80) : '';
  if (await addContact(email, name)) await sendEvent('account.created', email); // starts the welcome automation once enabled
  const r = await sendMail({
    to: email,
    subject: 'Your Nuvera Form account and 20% welcome code',
    html: `<div style="font-family:Arial,sans-serif;background:#F7F0E3;color:#3A2816;padding:32px">
<h2 style="margin:0 0 12px">Welcome${name ? ', ' + esc(name) : ''}.</h2>
<p>Your account is active and prices are open to everyone. Use this code for 20% off your first order:</p>
<p style="font-size:26px;font-weight:700;letter-spacing:2px;color:#BF943C;border:2px dashed #BF943C;display:inline-block;padding:10px 18px">NUVERA20</p>
<p>Questions? Reply to this email or call (305) 457-3814, Monday to Friday, 9 AM to 5 PM ET.</p>
<p style="font-size:12px">All products are for Research Use Only and are not for human or veterinary use. You can unsubscribe from promotional emails at any time by replying "unsubscribe".</p></div>`
  });
  if (!r.ok) return res.status(502).json({ error: 'Email provider error' });
  return res.status(200).json({ ok: true });
}
