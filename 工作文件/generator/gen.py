"""Rose 个人网站生成器：python 工作文件/generator/gen.py 会重新生成首页、关于、项目目录和所有项目详情页。
文章（writing/）是手写页面，不由本脚本生成。改这些页面请改本脚本后重新生成，不要直接改 HTML，否则下次生成会被覆盖。"""
"""一次性生成静态页面（不放进网站仓库，生成后的 HTML 可以直接手改）。"""
import training
import os
import json
from art import ART

# 输出目录：默认是网站仓库根目录（本文件在 工作文件/generator/ 下），也可用环境变量 SITE_ROOT 指定
ROOT = os.environ.get("SITE_ROOT") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GH = "https://github.com/Rose-MYS"


def B(zh, en, tag="span", cls=""):
    c = f" {cls}" if cls else ""
    return f'<{tag} class="zh{c}">{zh}</{tag}><{tag} class="en{c}">{en}</{tag}>'


def page(path, depth, title_zh, title_en, current, body, desc_zh, body_cls=""):
    up = "../" * depth
    nav = [("", "首页", "Home", "home"), ("about/", "关于", "About", "about"), ("projects/", "项目", "Projects", "projects"), ("writing/", "文章", "Writing", "writing")]
    links = "".join(
        f'<a href="{up}{h}"{" aria-current=\"page\"" if k == current else ""}>{B(z, e)}</a>' for h, z, e, k in nav
    )
    html = f"""<!DOCTYPE html>
<html lang="en" data-lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_en}</title>
<meta name="title-zh" content="{title_zh}">
<meta name="title-en" content="{title_en}">
<meta name="description" content="{desc_zh}">
<meta name="theme-color" content="#10131c">
<link rel="icon" href="{up}assets/favicon.svg?v=202611271640" type="image/svg+xml">
<link rel="stylesheet" href="{up}assets/style.css?v=202611271640">
<script src="{up}assets/site.js?v=202611271640"></script>
<script data-goatcounter="https://rose-mys.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</head>
<body class="{body_cls}">
<header class="mast">
  <div class="wrap">
    <a class="brand" href="{up}"><svg class="brand-mark" width="30" height="30" viewBox="10 8 44 50" aria-hidden="true"><path d="M32 33 c3 0 4 -3 2 -5 c-3 -3 -8 0 -8 4 c0 6 7 9 12 6 c6 -4 5 -13 -1 -16 c-8 -4 -17 2 -17 10 c0 10 9 16 18 14" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round"/><path d="M32 46 V56" stroke="#7fbf8a" stroke-width="3.6" stroke-linecap="round"/><path d="M32 52 q-6 -1 -8 -6 q6 0 8 6z" fill="#7fbf8a"/></svg>Rose</a>
    <nav class="nav">{links}</nav>
    <div class="mast-tools"><button class="theme-btn" type="button" aria-label="Switch light or dark theme" title="Switch theme"><svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4L6 18M18 6l1.4-1.4"/></svg><svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg></button><button class="lang-btn" type="button" aria-label="Switch language" title="Switch language"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9M12 3c-2.6 2.6-3.8 5.6-3.8 9s1.2 6.4 3.8 9"/></svg><span class="lang-code">EN</span></button></div>
  </div>
</header>
<main>
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <span>© 2026 Rose</span>
    <span>{B('纯手写 HTML / CSS / JS · 托管于 GitHub Pages', 'Hand-written HTML / CSS / JS · Hosted on GitHub Pages')} · <a href="{GH}">GitHub ↗</a></span>
  </div>
</footer>
</body>
</html>
"""
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


AFE_SVG = """<svg viewBox="0 0 720 345" role="img" aria-label="AFE topology" xmlns="http://www.w3.org/2000/svg">
<g fill="none" stroke="#1c2230" stroke-width="2" stroke-linejoin="round">
  <path d="M20 200 V280"/>
  <path d="M20 200 H36 M64 200 H110 M170 200 H230 V120 H260"/>
  <path d="M20 240 H36 M64 240 H110 M170 240 H300 V120 H330"/>
  <path d="M20 280 H36 M64 280 H110 M170 280 H370 V120 H400"/>
  <circle cx="50" cy="200" r="14"/><circle cx="50" cy="240" r="14"/><circle cx="50" cy="280" r="14"/>
  <path d="M42 200 q4 -6 8 0 t8 0 M42 240 q4 -6 8 0 t8 0 M42 280 q4 -6 8 0 t8 0" stroke-width="1.6"/>
  <path d="M110 200 q7.5 -12 15 0 t15 0 t15 0 t15 0 M110 240 q7.5 -12 15 0 t15 0 t15 0 t15 0 M110 280 q7.5 -12 15 0 t15 0 t15 0 t15 0"/>
  <path d="M260 40 V310 M330 40 V310 M400 40 V310"/>
  <path d="M260 40 H600 M260 310 H600"/>
  <path d="M500 40 V168 M500 182 V310"/>
  <path d="M484 168 H516 M484 182 H516" stroke-width="3"/>
  <path d="M600 40 V135 M600 310 V215"/>
</g>
<g fill="#fbf8f1" stroke="#1c2230" stroke-width="2">
  <rect x="246" y="55" width="28" height="40" rx="3"/><rect x="316" y="55" width="28" height="40" rx="3"/><rect x="386" y="55" width="28" height="40" rx="3"/>
  <rect x="246" y="145" width="28" height="40" rx="3"/><rect x="316" y="145" width="28" height="40" rx="3"/><rect x="386" y="145" width="28" height="40" rx="3"/>
  <rect x="560" y="135" width="140" height="80" rx="6" stroke="#c4432b"/>
</g>
<g fill="#1c2230">
  <circle cx="260" cy="120" r="4"/><circle cx="330" cy="120" r="4"/><circle cx="400" cy="120" r="4"/>
  <circle cx="500" cy="40" r="4"/><circle cx="500" cy="310" r="4"/><circle cx="20" cy="240" r="4"/>
</g>
<g font-family="Consolas, monospace" font-size="13" fill="#1c2230" text-anchor="middle">
  <text x="260" y="80">S1</text><text x="330" y="80">S3</text><text x="400" y="80">S5</text>
  <text x="260" y="170">S4</text><text x="330" y="170">S6</text><text x="400" y="170">S2</text>
  <text x="140" y="186">L</text><text x="140" y="226">L</text><text x="140" y="266">L</text>
  <text x="86" y="193">e<tspan font-size="10" dy="3">a</tspan></text><text x="86" y="233">e<tspan font-size="10" dy="3">b</tspan></text><text x="86" y="273">e<tspan font-size="10" dy="3">c</tspan></text>
  <text x="524" y="179" text-anchor="start">C</text>
  <text x="472" y="115">+</text><text x="472" y="245">&#8722;</text>
  <text x="458" y="179">U<tspan font-size="10" dy="3">dc</tspan></text>
</g>
<g font-size="13" fill="#4a5263" text-anchor="middle">
  <text x="85" y="335" class="zh">三相交流侧</text><text x="85" y="335" class="en">3-phase AC side</text>
  <text x="330" y="335" class="zh">六开关三桥臂</text><text x="330" y="335" class="en">6-switch bridge</text>
  <text x="500" y="335" class="zh">直流母线</text><text x="500" y="335" class="en">DC link</text>
  <text x="630" y="170" fill="#c4432b" class="zh">机侧变流器</text><text x="630" y="170" fill="#c4432b" class="en">Machine-side</text>
  <text x="630" y="190" fill="#c4432b" class="zh">起动/发电机</text><text x="630" y="190" fill="#c4432b" class="en">converter + S/G</text>
</g>
</svg>"""


