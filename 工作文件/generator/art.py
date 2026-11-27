"""每个项目一张原创插画（纯 SVG，跟随主题色）。viewBox 统一 600x360。"""

_SHADOW = '<ellipse cx="300" cy="318" rx="230" ry="26" fill="#000" opacity=".28"/>'


def _svg(inner, label):
    return (f'<svg class="art" viewBox="0 0 600 360" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg>')


# 形声：一张斜放的画纸，彩色线条 + 扫过的播放头
shapesound = _svg(f"""
{_SHADOW}
<g transform="translate(300 175) skewX(-14) rotate(-4)">
  <rect x="-210" y="-120" width="420" height="250" rx="10" fill="#e9e3cf"/>
  <rect x="-210" y="-120" width="420" height="250" rx="10" fill="none" stroke="#c9bf9f" stroke-width="2"/>
  <g stroke="#d3caae" stroke-width="1">
    <path d="M-210 -70H210M-210 -20H210M-210 30H210M-210 80H210"/>
    <path d="M-140 -120V130M-70 -120V130M0 -120V130M70 -120V130M140 -120V130"/>
  </g>
  <g fill="none" stroke-linecap="round" stroke-width="7">
    <path class="ss-line" d="M-185 60 C-140 60 -120 -40 -70 -40 S 10 40 60 10 S 140 -80 190 -60" stroke="#e8875b"/>
    <path class="ss-line" d="M-180 -85 H-60" stroke="#3f8f8a"/>
    <path class="ss-line" d="M-30 95 L40 -5" stroke="#c45b8a"/>
    <path class="ss-chord" data-x="90" d="M90 100 V20" stroke="#7a9b3c"/>
    <path class="ss-chord" data-x="110" d="M110 100 V40" stroke="#7a9b3c"/>
    <path class="ss-chord" data-x="130" d="M130 100 V10" stroke="#7a9b3c"/>
  </g>
  <g class="ss-head" style="transform:translateX(calc(var(--phase,0) * 340px - 170px));">
  <rect x="-8" y="-128" width="16" height="266" rx="8" fill="var(--accent)" opacity=".35"/>
  <rect x="-2" y="-128" width="4" height="266" fill="var(--accent)"/>
  </g>
  <circle class="ss-hit" cx="0" cy="0" r="8" fill="#fff" stroke="var(--accent)" stroke-width="3.5" style="display:none"/>
  <circle class="ss-hit" cx="0" cy="0" r="8" fill="#fff" stroke="var(--accent)" stroke-width="3.5" style="display:none"/>
  <circle class="ss-hit" cx="0" cy="0" r="8" fill="#fff" stroke="var(--accent)" stroke-width="3.5" style="display:none"/>

</g>
<g fill="var(--accent)" opacity=".8" style="transform:translateY(calc(var(--phase,0) * -40px));">
  <path d="M500 70 q10 -20 20 0 v28 a8 8 0 1 1 -4 -7 v-17" />
  <path d="M80 250 q8 -16 16 0 v22 a7 7 0 1 1 -4 -6 v-12"/>
</g>""", "ShapeSound")

# 郝哥快跑：三车道 + 西瓜 + 障碍
haoge = _svg(f"""
{_SHADOW}
<path d="M250 70 H350 L560 320 H40 Z" fill="#3a3530"/>
<path d="M250 70 H350 L560 320 H40 Z" fill="none" stroke="#5a5048" stroke-width="3"/>
<g stroke="#e9e3cf" stroke-width="4" stroke-dasharray="18 16" opacity=".7" style="stroke-dashoffset:calc(var(--phase,0) * -170)">
  <path d="M283 72 L180 318"/><path d="M317 72 L420 318"/>
</g>
<g style="transform:translateY(calc(var(--phase,0) * 46px)) scale(calc(1 + var(--phase,0) * .12));transform-box:fill-box;transform-origin:center;">
  <rect x="268" y="120" width="30" height="22" rx="3" fill="#8a6d4f"/>
  <rect x="380" y="200" width="56" height="40" rx="4" fill="#8a6d4f"/><rect x="380" y="200" width="56" height="10" fill="#a8875f"/>
  <rect x="120" y="230" width="70" height="20" rx="4" fill="#c4432b"/>
</g>
<g transform="translate(300 255)"><g style="transform:translateY(calc(sin(var(--phase,0) * 6.283rad * 2) * -10px)) rotate(calc(sin(var(--phase,0) * 6.283rad) * 6deg));">
  <path d="M-62 0 A62 62 0 0 0 62 0 Z" fill="#2f7d4f"/>
  <path d="M-52 0 A52 52 0 0 0 52 0 Z" fill="#e9f0d0"/>
  <path d="M-46 0 A46 46 0 0 0 46 0 Z" fill="var(--accent)"/>
  <g fill="#1c2230"><ellipse cx="-22" cy="14" rx="3" ry="5"/><ellipse cx="0" cy="24" rx="3" ry="5"/><ellipse cx="22" cy="14" rx="3" ry="5"/><ellipse cx="-10" cy="34" rx="3" ry="5"/><ellipse cx="12" cy="34" rx="3" ry="5"/></g>
</g></g>
<g stroke="var(--accent)" stroke-width="4" stroke-linecap="round" opacity=".7" style="transform:translateX(calc(var(--phase,0) * -30px));">
  <path d="M470 120 H540"/><path d="M490 145 H570"/><path d="M60 140 H120"/><path d="M40 165 H100"/>
</g>""", "Run Haoge Run")

