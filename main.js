// VIBES — landing page : menu mobile, apparition douce des blocs, repli si une maquette est absente.
(function () {
  var toggle = document.querySelector('.nav__toggle');
  var menu = document.getElementById('menu');

  function setMenu(open) {
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? toggle.dataset.labelClose : toggle.dataset.labelOpen);
    toggle.querySelector('use').setAttribute('href', open ? '#i-x' : '#i-menu');
  }

  toggle.addEventListener('click', function () {
    setMenu(toggle.getAttribute('aria-expanded') !== 'true');
  });
  menu.addEventListener('click', function (e) {
    if (e.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      toggle.focus();
    }
  });
  window.matchMedia('(min-width: 960px)').addEventListener('change', function (e) {
    if (e.matches) setMenu(false);
  });

  // Si un fichier de maquette est introuvable, on l'indique au lieu d'afficher une image cassée.
  document.querySelectorAll('[data-shot] img').forEach(function (img) {
    function flag() { img.closest('[data-shot]').classList.add('is-missing'); }
    if (img.complete && img.naturalWidth === 0) flag();
    img.addEventListener('error', flag);
  });

  // Apparition douce au défilement (sans effet si l'utilisateur préfère réduire les animations).
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      // Visible, ou déjà dépassé (ex. saut par un lien d'ancre) : on l'affiche.
      if (en.isIntersecting || en.boundingClientRect.top < 0) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  items.forEach(function (el) { io.observe(el); });
})();
