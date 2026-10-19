// Vercel serverless function: sends the welcome email with the NUVERA10 code via Resend.
// The API key lives in Vercel environment variables, never in the browser.
const hits = new Map();
const esc = (v = '') => String(v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const allowed = (process.env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  const origin = req.headers.origin || '';
  if (allowed.length && !allowed.includes(origin)) return res.status(403).json({ error: 'Forbidden' });

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0] || 'unknown';
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter(t => now - t < 3600e3);
  if (recent.length >= 5) return res.status(429).json({ error: 'Too many requests' });
  hits.set(ip, [...recent, now]);

  const { email, first_name } = req.body || {};
  if (typeof email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254)
    return res.status(400).json({ error: 'Invalid email' });

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: process.env.MAIL_FROM || 'Nuvera Form <hello@nuveraform.com>',
      to: [email],
      reply_to: 'info@nuveraform.com',
      subject: 'Your Nuvera Form account and 10% welcome code',
      html: `<div style="font-family:Arial,sans-serif;background:#F7F0E3;color:#3A2816;padding:32px">
<img src="https://nuveraform.com/assets/logo-128.png" alt="Nuvera Form" width="72" height="72" style="display:block;width:72px;height:72px;border:0;margin:0 0 20px">
<h2 style="margin:0 0 12px">Welcome${first_name ? ', ' + esc(first_name) : ''}.</h2>
<p>Your account is active and the catalog is unlocked. Use this code for 10% off your first order:</p>
<p style="font-size:26px;font-weight:700;letter-spacing:2px;color:#BF943C;border:2px dashed #BF943C;display:inline-block;padding:10px 18px">NUVERA10</p>
<p style="font-size:12px">All products are for Research Use Only and are not for human or veterinary use. Questions? Reply to this email.</p></div>`
    })
  });
  if (!r.ok) return res.status(502).json({ error: 'Email provider error' });
  return res.status(200).json({ ok: true });
}
