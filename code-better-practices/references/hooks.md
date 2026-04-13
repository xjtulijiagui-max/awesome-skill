# Hooks 系统详解

李家贵验证过的 Claude Code Hooks 配置，已成功配置飞书私信通知。

## Hooks 配置层次

| 优先级 | 配置文件 | 说明 |
|--------|---------|------|
| 1 | hooks-config.local.json | 本地覆盖，git 忽略 |
| 2 | hooks-config.json | 团队共享 |
| 3 | ~/.claude/settings.json | 全局个人默认 |

## 李家贵已配置的 Hooks

### 1. SessionStart — 会话开始检查

文件：`.claude/hooks/session-start.js`

功能：
- 检查 Python/Node.js 版本
- 显示 Git 状态
- 显示 HTML Generator Agent 可用性

### 2. PostToolUse — HTML 验证

文件：`.claude/hooks/html-validator.js`

功能：
- 检查 DOCTYPE 是否存在
- 检查 viewport meta 标签
- 检查基本 HTML 结构

```javascript
// 运行方式
node .claude/hooks/html-validator.js $FILE_PATH
```

### 3. TaskCompleted — 任务完成总结 + 飞书私信通知

文件：`.claude/hooks/task-completed.js` + `.claude/hooks/feishu-task-notification.js`

配置（hooks-config.json）：
```json
{
  "TaskCompleted": {
    "enabled": true,
    "command": "node .claude/hooks/task-completed.js && node .claude/hooks/feishu-task-notification.js"
  }
}
```

### 4. PreToolUse — Bash 安全检查

文件：`.claude/hooks/bash-safety-check.js`

检测危险命令模式：`rm -rf`、`format`、`del /q`

### 5. SubagentStart — Agent 启动欢迎

显示欢迎信息和已加载的设计偏好。

## 飞书私信通知配置（已验证成功）

### 前置条件

李家贵已完成的配置：
1. ✅ lark-cli 已安装（`C:\Users\xjtul\AppData\Roaming\npm\lark-cli`）
2. ✅ lark-cli 已登录（李家贵账号）
3. ✅ user_id 已获取：`ou_e7279fdd94c43c1558e9f1f7a5b164e0`

### 配置步骤

**步骤 1**: 安装 lark-cli
```bash
npm install -g lark-cli
```

**步骤 2**: 登录飞书
```bash
lark-cli auth login --recommend
```

**步骤 3**: 创建配置文件

`.claude/hooks/feishu-config.json`:
```json
{
  "user_id": "YOUR_USER_OPEN_ID",
  "auto_detect": true,
  "notify_on": {
    "task_completed": true,
    "error": true,
    "long_task": true,
    "long_task_threshold": 30000
  }
}
```

**步骤 4**: 启用通知

在 `hooks-config.json` 的 TaskCompleted 中添加：
```json
"command": "node .claude/hooks/task-completed.js && node .claude/hooks/feishu-task-notification.js"
```

### 通知效果

任务完成后飞书私信收到：
```
✅ Claude Code 任务完成
📁 项目: my-project
🕐 时间: 2026-04-13 18:00:00

📄 修改文件 (2个):
➕ new-page.html
✏️ config.json
```

### 故障排查

| 问题 | 解决方案 |
|------|---------|
| lark-cli 未安装 | `npm install -g lark-cli` |
| lark-cli 未登录 | `lark-cli auth login --recommend` |
| 获取 user_id 失败 | 运行 `lark-cli contact +get-user` 手动查看 |
| 权限错误 | 重新登录 `lark-cli auth login` |

### 相关文件

- `.claude/hooks/feishu-task-notification.js` — 飞书通知脚本
- `.claude/hooks/feishu-config.example.json` — 配置模板
- `.claude/hooks/feishu-config.json` — 实际配置
- `.claude/hooks/FEISHU_SETUP.md` — 详细设置指南

## 生命周期钩子完整列表

| 事件 | 说明 |
|------|------|
| PreToolUse | 工具执行前 |
| PostToolUse | 工具执行后 |
| UserPromptSubmit | 用户提交提示 |
| Notification | 通知触发 |
| Stop | 停止时 |
| SubagentStart | Subagent 启动 |
| SubagentStop | Subagent 停止 |
| SessionStart | 会话开始 |
| SessionEnd | 会话结束 |
| TaskCompleted | 任务完成 |
| ConfigChange | 配置变更 |

## 禁用 Hooks

在 `settings.local.json` 中设置：
```json
{
  "disableAllHooks": true
}
```
