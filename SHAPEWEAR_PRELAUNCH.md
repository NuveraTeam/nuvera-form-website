# Shapewear prelaunch page

Branch: `shapewear-prelaunch`. Files: `shapewear.html`, `assets/shapewear.css`, this file.

The page is a **prelaunch preview only**:

- `noindex`, not in the site nav, not in `sitemap.xml`.
- No cart, checkout, payment link, price, stock claim, reviews or ratings.
- The main button opens an email to info@nuveraform.com (subject "Shapewear launch waitlist"). No form posts anywhere.
- Every product attribute has a "Pending sample testing" badge. Size and color options are all shown as "Not available yet".
- No peptide or research-compound content or links on the page itself. The og:image is the logo, not `/og.png`, because `og.png` has peptide text.
- No analytics or cookies. `window.nuveraTrack` is a no-op stub. The page also does not load the Vercel Insights script that other pages use.

## Owner inputs still needed

| # | Item | Where it goes |
|---|------|---------------|
| 1 | Final supplier and SKU(s) | `api/_catalog.js` at launch; `ITEM.item_id` in the page script |
| 2 | Product photos and video, with written usage rights (supplier or creator) | Replace the `.ph` placeholder boxes in the hero gallery |
| 3 | Product name | `<h1 id="product-title">`, `<title>`, og tags, `ITEM.item_name` |
| 4 | Price (and any launch discount, with real terms) | `.price` line in the hero |
| 5 | Final size range and color names (with real swatch colors) | Size and color selector buttons, size table rows |
| 6 | Size chart measurements (bust, waist, hips) from measured samples | Size table, replacing every "TBD after samples" |
| 7 | Model height, size worn, measurements, fit advice (true to size or not) | "Fit notes" list |
| 8 | Inventory: how many units on hand or the pre-order plan | Decides whether "in stock" can ever be said |
| 9 | Shipping origin, processing time, delivery times, cost | Shipping section, FAQ, and `shipping-returns.html` |
| 10 | Return and exchange rules for apparel (window, condition, hygiene rules, who pays return shipping) | Shipping section, FAQ, and `shipping-returns.html` |
| 11 | Verified features: which of comfort, stays in place, easy-off closure, tummy control, works under outfits actually held up in sample wear tests | Remove the "Pending sample testing" badge only for claims you can back up; rewrite or delete any that did not hold up |
| 12 | Fabric content and care instructions (from the label or supplier spec) | Comfort card and fabric FAQ. U.S. textile labeling rules require fiber content and country of origin on the product label |
| 13 | Support workflow: who answers email and phone, office hours, response time | Contact section (`[hours — pending]`) |
| 14 | Payment method for this product (current site checkout takes Zelle only) | Checkout wiring, Terms of Sale |
| 15 | Ad budget and channels | Outside the site. Ad copy must match what the page can back up |
| 16 | Creator / affiliate commission terms for this product | Rep program (`rep.html`, `api/_reps.js`) at launch, if used |
| 17 | Whether to keep the phone number 305-457-3814 public on this page | Contact section and footer |

## Things to decide before launch

- **Policy pages.** The footer links to `/shipping-returns`, `/privacy` and `/terms`. Right now those pages are written for the research-compound catalog, and their footers link to compounds. If this page will be an ad landing page with no peptide content, those pages need apparel-specific wording, or separate apparel versions.
- **Canonical host.** The brief said `https://nuveraform.com/shapewear`. The page uses `https://www.nuveraform.com/shapewear` to match every other page's canonical. Change it if the site's main host is the non-www one.
- **Fonts.** The page loads Poppins from Google Fonts, the same as the rest of the site.

## Switching from prelaunch to purchasable (steps, not done yet)

1. **Fill in content.** Replace every placeholder: search `shapewear.html` for `pending`, `TBD`, `[` and `placeholder`. Swap the `.ph` boxes for real `<img>` tags with descriptive `alt` text, `width`/`height`, and WebP plus a fallback (see `tools/make-images.py` for how the site makes product images).
2. **Remove the prelaunch markers.** Delete the `.prebar` banner. Remove each "Pending sample testing" badge only for features you verified. Change the footer blurb.
3. **Make selectors real.** For sizes and colors in stock, remove `aria-disabled="true"`, the line-through style, and the "(not available yet)" text. Turn them into a real radio group (`<input type="radio">` with `<label>`s) so the chosen value can be submitted. Keep out-of-stock options disabled.
4. **Wire into the catalog and order flow.**
   - Add the SKU(s), with price and size/color variants, to `api/_catalog.js`. `api/order.js` checks prices against it, so the server will reject any price it does not know.
   - Add an add-to-cart button that uses the same cart and checkout as `index.html`, or link to the product in the main catalog. Test a full order on a Vercel preview deployment before merging.
   - If needed, set `REORDER_WEEKS` for the SKU in `api/_catalog.js`. Usually not needed for apparel.
5. **Analytics.** If you add analytics, replace the body of `window.nuveraTrack` with the real call. Fire `add_to_cart`, `begin_checkout` and `purchase` from the checkout code. If the tool sets cookies or tracks across sites, add consent and update `privacy.html` first.
6. **SEO and discovery.**
   - Change `<meta name="robots" content="noindex">` to `index,follow,max-image-preview:large`.
   - Add `<url><loc>https://www.nuveraform.com/shapewear</loc>...</url>` to `sitemap.xml`.
   - Add a link in the site nav or footer if wanted.
   - Optional: add `Product` JSON-LD with the real price and availability. Only use real values, and add no `aggregateRating` until real reviews exist.
   - Optional: make a shapewear-specific `og:image` (1200×630).
7. **Policies.** Update `shipping-returns.html`, `terms.html` and `privacy.html` for apparel (see "Things to decide" above).
8. **Review the copy.** Re-read every claim against the sample test results (FTC truth-in-advertising: every claim needs support). Make sure there are no medical, health or compression claims, no body-shaming, and no before/after transformation language.
9. **Ship it.** Open a normal (non-draft) PR, check the Vercel preview, then merge to `main`. Merging to `main` deploys to production.
