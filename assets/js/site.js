/* Painting With Purpose, demo 2: site behaviour (no dependencies) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- header ---------- */
  const hdr = $('.hdr');
  let lastY = scrollY;
  const onScroll = () => {
    const y = scrollY;
    if (hdr) {
      hdr.classList.toggle('is-solid', y > 40);
      hdr.classList.toggle('is-hidden', y > 400 && y > lastY && !document.body.classList.contains('menu-open'));
    }
    lastY = y;
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const menuBtn = $('.menu-btn');
  if (menuBtn) {
    const mnav = $('.mnav');
    const setMenu = (open) => {
      document.body.classList.toggle('menu-open', open);
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      mnav.toggleAttribute('inert', !open);
    };
    setMenu(false);
    menuBtn.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
    addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
    $$('a', mnav).forEach((a) => a.addEventListener('click', () => setMenu(false)));
  }

  /* ---------- reveal on scroll ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  $$('.rv, .lines, .goal').forEach((el) => io.observe(el));

  /* ---------- counters ---------- */
  const fmt = new Intl.NumberFormat('en-US');
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const el = e.target;
      countIO.unobserve(el);
      const end = +el.dataset.count;
      const pre = el.dataset.pre || '';
      const suf = el.dataset.suf || '';
      if (reduce) { el.textContent = pre + fmt.format(end) + suf; return; }
      const t0 = performance.now();
      const dur = 1800;
      const tick = (t) => {
        const p = Math.min(1, (t - t0) / dur);
        const v = Math.round(end * (1 - Math.pow(1 - p, 4)));
        el.textContent = pre + fmt.format(v) + suf;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }, { threshold: 0.6 });
  $$('[data-count]').forEach((el) => countIO.observe(el));

  /* ---------- hero: watercolor drifts slower than the page, photo card floats ---------- */
  const heroArt = $('.hero__art');
  const pol = $('.polaroid');
  if (heroArt && !reduce) {
    let ticking = false;
    const update = () => {
      ticking = false;
      const y = Math.min(scrollY, innerHeight * 1.2);
      heroArt.style.setProperty('--hy', (y * 0.28).toFixed(1));
      if (pol) pol.style.setProperty('--py', (-y * 0.12).toFixed(1));
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  /* ---------- art slots: load generated art if the file exists ---------- */
  $$('[data-art]').forEach((slot) => {
    const id = slot.dataset.art;
    const exts = ['jpg', 'png', 'webp'];
    const tryNext = (i) => {
      if (i >= exts.length) return;
      const img = new Image();
      img.alt = slot.dataset.alt || '';
      img.decoding = 'async';
      img.onload = () => { slot.appendChild(img); requestAnimationFrame(() => slot.classList.add('has-img')); };
      img.onerror = () => tryNext(i + 1);
      img.src = `assets/art/${id}.${exts[i]}`;
    };
    tryNext(0);
  });

  /* ---------- services: sticky media follows the active item ---------- */
  const svcItems = $$('.svc__item');
  const svcMedia = $$('.svc__media > *');
  if (svcItems.length && svcMedia.length) {
    const setActive = (i) => {
      svcItems.forEach((el, j) => el.classList.toggle('on', i === j));
      svcMedia.forEach((el, j) => el.classList.toggle('on', i === j));
    };
    setActive(0);
    const sio = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) setActive(svcItems.indexOf(e.target)); });
    }, { rootMargin: '-45% 0px -45% 0px' });
    svcItems.forEach((el) => sio.observe(el));
  }

  /* ---------- before / after ---------- */
  function initCompare(ba) {
    const range = $('input[type=range]', ba);
    const set = (v) => { ba.style.setProperty('--pos', v + '%'); range.value = v; };
    range.addEventListener('input', () => set(range.value));
    let dragging = false;
    const fromEvent = (e) => {
      const r = ba.getBoundingClientRect();
      return Math.max(0, Math.min(100, ((e.clientX - r.left) / r.width) * 100));
    };
    ba.addEventListener('pointerdown', (e) => { dragging = true; ba.setPointerCapture(e.pointerId); set(fromEvent(e)); ba.classList.remove('ba--hint'); });
    ba.addEventListener('pointermove', (e) => { if (dragging) set(fromEvent(e)); });
    ba.addEventListener('pointerup', () => { dragging = false; });
    ba.addEventListener('pointercancel', () => { dragging = false; });
    ba._set = set;
    return set;
  }

  // a gentle sweep the first time a slider scrolls into view, so people know it moves
  function sweep(ba) {
    if (reduce || !ba._set) return;
    const seq = [[50, 22, 650], [22, 78, 900], [78, 50, 650]];
    let k = 0;
    const run = () => {
      if (k >= seq.length) return;
      const [a, b, d] = seq[k++];
      const t0 = performance.now();
      const step = (t) => {
        const p = Math.min(1, (t - t0) / d);
        const e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
        ba._set(a + (b - a) * e);
        if (p < 1) requestAnimationFrame(step); else run();
      };
      requestAnimationFrame(step);
    };
    run();
  }

  const baRoot = $('[data-ba-root]');
  const BA = window.PWP_BEFORE_AFTER || [];
  if (baRoot && BA.length) {
    const limit = +baRoot.dataset.limit || BA.length;
    const list = BA.slice(0, limit);
    const ba = $('.ba', baRoot);
    const imgB = $('.ba__before', ba);
    const imgA = $('.ba__after', ba);
    const title = $('[data-ba-title]', baRoot);
    const desc = $('[data-ba-desc]', baRoot);
    const where = $('[data-ba-where]', baRoot);
    const what = $('[data-ba-what]', baRoot);
    const count = $('[data-ba-count]', baRoot);
    const thumbs = $('.ba-thumbs', baRoot);
    const set = initCompare(ba);
    let cur = 0;

    list.forEach((p, i) => {
      const b = document.createElement('button');
      b.className = 'ba-thumb';
      b.type = 'button';
      b.setAttribute('aria-label', `Show ${p.title}`);
      b.innerHTML = `<img src="${p.after}" alt="" loading="lazy" width="300" height="300"><img class="t-before" src="${p.before}" alt="" loading="lazy" width="300" height="300"><span>${p.short || p.title}</span>`;
      b.addEventListener('click', () => show(i, true));
      thumbs.appendChild(b);
    });

    function show(i, fromUser) {
      cur = (i + list.length) % list.length;
      const p = list[cur];
      ba.animate?.([{ opacity: .35 }, { opacity: 1 }], { duration: 500, easing: 'ease-out' });
      imgB.src = p.before; imgB.alt = `Before: ${p.title}`;
      imgA.src = p.after; imgA.alt = `After: ${p.title}`;
      title.textContent = p.title;
      desc.textContent = p.desc;
      where.textContent = p.where;
      what.textContent = p.what;
      count.innerHTML = `<b>${String(cur + 1).padStart(2, '0')}</b> / ${String(list.length).padStart(2, '0')}`;
      $$('.ba-thumb', thumbs).forEach((t, j) => t.setAttribute('aria-current', String(j === cur)));
      ba.style.aspectRatio = String(Math.min(1.45, Math.max(0.8, p.ratio || 4 / 3)));
      set(50);
      if (fromUser) sweep(ba);
    }
    $('[data-ba-prev]', baRoot)?.addEventListener('click', () => show(cur - 1, true));
    $('[data-ba-next]', baRoot)?.addEventListener('click', () => show(cur + 1, true));
    show(0, false);
    const hio = new IntersectionObserver((es) => {
      es.forEach((e) => { if (e.isIntersecting) { hio.disconnect(); setTimeout(() => sweep(ba), 300); } });
    }, { threshold: 0.6 });
    hio.observe(ba);
  }
  // stand-alone sliders (pages may also include static ones)
  $$('.ba[data-static]').forEach((el) => initCompare(el));

  /* ---------- horizontal work rail ---------- */
  $$('[data-rail]').forEach((wrap) => {
    const rail = $('.rail', wrap);
    const bar = $('.rail-prog i', wrap);
    const upd = () => {
      const max = rail.scrollWidth - rail.clientWidth;
      const ratio = rail.clientWidth / rail.scrollWidth;
      if (bar) {
        bar.style.width = (ratio * 100) + '%';
        bar.style.transform = `translateX(${max > 0 ? (rail.scrollLeft / max) * ((1 / ratio) - 1) * 100 : 0}%)`;
      }
    };
    rail.addEventListener('scroll', upd, { passive: true });
    addEventListener('resize', upd);
    upd();
    const step = () => Math.min(rail.clientWidth * 0.8, 600);
    $('[data-rail-prev]', wrap)?.addEventListener('click', () => rail.scrollBy({ left: -step(), behavior: reduce ? 'auto' : 'smooth' }));
    $('[data-rail-next]', wrap)?.addEventListener('click', () => rail.scrollBy({ left: step(), behavior: reduce ? 'auto' : 'smooth' }));

    if (fine) {
      let down = false, sx = 0, sl = 0, moved = 0;
      rail.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') return; down = true; moved = 0; sx = e.clientX; sl = rail.scrollLeft; });
      addEventListener('pointermove', (e) => {
        if (!down) return;
        const dx = e.clientX - sx;
        moved = Math.max(moved, Math.abs(dx));
        if (moved > 4) rail.classList.add('drag');
        rail.scrollLeft = sl - dx;
      });
      addEventListener('pointerup', () => { if (!down) return; down = false; setTimeout(() => rail.classList.remove('drag'), 0); });
      rail.addEventListener('dragstart', (e) => e.preventDefault());
    }
  });

  /* ---------- cursor bubble on hoverable media ---------- */
  if (fine && !reduce) {
    const c = document.createElement('div');
    c.className = 'cursor';
    c.setAttribute('aria-hidden', 'true');
    document.body.appendChild(c);
    addEventListener('pointermove', (e) => {
      c.style.setProperty('--x', e.clientX + 'px');
      c.style.setProperty('--y', e.clientY + 'px');
    }, { passive: true });
    $$('[data-cursor]').forEach((el) => {
      el.addEventListener('pointerenter', () => { c.textContent = el.dataset.cursor; c.style.setProperty('--s', 1); });
      el.addEventListener('pointerleave', () => c.style.setProperty('--s', 0));
    });
  }

  /* ---------- kind words ---------- */
  $$('[data-quotes]').forEach((root) => {
    const qs = $$('.quote', root);
    const count = $('.kw__count', root);
    const dots = $('.kw__dots', root);
    let i = 0;
    qs.forEach((_, j) => {
      const d = document.createElement('button');
      d.type = 'button';
      d.setAttribute('aria-label', `Review ${j + 1} of ${qs.length}`);
      d.addEventListener('click', () => go(j));
      dots.appendChild(d);
    });
    function go(n) {
      i = (n + qs.length) % qs.length;
      qs.forEach((q, j) => { q.classList.toggle('on', j === i); q.setAttribute('aria-hidden', String(j !== i)); });
      $$('button', dots).forEach((d, j) => d.setAttribute('aria-current', String(j === i)));
      count.textContent = `${String(i + 1).padStart(2, '0')} / ${String(qs.length).padStart(2, '0')}`;
    }
    $('[data-q-prev]', root).addEventListener('click', () => go(i - 1));
    $('[data-q-next]', root).addEventListener('click', () => go(i + 1));
    go(0);
  });

  /* ---------- work grid: filters + lightbox ---------- */
  const grid = $('[data-grid]');
  if (grid) {
    const items = $$('.gitem', grid);
    const chips = $$('[data-filter]');
    const moreBtn = $('[data-more]');
    let expanded = false;
    let current = 'all';
    moreBtn?.addEventListener('click', () => { expanded = true; apply(current); });
    const apply = (f) => {
      chips.forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.filter === f)));
      let shown = 0;
      items.forEach((it) => {
        const match = f === 'all' || it.dataset.cat.split(' ').includes(f);
        const over = match && !expanded && ++shown > 12;
        it.classList.toggle('hide', !match || over);
      });
      if (moreBtn) moreBtn.hidden = expanded || shown <= 12;
      current = f;
      const u = new URL(location.href);
      if (f === 'all') u.searchParams.delete('type'); else u.searchParams.set('type', f);
      history.replaceState(null, '', u);
    };
    chips.forEach((c) => {
      const n = c.dataset.filter === 'all' ? items.length : items.filter((it) => it.dataset.cat.split(' ').includes(c.dataset.filter)).length;
      c.insertAdjacentHTML('beforeend', `<sup>${n}</sup>`);
      c.addEventListener('click', () => apply(c.dataset.filter));
    });
    apply(new URL(location.href).searchParams.get('type') || 'all');

    const lb = $('.lb');
    const lbImg = $('img', lb);
    const lbCap = $('.lb__cap', lb);
    let li = 0;
    let lastFocus = null;
    const visible = () => items.filter((it) => !it.classList.contains('hide'));
    const open = (it) => {
      const vis = visible();
      li = vis.indexOf(it);
      lastFocus = document.activeElement;
      render();
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
      $('.lb__x', lb).focus();
    };
    const render = () => {
      const it = visible()[li];
      lbImg.src = it.dataset.full;
      lbImg.alt = $('img', it).alt;
      lbCap.textContent = it.dataset.caption;
    };
    const close = () => { lb.classList.remove('open'); document.body.style.overflow = ''; lastFocus?.focus(); };
    const move = (d) => { const v = visible(); li = (li + d + v.length) % v.length; render(); };
    items.forEach((it) => it.addEventListener('click', () => open(it)));
    $('.lb__x', lb).addEventListener('click', close);
    $('.lb__p', lb).addEventListener('click', () => move(-1));
    $('.lb__n', lb).addEventListener('click', () => move(1));
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    addEventListener('keydown', (e) => {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') move(-1);
      if (e.key === 'ArrowRight') move(1);
    });
  }

  /* ---------- forms (demo: no backend yet) ---------- */
  $$('[data-demo-form]').forEach((wrap) => {
    const form = $('form', wrap);
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const bad = $$('[required]', form).find((f) => !f.value.trim());
      if (bad) { bad.focus(); bad.reportValidity(); return; }
      const btn = $('button[type=submit]', form);
      btn.textContent = 'Sending…';
      setTimeout(() => {
        wrap.classList.add('sent');
        wrap.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      }, 700);
    });
  });

  /* ---------- footer year ---------- */
  $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
