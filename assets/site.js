// 语言切换：默认英文，可切换中文；选择记在浏览器里
(function () {
  function getLang() {
    try { return localStorage.getItem('lang') || 'en'; } catch (e) { return 'en'; }
  }
  function setLang(lang) {
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    try { localStorage.setItem('lang', lang); } catch (e) {}
    var code = document.querySelector('.lang-code');
    if (code) code.textContent = lang === 'en' ? 'EN' : 'ZH';
    var t = document.querySelector('meta[name="title-' + lang + '"]');
    if (t) document.title = t.content;
  }
  setLang(getLang());

  // 主题：默认深色，可切换浅色；选择记在浏览器里
  function getTheme() {
    try { return localStorage.getItem('theme') || 'dark'; } catch (e) { return 'dark'; }
  }
  function setTheme(th) {
    document.documentElement.setAttribute('data-theme', th);
    try { localStorage.setItem('theme', th); } catch (e) {}
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', th === 'dark' ? '#10131c' : '#faf9f5');
  }
  setTheme(getTheme());

  // 形声插画：播放头与线条的真实交点（圆点跟着曲线走），扫过和弦竖线时竖线亮起
  var ssCache = new WeakMap();
  function updateShapeSound(root, phase) {
    if (!root) return;
    var head = root.querySelector('.ss-head');
    if (!head) return;
    var data = ssCache.get(root);
    if (!data) {
      data = { lines: [], chords: root.querySelectorAll('.ss-chord'), hits: root.querySelectorAll('.ss-hit') };
      root.querySelectorAll('.ss-line').forEach(function (p) {
        var len = p.getTotalLength(), pts = [], N = 160;
        for (var i = 0; i <= N; i++) { var q = p.getPointAtLength(len * i / N); pts.push([q.x, q.y]); }
        data.lines.push(pts);
      });
      ssCache.set(root, data);
    }
    var X = phase * 340 - 170, k = 0;
    data.lines.forEach(function (pts) {
      for (var i = 1; i < pts.length && k < data.hits.length; i++) {
        var a = pts[i - 1], b = pts[i];
        if ((a[0] - X) * (b[0] - X) <= 0 && a[0] !== b[0]) {
          var t = (X - a[0]) / (b[0] - a[0]);
          var h = data.hits[k++];
          h.setAttribute('cx', X.toFixed(1));
          h.setAttribute('cy', (a[1] + (b[1] - a[1]) * t).toFixed(1));
          h.style.display = '';
          break;
        }
      }
    });
    for (; k < data.hits.length; k++) data.hits[k].style.display = 'none';
    data.chords.forEach(function (c) {
      var on = Math.abs(X - parseFloat(c.getAttribute('data-x'))) < 7;
      c.style.strokeWidth = on ? '10' : '';
      c.style.stroke = on ? '#a6cf5a' : '';
    });
  }

  // 首页精选：一次展示一个项目
  // 插画里的零件跟着进度 --phase（0→1）动：滚轮往下滚，进度往前走，走完一段就切到下一个项目；往上滚倒放。
  // 没人操作时自动慢慢播放；也可以点列表、手机左右滑、方向键切换。手机上切换时轻微震动（仅安卓浏览器支持）。
  function initFeature() {
    var box = document.getElementById('feature');
    if (!box) return;
    var stage = box.querySelector('.fstage');
    var slides = box.querySelectorAll('.fslide');
    var tabs = box.querySelectorAll('.ftab');
    var cur = box.querySelector('.fcur');
    var n = slides.length, active = 0, phase = 0, target = 0, lastUser = 0, lockUntil = 0, hovering = false;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var AUTO_MS = 7000, IDLE_MS = 4000, PER_PROJECT = 650; // 滚多少像素走完一个项目

    function now() { return performance.now(); }
    function buzz() { try { if (navigator.vibrate) navigator.vibrate(12); } catch (e) {} }

    function switchTo(i, dir, start) {
      i = (i + n) % n;
      if (i === active) return;
      var prev = slides[active];
      stage.classList.remove('dir-up', 'dir-down');
      stage.classList.add(dir > 0 ? 'dir-down' : 'dir-up');
      prev.classList.add('leaving');
      setTimeout(function () { prev.classList.remove('leaving'); }, 460);
      active = i; phase = target = start;
      for (var k = 0; k < n; k++) {
        var on = k === active;
        slides[k].classList.toggle('is-active', on);
        slides[k].setAttribute('aria-hidden', on ? 'false' : 'true');
        tabs[k].classList.toggle('is-active', on);
        tabs[k].setAttribute('aria-selected', on ? 'true' : 'false');
      }
      if (cur) cur.textContent = (active + 1 < 10 ? '0' : '') + (active + 1);
      lockUntil = now() + 450;
    }

    function userTouched() { lastUser = now(); box.classList.add('used'); }

    function nudge(delta) {          // delta：以"一个项目"为单位的进度变化；返回是否消费了这次滚动
      if (delta > 0 && active === n - 1 && target >= 1) return false;
      if (delta < 0 && active === 0 && target <= 0) return false;
      userTouched();
      if (now() < lockUntil) return true;                 // 刚切换完，吞掉惯性滚动
      target += delta;
      if (target > 1) {
        if (active < n - 1) switchTo(active + 1, 1, 0); else target = 1;
      } else if (target < 0) {
        if (active > 0) switchTo(active - 1, -1, 1); else target = 0;
      }
      return true;
    }

    stage.addEventListener('wheel', function (e) {
      var d = Math.abs(e.deltaY) >= Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
      if (e.deltaMode === 1) d *= 33; else if (e.deltaMode === 2) d *= 400;
      if (nudge(d / PER_PROJECT)) e.preventDefault();
    }, { passive: false });

    function jump(dir) {
      var next = active + dir;
      if (next < 0 || next >= n) return false;
      userTouched(); switchTo(next, dir, 0); return true;
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { userTouched(); switchTo(k, k > active ? 1 : -1, 0); });
    });

    var sx = 0, sy = 0, st = 0;
    stage.addEventListener('touchstart', function (e) { var t = e.touches[0]; sx = t.clientX; sy = t.clientY; st = Date.now(); }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
      if (Date.now() - st > 600) return;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.2) { if (jump(dx < 0 ? 1 : -1)) buzz(); }
    }, { passive: true });

    function onKey(e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { if (jump(1)) e.preventDefault(); }
      else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { if (jump(-1)) e.preventDefault(); }
    }
    stage.addEventListener('keydown', onKey);
    box.querySelector('.ftabs').addEventListener('keydown', onKey);

    box.addEventListener('mouseenter', function () { hovering = true; });
    box.addEventListener('mouseleave', function () { hovering = false; });

    var last = now();
    function frame(t) {
      var dt = Math.min(64, t - last); last = t;
      if (!reduce && !hovering && !document.hidden && t - lastUser > IDLE_MS) {
        target += dt / AUTO_MS;
        if (target >= 1) switchTo(active + 1, 1, 0);
      }
      phase += (target - phase) * Math.min(1, dt / 110);
      if (Math.abs(target - phase) < 0.0005) phase = target;
      slides[active].style.setProperty('--phase', phase.toFixed(4));
      updateShapeSound(slides[active].querySelector('.art'), phase);
      for (var k = 0; k < n; k++) {
        var f = tabs[k].querySelector('.fill');
        if (f) f.style.width = (k === active ? phase * 100 : 0).toFixed(1) + '%';
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  // 项目页大图、项目目录卡片：插画零件跟着页面滚动位置动
  function initScrollArt() {
    var els = document.querySelectorAll('.dh-art, .pcard-art');
    if (!els.length) return;
    var ticking = false;
    function update() {
      ticking = false;
      var vh = window.innerHeight;
      els.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var p = (vh - r.top) / (vh + r.height);
        if (el.classList.contains('dh-art')) p = Math.min(1, window.scrollY / Math.max(1, r.height + 160)); // 顶部大图：从页面顶端开始算
        p = Math.min(1, Math.max(0, p));
        el.style.setProperty('--phase', p.toFixed(4));
        updateShapeSound(el.querySelector('.art'), p);
      });
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    setLang(getLang());
    var btn = document.querySelector('.lang-btn');
    if (btn) btn.addEventListener('click', function () {
      setLang(document.documentElement.getAttribute('data-lang') === 'en' ? 'zh' : 'en');
    });
    setTheme(getTheme());
    var tb = document.querySelector('.theme-btn');
    if (tb) tb.addEventListener('click', function () {
      setTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
    initFeature();
    initScrollArt();
    // 返回按钮：从本站页面进来就退回上一页，否则去链接指定的页面
    document.querySelectorAll('[data-back]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        var ref = document.referrer;
        if (ref && ref.indexOf(location.origin) === 0 && ref !== location.href && history.length > 1) { e.preventDefault(); history.back(); }
      });
    });
  });
})();
