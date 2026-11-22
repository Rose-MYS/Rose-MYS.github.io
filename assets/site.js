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

  // 首页精选：一次展示一个项目
  // 切换方式：自动轮播 / 点列表 / 在大图上滚动滚轮 / 手机滑动 / 方向键；手机上切换时轻微震动（仅安卓浏览器支持）
  function initFeature() {
    var box = document.getElementById('feature');
    if (!box) return;
    var stage = box.querySelector('.fstage');
    var slides = box.querySelectorAll('.fslide');
    var tabs = box.querySelectorAll('.ftab');
    var cur = box.querySelector('.fcur');
    var n = slides.length, active = 0, lock = false;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function buzz() { try { if (navigator.vibrate) navigator.vibrate(12); } catch (e) {} }

    function show(i, dir) {
      i = (i + n) % n;
      if (i === active && dir) return;
      var prev = slides[active];
      stage.classList.remove('dir-up', 'dir-down');
      if (dir) stage.classList.add(dir > 0 ? 'dir-down' : 'dir-up');
      if (dir && prev && i !== active) {
        prev.classList.add('leaving');
        setTimeout(function () { prev.classList.remove('leaving'); }, 460);
      }
      active = i;
      for (var k = 0; k < n; k++) {
        var on = k === active;
        slides[k].classList.toggle('is-active', on);
        slides[k].setAttribute('aria-hidden', on ? 'false' : 'true');
        tabs[k].classList.toggle('is-active', on);
        tabs[k].setAttribute('aria-selected', on ? 'true' : 'false');
        var f = tabs[k].querySelector('.fill');
        if (f) { f.style.animation = 'none'; void f.offsetWidth; f.style.animation = ''; }
      }
      if (cur) cur.textContent = (active + 1 < 10 ? '0' : '') + (active + 1);
    }

    function step(dir, fromUser) {
      if (lock) return true;
      var next = active + dir;
      if (fromUser && (next < 0 || next >= n)) return false;   // 到头了：把滚动还给页面
      lock = true; setTimeout(function () { lock = false; }, 650);
      show(next, dir);
      if (fromUser) { box.classList.add('used'); }
      return true;
    }

    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { show(k, k > active ? 1 : -1); box.classList.add('used'); });
      var f = t.querySelector('.fill');
      if (f) f.addEventListener('animationend', function () { if (k === active) show(active + 1, 1); });
    });

    // 滚轮：在大图上滚动切换
    var acc = 0;
    stage.addEventListener('wheel', function (e) {
      var d = Math.abs(e.deltaY) >= Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
      var dir = d > 0 ? 1 : -1;
      var next = active + dir;
      if (next < 0 || next >= n) { acc = 0; return; }       // 第一个往上、最后一个往下：正常滚动页面
      e.preventDefault();
      acc += d;
      if (Math.abs(acc) < 30) return;
      acc = 0;
      step(dir, true);
    }, { passive: false });

    // 触摸滑动（手机）：左右或上下滑
    var sx = 0, sy = 0, st = 0;
    stage.addEventListener('touchstart', function (e) { var t = e.touches[0]; sx = t.clientX; sy = t.clientY; st = Date.now(); }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
      if (Date.now() - st > 600) return;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.2) { if (step(dx < 0 ? 1 : -1, true)) buzz(); }
    }, { passive: true });

    // 键盘
    function onKey(e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { if (step(1, true)) e.preventDefault(); }
      else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { if (step(-1, true)) e.preventDefault(); }
    }
    stage.addEventListener('keydown', onKey);
    box.querySelector('.ftabs').addEventListener('keydown', onKey);

    if (!reduce) box.classList.add('playing');
    box.addEventListener('mouseenter', function () { box.classList.add('paused'); });
    box.addEventListener('mouseleave', function () { box.classList.remove('paused'); });
    box.addEventListener('focusin', function () { box.classList.add('paused'); });
    box.addEventListener('focusout', function () { box.classList.remove('paused'); });
    document.addEventListener('visibilitychange', function () { box.classList.toggle('paused', document.hidden); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    setLang(getLang());
    var btn = document.querySelector('.lang-btn');
    if (btn) btn.addEventListener('click', function () {
      setLang(document.documentElement.getAttribute('data-lang') === 'en' ? 'zh' : 'en');
    });
    initFeature();
    // 返回按钮：从本站页面进来就退回上一页，否则去链接指定的页面
    document.querySelectorAll('[data-back]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        var ref = document.referrer;
        if (ref && ref.indexOf(location.origin) === 0 && ref !== location.href && history.length > 1) { e.preventDefault(); history.back(); }
      });
    });
  });
})();
