// Rep portal data. POST { user, pass } to sign in, or { token } to refresh.
// Returns sales, commission and payout figures for orders placed with the rep's code.
// Customer details are never returned: only initials, state and items.
import { REPS, PROMO, costOf } from './_catalog.js';
import { checkLogin, PAYOUTS } from './_reps.js';
import { listOrders, storeReady, sign, verify } from './_store.js';

const tries = new Map();
const SESSION_HOURS = 12;
const STALE_DAYS = 30; // unshipped orders older than this are treated as never paid
const r2 = n => Math.round(n * 100) / 100;
const nyDay = d => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(d));

export function buildReport(repId, orders, now = Date.now()) {
  const rep = REPS[repId];
  const code = rep.code;
  const rate = PROMO[code] ? PROMO[code].rate : 0;
  const mine = orders.filter(o => o && (o.rep === repId || o.promo === code))
    .sort((a, b) => String(b.createdAt).localeCompare(String(a.createdAt)));

  const rows = mine.map(o => {
    const subtotal = typeof o.subtotal === 'number' ? o.subtotal : 0;
    const discount = typeof o.discount === 'number' ? o.discount : r2(subtotal * rate);
    const net = r2(subtotal - discount);
    // Commission is paid on profit: sale after the discount minus product cost (no shipping).
    // Uses the cost saved with the order, else today's cost list; unknown cost counts as $0.
    const cost = r2((o.items || []).reduce((a, i) => {
      const c = typeof i.cost === 'number' ? i.cost : costOf(i.id, i.v);
      return a + (c || 0) * (i.q || 0);
    }, 0));
    const base = Math.max(0, r2(net - cost));
    const ageDays = (now - Date.parse(o.createdAt)) / 864e5;
    const status = o.shippedAt ? 'earned' : ageDays > STALE_DAYS ? 'void' : 'pending';
    const units = (o.items || []).reduce((a, i) => a + (i.q || 0), 0);
    return {
      order: String(o.order || '').replace(/.{2}$/, '••'),
      date: o.createdAt, day: nyDay(o.createdAt),
      customer: ((o.first || '?')[0] + '.' + (o.last || '?')[0] + '.').toUpperCase(),
      state: o.state || '',
      items: (o.items || []).map(i => ({ name: i.name, v: i.v, q: i.q })),
      units, subtotal: r2(subtotal), discount: r2(discount), net,
      commission: status === 'void' ? 0 : r2(base * rep.commission), status,
      _email: String(o.email || '').toLowerCase()
    };
  });

  const live = rows.filter(r => r.status !== 'void');
  const sum = (arr, k) => r2(arr.reduce((a, r) => a + r[k], 0));
  const earned = sum(rows.filter(r => r.status === 'earned'), 'commission');
  const pending = sum(rows.filter(r => r.status === 'pending'), 'commission');
  const payouts = (PAYOUTS[repId] || []).slice().sort((a, b) => String(b.date).localeCompare(String(a.date)));
  const paid = r2(payouts.reduce((a, p) => a + (+p.amount || 0), 0));

  // customers: distinct emails, repeat = more than one order
  const per = new Map();
  for (const r of live) per.set(r._email, (per.get(r._email) || 0) + 1);
  const customers = per.size;
  const repeat = [...per.values()].filter(n => n > 1).length;

  // last 30 days, by day (New York time)
  const today = nyDay(now);
  const days = [];
  for (let i = 29; i >= 0; i--) {
    const d = nyDay(now - i * 864e5);
    const on = live.filter(r => r.day === d);
    days.push({ day: d, orders: on.length, net: sum(on, 'net'), commission: sum(on, 'commission') });
  }
  // last 6 months
  const months = [];
  const base = new Date(today + 'T12:00:00Z');
  for (let i = 5; i >= 0; i--) {
    const m = new Date(Date.UTC(base.getUTCFullYear(), base.getUTCMonth() - i, 1)).toISOString().slice(0, 7);
    const on = live.filter(r => r.day.startsWith(m));
    months.push({ month: m, orders: on.length, net: sum(on, 'net'), commission: sum(on, 'commission') });
  }
  const thisM = months[5], lastM = months[4];

  // top products by units (bundles stay as bundles)
  const prod = new Map();
  for (const r of live) for (const i of r.items) {
    const k = i.name;
    const p = prod.get(k) || { name: k, units: 0, orders: 0 };
    p.units += i.q; p.orders += 1; prod.set(k, p);
  }
  const products = [...prod.values()].sort((a, b) => b.units - a.units).slice(0, 6);
  const st = new Map();
  for (const r of live) if (r.state) st.set(r.state, (st.get(r.state) || 0) + 1);
  const states = [...st.entries()].map(([state, orders]) => ({ state, orders })).sort((a, b) => b.orders - a.orders).slice(0, 5);

  return {
    rep: { id: repId, name: rep.name, code, discount: rate, commission: rep.commission, basis: 'profit',
      link: `https://www.nuveraform.com/?code=${code}` },
    updatedAt: new Date(now).toISOString(),
    totals: {
      orders: live.length, units: live.reduce((a, r) => a + r.units, 0),
      gross: sum(live, 'subtotal'), savings: sum(live, 'discount'), net: sum(live, 'net'),
      aov: live.length ? r2(sum(live, 'net') / live.length) : 0,
      customers, repeat, repeatRate: customers ? Math.round((repeat / customers) * 100) : 0,
      earned, pending, paid, balance: r2(earned - paid), lifetime: r2(earned + pending)
    },
    thisMonth: thisM, lastMonth: lastM, days, months, products, states,
    orders: rows.slice(0, 50).map(({ _email, ...r }) => r),
    payouts
  };
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const b = req.body || {};
  let repId = null;

  if (b.token) {
    const [id, exp, sig] = String(b.token).split('.');
    if (REPS[id] && +exp > Date.now() && verify(`rep:${id}:${exp}`, sig)) repId = id;
    else return res.status(401).json({ error: 'Your session ended. Please sign in again.' });
  } else {
    const ip = (req.headers['x-forwarded-for'] || '').split(',')[0] || 'unknown';
    const now = Date.now();
    const recent = (tries.get(ip) || []).filter(t => now - t < 15 * 60e3);
    if (recent.length >= 8) return res.status(429).json({ error: 'Too many sign-in attempts. Try again in 15 minutes.' });
    repId = checkLogin(b.user, b.pass);
    if (!repId || !REPS[repId]) {
      tries.set(ip, [...recent, now]);
      return res.status(401).json({ error: 'Username or password is incorrect.' });
    }
  }

  const exp = Date.now() + SESSION_HOURS * 3600e3;
  const token = `${repId}.${exp}.${sign(`rep:${repId}:${exp}`)}`;
  let orders = [];
  try { orders = storeReady() ? await listOrders() : []; } catch (e) { console.error('rep listOrders', e && e.message); }
  return res.status(200).json({ ok: true, token, ...buildReport(repId, orders) });
}