READING = [
    ("https://imperix.com/doc/TN166", "Active Front End (AFE)", "imperix · Technical note",
     ("AFE 的工作原理、典型拓扑和直流母线预充电。", "How an AFE works, its typical topology and DC-bus pre-charging.")),
    ("https://www.mathworks.com/help/sps/ug/grid-connected-rectifier.html", "Three-Phase Grid-Connected Rectifier Control", "MathWorks · Simscape example",
     ("用 PI 级联控制稳定直流母线电压的 Simulink 示例。", "A Simulink example that regulates the DC-link voltage with cascaded PI control.")),
    ("https://www.mathworks.com/help/sps/ref/pfcrectifiercontrollerthreephase.html", "PFC Rectifier Controller (Three-Phase)", "MathWorks · Block reference",
     ("三相 PFC 整流控制器模块：内置锁相环，dq 轴电流控制。", "Three-phase PFC rectifier controller block with a built-in PLL and dq-axis current control.")),
    ("https://doi.org/10.3384/ecp11063388", "Modeling a Mains Connected PWM Converter with Voltage-Oriented Control", "Haumer & Kral · Modelica Conference 2011",
     ("讲解电压定向控制（VOC）下 AFE 的建模与参数设计。", "Modelling and tuning an AFE under voltage-oriented control (VOC).")),
    ("https://doi.org/10.1109/ACCESS.2020.3007791", "High-Power Machines and Starter-Generator Topologies for More Electric Aircraft", "Nøland et al. · IEEE Access 2020 (open access)",
     ("多电飞机中大功率电机与起动/发电机拓扑的综述。", "A review of high-power machines and starter/generator topologies for more-electric aircraft.")),
    ("https://aperta.ulakbim.gov.tr/record/260281", "A Review of Conventional and New-Generation Aircraft Starter/Generators", "Oksuztepe, Kaya & Kurum · open access",
     ("从电驱动角度对比传统与新一代飞机起动/发电机。", "Compares conventional and new-generation aircraft starter/generators from an electric-drive perspective.")),
]


def reading_html():
    items = "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a> <span class="src">{src}</span><br>{B(*note)}</li>' for u, t, src, note in READING)
    return (f"<h2>{B('延伸阅读', 'Further reading')}</h2>"
            f"<p class=\"muted\">{B('以下是公开的外部资料，供了解相关背景，与本项目的模型无直接关联。', 'Public external resources for background; they are not part of this project’s model.')}</p>"
            f'<ul class="reading">{items}</ul>')

# ---------- 项目数据 ----------
P = [
    dict(
        slug="shapesound", color="var(--accent)",
        cat=("网页乐器", "Web instrument"), status=("可玩", "Playable"), live=True,
        date="2026-11-18",
        name=("形声 ShapeSound", "ShapeSound"), sub=("画出来的音乐", "形声 · Music you can draw"),
        desc=("在纸上画线，播放头扫过就发声：线越高音越高，颜色就是乐器。16 种实时合成音色、11 首示例曲，还能导入谱子、把照片描成会响的画。",
              "Draw lines on paper and a playhead turns them into sound: height is pitch, colour is instrument. 16 synthesised instruments, 11 demo songs, score import and photo-to-line tracing."),
        play="projects/shapesound/play/", repo=f"{GH}/ShapeSound",
    ),
    dict(
        slug="run-haoge-run", color="var(--accent-2)",
        cat=("3D 网页游戏", "3D web game"), status=("可玩", "Playable"), live=True,
        date="2026-08-07",
        name=("郝哥快跑", "Run Haoge Run"), sub=("Run Haoge Run", "郝哥快跑"),
        desc=("一款 3D 三车道追逃游戏：郝哥从菜市场一路跑过老街和后巷，完成每一段的目标、抵达出口。躲障碍、收西瓜，用「保熟」技能甩开追兵。",
              "A 3D three-lane chase game: Haoge runs from the market through an old street and a back alley, clearing each segment’s goal to reach the exit. Dodge obstacles, grab watermelons and use the “Baoshu” skill to shake off the chaser."),
        play="https://rose-mys.github.io/run-haoge-run/", repo=f"{GH}/run-haoge-run",
    ),
    dict(
        slug="gesture-conductor", color="#8a5a2b",
        cat=("数字交互 · 比赛", "Interaction · Competition"), status=("团队项目 · 进行中", "Team · Ongoing"), live=False,
        date="2026-10-29",
        name=("模拟指挥", "Gesture Driven Ensemble"), sub=("Gesture Driven Ensemble", "模拟指挥"),
        desc=("东南大学第一届新生 AI 创客大赛参赛作品。站在摄像头前，用双手像指挥家一样控制一支乐队的速度与音量。",
              "Our entry for the 1st SEU Freshman AI Maker Competition. Stand in front of a camera and conduct a band with your hands — tempo and volume follow your gestures."),
        play=None, repo=None,
    ),
    dict(
        slug="auto-transcription", color="#6a4c93",
        cat=("音频 AI · 扒谱", "Audio AI · Transcription"), status=("进行中", "In progress"), live=False,
        date="2026-11-21",
        name=("全自动扒谱", "Auto Transcription"), sub=("录音 → 五线谱 + 简谱", "全自动扒谱 · Audio to sheet music"),
        desc=("把钢琴曲或单旋律录音自动转成能直接导入打谱软件的五线谱（MusicXML）、量化 MIDI 和简谱。在 16 首测试曲上调号与拍号全部识别正确。",
              "Turns piano or single-melody recordings into clean sheet music (MusicXML), quantised MIDI and numbered notation. Key and time signatures are correct on all 16 test pieces."),
        play=None, repo=None,
    ),
    dict(
        slug="qq-bot", color="#2f7d4f",
        cat=("AI 应用 · 聊天机器人", "AI app · Chatbot"), status=("长期运行", "Running"), live=False,
        date="2026-10-24",
        name=("QQ 机器人「小瓜」", "Xiaogua QQ Bot"), sub=("DeepSeek 接入 QQ", "小瓜 · DeepSeek on QQ"),
        desc=("接入 DeepSeek 等大模型的 QQ 群聊机器人：有人格、有情绪、有长期记忆，会看图、会斗图，还能自己学新梗、写周记，掉线了能自愈。",
              "A QQ group-chat bot powered by DeepSeek and other LLMs — with personas, moods and long-term memory. It reads images, trades memes, picks up new slang, writes a weekly diary and recovers from disconnects on its own."),
        play=None, repo=None,
    ),
    dict(
        slug="starter-generator", color="#3b4f7a",
        cat=("电力电子仿真", "Power electronics"), status=("已完成", "Completed"), live=False,
        date="2026-11-17",
        name=("航空起动/发电系统仿真", "Aircraft Starter/Generator Simulation"), sub=("Aircraft starter/generator · Simulink", "航空起动/发电系统仿真 · Simulink"),
        desc=("在 MATLAB/Simulink 中搭建的航空大功率起动/发电系统模型，网侧采用三相两电平六开关 AFE 变流器。项目已完成并交付。",
              "A MATLAB/Simulink model of a high-power aircraft starter/generator system, with a three-phase two-level six-switch active front end (AFE) on the grid side. Completed and delivered."),
        play=None, repo=None,
    ),
    dict(
        slug="usage-dashboard", color="#4285f4",
        cat=("开发者工具 · 本地面板", "Dev tool · Local dashboard"), status=("可用 · v1.1", "Usable · v1.1"), live=False,
        date="2026-11-25",
        name=("Antigravity 用量面板", "Antigravity Usage Dashboard"), sub=("Antigravity Usage Dashboard", "Antigravity 用量面板"),
        desc=("一个本地运行的网页面板，读取 Antigravity 留在电脑上的日志，统计每天、每个模型、每个会话用了多少 token、缓存命中率多少。无需安装依赖，可装成后台服务开机自启。",
              "A local web dashboard that reads the logs Antigravity leaves on your computer and shows token usage and cache hit rate by day, model and session. No dependencies to install, and it can run as a background service at login."),
        play=None, repo=f"{GH}/antigravity-usage-dashboard",
    ),
    dict(
        slug="claude-fortress", color="#5fd1b6",
        cat=("安全 · Agent Skill", "Security · Agent Skill"), status=("开源 · v1.2", "Open source · v1.2"), live=False,
        date="2026-11-26",
        name=("Claude 堡垒", "Claude Fortress"), sub=("Claude Fortress", "Claude 堡垒"),
        desc=("一套开源 Agent Skill 加中英交互式路线图：一步步把 AI Agent 关进隔离环境——专用虚拟机、默认拒绝的出口网关、操作分级确认，并在自己机器上做冷启动、热启动和断网自检。",
              "An open-source Agent Skill with a bilingual interactive roadmap that walks you through putting an AI agent in an isolated environment — a dedicated VM, a default-deny egress gateway, tiered approvals — and self-testing it on your own machine."),
        play=None, site="https://rose-mys.github.io/claude-fortress/", repo=f"{GH}/claude-fortress",
    ),
]


