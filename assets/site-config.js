// Public site settings. The Turnstile SITE key is public by design (the secret key lives in Vercel env vars).
// Leave TS_KEY empty until the Cloudflare Turnstile widget is created; forms keep working without it.
window.NV = { TS_KEY: '' };
