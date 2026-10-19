# Welcome email series (DRAFT, not activated)

Trigger: account created. All emails: RUO footer, unsubscribe link, no health or dosing claims, no unverified testing claims.
Send from hello@nuveraform.com via Resend. Day 0 is already sent by `api/welcome.js`.

## Email 1 (day 0, exists): Your Nuvera Form account and 10% welcome code
Contains NUVERA10 and a link to the catalog.

## Email 2 (day 2): Start with the paperwork
Subject: How to read a certificate of analysis
Body: Short intro; links to /learn/how-to-read-a-certificate-of-analysis and /learn/peptide-research-glossary; a line that documentation availability varies by batch and can be requested at info@nuveraform.com.

## Email 3 (day 5): Handling and storage
Subject: Storing and reconstituting research material
Body: Links to /learn/storing-lyophilized-peptides, /learn/reconstitution-for-lab-work and /learn/bacteriostatic-vs-sterile-water. Reminder that NUVERA10 is still active on a first order.

## Email 4 (day 10, only if no order): Your code is still waiting
Subject: Your 10% code is still active
Body: Link to categories; free shipping on orders of $200 or more; reply-to info@nuveraform.com.

## To activate
1. Decide whether contacts live in Resend (Audience) or stay in Web3Forms; add a contact-create call to `api/welcome.js` if Resend.
2. Build the sequence as a Resend automation using the copy above, then review before enabling.