# 模拟指挥：摄像头取景框 + 双手骨架 + 声波
_hand = lambda x, flip, mv: f"""
<g style="transform:translateY(calc(sin(var(--phase,0) * 6.283rad * 1.5) * {mv}px))"><g transform="translate({x} 175) scale({flip} 1)" fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round">
  <path d="M0 60 L0 10 M0 10 L-22 -30 M0 10 L-6 -46 M0 10 L10 -44 M0 10 L24 -34 M0 40 L-30 20"/>
  <g fill="#eceee0" stroke="none">
    <circle cx="0" cy="60" r="6"/><circle cx="0" cy="10" r="6"/><circle cx="-22" cy="-30" r="5"/><circle cx="-6" cy="-46" r="5"/>
    <circle cx="10" cy="-44" r="5"/><circle cx="24" cy="-34" r="5"/><circle cx="-30" cy="20" r="5"/>
  </g>
</g></g>"""
gesture = _svg(f"""
{_SHADOW}
<rect x="90" y="40" width="420" height="250" rx="16" fill="#18241f" stroke="#3a4a40" stroke-width="2"/>
<g stroke="#eceee0" stroke-width="4" fill="none" stroke-linecap="round">
  <path d="M110 80 V60 H130"/><path d="M470 60 H490 V80"/><path d="M110 250 V270 H130"/><path d="M470 270 H490 V250"/>
</g>
<circle cx="490" cy="54" r="5" fill="#e8736b"/>
{_hand(200, 1, -22)}
{_hand(400, -1, 22)}
<g fill="none" stroke="var(--accent)" stroke-width="2.5" opacity=".6" style="transform:scale(calc(.85 + var(--phase,0) * .35));transform-origin:300px 130px">
  <path d="M260 120 q40 -40 80 0"/><path d="M245 100 q55 -60 110 0"/><path d="M230 80 q70 -80 140 0"/>
</g>
<g fill="var(--accent)" style="transform:scaleY(calc(.6 + sin(var(--phase,0) * 6.283rad * 3) * .35 + .35));transform-origin:300px 316px">
  <rect x="215" y="300" width="14" height="16" rx="2"/><rect x="237" y="290" width="14" height="26" rx="2"/><rect x="259" y="278" width="14" height="38" rx="2"/>
  <rect x="281" y="270" width="14" height="46" rx="2"/><rect x="303" y="282" width="14" height="34" rx="2"/><rect x="325" y="292" width="14" height="24" rx="2"/>
  <rect x="347" y="286" width="14" height="30" rx="2"/><rect x="369" y="298" width="14" height="18" rx="2"/>
</g>""", "Gesture Driven Ensemble")

# 全自动扒谱：波形 → 钢琴卷帘 → 五线谱
_wave = " ".join(f"L{60 + i * 4} {175 + (((i * 37) % 23) - 11) * (1.6 if i % 3 else 3)}" for i in range(36))
_wave2 = " ".join(f"L{200 + i * 4} {175 + (((i * 29) % 19) - 9) * (2 if i % 2 else 2.8)}" for i in range(20))
transcription = _svg(f"""
{_SHADOW}
<rect x="40" y="110" width="160" height="130" rx="12" fill="#18241f" stroke="#3a4a40" stroke-width="2"/>
<clipPath id="wclip"><rect x="48" y="118" width="144" height="114" rx="8"/></clipPath><g clip-path="url(#wclip)"><g style="transform:translateX(calc(var(--phase,0) * -60px))"><path d="M60 175 {_wave}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linejoin="round"/><path d="M200 175 {_wave2}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linejoin="round"/></g></g>
<path d="M210 175 H236" stroke="#eceee0" stroke-width="3" stroke-linecap="round"/><path d="M230 167 L240 175 L230 183" fill="none" stroke="#eceee0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="250" y="110" width="110" height="130" rx="12" fill="#18241f" stroke="#3a4a40" stroke-width="2"/>
<g fill="var(--accent)" opacity=".9" style="transform:translateX(calc(var(--phase,0) * -14px))">
  <rect x="262" y="128" width="30" height="9" rx="2"/><rect x="296" y="146" width="24" height="9" rx="2"/><rect x="270" y="164" width="40" height="9" rx="2"/>
  <rect x="316" y="182" width="32" height="9" rx="2"/><rect x="262" y="200" width="22" height="9" rx="2"/><rect x="290" y="218" width="44" height="9" rx="2"/>
</g>
<path d="M370 175 H396" stroke="#eceee0" stroke-width="3" stroke-linecap="round"/><path d="M390 167 L400 175 L390 183" fill="none" stroke="#eceee0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate(410 90) rotate(3)"><g style="transform:rotate(calc(var(--phase,0) * -5deg)) translateY(calc(var(--phase,0) * -8px));transform-origin:80px 90px">
  <rect width="160" height="180" rx="6" fill="#e9e3cf"/>
  <g stroke="#6b6450" stroke-width="1.4"><path d="M14 50H146M14 60H146M14 70H146M14 80H146M14 90H146"/><path d="M14 120H146M14 130H146M14 140H146M14 150H146M14 160H146"/></g>
  <g fill="#1c2230">
    <g style="opacity:clamp(.15, calc(var(--phase,0) * 7 - 0), 1)"><ellipse cx="40" cy="85" rx="6" ry="4.5" transform="rotate(-20 40 85)"/><path d="M45.5 84 V58" stroke="#1c2230" stroke-width="1.6"/></g>
    <g style="opacity:clamp(.15, calc(var(--phase,0) * 7 - 1), 1)"><ellipse cx="66" cy="75" rx="6" ry="4.5" transform="rotate(-20 66 75)"/><path d="M71.5 74 V48" stroke="#1c2230" stroke-width="1.6"/></g>
    <g style="opacity:clamp(.15, calc(var(--phase,0) * 7 - 2), 1)"><ellipse cx="92" cy="70" rx="6" ry="4.5" transform="rotate(-20 92 70)"/><path d="M97.5 69 V43" stroke="#1c2230" stroke-width="1.6"/></g>
    <g style="opacity:clamp(.15, calc(var(--phase,0) * 7 - 3), 1)"><ellipse cx="118" cy="80" rx="6" ry="4.5" transform="rotate(-20 118 80)"/><path d="M123.5 79 V53" stroke="#1c2230" stroke-width="1.6"/></g>
    <g style="opacity:clamp(.15, calc(var(--phase,0) * 7 - 4), 1)"><ellipse cx="52" cy="155" rx="6" ry="4.5" transform="rotate(-20 52 155)"/><path d="M57.5 154 V128" stroke="#1c2230" stroke-width="1.6"/></g>
    <g style="opacity:clamp(.15, calc(var(--phase,0) * 7 - 5), 1)"><ellipse cx="104" cy="150" rx="6" ry="4.5" transform="rotate(-20 104 150)"/><path d="M109.5 149 V123" stroke="#1c2230" stroke-width="1.6"/></g>
  </g>
  <text x="80" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#1c2230">MusicXML</text>
</g></g>""", "Auto Transcription")

