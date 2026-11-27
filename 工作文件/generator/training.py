"""全自动扒谱：训练过程（版本迭代时间线 + 分数图 + 前后对比）。数据来自项目的 runs/*/results.json 与验收记录。"""


def build(B):
    def T_(zh, en):  # SVG 内用 tspan
        return f'<tspan class="zh">{zh}</tspan><tspan class="en">{en}</tspan>'

    # ---------- 总览数字 ----------
    stats = [("6", ("轮迭代", "iterations")), ("2", ("天", "days")), ("31", ("首测试曲", "test pieces")),
             ("16/16", ("核心集调号", "keys, core set")), ("14/15", ("训练集外严格拍号", "strict meter, held-out"))]
    stat_html = "".join(f'<div class="tl-stat"><b>{n}</b><span>{B(*lab)}</span></div>' for n, lab in stats)

    # ---------- 迭代流程 ----------
    loop = [("01", ("发布任务", "Write the task"), ("写清目标和验收标准", "Goal + acceptance bar")),
            ("02", ("独立分支实现", "Build on a branch"), ("只改流水线代码", "Pipeline code only")),
            ("03", ("全量测评", "Full evaluation"), ("所有测试曲重跑一遍", "Re-run every piece")),
            ("04", ("独立验收", "Independent review"), ("复现分数、查退步", "Reproduce, catch regressions"))]
    loop_html = "".join(
        f'<li><span class="lp-n">{n}</span><b>{B(*t)}</b><small>{B(*d)}</small></li>' for n, t, d in loop)

    # ---------- 图 1：核心 16 首调号（v2→v4），带退步与修复 ----------
    vs = ["v2", "v3", "v3.1", "v4"]; vals = [15, 13, 16, 16]
    X = [60 + i * 110 for i in range(4)]
    Y = [20 + (16 - v) * 30 for v in vals]          # 16→20, 12→140
    grid = "".join(f'<line x1="44" x2="410" y1="{20 + k * 30}" y2="{20 + k * 30}" class="ch-grid"/><text x="36" y="{24 + k * 30}" class="ch-y">{16 - k}</text>' for k in range(5))
    pts = " ".join(f"{x},{y}" for x, y in zip(X, Y))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="5" class="ch-dot{" bad" if v < 15 else ""}"/><text x="{x}" y="{y - 12}" class="ch-v">{v}</text><text x="{x}" y="176" class="ch-x">{n}</text>' for x, y, v, n in zip(X, Y, vals, vs))
    chart1 = f'''<svg viewBox="0 0 420 190" class="chart" role="img" aria-label="Key signatures correct on the 16-piece core set: v2 15, v3 13, v3.1 16, v4 16">
{grid}<polyline points="{pts}" class="ch-line" pathLength="1"/>{dots}
<text x="{X[1] + 8}" y="{Y[1] + 20}" class="ch-note">{T_('改可读性时退步', 'regressed while fixing readability')}</text>
<text x="{X[2] + 10}" y="{Y[2] + 22}" class="ch-note ok">{T_('验收发现 → 修复', 'caught in review → fixed')}</text></svg>'''

    # ---------- 图 2：可读性，每小节休止符 ----------
    groups = [("L3", 1.24, 0.11), ("L4", 0.94, 0.15)]
    bars = ""
    for gi, (lab, a, b) in enumerate(groups):
        gx = 70 + gi * 180
        for k, (v, cls, t) in enumerate(((a, "before", "v2"), (b, "after", "v3"))):
            h = v / 1.3 * 130; x = gx + k * 56
            bars += f'<rect x="{x}" y="{150 - h:.1f}" width="44" height="{h:.1f}" rx="4" class="ch-bar {cls}" style="--h:{h:.1f}px"/><text x="{x + 22}" y="{144 - h:.1f}" class="ch-v">{v}</text><text x="{x + 22}" y="166" class="ch-x small">{t}</text>'
        bars += f'<text x="{gx + 50}" y="184" class="ch-x">{lab}</text>'
    chart2 = f'''<svg viewBox="0 0 420 190" class="chart" role="img" aria-label="Rests per bar: L3 1.24 to 0.11, L4 0.94 to 0.15">
<line x1="44" x2="410" y1="150" y2="150" class="ch-grid"/>{bars}</svg>'''

    # ---------- 图 3：训练集外 15 首严格拍号 ----------
    def meter_bar(y, n, lab, cls):
        w = n / 15 * 300
        return (f'<text x="0" y="{y + 15}" class="ch-x left">{lab}</text>'
                f'<rect x="70" y="{y}" width="300" height="22" rx="11" class="ch-track"/>'
                f'<rect x="70" y="{y}" width="{w:.0f}" height="22" rx="11" class="ch-fill {cls}" style="--w:{w:.0f}px"/>'
                f'<text x="{70 + w - 10:.0f}" y="{y + 15}" class="ch-in">{n}/15</text>')
    chart3 = f'''<svg viewBox="0 0 420 190" class="chart" role="img" aria-label="Strict time signature on 15 held-out recordings: 7 before, 14 after">
{meter_bar(40, 7, "v4-test", "before")}{meter_bar(100, 14, "v4", "after")}
<text x="70" y="160" class="ch-note">{T_('12/8 不再被写成 4/4，老录音不再错拍', '12/8 no longer becomes 4/4; old recordings stay in time')}</text></svg>'''

    # ---------- 图 4：测试集规模 ----------
    sizes = [("v1", 11), ("v2", 16), ("v4-test", 31), ("v4", 31)]
    sx = [60 + i * 110 for i in range(4)]
    sy = [160 - n / 31 * 130 for _, n in sizes]
    step = f"M{sx[0]},{sy[0]:.0f}"
    for i in range(1, 4):
        step += f" H{sx[i]} V{sy[i]:.0f}"
    sdots = "".join(f'<circle cx="{x}" cy="{y:.0f}" r="5" class="ch-dot"/><text x="{x}" y="{y - 12:.0f}" class="ch-v">{n}</text><text x="{x}" y="180" class="ch-x">{v}</text>' for x, y, (v, n) in zip(sx, sy, sizes))
    chart4 = f'''<svg viewBox="0 0 420 190" class="chart" role="img" aria-label="Test set size: 11, 16, 31, 31 pieces">
<line x1="44" x2="410" y1="160" y2="160" class="ch-grid"/><path d="{step}" class="ch-line" pathLength="1"/>{sdots}
<text x="292" y="72" class="ch-note">{T_('+15 首训练集外录音', '+15 held-out recordings')}</text></svg>'''

    charts = [
        (("核心 16 首 · 调号正确数", "Core 16 · key signatures correct"), ("v3 一度退步，被验收抓到后在 v3.1 修好。", "v3 slipped; review caught it and v3.1 fixed it."), chart1),
        (("谱面可读性 · 每小节休止符", "Readability · rests per bar"), ("碎休止减少九成，连音占比 12.3% → 0.4%。", "Fragmented rests cut by ~90%; tuplets 12.3% → 0.4%."), chart2),
        (("训练集外 15 首 · 严格拍号", "Held-out 15 · strict time signature"), ("最大的短板，在 v4 集中修复。", "The biggest weak spot, fixed in v4."), chart3),
        (("测试集规模", "Test set size"), ("从儿歌到真人录音，测试越来越难。", "From nursery tunes to real recordings — harder each round."), chart4),
    ]
    chart_html = "".join(
        f'<figure class="tl-chart"><figcaption><b class="cap-t">{B(*t)}</b><span class="cap-s">{B(*s)}</span></figcaption>{svg}</figure>' for t, s, svg in charts)

    # ---------- 时间线 ----------
    T = [
        ("v1", "11-22", ("第一版流水线", "First pipeline"), None,
         ("音频 → MIDI → 五线谱 + 简谱跑通；钢琴用 Transkun，单旋律用 pYIN。", "Audio → MIDI → staff + numbered notation, end to end; Transkun for piano, pYIN for melodies."),
         [("11 首测试曲", "11 pieces"), ("调号 11/11", "keys 11/11"), ("L3 拍号 3/5", "L3 meter 3/5")]),
        ("v2", "11-22", ("节拍跟踪", "Beat tracking"), ("合格", "Passed"),
         ("接入 beat_this 节拍与强拍模型，强拍锁定细化、支持复拍子；新增 L4 真人演奏测试集。", "beat_this beats and downbeats, downbeat-locked refinement, compound meters; new L4 real-performance set."),
         [("L4 小节线 F 0.997", "L4 bar F 0.997"), ("L4 拍号 5/5", "L4 meter 5/5"), ("L3 拍号 4/5", "L3 meter 4/5")]),
        ("v3", "11-22", ("谱面可读性", "Readability"), ("基本合格", "Mostly passed"),
         ("踏板延音、随速度自适应量化、抑制碎连音、简化休止符、真正的弱起小节。", "Pedal-aware durations, tempo-adaptive quantisation, tuplet suppression, simpler rests, real pickups."),
         [("休止/小节 1.24 → 0.11", "rests/bar 1.24 → 0.11"), ("连音 12.3% → 0.4%", "tuplets 12.3% → 0.4%"), ("! 调号退步 13/16", "! keys regressed 13/16")]),
        ("v3.1", "11-22", ("调号修正", "Key fix"), ("合格", "Passed"),
         ("调性分析改用原始音符，开头乐句判断大小调，超过 6 个升降号自动等音简化。", "Key detection on raw notes, opening-phrase major/minor check, enharmonic simplification past 6 accidentals."),
         [("调号 13 → 16/16", "keys 13 → 16/16"), ("其他指标零退步", "zero regressions")]),
        ("v4-test", "11-23", ("训练集外测试", "Held-out test"), ("合格", "Passed"),
         ("新增 15 首没参与训练的录音（L5）：自动钢琴、历史录音和 Rose 的钢琴翻弹，专门检验泛化。", "15 recordings outside the training data (L5): Disklavier, historic recordings and Rose’s own covers."),
         [("音符 F1 0.993–1.000", "note F1 0.993–1.000"), ("严格拍号仅 7/15", "strict meter only 7/15"), ("调号 13/15", "keys 13/15")]),
        ("v4", "11-23", ("拍号与复拍子", "Meter & compound time"), ("合格", "Passed"),
         ("复拍子判别、强拍纯度、机械速度加力度条件、快三拍 3/8；测评改成严格拍号。", "Compound-meter detection, downbeat purity, velocity-aware mechanical tempo, fast 3/8; strict meter scoring."),
         [("严格拍号 7 → 14/15", "strict meter 7 → 14/15"), ("12/8 连音 52% → 0", "12/8 tuplets 52% → 0"), ("L1–L4 零退步", "L1–L4 unchanged")]),
        ("next", ("进行中", "now"), ("新曲验证", "New-song validation"), None,
         ("v4 的阈值是在这 15 首上调出来的，下一步用没见过的新曲子检验有没有过拟合。", "v4’s thresholds were tuned on these 15 pieces; next, fresh songs check for overfitting."),
         [("TASK-007", "TASK-007")]),
    ]
    items = ""
    for v, date, title, review, desc, chips in T:
        d = B(*date) if isinstance(date, tuple) else date
        rv = f'<span class="tl-review{" warn" if review and review[1] != "Passed" else ""}">{B("验收 · ", "Review · ")}{B(*review)}</span>' if review else ""
        ch = "".join(f'<span class="tl-chip{" warn" if c[0].startswith("!") else ""}">{B(c[0].lstrip("! "), c[1].lstrip("! "))}</span>' for c in chips)
        items += f'''<li class="tl-item{" now" if v == "next" else ""}"><div class="tl-dot"></div>
  <div class="tl-head"><span class="tl-ver">{v}</span><span class="tl-date">{d}</span>{rv}</div>
  <h3>{B(*title)}</h3><p>{B(*desc)}</p><div class="tl-chips">{ch}</div></li>'''

    # ---------- 前后对比滑块 ----------
    def compare(name, t, cap, lb, la):
        return f'''<figure class="cmp-fig"><figcaption><b class="cap-t">{B(*t)}</b><span class="cap-s">{B(*cap)}</span></figcaption>
<div class="cmp" style="--pos:50%"><img src="img/{name}-before.jpg" alt="before" loading="lazy" draggable="false"><img class="cmp-after" src="img/{name}-after.jpg" alt="after" loading="lazy" draggable="false">
<span class="cmp-tag l">{lb}</span><span class="cmp-tag r">{la}</span><div class="cmp-handle" aria-hidden="true"><i>⇆</i></div>
<input class="cmp-range" type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after"></div></figure>'''
    cmps = (compare("grieg", ("格里格《圆舞曲》Op.38-7", "Grieg · Waltz Op.38 No.7"), ("v2 → v3：碎休止和六连音消失，左手变成干净的伴奏。", "v2 → v3: fragmented rests and sextuplets disappear; the left hand becomes a clean accompaniment."), "v2", "v3")
            + compare("chopin", ("肖邦《圆舞曲》Op.64-2（老录音）", "Chopin · Waltz Op.64 No.2 (historic recording)"), ("v4-test → v4：从错误的 2/4 改成正确的 3/4，小节线回到正确的位置。", "v4-test → v4: the wrong 2/4 becomes the correct 3/4, and bar lines land where they should."), "v4-test", "v4"))

    return f"""<h2 id="training">{B('训练过程', 'How it was trained')}</h2>
<p>{B('这个项目没有从零训练模型，而是在现成的音频模型之上，一轮轮改进"音符 → 乐谱"的算法。每一轮都按同一个流程走：先写清任务，再在独立分支上实现、对所有测试曲重跑测评，最后由另一方独立复现分数并检查有没有退步，通过了才进入下一轮。',
     'Rather than training a model from scratch, the project improves the notes-to-score algorithm on top of existing audio models, one round at a time. Every round follows the same loop: write the task, build it on its own branch, re-run the full evaluation, then have a reviewer reproduce the scores and check for regressions before moving on.')}</p>
<div class="tl-stats">{stat_html}</div>
<ol class="tl-loop">{loop_html}</ol>
<div class="tl-charts">{chart_html}</div>
<h3 class="tl-sub">{B('版本时间线', 'Version timeline')}</h3>
<ol class="tl">{items}</ol>
<h3 class="tl-sub">{B('改进前后对比', 'Before and after')} <small>{B('拖动中间的把手', 'drag the handle')}</small></h3>
{cmps}
<p class="note">{B('分数可能偏乐观：Transkun 和 beat_this 的训练数据可能包含部分测试曲（MAESTRO / ASAP），所以 v4-test 起专门加入了训练集外的录音来检验。',
                 'Scores may be optimistic: Transkun and beat_this may have seen some test pieces (MAESTRO / ASAP) during training, which is why held-out recordings were added from v4-test on.')}</p>"""
