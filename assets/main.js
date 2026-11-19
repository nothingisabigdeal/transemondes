(function () {
  // Menu mobile
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');
  if (header && toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('is-open');
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.querySelector('span').textContent = open ? 'Fermer' : 'Menu';
    });
    header.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('is-open');
        document.body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.querySelector('span').textContent = 'Menu';
      });
    });
  }

  // Rubrique active
  var page = document.body.getAttribute('data-page');
  document.querySelectorAll('.nav__item[data-section]').forEach(function (item) {
    if (item.getAttribute('data-section').split(' ').indexOf(page) > -1) item.classList.add('is-active');
  });

  // Dates passées grisées
  var today = new Date(); today.setHours(0, 0, 0, 0);
  document.querySelectorAll('[data-date]').forEach(function (el) {
    var d = new Date(el.getAttribute('data-date') + 'T23:59:59');
    if (d < today) el.classList.add('is-past');
  });

  // Images indisponibles : on garde un cadre teinté
  document.querySelectorAll('.media img, .brand img').forEach(function (img) {
    function broken() {
      var box = img.closest('.media');
      if (box) box.classList.add('is-broken'); else img.style.display = 'none';
    }
    if (img.complete && img.naturalWidth === 0) broken();
    img.addEventListener('error', broken);
  });

  // Copier l'IBAN
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = document.getElementById(btn.getAttribute('data-copy')).textContent.trim();
      var done = function () { btn.textContent = 'Copié'; setTimeout(function () { btn.textContent = 'Copier'; }, 1800); };
      var fallback = function () {
        var r = document.createRange(); r.selectNodeContents(document.getElementById(btn.getAttribute('data-copy')));
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        btn.textContent = 'Sélectionné';
      };
      try { navigator.clipboard.writeText(text).then(done, fallback); } catch (e) { fallback(); }
    });
  });
})();
