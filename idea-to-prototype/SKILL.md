---
name: idea-to-prototype
description: |
  从一个产品idea和参考图出发，自动完成设计系统文档生成、低保真线框图、高保真UI原型全套流程。
  当用户描述一个产品概念（APP/网页/小程序），并提供一张视觉参考图时，激活此技能。
  适用场景：产品设计、原型制作、UIUX概念验证、创业团队MVP。
---

# Idea → 高保真原型技能

用户输入：**产品概念描述** + **参考图URL**，输出：**完整高保真UI原型图片组**。

## 整体流程（3步，自动串联）

```
Step 1 → 设计系统文档（Markdown）
Step 2 → 低保真线框图（HTML）
Step 3 → 高保真UI原型（图片）← 最终交付物
```

---

## Step 1：生成设计系统文档

**目标**：根据用户提供的 idea 和核心色系，生成完整的设计系统 Design Tokens。

**执行方式**：直接用 LLM 根据下方提示词模板生成设计系统文档。

**提示词模板**：

```
# 角色与目标
你是一位顶级的UI/UX设计系统架构师AI。基于用户提供的极简信息，生成一份全面、结构化且对AI编程极其友好的设计系统文档。

# 用户输入

## 产品需求
[产品概念描述]

## 核心色系（用户已提供）
--primary-100: [从参考图提取的主色，建议从参考图中提取5-7种主色]
--accent-100: [辅助色/点缀色]
--text-100: [深色文字]
--text-200: [浅色文字/次要文字]
--bg-100: [背景色]
--bg-200: [卡片/区块背景]
（如果没有提供颜色，从参考图中智能提取并说明）

# 你的任务
请严格按照以下步骤生成设计系统文档：

1. **颜色（Colors）**：将用户提供的核心色扩展为完整的色板（主色阶100-900、中性灰阶、语义色：success/error/warning/info）
2. **字体（Typography）**：定义 fontFamily、fontWeight、fontSize、lineHeight；选择与产品气质匹配的免费字体（中文推荐：思源黑体/阿里巴巴普惠体；英文推荐：Inter/Poppins）
3. **间距（Spacing）**：基于8px网格，定义 4/8/12/16/24/32/48/64px 间距单位
4. **效果（Effects）**：定义 borderRadius、boxShadow、blur 等
5. **组件（Components）**：主动识别并定义：Button、Input、Card、Modal、TabBar、Avatar、Badge、Tag

# 输出格式
输出一个完整的 Markdown 文档，所有技术规范用 YAML 代码块包裹。
```

**产物**：`/workspace/prototype-workspace/{project_name}/design-system.md`

---

## Step 2：生成低保真线框图 HTML

**目标**：将设计系统转化为可预览的多页面手机界面 HTML 原型（黑白线框图风格）。

**执行方式**：直接用 LLM 生成单一 HTML 文件，参考 Step 1 提示词模板中的设计系统。

**关键实现要求**：
- 技术栈：`HTML + Tailwind CSS CDN + FontAwesome Icons`
- 画板：375×812px 手机模拟框（带 1px #ccc 边框）
- iOS 状态栏：时间 9:41、信号、电池图标
- 内容区独立滚动，底部 TabBar 固定
- 页面网格排列（每行 3-4 个预览）
- 所有 CSS 变量必须从设计系统中提取，使用 `var(--xxx)` 调用
- **禁止使用彩色，所有颜色仅为 #000 / #fff / #ccc / #eee 等灰度色**
- 图标：FontAwesome 免费图标
- 图片占位：`https://source.unsplash.com/random/400x300?&nature,calm`（根据产品调性调整关键词）

**提示词模板**：

