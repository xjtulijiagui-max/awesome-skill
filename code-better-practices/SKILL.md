---
name: claude-code-best-practices
description: Claude Code 最佳实践配置技能，专为李家贵定制。基于其 765 条消息、94 个会话的使用分析，封装其验证过的配置方法论和工作流。包括：CLAUDE.md 最优配置（含 Python/Node.js 环境偏好、蓝紫色渐变设计风格）、自定义 Agent 创建（html-generator）、飞书私信通知 Hooks、Hooks 系统详解、以及 6 类常见问题的解决方案。当李家贵提到"配置 Claude Code"、"创建 Agent"、"配置 Hooks"、"优化工作流"、"Claude Code 最佳实践"、"飞书通知"、"Python 环境"时触发。
---

# Claude Code Best Practices - 李家贵专属配置

本 Skill 包含李家贵验证过的 Claude Code 配置方法论，基于 765 条消息、94 个会话（2026-03-14 至 2026-04-12）的使用分析。

## 核心配置原则

1. **Python 3.12.10 可用** — Windows Store stub 问题已修复，不再需要强制使用 Node.js
2. **Node.js v24+ 可用** — 文档处理首选 Node.js 库（docx/pptxgenjs/jszip）
3. **飞书私信通知** — 任务完成自动发通知到个人飞书
4. **离线优先** — 网络限制（403/503 错误）频繁，需准备 CDN 备选和镜像

## 立即可用的配置

### 1. CLAUDE.md 最优配置

李家贵的 CLAUDE.md 应包含以下关键配置：

```markdown
## Environment
- Python 3.12.10 is available at: `C:\Users\xjtul\AppData\Local\Programs\Python\Python312\python.exe`
- Node.js v24+ is available
- Both Python and Node.js can be used for scripting tasks
- pandoc is NOT available. Use Python libraries (python-docx, python-pptx) or Node.js libraries (docx, officegen, pptxgenjs) for document conversions.

## Document Processing
- For document conversion tasks (Word, PPT, HTML), both Python and Node.js are available
- Choose Python for: pandas, numpy, data analysis
- Choose Node.js for: Web requests (axios), file operations (fs-extra), HTML generation

## HTML Design Style
- Primary color: Blue-purple gradient (e.g., #667eea → #764ba2)
- Card border-radius: 16-22px
- Navigation: Fixed top navbar
- Font: Inter, -apple-system, BlinkMacSystemFont, sans-serif

## File Operations
- When writing large files (>50KB), use Bash with echo/cat append redirection instead of Write tool
- Break large content into chunks (5-10KB each) to avoid size limitations

## SVG and Canvas
- For cross-origin canvas issues when implementing save-as-image, inline SVG content directly in HTML
- Never load external SVG files in canvas-based export functionality

## Parallel Subagent Workflow
- When using parallel subagents for batch generation, ~35% may fail due to API errors
- Always implement retry mechanism: failed agent retries up to 3 times before escalating
- Report progress after each completion, log filenames for tracking
```

### 2. 推荐的 CLAUDE.md 增量配置

来自 Insights 报告的建议（全部已验证推荐添加）：

```markdown
## Environment Constraints
- For HTML-to-PPTX conversions and Word document manipulation, use 'frontend-design' skill or direct Node.js scripts with pptxgenjs, docx, jszip rather than external CLI tools that may fail due to network restrictions.

## Parallel Task Execution
- When using parallel subagents for batch file generation (chapters, slides, etc.), implement explicit file verification and retry mechanism — approximately 35% of subagents may fail due to API errors.

## Internationalization
- For Chinese document processing (inserting 篇 titles, 导语 content), analyze document structure first to identify correct insertion points before modifying.
```

## 自定义 Agent 和 Command

### 创建专用 HTML Generator Agent

李家贵已验证有效的 Agent 配置（`.claude/agents/html-generator.md`）：

