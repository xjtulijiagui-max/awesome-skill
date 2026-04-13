# 常见问题解决方案

基于李家贵 94 个会话、765 条消息分析，总结 6 类高频问题及解决方案。

## 1. Python 环境问题（已解决）

**问题**：之前认为 Python 不可用（Windows Store stub）

**实际情况**：Python 3.12.10 完全可用
```
C:\Users\xjtul\AppData\Local\Programs\Python\Python312\python.exe
```

**症状**：之前 Claude Code 误判 Python 不可用，错误提示 `exit code 49`

**解决方案**：更新 CLAUDE.md，明确 Python 可用：
```markdown
## Environment
- Python 3.12.10 is available
- Node.js v24+ is available
- Both can be used — choose based on task requirements
```

**注意**：Windows 上可能有两个 python.exe：
- `C:\Users\xjtul\AppData\Local\Programs\Python\Python312\python.exe` ✅ 真正的 Python
- `C:\Users\xjtul\AppData\Local\Microsoft\WindowsApps\python.exe` ❌ Windows Store 存根

## 2. API 错误（403/503/504）

**问题**：频繁出现 API 错误，完全阻塞工作

**出现场景**：
- 会话开始时
- 并行子代理运行时
- 关键操作执行中

**解决方案**：

1. **实现重试机制**：
```javascript
// Node.js 重试示例
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(1000 * (i + 1)); // 指数退避
    }
  }
}
```

2. **并行任务预留失败补偿**：
```markdown
## Parallel Task Execution
- When using parallel subagents, ~35% may fail
- Implement retry: failed agent retries up to 3 times
- Always have sequential fallback ready
```

3. **备用方案准备**：
- API 失败时切换到本地 Node.js 处理
- 准备好离线工作模式

## 3. 大文件写入失败

**问题**：Write 工具写入大文件（CSS、含内联 SVG 的 HTML）失败

**阈值**：超过 50KB 的文件容易失败

**解决方案**：使用 Bash 分块写入

```bash
# 分块写入示例
# 先写头部
cat > large-file.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
EOF

# 追加内容块（每块 5-10KB）
echo '<title>Large File</title>' >> large-file.html

# 最后追加尾部
echo '</html>' >> large-file.html
```

CLAUDE.md 配置：
```markdown
## File Operations
- When writing large files (>50KB), use Bash echo/cat append redirection
- Break content into 5-10KB chunks to avoid Write tool limitations
```

## 4. 并行子代理高失败率

**问题**：14 个并行子代理，约 5 个失败（~35% 失败率）

**原因**：API 错误、权限问题、网络中断

**解决方案**：

1. **结构化并行任务提示**：
```markdown
Use parallel subagents for this task. Each agent should:
1. Report completion immediately after finishing
2. If it fails, retry the same task up to 3 times
3. Log the filename after each successful save

Coordinator should:
1. Track progress: completed / failed / remaining
2. Redistribute work from failed agents
3. Report real-time progress
```

2. **进度聚合**：
```
✅ Chapter 1-5 completed
⚠️ Chapter 6 failed (retrying 2/3)...
⚠️ Chapter 7 failed (retrying 2/3)...
⏳ Chapter 8-14 pending
```

3. **单次任务足够大时才并行**：小任务串行更快

## 5. 跨域 Canvas 问题

**问题**：HTML 实现 save-as-image 功能时，外部加载的 SVG 导致 canvas 污染

**症状**：`DOMException: Failed to execute 'toDataURL' on 'HTMLCanvasElement': Tainted canvas`

**解决方案**：SVG 内联到 HTML

```javascript
// ❌ 错误：外部加载 SVG
const svg = '<object data="diagram.svg" type="image/svg+xml"></object>';

// ✅ 正确：读取 SVG 内容并内联
const fs = require('fs');
const svgContent = fs.readFileSync('diagram.svg', 'utf8');
// 然后将 svgContent 直接写入 HTML 的 <svg> 标签中
```

CLAUDE.md 配置：
```markdown
## SVG and Canvas
- For save-as-image functionality, inline SVG content directly in HTML
- Never load external SVG files in canvas-based export
- Read SVG file content and embed it inline
```

## 6. 文档合并验证

**问题**：合并 22 个 Word 文件后，无法确认是否所有章节都存在

**原因**：章节标题格式不一致（数字 vs 标题），难以人工检查

**解决方案**：程序化验证

```javascript
// 合并后验证脚本
const fs = require('fs');
const content = fs.readFileSync('merged.docx', 'utf8');

const expectedChapters = [
  '第一章：引言',
  '第二章：基础知识',
  // ... 22 个章节
];

const missing = expectedChapters.filter(ch => !content.includes(ch));
if (missing.length > 0) {
  console.log(`❌ Missing ${missing.length} chapters:`, missing);
} else {
  console.log('✅ All chapters verified');
}
```

CLAUDE.md 配置：
```markdown
## Document Processing
- After merging/converting documents, programmatically verify all sections exist
- Check file count and scan for expected headers before declaring success
- Report exact count and list any missing sections
```

## 问题-解决索引

| 问题 | 解决要点 | 参考 |
|------|---------|------|
| Python 不可用 | Python 3.12.10 可用，更新 CLAUDE.md | 环境配置 |
| API 错误阻塞 | 重试机制 + 备用方案 + 离线模式 | 第 2 节 |
| 大文件写入失败 | Bash 分块写入（echo/cat） | 第 3 节 |
| 并行子代理高失败率 | 自动重试 + 进度聚合 + 串行备选 | 第 4 节 |
| Canvas 跨域错误 | SVG 内联到 HTML | 第 5 节 |
| 文档合并验证 | 程序化检查章节完整性 | 第 6 节 |
| 网络限制 | CDN 备选 + npm 镜像 + fastgit | CDN 列表 |
| 工具选择错误 | 明确 Python/Node.js 适用场景 | 工具链参考 |
