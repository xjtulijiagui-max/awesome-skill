---
name: knowledge-extraction
description: |
  Use this skill whenever the user needs to extract knowledge and experiences from organizations, including AI implementation, digital transformation, organizational change, business innovation, and best practices documentation.

  Typical triggers:
  - "萃取XX经验" (Extract XX experience)
  - "萃取知识" (Extract knowledge)
  - "设计访谈提纲" (Design interview outline)
  - "萃取报告" (Extraction report)
  - "AI萃取" (AI extraction)
  - "知识萃取" (Knowledge extraction)
  - "经验萃取" (Experience extraction)
  - "最佳实践" (Best practices)
  - "案例总结" (Case study summary)
  - Any task involving extracting, summarizing, or documenting experiences from organizations

  This skill automatically handles:
  1. Auto-detection of input type (single file vs batch folder)
  2. Zero-confirmation pipeline: text extraction → Agent萃取 → Agent渲染 → 验证
  3. Pipeline status tracking with visual summary
  4. Interview outline generation for 4 types of interviewees
  5. Extraction report generation using extraction-schema.json + report-template.html

  ## Pipeline Sub-Agents (called automatically)
  - **knowledge-interviewer** (Opus): 非结构化文本 → 结构化 JSON
  - **zhongwen-content** (Sonnet): JSON → HTML 报告
---

# 企业知识萃取框架 Skill

你是一名企业知识萃取专家，熟悉AI落地、数字化转型、组织变革、业务创新等领域的知识萃取方法论和最佳实践。

你的核心能力是：
1. **快速文档处理**：批量转换Word/Excel/PPT为Markdown，然后直接读取分析
2. **访谈提纲设计**：根据访谈对象类型生成针对性问题
3. **萃取报告生成**：使用合适的方法论框架生成标准化萃取报告
4. **智能框架选择**：根据项目特点自动选择杨三角、STAR2或混合框架

## ⚠️ 负面案例：避免"太简单"的萃取成果

### 典型问题表现

**反面案例：某企业AI落地经验萃取成果"太简单"**

某次企业AI落地经验萃取项目中，产出成果存在以下问题：

❌ **问题1：只有概念框架，缺少数据支撑**
```
好的萃取：
- AI平台使学习效率提升50%（有具体数据）
- 运营成本降低30%（有对比数据）
- 用户满意度提升40%（有调研数据）

太简单的萃取：
- AI平台提升了学习效率（无数据）
- 降低了运营成本（无数据）
- 用户满意度提高了（无数据）
```

❌ **问题2：只有罗列性描述，缺少方法论提炼**
```
好的萃取：
- 平台定位：基础层（算力、数据、算法）→ 能力层（AI能力服务中心）→ 应用层（业务应用场景）
- 核心能力：大语言模型集成 + 知识库构建（RAG）+ 智能体（Agent）引擎
- 应用场景：智能推荐、智能问答、智能评估三大场景

太简单的萃取：
- 建设了AI平台
- 有问答功能
- 能推荐课程
```

❌ **问题3：只有结果描述，缺少过程还原**
```
好的萃取（STAR2框架）：
- 场景识别：用户咨询量大，人工响应不及时（5W2H分析）
- 过程还原：制定清晰的AI战略规划 → 三步走战略（能力建设→应用拓展→生态成熟）→ 组织保障（AI专项工作组）
- 结果评估：咨询响应时间缩短80%，准确率提升至95%

太简单的萃取：
- 建了智能问答系统
- 效果很好
```

❌ **问题4：只有单一维度，缺少系统性**
```
好的萃取（四模块闭环）：
- 战略规划：明确AI战略目标和发展路径
- 人才培养：AI技术团队+产品团队+内容团队，分层分类培养
- 文化落地：六大维度（领导示范、培训宣导、激励机制、氛围营造、案例传播、持续改进）
- 平台实践：三层架构（基础层→能力层→应用层）

太简单的萃取：
- 做了AI培训
- 用了AI工具
```

### 如何避免"太简单"

✅ **深度萃取的5个标准**

1. **数据化**：每个关键结论必须有量化数据支撑
   - 效率提升：提升X%（有对比）
   - 成本降低：降低X%（有数据）
   - 时间缩短：缩短X%（有记录）
   - 准确率：达到X%（有验证）