```markdown
---
name: html-generator
description: PROACTIVELY invoke when user needs to create HTML pages, web applications, or frontend interfaces. Specializes in Vue+Element UI, Bootstrap 5, and Tailwind CSS projects.
model: sonnet
tools: Read, Write, Edit, Glob, Bash, Skill
skills: multi-page-hub, vue-element-app
maxTurns: 50
---

# HTML Generator Agent

[完整 Agent 配置见 references/agents-commands.md]
```

### 创建 /html 快捷命令

李家贵验证有效的 Command 配置（`.claude/commands/html.md`）：

```markdown
---
name: html
description: Create HTML pages, web applications, or frontend interfaces using the html-generator agent
argument-hint: [description of what to build]
---

Invoke the html-generator agent to create HTML pages...
```

详见 [references/agents-commands.md](references/agents-commands.md)

## Hooks 系统配置

### 李家贵已配置的 Hooks

| Hook | 触发时机 | 功能 | 状态 |
|------|---------|------|------|
| SessionStart | 会话开始 | 检查 Python/Node.js/Git 状态 | ✅ |
| PostToolUse (Write) | HTML 文件创建/编辑 | HTML 语法验证 | ✅ |
| TaskCompleted | 任务完成 | 显示完成信息 + 飞书私信通知 | ✅ |
| PreToolUse (Bash) | Bash 执行前 | 危险命令警告 | ✅ |
| SubagentStart | Agent 启动 | 显示欢迎信息 | ✅ |

### 飞书私信通知配置（已验证成功）

李家贵已通过 lark-cli 登录配置了飞书私信通知，配置文件位于 `.claude/hooks/feishu-config.json`：

```json
{
  "user_id": "ou_e7279fdd94c43c1558e9f1f7a5b164e0",
  "auto_detect": true,
  "notify_on": {
    "task_completed": true
  }
}
```

通知触发命令：
```bash
node .claude/hooks/task-completed.js && node .claude/hooks/feishu-task-notification.js
```

详见 [references/hooks.md](references/hooks.md)

## 推荐工具链

### Node.js 库（首选）

| 任务 | 推荐库 | 备注 |
|------|--------|------|
| Word 文档 | docx | 跨平台，无需 Python |
| PPT 生成 | pptxgenjs | 原生 JS，支持中文 |
| 文件压缩 | jszip | 处理 zip/office 文件 |
| Excel 操作 | exceljs | 读写 xlsx |
| HTTP 请求 | axios / node-fetch | 文档下载 |
| 文件操作 | fs-extra | 增强型 fs |

### Python 库（可用）

| 任务 | 推荐库 |
|------|--------|
| Word 文档 | python-docx |
| PPT 生成 | python-pptx |
| 数据处理 | pandas, numpy |
| PDF 生成 | reportlab |

### CDN 备选（应对网络限制）

```html
<!-- Bootstrap -->
https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js

<!-- Icon -->
https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css

<!-- 备选 CDN -->
<!-- unpkg.com → cdnjs.cloudflare.com -->
<!-- fastgit.org (GitHub 镜像) -->
<!-- npmmirror.com (npm 镜像): npm config set registry https://registry.npmmirror.com -->
```

## 常见问题解决

详见 [references/troubleshooting.md](references/troubleshooting.md)，包含：

1. **Python Windows Store stub 问题** — 已解决（Python 3.12.10 实际可用）
2. **API 错误（403/503/504）** — 频繁出现，需准备重试机制和备选方案
3. **大文件写入失败** — 使用 Bash 分块写入（echo/cat 追加方式）
4. **并行子代理失败率 ~35%** — 必须配置自动重试（最多 3 次）
5. **跨域 Canvas 问题** — SVG 内联到 HTML 避免外部加载
6. **文档合并验证** — 合并后必须程序化验证所有章节是否存在

## 参考文件

- [references/agents-commands.md](references/agents-commands.md) — Agent/Command 创建完整指南
- [references/hooks.md](references/hooks.md) — Hooks 系统详解（含飞书通知配置）
- [references/troubleshooting.md](references/troubleshooting.md) — 常见问题解决方案
