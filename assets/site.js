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

  // 首页项目星座：六颗星代表六个项目。可以抓起、甩出（弹簧拉回）；靠近会被吸引并显示名字；点击进入项目页；
  // 抓起/点击时按五声音阶发声；背景小星点随鼠标视差闪烁，偶尔划过流星。
  function initConstellation() {
    var sky = document.getElementById('sky');
    if (!sky) return;
    var cv = sky.querySelector('canvas'), ctx = cv.getContext('2d');
    var data = JSON.parse(document.getElementById('stars-data').textContent);
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    // 北斗七星（按真实星图的相对位置）：天枢 天璇 天玑 天权 玉衡 开阳 瑶光
    var homes = [[0.86, 0.30], [0.84, 0.60], [0.62, 0.66], [0.58, 0.40], [0.42, 0.36], [0.26, 0.33], [0.09, 0.48]];
    var edges = [[6, 5], [5, 4], [4, 3], [3, 0], [0, 1], [1, 2], [2, 3]];
    var notes = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.66]; // 五声音阶 C D E G A C D
    var W = 0, H = 0, dpr = 1, mouse = { x: -999, y: -999, in: false }, grab = null, hover = -1, t0 = performance.now();
    var muted = false; try { muted = localStorage.getItem('skyMuted') === '1'; } catch (e) {}
    sky.classList.toggle('muted', muted);

    var stars = data.map(function (d, i) {
      return { d: d, i: i, x: 0, y: 0, vx: 0, vy: 0, r: 4 + (3.6 - d.mag) * 4.2, ph: Math.random() * 6.28, pulse: 0 };
    });
    var dust = [];
    for (var k = 0; k < 90; k++) dust.push({ x: Math.random(), y: Math.random(), r: Math.random() * 1.3 + .3, z: Math.random() * .8 + .2, ph: Math.random() * 6.28 });
    var shoot = null, nextShoot = performance.now() + 4000;

    function home(s, t) {
      var h = homes[s.i];
      return [h[0] * W + Math.sin(t / 2300 + s.ph) * 10, h[1] * H + Math.cos(t / 2900 + s.ph) * 8];
    }
    function resize() {
      var r = cv.getBoundingClientRect();
      dpr = Math.min(2, window.devicePixelRatio || 1);
      W = r.width; H = r.height;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      stars.forEach(function (s) { if (!s.x) { var h = home(s, 0); s.x = h[0]; s.y = h[1]; } });
    }

    // 声音
    var ac = null;
    function pluck(i) {
      if (muted) return;
      try {
        ac = ac || new (window.AudioContext || window.webkitAudioContext)();
        if (ac.state === 'suspended') ac.resume();
        var t = ac.currentTime, o = ac.createOscillator(), o2 = ac.createOscillator(), g = ac.createGain();
        o.type = 'triangle'; o2.type = 'sine';
        o.frequency.value = notes[i % notes.length]; o2.frequency.value = notes[i % notes.length] * 2;
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.18, t + 0.01); g.gain.exponentialRampToValueAtTime(0.0001, t + 1.2);
        o.connect(g); o2.connect(g); g.connect(ac.destination);
        o.start(t); o2.start(t); o.stop(t + 1.25); o2.stop(t + 1.25);
      } catch (e) {}
    }

    function pick(x, y) {
      var best = -1, bd = 30 * 30;
      stars.forEach(function (s, i) { var dx = s.x - x, dy = s.y - y, dd = dx * dx + dy * dy; if (dd < bd) { bd = dd; best = i; } });
      return best;
    }
    function pos(e) { var r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }

    cv.addEventListener('pointermove', function (e) {
      var p = pos(e); mouse.x = p.x; mouse.y = p.y; mouse.in = true;
      if (grab) {
        var s = stars[grab.i];
        if (Math.abs(p.x - grab.sx) + Math.abs(p.y - grab.sy) > 6) grab.moved = true;
        grab.vx = p.x - grab.lx; grab.vy = p.y - grab.ly; grab.lx = p.x; grab.ly = p.y;
        s.x = p.x; s.y = p.y;
        if (grab.moved) e.preventDefault();
      } else {
        hover = pick(p.x, p.y);
        cv.classList.toggle('pointing', hover >= 0);
      }
    });
    cv.addEventListener('pointerleave', function () { mouse.in = false; if (!grab) hover = -1; });
    cv.addEventListener('pointerdown', function (e) {
      var p = pos(e), i = pick(p.x, p.y);
      if (i < 0) return;
      grab = { i: i, sx: p.x, sy: p.y, lx: p.x, ly: p.y, vx: 0, vy: 0, moved: false, id: e.pointerId, prev: hover };
      hover = i; stars[i].pulse = 1; pluck(i);
      sky.classList.add('used'); cv.classList.add('grabbing');
      try { cv.setPointerCapture(e.pointerId); } catch (err) {}
      if (e.pointerType !== 'mouse') e.preventDefault();
    });
    function release(e) {
      if (!grab) return;
      var s = stars[grab.i];
      if (!grab.moved) {
        if (e && e.pointerType !== 'mouse' && grab.prev !== grab.i) { hover = grab.i; }   // 手机第一次点：先显示名字，再点才进入
        else { var href = s.d.href; setTimeout(function () { location.href = href; }, 160); }
      } else { s.vx = grab.vx * 0.9; s.vy = grab.vy * 0.9; }
      grab = null; cv.classList.remove('grabbing');
    }
    cv.addEventListener('pointerup', release);
    cv.addEventListener('pointercancel', release);
    sky.querySelector('.sky-mute').addEventListener('click', function () {
      muted = !muted; sky.classList.toggle('muted', muted);
      try { localStorage.setItem('skyMuted', muted ? '1' : '0'); } catch (e) {}
      if (!muted) pluck(2);
    });

    function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
    var col = {}, colAt = 0;
    function colors(t) {
      if (t - colAt < 800) return col;
      colAt = t; col = { paper: css('--paper') || '#efebe1', line: css('--line') || '#2b3146', dim: css('--dim') || '#767c93', panel: css('--panel') || '#181c2a', light: document.documentElement.getAttribute('data-theme') === 'light' };
      return col;
    }
    function rgba(hex, a) {
      var m = hex.replace('#', ''); if (m.length === 3) m = m.split('').map(function (c) { return c + c; }).join('');
      var n = parseInt(m, 16); return 'rgba(' + (n >> 16 & 255) + ',' + (n >> 8 & 255) + ',' + (n & 255) + ',' + a + ')';
    }

    function step(t) {
      var c = colors(t), lang = document.documentElement.getAttribute('data-lang') === 'zh' ? 'zh' : 'en';
      // 物理
      stars.forEach(function (s, i) {
        if (grab && grab.i === i) return;
        var h = home(s, reduce ? 0 : t);
        var ax = (h[0] - s.x) * 0.012, ay = (h[1] - s.y) * 0.012;
        if (mouse.in && !grab) {
          var dx = mouse.x - s.x, dy = mouse.y - s.y, d = Math.sqrt(dx * dx + dy * dy);
          if (d < 160 && d > 1) { var f = (1 - d / 160) * 0.9; ax += dx / d * f; ay += dy / d * f; }
        }
        s.vx = (s.vx + ax) * 0.92; s.vy = (s.vy + ay) * 0.92;
        s.x += s.vx; s.y += s.vy;
        s.x = Math.max(12, Math.min(W - 12, s.x)); s.y = Math.max(12, Math.min(H - 12, s.y));
        s.pulse *= 0.94;
      });
      // 绘制
      ctx.clearRect(0, 0, W, H);
      var px = mouse.in ? (mouse.x / W - .5) : 0, py = mouse.in ? (mouse.y / H - .5) : 0;
      // 星图坐标线：几条淡淡的赤纬弧线和赤经线
      ctx.strokeStyle = c.light ? 'rgba(80,64,40,.10)' : 'rgba(214,220,240,.07)'; ctx.lineWidth = 1;
      for (var q = 1; q <= 3; q++) { ctx.beginPath(); ctx.arc(W * 0.5 - px * 6, H * 2.4 - py * 6, H * (1.6 + q * 0.42), Math.PI * 1.15, Math.PI * 1.85); ctx.stroke(); }
      for (var m = -2; m <= 2; m++) { ctx.beginPath(); ctx.moveTo(W * 0.5 - px * 6, H * 2.4); ctx.lineTo(W * (0.5 + m * 0.22) - px * 6, -10); ctx.stroke(); }
      dust.forEach(function (p) {
        var a = (0.25 + 0.5 * (0.5 + 0.5 * Math.sin(t / 900 * p.z + p.ph))) * (c.light ? .55 : 1);
        ctx.fillStyle = c.light ? 'rgba(80,64,40,' + (a * .6) + ')' : 'rgba(239,235,225,' + a * .7 + ')';
        ctx.beginPath(); ctx.arc(p.x * W - px * 18 * p.z, p.y * H - py * 14 * p.z, p.r, 0, 6.283); ctx.fill();
      });
      // 流星
      if (!reduce && t > nextShoot && !shoot) { shoot = { x: W * (0.3 + Math.random() * .6), y: -10, t: t }; nextShoot = t + 7000 + Math.random() * 7000; }
      if (shoot) {
        var k = (t - shoot.t) / 900;
        if (k > 1) shoot = null; else {
          var sx = shoot.x - k * 240, sy = shoot.y + k * 160, g = ctx.createLinearGradient(sx, sy, sx + 70, sy - 46);
          g.addColorStop(0, rgba('#ffffff', c.light ? .5 : .9 * (1 - k))); g.addColorStop(1, rgba('#ffffff', 0));
          ctx.strokeStyle = g; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx + 70, sy - 46); ctx.stroke();
        }
      }
      // 连线：拉得越长越亮
      edges.forEach(function (e) {
        var a = stars[e[0]], b = stars[e[1]], ha = homes[e[0]], hb = homes[e[1]];
        var d = Math.hypot(a.x - b.x, a.y - b.y), d0 = Math.hypot((ha[0] - hb[0]) * W, (ha[1] - hb[1]) * H);
        var stretch = Math.max(0, Math.min(1, (d - d0) / 120));
        var g = ctx.createLinearGradient(a.x, a.y, b.x, b.y);
        g.addColorStop(0, rgba(a.d.color, .35 + stretch * .5)); g.addColorStop(1, rgba(b.d.color, .35 + stretch * .5));
        ctx.strokeStyle = g; ctx.lineWidth = 1.2 + stretch * 1.6;
        ctx.setLineDash(stretch > .05 ? [] : [4, 5]);
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      });
      ctx.setLineDash([]);
      // 星星：星图式四角星芒，大小按星等
      function spark(x, y, R, rot) {
        ctx.beginPath();
        for (var q = 0; q < 8; q++) {
          var ang = rot + q * Math.PI / 4, rr = q % 2 === 0 ? R : R * 0.26;
          ctx.lineTo(x + Math.cos(ang) * rr, y + Math.sin(ang) * rr);
        }
        ctx.closePath();
      }
      stars.forEach(function (s, i) {
        var on = i === hover || (grab && grab.i === i);
        var tw = 0.5 + 0.5 * Math.sin(t / 700 + s.ph);
        var R = s.r * (on ? 1.35 : 1) + s.pulse * 6;
        var gl = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, R * 3.2);
        gl.addColorStop(0, rgba(s.d.color, on ? .45 : .22 + tw * .1)); gl.addColorStop(1, rgba(s.d.color, 0));
        ctx.fillStyle = gl; ctx.beginPath(); ctx.arc(s.x, s.y, R * 3.2, 0, 6.283); ctx.fill();
        var len = R * (2.1 + tw * .35);
        ctx.fillStyle = s.d.color; spark(s.x, s.y, len, -Math.PI / 2); ctx.fill();               // 长星芒（上下左右）
        ctx.globalAlpha = .55; spark(s.x, s.y, len * .55, -Math.PI / 4); ctx.fill(); ctx.globalAlpha = 1; // 短星芒（斜向）
        ctx.fillStyle = rgba('#ffffff', .95); ctx.beginPath(); ctx.arc(s.x, s.y, Math.max(1.6, R * .34), 0, 6.283); ctx.fill();
        if (s.pulse > .05) { ctx.strokeStyle = rgba(s.d.color, s.pulse); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(s.x, s.y, R + (1 - s.pulse) * 26, 0, 6.283); ctx.stroke(); }
        // 小字星名（像星图上的标注）
        ctx.font = '500 9.5px "Cascadia Mono", Consolas, monospace';
        ctx.fillStyle = on ? s.d.color : c.dim;
        ctx.fillText((lang === 'zh' ? s.d.star_zh : s.d.star_en).toUpperCase(), s.x + len * .6 + 4, s.y + len * .6 + 10);
      });
      // 开阳旁边的辅星 Alcor
      var mz = stars[5];
      ctx.fillStyle = c.light ? 'rgba(80,64,40,.55)' : 'rgba(239,235,225,.75)';
      spark(mz.x + 13, mz.y - 9, 4.2, -Math.PI / 2); ctx.fill();
      // 标签
      var li = grab ? grab.i : hover;
      if (li >= 0) {
        var s = stars[li], name = s.d[lang], cat = (lang === 'zh' ? s.d.star_zh + ' · ' + s.d.czh : s.d.star_en + ' · ' + s.d.cen), sub = lang === 'zh' ? '点击进入 →' : 'Click to open →';
        ctx.font = '400 17px Georgia, "Noto Serif SC", serif'; var w1 = ctx.measureText(name).width;
        ctx.font = '500 10px "Cascadia Mono", Consolas, monospace'; var w2 = ctx.measureText(cat.toUpperCase()).width, w3 = ctx.measureText(sub).width;
        var bw = Math.max(w1, w2, w3) + 24, bh = 64, bx = s.x + 18, by = s.y - bh - 10;
        if (bx + bw > W - 6) bx = s.x - bw - 18; if (by < 6) by = s.y + 18;
        ctx.fillStyle = c.light ? 'rgba(255,255,255,.94)' : 'rgba(24,28,42,.92)';
        ctx.strokeStyle = rgba(s.d.color, .7); ctx.lineWidth = 1;
        if (ctx.roundRect) { ctx.beginPath(); ctx.roundRect(bx, by, bw, bh, 9); ctx.fill(); ctx.stroke(); } else { ctx.fillRect(bx, by, bw, bh); ctx.strokeRect(bx, by, bw, bh); }
        ctx.fillStyle = c.paper; ctx.font = '400 17px Georgia, "Noto Serif SC", serif'; ctx.fillText(name, bx + 12, by + 24);
        ctx.fillStyle = s.d.color; ctx.font = '500 10px "Cascadia Mono", Consolas, monospace'; ctx.fillText(cat.toUpperCase(), bx + 12, by + 40);
        ctx.fillStyle = c.dim; ctx.fillText(sub, bx + 12, by + 55);
      }
      requestAnimationFrame(step);
    }
    resize();
    window.addEventListener('resize', resize);
    requestAnimationFrame(step);
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
      var row = box.querySelector('.ftabs');
      if (row && row.scrollWidth > row.clientWidth + 4) {
        try { row.scrollTo({ left: Math.max(0, tabs[active].offsetLeft - 16), behavior: 'smooth' }); } catch (e) { row.scrollLeft = tabs[active].offsetLeft - 16; }
      }
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

    // 手机/触控笔：左右拖动插画来播放动画，拖过一个项目的长度就切换；上下滑照常滚动页面
    var drag = null, justDragged = false;
    stage.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse') return;
      drag = { id: e.pointerId, x: e.clientX, y: e.clientY, base: target, on: false };
    });
    stage.addEventListener('pointermove', function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      if (!drag.on) {
        if (Math.abs(dx) < 8 || Math.abs(dx) < Math.abs(dy)) return;
        drag.on = true; userTouched();
        try { stage.setPointerCapture(e.pointerId); } catch (err) {}
      }
      var w = stage.clientWidth || 300;
      var t = drag.base - dx / (w * 0.9);
      lastUser = now();
      if (t > 1) {
        if (active < n - 1) { switchTo(active + 1, 1, 0); buzz(); drag.x = e.clientX; drag.base = 0; t = 0; } else t = 1;
      } else if (t < 0) {
        if (active > 0) { switchTo(active - 1, -1, 1); buzz(); drag.x = e.clientX; drag.base = 1; t = 1; } else t = 0;
      }
      target = t;
    });
    function endDrag(e) {
      if (!drag || (e && e.pointerId !== drag.id)) return;
      if (drag.on) { justDragged = true; setTimeout(function () { justDragged = false; }, 50); }
      drag = null;
    }
    stage.addEventListener('pointerup', endDrag);
    stage.addEventListener('pointercancel', endDrag);
    stage.addEventListener('click', function (e) { if (justDragged) { e.preventDefault(); e.stopPropagation(); } }, true);

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
      phase += (target - phase) * Math.min(1, dt / (drag && drag.on ? 40 : 110));
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
    initConstellation();
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
