---
name: tencent-docs-mcp
version: 1.0.0
description: "腾讯文档 MCP — docs.qq.com 在线文档全功能操作封装。涵盖智能文档（SmartCanvas）、在线表格（Sheet）、文档（DOC）、OCR、网页剪藏、幻灯片等全部工具。当用户提到腾讯文档、docs.qq.com、需要创建/编辑/读取在线文档时使用。核心能力：创建文档、读取内容、编辑文档、管理文件、搜索文件、OCR识别、网页剪藏、AI生成PPT。"
metadata:
  emoji: "📝"
  primaryEnv: "TENCENT_DOCS_TOKEN"
  tencentTokenMode: "custom"
  tokenUrl: "https://docs.qq.com/scenario/open-claw.html"
---

# 腾讯文档 MCP Skill

## 工具调用方式

所有工具通过 `mcporter` 调用，格式：

```bash
mcporter call "tencent-docs" "<工具名>" --args '<JSON参数>'
```

## 工具分类速查

| 类别 | 工具 |
|------|------|
| **创建文档** | `manage.create_file` `create_smartcanvas_by_mdx` `create_mind_by_markdown` `create_flowchart_by_mermaid` `create_slide` |
| **读取文档** | `get_content` `smartcanvas.read` `smartcanvas.list_pages` `smartcanvas.find` |
| **编辑文档** | `smartcanvas.edit` `smartcanvas.append_insert_smartcanvas_by_markdown` |
| **文件管理** | `manage.copy_file` `manage.move_file` `manage.delete_file` `manage.rename_file_title` `manage.set_privilege` |
| **目录/搜索** | `manage.list_folder` `manage.search_file` `manage.query_folder_meta` |
| **在线表格** | `sheet.*` 系列（见下方 Sheet 工具区） |
| **智能表格** | `smartsheet.*` 系列（见下方 SmartSheet 工具区） |
| **知识空间** | `create_space` `delete_space_node` |
| **OCR / 剪藏** | `ocr.extract` `ocr.toword` `ocr.toexcel` `scrape_url` `scrape_progress` |
| **文档(DOC)** | `doc.*` 系列（见下方 DOC 工具区） |
| **导入导出** | `manage.pre_import` `manage.async_import` `manage.import_progress` `manage.export_file` `manage.export_progress` |
| **辅助** | `upload_image` `check_skill_update` |

---

## 🔑 鉴权流程（首次使用必须执行）

### 第一步：检查状态

```bash
bash "$SKILL_DIR/setup.sh" tdoc_check_and_start_auth
```

| 输出 | 含义 | 处理 |
|------|------|------|
| `READY` | ✅ 已授权，直接干活 | — |
| `AUTH_REQUIRED:<url>` | 需授权 | 向用户展示链接，等用户回复"已完成授权" |
| `ERROR:*` | 错误 | 展示错误信息，引导走第三步 |

### 第二步：用户确认后取 Token

用户回复"已完成授权"后：

```bash
bash "$SKILL_DIR/setup.sh" tdoc_fetch_token
```

| 输出 | 含义 | 处理 |
|------|------|------|
| `TOKEN_READY` | ✅ 成功 | 继续干活 |
| `ERROR:not_authorized` | 未完成授权 | 提示用户去浏览器完成 |
| `ERROR:expired` | Token 过期 | 引导重新获取 Token |

### 第三步：人工兜底

访问 https://docs.qq.com/scenario/open-claw.html 获取 Token，然后配置：

```bash
mcporter config add tencent-docs "https://docs.qq.com/openapi/mcp" \
    --header "Authorization=$Token" \
    --transport http \
    --scope home
```

> 💡 Token 配置一次，`tencent-docs` / `tencent-docengine` / `tencent-sheetengine` 三个服务共用。

---

## 🎯 场景路由

| 任务 | 推荐工具 | 说明 |
|------|---------|------|
| 新建文档（推荐格式） | `create_smartcanvas_by_mdx` | MDX 格式，支持丰富排版 |
| 新建思维导图 | `create_mind_by_markdown` | 传入 Markdown 格式内容 |
| 新建流程图 | `create_flowchart_by_mermaid` | 传入 Mermaid 格式内容 |
| AI 生成 PPT | `create_slide` | 异步，需轮询 `slide_progress` |
| 读取文档内容 | `get_content`（通用） | 通用接口，支持所有文档类型 |
| 读取智能文档 | `smartcanvas.read` | 返回 MDX 格式 |
| 编辑智能文档 | `smartcanvas.edit` | 支持 INSERT_BEFORE/AFTER/DELETE/UPDATE |
| 追加内容到智能文档 | `smartcanvas.edit(action=INSERT_AFTER, id为空)` | 自动追加到末尾 |
| 搜索文档内容 | `smartcanvas.find` | 按关键词定位 Block |
| 上传图片 | `upload_image` | 获取 image_id 供文档使用 |
| OCR 识别文字 | `ocr.extract` | 支持 base64 或 URL |
| OCR 生成文档 | `ocr.toword` | 图片→在线文档 |
| OCR 生成表格 | `ocr.toexcel` | 图片→在线表格 |
| 网页剪藏 | `scrape_url` → `scrape_progress` | 异步轮询 |
| 搜索文件 | `manage.search_file` | 按关键词搜索个人文件 |
| 复制文档 | `manage.copy_file` | 生成副本文档 |
| 移动/重命名 | `manage.move_file` `manage.rename_file_title` | — |
| 删除文档 | `manage.delete_file` | — |