EXTRA = {
    "shapesound": dict(accent="#f2b880", tt=(("形声 ", "ShapeSound"), ("Shape", "Sound")),
                       short=("画线即作曲的网页乐器，点开就能在浏览器里玩。", "A web instrument where drawing a line writes music — playable right in your browser.")),
    "run-haoge-run": dict(accent="#ef8a7f", tt=(("郝哥", "快跑"), ("Run Haoge ", "Run")),
                          short=("3D 三车道追逃：从菜市场一路跑到出口，分段闯关。", "A 3D three-lane chase — from the market to the exit, one segment at a time.")),
    "gesture-conductor": dict(accent="#c9b2ff", tt=(("模拟", "指挥"), ("Gesture ", "Ensemble")),
                              short=("站在摄像头前，用双手指挥一支乐队。东南大学新生 AI 创客大赛参赛作品。", "Conduct a band with your hands in front of a camera. Our SEU Freshman AI Maker Competition entry.")),
    "auto-transcription": dict(accent="#9fd3e8", tt=(("全自动", "扒谱"), ("Auto ", "Transcription")),
                               short=("录音进去，五线谱、MIDI 和简谱出来。", "Audio in — sheet music, MIDI and numbered notation out.")),
    "qq-bot": dict(accent="#a6e3a1", tt=(("QQ 机器人", "「小瓜」"), ("Xiaogua ", "QQ Bot")),
                   short=("有人格、有情绪、会记事、会斗图的 QQ 群聊 AI 机器人。", "A QQ group-chat AI with personas, moods, memory and a meme habit.")),
    "starter-generator": dict(accent="#f0d36b", tt=(("航空起动/", "发电系统"), ("Starter/", "Generator")),
                              short=("Simulink 中的航空大功率起动/发电系统模型，网侧为两电平 AFE。已完成。", "A Simulink model of a high-power aircraft starter/generator with a two-level AFE. Completed.")),
    "claude-fortress": dict(accent="#5fd1b6", tt=(("Claude ", "堡垒"), ("Claude ", "Fortress")),
                            short=("把 AI Agent 关进可验证的隔离环境：虚拟机、默认拒绝网关、分级确认。", "Put an AI agent in a verifiable sandbox: a VM, a default-deny gateway and tiered approvals.")),
    "usage-dashboard": dict(accent="#7ea6f6", tt=(("Antigravity<br>", "用量面板"), ("Antigravity<br>", "Usage")),
                            short=("在本机看清 Antigravity 每天、每个模型、每个会话用了多少 token。", "See how many tokens Antigravity uses — per day, per model, per session — right on your machine.")),
}
for _p in P:
    _p.update(EXTRA[_p["slug"]])


def title(p, tag="h2", cls=""):
    (zm, ze), (em, ee) = p["tt"]
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c}>{B(f"{zm}<em>{ze}</em>", f"{em}<em>{ee}</em>")}</{tag}>'


def meta(p):
    return (f'<p class="meta"><span>{B(*p["cat"])}</span><span class="sep"></span>'
            f'<span class="st">{B(*p["status"])}</span><span class="sep"></span>'
            f'<span class="st since">{B("始于", "Since")} {p["date"]}</span></p>')