```
# 角色
你是一位前端架构师AI，严格遵循设计系统文档，生成低保真黑白线框图HTML原型。

# 输入
设计系统文档路径：/workspace/prototype-workspace/{project_name}/design-system.md
产品需求：来自 Step 1

# 技术要求
1. <style>中用:root 定义所有 CSS 自定义变量（来自设计系统）
2. Tailwind CSS CDN + FontAwesome CDN
3. 页面结构：
   - 网格容器，每行3-4个375×812px手机画板
   - 每个画板：iOS状态栏 + 独立滚动内容区 + 固定底部TabBar
4. 必须包含的核心页面：
   - 引导页/欢迎页（1-2个）
   - 登录/注册页
   - 首页/主Tab页
   - 核心功能页面（根据产品需求，至少3个不同功能页）
   - 个人中心/设置页
5. 所有颜色只能用灰度（#000/#333/#666/#999/#ccc/#eee/#fff）
6. 禁止任何彩色
7. 添加按钮、卡片的hover微动效（transform: scale(0.98)）
```

**产物**：`/workspace/prototype-workspace/{project_name}/wireframe.html`
**预览**：用 `exec` 启动本地 HTTP server 或直接提供文件路径

---

## Step 3：生成高保真 UI 原型图片

**目标**：以参考图为视觉模板，为每个页面生成高保真的彩色 UI 原型图。

**核心方法**：使用 `image_synthesize` 工具的 **img2img（编辑/变换）** 模式：
- 将低保真线框图截图作为 `input_files`
- 将参考图 URL 作为 `input_urls`
- Prompt 描述：参考图的视觉风格 + 线框图页面内容

**执行步骤**：

### 3.1 先用浏览器截图线框图
```python
browser(action="open", url="file:///workspace/prototype-workspace/{project_name}/wireframe.html")
# 等待加载后截图
browser(action="screenshot", fullPage=false)
```

### 3.2 为每个页面生成高保真图

**为每个关键页面单独生成**（不要一次生成太多），每个页面使用以下参数：

```
requests:
  - prompt: |
      [参考图的完整视觉风格描述] + 
      "High-fidelity mobile UI design, [页面名称], [页面核心内容描述], 
      precise alignment, [产品调性描述], professional app design, 4K quality"
    input_files: [wireframe_screenshot.png]
    input_urls: [reference_image_url]
    output_file: /workspace/prototype-workspace/{project_name}/hifi_1_home.png
    aspect_ratio: 9:16
    resolution: 2K
```

**Prompt 构造原则**：
- 前半句描述参考图的风格（颜色、圆角、阴影、字体风格、卡片风格）
- 后半句描述目标页面的内容和布局
- 强调 "high-fidelity mobile UI, [product vibe]"

**需要生成的页面**（至少 4 个）：
1. 首页/主Tab
2. 核心功能页 1（如：列表/看板页）
3. 核心功能页 2（如：详情/编辑页）
4. 个人中心/设置页

### 3.3 提供最终交付物

所有高保真图片 + 线框图 HTML → 整理到 `/workspace/prototype-workspace/{project_name}/` 目录

**向用户展示方式**：
```
<deliver_assets>
<item>
<path>/workspace/prototype-workspace/{project_name}/hifi_1_home.png</path>
</item>
...
</deliver_assets>
```
附上每个页面的简短说明。

---

## 项目目录结构

```
/workspace/prototype-workspace/{project_name}/
├── design-system.md        # 设计系统文档
├── wireframe.html          # 低保真线框图（可浏览器打开）
├── hifi_1_首页.png         # 高保真原型图
├── hifi_2_功能页.png
├── hifi_3_详情页.png
└── hifi_4_设置页.png
```

---

## 视觉参考图分析（必须步骤）

在生成高保真原型前，**必须先用 `images_understand`** 分析参考图，获取其视觉特征：

```json
{
  "image_info": [
    {
      "url": "[用户提供的参考图URL]",
      "prompt": "描述这张图的视觉风格：主色调、字体风格、圆角大小、阴影效果、卡片风格、按钮样式、整体氛围。用中文回答。"
    }
  ]
}
```

将分析结果融入 Step 1 的设计系统和 Step 3 的 img2img prompt 中。

---

## 质量检查清单

生成完成后，自查以下内容：
- [ ] 设计系统包含完整的 Colors/Typography/Spacing/Effects/Components
- [ ] 线框图 HTML 所有颜色均为灰度，无彩色
- [ ] 每个手机画板有 iOS 状态栏和固定 TabBar
- [ ] 高保真图片风格与参考图一致
- [ ] 所有页面关键内容清晰可读
- [ ] 交付物目录已整理好
