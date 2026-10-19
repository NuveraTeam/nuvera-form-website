// Emails the customer their order number and Zelle payment instructions.
// The order itself is also sent to the store owner through Web3Forms from the browser.
import { guard, mailLimited, validEmail, esc, sendMail } from './_lib.js';

export default async function handler(req, res) {
  if (guard(req, res, { limit: 10, bucket: 'order' })) return;
  const { email, name, order_number, total, items } = req.body || {};
  if (!validEmail(email)) return res.status(400).json({ error: 'Invalid email' });
  if (typeof order_number !== 'string' || !/^NF-\d{6}-[A-Z0-9]{4}$/.test(order_number)) return res.status(400).json({ error: 'Invalid order' });
  // Items must look like the lines the storefront builds, and the total must equal what the storefront's own
  // pricing rules give for them (optional 20% first-order code, $15 shipping under $200). This keeps the endpoint
  // from being used to send arbitrary text or amounts from our domain to a third party.
  if (!Array.isArray(items) || !items.length || items.length > 30) return res.status(400).json({ error: 'Invalid items' });
  let sub = 0;
  for (const i of items) {
    const m = typeof i === 'string' && /^([\w .+\/()\-:,]{1,100}) x(\d{1,2}) @ \$(\d{1,4}\.\d{2})$/.exec(i);
    if (!m) return res.status(400).json({ error: 'Invalid items' });
    sub += Math.round(parseFloat(m[3]) * 100) * Number(m[2]);
  }
  const cents = Math.round(Number(total) * 100);
  const expect = d => { const net = sub - d; return net + (net >= 20000 ? 0 : 1500); };
  if (!Number.isFinite(cents) || ![expect(0), expect(Math.round(sub * 0.2))].includes(cents)) return res.status(400).json({ error: 'Invalid total' });
  if (mailLimited(res, 'order', email, 5)) return;
  const amt = cents / 100;
  const lines = items.map(i => `<li>${esc(i)}</li>`).join('');
  const who = typeof name === 'string' && /^[\p{L}\p{M} .'’-]{1,80}$/u.test(name.trim()) ? name.trim() : '';
  const r = await sendMail({
    to: email,
    subject: `Nuvera Form order ${order_number}: payment instructions`,
    html: `<div style="font-family:Arial,sans-serif;background:#F7F0E3;color:#3A2816;padding:32px">
<h2 style="margin:0 0 12px">Thank you${who ? ', ' + esc(who) : ''}.</h2>
<p>We received your order <b>${esc(order_number)}</b>.</p><ul>${lines}</ul>
<p><b>Total due: $${amt.toFixed(2)}</b></p>
<p><b>Pay by Zelle:</b> send $${amt.toFixed(2)} to <b>(305) 457-3814</b> and put <b>${esc(order_number)}</b> in the memo. Please check the recipient name shown by your bank before sending.</p>
<p>We confirm payment by email and ship within 1–2 business days after that. The amount above is confirmed by us when we review your order.</p>
<p>Questions? Reply to this email or call (305) 457-3814, Monday to Friday, 9 AM to 5 PM ET.</p>
<p style="font-size:12px">All products are for Research Use Only and are not for human or veterinary use.</p></div>`
  });
  if (!r.ok) return res.status(502).json({ error: 'Email provider error' });
  return res.status(200).json({ ok: true });
}