# QQ 机器人小瓜：西瓜角色 + 聊天气泡
qqbot = _svg(f"""
{_SHADOW}
<g transform="translate(300 235)"><g style="transform:rotate(calc(sin(var(--phase,0) * 6.283rad) * 7deg))">
  <path d="M-110 0 A110 110 0 0 0 110 0 Z" fill="#2f7d4f"/>
  <path d="M-96 0 A96 96 0 0 0 96 0 Z" fill="#e9f0d0"/>
  <path d="M-86 0 A86 86 0 0 0 86 0 Z" fill="#e8736b"/>
  <path d="M-110 0 H110" stroke="#24603c" stroke-width="4"/>
  <g fill="#1c2230"><circle cx="-30" cy="26" r="9"/><circle cx="30" cy="26" r="9"/></g>
  <g fill="#fff"><circle cx="-27" cy="23" r="3"/><circle cx="33" cy="23" r="3"/></g>
  <path d="M-12 46 q12 12 24 0" fill="none" stroke="#1c2230" stroke-width="4" stroke-linecap="round"/>
  <g fill="#1c2230" opacity=".8"><ellipse cx="-56" cy="40" rx="3" ry="5"/><ellipse cx="56" cy="40" rx="3" ry="5"/><ellipse cx="-40" cy="64" rx="3" ry="5"/><ellipse cx="40" cy="64" rx="3" ry="5"/></g>
  <g fill="#f4a6a0" opacity=".8"><ellipse cx="-58" cy="18" rx="10" ry="5"/><ellipse cx="58" cy="18" rx="10" ry="5"/></g>
</g></g>
<g>
  <g style="transform:translateY(calc(var(--phase,0) * -22px))"><path d="M70 70 h150 a14 14 0 0 1 14 14 v40 a14 14 0 0 1 -14 14 h-110 l-22 18 v-18 h-18 a14 14 0 0 1 -14 -14 v-40 a14 14 0 0 1 14 -14z" fill="#eceee0"/>
  <g fill="#1c2230"><circle cx="120" cy="104" r="6" style="opacity:calc(.3 + var(--phase,0) * 2.1)"/><circle cx="145" cy="104" r="6" style="opacity:calc(var(--phase,0) * 2.1 - .3)"/><circle cx="170" cy="104" r="6" style="opacity:calc(var(--phase,0) * 2.1 - .9)"/></g></g>
  <g style="transform:translateY(calc(var(--phase,0) * -34px))"><path d="M380 50 h140 a14 14 0 0 1 14 14 v44 a14 14 0 0 1 -14 14 h-18 v18 l-22 -18 h-100 a14 14 0 0 1 -14 -14 v-44 a14 14 0 0 1 14 -14z" fill="var(--accent)"/>
  <path d="M412 78 h92 M412 96 h60" stroke="#10201a" stroke-width="6" stroke-linecap="round"/></g>
  <path style="transform:translateY(calc(var(--phase,0) * -30px)) scale(calc(.8 + var(--phase,0) * .6));transform-box:fill-box;transform-origin:center;" d="M470 175 l10 -10 a8 8 0 0 1 12 12 l-22 22 l-22 -22 a8 8 0 0 1 12 -12z" fill="#e8736b"/>
</g>""", "Xiaogua QQ bot")

