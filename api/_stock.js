// Inventory in Redis (Upstash REST, added through the Vercel Marketplace: KV_REST_API_URL / KV_REST_API_TOKEN).
// Stock lives in one hash, "stock", field = "<id>|<variant>". Decrements use HINCRBY, which is atomic per field,
// so two buyers can never both take the last unit: whoever drives the count below zero is rolled back.
import { DEFAULT_STOCK, PRODUCTS, components, sku } from './_catalog.js';

const URL_ = () => process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
const TOKEN = () => process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
export const configured = () => Boolean(URL_() && TOKEN());

/** Runs commands in one round trip. Returns the raw results, or throws. */
export async function redis(commands) {
  const r = await fetch(`${URL_()}/pipeline`, { method: 'POST', headers: { Authorization: `Bearer ${TOKEN()}`, 'Content-Type': 'application/json' }, body: JSON.stringify(commands) });
  if (!r.ok) throw new Error('redis ' + r.status);
  const out = await r.json();
  if (out.some(x => x.error)) throw new Error('redis command error');
  return out.map(x => x.result);
}

/** Creates any missing stock fields from the defaults (never overwrites). */
export async function seed() {
  await redis(Object.entries(DEFAULT_STOCK).map(([k, v]) => ['HSETNX', 'stock', k, v]));
}

export async function readStock() {
  await seed();
  const [flat] = await redis([['HGETALL', 'stock']]);
  const s = {};
  for (let i = 0; i < flat.length; i += 2) s[flat[i]] = Number(flat[i + 1]);
  // Bundles are limited by their scarcest component.
  for (const [id, p] of Object.entries(PRODUCTS)) if (p.parts) s[sku(id, 'Bundle')] = Math.max(0, Math.min(...p.parts.map(([i, v]) => s[sku(i, v)] ?? 0)));
  return s;
}

/** lines: [{id, v, q}] (already validated). Returns {ok:true} or {ok:false, sku, available}. */
export async function reserve(lines) {
  const need = {};
  for (const l of lines) for (const [k, n] of components(l.id, l.v)) need[k] = (need[k] || 0) + n * l.q;
  await seed();
  const keys = Object.keys(need);
  const res = await redis(keys.map(k => ['HINCRBY', 'stock', k, -need[k]]));
  const bad = keys.findIndex((k, i) => res[i] < 0);
  if (bad >= 0) {
    await redis(keys.map(k => ['HINCRBY', 'stock', k, need[k]]));
    return { ok: false, sku: keys[bad], available: Math.max(0, res[bad] + need[keys[bad]]) };
  }
  return { ok: true, need };
}

/** Gives reserved units back (order cancelled or failed after reserving). */
export async function release(need) {
  const keys = Object.keys(need);
  if (keys.length) await redis(keys.map(k => ['HINCRBY', 'stock', k, need[k]]));
}
