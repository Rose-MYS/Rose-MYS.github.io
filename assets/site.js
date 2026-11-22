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

  // 首页精选：一次展示一个项目，自动轮播；悬停暂停，点列表切换
  function initFeature() {
    var box = document.getElementById('feature');
    if (!box) return;
    var slides = box.querySelectorAll('.fslide');
    var tabs = box.querySelectorAll('.ftab');
    var n = slides.length, active = 0;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function show(i) {
      active = (i + n) % n;
      for (var k = 0; k < n; k++) {
        var on = k === active;
        slides[k].classList.toggle('is-active', on);
        slides[k].setAttribute('aria-hidden', on ? 'false' : 'true');
        tabs[k].classList.toggle('is-active', on);
        tabs[k].setAttribute('aria-selected', on ? 'true' : 'false');
        var f = tabs[k].querySelector('.fill');
        if (f) { f.style.animation = 'none'; void f.offsetWidth; f.style.animation = ''; }
      }
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { show(k); });
      var f = t.querySelector('.fill');
      if (f) f.addEventListener('animationend', function () { if (k === active) show(active + 1); });
    });
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
