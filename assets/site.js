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

  // 首页展台：滚动切换项目
  function initShowcase() {
    var sc = document.getElementById('showcase');
    if (!sc) return;
    var slides = sc.querySelectorAll('.slide');
    var tabs = sc.querySelectorAll('.tab');
    var cur = sc.querySelector('.sc-cur');
    var sticky = sc.querySelector('.sc-sticky');
    var n = slides.length, active = -1, ticking = false;

    function range() { return Math.max(1, sc.offsetHeight - sticky.offsetHeight); }

    function show(i) {
      if (i === active) return;
      active = i;
      for (var k = 0; k < n; k++) {
        var on = k === i;
        slides[k].classList.toggle('is-active', on);
        slides[k].setAttribute('aria-hidden', on ? 'false' : 'true');
        tabs[k].classList.toggle('is-active', on);
        tabs[k].classList.toggle('done', k < i);
        tabs[k].setAttribute('aria-selected', on ? 'true' : 'false');
      }
      if (cur) cur.textContent = (i + 1 < 10 ? '0' : '') + (i + 1);
      sticky.style.setProperty('--glow', getComputedStyle(slides[i]).getPropertyValue('--accent'));
    }

    function update() {
      ticking = false;
      var p = Math.min(Math.max(-sc.getBoundingClientRect().top / range(), 0), 0.9999);
      var x = p * n, i = Math.floor(x);
      show(i);
      for (var k = 0; k < n; k++) {
        var f = tabs[k].querySelector('.fill');
        if (f) f.style.width = k < i ? '100%' : k === i ? ((x - i) * 100).toFixed(1) + '%' : '0%';
      }
    }

    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () {
        var y = sc.getBoundingClientRect().top + window.scrollY + range() * (k + 0.02) / n;
        window.scrollTo({ top: y, behavior: 'smooth' });
      });
    });
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    setLang(getLang());
    var btn = document.querySelector('.lang-btn');
    if (btn) btn.addEventListener('click', function () {
      setLang(document.documentElement.getAttribute('data-lang') === 'en' ? 'zh' : 'en');
    });
    initShowcase();
  });
})();