# 航空起动/发电：发动机 + 闪电 + 交流→直流
starter = _svg(f"""
{_SHADOW}
<g transform="translate(200 180)">
  <path d="M0 -90 H150 Q200 -90 200 0 Q200 90 150 90 H0 Z" fill="#3b4a44"/>
  <path d="M0 -90 H150 Q200 -90 200 0 Q200 90 150 90 H0 Z" fill="none" stroke="#56685f" stroke-width="3"/>
  <ellipse cx="0" cy="0" rx="40" ry="90" fill="#26322d" stroke="#6d8077" stroke-width="4"/>
  <clipPath id="fanclip"><ellipse cx="0" cy="0" rx="38" ry="88"/></clipPath>
  <g clip-path="url(#fanclip)"><g transform="scale(.44 1)"><g stroke="#9fb1a6" stroke-width="5" stroke-linecap="round" style="transform:rotate(calc(var(--phase,0) * 540deg));transform-origin:0 0">
    <path vector-effect="non-scaling-stroke" d="M0 0 L0 -84 M0 0 L59 -59 M0 0 L84 0 M0 0 L59 59 M0 0 L0 84 M0 0 L-59 59 M0 0 L-84 0 M0 0 L-59 -59"/>
  </g></g></g>
  <circle r="12" fill="var(--accent)"/>
</g>
<path d="M330 60 l-26 52 h22 l-16 46 l44 -62 h-22 l18 -36z" fill="var(--accent)" style="opacity:calc(.45 + ((1 - cos(var(--phase,0) * 6.283rad * 4)) / 2) * .55);transform:scale(calc(.9 + ((1 - cos(var(--phase,0) * 6.283rad * 4)) / 2) * .15));transform-box:fill-box;transform-origin:center;"/>
<rect x="420" y="130" width="130" height="90" rx="10" fill="#18241f" stroke="var(--accent)" stroke-width="2.5"/>
<clipPath id="sclip"><rect x="432" y="140" width="104" height="40"/></clipPath><g clip-path="url(#sclip)"><path style="transform:translateX(calc(var(--phase,0) * -40px))" d="M436 160 q10 -16 20 0 t20 0 t20 0 t20 0 t20 0 t20 0" fill="none" stroke="#eceee0" stroke-width="3"/></g>
<path d="M436 196 H530" stroke="var(--accent)" stroke-width="3"/><path d="M436 206 H530" stroke="var(--accent)" stroke-width="3" stroke-dasharray="8 6"/>
<path d="M400 175 H418" stroke="#eceee0" stroke-width="3"/>""", "Aircraft starter/generator")

# Antigravity 用量面板：一块仪表盘窗口，滚动时柱子长高、圆环转满、曲线画出
dashboard = _svg(f"""
{_SHADOW}
<g transform="translate(300 180) rotate(-3)"><g transform="translate(-235 -140)">
  <rect width="470" height="270" rx="16" fill="#151a26" stroke="#2c3446" stroke-width="2"/>
  <circle cx="22" cy="20" r="4.5" fill="#ea4335"/><circle cx="38" cy="20" r="4.5" fill="#fbbc04"/><circle cx="54" cy="20" r="4.5" fill="#34a853"/>
  <rect x="18" y="38" width="196" height="96" rx="10" fill="#1d2433"/>
  <text x="32" y="62" font-family="Cascadia Mono, Consolas, monospace" font-size="10" fill="#8d96aa">TOTAL TOKENS</text>
  <text x="32" y="104" font-family="Georgia, serif" font-size="36" fill="#eef1f7" class="count" data-from="42.1" data-to="92.0" data-unit="M">42.1M</text>
  <path d="M120 122 C140 120 150 112 162 104 S184 84 200 58" fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round" pathLength="1" stroke-dasharray="1" style="stroke-dashoffset:calc(1 - var(--phase,0) * .9 - .1)"/>
  <rect x="224" y="38" width="110" height="96" rx="10" fill="#1d2433"/>
  <circle cx="279" cy="86" r="28" fill="none" stroke="#2c3446" stroke-width="9"/>
  <circle cx="279" cy="86" r="28" fill="none" stroke="#fbbc04" stroke-width="9" stroke-linecap="round" pathLength="100" stroke-dasharray="100" transform="rotate(-90 279 86)" style="stroke-dashoffset:calc(100 - (25 + var(--phase,0) * 65))"/>
  <rect x="344" y="38" width="108" height="96" rx="10" fill="#1d2433"/>
  <circle cx="398" cy="86" r="28" fill="none" stroke="#2c3446" stroke-width="9"/>
  <circle cx="398" cy="86" r="28" fill="none" stroke="#34a853" stroke-width="9" stroke-linecap="round" pathLength="100" stroke-dasharray="100" transform="rotate(-90 398 86)" style="stroke-dashoffset:calc(100 - (40 + var(--phase,0) * 44))"/>
  <text x="398" y="90" text-anchor="middle" font-family="Cascadia Mono, Consolas, monospace" font-size="11" fill="#eef1f7" class="count" data-from="40" data-to="84" data-dec="0" data-unit="%">40%</text>
  <rect x="18" y="144" width="270" height="110" rx="10" fill="#1d2433"/>
  <g fill="#2c3446"><rect x="32" y="160" width="120" height="8" rx="4"/><rect x="32" y="182" width="200" height="7" rx="3.5"/><rect x="32" y="200" width="170" height="7" rx="3.5"/><rect x="32" y="218" width="214" height="7" rx="3.5"/><rect x="32" y="236" width="150" height="7" rx="3.5"/></g>
  <g style="transform:translateY(calc(var(--phase,0) * 54px))"><rect x="24" y="176" width="258" height="18" rx="5" fill="var(--accent)" opacity=".18"/></g>
  <rect x="298" y="144" width="154" height="110" rx="10" fill="#1d2433"/>
  <g transform="translate(0 -16)"><rect x="312" y="234" width="13" height="28" rx="3" fill="#4285f4" style="transform:scaleY(calc(.25 + var(--phase,0) * .75 + 0.0));transform-box:fill-box;transform-origin:bottom"/><rect x="332" y="218" width="13" height="44" rx="3" fill="#34a853" style="transform:scaleY(calc(.25 + var(--phase,0) * .75 + 0.0));transform-box:fill-box;transform-origin:bottom"/><rect x="352" y="228" width="13" height="34" rx="3" fill="#fbbc04" style="transform:scaleY(calc(.25 + var(--phase,0) * .75 + 0.0));transform-box:fill-box;transform-origin:bottom"/><rect x="372" y="206" width="13" height="56" rx="3" fill="#ea4335" style="transform:scaleY(calc(.25 + var(--phase,0) * .75 + 0.0));transform-box:fill-box;transform-origin:bottom"/><rect x="392" y="222" width="13" height="40" rx="3" fill="#4285f4" style="transform:scaleY(calc(.25 + var(--phase,0) * .75 + 0.0));transform-box:fill-box;transform-origin:bottom"/><rect x="412" y="196" width="13" height="66" rx="3" fill="#34a853" style="transform:scaleY(calc(.25 + var(--phase,0) * .75 + 0.0));transform-box:fill-box;transform-origin:bottom"/><rect x="432" y="182" width="13" height="80" rx="3" fill="#fbbc04" style="transform:scaleY(calc(.25 + var(--phase,0) * .75 + 0.0));transform-box:fill-box;transform-origin:bottom"/></g>
</g></g>""", "Antigravity Usage Dashboard")

