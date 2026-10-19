/* Forms on the static pages: newsletter (#nl) and service review (#rv). Optional Cloudflare Turnstile via assets/site-config.js. */
(function () {
  var KEY = 'e71a64f9-3da5-4fde-b2ff-3463cd3f1c41', TS = (window.NV || {}).TS_KEY || '';
  var forms = ['nl', 'rv'].map(function (id) { return document.getElementById(id); }).filter(Boolean);
  if (TS && forms.length) {
    forms.forEach(function (f) { var d = document.createElement('div'); d.className = 'cf-turnstile'; d.setAttribute('data-sitekey', TS); f.insertBefore(d, f.querySelector('button')); });
    var s = document.createElement('script'); s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js'; s.async = true; s.defer = true; document.head.appendChild(s);
  }
  function tok(f) { var i = f.querySelector('[name=cf-turnstile-response]'); return i ? i.value : ''; }
  function reset() { try { if (window.turnstile) turnstile.reset(); } catch (e) {} }
  function send(data) {
    return fetch('https://api.web3forms.com/submit', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(Object.assign({ access_key: KEY, from_name: 'Nuvera Form Store', page: location.pathname }, data)) })
      .then(function (r) { return r.json(); }).then(function (j) { if (!j.success) throw 0; });
  }
  var nl = document.getElementById('nl');
  if (nl) nl.addEventListener('submit', function (e) {
    e.preventDefault(); var m = document.getElementById('nlm'); m.textContent = 'Subscribing…'; var f = new FormData(nl);
    send({ subject: 'Nuvera Form list sign-up', email: f.get('email'), botcheck: f.get('botcheck') ? '1' : '' }).then(function () {
      fetch('/api/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: f.get('email'), cf_token: tok(nl) }) }).catch(function () {});
      m.textContent = 'You are on the list.'; nl.reset(); reset();
    }).catch(function () { m.textContent = 'Could not subscribe. Please try again or email info@nuveraform.com.'; reset(); });
  });
  var rv = document.getElementById('rv');
  if (rv) rv.addEventListener('submit', function (e) {
    e.preventDefault(); var m = document.getElementById('rvm'); m.textContent = 'Sending…'; var f = new FormData(rv), d = {};
    f.forEach(function (v, k) { if (k !== 'cf-turnstile-response') d[k] = v; });
    send(Object.assign({ subject: 'Service review submitted (pending moderation)' }, d)).then(function () { m.textContent = 'Thank you. We check every review against your order before publishing.'; rv.reset(); reset(); })
      .catch(function () { m.textContent = 'Could not send your review. Please email info@nuveraform.com.'; reset(); });
  });
})();
