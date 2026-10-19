// Emails the customer their order number and Zelle payment instructions.
// The order itself is also sent to the store owner through Web3Forms from the browser.
import { guard, validEmail, esc, sendMail } from './_lib.js';

export default async function handler(req, res) {
  if (guard(req, res, { limit: 10, bucket: 'order' })) return;
  const { email, name, order_number, total, items } = req.body || {};
  if (!validEmail(email)) return res.status(400).json({ error: 'Invalid email' });
  if (typeof order_number !== 'string' || !/^NF-\d{6}-[A-Z0-9]{4}$/.test(order_number)) return res.status(400).json({ error: 'Invalid order' });
  const amt = Number(total);
  if (!Number.isFinite(amt) || amt <= 0 || amt > 100000) return res.status(400).json({ error: 'Invalid total' });
  const lines = Array.isArray(items) ? items.slice(0, 30).map(i => `<li>${esc(String(i).slice(0, 160))}</li>`).join('') : '';
  const r = await sendMail({
    to: email,
    subject: `Nuvera Form order ${order_number}: payment instructions`,
    html: `<div style="font-family:Arial,sans-serif;background:#F7F0E3;color:#3A2816;padding:32px">
<h2 style="margin:0 0 12px">Thank you${name ? ', ' + esc(String(name).slice(0, 80)) : ''}.</h2>
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
