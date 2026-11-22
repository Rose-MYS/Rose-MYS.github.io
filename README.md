# Rose-MYS.github.io

Rose 的个人网站：纯手写 HTML / CSS / JS，用 GitHub Pages 托管，中英双语。

## 结构

```
index.html                 首页（项目卡片）
about/                     关于我
projects/                  项目目录
  shapesound/              形声：介绍页 + play/ 在线试玩（来自 Rose-MYS/ShapeSound 的单文件成品）
  run-haoge-run/           郝哥快跑：介绍页 + play/ 在线试玩（来自 Rose-MYS/run-haoge-run）
  gesture-conductor/       模拟指挥（东南大学第一届新生 AI 创客大赛，团队项目）
  starter-generator/       航空起动/发电系统 Simulink 仿真
assets/style.css           全站样式
assets/site.js             中英文切换
```

## 怎么改

- 每段文字都写了两遍：`<span class="zh">中文</span><span class="en">English</span>`，改的时候两种语言一起改。
- 加新项目：复制 `index.html` 和 `projects/index.html` 里的一张 `<article class="card">`，再照着现有项目新建一个 `projects/<名字>/index.html`。
- 本地预览：直接双击 `index.html` 就能看。

## 发布

把这个文件夹推送到 GitHub 上名为 `Rose-MYS.github.io` 的仓库，几分钟后就能在 https://rose-mys.github.io/ 访问。

`参考资料/` 只放在本地参考用，已在 `.gitignore` 里排除，不会推送上去。
