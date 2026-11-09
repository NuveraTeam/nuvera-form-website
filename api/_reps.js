// Rep portal accounts (/rep). Passwords are stored only as scrypt hashes.
// To change a password, run:
//   node -e "const c=require('crypto');const s=c.randomBytes(16).toString('hex');console.log(s,c.scryptSync('NEW-PASSWORD',s,32).toString('hex'))"
// and paste the two values below.
// Commission rates and rep names live in REPS in api/_catalog.js.
import { scryptSync, timingSafeEqual } from 'node:crypto';

const LOGINS = {
  FY305: { salt: '2f3c05d32351b9bfee482c60787f626f', hash: 'cb739977f51f47b5a9f3287f7ccae4ad5eca0ceb1a4b5f9ea01bf7d60083028c' }
};

// Commission payouts already sent to each rep. Add a line every time you pay a rep:
//   { date: '2026-12-01', amount: 120.50, note: 'Zelle, November' }
export const PAYOUTS = {
  FY305: []
};

export function checkLogin(user, pass) {
  const u = String(user || '').trim().toUpperCase();
  const rec = LOGINS[u];
  if (!rec || typeof pass !== 'string' || pass.length > 200) return null;
  const got = scryptSync(pass, rec.salt, 32);
  return timingSafeEqual(got, Buffer.from(rec.hash, 'hex')) ? u : null;
}
