# Welcome email series

Built in Resend (automation **disabled** until reviewed):
- Event: `account.created`, sent by `api/welcome.js` after the contact is saved to the "General" segment.
- Day 0: welcome + NUVERA20 code (sent directly by `api/welcome.js`).
- Day 2: "How to read a certificate of analysis" (template `welcome-2-coa`).
- Day 5: "Storing and reconstituting research material" (template `welcome-3-handling`).
All emails carry the RUO footer and an unsubscribe link. Preview/edit in the Resend dashboard, then switch the automation on.
