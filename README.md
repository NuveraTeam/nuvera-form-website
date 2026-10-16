# Nuvera Form storefront

Static site (`index.html`) plus one serverless function (`api/welcome.js`) that sends the welcome email through Resend.

## 1. GitHub
```bash
cd nuvera-form
git init -b main
git add .
git commit -m "Initial Nuvera Form storefront"
# create an empty repo named nuvera-form on github.com first, then:
git remote add origin https://github.com/YOUR-USER/nuvera-form.git
git push -u origin main
```

## 2. Vercel
1. vercel.com > Add New > Project > import the GitHub repo. Framework preset: Other. No build command.
2. Settings > Environment Variables, add the three values from `.env.example` (Production and Preview).
3. Deploy. Every push to `main` redeploys automatically.

## 3. Domain (nuveraform.com)
1. Vercel > Project > Settings > Domains > add `nuveraform.com` and `www.nuveraform.com`.
2. At your registrar, add the records Vercel shows you. Typically:
   - `A` record, host `@`, value `76.76.21.21`
   - `CNAME`, host `www`, value `cname.vercel-dns.com`
   Use the exact values Vercel displays for your project if they differ.
3. Wait for propagation (minutes to a few hours). Vercel issues the HTTPS certificate automatically.

## 4. Resend (email)
1. resend.com > Domains > add `nuveraform.com`.
2. Add the SPF and DKIM DNS records Resend gives you at your registrar (they are specific to your account), then click Verify.
3. Create an API key (sending access only) and paste it into Vercel as `RESEND_API_KEY`. Redeploy.
4. Test: sign up on the live site with your own email.

## 5. Web3Forms
The access key in `index.html` is a public key by design. In the Web3Forms dashboard, add `nuveraform.com` as an allowed domain and set the notification email for leads and affiliate applications.

## 6. Before taking payments
Replace the placeholder Privacy and Terms text, connect a real checkout and payment processor, and confirm every claim on the site is supportable.
