// VIBES — landing page : menu mobile et repli si une maquette est absente.
(function () {
  var toggle = document.querySelector('.nav__toggle');
  var menu = document.getElementById('menu');

  function setMenu(open) {
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
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

  // Si un fichier de maquette est introuvable, on l'indique au lieu d'afficher une image cassée.
  document.querySelectorAll('[data-shot] img').forEach(function (img) {
    function flag() { img.closest('[data-shot]').classList.add('is-missing'); }
    if (img.complete && img.naturalWidth === 0) flag();
    img.addEventListener('error', flag);
  });
})();