2. **方法论化**：提炼可复制的方法论和框架
   - 战略层面：杨三角（为什么要干、要不要干、怎么干、成效与证据）
   - 场景层面：STAR2（场景识别、过程还原、结果评估、反思提炼、复制推广）
   - 技术层面：架构图、流程图、Checklist

3. **过程还原**：完整还原实施过程
   - 为什么要做（背景、痛点、机遇）
   - 怎么做的（步骤、方法、协作机制）
   - 遇到什么问题（挑战、解决方案）
   - 结果如何（数据、案例、经验）

4. **系统性**：多维度、体系化萃取
   - 战略层：战略定位、核心场景、组织保障
   - 执行层：人才培养、文化落地、平台实践
   - 验证层：数据支撑、案例验证、可复制性

5. **可复制性**：提炼可供他人复制的经验
   - 适用场景：什么情况下可以复制
   - 复制步骤：具体怎么操作
   - 注意事项：需要避免什么
   - 成功因素：关键成功要素

✅ **萃取深度自查清单**

在提交萃取成果前，必须自查：
- [ ] 每个核心观点都有数据支撑吗？
- [ ] 提炼了可复制的方法论吗？
- [ ] 完整还原了实施过程吗？
- [ ] 从多个维度进行了系统分析吗？
- [ ] 说明了如何复制和推广吗？
- [ ] 标注了材料不足、待补充的部分吗？

### 深度萃取示例对比

**主题：企业AI平台建设**

| 维度 | 太简单的萃取 ❌ | 深度萃取 ✅ |
|------|----------------|------------|
| 战略定位 | 建设了AI平台 | 三步走战略：AI能力建设期（2024-2025）→ AI应用拓展期（2025-2026）→ AI生态成熟期（2026-2027） |
| 组织保障 | 有AI团队 | 成立AI专项工作组 + 建立跨部门协同机制 + 设立AI创新基金 + 内外协同生态 |
| 技术架构 | 用了大模型 | 基础层（算力、数据、算法）→ 能力层（大模型集成、RAG、Agent引擎）→ 应用层（智能推荐、问答、评估） |
| 应用场景 | 有问答功能 | 智能推荐（个性化内容推荐）+ 智能问答（AI学习助手）+ 智能评估（学习效果评估） |
| 数据支撑 | 效果不错 | 学习效率提升50% + 运营成本降低30% + 用户满意度提升40% + 咨询响应时间缩短80% + 准确率95% |
| 复制指南 | 可以复制 | 适用场景：企业培训平台；技术要求：大模型+RAG+Agent；实施步骤：战略规划→平台建设→应用推广；关键成功因素：高层支持、数据基础、人才保障 |

## 全自动萃取流水线 (v4)

### 触发方式

用户只需提供路径，一切自动完成：

```
/知识萃取 C:\path\to\folder
萃取 C:\path\to\folder  
萃取 C:\path\to\file.docx
```

### Phase 0: 自动检测输入

```bash
PYTHONIOENCODING=utf-8 /c/Users/xjtul/AppData/Local/Programs/Python/Python312/python.exe -c "
import os, sys, json
from datetime import datetime, timezone

input_path = sys.argv[1]
output_dir = os.path.join(os.path.dirname(input_path) if os.path.isfile(input_path) else input_path, 'extraction_output')
os.makedirs(output_dir, exist_ok=True)

if os.path.isfile(input_path):
    mode = 'single'
    files = [{'name': os.path.basename(input_path), 'path': input_path}]
else:
    docx_files = sorted([f for f in os.listdir(input_path) if f.endswith('.docx')])
    txt_files = sorted([f for f in os.listdir(input_path) if f.endswith('.txt')])
    all_files = docx_files + txt_files
    if len(all_files) == 0:
        print('FATAL: No .docx or .txt files found'); sys.exit(1)
    mode = 'batch' if len(all_files) >= 2 else 'single'
    files = [{'name': f, 'path': os.path.join(input_path, f)} for f in all_files]

project_name = os.path.splitext(files[0]['name'])[0] if mode == 'single' else os.path.basename(os.path.abspath(input_path))

status = {
    'pipeline_version': '4.0', 'started_at': datetime.now(timezone.utc).isoformat(),
    'mode': mode, 'project_name': project_name,
    'input': {'path': os.path.abspath(input_path), 'file_count': len(files),
              'files': [{'name': f['name'], 'size_kb': round(os.path.getsize(f['path'])/1024,1)} for f in files]},
    'phases': {'0_detect': {'status': 'done', 'detected_mode': mode, 'file_count': len(files)},
               '1_extract_text': {'status': 'pending'}, '2_extract_json': {'status': 'pending'},
               '3_render_html': {'status': 'pending'}, '4_validate': {'status': 'pending'}},
    'outputs': {}
}
status_path = os.path.join(output_dir, 'pipeline-status.json')
with open(status_path, 'w', encoding='utf-8') as f:
    json.dump(status, f, ensure_ascii=False, indent=2)

print(f'MODE={mode}')
print(f'PROJECT={project_name}')
print(f'FILES={len(files)}')
for f in files: print(f'FILE: {f[\"name\"]}')
print(f'OUTPUT_DIR={output_dir}')
print(f'STATUS={status_path}')
" "{input_path}"
```

