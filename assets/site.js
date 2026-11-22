// 语言切换：中文 / English，选择记在浏览器里
(function () {
  function getLang() {
    try { return localStorage.getItem('lang') || 'zh'; } catch (e) { return 'zh'; }
  }
  function setLang(lang) {
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    try { localStorage.setItem('lang', lang); } catch (e) {}
    var btn = document.querySelector('.lang-btn');
    if (btn) btn.textContent = lang === 'en' ? '中文' : 'EN';
    var t = document.querySelector('meta[name="title-' + lang + '"]');
    if (t) document.title = t.content;
  }
  setLang(getLang());
  document.addEventListener('DOMContentLoaded', function () {
    setLang(getLang());
    var btn = document.querySelector('.lang-btn');
    if (btn) btn.addEventListener('click', function () {
      setLang(document.documentElement.getAttribute('data-lang') === 'en' ? 'zh' : 'en');
    });
  });
})();
