(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ----- Header scroll state -----
  const header = document.getElementById('header');
  if (header) {
    let lastY = window.scrollY;
    const onScroll = () => {
      const y = window.scrollY;
      header.classList.toggle('is-scrolled', y > 20);
      lastY = y;
    };
    if (!prefersReducedMotion) {
      let ticking = false;
      window.addEventListener('scroll', () => {
        if (!ticking) {
          requestAnimationFrame(() => {
            onScroll();
            ticking = false;
          });
          ticking = true;
        }
      }, { passive: true });
    } else {
      window.addEventListener('scroll', onScroll, { passive: true });
    }
    onScroll();
  }

  // ----- Mobile nav -----
  const navToggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const open = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', !open);
      nav.classList.toggle('is-open', !open);
      document.body.style.overflow = open ? '' : 'hidden';
    });
    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navToggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        document.body.style.overflow = '';
      });
    });
  }

  // ----- Reveal on scroll -----
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && !prefersReducedMotion) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -40px 0px', threshold: 0.01 }
    );
    revealEls.forEach((el) => observer.observe(el));
  } else if (revealEls.length) {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  // ----- Counter animation -----
  const statValues = document.querySelectorAll('.about-stat-value[data-count], .stats-bar-value[data-count]');
  const animateValue = (el, end, duration = 1500) => {
    const start = 0;
    const startTime = performance.now();
    const step = (now) => {
      const t = Math.min((now - startTime) / duration, 1);
      const easeOut = 1 - Math.pow(1 - t, 3);
      const current = Math.round(start + (end - start) * easeOut);
      el.textContent = current;
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  if (statValues.length && !prefersReducedMotion) {
    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const end = parseInt(el.getAttribute('data-count'), 10);
          if (!isNaN(end)) animateValue(el, end);
          counterObserver.unobserve(el);
        });
      },
      { rootMargin: '0px 0px -60px 0px', threshold: 0.2 }
    );
    statValues.forEach((el) => counterObserver.observe(el));
  } else {
    statValues.forEach((el) => {
      const end = parseInt(el.getAttribute('data-count'), 10);
      if (!isNaN(end)) el.textContent = end;
    });
  }

  // ----- Footer year (in slanted bar) -----
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