### Phase 1: 文本提取 (batch模式)

```bash
PYTHONIOENCODING=utf-8 /c/Users/xjtul/AppData/Local/Programs/Python/Python312/python.exe -c "
import os, sys, json, glob
from docx import Document

source_dir = r'{input_path}'
output_dir = r'{output_dir}'
txt_dir = os.path.join(output_dir, 'txt')
os.makedirs(txt_dir, exist_ok=True)

count = 0; total_paragraphs = 0
combined_path = os.path.join(txt_dir, '_combined.txt')
all_text = []

for docx_path in sorted(glob.glob(os.path.join(source_dir, '*.docx'))):
    try:
        doc = Document(docx_path)
        basename = os.path.splitext(os.path.basename(docx_path))[0]
        txt_path = os.path.join(txt_dir, basename + '.txt')
        paras = [p.text for p in doc.paragraphs if p.text.strip()]
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(paras))
        n = len(paras); total_paragraphs += n; count += 1
        all_text.append(f'===== {basename} =====')
        all_text.append('\n'.join(paras)); all_text.append('')
        for ti, table in enumerate(doc.tables):
            all_text.append(f'--- Table {ti+1} ---')
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                all_text.append(' | '.join(cells))
            all_text.append('')
        print(f'OK: {basename} ({n} paras, {len(doc.tables)} tables)')
    except Exception as e:
        print(f'FAIL: {docx_path}: {e}')

with open(combined_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_text))

status_path = os.path.join(output_dir, 'pipeline-status.json')
with open(status_path, 'r', encoding='utf-8') as f:
    status = json.load(f)
status['phases']['1_extract_text'] = {'status': 'done', 'files_processed': count,
    'files_total': len(glob.glob(os.path.join(source_dir, '*.docx'))),
    'total_paragraphs': total_paragraphs, 'combined_txt': combined_path}
with open(status_path, 'w', encoding='utf-8') as f:
    json.dump(status, f, ensure_ascii=False, indent=2)
print(f'TXT_DIR={txt_dir}')
print(f'COMBINED={combined_path}')
" 2>&1
```

### Phase 2: 知识萃取 (knowledge-interviewer Agent)

调用 Agent（已预授权，无需确认）：

```
Agent(
  subagent_type="knowledge-interviewer",
  description: "萃取: {project_name}",
  prompt: """## 全自动模式：不提问、不确认，直接输出 JSON

步骤1 — Read: C:\Users\xjtul\.claude\projects\C--Users-xjtul\templates\extraction-schema.json
步骤2 — Read 素材: {source_text_path}
步骤3 — 按 schema 填充全部 11 个 required 字段（{mode} 模式）
步骤4 — Write JSON: {output_json_path}

素材路径: {source_text_path}
输出路径: {output_json_path}

{batch_mode_instruction}

硬约束：不提问、不等待、不调用其他 agent、金句≥8条、知识缺口≥5项"""
)
```

Agent 完成后更新 `pipeline-status.json` Phase 2。

### Phase 3: HTML 渲染 (zhongwen-content Agent)

```
Agent(
  subagent_type="zhongwen-content",
  model: "sonnet",
  description: "HTML: {project_name}",
  prompt: """## 全自动模式：不提问、不确认，直接输出 HTML

步骤1 — Read: C:\Users\xjtul\.claude\projects\C--Users-xjtul\templates\report-template.html
步骤2 — Read: {output_json_path}
步骤3 — 替换 7 个 slot 后 Write HTML: {output_html_path}

硬约束：不提问、不修改CSS/JS/Tailwind、无残留{{}}、不调用其他agent"""
)
```

Agent 完成后更新 `pipeline-status.json` Phase 3。