# Claude 堡垒：月夜里的城堡，罩在能量护盾中（主楼有 Claude 风格的星芒徽章和牌匾）；滚动时导弹依次飞来，在护盾上爆炸
fortress = _svg(f"""
<defs>
  <linearGradient id="cf-tower" x1="0" x2="1"><stop offset="0" stop-color="#6b7591"/><stop offset=".45" stop-color="#535c76"/><stop offset="1" stop-color="#3a4157"/></linearGradient>
  <linearGradient id="cf-keep" x1="0" x2="1"><stop offset="0" stop-color="#626c88"/><stop offset=".5" stop-color="#4f5872"/><stop offset="1" stop-color="#3b4258"/></linearGradient>
  <linearGradient id="cf-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a536b"/><stop offset="1" stop-color="#363d52"/></linearGradient>
  <linearGradient id="cf-roof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e08a66"/><stop offset="1" stop-color="#8e4f45"/></linearGradient>
  <linearGradient id="cf-hill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27324a"/><stop offset="1" stop-color="#171d2b"/></linearGradient>
  <linearGradient id="cf-door" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffcf7a" stop-opacity=".55"/><stop offset="1" stop-color="#d97757" stop-opacity=".25"/></linearGradient>
  <linearGradient id="cf-metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f4f8"/><stop offset="1" stop-color="#9aa3b8"/></linearGradient>
  <radialGradient id="cf-glow"><stop offset="0" stop-color="#ffcf7a" stop-opacity=".55"/><stop offset="1" stop-color="#ffcf7a" stop-opacity="0"/></radialGradient>
  <radialGradient id="cf-emblem-glow"><stop offset="0" stop-color="#d97757" stop-opacity=".55"/><stop offset="1" stop-color="#d97757" stop-opacity="0"/></radialGradient>
  <radialGradient id="cf-burst"><stop offset="0" stop-color="#ffd98a" stop-opacity=".7"/><stop offset=".6" stop-color="#ef8a6f" stop-opacity=".25"/><stop offset="1" stop-color="#ef8a6f" stop-opacity="0"/></radialGradient>
  <radialGradient id="cf-dome" cx="50%" cy="100%" r="100%"><stop offset="0" stop-color="var(--accent)" stop-opacity="0"/><stop offset=".82" stop-color="var(--accent)" stop-opacity=".07"/><stop offset="1" stop-color="var(--accent)" stop-opacity=".30"/></radialGradient>
  <linearGradient id="cf-flame" x1="1" x2="0"><stop offset="0" stop-color="#fff1c2"/><stop offset=".35" stop-color="#f6a35b"/><stop offset="1" stop-color="#ef8a6f" stop-opacity="0"/></linearGradient>
  <pattern id="cf-hex" width="24" height="41.6" patternUnits="userSpaceOnUse"><path d="M12 0 L24 6.9 V20.8 L12 27.7 L0 20.8 V6.9 Z M12 27.7 V41.6" fill="none" stroke="var(--accent)" stroke-width=".8"/></pattern>
  <mask id="cf-moon"><rect x="60" y="30" width="70" height="70" fill="#fff"/><circle cx="101" cy="56" r="18" fill="#000"/></mask>
  <clipPath id="cf-domeclip"><path d="M72 292 A228 228 0 0 1 528 292 Z"/></clipPath>
  <filter id="cf-soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
{_SHADOW}

  <!-- 夜空 -->
  <circle cx="92" cy="62" r="20" fill="#f3ecd8" opacity=".9" mask="url(#cf-moon)"/>
  <g fill="#e9e4d4"><circle cx="160" cy="40" r="1.4"/><circle cx="455" cy="46" r="1.2"/><circle cx="520" cy="96" r="1.6"/><circle cx="60" cy="140" r="1.1"/><circle cx="545" cy="168" r="1.1"/><circle cx="230" cy="30" r="1"/></g>
  <!-- 山丘 + 小路 -->
  <path d="M64 300 Q170 252 300 262 Q430 252 536 300 Q300 318 64 300 Z" fill="url(#cf-hill)"/>
  <path d="M286 294 L276 312 L324 312 L314 294 Z" fill="#3a4258" opacity=".8"/>
  <!-- 后层城墙 -->
  <rect x="152" y="226" width="296" height="68" fill="url(#cf-wall)"/><rect x="150.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="166.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="182.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="198.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="214.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="230.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="246.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="262.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="278.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="294.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="310.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="326.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="342.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="358.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="374.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="390.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="406.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="422.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/><rect x="438.0" y="218" width="9" height="9" rx="1.2" fill="url(#cf-wall)"/>
  <g stroke="#262c3d" stroke-width="1" opacity=".55"><path d="M152 246 H448 M152 266 H448 M152 284 H448"/>
  <path d="M170 226 v20 M200 246 v20 M230 226 v20 M188 266 v18 M218 266 v18 M378 226 v20 M408 246 v20 M432 226 v20 M392 266 v18 M422 266 v18"/></g>
  
  <rect x="120" y="170" width="58" height="124" fill="url(#cf-tower)"/>
  <rect x="118.0" y="162" width="9" height="9" rx="1.2" fill="url(#cf-tower)"/><rect x="134.0" y="162" width="9" height="9" rx="1.2" fill="url(#cf-tower)"/><rect x="150.0" y="162" width="9" height="9" rx="1.2" fill="url(#cf-tower)"/><rect x="166.0" y="162" width="9" height="9" rx="1.2" fill="url(#cf-tower)"/>
  <rect x="115" y="159" width="68" height="4" rx="1" fill="#5a6480"/>
  <path d="M113 158 L149.0 112 L185 158 Z" fill="url(#cf-roof)"/>
  <path d="M149.0 112 L185 158 L155.0 158 Z" fill="#000" opacity=".18"/>
  <line x1="149.0" y1="112" x2="149.0" y2="90" stroke="#cfd5e2" stroke-width="1.8"/>
  <path d="M149.0 90 q10 -3 20 2 q-8 4 -20 8 Z" fill="#d97757"/>
  <circle cx="149.0" cy="208" r="12" fill="url(#cf-glow)"/><path d="M144.0 214 v-8 a5 5 0 0 1 10 0 v8 Z" fill="#ffd27a"/>
  <rect x="147.5" y="240" width="3" height="16" rx="1.5" fill="#1d2232"/>
  <rect x="422" y="170" width="58" height="124" fill="url(#cf-tower)"/>
  <rect x="420.0" y="162" width="9" height="9" rx="1.2" fill="url(#cf-tower)"/><rect x="436.0" y="162" width="9" height="9" rx="1.2" fill="url(#cf-tower)"/><rect x="452.0" y="162" width="9" height="9" rx="1.2" fill="url(#cf-tower)"/><rect x="468.0" y="162" width="9" height="9" rx="1.2" fill="url(#cf-tower)"/>
  <rect x="417" y="159" width="68" height="4" rx="1" fill="#5a6480"/>
  <path d="M415 158 L451.0 112 L487 158 Z" fill="url(#cf-roof)"/>
  <path d="M451.0 112 L487 158 L457.0 158 Z" fill="#000" opacity=".18"/>
  <line x1="451.0" y1="112" x2="451.0" y2="90" stroke="#cfd5e2" stroke-width="1.8"/>
  <path d="M451.0 90 q10 -3 20 2 q-8 4 -20 8 Z" fill="#d97757"/>
  <circle cx="451.0" cy="208" r="12" fill="url(#cf-glow)"/><path d="M446.0 214 v-8 a5 5 0 0 1 10 0 v8 Z" fill="#ffd27a"/>
  <rect x="449.5" y="240" width="3" height="16" rx="1.5" fill="#1d2232"/>
  <!-- 主楼 -->
  <rect x="244" y="132" width="112" height="162" fill="url(#cf-keep)"/><rect x="242.0" y="124" width="9" height="9" rx="1.2" fill="url(#cf-keep)"/><rect x="258.0" y="124" width="9" height="9" rx="1.2" fill="url(#cf-keep)"/><rect x="274.0" y="124" width="9" height="9" rx="1.2" fill="url(#cf-keep)"/><rect x="290.0" y="124" width="9" height="9" rx="1.2" fill="url(#cf-keep)"/><rect x="306.0" y="124" width="9" height="9" rx="1.2" fill="url(#cf-keep)"/><rect x="322.0" y="124" width="9" height="9" rx="1.2" fill="url(#cf-keep)"/><rect x="338.0" y="124" width="9" height="9" rx="1.2" fill="url(#cf-keep)"/>
  <rect x="280" y="98" width="40" height="36" fill="url(#cf-tower)"/><rect x="278.0" y="90" width="8" height="9" rx="1.2" fill="url(#cf-tower)"/><rect x="292.0" y="90" width="8" height="9" rx="1.2" fill="url(#cf-tower)"/><rect x="306.0" y="90" width="8" height="9" rx="1.2" fill="url(#cf-tower)"/>
  <line x1="300" y1="90" x2="300" y2="66" stroke="#cfd5e2" stroke-width="2"/><path d="M300 66 q13 -4 26 2 q-10 5 -26 10 Z" fill="#d97757"/>
  <g stroke="#2a3043" stroke-width="1" opacity=".5"><path d="M244 196 H356 M244 238 H356 M244 268 H276 M324 268 H356"/></g>
  <!-- Claude 徽章 -->
  <circle cx="300" cy="164" r="26" fill="url(#cf-emblem-glow)"/>
  <circle cx="300" cy="164" r="17" fill="#232a3b" stroke="#d97757" stroke-width="2"/>
  <g stroke="#f4a882" stroke-width="3" stroke-linecap="round" filter="url(#cf-soft)"><path d="M300.0 161.0 L300.0 152.5"/><path d="M302.1 161.9 L306.7 157.3"/><path d="M303.0 164.0 L311.5 164.0"/><path d="M302.1 166.1 L306.7 170.7"/><path d="M300.0 167.0 L300.0 175.5"/><path d="M297.9 166.1 L293.3 170.7"/><path d="M297.0 164.0 L288.5 164.0"/><path d="M297.9 161.9 L293.3 157.3"/></g>
  <g><circle cx="270" cy="214" r="10" fill="url(#cf-glow)"/><circle cx="330" cy="214" r="10" fill="url(#cf-glow)"/>
  <path d="M265 219 v-8 a5 5 0 0 1 10 0 v8 Z M325 219 v-8 a5 5 0 0 1 10 0 v8 Z" fill="#ffd27a"/></g>
  <!-- 牌匾 + 城门 -->
  <rect x="261" y="228" width="78" height="18" rx="2.5" fill="#232a3b" stroke="#d97757" stroke-width="1.4"/>
  <text x="300" y="241" text-anchor="middle" font-family="Georgia, serif" font-size="11.5" letter-spacing="2.6" fill="#f4a882">CLAUDE</text>
  <path d="M278 294 V268 a22 22 0 0 1 44 0 V294 Z" fill="#1a1f2d"/>
  <path d="M278 294 V268 a22 22 0 0 1 44 0 V294" fill="none" stroke="#6d7690" stroke-width="2.5"/>
  <path d="M282 294 V268 a18 18 0 0 1 36 0 V294 Z" fill="url(#cf-door)"/>
  <g stroke="#5d667d" stroke-width="1.6"><path d="M288 256 V294 M296 251 V294 M304 251 V294 M312 256 V294 M283 270 H317 M283 284 H317"/></g>

<g style="opacity:calc(.35 + .65 * clamp(0, var(--phase,0) * 4, 1))">
  <path d="M72 292 A228 228 0 0 1 528 292 Z" fill="url(#cf-dome)"/>
  <rect x="72" y="64" width="456" height="228" fill="url(#cf-hex)" opacity=".16" clip-path="url(#cf-domeclip)"/>
  <path d="M72 292 A228 228 0 0 1 528 292" fill="none" stroke="var(--accent)" stroke-width="6" opacity=".25" filter="url(#cf-soft)"/>
  <path d="M72 292 A228 228 0 0 1 528 292" fill="none" stroke="var(--accent)" stroke-width="2.2"/>
  <path d="M98 292 A202 202 0 0 1 502 292" fill="none" stroke="var(--accent)" stroke-width="1" opacity=".25" stroke-dasharray="2 6"/>
</g>
<g style="transform:translate(calc((-20 + 122.5 * clamp(0, (var(--phase,0) - 0.04) / 0.27, 1)) * 1px), calc((20 + 158.0 * clamp(0, (var(--phase,0) - 0.04) / 0.27, 1)) * 1px)) rotate(52.2deg) scale(1.25);opacity:calc(clamp(0, (var(--phase,0) - 0.04) * 40, 1) - clamp(0, (var(--phase,0) - 0.306) * 200, 1))">
  <circle cx="-70" cy="0" r="5" fill="#9aa3b8" opacity=".18"/><circle cx="-84" cy="1" r="6.5" fill="#9aa3b8" opacity=".12"/><circle cx="-100" cy="-1" r="8" fill="#9aa3b8" opacity=".07"/>
  <path d="M-16 0 L-62 -5 Q-66 0 -62 5 Z" fill="url(#cf-flame)"/>
  <rect x="-18" y="-4.2" width="22" height="8.4" rx="3.5" fill="url(#cf-metal)"/><path d="M4 -4.2 Q14 0 4 4.2 Z" fill="#ef8a6f"/>
  <path d="M-17 -4 L-24 -10 L-11 -4 Z M-17 4 L-24 10 L-11 4 Z" fill="#8a93a8"/></g>
<g style="transform:translate(calc((620 + -220.1 * clamp(0, (var(--phase,0) - 0.27) / 0.27, 1)) * 1px), calc((-10 + 97.1 * clamp(0, (var(--phase,0) - 0.27) / 0.27, 1)) * 1px)) rotate(156.2deg) scale(1.25);opacity:calc(clamp(0, (var(--phase,0) - 0.27) * 40, 1) - clamp(0, (var(--phase,0) - 0.536) * 200, 1))">
  <circle cx="-70" cy="0" r="5" fill="#9aa3b8" opacity=".18"/><circle cx="-84" cy="1" r="6.5" fill="#9aa3b8" opacity=".12"/><circle cx="-100" cy="-1" r="8" fill="#9aa3b8" opacity=".07"/>
  <path d="M-16 0 L-62 -5 Q-66 0 -62 5 Z" fill="url(#cf-flame)"/>
  <rect x="-18" y="-4.2" width="22" height="8.4" rx="3.5" fill="url(#cf-metal)"/><path d="M4 -4.2 Q14 0 4 4.2 Z" fill="#ef8a6f"/>
  <path d="M-17 -4 L-24 -10 L-11 -4 Z M-17 4 L-24 10 L-11 4 Z" fill="#8a93a8"/></g>
<g style="transform:translate(calc((650 + -141.7 * clamp(0, (var(--phase,0) - 0.5) / 0.27, 1)) * 1px), calc((150 + 49.3 * clamp(0, (var(--phase,0) - 0.5) / 0.27, 1)) * 1px)) rotate(160.8deg) scale(1.25);opacity:calc(clamp(0, (var(--phase,0) - 0.5) * 40, 1) - clamp(0, (var(--phase,0) - 0.766) * 200, 1))">
  <circle cx="-70" cy="0" r="5" fill="#9aa3b8" opacity=".18"/><circle cx="-84" cy="1" r="6.5" fill="#9aa3b8" opacity=".12"/><circle cx="-100" cy="-1" r="8" fill="#9aa3b8" opacity=".07"/>
  <path d="M-16 0 L-62 -5 Q-66 0 -62 5 Z" fill="url(#cf-flame)"/>
  <rect x="-18" y="-4.2" width="22" height="8.4" rx="3.5" fill="url(#cf-metal)"/><path d="M4 -4.2 Q14 0 4 4.2 Z" fill="#ef8a6f"/>
  <path d="M-17 -4 L-24 -10 L-11 -4 Z M-17 4 L-24 10 L-11 4 Z" fill="#8a93a8"/></g>
<g transform="translate(102.5 178.0)"><g style="opacity:calc(clamp(0, (var(--phase,0) - 0.305) * 60, 1) - clamp(0, (var(--phase,0) - 0.340) * 7, 1));transform:scale(calc(.35 + 1.1 * clamp(0, (var(--phase,0) - 0.305) * 7, 1)))">
  <circle r="40" fill="url(#cf-burst)"/><circle r="32" fill="none" stroke="var(--accent)" stroke-width="2.5" opacity=".9"/>
  <circle r="15" fill="#ef8a6f"/><circle r="8" fill="#fff6dc"/><path d="M9.0 0.0 L34.0 0.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M7.8 4.5 L24.2 14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M4.5 7.8 L14.0 24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M0.0 9.0 L0.0 34.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-4.5 7.8 L-14.0 24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-7.8 4.5 L-24.2 14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-9.0 0.0 L-34.0 0.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-7.8 -4.5 L-24.2 -14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-4.5 -7.8 L-14.0 -24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-0.0 -9.0 L-0.0 -34.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M4.5 -7.8 L14.0 -24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M7.8 -4.5 L24.2 -14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/></g></g>
<g transform="translate(399.9 87.1)"><g style="opacity:calc(clamp(0, (var(--phase,0) - 0.535) * 60, 1) - clamp(0, (var(--phase,0) - 0.570) * 7, 1));transform:scale(calc(.35 + 1.1 * clamp(0, (var(--phase,0) - 0.535) * 7, 1)))">
  <circle r="40" fill="url(#cf-burst)"/><circle r="32" fill="none" stroke="var(--accent)" stroke-width="2.5" opacity=".9"/>
  <circle r="15" fill="#ef8a6f"/><circle r="8" fill="#fff6dc"/><path d="M9.0 0.0 L34.0 0.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M7.8 4.5 L24.2 14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M4.5 7.8 L14.0 24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M0.0 9.0 L0.0 34.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-4.5 7.8 L-14.0 24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-7.8 4.5 L-24.2 14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-9.0 0.0 L-34.0 0.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-7.8 -4.5 L-24.2 -14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-4.5 -7.8 L-14.0 -24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-0.0 -9.0 L-0.0 -34.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M4.5 -7.8 L14.0 -24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M7.8 -4.5 L24.2 -14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/></g></g>
<g transform="translate(508.3 199.3)"><g style="opacity:calc(clamp(0, (var(--phase,0) - 0.765) * 60, 1) - clamp(0, (var(--phase,0) - 0.800) * 7, 1));transform:scale(calc(.35 + 1.1 * clamp(0, (var(--phase,0) - 0.765) * 7, 1)))">
  <circle r="40" fill="url(#cf-burst)"/><circle r="32" fill="none" stroke="var(--accent)" stroke-width="2.5" opacity=".9"/>
  <circle r="15" fill="#ef8a6f"/><circle r="8" fill="#fff6dc"/><path d="M9.0 0.0 L34.0 0.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M7.8 4.5 L24.2 14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M4.5 7.8 L14.0 24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M0.0 9.0 L0.0 34.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-4.5 7.8 L-14.0 24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-7.8 4.5 L-24.2 14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-9.0 0.0 L-34.0 0.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-7.8 -4.5 L-24.2 -14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-4.5 -7.8 L-14.0 -24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M-0.0 -9.0 L-0.0 -34.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M4.5 -7.8 L14.0 -24.2" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/><path d="M7.8 -4.5 L24.2 -14.0" stroke="#ffd98a" stroke-width="2.2" stroke-linecap="round"/></g></g>
""", "Claude Fortress")

ART = {
    "shapesound": shapesound, "run-haoge-run": haoge, "gesture-conductor": gesture,
    "auto-transcription": transcription, "qq-bot": qqbot, "starter-generator": starter,
    "usage-dashboard": dashboard, "claude-fortress": fortress,
}