_ZHN = {6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 11: '十一', 12: '十二'}
_ENN = {6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve'}

TRAINING = training.build(B)


def play_url(p, up):
    u = p["play"]
    return u if u.startswith("http") else up + u


def actions(p, up, detail_link=True):
    acts = []
    if p["play"]:
        acts.append(f'<a class="btn solid" href="{play_url(p, up)}">{B("在线试玩", "Play")} <i>↗</i></a>')
    if p.get("site"):
        acts.append(f'<a class="btn solid" href="{p["site"]}">{B("交互指南", "Guide")} <i>↗</i></a>')
    if detail_link:
        acts.append(f'<a class="btn" href="{up}projects/{p["slug"]}/">{B("项目介绍", "Details")} <i>→</i></a>')
    if p["repo"]:
        acts.append(f'<a class="btn" href="{p["repo"]}">GitHub <i>↗</i></a>')
    return '<div class="actions">' + "".join(acts) + "</div>"


def card(p, up):
    return f"""<article class="pcard" style="--accent:{p['accent']}">
  <a class="pcard-art" href="{up}projects/{p['slug']}/" aria-label="{p['name'][1]}">{ART[p['slug']]}</a>
  <div class="pcard-body">
    <div class="pcard-top">{meta(p)}</div>
    {title(p, 'h3')}
    <p class="desc">{B(*p['desc'])}</p>
    {actions(p, up)}
  </div>
</article>"""


def cards(up):
    return '<div class="pgrid">' + "\n".join(card(p, up) for p in P) + "</div>"


# ---------- 首页：大标题 + 拼贴项目墙 ----------
def feat_slide(i, p):
    on = " is-active" if i == 0 else ""
    href = f"projects/{p['slug']}/"
    play = (f'<a class="btn solid" href="{p["play"]}">{B("在线试玩", "Play")} <i>↗</i></a>') if p["play"] else ""
    return f"""<article class="fslide{on}" style="--accent:{p['accent']}" data-i="{i}" aria-hidden="{'false' if i == 0 else 'true'}">
  <a class="fslide-art" href="{href}" tabindex="-1" aria-label="{p['name'][1]}">{ART[p['slug']]}</a>
  <div class="fslide-body">
    {meta(p)}
    {title(p, 'h3')}
    <p>{B(*p['short'])}</p>
    <div class="actions">{play}<a class="btn{'' if p['play'] else ' solid'}" href="{href}">{B('项目介绍', 'Details')} <i>→</i></a></div>
  </div>
</article>"""


def feat_tab(i, p):
    on = " is-active" if i == 0 else ""
    (zm, ze), (em, ee) = p["tt"]
    return (f'<button class="ftab{on}" type="button" data-i="{i}" style="--accent:{p["accent"]}" role="tab" aria-selected="{"true" if i == 0 else "false"}">'
            f'<span class="ftab-num">{i + 1:02d}</span><span class="ftab-txt"><b>{B(zm + ze, em + ee)}</b><small>{B(*p["cat"])}</small></span>'
            f'<span class="ftab-bar"><span class="fill"></span></span></button>')


def index_row(i, p):
    (zm, ze), (em, ee) = p["tt"]
    return (f'<a class="irow" href="projects/{p["slug"]}/" style="--accent:{p["accent"]}">'
            f'<span class="irow-num">{i + 1:02d}</span>'
            f'<span class="irow-title">{B(f"{zm}<em>{ze}</em>", f"{em}<em>{ee}</em>")}</span>'
            f'<span class="irow-cat">{B(*p["cat"])}</span>'
            f'<span class="irow-st">{B(*p["status"])}</span>'
            f'<span class="irow-arr">→</span></a>')


_SM = {p["slug"]: p for p in P}
# 北天星空：大熊座（音乐与创作）→ 指极线 → 小熊座（AI 与工程）→ 仙后座（待点亮）。坐标是星图画布里的相对位置
_SKY = [
    # slug / 英文星名 / 中文星名 / 星等 / x / y
    ("shapesound", "Dubhe", "天枢", 1.8, .585, .555), ("run-haoge-run", "Merak", "天璇", 2.3, .57, .775),
    ("gesture-conductor", "Phecda", "天玑", 2.4, .435, .82), ("about", "Megrez", "天权", 3.0, .41, .625),
    ("auto-transcription", "Alioth", "玉衡", 1.8, .31, .595), (None, "Mizar", "开阳", 2.2, .21, .57),
    (None, "Alkaid", "瑶光", 1.9, .105, .685),
    ("usage-dashboard", "Polaris", "北极星", 2.0, .62, .27), ("claude-fortress", "Yildun", "勾陈二", 2.6, .565, .30),
    (None, "ε UMi", "勾陈三", 3.6, .505, .315), (None, "ζ UMi", "勾陈四", 3.4, .445, .345),
    ("qq-bot", "Kochab", "帝星", 2.1, .33, .30), ("starter-generator", "Pherkad", "太子", 2.4, .30, .405),
    (None, "η UMi", "少卫增", 3.6, .415, .43),
    (None, "Segin", "阁道二", 3.0, .68, .10), (None, "Ruchbah", "阁道三", 2.7, .74, .185),
    (None, "Navi", "策", 2.4, .80, .12), (None, "Schedar", "王良四", 2.3, .87, .20), (None, "Caph", "王良一", 2.4, .94, .11),
]
_EDGES = [(6, 5), (5, 4), (4, 3), (3, 0), (0, 1), (1, 2), (2, 3),          # 北斗
          (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 10),  # 小北斗
          (14, 15), (15, 16), (16, 17), (17, 18)]                           # 仙后 W
_POINTER = [(1, 0), (0, 7)]                                                  # 天璇→天枢→北极星 指极线
_GROUPS = [dict(zh="大熊座 · 音乐与创作", en="URSA MAJOR · MUSIC & MAKING", x=.06, y=.80),
           dict(zh="小熊座 · AI 与工程", en="URSA MINOR · AI & ENGINEERING", x=.20, y=.235),
           dict(zh="仙后座 · 待点亮", en="CASSIOPEIA · COMING NEXT", x=.70, y=.035)]


def _star(slug, sen, szh, mag, x, y):
    d = dict(star_en=sen, star_zh=szh, mag=mag, x=x, y=y)
    if slug == "about":
        d.update(slug="about", href="about/", zh="关于我", en="About me", czh="Rose", cen="Rose", color="#efebe1")
    elif slug:
        q = _SM[slug]
        d.update(slug=slug, href=f"projects/{slug}/", zh=q["name"][0], en=q["name"][1], czh=q["cat"][0], cen=q["cat"][1], color=q["accent"])
    else:
        d.update(slug=None, href=None, zh="待点亮", en="Unlit", czh="下一个项目", cen="next project", color="#a7adc2", unlit=True)
    return d


STARS = json.dumps(dict(stars=[_star(*t) for t in _SKY], edges=_EDGES, pointer=_POINTER, groups=_GROUPS), ensure_ascii=False)

home = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-inner">
      <p class="kicker"><i></i>{B('项目笔记本 · 2026', 'Project notebook · 2026')}</p>
      <h1>{B('你好，我是 <em>Rose</em>。', 'Hi, I’m <em>Rose</em>.')}</h1>
      <p class="lede">{B('东南大学计算机专业大一学生。我喜欢把线条变成声音、把手势变成指挥、把录音变成乐谱——这里收着我做过和正在做的东西。',
                       'A first-year CS student at Southeast University. I turn lines into sound, gestures into conducting and recordings into sheet music — this is where I keep what I build.')}</p>
      <div class="hero-cta"><a class="btn solid" href="#work">{B('看看项目', 'See my work')} <i>↓</i></a><a class="btn" href="{GH}">GitHub <i>↗</i></a></div>
      <dl class="stats">
        <div><dt>{B('项目', 'Projects')}</dt><dd>{len(P):02d}</dd></div>
        <div><dt>{B('可在线玩', 'Playable')}</dt><dd>{sum(1 for p in P if p['play']):02d}</dd></div>
        <div><dt>{B('进行中', 'In progress')}</dt><dd>{sum(1 for p in P if p['status'][1] in ('In progress', 'Team · Ongoing')):02d}</dd></div>
      </dl>
    </div>
    <div class="sky" id="sky">
      <canvas aria-label="Big Dipper constellation: six stars are projects, one is the About page. Drag them around; click one to open it." role="img"></canvas>
      <div class="sky-ui">
        <span class="sky-hint"><span class="h-mouse">{B('北天星空 · 单击弹奏，双击进入，可拖动', 'Northern sky · click to play, double-click to open, drag to fling')}</span><span class="h-touch">{B('北天星空 · 点一下弹奏，再点进入，可拖动', 'Northern sky · tap to play, tap again to open, drag to fling')}</span></span>
        <button class="sky-mute" type="button" aria-label="Mute or unmute star sounds" title="Sound"><svg class="on" viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg><svg class="off" viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M17 9l5 6M22 9l-5 6"/></svg></button>
      </div>
      <noscript><ul>{''.join(f'<li><a href="projects/{p["slug"]}/">{p["name"][1]}</a></li>' for p in P)}</ul></noscript>
      <script type="application/json" id="stars-data">{STARS}</script>
    </div>
  </div>
</section>

<section class="work" id="work">
  <div class="wrap">
    <div class="sec-head"><h2>{B('精选<em>作品</em>', 'Featured <em>work</em>')}</h2><span class="rule"></span><a class="kicker-s" href="projects/">{B('项目目录 →', 'Directory →')}</a></div>
    <div class="feature" id="feature">
      <div class="ftabs" role="tablist">{''.join(feat_tab(i, p) for i, p in enumerate(P))}</div>
      <div class="fstage" tabindex="0" aria-label="Featured projects — scroll, swipe or use arrow keys to switch">{''.join(feat_slide(i, p) for i, p in enumerate(P))}
        <div class="fhint" aria-hidden="true"><span class="mouse"><i></i></span><span class="finger"><i></i></span><span class="h-mouse">{B('滚动播放', 'Scroll to animate')}</span><span class="h-touch">{B('左右拖动播放', 'Swipe to animate')}</span></div>
        <div class="fcount" aria-hidden="true"><b class="fcur">01</b> / {len(P):02d}</div>
      </div>
    </div>
  </div>
</section>

<section class="explore" id="explore">
  <div class="wrap">
    <div class="sec-head"><h2>{B('去别处<em>看看</em>', 'Elsewhere')}</h2><span class="rule"></span><span class="kicker-s">04 {B('个入口', 'links')}</span></div>
    <div class="dests">
      <a class="dest" href="about/" style="--accent:#f2b880">
        <span class="dest-top"><span class="ico"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg></span><span class="num">01 / {B('关于', 'About')}</span><span class="arr">↗</span></span>
        <h3>{B('关于我', 'About me')}</h3><p>{B('我是谁、在学什么、对什么感兴趣。', 'Who I am, what I study and what I’m into.')}</p></a>
      <a class="dest" href="projects/" style="--accent:#9fd3e8">
        <span class="dest-top"><span class="ico"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="8" height="7" rx="1.5"/><rect x="13" y="4" width="8" height="7" rx="1.5"/><rect x="3" y="13" width="8" height="7" rx="1.5"/><rect x="13" y="13" width="8" height="7" rx="1.5"/></svg></span><span class="num">02 / {B('项目', 'Projects')}</span><span class="arr">↗</span></span>
        <h3>{B('项目目录', 'Project directory')}</h3><p>{B(f'{_ZHN[len(P)]}个项目的介绍、试玩入口和代码仓库。', f'Write-ups, live demos and repositories for all {_ENN[len(P)]} projects.')}</p></a>
      <a class="dest" href="writing/" style="--accent:#f0d36b">
        <span class="dest-top"><span class="ico"><svg viewBox="0 0 24 24"><path d="M4 20h4L19 9l-4-4L4 16v4z"/><path d="M13 7l4 4"/></svg></span><span class="num">03 / {B('文章', 'Writing')}</span><span class="arr">↗</span></span>
        <h3>{B('文章', 'Writing')}</h3><p>{B('一些想法、尝试和踩过的坑。', 'Ideas, experiments and lessons learned.')}</p></a>
      <a class="dest" href="{GH}" style="--accent:#c9b2ff">
        <span class="dest-top"><span class="ico"><svg viewBox="0 0 24 24"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/></svg></span><span class="num">04 / GitHub</span><span class="arr">↗</span></span>
        <h3>{B('源代码', 'Source code')}</h3><p>{B('公开项目的代码都在这里。', 'Where the code for public projects lives.')}</p></a>
    </div>
  </div>
</section>"""
page("index.html", 0, "Rose · 个人主页", "Rose · Personal site", "home", home,
     "Rose 的个人主页：网页乐器、小游戏、交互装置、自动扒谱、AI 聊天机器人与电力电子仿真。", "is-home")

# ---------- 关于 ----------
about = f"""<section class="phead"><div class="wrap">
  <a class="back" href="../" data-back><i>←</i> {B('首页', 'Home')}</a>
  <p class="crumb"><a href="../">{B('首页', 'Home')}</a> <span>/</span> {B('关于', 'About')}</p>
  <h1>{B('关于<em>我</em>', 'About <em>me</em>')}</h1>
  <p class="sub">{B('Rose，东南大学计算机专业大一学生。', 'Rose — a first-year computer science student at Southeast University, Nanjing.')}</p>
</div></section>
<section class="wrap"><div class="prose">
  <h2>{B('我在做什么', 'What I do')}</h2>
  <p>{B('我喜欢把抽象的东西变得能看、能听、能玩：把线条变成音乐，把手势变成指挥，把录音变成乐谱，把变流器的控制策略变成仿真模型。',
        'I like making abstract things visible, audible and playable — lines into music, gestures into conducting, recordings into sheet music, converter control into simulation models.')}</p>
  <h2>{B('感兴趣的方向', 'Interests')}</h2>
  <ul>
    <li>{B('Web 音频与创意编程：Web Audio API、实时合成、可视化', 'Web audio and creative coding: Web Audio API, real-time synthesis, visualisation')}</li>
    <li>{B('音频 AI：自动扒谱、节拍与调性分析', 'Audio AI: automatic transcription, beat and key analysis')}</li>
    <li>{B('人机交互：用摄像头和手势控制声音', 'Human–computer interaction: controlling sound with cameras and gestures')}</li>
    <li>{B('大模型应用：有记忆、有性格的聊天机器人', 'LLM apps: chatbots with memory and personality')}</li>
    <li>{B('电力电子与控制：MATLAB / Simulink 建模与仿真', 'Power electronics and control: modelling and simulation in MATLAB / Simulink')}</li>
    <li>{B('网页游戏：Three.js 3D 小游戏', 'Web games: small 3D games with Three.js')}</li>
  </ul>
  <h2>{B('开源贡献', 'Open source')}</h2>
  <p>{B('给 <a href="https://github.com/LiuMengxuan04/vibe-resume">Vibe-Resume</a> 提交了两个 PR：英文单页简历模板和 GitHub Actions 自动测试，详见<a href="../projects/#open-source">项目页</a>。', 'Two pull requests to <a href="https://github.com/LiuMengxuan04/vibe-resume">Vibe-Resume</a> — an English one-page résumé template and a GitHub Actions test workflow. See the <a href="../projects/#open-source">Projects page</a>.')}</p>
  <h2>{B('联系', 'Contact')}</h2>
  <ul class="contact">
    <li><span>{B('邮箱', 'Email')}</span><a href="mailto:3152542774@163.com">3152542774@163.com</a></li>
    <li><span>GitHub</span><a href="{GH}">Rose-MYS</a></li>
  </ul>
  <p class="credit">{B('首页星图的钢琴音色来自 Salamander Grand Piano（Alexander Holm，CC BY 3.0）。', 'Homepage piano sound: Salamander Grand Piano by Alexander Holm (CC BY 3.0).')}</p>
</div></section>"""
page("about/index.html", 1, "关于 · Rose", "About · Rose", "about", about, "关于 Rose。")

# ---------- 项目目录 ----------
plist = f"""<section class="phead"><div class="wrap">
  <a class="back" href="../" data-back><i>←</i> {B('首页', 'Home')}</a>
  <p class="crumb"><a href="../">{B('首页', 'Home')}</a> <span>/</span> {B('项目', 'Projects')}</p>
  <h1>{B('项目<em>目录</em>', 'Project <em>directory</em>')}</h1>
  <p class="sub">{B('工程作品、创意软件和比赛项目。能在线玩的，点「在线试玩」直接在浏览器里打开。', 'Engineering builds, creative software and competition work. Anything playable opens right in your browser.')}</p>
</div></section>
<section class="wrap">{cards('../')}</section>
<section class="wrap" id="open-source" style="margin-top:72px;padding-bottom:48px">
  <div class="sec-head"><h2>{B('开源<em>贡献</em>', 'Open-source <em>contributions</em>')}</h2><span class="rule"></span><span class="kicker-s">02 PRs</span></div>
  <div class="prose">
    <p>{B('给别人的开源项目提交的代码。', 'Code I’ve contributed to other people’s open-source projects.')}</p>
    <p><b><a href="https://github.com/LiuMengxuan04/vibe-resume">Vibe-Resume</a></b> {B('— 面向 AI 协作的开源简历工作流：HTML/CSS 简历、实时预览、导出 PDF（GitHub 700+ ★）', '— an open-source, AI-friendly résumé workflow: HTML/CSS résumés, live preview and PDF export (700+ ★ on GitHub)')}</p>
    <ul>
      <li><a href="https://github.com/LiuMengxuan04/vibe-resume/pull/7">PR #7</a> · {B('新增英文单页简历模板（已被维护者关闭，复盘见<a href="../writing/first-pr-closed/">这篇文章</a>）', 'Add an English one-page résumé template (closed by the maintainer — see <a href="../writing/first-pr-closed/">what I learned</a>)')}</li>
      <li><a href="https://github.com/LiuMengxuan04/vibe-resume/pull/8">PR #8</a> · {B('新增 GitHub Actions 自动测试：在 Node 20 / 22 上运行，并配置 Chrome，让浏览器测试不再被跳过（35 / 35 通过）', 'Add a GitHub Actions test workflow on Node 20 / 22, with Chrome configured so browser tests are no longer skipped (35 / 35 passing)')}</li>
    </ul>
  </div>
</section>"""
page("projects/index.html", 1, "项目 · Rose", "Projects · Rose", "projects", plist, "Rose 的项目目录。")


def detail(p, facts, sections, demo=None):
    up = "../../"
    demo_src = p["play"] if (p["play"] or "").startswith("http") else "play/"
    fx = "".join(f"<div><dt>{B(*k)}</dt><dd>{B(*v) if isinstance(v, tuple) else v}</dd></div>" for k, v in facts)
    demo_html = ""
    if demo:
        demo_html = f"""<div class="demo">
  <div class="demo-bar"><span><i class="dot"></i>{B(*demo[1])}</span><a href="{demo_src}" target="_blank" rel="noopener">{B('新窗口打开 ↗', 'Open in new tab ↗')}</a></div>
  <iframe src="{demo_src}" title="{p['name'][1]}" loading="lazy" allow="autoplay; midi; fullscreen" allowfullscreen></iframe>
</div>"""
    acts = actions(p, up, detail_link=False)
    if p["play"] and not p["play"].startswith("http"):
        acts = acts.replace(f'href="{up}{p["play"]}"', 'href="play/"')
    body = f"""<section class="phead detail-head" style="--accent:{p['accent']}"><div class="wrap dh-grid">
  <div>
    <a class="back" href="{up}projects/" data-back><i>←</i> {B('返回', 'Back')}</a>
    <p class="crumb"><a href="{up}">{B('首页', 'Home')}</a> <span>/</span> <a href="{up}projects/">{B('项目', 'Projects')}</a> <span>/</span> {B(*p['name'])}</p>
    {meta(p)}
    {title(p, 'h1')}
    <p class="sub">{B(*p['desc'])}</p>
    {acts}
  </div>
  <div class="dh-art">{ART[p['slug']]}</div>
</div></section>
<section class="wrap" style="--accent:{p['accent']}">
  <dl class="facts">{fx}</dl>
  {demo_html}
  <div class="dlayout"><nav class="toc" aria-label="On this page"><div class="toc-in"><p class="toc-h">{B('本页目录', 'On this page')}</p><ol></ol></div></nav>
  <div class="prose">{sections}</div></div>
</section>"""
    page(f"projects/{p['slug']}/index.html", 2, f"{p['name'][0]} · Rose", f"{p['name'][1]} · Rose", "projects", body, p["desc"][0])


S, H, G, T, Q, M, U, F = P
detail(S,
       [(("类型", "Type"), ("网页乐器", "Web instrument")), (("平台", "Platform"), ("电脑 / 手机浏览器", "Desktop & mobile browsers")),
        (("技术", "Stack"), "HTML · CSS · JS · Web Audio"), (("依赖", "Dependencies"), ("无，单文件离线可用", "None — one offline file"))],
       f"""<h2>{B('怎么玩', 'How to play')}</h2>
<ul>
<li>{B('竖直位置就是音高：横线是长音，斜线是琶音，竖线是和弦。', 'Vertical position is pitch: horizontal lines hold, diagonals arpeggiate, verticals make chords.')}</li>
<li>{B('16 种颜色对应 16 种乐器，全部用 Web Audio 实时合成。', '16 colours map to 16 instruments, all synthesised live with the Web Audio API.')}</li>
<li>{B('12 个调 × 11 种音阶，选对音阶，怎么画都和谐。', '12 keys × 11 scales — pick a scale and anything you draw sounds right.')}</li>
<li>{B('支持导入简谱、MusicXML、MIDI，或者把照片自动描成线条。', 'Import numbered notation, MusicXML or MIDI, or trace a photo into lines.')}</li>
<li>{B('可以导出 WAV / MIDI，也能接 MIDI 键盘弹奏。', 'Export WAV / MIDI, or play along on a MIDI keyboard.')}</li>
</ul>
<p class="note">{B('玩法与界面布局参考了 playmusictheory.net/play（作者 Tala Rae Schlossberg），代码、文字、配色与图标均为独立编写。',
                  'Gameplay and layout are inspired by playmusictheory.net/play by Tala Rae Schlossberg; all code, text, colours and icons were written independently.')}</p>""",
       demo=True and ("demo", ("可以直接在下面画线试试", "Try drawing right here")))

detail(H,
       [(("类型", "Type"), ("3D 网页游戏", "3D web game")), (("引擎", "Engine"), "Three.js"),
        (("平台", "Platform"), ("电脑 / 手机浏览器", "Desktop & mobile browsers")), (("离线", "Offline"), ("可以", "Yes"))],
       f"""<h2>{B('操作', 'Controls')}</h2>
<ul>
<li>{B('换道：← → 或 A / D（手机左右滑）', 'Change lane: ← → or A / D (swipe on mobile)')}</li>
<li>{B('转弯：绿灯亮时按 ← 或 → 确认（手机上有专门的按钮）', 'Turn: press ← or → on a green light (dedicated buttons on mobile)')}</li>
<li>{B('跳跃 / 二段跳：↑ 或 W（上滑）', 'Jump / double jump: ↑ or W (swipe up)')}</li>
<li>{B('滑铲 / 快速落地：↓ 或 S（下滑）', 'Slide / fast drop: ↓ or S (swipe down)')}</li>
<li>{B('「保熟」技能：E；暂停：空格 / Esc / P；静音：M', '“Baoshu” skill: E · Pause: Space / Esc / P · Mute: M')}</li>
</ul>
<p class="note">{B('这里嵌入的是游戏在 GitHub Pages 上的在线版本：分段闯关，每段结束自动存档；音效为合成音效。', 'This is the live version hosted on GitHub Pages: a segmented campaign that saves after each segment, with synthesised sound effects.')}</p>""",
       demo=True and ("demo", ("点一下画面再用键盘操作", "Click the game, then use your keyboard")))

detail(G,
       [(("比赛", "Competition"), ("东南大学第一届新生 AI 创客大赛", "1st SEU Freshman AI Maker Competition")),
        (("方向", "Track"), ("数字交互类", "Digital interaction")),
        (("形式", "Format"), ("团队项目", "Team project")), (("状态", "Status"), ("比赛进行中", "Ongoing"))],
       f"""<h2>{B('这是什么', 'What it is')}</h2>
<p>{B('参与者站在摄像头前，像指挥家一样挥动双手：一只手控制乐队的速度，另一只手控制整体音量。动作不是装饰，而是直接改变音乐的节奏和动态。',
      'Participants stand in front of a camera and conduct with both hands — one hand sets the tempo, the other the overall volume. The gestures are not decoration; they directly reshape the music.')}</p>
<p class="note">{B('比赛还在进行中，更多细节会在比赛结束后补充。', 'The competition is still running — more details will follow once it ends.')}</p>""")


detail(T,
       [(("类型", "Type"), ("音频转谱流水线", "Audio-to-score pipeline")), (("语言", "Language"), "Python"),
        (("输出", "Output"), ("MusicXML · MIDI · 简谱 · SVG", "MusicXML · MIDI · Jianpu · SVG")), (("版本", "Version"), "v4 (2026-11-23)")],
       f"""<h2>{B('流程', 'Pipeline')}</h2>
<ol>
<li>{B('<b>音频 → MIDI</b>：自动判断类型，钢琴用 Transkun v2，长笛、小提琴、人声等单旋律用 pYIN 音高跟踪。', '<b>Audio → MIDI</b>: detects the source automatically — Transkun v2 for piano, pYIN pitch tracking for single melodies such as flute, violin or voice.')}</li>
<li>{B('<b>MIDI → 乐谱</b>（核心）：节拍跟踪 → 量化（16 分音符 / 三连音）→ 拍号与强拍 → 调号与升降号拼写 → 左右手分配。', '<b>MIDI → score</b> (the core): beat tracking → quantisation (16ths / triplets) → time signature and downbeats → key signature and accidental spelling → left/right-hand split.')}</li>
<li>{B('<b>输出</b>：钢琴大谱表 MusicXML（可导入 MuseScore / Sibelius / Finale / Dorico）、量化 MIDI、简谱文本和谱面预览。', '<b>Output</b>: grand-staff MusicXML (opens in MuseScore / Sibelius / Finale / Dorico), quantised MIDI, numbered notation and a rendered preview.')}</li>
</ol>
<h2>{B('效果', 'Results')}</h2>
<ul>
<li>{B('测试集分四级：从单旋律儿歌到巴赫、肖邦、舒伯特、莫扎特的钢琴曲，共 16 首。', 'A four-level test set of 16 pieces, from simple melodies to piano works by Bach, Chopin, Schubert and Mozart.')}</li>
<li>{B('v4：核心 16 首调号全对；15 首训练集外录音中，严格拍号 14 首正确，音符 F1 0.993 以上。', 'v4: key signatures 16/16 on the core set; on 15 held-out recordings, strict time signature 14/15 and note F1 above 0.993.')}</li>
<li>{B('全部在 CPU 上运行，每次运行自动生成测评报告，方便对比版本。', 'Runs entirely on CPU and writes an evaluation report on every run, so versions can be compared.')}</li>
</ul>
<figure class="fig"><img src="score-preview.svg" alt="Auto-generated score preview" loading="lazy" style="width:100%;height:auto;background:#fff">
<figcaption>{B('流水线自动生成的谱面预览：《欢乐颂》双手钢琴版（Verovio 渲染）。', 'A score preview generated by the pipeline: “Ode to Joy” for two-hand piano (rendered with Verovio).')}</figcaption></figure>
{TRAINING}
<p class="note">{B('用到的开源工具：Transkun、librosa、music21、mir_eval、verovio。部分测试音频来自 MAESTRO 数据集（CC BY-NC-SA）。项目还在继续。',
 'Built on Transkun, librosa, music21, mir_eval and verovio. Part of the test audio comes from the MAESTRO dataset (CC BY-NC-SA). Still in progress.')}</p>""")

detail(Q,
       [(("类型", "Type"), ("QQ 群聊 AI 机器人", "QQ group-chat AI bot")), (("架构", "Stack"), "NapCat · AstrBot · LLM API"),
        (("插件", "Plugins"), ("20 个自研插件", "20 custom plugins")), (("状态", "Status"), ("长期在线", "Always on"))],
       f"""<h2>{B('架构', 'Architecture')}</h2>
<p><code>QQ ⇄ NapCat {B('（协议端）', '(protocol)')} ⇄ AstrBot {B('（AI 框架）', '(AI framework)')} ⇄ DeepSeek {B('等大模型 API', 'and other LLM APIs')}</code></p>
<h2>{B('小瓜会做什么', 'What Xiaogua can do')}</h2>
<ul>
<li>{B('<b>人格系统</b>：本体人格加多套预设，可以模仿、切换人格。', '<b>Personas</b>: a core persona plus presets; it can switch or imitate styles.')}</li>
<li>{B('<b>情绪与节奏</b>：七种情绪，先判断该不该接话，再加冷却和每小时上限，不刷屏。', '<b>Mood & pacing</b>: seven moods and a “should I reply?” gate with cooldowns and hourly caps, so it never spams.')}</li>
<li>{B('<b>长期记忆</b>：按人、群、全局三层记忆，聊天中自动提炼。', '<b>Long-term memory</b>: per-person, per-group and global memories distilled from chats.')}</li>
<li>{B('<b>看图和斗图</b>：能看懂群友发的图片；两百多张带语义标签的表情包，可以自主斗图。', '<b>Images & memes</b>: understands pictures people send and picks from 200+ tagged memes on its own.')}</li>
<li>{B('<b>自我进化</b>：定时去 B 站学新梗，感知群里的氛围，调整说话口味。', '<b>Self-evolution</b>: periodically learns new slang from Bilibili and adapts to each group’s vibe.')}</li>
<li>{B('<b>约定追踪和周记</b>：记住聊天里的约定，到点提醒；每周日自动写一篇周记。', '<b>Follow-ups & diary</b>: remembers promises made in chat and checks back; writes a weekly diary every Sunday.')}</li>
<li>{B('<b>作息与自愈</b>：按作息睡觉、起床；看护脚本自动处理掉线、重连和扫码。', '<b>Routine & self-healing</b>: keeps a sleep schedule; a watchdog handles disconnects, reconnection and QR re-login.')}</li>
<li>{B('<b>控制台</b>：网页面板，查看各插件状态，一键暂停或恢复。', '<b>Dashboard</b>: a web panel showing every plugin’s status, with one-click pause and resume.')}</li>
</ul>
<p class="note">{B('机器人涉及账号和 API 密钥，代码不公开。', 'The bot involves account credentials and API keys, so the code is not public.')}</p>""")

detail(M,
       [(("工具", "Tools"), "MATLAB / Simulink"), (("对象", "System"), ("航空大功率起动/发电系统", "High-power aircraft starter/generator")),
        (("网侧", "Grid side"), ("三相两电平六开关 AFE", "3-phase 2-level 6-switch AFE")), (("状态", "Status"), ("已完成并交付", "Completed & delivered"))],
       f"""<h2>{B('简介', 'Overview')}</h2>
<p>{B('飞机上的起动/发电机在发动机启动时作为电动机工作，启动完成后转为发电机为机上设备供电。这个项目在 Simulink 中搭建整套系统模型，网侧采用三相两电平六开关有源前端（AFE）变流器。',
      'An aircraft starter/generator runs as a motor to start the engine, then switches to generating power for on-board systems. This project builds the full system model in Simulink, with a three-phase two-level six-switch active front end (AFE) converter on the grid side.')}</p>
<h2>{B('网侧变流器拓扑', 'Grid-side converter topology')}</h2>
<figure class="fig">{AFE_SVG}<figcaption>{B('三相两电平六开关 AFE 原理示意：三相交流经滤波电感 L 接入六个开关管 S1–S6 组成的三桥臂，整流/逆变后在直流母线电容 C 上建立 U<sub>dc</sub>，再连接机侧变流器与起动/发电机。（原理示意图，非仿真结果）',
 'Three-phase two-level six-switch AFE: the AC side connects through filter inductors L to three bridge legs (S1–S6), which build the DC-link voltage U<sub>dc</sub> across capacitor C for the machine-side converter and the starter/generator. (Schematic only — not a simulation result.)')}</figcaption></figure>
{reading_html()}""")

detail(U,
       [(("类型", "Type"), ("本地网页面板", "Local web dashboard")), (("技术", "Stack"), ("Node.js 20 · 原生 JS，无依赖", "Node.js 20 · vanilla JS, no deps")),
        (("系统", "Platforms"), "Windows · macOS · Linux"), (("版本", "Version"), "v1.1.0")],
       f"""<h2>{B('做什么', 'What it does')}</h2>
<p>{B('Antigravity 会把每次对话的记录写在本机日志里，但不会告诉你一共用了多少 token。这个面板读取这些日志，把用量按日期、模型和会话整理出来，打开浏览器就能看。',
      'Antigravity writes every conversation to local logs but never tells you how many tokens you have used. This dashboard reads those logs and organises usage by date, model and session in your browser.')}</p>
<figure class="fig"><img src="img/dashboard.jpg" alt="Antigravity Usage Dashboard showing totals, sessions grouped by model and a session detail panel" loading="lazy" style="width:100%;height:auto">
<figcaption>{B('面板全貌：顶部四张总览卡，左边按模型分组的会话列表，右边是选中会话的用量构成和累计走势。（截图使用示例数据）',
 'The full dashboard: four summary cards on top, sessions grouped by model on the left, and the selected session’s token mix and cumulative trend on the right. (Screenshot uses sample data.)')}</figcaption></figure>
<h2>{B('主要功能', 'Features')}</h2>
<ul>
<li>{B('<b>四张总览卡</b>：总用量、输出用量、会话数、缓存命中率，悬停可看具体数值。', '<b>Four summary cards</b>: total and output tokens, session count and cache hit rate, with hover details.')}</li>
<li>{B('<b>按模型查看</b>：点「总用量」卡片，其他卡片切换成各模型的用量和占比，边框按占比分段着色。', '<b>By model</b>: click the total card and the others turn into per-model usage and share, with borders coloured by share.')}</li>
<li>{B('<b>日历选区间</b>：日历格子里直接显示每天的用量，点两天就选出一段区间，底部有本月和今年合计。', '<b>Calendar range picker</b>: each day shows its usage; click two days to pick a range, with month and year totals below.')}</li>
<li>{B('<b>会话详情</b>：未缓存输入、缓存输入和输出的构成，累计走势图可以用方向键逐条看每次请求。', '<b>Session detail</b>: uncached input, cached input and output, plus a cumulative chart you can step through request by request with the arrow keys.')}</li>
<li>{B('<b>后台常驻</b>：一条命令装成后台服务，可选开机自启和异常退出后自动重启，Windows、macOS、Linux 都支持。', '<b>Background service</b>: one command installs it, with optional autostart and auto-restart on Windows, macOS and Linux.')}</li>
<li>{B('<b>新版本提醒</b>：有新版本时顶部出现提示条，运行 <code>npm run update</code> 即可更新，不会覆盖本地改动。', '<b>Update notice</b>: a banner appears when a new release is out; <code>npm run update</code> updates without overwriting local changes.')}</li>
</ul>
<figure class="fig"><img src="img/by-model.jpg" alt="Summary cards switched to per-model usage" loading="lazy" style="width:100%;height:auto">
<figcaption>{B('点开「按模型」后，概览卡变成每个模型的用量、占比和缓存命中率。（示例数据）', 'With “By model” open, the summary cards show each model’s usage, share and cache hit rate. (Sample data.)')}</figcaption></figure>
<h2>{B('统计口径与隐私', 'How it counts, and privacy')}</h2>
<ul>
<li>{B('每条有效的模型回复日志算一次请求；总用量 = 未缓存输入 + 缓存输入 + 输出；缓存命中率 = 缓存输入 ÷ 全部输入。', 'Each model response in the log counts as one request; total = uncached input + cached input + output; cache hit rate = cached input ÷ all input.')}</li>
<li>{B('服务只监听本机 <code>127.0.0.1</code>，只读本地日志，不需要任何 API 密钥。唯一的联网请求是检查新版本，可以关掉。', 'It only listens on <code>127.0.0.1</code>, only reads local logs and needs no API key. The one network request is the update check, which can be turned off.')}</li>
</ul>
<h2>{B('试一试', 'Try it')}</h2>
<p><code>git clone {GH}/antigravity-usage-dashboard.git &amp;&amp; cd antigravity-usage-dashboard &amp;&amp; npm start</code></p>
<p>{B('然后打开 <code>http://127.0.0.1:8768</code>。需要 Node.js 20 或更新版本。', 'Then open <code>http://127.0.0.1:8768</code>. Requires Node.js 20 or newer.')}</p>
<p class="note">{B('界面布局和交互参考了 luyh7/codex-usage-dashboard。Antigravity 名称和图标归 Google 所有，本项目为个人开发的非官方工具。',
 'Layout and interactions are modelled on luyh7/codex-usage-dashboard. The Antigravity name and icon belong to Google; this is an unofficial personal tool.')}</p>""")

detail(F,
       [(("类型", "Type"), ("Agent Skill + 交互式路线图", "Agent Skill + interactive roadmap")), (("语言", "Language"), ("中文 · English", "Chinese · English")),
        (("内容", "Contents"), ("SKILL.md · 9 篇参考 · 脚本 · 模板", "SKILL.md · 9 references · scripts · templates")), (("版本", "Version"), "v1.2.0 · MIT")],
       f"""<h2>{B('是什么', 'What it is')}</h2>
<p>{B('让 AI Agent 帮你在电脑上干活很方便，但它能联网、能跑命令，一旦出错影响的是整台机器。Claude 堡垒把我自己搭隔离环境的经验整理成一套开源 Agent Skill：装好之后，Agent 会按规范一步步带你把它自己关进隔离环境，每一步先说清风险等级，高风险操作必须你本人确认。',
      'Letting an AI agent work on your computer is handy, but it can reach the network and run commands, so a mistake affects the whole machine. Claude Fortress turns my own isolation setup into an open-source Agent Skill: once installed, the agent walks you through sandboxing itself step by step, states the risk tier of each step, and needs your explicit approval for anything high-risk.')}</p>
<p><a class="btn solid" href="https://rose-mys.github.io/claude-fortress/">{B('打开交互式路线图', 'Open the interactive roadmap')} <i>↗</i></a></p>
<h2>{B('三档风险，按步走', 'Three risk tiers, one step at a time')}</h2>
<ul>
<li>{B('<b>A 档 · 纯只读</b>：离线盘点机器配置，不写文件、不联网、不改网卡。', '<b>Tier A · read-only</b>: an offline inventory of the machine — no writes, no network, no adapter changes.')}</li>
<li>{B('<b>B 档 · 可逆</b>：中性的功能探测，随时能撤回。', '<b>Tier B · reversible</b>: neutral functional probes that can be undone.')}</li>
<li>{B('<b>C 档 · 高风险</b>：改网关规则、可能断网的动作，必须你本人逐项确认。', '<b>Tier C · high-risk</b>: gateway rules and anything that might cut the network — each needs your own sign-off.')}</li>
</ul>
<h2>{B('几条路线', 'Routes')}</h2>
<ul>
<li>{B('<b>虚拟机堡垒</b>：Windows 虚拟机只接一个隔离网段，出口经过一台默认拒绝的 OpenWrt 网关，客机再加一层防火墙白名单。', '<b>VM fortress</b>: a Windows VM on a single isolated network, egress through a default-deny OpenWrt gateway, plus a firewall allow-list inside the guest.')}</li>
<li>{B('<b>本机轻量</b>：不开虚拟机，用独立浏览器配置和命令行做应用层隔离。', '<b>Lightweight local</b>: no VM; app-level isolation with separate browser profiles and the CLI.')}</li>
<li>{B('<b>远程开发机</b>：把 Agent 放在一台 Linux 服务器上，本机只连终端。', '<b>Remote dev box</b>: run the agent on a Linux server and only connect a terminal locally.')}</li>
<li>{B('<b>可选进阶：多 Agent 协作</b>：共享协作区、两层 Git、交接文档制度，和账号、网络无关，可以单独用。', '<b>Optional: multi-agent workflow</b>: a shared workspace, two-level Git and handoff documents — independent of accounts or networking.')}</li>
</ul>
<h2>{B('先自检，再上线', 'Self-test before going live')}</h2>
<p>{B('它不是"装了就安全"的黑盒。每台机器的系统、网卡和固件都不同，所以 Skill 会陪你在自己的机器上做四类实测：冷启动时网关默认不放行、重启或重载规则后边界依然闭合、主动断开上游时客机彻底断网不回退直连、DNS / IPv6 / UDP / WebRTC 没有泄漏。',
      'It is not a black box that makes you safe on install. Every machine differs, so the Skill has you run four checks on your own hardware: the gateway forwards nothing on a cold boot, the boundary stays closed after restarts and rule reloads, the guest goes fully offline (no fallback) when upstream is cut, and DNS / IPv6 / UDP / WebRTC do not leak.')}</p>
<h2>{B('怎么装', 'Install')}</h2>
<p>{B('Claude Code 里输入：', 'In Claude Code:')} <code>/plugin marketplace add Rose-MYS/claude-fortress</code> {B('再', 'then')} <code>/plugin install fortress@rose-mys</code>{B('。也可以 git clone 到 Skills 目录，或下载 Release 里的 zip 上传到 Claude 应用。', '. You can also git clone it into your Skills folder, or upload the release zip to the Claude app.')}</p>
<p class="note">{B('多个 Agent 协作完成：经过两轮独立红队审阅并修复全部高优先级问题；仓库只放脱敏后的模板和文档，不含任何真实配置或账号信息。',
 'Built with several agents and two rounds of independent red-team review, with every high-priority issue fixed; the repo holds only sanitised templates and docs, with no real configs or account data.')}</p>""")

print("ok")