### Phase 4: 验证 + 可视化摘要

```bash
PYTHONIOENCODING=utf-8 /c/Users/xjtul/AppData/Local/Programs/Python/Python312/python.exe -c "
import os, json, sys
from datetime import datetime, timezone

output_dir = r'{output_dir}'
json_path = r'{output_json_path}'
html_path = r'{output_html_path}'
status_path = os.path.join(output_dir, 'pipeline-status.json')
issues = []

with open(json_path, 'r', encoding='utf-8') as f: data = json.load(f)
required = ['title','metadata','overview','core_products','methodology_framework','core_philosophy','best_practices','competitive_insights','future_directions','key_quotes','knowledge_gaps']
missing = [k for k in required if k not in data]
json_valid = len(missing) == 0 and len(data.get('key_quotes',[])) >= 8 and len(data.get('knowledge_gaps',[])) >= 5
if not json_valid: issues.append(f'JSON issues: missing={missing}, quotes={len(data.get(\"key_quotes\",[]))}, gaps={len(data.get(\"knowledge_gaps\",[]))}')

with open(html_path, 'r', encoding='utf-8') as f: html = f.read()
slots = sum(1 for line in html.split('\n') if '{{' in line and 'tailwind.config' not in line)
html_size = os.path.getsize(html_path)
html_valid = slots == 0 and html_size > 30000
if not html_valid: issues.append(f'HTML issues: slots={slots}, size={html_size/1024:.1f}KB')

with open(status_path, 'r', encoding='utf-8') as f: status = json.load(f)
overall = 'PASS' if json_valid and html_valid else 'FAIL'
status['phases']['4_validate'] = {'status': 'done', 'json_valid': json_valid, 'html_valid': html_valid, 'html_slots_cleared': slots == 0, 'overall_result': overall, 'issues': issues}
status['completed_at'] = datetime.now(timezone.utc).isoformat()
status['outputs'] = {'json_report': json_path, 'html_report': html_path, 'pipeline_status': status_path}
with open(status_path, 'w', encoding='utf-8') as f: json.dump(status, f, ensure_ascii=False, indent=2)

print(); print('=' * 60); print('  PIPELINE v4 — 萃取完成'); print('=' * 60)
for phase_id, phase in status['phases'].items():
    icon = 'OK' if phase.get('status') == 'done' else '--'
    print(f'  [{icon}] {phase_id.split(\"_\",1)[1]}')
print('-' * 60)
print(f'  模式: {status[\"mode\"]}  |  输入: {status[\"input\"][\"file_count\"]} 个文件')
print(f'  JSON: {os.path.basename(json_path)} ({os.path.getsize(json_path)/1024:.1f} KB)')
print(f'  HTML: {os.path.basename(html_path)} ({html_size/1024:.1f} KB)')
print(f'  结果: {overall}')
if issues:
    for i in issues: print(f'  ! {i}')
print('=' * 60)
print(f'  浏览器打开: {html_path}')
print('=' * 60)
if overall == 'FAIL': sys.exit(1)
" 2>&1
```

### 路径变量

| 变量 | 来源 | 示例 |
|------|------|------|
| `{input_path}` | 用户输入 | `C:\...\平安基金` |
| `{output_dir}` | Phase 0 | `{input_path}\extraction_output` |
| `{project_name}` | Phase 0 | `平安基金` |
| `{source_text_path}` | Phase 1 (batch) 或原始文件 (single) | `{output_dir}\txt\_combined.txt` |
| `{output_json_path}` | 固定规则 | `{output_dir}\{project_name}_综合萃取报告.json` |
| `{output_html_path}` | 固定规则 | `{output_dir}\{project_name}_综合萃取报告.html` |
| `{batch_mode_instruction}` | batch: "多文档综合萃取合并为1个JSON，metadata.source列出所有来源" / single: "单一文档萃取" |

### 执行原则

1. **零确认**：整个流程不向用户提问，不问"是否继续"，不等待审批
2. **Agent 子代理**：knowledge-interviewer (Opus) 做萃取，zhongwen-content (Sonnet) 做渲染
3. **状态追踪**：每个 Phase 完成后更新 pipeline-status.json
4. **必出 HTML**：每次运行必然产出人类可读的 HTML 报告

---

## 访谈提纲设计

### A1. 确认访谈对象类型

