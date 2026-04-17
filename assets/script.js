// ===================== THEME TOGGLE =====================
(function () {
  const root = document.documentElement;
  let theme = 'light';
  root.setAttribute('data-theme', theme);

  const SUN = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>`;
  const MOON = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

  function setToggleIcon(btn, t) {
    if (!btn) return;
    btn.innerHTML = t === 'dark' ? SUN : MOON;
    btn.setAttribute('aria-label', t === 'dark' ? 'Включить светлую тему' : 'Включить тёмную тему');
  }

  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('[data-theme-toggle]');
    setToggleIcon(btn, theme);
    btn && btn.addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', theme);
      setToggleIcon(btn, theme);
    });
  });
})();

// ===================== FAQ ACCORDION =====================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      const answer = document.getElementById(btn.getAttribute('aria-controls'));

      document.querySelectorAll('.faq-question').forEach(b => {
        b.setAttribute('aria-expanded', 'false');
        const a = document.getElementById(b.getAttribute('aria-controls'));
        if (a) a.hidden = true;
      });

      if (!expanded) {
        btn.setAttribute('aria-expanded', 'true');
        answer.hidden = false;
      }
    });
  });
});

// ===================== SMOOTH SCROLL =====================
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});

// ===================== SCROLL REVEAL =====================
document.addEventListener('DOMContentLoaded', () => {
  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.service-card, .city-card, .info-card, .faq-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    observer.observe(el);
  });
});