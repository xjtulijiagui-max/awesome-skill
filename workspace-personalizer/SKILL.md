---
name: workspace-personalizer
description: "OpenClaw workspace 开机配置向导。当用户提到自己的职业、岗位、主要输出物，或希望配置或刷新 OpenClaw 的配置文件时触发。也适用于用户说帮我配置 OpenClaw、初始化工作区、我想让 AI 更了解我的工作、刷新配置、设置 AI 搭档等场景。即使用户没有明确提到文件名，只要表达了让 AI 搭档更懂我的意图，也应触发。不适用于：用户已经在配置文件中填好了信息，只需要调用现有 skill 完成具体任务。"
---

# SKILL.md - OpenClaw Workspace Personalizer

## 概述

这是一个 **workspace 开机配置向导**，帮助用户配置/刷新 OpenClaw 的核心配置文件（IDENTITY.md / SOUL.md / USER.md / TOOLS.md / HEARTBEAT.md / AGENTS.md / MEMORY.md）。

当用户提到自己的职业、岗位、主要输出物，或希望配置/刷新 OpenClaw 时触发。
也适用于用户说"帮我配置 OpenClaw"、"初始化我的工作区"、"我想让 AI 更了解我的工作"、"刷新我的配置"、"设置我的 AI 搭档"等场景。

**不适用**：用户已经在配置文件中填好了信息，只需要调用现有 skill 完成具体任务。

---

## 主流程（4步走）

### 第1步：收集信息（references/questionnaire.md）

通过交互式问卷收集用户信息：

- **第一层（必填）**：职业、主要输出物、服务对象/行业、协作风格偏好、AI搭档名字
- **第二层（推荐）**：基于第一层动态生成的追问（工具偏好、工作节奏等）
- **第三层（可选）**：上传典型输出物样本、过往AI工具使用体验

每条信息收集时，同步展示推断逻辑（references/reverse-engineer.md），要求用户确认。

### 第2步：生成预览（scripts/generate_config.py）

基于收集到的信息，生成各配置文件的候选内容（带 `{{变量名}}` 标记）。

**不做任何写入**——只生成预览文本。

### 第3步：用户确认预览（scripts/diff_preview.py）

调用 `diff_preview()` 展示变更预览：
- 新建文件：标注"新增"
- 已有文件：对比当前内容与新内容，标注"变更"
- 未变更部分：保留用户已有内容

用户逐文件确认或批量确认。

### 第4步：备份并写入（scripts/backup_and_write.py）

用户确认后：
1. 对每个目标文件执行 `backup_file()`，备份到 `/workspace/.openclaw-backup/`
2. 执行 `write_with_backup()` 写入新内容
3. 若任何一步失败，执行 `rollback()` 回滚

---

## 关键约束

1. **必须预览**——写入前必须展示 diff，不允许静默写入
2. **必须确认**——每条推断逻辑必须向用户展示，不允许静默推断
3. **必须备份**——写入任何文件前必须先备份，允许回滚
4. **幂等性**——同样的输入跑两次，结果一致；自动生成块可安全覆盖，用户内容不受影响
5. **渐进加载**——只加载当前步骤需要的 reference，按需读取

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 输入不足 | 追问，不允许跳过必填项 |
| 输入矛盾 | 暂停，列出矛盾点，要求用户澄清 |
| 写入失败 | 自动回滚，报告失败文件 |
| 用户拒绝确认 | 停止写入，保留原文件 |

---

## 文件结构

```
workspace-personalizer/
├── SKILL.md                    ← 主入口
├── references/
│   ├── questionnaire.md         ← 三层问卷
│   ├── reverse-engineer.md     ← 推断规则映射表
│   ├── templates.md             ← 配置文件模板
│   └── file-specs.md           ← 字段规范
├── scripts/
│   ├── diff_preview.py         ← 变更预览
│   ├── backup_and_write.py     ← 备份+幂等写入
│   └── generate_config.py      ← 配置生成
├── assets/
│   └── default-soul-snippets.json ← 职业 SOUL 预设
└── evals/
    └── evals.json              ← 测试用例
```
