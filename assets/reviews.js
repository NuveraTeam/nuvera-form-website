// Product page reviews: loads approved verified-buyer reviews and adds the rating to the
// page's product data for Google. Runs only where a #reviews element exists.
(function () {
  var box = document.getElementById('reviews');
  if (!box) return;
  var ids = box.getAttribute('data-ids');
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var stars = function (n) { return '<span style="color:#BF943C;letter-spacing:1px" aria-label="' + n + ' out of 5 stars">' + '★★★★★'.slice(0, n) + '<span style="opacity:.3">' + '★★★★★'.slice(0, 5 - n) + '</span></span>'; };
  fetch('/api/reviews?product=' + encodeURIComponent(ids)).then(function (r) { return r.json(); }).then(function (d) {
    var list = box.querySelector('[data-list]');
    if (!d || !d.count) { list.innerHTML = '<p>No reviews yet. Bought this? <a href="/review">Leave a verified review</a>.</p>'; return; }
    box.querySelector('[data-summary]').innerHTML = stars(Math.round(d.avg)) + ' <strong>' + d.avg.toFixed(1) + '</strong> out of 5 · ' + d.count + ' verified review' + (d.count === 1 ? '' : 's');
    list.innerHTML = d.reviews.map(function (r) {
      return '<div class="card" style="margin:.8rem 0">' + stars(r.rating) + '<p style="margin:.4rem 0">' + esc(r.text).replace(/\n/g, '<br>') + '</p><p style="font-size:.8rem;margin:0">' + esc(r.name) + ' · Verified buyer · ' + esc(r.date) + '</p></div>';
    }).join('') + '<p><a href="/review">Leave a verified review</a></p>';
    var ld = [].slice.call(document.querySelectorAll('script[type="application/ld+json"]')).filter(function (s) { return s.textContent.indexOf('"Product"') > -1; })[0];
    if (ld) {
      try {
        var p = JSON.parse(ld.textContent);
        p.aggregateRating = { '@type': 'AggregateRating', ratingValue: d.avg, reviewCount: d.count, bestRating: 5, worstRating: 1 };
        p.review = d.reviews.slice(0, 10).map(function (r) { return { '@type': 'Review', reviewRating: { '@type': 'Rating', ratingValue: r.rating, bestRating: 5 }, author: { '@type': 'Person', name: r.name }, datePublished: r.date, reviewBody: r.text }; });
        ld.textContent = JSON.stringify(p);
      } catch (e) { /* leave product data as is */ }
    }
  }).catch(function () {});
})();