---

## 📄 核心工具详解

### 1. 创建智能文档（首选）— `create_smartcanvas_by_mdx`

```bash
mcporter call "tencent-docs" "create_smartcanvas_by_mdx" --args '{
  "title": "文档标题",
  "mdx": "MDX格式内容",
  "content_format": "mdx"
}'
```

**参数：**
- `title`（必填）：文档标题
- `mdx`（必填）：MDX 格式正文内容
- `content_format`：可选 `"mdx"`（默认）或 `"markdown"`

**返回：** `{ "file_id": "...", "url": "...", "error": "" }`

### 2. 读取智能文档 — `smartcanvas.read`

```bash
mcporter call "tencent-docs" "smartcanvas.read" --args '{
  "file_id": "文档ID"
}'
```

返回 MDX 格式内容，`smartcanvas.find` 找不到时降级使用此工具。

### 3. 编辑智能文档 — `smartcanvas.edit`

**四种操作：**

```bash
# 在指定位置前插入
mcporter call "tencent-docs" "smartcanvas.edit" --args '{
  "action": "INSERT_BEFORE",
  "id": "锚点BlockID",
  "content": "MDX内容",
  "file_id": "文档ID"
}'

# 在指定位置后插入（或追加到末尾）
mcporter call "tencent-docs" "smartcanvas.edit" --args '{
  "action": "INSERT_AFTER",
  "id": "锚点BlockID",
  "content": "MDX内容",
  "file_id": "文档ID"
}'

# 修改内容
mcporter call "tencent-docs" "smartcanvas.edit" --args '{
  "action": "UPDATE",
  "id": "BlockID",
  "content": "新MDX内容",
  "file_id": "文档ID"
}'

# 删除内容
mcporter call "tencent-docs" "smartcanvas.edit" --args '{
  "action": "DELETE",
  "id": "BlockID",
  "file_id": "文档ID"
}'
```

> ⚠️ `UPDATE` / `DELETE` 的 `id` 必须来自 `smartcanvas.find` 或 `smartcanvas.read` 的返回值。

### 4. 搜索文档内容 — `smartcanvas.find`

```bash
mcporter call "tencent-docs" "smartcanvas.find" --args '{
  "file_id": "文档ID",
  "query": "关键词"
}'
```

返回匹配的 Block 列表及其 ID，可作为 `smartcanvas.edit` 的锚点。

### 5. 获取文档内容（通用）— `get_content`

```bash
mcporter call "tencent-docs" "smartcanvas.find" --args '{
  "file_id": "文档ID"
}'
```

支持所有文档类型的通用读取接口。

### 6. 创建文件 — `manage.create_file`

```bash
mcporter call "tencent-docs" "manage.create_file" --args '{
  "file_type": "smartcanvas|doc|sheet|slide|form|mind|flowchart|smartsheet|folder",
  "title": "文档标题",
  "parent_id": "父文件夹ID（可选）",
  "space_id": "空间ID（可选，传入则在知识空间创建）"
}'
```

### 7. 搜索文件 — `manage.search_file`

```bash
mcporter call "tencent-docs" "manage.search_file" --args '{
  "keyword": "搜索关键词"
}'
```

### 8. 复制文档 — `manage.copy_file`

```bash
mcporter call "tencent-docs" "manage.copy_file" --args '{
  "file_id": "文档ID",
  "title": "新文档标题（可选）"
}'
```

### 9. 上传图片 — `upload_image`

```bash
mcporter call "tencent-docs" "upload_image" --args '{
  "file_name": "image.png",
  "image_base64": "图片base64数据"
}'
```

返回 `image_id`，可用于智能文档的 `<Image src="image_id">` 或 Markdown 中的 `![](image_id)`。

### 10. OCR 识别 — `ocr.extract`

```bash
mcporter call "tencent-docs" "ocr.extract" --args '{
  "image_url": "https://example.com/image.png",
  "extract_type": "accurate"
}'
```

### 11. OCR 生成文档 — `ocr.toword`

