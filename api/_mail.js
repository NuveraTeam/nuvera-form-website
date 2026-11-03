// Shared email sending (Resend) and the branded email layout.
export const SITE = 'https://www.nuveraform.com';
export const esc = (v = '') => String(v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export async function send(payload) {
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: process.env.MAIL_FROM || 'Nuvera Form <hello@nuveraform.com>', reply_to: 'info@nuveraform.com', ...payload })
    });
    return r.ok;
  } catch { return false; }
}

export const button = (href, label) =>
  `<a href="${esc(href)}" style="display:inline-block;background:#BF943C;color:#fff;font-weight:700;text-decoration:none;border-radius:999px;padding:12px 22px">${esc(label)}</a>`;

export function layout(body, footerExtra = '') {
  return `<div style="font-family:Arial,sans-serif;background:#F7F0E3;color:#3A2816;padding:32px">
<img src="${SITE}/assets/nuvera-logo-hd-192.png" alt="Nuvera Form" width="64" height="64" style="display:block;width:64px;height:64px;border:0;margin:0 0 16px">
${body}
<p style="font-size:12px;margin-top:24px">All products are for Research Use Only and are not for human or veterinary use. Questions? Reply to this email or call 305-457-3814.</p>${footerExtra}</div>`;
}
