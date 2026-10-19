/* =========================================================
   WICCOM · main.js  (vanilla JS, sin dependencias salvo AOS)
   ========================================================= */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const CFG = window.WICCOM || {};
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Modo demo: en tu computadora o en la vista previa de Vercel los formularios simulan el envío.
  const DEMO_FILE = location.protocol === 'file:';
  const DEMO = DEMO_FILE || ['localhost', '127.0.0.1'].includes(location.hostname) || location.hostname.endsWith('vercel.app');

  /* ---------- Placeholders: marca imágenes cargadas / faltantes ---------- */
  const handleImg = img => {
    const ph = img.closest('.ph');
    const done = () => { if (img.naturalWidth > 0) { ph && ph.classList.add('is-loaded'); } else { img.remove(); } };
    if (img.complete) done(); else { img.addEventListener('load', done, { once: true }); img.addEventListener('error', () => img.remove(), { once: true }); }
  };
  $$('.ph > img').forEach(handleImg);

  /* ---------- AOS ---------- */
  if (window.AOS) {
    // En pantallas chicas, las entradas laterales salen de la pantalla y generan scroll horizontal:
    // se cambian por entradas desde abajo.
    if (matchMedia('(max-width: 860px)').matches) {
      $$('[data-aos^="fade-left"],[data-aos^="fade-right"],[data-aos^="slide-"],[data-aos^="zoom-in-left"],[data-aos^="zoom-in-right"]').forEach(el => el.setAttribute('data-aos', 'fade-up'));
    }
    AOS.init({ duration: 750, easing: 'ease-out-cubic', once: true, offset: 60, disable: reduceMotion });
    // Recalcula posiciones cuando la página cambia de alto (imágenes cargadas, filtros, etc.)
    addEventListener('load', () => AOS.refresh());
  }
  const refreshAOS = () => { if (window.AOS) requestAnimationFrame(() => AOS.refresh()); };

  /* ---------- Header ---------- */
  const header = $('.site-header');
  const toTop = $('.to-top');
  const progress = $('.progress');
  const onScroll = () => {
    const y = scrollY;
    header?.classList.toggle('is-scrolled', y > 10);
    toTop?.classList.toggle('is-visible', y > 600);
    if (progress) {
      const art = $('.prose');
      if (art) {
        const r = art.getBoundingClientRect();
        const pct = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight + 200)));
        progress.style.width = (pct * 100) + '%';
      }
    }
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  toTop?.addEventListener('click', () => scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));

  /* ---------- Menú móvil ---------- */
  const mnav = $('#mnav');
  let lastFocus;
  const openNav = () => { lastFocus = document.activeElement; mnav.classList.add('is-open'); mnav.removeAttribute('aria-hidden'); $('.burger')?.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; setTimeout(() => $('.mnav__panel', mnav)?.focus({ preventScroll: true }), 50); };
  const closeNav = () => { mnav.classList.remove('is-open'); mnav.setAttribute('aria-hidden', 'true'); $('.burger')?.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; lastFocus?.focus(); };
  $('.burger')?.addEventListener('click', openNav);
  $$('[data-close-nav]').forEach(b => b.addEventListener('click', closeNav));
  addEventListener('keydown', e => { if (e.key === 'Escape' && mnav?.classList.contains('is-open')) closeNav(); });

  /* ---------- Buscador global ---------- */
  const search = $('#search');
  const sInput = $('#search-input');
  const sResults = $('#search-results');
  const norm = s => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const renderSearch = q => {
    const idx = window.SEARCH_INDEX || [];
    const n = norm(q.trim());
    const list = n ? idx.filter(i => norm(i.t + ' ' + i.d + ' ' + (i.k || '')).includes(n)).slice(0, 8) : idx.slice(0, 6);
    sResults.innerHTML = list.length
      ? list.map(i => `<a href="${CFG.root}${i.u}"><strong>${i.t}</strong><span>${i.d}</span></a>`).join('')
      : `<p class="search__empty">No encontramos “${q}”. Prueba con “cámaras”, “UPS” o “cableado”, o <a class="hl-blue" href="${CFG.root}contacto.html">escríbenos</a>.</p>`;
  };
  const openSearch = () => { search.classList.add('is-open'); search.removeAttribute('aria-hidden'); renderSearch(''); setTimeout(() => sInput.focus(), 60); };
  const closeSearch = () => { search.classList.remove('is-open'); search.setAttribute('aria-hidden', 'true'); };
  $$('[data-open-search]').forEach(b => b.addEventListener('click', () => { if (mnav?.classList.contains('is-open')) closeNav(); openSearch(); }));
  search?.addEventListener('click', e => { if (e.target === search) closeSearch(); });
  $('[data-close-search]')?.addEventListener('click', closeSearch);
  sInput?.addEventListener('input', () => renderSearch(sInput.value));
  addEventListener('keydown', e => {
    if (e.key === 'Escape' && search?.classList.contains('is-open')) closeSearch();
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
  });

  /* ---------- Carruseles ---------- */
  $$('[data-carousel]').forEach(car => {
    const track = $('.carousel__track', car);
    const slides = [...track.children];
    const prev = $('[data-prev]', car), next = $('[data-next]', car);
    const dotsWrap = $('.carousel__dots', car);
    const autoplay = +car.dataset.autoplay || 2000;
    let timer, pages = 1;

    const step = () => slides[0].getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 0);
    const perView = () => Math.max(1, Math.round(track.clientWidth / step()));
    const maxScroll = () => track.scrollWidth - track.clientWidth;

    const build = () => {
      const visible = slides.filter(s => s.offsetParent !== null || getComputedStyle(s).display !== 'none');
      pages = Math.max(1, Math.ceil((visible.length - perView()) / perView()) + 1);
      car.classList.toggle('is-static', maxScroll() <= 4);
      dotsWrap.innerHTML = '';
      if (pages > 1) for (let i = 0; i < pages; i++) {
        const d = document.createElement('button');
        d.className = 'carousel__dot'; d.type = 'button';
        d.setAttribute('aria-label', `Ir al grupo ${i + 1} de ${pages}`);
        d.addEventListener('click', () => go(i * perView()));
        dotsWrap.appendChild(d);
      }
      update();
    };
    const go = i => track.scrollTo({ left: Math.min(maxScroll(), i * step()), behavior: reduceMotion ? 'auto' : 'smooth' });
    const current = () => Math.round(track.scrollLeft / step());
    const update = () => {
      const m = maxScroll();
      if (prev) prev.disabled = track.scrollLeft <= 4;
      if (next) next.disabled = track.scrollLeft >= m - 4;
      const page = track.scrollLeft >= m - 4 ? pages - 1 : Math.round(current() / perView());
      $$('.carousel__dot', dotsWrap).forEach((d, i) => d.setAttribute('aria-current', i === page ? 'true' : 'false'));
    };
    prev?.addEventListener('click', () => go(Math.max(0, current() - perView())));
    next?.addEventListener('click', () => go(current() + perView()));
    let raf; track.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(update); }, { passive: true });
    addEventListener('resize', () => { clearTimeout(car._rt); car._rt = setTimeout(build, 150); });

    // Arrastre con mouse
    let down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = track.scrollLeft; });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 5) { moved = true; track.classList.add('is-dragging'); } track.scrollLeft = sl - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; track.classList.remove('is-dragging'); if (moved) go(current()); });
    track.addEventListener('click', e => { if (moved) { e.preventDefault(); moved = false; } }, true);

    // Autoplay
    const play = () => { if (!autoplay || reduceMotion) return; stop(); timer = setInterval(() => { track.scrollLeft >= maxScroll() - 4 ? go(0) : go(current() + perView()); }, autoplay); };
    const stop = () => clearInterval(timer);
    ['mouseenter', 'focusin', 'touchstart'].forEach(ev => car.addEventListener(ev, stop, { passive: true }));
    ['mouseleave', 'focusout'].forEach(ev => car.addEventListener(ev, play));
    new IntersectionObserver(([en]) => en.isIntersecting ? play() : stop()).observe(car);
    car._rebuild = build;
    build();
  });

  /* ---------- Contadores ---------- */
  const counters = $$('[data-count]');
  if (counters.length) {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (!en.isIntersecting) return;
      const el = en.target, end = +el.dataset.count, pre = el.dataset.prefix || '', suf = el.dataset.suffix || '';
      io.unobserve(el);
      if (reduceMotion) { el.textContent = pre + end + suf; return; }
      const t0 = performance.now(), dur = 1600;
      const tick = t => { const p = Math.min(1, (t - t0) / dur); el.textContent = pre + Math.round(end * (1 - Math.pow(1 - p, 3))) + suf; if (p < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    }), { threshold: .6 });
    counters.forEach(c => io.observe(c));
  }

  /* ---------- Filtros (marcas / recursos) ---------- */
  $$('[data-filter-group]').forEach(group => {
    const items = $$('[data-cat]', group.querySelector('[data-filter-items]'));
    const chips = $$('[data-filter]', group);
    const select = $('[data-filter-select]', group);
    const input = $('[data-filter-search]', group);
    const empty = $('.empty-state', group);
    let cat = 'all', q = '';

    const apply = () => {
      const nq = norm(q.trim());
      const matches = items.filter(it => (cat === 'all' || it.dataset.cat.split(' ').includes(cat)) && (!nq || norm(it.dataset.name || it.textContent).includes(nq)));
      items.forEach(it => it.classList.add('is-hidden'));
      matches.forEach((it, i) => { it.classList.remove('is-hidden'); if (!reduceMotion) it.animate([{ opacity: 0, transform: 'translateY(12px)' }, { opacity: 1, transform: 'none' }], { duration: 400, delay: Math.min(i, 12) * 30, easing: 'ease-out', fill: 'backwards' }); });
      empty?.classList.toggle('is-visible', matches.length === 0);
      chips.forEach(c => c.setAttribute('aria-pressed', c.dataset.filter === cat ? 'true' : 'false'));
      if (select) select.value = cat;
      refreshAOS();
    };
    const setCat = c => { cat = c; apply(); };
    chips.forEach(c => c.addEventListener('click', () => setCat(c.dataset.filter)));
    select?.addEventListener('change', () => setCat(select.value));
    input?.addEventListener('input', () => { q = input.value; apply(); });
    $$('[data-set-filter]').forEach(a => a.addEventListener('click', () => setCat(a.dataset.setFilter)));
    const hashCat = new URLSearchParams(location.search).get('categoria');
    if (hashCat) cat = hashCat;
    apply();
  });

  /* ---------- Modales ---------- */
  const waLink = msg => `https://wa.me/${CFG.whatsapp}?text=${encodeURIComponent(msg)}`;
  $$('[data-modal]').forEach(btn => btn.addEventListener('click', e => {
    const dlg = $('#modal-' + btn.dataset.modal);
    if (!dlg) return;
    e.preventDefault();
    const ctx = btn.dataset.context || '';
    dlg.dataset.context = ctx;
    $$('.modal__view', dlg).forEach((v, i) => v.hidden = i !== 0);
    $$('.modal__form', dlg).forEach(f => f.classList.remove('is-sent'));
    const wa = $('[data-wa-link]', dlg);
    if (wa) wa.href = waLink(`¡Hola! ${ctx ? `Me interesa ${ctx} y` : 'Me'} me gustaría hablar con un asesor de Wiccom.`);
    $$('[data-prefill]', dlg).forEach(f => { if (ctx) f.value = ctx; });
    const ctxInput = $('input[name="contexto"]', dlg); if (ctxInput) ctxInput.value = ctx || document.title;
    dlg.showModal();
  }));
  $$('dialog.modal').forEach(dlg => {
    dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
    $$('[data-close-modal]', dlg).forEach(b => b.addEventListener('click', () => dlg.close()));
    $$('[data-view]', dlg).forEach(b => b.addEventListener('click', () => {
      $$('.modal__view', dlg).forEach(v => v.hidden = v.dataset.name !== b.dataset.view);
      $(`.modal__view[data-name="${b.dataset.view}"] input, .modal__view[data-name="${b.dataset.view}"] a`, dlg)?.focus();
    }));
  });

  /* ---------- Formularios ---------- */
  const toast = (msg, ms = 4200, type = 'ok') => {
    const t = $('#toast'); if (!t) return;
    ($('.toast__msg', t) || $('span', t)).textContent = msg;
    t.classList.toggle('is-error', type === 'error');
    t.classList.add('is-visible');
    clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('is-visible'), ms);
  };

  $$('form[data-validate]').forEach(form => {
    const started = Date.now();
    const ts = $('input[name="_ts"]', form); if (ts) ts.value = started;

    // Prefill desde URL (?interes=Mantenimiento)
    const params = new URLSearchParams(location.search);
    const pre = params.get('interes');
    const sel = $('select[data-from-url]', form);
    if (pre && sel) {
      const opt = [...sel.options].find(o => norm(o.value) === norm(pre) || norm(o.textContent) === norm(pre));
      if (opt) sel.value = opt.value; else { sel.add(new Option(pre, pre, true, true)); }
    }

    // Contadores de caracteres
    $$('textarea[maxlength]', form).forEach(ta => {
      const out = $(`[data-count-for="${ta.name}"]`, form);
      const upd = () => out && (out.textContent = `${ta.value.length}/${ta.maxLength}`);
      ta.addEventListener('input', upd); upd();
    });

    const setErr = (field, msg) => {
      const wrap = field.closest('.field') || field.closest('.check');
      wrap?.classList.toggle('is-invalid', !!msg);
      const err = wrap?.querySelector('.field__error');
      if (err) err.textContent = msg || '';
      field.setAttribute('aria-invalid', msg ? 'true' : 'false');
    };
    const check = f => {
      const v = f.type === 'checkbox' ? f.checked : f.value.trim();
      if (f.required && !v) return setErr(f, f.type === 'checkbox' ? 'Necesitamos tu autorización para continuar.' : 'Este campo es obligatorio.'), false;
      if (f.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return setErr(f, 'Escribe un correo válido, por ejemplo nombre@empresa.com.'), false;
      if (f.type === 'tel' && v && v.replace(/\D/g, '').length < 10) return setErr(f, 'Escribe un teléfono de 10 dígitos.'), false;
      setErr(f, ''); return true;
    };
    $$('input, select, textarea', form).forEach(f => {
      f.addEventListener('blur', () => f.closest('.is-invalid') && check(f));
      f.addEventListener('input', () => f.closest('.is-invalid') && check(f));
    });

    form.addEventListener('submit', async e => {
      e.preventDefault();
      const fields = $$('input:not([type=hidden]):not(.hp input), select, textarea', form).filter(f => !f.closest('.hp'));
      const bad = fields.filter(f => !check(f));
      if (bad.length) { bad[0].focus(); toast('Revisa los campos marcados.', 4200, 'error'); return; }
      // CAPTCHA (Cloudflare Turnstile)
      const cap = $('.captcha', form);
      const token = $('[name="cf-turnstile-response"]', form)?.value;
      if (cap && !DEMO_FILE && !token) {
        cap.classList.add('is-invalid');
        $('.field__error', cap).textContent = window.turnstile ? 'Completa la verificación de seguridad.' : 'No se pudo cargar la verificación de seguridad. Recarga la página.';
        toast('Completa la verificación de seguridad.', 4200, 'error'); return;
      }
      cap?.classList.remove('is-invalid');
      if ($('.hp input', form)?.value) return; // bot
      const btn = $('[type=submit]', form);
      btn.classList.add('is-loading');
      const data = new FormData(form);
      data.set('_ts', String(Date.now() - started)); // milisegundos en la página (no depende del reloj de la computadora)
      const wrap = form.parentElement;
      try {
        if (DEMO) await new Promise(r => setTimeout(r, 900)); // modo demo (local o vista previa): no envía
        else {
          const res = await fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
          const json = await res.json().catch(() => ({}));
          if (!res.ok || json.ok === false) throw new Error(json.message || 'Error');
        }
        wrap.classList.add('is-sent');
        form.reset();
        wrap.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
      } catch (err) {
        toast(err.message && err.message !== 'Error' ? err.message : 'No pudimos enviar tu solicitud. Intenta de nuevo o escríbenos por WhatsApp.', 6000, 'error');
      } finally {
        btn.classList.remove('is-loading');
        const w = $('.cf-turnstile', form); if (w && window.turnstile) try { window.turnstile.reset(w); } catch (_) {}
      }
    });
  });
  $$('[data-reset-form]').forEach(b => b.addEventListener('click', () => b.closest('.is-sent')?.classList.remove('is-sent')));

  /* ---------- Compartir / copiar enlace ---------- */
  $$('[data-copy-link]').forEach(b => b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(location.href); toast('Enlace copiado al portapapeles.'); } catch { toast(location.href); }
  }));
  $$('[data-share]').forEach(a => {
    const u = encodeURIComponent(location.href), t = encodeURIComponent(document.title);
    const map = { linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${u}`, facebook: `https://www.facebook.com/sharer/sharer.php?u=${u}`, whatsapp: `https://wa.me/?text=${t}%20${u}` };
    a.href = map[a.dataset.share];
  });

  /* ---------- Índice activo del artículo ---------- */
  const tocLinks = $$('.toc a');
  if (tocLinks.length) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) tocLinks.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id));
    }), { rootMargin: '-30% 0px -60% 0px' });
    tocLinks.forEach(a => { const s = $(a.getAttribute('href')); s && io.observe(s); });
  }

  /* ---------- Año del footer ---------- */
  $$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
