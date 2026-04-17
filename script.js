// script.js — FAQ accordion
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    const answer = document.getElementById(btn.getAttribute('aria-controls'));

    // Закрыть все
    document.querySelectorAll('.faq-question').forEach(b => {
      b.setAttribute('aria-expanded', 'false');
      document.getElementById(b.getAttribute('aria-controls')).hidden = true;
    });

    // Открыть текущий если был закрыт
    if (!expanded) {
      btn.setAttribute('aria-expanded', 'true');
      answer.hidden = false;
    }
  });
});

// Раскрываем реф-ссылки только при клике
document.querySelectorAll('a[data-href]').forEach(function(a) {
  a.addEventListener('click', function(e) {
    e.preventDefault();
    window.open(a.dataset.href, '_blank', 'noopener,noreferrer');
  });
});
// Nearby cards — показывать первые 5, остальные скрывать
document.addEventListener('DOMContentLoaded', function () {
  var grid = document.getElementById('nearby-grid');
  var btn = document.getElementById('nearby-show-more');

  if (!grid || !btn) return;

  var cards = Array.from(grid.querySelectorAll('.city-card'));
  if (cards.length <= 5) return;

  cards.forEach(function (card, i) {
    if (i >= 5) card.style.display = 'none';
  });

  btn.style.display = 'inline-flex';

  btn.addEventListener('click', function () {
    cards.forEach(function (card) {
      card.style.display = '';
    });
    btn.style.display = 'none';
  });
});
document.addEventListener('DOMContentLoaded', function () {
  var grid = document.getElementById('nearby-grid');
  var btn = document.getElementById('nearby-show-more');

  if (!grid || !btn) return;

  var cards = Array.from(grid.querySelectorAll('.city-card'));
  if (cards.length <= 5) return;

  cards.forEach(function (card, i) {
    if (i >= 5) card.style.display = 'none';
  });

  btn.style.display = 'inline-flex';

  btn.addEventListener('click', function () {
    cards.forEach(function (card) {
      card.style.display = '';
    });
    btn.style.display = 'none';
  });
});