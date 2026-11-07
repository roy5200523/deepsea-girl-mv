# 深海少女 MV · 手绘风 AI 动画管线

> **EN**: Pipeline code for a hand-drawn-style AI music video: storyboard → image generation → anatomy QA → layered parallax → beat-synced render. **Code only** — no song, lyrics, character art or rendered video (copyright). Needs your own assets and an OpenAI-compatible relay.

把一首歌做成「手绘动画感」MV 的完整管线：**分镜 → 出图 → 解剖质检 → 分层 → 运镜合成 → 卡点剪辑 → 手写字幕**。

这是《深海少女》手书 MV 的真实工程代码（v1 与 v2 两版），开源的是**代码、分镜数据和提示词**。

> **仓库里不包含**歌曲音频、歌词、角色设定图、AI 分镜图片和成片——版权和体积原因，见下面「不包含什么」。

## 能不能直接用？先看这里

| 你想做的事 | 现在能不能 |
|---|---|
| 看这套 MV 怎么做、抄思路 | ✅ 能，代码和分镜表都在这 |
| 拿分镜表 / 提示词改自己的视频 | ✅ 能，`v2/shotlist.py` 和 `v2/prompts.py` 直接改 |
| `git clone` 下来直接跑出片 | ❌ 不行，缺素材（音频 / 分镜图 / 字体）和 API key |
| 接自己的模型跑完整条管线 | ⚠️ 能，但要改几处，见下 |

跑起来至少要准备：

1. Python 3.10+，`pip install -r requirements.txt`；跑 `masks.py` 还要 `pip install rembg`
2. `ref/song.mp3`（你有版权的音频）+ `v2/lyrics_times.txt`（可先照 `lyrics_times.example.txt` 填）
3. 分镜图：用 `paint.py` 生成，或自己画好后放进 `v2/img/<key>.png`
4. 字体：`v2/fonts/KleeOne-SemiBold.ttf`、`LXGWWenKai-Medium.ttf`（都是开源字体，自行下载）
5. 一个兼容 OpenAI 接口的中转。代码里写死的是当时用的模型名，换成你自己的：
   - 出图：`gpt-image-2` / `gpt-image-2.6-sunburst` → 改 `v2/scripts/creds.py` 的 `IMAGE_MODELS` 和 `v2/prompts.py` 的 `model_for()`
   - 视觉质检：`gpt-6.1-sol` → 改 `v2/scripts/qa.py`
   - 歌词对齐交叉验证：`gemini-3.8-flash` → 改 `v1/align_gemini.py` 或 `v2/scripts/consensus.py`

另外：这是**实际工程文件**，不是打包好的库。里面还留着一些一次性脚本（probe / 检查用的），路径和字体名是按当时的 Windows 环境写的，换机器可能要顺手改一下。

## 目录

```
v1/            第一版：分镜图 + 推拉 + 叠化
  gen.py       调 relay 出图
  scenes.py    分镜/剧情数据
  render.py    合成渲染
  batch_gen.py 批量出图
  align_gemini.py  用 Gemini 听音频对歌词时间轴

v2/            第二版：手绘质感 + 高密度镜头（116 个镜头）
  shotlist.py  分镜表（时间 / 图片 key / 运镜 / 画面说明）
  beats.py     BPM、小节、拍点
  prompts.py   每个镜头的出图提示词（手绘 tegaki 风格、角色一致性）
  scripts/
    gen2.py    图像生成（支持参考图 / 编辑）
    paint.py   批量出图 + 自动质检 + 失败重试
    qa.py      解剖检查（多手、少手、肢体畸形）
    masks.py   rembg 分层遮罩（视差用）
    render2.py 合成渲染：boil 抖动、粒子、卡点闪白、手写双语字幕、纸纹
    contact.py 拼 contact sheet 检查
    ...

docs/storyboard_v2.md  分镜表（已删掉版权歌词列）
```

## 管线怎么跑

1. **分镜**：`v2/shotlist.py` 里 116 个镜头按小节网格排好（136.9 BPM）。想改节奏就改这里。
2. **出图**：`paint.py` 读 `prompts.py`，调 `gen2.py` 生成每张分镜，再用 `qa.py` 把图丢给视觉模型检查手和肢体，不合格就重试。
3. **分层**：`masks.py` 用 rembg 把人从背景里抠出来，渲染时做视差。
4. **渲染**：`render2.py` 按分镜表逐镜头合成——镜头运动、纸纹噪点、boil（每 3 帧抖动一次模拟手绘）、粒子、卡点闪白、叠化、字幕。
5. **检查**：`contact.py` 拼总览图；`--still t` 可以只渲染指定秒数的一帧。

```bash
pip install -r requirements.txt

# 可选：图像 / 质检用的中转（不设就只能跑渲染）
export SHINKAI_IMAGE_BASE_URL=https://your-relay/v1
export SHINKAI_IMAGE_API_KEY=sk-...
export SHINKAI_GPT_BASE_URL=https://your-relay/v1
export SHINKAI_GPT_API_KEY=sk-...

python v2/scripts/paint.py all
python v2/scripts/render2.py --out out.mp4
```

## 你自己要准备的东西

| 放哪 | 是什么 |
|---|---|
| `ref/song.mp3` | 你自己有版权的音频 |
| `v2/lyrics_times.txt` | 歌词时间轴，格式 `起|止|文本`；先参考 `lyrics_times.example.txt` |
| `v2/img/<key>.png` | 分镜图（`paint.py` 生成，或你自己画） |
| `v2/masks/<key>.png` | 分层遮罩（`masks.py` 生成） |
| `v2/fonts/` | 手写风字体（Klee One、LXGW WenKai 等，自行下载） |

## 不包含什么（版权说明）

- **歌曲和歌词**：《深海少女》（初音ミク）的词曲版权归原作者，仓库不含音频和歌词原文；`docs/storyboard_v2.md` 已把原分镜表里的歌词列删掉，`lyrics_times.example.txt` 里也只有占位文字。
- **角色形象**：「大肥鱼」是 DeepSeek 的拟人化二创形象，「小克」是 Claude 的拟人化二创形象。角色相关权利归各自公司，本项目是非商业二创，不提供角色设定图。
- **成片和分镜图**：AI 生成的图片与视频体积太大，也没有随仓库分发。

代码部分用 MIT 许可，见 `LICENSE`。
