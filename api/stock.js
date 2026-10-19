// Public, read-only stock levels. Falls back to an empty object (the page then uses its built-in defaults).
import { configured, readStock } from './_stock.js';
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });
  if (!configured()) return res.status(200).json({ tracked: false, stock: {} });
  try { return res.status(200).json({ tracked: true, stock: await readStock() }); }
  catch { return res.status(200).json({ tracked: false, stock: {} }); }
}
