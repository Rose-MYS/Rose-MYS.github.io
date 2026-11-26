// 语言切换：默认英文，可切换中文；选择记在浏览器里
(function () {
  var BASE = ((document.currentScript && document.currentScript.src) || '').replace(/site\.js.*$/, '');
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

  // 全站星空背景（炫酷版）：
  //  · 密集的星点 + 少量带四角星芒的亮星 + 一条斜穿屏幕的银河星带
  //  · 鼠标附近星星变亮变大、暗星显现，并自动用细线连成"临时星座"，跟随光晕
  //  · 两团星云和银河的颜色在陶土橙 / 紫罗兰 / 青绿 / 金色之间定时渐变
  //  · 不时划过彩色流星；在空白处点击会荡开一圈光波
  function initStarfield() {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var cv = document.createElement('canvas');
    cv.className = 'bg-sky'; cv.setAttribute('aria-hidden', 'true');
    document.body.insertBefore(cv, document.body.firstChild);
    document.documentElement.classList.add('sky-on');
    var ctx = cv.getContext('2d'), W = 0, H = 0, dpr = 1, stars = [], bright = [];
    var mouse = { x: -9999, y: -9999, sx: -9999, sy: -9999 };
    var palette = [[217, 119, 87], [155, 135, 245], [94, 196, 196], [232, 182, 90]];
    var CYCLE = 24000, BAND = -0.38, meteors = [], nextMeteor = 0, ripples = [];

    function gauss() { return (Math.random() + Math.random() + Math.random() - 1.5) / 1.5; }
    function build() {
      dpr = Math.min(1.5, window.devicePixelRatio || 1);
      W = window.innerWidth; H = window.innerHeight;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.min(1100, Math.round(W * H / 1700));
      stars = [];
      function add(x, y, inBand) {
        var hidden = Math.random() < (inBand ? 0.25 : 0.38);
        stars.push({ x: x, y: y, r: Math.random() * (inBand ? 0.9 : 1.15) + 0.3,
          a: hidden ? 0.035 : Math.random() * 0.55 + (inBand ? 0.2 : 0.16), ph: Math.random() * 6.28, sp: Math.random() * 0.9 + 0.35,
          z: Math.random() * 0.8 + 0.2, tint: Math.random() < 0.12, kick: 0 });
      }
      for (var i = 0; i < n; i++) add(Math.random() * W, Math.random() * H, false);
      // 银河：沿一条斜线高斯分布的额外星点
      var cx = W / 2, cy = H / 2, ca = Math.cos(BAND), sa = Math.sin(BAND), L = Math.hypot(W, H);
      for (var k = 0; k < n * 0.55; k++) {
        var u = (Math.random() - 0.5) * L, v = gauss() * H * 0.11;
        var x = cx + u * ca - v * sa, y = cy + u * sa + v * ca;
        if (x > -10 && x < W + 10 && y > -10 && y < H + 10) add(x, y, true);
      }
      bright = [];
      for (var b = 0; b < Math.max(6, Math.round(W * H / 90000)); b++)
        bright.push({ x: Math.random() * W, y: Math.random() * H, r: Math.random() * 1.4 + 1.6, ph: Math.random() * 6.28, z: Math.random() * 0.6 + 0.4 });
    }
    function cycleColor(t, off) {
      var k = ((t + off) % CYCLE) / CYCLE * palette.length, i = Math.floor(k), f = k - i;
      f = f * f * (3 - 2 * f);
      var a = palette[i % palette.length], b = palette[(i + 1) % palette.length];
      return [Math.round(a[0] + (b[0] - a[0]) * f), Math.round(a[1] + (b[1] - a[1]) * f), Math.round(a[2] + (b[2] - a[2]) * f)];
    }
    function rgb(c, a) { return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; }
    function spark(x, y, R) {
      ctx.beginPath();
      for (var q = 0; q < 8; q++) { var ang = -Math.PI / 2 + q * Math.PI / 4, rr = q % 2 === 0 ? R : R * 0.22; ctx.lineTo(x + Math.cos(ang) * rr, y + Math.sin(ang) * rr); }
      ctx.closePath(); ctx.fill();
    }

    // 鼠标：跟随指针。手指：单独用 touch 事件（很多手机浏览器在滚动时会取消 pointer 事件，或根本不支持 pointer 事件）
    var touchOn = false, touchEnd = -1e9, usingTouch = false, act = 0;
    window.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch') return;
      usingTouch = false; mouse.x = e.clientX; mouse.y = e.clientY;
    }, { passive: true });
    function tpos(e, start) {
      var p = e.touches && e.touches[0]; if (!p) return;
      usingTouch = true; touchOn = true; mouse.x = p.clientX; mouse.y = p.clientY;
      if (start) { mouse.sx = mouse.x; mouse.sy = mouse.y; }
    }
    window.addEventListener('touchstart', function (e) {
      tpos(e, true);
      if (!window.PointerEvent && !reduce && e.touches[0] && !(e.target.closest && e.target.closest('a, button, input, textarea, select, iframe, canvas, .fstage, .ftabs, .pcard, .dest, .demo')))
        ripples.push({ x: e.touches[0].clientX, y: e.touches[0].clientY, t: performance.now() });
    }, { passive: true });
    window.addEventListener('touchmove', function (e) { tpos(e, false); }, { passive: true });
    function tend(e) { if (!e.touches || !e.touches.length) { touchOn = false; touchEnd = performance.now(); } }
    window.addEventListener('touchend', tend, { passive: true });
    window.addEventListener('touchcancel', tend, { passive: true });
    document.addEventListener('pointerleave', function () { mouse.x = mouse.y = -9999; });
    window.addEventListener('resize', build);
    window.addEventListener('pointerdown', function (e) {
      if (reduce) return;
      if (e.target.closest && e.target.closest('a, button, input, textarea, select, iframe, canvas, .fstage, .ftabs, .pcard, .dest, .demo')) return;
      ripples.push({ x: e.clientX, y: e.clientY, t: performance.now() });
    }, { passive: true });

    var slow = 0, frames = 0, budgetCut = false;
    function frame(t) {
      if (document.hidden) { requestAnimationFrame(frame); return; }
      var f0 = performance.now();
      var light = document.documentElement.getAttribute('data-theme') === 'light';
      var tt = reduce ? 0 : t, A = light ? 0.55 : 1;
      if (mouse.sx < -9000) { mouse.sx = mouse.x; mouse.sy = mouse.y; }
      mouse.sx += (mouse.x - mouse.sx) * 0.12; mouse.sy += (mouse.y - mouse.sy) * 0.12;
      // 手指松开后，光晕和临时星座停留一会儿再淡出
      var want = mouse.x > -9000 ? (usingTouch ? (touchOn ? 1 : Math.max(0, 1 - (t - touchEnd) / 1500)) : 1) : 0;
      act += (want - act) * 0.15;
      if (usingTouch && !touchOn && t - touchEnd > 1700) { mouse.x = mouse.y = -9999; act = 0; }
      var on = mouse.sx > -9000 && mouse.x > -9000 && act > 0.01;
      ctx.clearRect(0, 0, W, H);
      var c1 = cycleColor(tt, 0), c2 = cycleColor(tt, CYCLE / 2), c3 = cycleColor(tt, CYCLE / 4);
      var base = light ? [90, 70, 40] : [236, 232, 222];
      // 星云
      var nx = W * (0.22 + 0.06 * Math.sin(tt / 9000)), ny = H * (0.28 + 0.05 * Math.cos(tt / 11000));
      var g = ctx.createRadialGradient(nx, ny, 0, nx, ny, Math.max(W, H) * 0.55);
      g.addColorStop(0, rgb(c1, 0.13 * A)); g.addColorStop(1, rgb(c1, 0)); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      var mx2 = W * (0.80 + 0.05 * Math.cos(tt / 10000)), my2 = H * (0.75 + 0.06 * Math.sin(tt / 12000));
      g = ctx.createRadialGradient(mx2, my2, 0, mx2, my2, Math.max(W, H) * 0.5);
      g.addColorStop(0, rgb(c2, 0.10 * A)); g.addColorStop(1, rgb(c2, 0)); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      // 银河光带
      ctx.save(); ctx.translate(W / 2, H / 2); ctx.rotate(BAND); ctx.scale(1, 0.16);
      g = ctx.createRadialGradient(0, 0, 0, 0, 0, Math.hypot(W, H) * 0.6);
      g.addColorStop(0, rgb(c3, 0.10 * A)); g.addColorStop(0.5, rgb(c3, 0.04 * A)); g.addColorStop(1, rgb(c3, 0));
      ctx.fillStyle = g; ctx.fillRect(-W * 2, -H * 4, W * 4, H * 8); ctx.restore();
      // 鼠标光晕
      if (on) {
        g = ctx.createRadialGradient(mouse.sx, mouse.sy, 0, mouse.sx, mouse.sy, 260);
        g.addColorStop(0, rgb(c1, (usingTouch ? 0.2 : 0.14) * A * act)); g.addColorStop(1, rgb(c1, 0));
        ctx.fillStyle = g; ctx.fillRect(mouse.sx - 260, mouse.sy - 260, 520, 520);
      }
      // 涟漪
      for (var ri = ripples.length - 1; ri >= 0; ri--) {
        var rp = ripples[ri], age = (t - rp.t) / 1400;
        if (age > 1) { ripples.splice(ri, 1); continue; }
        rp.R = age * 520;
        ctx.strokeStyle = rgb(c1, (1 - age) * 0.55 * A); ctx.lineWidth = 2 * (1 - age) + 0.5;
        ctx.beginPath(); ctx.arc(rp.x, rp.y, rp.R, 0, 6.283); ctx.stroke();
      }
      // 星星
      var px = on ? (mouse.sx / W - 0.5) : 0, py = on ? (mouse.sy / H - 0.5) : 0, near = [];
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        var x = s.x - px * 16 * s.z, y = s.y - py * 12 * s.z, boost = 0;
        if (on) { var dx = x - mouse.sx, dy = y - mouse.sy, d2 = dx * dx + dy * dy; if (d2 < 52900) { boost = (1 - Math.sqrt(d2) / 230) * act; if (d2 < 22500 && s.a > 0.1) near.push([x, y, boost]); } }
        for (var rj = 0; rj < ripples.length; rj++) { var r2 = ripples[rj], dd = Math.abs(Math.hypot(x - r2.x, y - r2.y) - r2.R); if (dd < 30) s.kick = Math.max(s.kick, 1 - dd / 30); }
        s.kick *= 0.93;
        var tw = reduce ? 0.7 : 0.55 + 0.45 * Math.sin(tt / 1000 * s.sp + s.ph);
        var a = s.a * tw + boost * boost * 0.9 + s.kick * 0.8;
        if (a < 0.02) continue;
        var r = s.r * (1 + boost * 1.2 + s.kick);
        ctx.fillStyle = rgb(s.tint || s.kick > .3 ? c2 : base, Math.min(1, a) * (light ? 0.6 : 1));
        ctx.beginPath(); ctx.arc(x, y, r, 0, 6.283); ctx.fill();
      }
      // 鼠标附近自动连成临时星座
      if (near.length > 1) {
        near.sort(function (p, q) { return q[2] - p[2]; }); near = near.slice(0, 22);
        ctx.lineWidth = 0.8;
        for (var m = 0; m < near.length; m++) for (var nn = m + 1; nn < near.length; nn++) {
          var p1 = near[m], p2 = near[nn], dl = Math.hypot(p1[0] - p2[0], p1[1] - p2[1]);
          if (dl < 75) { ctx.strokeStyle = rgb(c1, Math.min(p1[2], p2[2]) * (1 - dl / 75) * 0.9 * A); ctx.beginPath(); ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke(); }
        }
      }
      // 亮星（四角星芒）
      for (var bi = 0; bi < bright.length; bi++) {
        var bs = bright[bi], bx = bs.x - px * 20 * bs.z, by = bs.y - py * 15 * bs.z;
        var tw2 = reduce ? 0.8 : 0.6 + 0.4 * Math.sin(tt / 1300 + bs.ph);
        var gl = ctx.createRadialGradient(bx, by, 0, bx, by, bs.r * 6);
        gl.addColorStop(0, rgb(base, 0.25 * tw2 * A)); gl.addColorStop(1, rgb(base, 0)); ctx.fillStyle = gl;
        ctx.beginPath(); ctx.arc(bx, by, bs.r * 6, 0, 6.283); ctx.fill();
        ctx.fillStyle = rgb(base, (0.55 + 0.4 * tw2) * (light ? 0.7 : 1)); spark(bx, by, bs.r * (3 + tw2));
      }
      // 流星
      if (!reduce && t > nextMeteor) {
        var fromLeft = Math.random() < 0.5;
        meteors.push({ x: fromLeft ? Math.random() * W * 0.5 : W * (0.5 + Math.random() * 0.5), y: -20, vx: (fromLeft ? 1 : -1) * (6 + Math.random() * 4), vy: 3.5 + Math.random() * 2.5, life: 0 });
        nextMeteor = t + 3500 + Math.random() * 5000;
      }
      for (var mi = meteors.length - 1; mi >= 0; mi--) {
        var me = meteors[mi]; me.x += me.vx; me.y += me.vy; me.life++;
        if (me.y > H + 40 || me.x < -60 || me.x > W + 60) { meteors.splice(mi, 1); continue; }
        var tx = me.x - me.vx * 14, ty = me.y - me.vy * 14, lg = ctx.createLinearGradient(me.x, me.y, tx, ty);
        lg.addColorStop(0, rgb([255, 255, 255], 0.9 * A)); lg.addColorStop(0.25, rgb(c2, 0.6 * A)); lg.addColorStop(1, rgb(c2, 0));
        ctx.strokeStyle = lg; ctx.lineWidth = 1.8; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(me.x, me.y); ctx.lineTo(tx, ty); ctx.stroke();
      }
      // 自动降级：设备画得太慢就减少星星数量
      frames++; if (performance.now() - f0 > 14) slow++;
      if (frames === 90) { if (!budgetCut && slow > 45) { budgetCut = true; stars = stars.filter(function (_, i) { return i % 2 === 0; }); } frames = slow = 0; }
      requestAnimationFrame(frame);
    }
    build();
    requestAnimationFrame(frame);
  }

  // 首页项目星座：六颗星代表六个项目。可以抓起、甩出（弹簧拉回）；靠近会被吸引并显示名字；点击进入项目页；
  // 抓起/点击时按五声音阶发声；背景小星点随鼠标视差闪烁，偶尔划过流星。
  function initConstellation() {
    var sky = document.getElementById('sky');
    if (!sky) return;
    var cv = sky.querySelector('canvas'), ctx = cv.getContext('2d');
    var SKY = JSON.parse(document.getElementById('stars-data').textContent), data = SKY.stars;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    // 北斗七星（按真实星图的相对位置）：天枢 天璇 天玑 天权 玉衡 开阳 瑶光；再沿天璇→天枢的指极线找到北极星
    var homes = data.map(function (d) { return [d.x, d.y]; }), edges = SKY.edges, pointer = SKY.pointer || [], groups = SKY.groups || [];
    var MIZAR = data.findIndex ? data.findIndex(function (d) { return d.star_en === 'Mizar'; }) : 5;
    var notes = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.66]; // 五声音阶 C D E G A C D
    var W = 0, H = 0, dpr = 1, mouse = { x: -999, y: -999, in: false }, grab = null, hover = -1, t0 = performance.now();
    var muted = false; try { muted = localStorage.getItem('skyMuted') === '1'; } catch (e) {}
    sky.classList.toggle('muted', muted);

    var stars = data.map(function (d, i) {
      return { d: d, i: i, x: 0, y: 0, vx: 0, vy: 0, r: d.unlit ? 3 + (3.8 - d.mag) * 1.8 : 4 + (3.6 - d.mag) * 4.2, ph: Math.random() * 6.28, pulse: 0 };
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

    // 声音：真钢琴采样（Salamander Grand Piano，CC BY 3.0），首次靠近星图时预加载
    var ac = null, master = null, bufs = {}, loading = false;
    var MAP = [['C5', 0], ['C5', 2], ['Ds5', 1], ['Fs5', 1], ['A5', 0], ['C6', 0], ['C6', 2], ['Ds6', 1]]; // C D E G A C D E
    function audio() {
      if (!ac) {
        ac = new (window.AudioContext || window.webkitAudioContext)();
        master = ac.createDynamicsCompressor(); master.threshold.value = -14; master.ratio.value = 4;
        var out = ac.createGain(); out.gain.value = 0.9; master.connect(out); out.connect(ac.destination);
        // 简单的房间混响：衰减噪声做冲激响应
        var len = Math.round(ac.sampleRate * 2.2), ir = ac.createBuffer(2, len, ac.sampleRate);
        for (var c = 0; c < 2; c++) { var d = ir.getChannelData(c); for (var k = 0; k < len; k++) d[k] = (Math.random() * 2 - 1) * Math.pow(1 - k / len, 3.2); }
        var rev = ac.createConvolver(); rev.buffer = ir;
        var wet = ac.createGain(); wet.gain.value = 0.22; rev.connect(wet); wet.connect(master);
        master.rev = rev;
      }
      return ac;
    }
    function preload() {
      if (loading || muted) return; loading = true;
      try { audio(); } catch (e) { return; }
      ['C5', 'Ds5', 'Fs5', 'A5', 'C6', 'Ds6'].forEach(function (n) {
        fetch(BASE + 'piano/' + n + '.mp3').then(function (r) { return r.arrayBuffer(); }).then(function (ab) {
          ac.decodeAudioData(ab, function (b) { bufs[n] = b; }, function () {});
        }).catch(function () {});
      });
    }
    function voice(m, vel) {
      var b = bufs[m[0]]; if (!b) return false;
      var t = ac.currentTime, src = ac.createBufferSource(), g = ac.createGain();
      src.buffer = b; src.playbackRate.value = Math.pow(2, m[1] / 12);
      g.gain.setValueAtTime(vel, t); g.gain.setValueAtTime(vel, t + 1.8); g.gain.exponentialRampToValueAtTime(0.0001, t + 3.2);
      src.connect(g); g.connect(master); g.connect(master.rev);
      src.start(t); src.stop(t + 3.3);
      return true;
    }
    function pluck(i) {
      if (muted) return;
      try {
        audio(); preload();
        if (ac.state === 'suspended') ac.resume();
        var m = MAP[i % MAP.length], vel = 0.5 + Math.random() * 0.15, t0 = Date.now();
        if (!voice(m, vel)) {
          // 采样还没下载好：等一下再弹，太久就放弃
          var tries = setInterval(function () { if (voice(m, vel) || Date.now() - t0 > 500) clearInterval(tries); }, 40);
        }
      } catch (e) {}
    }

    sky.addEventListener('pointerenter', preload, { once: true });
    sky.addEventListener('touchstart', preload, { passive: true, once: true });

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
      lastTouch = e.pointerType !== 'mouse';
      var p = pos(e), i = pick(p.x, p.y);
      if (i < 0) return;
      grab = { i: i, sx: p.x, sy: p.y, lx: p.x, ly: p.y, vx: 0, vy: 0, moved: false, id: e.pointerId, prev: hover };
      hover = i; stars[i].pulse = 1; pluck(i);
      sky.classList.add('used'); cv.classList.add('grabbing');
      try { cv.setPointerCapture(e.pointerId); } catch (err) {}
      if (e.pointerType !== 'mouse') e.preventDefault();
    });
    var lastClick = { i: -1, t: 0 }, lastTouch = false;
    function release(e) {
      if (!grab) return;
      var s = stars[grab.i];
      if (!grab.moved) {
        var now = Date.now(), href = s.d.href;
        if (!href) { hover = grab.i; }
        else if (e && e.pointerType === 'mouse') {
          // 电脑：单击弹一个音，双击进入项目
          if (lastClick.i === grab.i && now - lastClick.t < 420) { lastClick = { i: -1, t: 0 }; setTimeout(function () { location.href = href; }, 120); }
          else lastClick = { i: grab.i, t: now };
        } else if (grab.prev !== grab.i) { hover = grab.i; }   // 手机第一次点：弹音并显示名字，再点才进入
        else { setTimeout(function () { location.href = href; }, 160); }
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
      // 指极线：天璇→天枢延长到北极星（淡淡的点线）
      pointer.forEach(function (e) {
        var a = stars[e[0]], b = stars[e[1]];
        ctx.strokeStyle = c.light ? 'rgba(80,64,40,.22)' : 'rgba(239,235,225,.18)'; ctx.lineWidth = 1; ctx.setLineDash([1.5, 5]);
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      });
      ctx.setLineDash([]);
      // 星座名
      ctx.font = '500 9px "Cascadia Mono", Consolas, monospace';
      ctx.fillStyle = c.light ? 'rgba(80,64,40,.42)' : 'rgba(214,220,240,.32)';
      groups.forEach(function (g) { ctx.fillText(lang === 'zh' ? g.zh : g.en, g.x * W - px * 4, g.y * H - py * 4); });
      // 连线：拉得越长越亮
      edges.forEach(function (e) {
        var a = stars[e[0]], b = stars[e[1]], ha = homes[e[0]], hb = homes[e[1]];
        var d = Math.hypot(a.x - b.x, a.y - b.y), d0 = Math.hypot((ha[0] - hb[0]) * W, (ha[1] - hb[1]) * H);
        var stretch = Math.max(0, Math.min(1, (d - d0) / 120));
        var g = ctx.createLinearGradient(a.x, a.y, b.x, b.y);
        var la = (a.d.unlit ? .24 : .35) + stretch * .5, lb = (b.d.unlit ? .24 : .35) + stretch * .5;
        g.addColorStop(0, rgba(a.d.color, la)); g.addColorStop(1, rgba(b.d.color, lb));
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
        ctx.globalAlpha = s.d.unlit && !on ? .72 : 1;
        var tw = 0.5 + 0.5 * Math.sin(t / 700 + s.ph);
        var R = s.r * (on ? 1.35 : 1) + s.pulse * 6;
        var gl = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, R * 3.2);
        gl.addColorStop(0, rgba(s.d.color, on ? .45 : .22 + tw * .1)); gl.addColorStop(1, rgba(s.d.color, 0));
        ctx.fillStyle = gl; ctx.beginPath(); ctx.arc(s.x, s.y, R * 3.2, 0, 6.283); ctx.fill();
        var len = R * (2.1 + tw * .35);
        ctx.fillStyle = s.d.color; spark(s.x, s.y, len, -Math.PI / 2); ctx.fill();               // 长星芒（上下左右）
        var ga = ctx.globalAlpha; ctx.globalAlpha = ga * .55; spark(s.x, s.y, len * .55, -Math.PI / 4); ctx.fill(); ctx.globalAlpha = ga; // 短星芒（斜向）
        ctx.fillStyle = rgba('#ffffff', .95); ctx.beginPath(); ctx.arc(s.x, s.y, Math.max(1.6, R * .34), 0, 6.283); ctx.fill();
        if (s.pulse > .05) { ctx.strokeStyle = rgba(s.d.color, s.pulse); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(s.x, s.y, R + (1 - s.pulse) * 26, 0, 6.283); ctx.stroke(); }
        // 小字星名（像星图上的标注）
        ctx.font = '500 9.5px "Cascadia Mono", Consolas, monospace';
        ctx.fillStyle = on ? s.d.color : c.dim;
        if (!s.d.unlit || on) ctx.fillText((lang === 'zh' ? s.d.star_zh : s.d.star_en).toUpperCase(), s.x + len * .6 + 4, s.y + len * .6 + 10);
        ctx.globalAlpha = 1;
      });
      // 开阳旁边的辅星 Alcor
      var mz = stars[MIZAR >= 0 ? MIZAR : 5];
      ctx.fillStyle = c.light ? 'rgba(80,64,40,.55)' : 'rgba(239,235,225,.75)';
      spark(mz.x + 13, mz.y - 9, 4.2, -Math.PI / 2); ctx.fill();
      // 标签
      var li = grab ? grab.i : hover;
      if (li >= 0) {
        var s = stars[li], name = s.d[lang], cat = (lang === 'zh' ? s.d.star_zh + ' · ' + s.d.czh : s.d.star_en + ' · ' + s.d.cen), sub = !s.d.href ? (lang === 'zh' ? '这里会是下一个项目' : 'A future project goes here') : (lastTouch ? (lang === 'zh' ? '再点一下进入 →' : 'Tap again to open →') : (lang === 'zh' ? '双击进入 →' : 'Double-click to open →'));
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
      updateCounts(slides[active], phase);
      for (var k = 0; k < n; k++) {
        var f = tabs[k].querySelector('.fill');
        if (f) f.style.width = (k === active ? phase * 100 : 0).toFixed(1) + '%';
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }


  // 插画里的数字跟着 --phase 变化（如用量面板 42.1M → 92.0M）
  function updateCounts(root, p) {
    if (!root) return;
    var cs = root.querySelectorAll('.count');
    for (var i = 0; i < cs.length; i++) {
      var c = cs[i], a = parseFloat(c.getAttribute('data-from')), b = parseFloat(c.getAttribute('data-to'));
      var dec = c.hasAttribute('data-dec') ? +c.getAttribute('data-dec') : 1;
      var v = (a + (b - a) * p).toFixed(dec) + (c.getAttribute('data-unit') || '');
      if (c.textContent !== v) c.textContent = v;
    }
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
        updateCounts(el, p);
      });
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }


  // 训练过程：滚到可见时播放图表/时间线动画；对比滑块
  function initTraining() {
    var els = document.querySelectorAll('.tl-chart, .tl-item');
    if (els.length) {
      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (es) {
          es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
        }, { threshold: 0.25 });
        els.forEach(function (el) { io.observe(el); });
      } else els.forEach(function (el) { el.classList.add('in'); });
    }
    document.querySelectorAll('.cmp').forEach(function (c) {
      var r = c.querySelector('.cmp-range');
      if (!r) return;
      var set = function () { c.style.setProperty('--pos', r.value + '%'); };
      r.addEventListener('input', set); set();
    });
  }


  // 详情页左侧目录：从正文标题生成，滚动时高亮当前小节
  function initToc() {
    var toc = document.querySelector('.toc'), prose = document.querySelector('.dlayout .prose');
    if (!toc || !prose) return;
    var hs = prose.querySelectorAll(':scope > h2, :scope > h3.tl-sub');
    if (hs.length < 3) { toc.parentNode.classList.add('notoc'); return; }
    var ol = toc.querySelector('ol'), links = [];
    hs.forEach(function (h, i) {
      if (!h.id) h.id = 'sec-' + (i + 1);
      var li = document.createElement('li'); if (h.tagName === 'H3') li.className = 'sub';
      var a = document.createElement('a'); a.href = '#' + h.id;
      var c = h.cloneNode(true); c.querySelectorAll('small').forEach(function (s) { s.remove(); });
      a.innerHTML = c.innerHTML; li.appendChild(a); ol.appendChild(li); links.push(a);
    });
    var tick = false;
    function spy() {
      tick = false; var cur = 0, y = 120;
      hs.forEach(function (h, i) { if (h.getBoundingClientRect().top < y) cur = i; });
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) cur = hs.length - 1;
      links.forEach(function (a, i) { a.classList.toggle('on', i === cur); });
    }
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(spy); } }, { passive: true });
    spy();
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
    initStarfield();
    initConstellation();
    initFeature();
    initScrollArt();
    initTraining();
    initToc();
    // 返回按钮：从本站页面进来就退回上一页，否则去链接指定的页面
    document.querySelectorAll('[data-back]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        var ref = document.referrer;
        if (ref && ref.indexOf(location.origin) === 0 && ref !== location.href && history.length > 1) { e.preventDefault(); history.back(); }
      });
    });
  });
})();
