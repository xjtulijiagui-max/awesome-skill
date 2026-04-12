# Markdown to Word Converter

将 Markdown 文件转换为专业格式的 Word 文档。

## 功能特点

- ✅ 读取指定目录下的所有 `.md` 文件
- ✅ 转换为专业格式的 Word 文档（.docx）
- ✅ 书籍样式格式：页眉、页码、目录
- ✅ 支持标准 Markdown 语法
- ✅ 验证所有章节已包含

## 安装依赖

```bash
cd C:\Users\xjtul\.claude\skills\md-to-word
npm install
```

## 使用方法

### 通过 Claude Code 技能调用

```
/md-to-word chapters/ output.docx
```

### 直接运行脚本

```bash
node md-to-word.js <源目录> <输出文件.docx>
```

示例：
```bash
node md-to-word.js chapters/ my-book.docx
```

## 支持的 Markdown 语法

| 语法 | 效果 |
|------|------|
| `# 标题` | 一级标题（居中，大字号） |
| `## 标题` | 二级标题（左对齐，中字号） |
| `### 标题` | 三级标题（正常字号） |
| `#### 标题` | 四级标题 |
| `**粗体**` | 粗体文字 |
| `* 列表项` | 无序列表 |
| `1. 有序列表` | 有序列表 |
| ` ```代码``` ` | 代码块 |

## 文档格式

- **页面大小**: A4 (210mm × 297mm)
- **页边距**: 1 英寸（约 2.54cm）
- **字体**: Calibri
  - 正文: 11pt
  - H1: 16pt
  - H2: 14pt
  - H3: 12pt
- **页眉**: "Generated from Markdown"
- **页脚**: 居中页码

## 输出示例

```
Reading markdown files from: chapters/
Found 3 markdown file(s):
  - 01-introduction.md
  - 02-chapter1.md
  - 03-conclusion.md

Generating Word document: output.docx

✓ Success!
  Chapters processed: 3
  Output file: output.docx
  File size: 45.67 KB

✓ Conversion complete!
```

## 注意事项

- 文件按字母顺序处理
- 章节之间自动添加分页符
- 输出文件会覆盖已存在的同名文件
