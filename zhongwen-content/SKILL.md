---
name: zhongwen-content
description: >
  根据知识萃取 JSON 生成精良的 HTML 报告页面。TRIGGER when: 用户需要"生成交付物"、
  "生成萃取报告"、"convert extraction to HTML"、完成知识萃取后需要输出展示材料。
  自动处理单文件 JSON 和综合萃取 JSON（多文档合并）。
  SKIP: 知识萃取本身（那是 knowledge-interviewer 的职责）、PPTX/DOCX 生成（按需单独调用 pptx/docx skill）。
---

# 中文内容交付物生成器 (zhongwen-content)

## 功能

读取 knowledge-interviewer 输出的萃取 JSON，基于预置 HTML 模板填充 slot，生成自包含的 HTML 报告页面。

**自动适配两种 JSON 输入：**
- **单文件萃取 JSON**：单一来源的萃取结果
- **综合萃取 JSON**（多文档合并）：metadata.source 包含多个来源，overview 覆盖多主题

## 硬约束

1. **必须先读模板** — 第一步永远是 Read 模板文件，不重新设计 CSS/JS
2. **只替换 slot** — 模板中 {{SLOT_NAME}} 占位符，其他代码一字不改
3. **默认只输出 HTML** — 不生成 PPTX/DOCX（除非用户显式要求，且应单独调用 pptx/docx skill）
4. **不创建/修改 skill** — 不新建或修改任何 SKILL.md 文件
5. **无残留 slot** — 输出前确认所有 {{...}} 占位符已替换
6. **全自动模式** — 不向用户提问、不请求确认、不等待

## 执行步骤

### 步骤 1：读取 HTML 模板

```
Read: C:\Users\xjtul\.claude\projects\C--Users-xjtul\templates\report-template.html
```

模板已内嵌完整的 CSS/JS（Tailwind CDN + 自定义样式 + 粒子特效 + 导航切换）。
只需替换 7 个 slot，不修改任何样式代码。

### 步骤 2：读取萃取 JSON

读取 knowledge-interviewer 输出的 JSON 文件。
自动识别是单文件萃取还是综合萃取（检查 `metadata.material_type` 或 `metadata.source` 字段）。

### 步骤 3：填充 7 个 Slot

| Slot | 内容来源 | 示例 |
|------|---------|------|
| `{{REPORT_TITLE}}` | JSON 的 `title` 字段 | 平安基金AI实践知识萃取报告 |
| `{{TOPBAR_ICON}}` | 按产品类型选择图标 | fas fa-brain |
| `{{TOPBAR_TITLE}}` | 从 title 提取平台/产品名 | 平安基金 |
| `{{TOPBAR_SUBTITLE}}` | 萃取日期 + 素材类型 | 2026年4月 · 综合萃取报告 |
| `{{SIDEBAR_SUBTITLE}}` | 日期 + 来源摘要 | 2026-04-29 · 四份调研文档 |
| `{{SIDEBAR_ITEMS}}` | JSON 章节结构动态生成 | `<li class="nav-item">...` |
| `{{CONTENT_SECTIONS}}` | JSON 全部内容渲染为 section 块 | `<section class="section">...` |

### SIDEBAR_ITEMS 生成规则

- 一级菜单项对应 JSON 顶层章节（core_products、methodology_framework 等）
- 有子模块的产品（sub_modules）用可展开的 submenu
- 编号使用 `.nav-num` 样式
- 综合萃取 JSON 的章节顺序与单文件一致

### CONTENT_SECTIONS 生成规则

- 每段用 `<section class="section" id="sec-N">` 包裹
- 标题用 `.section-header > .accent-bar + .sec-num + h2`
- 产品卡片用 `.card` + `.card-tag` + `.tag-*` 类
- 子模块用 `.grid-2` 或 `.grid-3` 网格布局
- 金句用 `blockquote.insight` 类（左侧金色边框 + 引号图标）
- 方法论步骤用 `.step-list` + `.flow-container`
- 案例用 `.case-card` 格式
- 知识缺口用 `.gap-list` + `.priority-high/.priority-mid/.priority-low`
- 竞争洞察用 `.card` + `.grid-2` 网格
- 未来方向用 `.card` 列表

### 步骤 4：验证与输出

1. 确认无残留 `{{...}}` 占位符（Tailwind config 中的 `{{}}` 除外）
2. 确认 SIDEBAR_ITEMS 数量与 CONTENT_SECTIONS 对应
3. 写入 HTML 文件
4. 报告文件路径和大小

**文件命名规则**：
- 与输入 JSON 同名，后缀改为 .html
- 默认输出到 JSON 同目录

## 模型选择

**必须使用 Sonnet**（`model: "sonnet"`）。渲染型任务（JSON→HTML），Sonnet 更快且质量足够。

## 模板 CSS 类速查

| 类名 | 用途 |
|------|------|
| `.card` | 通用内容卡片 |
| `.card-tag` + `.tag-base/.tag-star/.tag-mature/.tag-new/.tag-tool` | 产品标签 |
| `.grid-2` / `.grid-3` / `.grid-4` | 双列/三列/四列网格 |
| `.module-card` | 子模块卡片（顶部分色条） |
| `.case-card` | STAR2 案例卡片（左侧粗边框） |
| `.insight` | 金句引用（深色背景+左侧金色边框+引号） |
| `.flow-container` | 流程图容器（flexbox横向排列） |
| `.flow-step` | 流程图单步（圆形图标+标题+描述） |
| `.step-list` | 步骤列表 |
| `.gap-list` + `.priority-high/.priority-mid/.priority-low` | 知识缺口列表 |
| `.section-header` + `.accent-bar` + `.sec-num` | 章节标题 |
| `.topbar` / `.sidebar` / `.main-content` | 固定布局框架 |
| `.nav-list` / `.nav-item` / `.submenu` | 侧边栏导航 |

## 与其他 Skill 的关系

- **knowledge-interviewer** → 产出 JSON（上游）
- **zhongwen-content** → JSON → HTML（本 skill）
- **pptx** / **docx** → 如需 PPT/Word，由主对话单独调用，不在本 skill 中生成
