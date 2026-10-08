/* ==================================================================
   Classic Comfort Interior and Exterior — landing page scripts
   ================================================================== */
(function () {
  'use strict';

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* ------------------------------------------------------------ header */
  const header = $('#siteHeader');
  const nav = $('#mainNav');
  const toggle = $('#navToggle');

  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 10);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  function closeMenu() {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    document.body.classList.remove('no-scroll');
  }

  toggle.addEventListener('click', () => {
    const open = !nav.classList.contains('open');
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('no-scroll', open);
  });
  $$('a', nav).forEach((a) => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });

  /* Highlight the nav link of the section in view. Sections without their own
     nav link (gallery, why us, process…) count as the nearest one above them. */
  const navLinks = $$('[data-nav]', nav);
  const navSections = navLinks
    .map((link) => document.getElementById(link.dataset.nav))
    .filter(Boolean);

  function updateActiveNav() {
    const y = window.scrollY + window.innerHeight * 0.35;
    let current = navSections[0];
    navSections.forEach((sec) => { if (sec.offsetTop <= y) current = sec; });
    // reached the bottom of the page: activate the last section
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 4) {
      current = navSections[navSections.length - 1];
    }
    navLinks.forEach((l) => l.classList.toggle('active', current && l.dataset.nav === current.id));
  }
  if (navSections.length) {
    updateActiveNav();
    window.addEventListener('scroll', updateActiveNav, { passive: true });
    window.addEventListener('resize', updateActiveNav);
  }

  /* ------------------------------------------------------------ scroll reveal */
  const revealEls = $$('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('in-view'));
  }

  /* ------------------------------------------------------------ enquire buttons + project arrows → contact form */
  const serviceSelect = $('#id_service');
  $$('a[href="#contact"][data-service]').forEach((link) => {
    link.addEventListener('click', () => {
      if (!serviceSelect) return;
      const wanted = link.dataset.service;
      const options = Array.from(serviceSelect.options).filter((o) => o.value);
      // exact match first (service cards), then a key-word match (project names like
      // "Modular Kitchen" → "Kitchen Interior", "Wardrobe" → "Wardrobes")
      const stem = (w) => w.toLowerCase().replace(/s$/, '');
      const words = wanted.split(/\s+/).map(stem).filter((w) => w.length > 3);
      const option = options.find((o) => o.value === wanted)
        || options.find((o) => o.value.split(/\s+/).map(stem).some((w) => words.includes(w)));
      if (option) {
        serviceSelect.value = option.value;
        validateField(serviceSelect);
      }
      // focus the first empty field once the smooth scroll has finished
      setTimeout(() => {
        const firstEmpty = $$('#enquiryForm input:not([name="website"]):not([type="hidden"]), #enquiryForm textarea')
          .find((f) => !f.value.trim());
        if (firstEmpty) firstEmpty.focus({ preventScroll: true });
      }, 700);
    });
  });

  /* ------------------------------------------------------------ portfolio filter */
  const filterBtns = $$('.filter-btn');
  const projectCards = $$('.project-card');
  const emptyMsg = $('#portfolioEmpty');

  function applyFilter(filter) {
    let visible = 0;
    projectCards.forEach((card) => {
      const show = filter === 'all' || card.dataset.category === filter;
      card.classList.toggle('is-hidden', !show);
      if (show) {
        visible += 1;
        card.classList.add('in-view');
      }
    });
    if (emptyMsg) emptyMsg.hidden = visible > 0;
  }

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach((b) => {
        b.classList.toggle('is-active', b === btn);
        b.setAttribute('aria-selected', String(b === btn));
      });
      applyFilter(btn.dataset.filter);
    });
  });
  if (projectCards.length === 0 && emptyMsg) emptyMsg.hidden = false;

  /* ------------------------------------------------------------ lightbox */
  const lb = $('#lightbox');
  const lbImg = $('#lbImage');
  const lbCaption = $('#lbCaption');
  const lbCount = $('#lbCount');
  let lbItems = [];
  let lbIndex = 0;
  let lastFocus = null;

  function showLb(i) {
    lbIndex = (i + lbItems.length) % lbItems.length;
    const item = lbItems[lbIndex];
    lbImg.src = item.src;
    lbImg.alt = item.caption || '';
    lbCaption.textContent = item.caption || '';
    lbCount.textContent = `${lbIndex + 1} / ${lbItems.length}`;
  }

  function openLb(items, start = 0) {
    if (!items.length) return;
    lbItems = items;
    lastFocus = document.activeElement;
    lb.classList.toggle('single', items.length < 2);
    showLb(start);
    lb.hidden = false;
    document.body.classList.add('no-scroll');
    $('.lb-close', lb).focus();
  }

  function closeLb() {
    lb.hidden = true;
    lbImg.removeAttribute('src');
    document.body.classList.remove('no-scroll');
    if (lastFocus) lastFocus.focus();
  }

  $('.lb-close', lb).addEventListener('click', closeLb);
  $('.lb-prev', lb).addEventListener('click', () => showLb(lbIndex - 1));
  $('.lb-next', lb).addEventListener('click', () => showLb(lbIndex + 1));
  lb.addEventListener('click', (e) => { if (e.target === lb) closeLb(); });
  document.addEventListener('keydown', (e) => {
    if (lb.hidden) return;
    if (e.key === 'Escape') closeLb();
    if (e.key === 'ArrowLeft') showLb(lbIndex - 1);
    if (e.key === 'ArrowRight') showLb(lbIndex + 1);
  });

  // swipe on touch screens
  let touchX = null;
  lb.addEventListener('touchstart', (e) => { touchX = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) showLb(lbIndex + (dx < 0 ? 1 : -1));
    touchX = null;
  });

  // Interior projects mosaic: one gallery of all tiles
  const mosaicItems = $$('.mosaic-item[data-lightbox-src]');
  const mosaicGallery = mosaicItems.map((el) => ({ src: el.dataset.lightboxSrc, caption: el.dataset.lightboxCaption }));
  mosaicItems.forEach((el, i) => {
    el.addEventListener('click', () => openLb(mosaicGallery, i));
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb(mosaicGallery, i); }
    });
  });

  // Portfolio: each project opens its own photos (cover + extra photos)
  projectCards.forEach((card) => {
    const items = $$('.gallery-src span', card).map((s) => ({ src: s.dataset.src, caption: s.dataset.caption }));
    const open = () => openLb(items, 0);
    const img = $('.project-img img', card);
    if (img && items.length) {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', open);
    }
  });

  /* ------------------------------------------------------------ enquiry form */
  const form = $('#enquiryForm');
  if (!form) return;

  const alertBox = $('#formAlert');
  const submitBtn = $('#enquirySubmit');

  // Strict rules — keep in sync with core/forms.py so messages match the server.
  const NAME_MIN = 3, NAME_MAX = 50, MESSAGE_MIN = 10, MESSAGE_MAX = 1000, EMAIL_MAX = 254;
  const NAME_RE = /^[A-Za-z]+(?:[ .'][A-Za-z]+)*\.?$/;
  const PHONE_INPUT_RE = /^(?:\+91|0)?[6-9]\d{9}$/;
  const EMAIL_RE = /^[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9])?@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,24}$/;
  const LINK_RE = /(https?:\/\/|www\.|<[^>]+>)/i;

  const rules = {
    name(v) {
      v = v.trim().replace(/\s+/g, ' ');
      if (!v) return 'Please enter your name.';
      if (v.length < NAME_MIN) return `Name must be at least ${NAME_MIN} characters.`;
      if (v.length > NAME_MAX) return `Name must be under ${NAME_MAX} characters.`;
      if (!NAME_RE.test(v)) return 'Name can only contain letters and spaces.';
      if ((v.match(/[A-Za-z]/g) || []).length < NAME_MIN) return 'Please enter your full name.';
      return '';
    },
    phone(v) {
      const raw = v.replace(/[\s-]/g, '');
      if (!raw) return 'Please enter your phone number.';
      const digits = raw.slice(-10);
      if (!PHONE_INPUT_RE.test(raw) || new Set(digits).size === 1) return 'Please enter a valid 10-digit mobile number.';
      return '';
    },
    email(v) {
      v = v.trim();
      if (!v) return 'Please enter your email.';
      if (v.length > EMAIL_MAX || v.includes('..') || !EMAIL_RE.test(v)) return 'Please enter a valid email address.';
      return '';
    },
    service(v) {
      return v ? '' : 'Please choose the service you need.';
    },
    message(v) {
      v = v.trim();
      if (!v) return 'Please tell us a little about your space.';
      if (v.length < MESSAGE_MIN) return `Message must be at least ${MESSAGE_MIN} characters.`;
      if (v.length > MESSAGE_MAX) return `Message must be under ${MESSAGE_MAX} characters.`;
      if (v.split(/\s+/).length < 2) return 'Please describe your requirement in a few words.';
      if (LINK_RE.test(v)) return 'Links and HTML are not allowed in the message.';
      return '';
    },
  };

  function setFieldError(name, message) {
    const input = form.elements[name];
    const holder = input && input.closest('.field');
    const errorEl = $(`[data-error-for="${name}"]`, form);
    if (errorEl) errorEl.textContent = message || '';
    if (holder) {
      holder.classList.toggle('has-error', Boolean(message));
      holder.classList.toggle('is-valid', !message && Boolean(input.value.trim()));
    }
    if (input) input.setAttribute('aria-invalid', message ? 'true' : 'false');
  }

  function validateField(input) {
    const rule = rules[input.name];
    if (!rule) return true;
    const message = rule(input.value);
    setFieldError(input.name, message);
    return !message;
  }

  Object.keys(rules).forEach((name) => {
    const input = form.elements[name];
    if (!input) return;
    const errorEl = $(`[data-error-for="${name}"]`, form);
    if (errorEl) {
      errorEl.id = `${name}-error`;
      input.setAttribute('aria-describedby', errorEl.id);
    }
    // validate when leaving a field, then live while correcting it
    input.addEventListener('blur', () => { if (input.value || input.dataset.touched) validateField(input); input.dataset.touched = '1'; });
    input.addEventListener('input', () => { if (input.closest('.field').classList.contains('has-error')) validateField(input); });
    input.addEventListener('change', () => validateField(input));
  });

  // phone: digits only, max 10 (a pasted +91 / 0 prefix is stripped)
  const phoneInput = form.elements.phone;
  if (phoneInput) {
    phoneInput.addEventListener('input', () => {
      let digits = phoneInput.value.replace(/\D/g, '');
      if (digits.length > 10 && digits.startsWith('91')) digits = digits.slice(2);
      if (digits.length > 10 && digits.startsWith('0')) digits = digits.slice(1);
      digits = digits.slice(0, 10);
      if (digits !== phoneInput.value) phoneInput.value = digits;
    });
  }

  // name: block digits and symbols as they are typed
  const nameInput = form.elements.name;
  if (nameInput) {
    nameInput.addEventListener('input', () => {
      const cleaned = nameInput.value.replace(/[^A-Za-z .']/g, '');
      if (cleaned !== nameInput.value) nameInput.value = cleaned;
    });
  }

  // message: live character counter
  const messageInput = form.elements.message;
  const counter = $('#messageCount');
  const updateCount = () => {
    if (!counter || !messageInput) return;
    const n = messageInput.value.trim().length;
    counter.textContent = `${n} / ${MESSAGE_MAX}`;
    counter.classList.toggle('is-over', n > 0 && n < MESSAGE_MIN);
  };
  if (messageInput) messageInput.addEventListener('input', updateCount);
  updateCount();

  function showAlert(type, text) {
    alertBox.className = `form-alert ${type}`;
    alertBox.textContent = text;
    alertBox.hidden = false;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    alertBox.hidden = true;

    const fields = Object.keys(rules).map((n) => form.elements[n]).filter(Boolean);
    const results = fields.map((f) => validateField(f));
    if (results.includes(false)) {
      // bring the first wrong field into view below the fixed header, then focus it
      const firstBad = fields[results.indexOf(false)];
      firstBad.closest('.field').scrollIntoView({ behavior: 'smooth', block: 'center' });
      firstBad.focus({ preventScroll: true });
      showAlert('error', 'Please correct the highlighted fields.');
      return;
    }

    submitBtn.classList.add('is-loading');
    submitBtn.disabled = true;

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin',
      });
      const data = await response.json().catch(() => ({}));

      if (response.ok && data.ok) {
        form.reset();
        updateCount();
        $$('.field', form).forEach((f) => f.classList.remove('is-valid', 'has-error'));
        fields.forEach((f) => { delete f.dataset.touched; });
        showAlert('success', data.message || 'Thank you! We will be in touch soon.');
      } else {
        Object.entries(data.errors || {}).forEach(([name, msgs]) => setFieldError(name, msgs[0]));
        showAlert('error', data.message || 'Something went wrong. Please try again.');
      }
    } catch (err) {
      showAlert('error', 'Could not send your enquiry. Please check your connection or call us directly.');
    } finally {
      submitBtn.classList.remove('is-loading');
      submitBtn.disabled = false;
      // keep the message visible without jumping the page under the fixed header
      const r = alertBox.getBoundingClientRect();
      const headerH = header.offsetHeight;
      if (r.top < headerH + 12 || r.bottom > window.innerHeight) {
        window.scrollTo({ top: window.scrollY + r.top - headerH - 24, behavior: 'smooth' });
      }
    }
  });
})();
