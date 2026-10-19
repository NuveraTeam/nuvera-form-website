// Server-side catalog: the source of truth for prices, default stock and bundle contents.
// Keep in sync with the P array in index.html (tools/check-catalog.mjs verifies this).
// price in dollars, stock = default on-hand units used to seed the inventory store.
export const PRODUCTS = {
  ret: { n: 'Retatrutide', v: { '5mg': { p: 115, s: 1 }, '10mg': { p: 180, s: 8 }, '15mg': { p: 240, s: 1 } } },
  ghk: { n: 'GHK-Cu 100mg', v: { '100mg': { p: 85, s: 10 } } },
  ta1: { n: 'Thymosin Alpha 1 10mg', v: { '10mg': { p: 95, s: 2 } } },
  bpc: { n: 'BPC-157 / TB-500 Blend 10mg', v: { '10mg': { p: 110, s: 5 } } },
  nad: { n: 'NAD+ 500mg', v: { '500mg': { p: 90, s: 1 } } },
  cjc: { n: 'CJC-1295 / Ipamorelin Blend 10mg', v: { '10mg': { p: 105, s: 2 } } },
  mot: { n: 'MOTS-c 10mg', v: { '10mg': { p: 95, s: 10 } } },
  klo: { n: 'KLOW Blend 80mg', v: { '80mg': { p: 120, s: 3 } } },
  kis: { n: 'Kisspeptin 10mg', v: { '10mg': { p: 85, s: 2 } } },
  bac: { n: 'Bacteriostatic Water 10ml', v: { '10ml': { p: 15, s: 3 } } },
  bn1: { n: 'Research Duo: BPC-157/TB-500 Blend + GHK-Cu 100mg', v: { Bundle: { p: 175.5 } }, parts: [['bpc', '10mg'], ['ghk', '100mg']] },
  bn2: { n: 'Retatrutide 10mg + Bacteriostatic Water 10ml', v: { Bundle: { p: 175.5 } }, parts: [['ret', '10mg'], ['bac', '10ml']] }
};
export const sku = (id, v) => `${id}|${v}`;
/** Default stock for every non-bundle SKU. */
export const DEFAULT_STOCK = Object.fromEntries(
  Object.entries(PRODUCTS).filter(([, p]) => !p.parts).flatMap(([id, p]) => Object.entries(p.v).map(([v, x]) => [sku(id, v), x.s])));
export const priceCents = (id, v) => Math.round(PRODUCTS[id].v[v].p * 100);
/** SKUs (and quantities) that one unit of this line consumes. */
export const components = (id, v) => PRODUCTS[id].parts ? PRODUCTS[id].parts.map(([i, vv]) => [sku(i, vv), 1]) : [[sku(id, v), 1]];
export const lineName = (id, v) => PRODUCTS[id].n + (Object.keys(PRODUCTS[id].v).length > 1 ? ' ' + v : '');
export const TOTALS = (sub, promo) => { const disc = promo ? Math.round(sub * 0.2) : 0, net = sub - disc, ship = sub && net < 20000 ? 1500 : 0; return { sub, disc, net, ship, total: net + ship }; };