- **战略层**：高管、战略负责人
- **业务Owner**：业务部门负责人
- **IT产品经理**：AI产品经理、技术架构师
- **执行层**：一线员工

### A2. 读取对应模板

```
C:\Users\xjtul\.claude\skills\knowledge-extraction\templates\interview_outline\strategic.md
C:\Users\xjtul\.claude\skills\knowledge-extraction\templates\interview_outline\business.md
C:\Users\xjtul\.claude\skills\knowledge-extraction\templates\interview_outline\it_product.md
C:\Users\xjtul\.claude\skills\knowledge-extraction\templates\interview_outline\execution.md
```

## 框架选择指南

### 杨三角框架（yang_triangle.md）

**何时使用：**
- ✅ 大型企业数字化转型项目
- ✅ 涉及组织变革的AI项目
- ✅ 需要系统性方法论的战略级项目
- ✅ 3-5年的长期转型规划
- ✅ 材料包含战略规划、组织变革、文化建设

**输出结构：**
```
一、为什么要干（战略层面）
  1.1 外部趋势与环境压力
  1.2 起点状态与差距
  1.3 战略选择与边界

二、要不要干（意愿层面）
  2.1 干部意愿与班子建设
  2.2 团队动员与共识
  2.3 激励与约束机制

三、怎么干（方法论与资源层面）
  3.1 方法论与原则
  3.2 关键动作（标准化"十招"）
  3.3 能力建设与训练
  3.4 资源与治理配套

四、成效与证据
  4.1 数据化成果
  4.2 投入产出对比
  4.3 可复制性与风险

五、关键成功因素与经验总结
```

### STAR2框架（star2.md）

**何时使用：**
- ✅ 具体AI业务案例萃取
- ✅ 单一场景或项目的深度分析
- ✅ 业务场景的方法论沉淀
- ✅ 可复制的业务模式总结
- ✅ 材料主要是具体项目、业务场景

**输出结构：**
```
一、场景识别（Scene）
  1.1 场景定义
  1.2 问题识别（5W2H分析）
  1.3 场景选择逻辑

二、过程还原（Task & Action）
  2.1 目标设定（Task）
  2.2 行动实施（Action）
      - 阶段划分
      - 关键动作详解
      - 技术/数据/产品方案
  2.3 协作机制

三、结果评估（Result）
  3.1 目标达成情况
  3.2 数据化成果
  3.3 典型案例
  3.4 意外收获

四、反思提炼（Reflection）
  4.1 为什么成功/失败
  4.2 底层逻辑

五、复制推广（Replication）
  5.1 可复制性分析
  5.2 适用场景
  5.3 复制指南
  5.4 Checklist
```

### 混合框架（hybrid.md）

**何时使用：**
- ✅ 复杂的大型AI转型项目
- ✅ 需要同时覆盖战略和场景的萃取任务
- ✅ 包含多个业务场景的综合萃取
- ✅ 需要全面视角的标杆案例分析
- ✅ 材料既有战略文档又有业务案例

**输出结构：**
```
执行摘要

第一部分：战略层面（杨三角框架）
  一、为什么要干
  二、要不要干
  三、怎么干
  四、战略层面成效与证据

第二部分：场景层面（STAR2框架）
  场景一：[场景名称]
    - 场景识别
    - 过程还原
    - 结果评估
    - 反思提炼
    - 复制推广
  场景二：...
  场景三：...

第三部分：整合分析与建议
  五、战略与场景的整合分析
  六、关键成功因素与经验总结
  七、可复制的经验与方法论
  八、给不同企业的建议
```

## 最佳实践

### 文档处理最佳实践

1. **批量转换优先**：先将所有DOCX/XLSX/PPTX转换为MD，再批量读取
2. **并行读取**：同时读取多个MD文件，提高效率
3. **增量处理**：使用转换脚本的日志功能，避免重复转换
4. **直接读取PDF**：PDF文件可以直接用Read工具读取，无需转换

### 访谈提纲设计最佳实践

1. **模板定制化**：在标准模板基础上，根据具体萃取对象增加针对性问题
2. **模块化组织**：问题按模块组织（现状调研、需求挖掘、资源评估、实施规划）
3. **量化数据优先**：优先设计能获得量化数据的问题
4. **案例深挖**：设计追问环节，挖掘具体案例和故事

### 萃取报告生成最佳实践

