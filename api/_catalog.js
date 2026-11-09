// Server-side price list used to check every order total.
// Keep in sync with the `P` list in index.html when prices or sizes change.
// (Files starting with "_" in /api are not deployed as endpoints.)
export const PRICES = {
  ret: { name: 'GLP-3', v: { '5mg': 105, '10mg': 140, '15mg': 170 } },
  ghk: { name: 'GHK-Cu 100mg', v: { '100mg': 85 } },
  ta1: { name: 'Thymosin Alpha 1 10mg', v: { '10mg': 95 } },
  bpc: { name: 'BPC-157 / TB-500 Blend 10mg', v: { '10mg': 110 } },
  nad: { name: 'NAD+ 500mg', v: { '500mg': 90 } },
  cjc: { name: 'CJC-1295 / Ipamorelin Blend 10mg', v: { '10mg': 105 } },
  mot: { name: 'MOTS-c 10mg', v: { '10mg': 95 } },
  klo: { name: 'KLOW Blend', v: { 'Blend': 145 } },
  kis: { name: 'Kisspeptin 10mg', v: { '10mg': 85 } },
  bac: { name: 'Bacteriostatic Water 10ml', v: { '10ml': 10 } },
  bn1: { name: 'Recovery Duo: BPC-157/TB-500 Blend + GHK-Cu 100mg', v: { 'Bundle': 175 } },
  bn2: { name: 'GLP-3 10mg + Bacteriostatic Water 10ml', v: { 'Bundle': 145 } }
};

export const SHIPPING = {
  ground: { label: 'Ground (3–5 business days)', price: 25 },
  overnight: { label: 'Overnight (next business day)', price: 60 }
};

// Promo codes. Only one code can be used per order.
// firstOrder: usable only by customers with no earlier order (email, phone or address).
// rep: the rep account credited with the sale in the rep portal (/rep).
export const PROMO = {
  NUVERA10: { rate: 0.10, firstOrder: true },
  FY305: { rate: 0.20, rep: 'FY305' }
};

// Rep accounts for the rep portal. commission = share of the order subtotal after the
// discount (shipping excluded). Change the rate here; the portal recalculates every order.
export const REPS = {
  FY305: { name: 'FightingYo305', code: 'FY305', commission: 0.10 }
};

// What a customer can review, and where it shows: catalog id -> display name + product page.
// Bundles count as their parts. Old orders used the id 'ret' for GLP-3.
export const REVIEWABLE = {
  ret: { name: 'GLP-3', page: 'glp-3' },
  ghk: { name: 'GHK-Cu', page: 'ghk-cu' },
  ta1: { name: 'Thymosin Alpha 1', page: 'thymosin-alpha-1' },
  bpc: { name: 'BPC-157 / TB-500 Blend', page: 'bpc-157' },
  nad: { name: 'NAD+', page: 'nad-plus' },
  cjc: { name: 'CJC-1295 / Ipamorelin Blend', page: 'cjc-1295-ipamorelin' },
  mot: { name: 'MOTS-c', page: 'mots-c' },
  klo: { name: 'KLOW Blend', page: 'klow-blend' },
  kis: { name: 'Kisspeptin', page: 'kisspeptin' },
  bac: { name: 'Bacteriostatic Water', page: 'bacteriostatic-water' }
};
export const BUNDLE_PARTS = { bn1: ['bpc', 'ghk'], bn2: ['ret', 'bac'] };
export const reviewableIds = items =>
  [...new Set(items.flatMap(i => BUNDLE_PARTS[i.id] || [i.id]))].filter(id => REVIEWABLE[id]);

// Weeks after shipping to send a reorder reminder, per catalog id. A product with no number
// gets no reminder. Bundles use the longest of their parts.
export const REORDER_WEEKS = {};

// Days after shipping to ask for a review.
export const REVIEW_REQUEST_DAYS = 7;
