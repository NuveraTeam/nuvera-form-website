// Server-side price list used to check every order total.
// Keep in sync with the `P` list in index.html when prices or sizes change.
// (Files starting with "_" in /api are not deployed as endpoints.)
export const PRICES = {
  ret: { name: 'Retatrutide', v: { '5mg': 115, '10mg': 180, '15mg': 240 } },
  ghk: { name: 'GHK-Cu 100mg', v: { '100mg': 85 } },
  ta1: { name: 'Thymosin Alpha 1 10mg', v: { '10mg': 95 } },
  bpc: { name: 'BPC-157 / TB-500 Blend 10mg', v: { '10mg': 110 } },
  nad: { name: 'NAD+ 500mg', v: { '500mg': 90 } },
  cjc: { name: 'CJC-1295 / Ipamorelin Blend 10mg', v: { '10mg': 105 } },
  mot: { name: 'MOTS-c 10mg', v: { '10mg': 95 } },
  klo: { name: 'KLOW Blend', v: { 'Blend': 120 } },
  kis: { name: 'Kisspeptin 10mg', v: { '10mg': 85 } },
  bac: { name: 'Bacteriostatic Water 10ml', v: { '10ml': 15 } },
  bn1: { name: 'Recovery Duo: BPC-157/TB-500 Blend + GHK-Cu 100mg', v: { 'Bundle': 175.5 } },
  bn2: { name: 'Retatrutide 10mg + Bacteriostatic Water 10ml', v: { 'Bundle': 175.5 } }
};

export const SHIPPING = {
  ground: { label: 'Ground (3–5 business days)', price: 25 },
  overnight: { label: 'Overnight (next business day)', price: 60 }
};

export const PROMO = { NUVERA10: 0.10 };
