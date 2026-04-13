# Agents 和 Commands 创建指南

李家贵验证过的 Agent/Command 创建方法论。

## Agent vs Command vs Skill 选型标准

| 工具 | 适用场景 | 示例 |
|------|---------|------|
| **Agent** | 独立上下文、多工具组合、长时任务 | HTML Generator、代码审查Agent |
| **Command** | 工作流模板、提示注入、快速调用 | /html、/weather-orchestrator |
| **Skill** | 跨会话复用知识、复杂多步骤流程 | 飞书文档Skill、多平台文案Skill |

## 创建 HTML Generator Agent

路径：`.claude/agents/html-generator.md`

```markdown
---
name: html-generator
description: PROACTIVELY invoke when user needs to create HTML pages, web applications, or frontend interfaces. Specializes in Vue+Element UI, Bootstrap 5, and Tailwind CSS projects based on user's established preferences.
model: sonnet
tools: Read, Write, Edit, Glob, Bash, Skill
skills: multi-page-hub, vue-element-app
maxTurns: 50
---

# HTML Generator Agent

李家贵的 HTML 生成专用 Agent，已内置以下知识：

## 技术栈选择

| 项目类型 | 技术栈 | CDN |
|---------|--------|-----|
| 企业应用 | Vue 2 + Element UI + ECharts | CDN 引入 |
| 简洁展示 | Tailwind CSS | CDN 引入 |
| 业务系统 | Bootstrap 5 | CDN 引入 |

## 设计风格

- **主色调**: 蓝紫渐变 `#667eea → #764ba2`
- **卡片圆角**: 16-22px
- **导航栏**: 固定顶部
- **字体**: Inter, -apple-system, BlinkMacSystemFont

## 布局偏好

- 左侧导航 + 右侧 iframe 多页面结构
- 蓝紫色渐变 header
- 卡片式内容区
- 固定宽度容器（max-width: 1200px）

## 工具链

- Node.js 用于文件操作和脚本
- Bash 分块写入大文件（>50KB）
- CDN 优先，避免构建工具

## 预加载 Skills

- multi-page-hub: 多页面集成
- vue-element-app: Vue+Element UI 原型

当用户说"创建XX页面"、"做一个XX系统"时，自动调用此 Agent。
```

## 创建 /html 快捷命令

路径：`.claude/commands/html.md`

```markdown
---
name: html
description: Create HTML pages, web applications, or frontend interfaces using the html-generator agent with established preferences (Vue+Element UI, Bootstrap 5, Tailwind CSS)
argument-hint: [description of what to build]
---

Invoke the html-generator agent to create HTML pages, web applications, or frontend interfaces.

The agent specializes in:
- Vue 2 + Element UI + ECharts (enterprise applications)
- Bootstrap 5 (business systems)
- Tailwind CSS (simple landing pages)
- Blue-purple gradient design style (#667eea → #764ba2)
- Left sidebar + right iframe multi-page structure

Always:
1. Apply the user's established design style and color scheme
2. Use CDN for all library imports (no build tools)
3. Use Bash with append redirection for files >50KB
4. Inline SVG directly in HTML for canvas export functionality
```

## 创建通用 Workflow Command

李家贵的 Command → Agent → Skill 架构模式（来自 shanraisshan/claude-code-best-practice）：

```
Command（入口） → Agent（核心逻辑） → Skill（按需调用）
```

示例 - 天气 SVG 生成：
```
/weather-orchestrator (Command)
    ↓
weather-agent (Agent, 预加载 weather-fetcher Skill)
    ↓ 返回结果
weather-svg-creator (Standalone Skill, 按需调用)
    ↓
生成 SVG 天气卡片
```

关键规则：
- **不要用 Bash 调用其他 Subagent** — 必须使用 Agent 工具
- **Command 调用 Agent，Agent 预加载 Skills** — 工作流编排模式
- **约 50% 上下文时手动执行 /compact** — 保持效率

## Git 提交规则

每个文件单独提交，不要捆绑多个文件到一次提交：

```bash
# Commit 1
git add README.md
git commit -m "Update README with new features"

# Commit 2
git add best-practice/claude-subagents.md
git commit -m "Add subagent documentation"
```

好处：Git 历史更清晰，易于审查、回滚或拣选单个变更。
