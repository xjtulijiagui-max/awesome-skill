---
name: knowledge-interviewer
description: >
  从访谈录音/文本中萃取结构化知识。TRIGGER when: 用户需要"萃取"、"提取知识"、"访谈分析"、
  "知识萃取报告"、从DOCX/TXT提取专家经验。支持单文件和多文件综合萃取，自动检测输入类型。
  输出严格按 extraction-schema.json 的 JSON 结构。
  SKIP: 生成 HTML/PPTX/DOCX 交付物（那是 zhongwen-content 的职责）。
---

# 知识萃取访谈者 (knowledge-interviewer)

## 功能

从领域专家访谈/调研文档中提取结构化知识，输出 JSON 格式的萃取结果。

**支持两种模式（自动检测）：**
- **单文件模式**：输入为单个 .txt/.docx 文件 → 产出 1 个 JSON
- **综合模式**：输入为包含多个文档的文件夹 → 所有文档合并萃取为 1 个 JSON（非多个独立 JSON）

## 硬约束

1. **只输出 JSON** — 不生成 HTML、PPTX、DOCX 或任何其他交付物
2. **不创建/修改 skill** — 不新建或修改任何 SKILL.md 文件
3. **不调用 zhongwen-content** — 那是主对话 orchestrator 的事
4. **金句保留口语化原文** — 不润色，不转述，原样保留
5. **缺失信息标注** — 访谈中未覆盖的内容填入 `knowledge_gaps`，不编造
6. **综合模式：一份 JSON 涵盖全部来源** — 多文档时合并萃取，`metadata.source` 列出所有来源文件

## 执行步骤

### 步骤 0：自动检测输入类型

检查用户指定的输入路径：
- 如果是**单个文件**（.txt / .docx）→ 单文件模式
- 如果是**目录**（包含多个 .docx/.txt）→ 综合模式，读取全部文件
- 如果是**目录但只有 1 个有效文件** → 降级为单文件模式

如果是 .docx 文件，需先用 python-docx 提取文本（同 Phase 1 逻辑）。

### 步骤 1：读取输出 Schema

```
Read: C:\Users\xjtul\.claude\projects\C--Users-xjtul\templates\extraction-schema.json
```

理解每个字段的含义和层级。输出必须严格匹配 schema 的 `required` 字段和类型。

### 步骤 2：读取全部素材

**单文件模式**：读取指定的单个文件。

**综合模式**：
1. 列出目录下所有 .docx/.txt 文件
2. 逐个提取文本（.docx 用 python-docx）
3. 汇总全部文本内容，标记每个段落来自哪个文件
4. 将所有内容作为整体进行分析萃取

### 步骤 3：按 Schema 逐字段萃取

对照 schema 的 10 个顶层字段（title/metadata/overview/core_products/methodology_framework/core_philosophy/best_practices/competitive_insights/future_directions/key_quotes/knowledge_gaps）逐一填充。

| 字段 | 填充要点 |
|------|---------|
| `title` | `{平台/产品名}知识萃取报告` |
| `metadata` | 日期、来源（综合模式列出所有文件）、受访者、素材类型、质量说明 |
| `overview` | 200-300字全景概述，含定位、产品矩阵、突破方向 |
| `core_products` | 每个产品5字段(product_name/tag/positioning/maturity/key_highlights)，子模块用 sub_modules |
| `methodology_framework` | 萃取出的方法论，每项含 stages(3-5步)/description/application |
| `core_philosophy` | 核心理念列表，每项含 name/description/quote_ref |
| `best_practices` | STAR2框架(Situation-Task-Action-Result-Reflection) |
| `competitive_insights` | 竞争维度/我方优势/行业现状/关键差异 |
| `future_directions` | 3-6项未来方向，标注优先级(高/中/低) |
| `key_quotes` | 8-15条，含 text/speaker/context/topic_tag |
| `knowledge_gaps` | 5-10项未覆盖知识点，标注优先级和补充来源 |

**综合模式特殊处理**：
- `metadata.source`：列出所有源文件名
- `metadata.material_type`：标注为"多文档综合分析"
- `overview`：覆盖所有文档的共同主题
- `core_products`：去重合并，同一产品在多文档中出现的合并为一个条目
- `best_practices`：案例可来自不同文档，标注来源
- `key_quotes`：可来自不同文档，speaker 标注来源文件名
- `knowledge_gaps`：综合判断，跨文档知识缺口

### 步骤 4：输出 JSON

将填充完成的 JSON 写入用户指定（或默认）的输出路径。

**文件命名规则**：
- 单文件模式：`{源文件名}_萃取报告.json`
- 综合模式：`{文件夹名}_综合萃取报告.json`

## 模型选择

使用默认模型（Opus），适合分析型任务（非结构化文本→结构化知识）。

## 与 zhongwen-content 的协作

knowledge-interviewer 只负责"文本→JSON"这一步。
由主对话 orchestrator 调用 zhongwen-content（Sonnet 模型）完成"JSON→HTML"渲染。
两者不互相调用。

## 全自动模式行为准则

- 不向用户提问、不请求确认、不等待
- 遇到模糊内容自行判断，缺失信息填入 knowledge_gaps
- 综合模式下，所有源文档合并分析，产出唯一 JSON
- 输出完成后报告文件路径和大小
