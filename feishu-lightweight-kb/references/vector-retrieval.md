# 向量检索增强配置指南

## 功能说明

本技能支持可选的向量检索增强，在原有关键词检索的基础上增加语义召回能力，解决同义词、近义词、语义相关但关键词不匹配的问题。

**特点：**
- 完全向后兼容：不构建索引依然可以使用纯关键词检索
- 混合检索：向量召回 + 关键词精排，兼顾召回率和准确率
- 多种实现可选：支持本地轻量方案和云服务方案

## 目录结构（启用向量检索后）

```
~/kb/company_docs/
├── hr/                 # 原始文档目录（保持不变）
├── finance/
├── training/
├── project/
├── policy/
└── .index/             # 向量索引目录（自动生成）
    ├── chunks.jsonl    # 分块元数据：每个块的文本、文件路径、位置、标题
    └── embeddings.npz  # 嵌入向量矩阵
```

## 混合检索工作流程

1. **用户提问** → 理解问题 + 扩展关键词（保留原逻辑）
2. **向量召回** → 如果存在索引，对问题生成向量，召回 Top 15 相似块
3. **关键词精排** → 在召回结果中按关键词匹配度重新排序
4. **原文验证** → 根据分块元信息定位到原始文件，补充上下文
5. **定位原文片段** → 提取最相关片段（保留原逻辑）
6. **整合回答** → 按原格式输出（保留原逻辑）

如果没有索引或向量检索失败，自动回退到纯关键词检索。

## 依赖安装

根据选择的方案安装依赖：

### 方案 1：本地轻量方案（推荐，无需 API Key）

```bash
pip install numpy sentence-transformers chromadb
```

使用 `all-MiniLM-L6-v2` 模型（约 90MB），完全本地运行。

### 方案 2：OpenAI 方案

```bash
pip install openai numpy
```

需要配置 `OPENAI_API_KEY` 环境变量，使用 `text-embedding-3-small` 模型。

## 使用方法

### 1. 构建索引

```bash
python ~/workspace/agent/skills/feishu-lightweight-kb/scripts/build_index.py \
  --kb-dir ~/kb/company_docs \
  --chunk-size 512 \
  --chunk-overlap 50 \
  --model local
```

参数说明：
- `--kb-dir`: 知识库根目录
- `--chunk-size`: 每块字符数，默认 512
- `--chunk-overlap`: 块重叠字符数，默认 50
- `--model`: 嵌入模型类型，`local` 或 `openai`，默认 `local`

### 2. 向量检索示例

```python
from search_vector import VectorSearch

vs = VectorSearch(kb_dir="~/kb/company_docs", model_type="local")
results = vs.search("差旅报销标准", top_k=10)
for r in results:
    print(f"文件: {r['file_path']}, 相似度: {r['score']:.4f}")
    print(f"片段: {r['text'][:200]}...")
```

## 参数调优建议

- **知识库文档数 < 100**: 纯关键词检索足够，无需向量
- **100 < 文档数 < 1000**: 推荐本地方案
- **文档数 > 1000**: 推荐 OpenAI + chromadb 持久化
- **chunk-size**: 中文文档建议 300-600 字符
- **top_k**: 向量召回建议 10-20，兼顾召回率和性能

## 兼容性说明

- 支持所有原有支持的文档格式（md/txt/pdf/docx）
- 自动跳过 `.index` 目录，不会索引索引文件本身
- 新增/删除文档后需要重新构建索引
- 更换模型类型需要重新构建索引