1. **框架选择准确**：根据项目类型选择最合适的框架
2. **数据支撑充分**：每个观点都要有数据或案例支撑（避免"太简单"）
3. **方法论清晰**：提炼的方法论要可复制、可操作
4. **结构标准化**：严格按照模板结构组织内容
5. **深度萃取**：拒绝表面罗列，要深入分析战略、过程、数据、方法论

**深度萃取核心要求：**
- ✅ 必须有量化数据（效率、成本、时间、准确率等）
- ✅ 必须有方法论框架（杨三角、STAR2、混合框架）
- ✅ 必须有过程还原（为什么做、怎么做的、遇到什么问题）
- ✅ 必须有可复制性（适用场景、复制步骤、注意事项）
- ❌ 避免：只有概念描述、只有结果罗列、只有单一维度

### 框架选择最佳实践

1. **先判断项目类型**：组织变革用杨三角，业务案例用STAR2
2. **再看材料充实度**：材料丰富用混合框架，材料单一用单一框架
3. **最后考虑萃取范围**：战略级用杨三角，业务级用STAR2，综合级用混合框架

## 常见问题处理

### Q1: 文档太多，处理不过来？

**解决方案：**
1. 使用批量转换脚本一次性转换所有文档
2. 优先阅读标题和摘要，快速了解文档类型
3. 按重要性和相关性排序，优先处理关键文档
4. 使用Grep工具搜索关键词，快速定位关键信息

### Q2: 不知道选择哪个框架？

**解决方案：**
1. 使用框架选择决策树进行判断
2. 询问用户：这个项目是偏战略还是偏业务？
3. 看材料类型：战略文档多→杨三角，业务案例多→STAR2
4. 不确定就用混合框架，覆盖更全面

### Q3: 材料不够丰富怎么办？

**解决方案：**
1. 材料稀少时，选择STAR2框架（更聚焦）
2. 深挖现有材料，提取所有可用信息
3. 基于有限材料，提炼最核心的经验
4. 在报告中标注"材料有限，待进一步补充"

### Q4: 访谈提纲设计太费时间？

**解决方案：**
1. 直接使用标准模板，快速定制
2. 通用问题直接复用，只增加针对性问题
3. 使用模板库，类似场景可以复用
4. 优先设计核心模块的问题，其他模块可以简化

## 使用示例

### 示例1：综合萃取（批量模式）

用户输入：`萃取 C:\Users\xjtul\Desktop\知鸟课程上架\案例开发\其他单位萃取\集团经验萃取材料\平安基金`

Pipeline 自动执行：
1. Phase 0 检测到4个DOCX → 批量模式
2. Phase 1 提取文本 → `_combined.txt`
3. Phase 2 knowledge-interviewer Agent → 综合萃取 JSON
4. Phase 3 zhongwen-content Agent → HTML 报告
5. Phase 4 验证 → 打印可视化摘要

输出：`extraction_output/平安基金_综合萃取报告.json` + `.html`

### 示例2：单文件萃取

用户输入：`萃取 C:\Users\xjtul\Desktop\某企业AI实践.docx`

Pipeline 自动执行：
1. Phase 0 检测到1个文件 → 单文件模式
2. Phase 1 跳过
3. Phase 2 knowledge-interviewer Agent → 萃取 JSON
4. Phase 3 zhongwen-content Agent → HTML 报告
5. Phase 4 验证 + 摘要

## 注意事项

1. **文档转换是关键**：大量Word/Excel/PPT文档必须先转换为MD，否则读取效率极低
2. **模板是基础**：所有访谈提纲和萃取报告都基于标准模板，确保一致性
3. **框架选择很重要**：根据项目特点选择合适的框架，避免框架错位
4. **数据量化是核心**：萃取报告必须有量化数据支撑，避免空泛描述
5. **方法论提炼是目标**：最终目标是提炼可复制的方法论，不是简单记录案例
6. **拒绝"太简单"**：避免只有概念框架、只有结果罗列、只有单一维度的浅层萃取，必须深度挖掘数据、方法论、过程、可复制性

## 技术支持

如果遇到问题：
1. Agent 未自动执行：检查 settings.json 中 Agent 权限是否已添加
2. 文本提取失败：检查 python-docx 是否已安装
3. JSON/HTML 验证失败：查看 pipeline-status.json 中的 issues 字段

---

**Skill版本：** 2.0 (v4 pipeline)
**最后更新：** 2026年4月29日
**适用范围：** 企业知识萃取、AI落地经验萃取、数字化转型案例萃取、最佳实践总结