```bash
mcporter call "tencent-docs" "ocr.toword" --args '{
  "images": [{"image_url": "图片URL"}],
  "title": "生成的文档标题"
}'
```

### 12. OCR 生成表格 — `ocr.toexcel`

```bash
mcporter call "tencent-docs" "ocr.toexcel" --args '{
  "images": [{"image_url": "图片URL"}],
  "title": "生成的表格标题"
}'
```

### 13. 网页剪藏 — `scrape_url` + `scrape_progress`

```bash
# 第一步：发起剪藏任务
mcporter call "tencent-docs" "scrape_url" --args '{
  "url": "https://example.com/article"
}'

# 第二步：轮询进度（5秒间隔，直到 status=2 完成）
mcporter call "tencent-docs" "scrape_progress" --args '{
  "task_id": "返回的task_id"
}'
```

### 14. 创建思维导图 — `create_mind_by_markdown`

```bash
mcporter call "tencent-docs" "create_mind_by_markdown" --args '{
  "title": "思维导图标题",
  "markdown": "Markdown格式层次结构内容",
  "parent_id": "父节点ID（可选）"
}'
```

### 15. 创建流程图 — `create_flowchart_by_mermaid`

```bash
mcporter call "tencent-docs" "create_flowchart_by_mermaid" --args '{
  "title": "流程图标题",
  "mermaid": "Mermaid格式流程图代码",
  "parent_id": "父节点ID（可选）"
}'
```

### 16. AI 生成 PPT — `create_slide`

> ⚠️ 异步接口，必须使用脚本完成：

```bash
node "$SKILL_DIR/scripts/generate_slide.js" \
  --description "用户原始需求描述" \
  --reference_context "用户提供的参考材料（可选）"
```

---

## 📊 Sheet 工具区（在线表格）

| 工具 | 功能 |
|------|------|
| `sheet.get_sheet_info` | 获取子表信息 |
| `sheet.set_cell_value` | 设置单元格值 |
| `sheet.set_range_value` | 批量设置单元格 |
| `sheet.get_range_value` | 获取区域值 |
| `sheet.operation_sheet` | JS 脚本精细操作 |
| `sheet.insert_row` / `sheet.insert_col` | 插入行/列 |
| `sheet.delete_dimension` | 删除行/列 |
| `sheet.add_sheet` | 新增子表 |
| `sheet.delete_sheet` | 删除子表 |
| `sheet.copy_sheet` | 复制子表 |
| `sheet.merge_cell` | 合并单元格 |
| `sheet.set_freeze` | 设置冻结 |
| `sheet.set_filter` / `sheet.remove_filter` | 筛选 |
| `sheet.clear_range_all` / `sheet.clear_range_style` | 清除 |
| `sheet.insert_image` | 插入图片 |

---

## 📋 SmartSheet 工具区（智能表格）

| 工具 | 功能 |
|------|------|
| `smartsheet.list_tables` | 列出工作表 |
| `smartsheet.add_table` | 新增工作表 |
| `smartsheet.delete_table` | 删除工作表 |
| `smartsheet.list_fields` | 列出字段 |
| `smartsheet.add_view` / `smartsheet.delete_view` | 视图管理 |
| `smartsheet.list_records` | 列出记录 |
| `smartsheet.update_records` | 批量更新记录 |
| `smartsheet.delete_records` | 删除记录 |

---

## 📝 DOC 工具区（传统在线文档）

| 工具 | 功能 |
|------|------|
| `doc.insert_text` | 插入文本 |
| `doc.insert_paragraph` | 插入段落 |
| `doc.insert_table` | 插入表格 |
| `doc.insert_page_break` | 插入分页符 |
| `doc.insert_markdown` | 插入 Markdown |
| `doc.insert_comment` | 插入批注 |
| `doc.replace_text` | 替换文本 |
| `doc.find_and_replace` | 查找替换 |
| `doc.update_text_property` | 更新文本样式 |
| `doc.replace_image` | 替换图片 |
| `doc.get_outline` | 获取大纲 |
| `doc.find` | 查找文本 |

---

## 🔧 环境变量

| 变量 | 说明 |
|------|------|
| `TENCENT_DOCS_TOKEN` | 腾讯文档授权 Token |

> 可通过 `mcporter config list` 查看当前配置状态。

---

## ⚠️ 常见错误处理

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| `400006` | Token 鉴权失败 | 重新授权，见鉴权流程 |
| `400007` | VIP 权限不足 | 升级腾讯文档 VIP |
| `-32601` | 接口不存在 | 检查工具名是否正确 |
| `-32603` / `11607` | 参数错误 | 检查 file_id、参数等 |

---

## 📁 本 Skill 目录结构

```
tencent-docs-mcp/
├── SKILL.md              # 入口文件（本文件）
└── scripts/
    └── generate_slide.js # AI生成PPT脚本（异步轮询）
```
