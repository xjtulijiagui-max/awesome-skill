# Awesome Skills

> **AI 顾问李家贵的自用 Skills 集合**
> 欢迎大家使用和交流！

这里收集了我在日常 AI 咨询工作中开发的各类实用 Skills，涵盖企业应用、文档处理、营销获客、知识管理等多个领域。

## 💡 设计理念

这些 Skills 都遵循**实用主义**原则：
- ✅ **从实战中提炼**：每个 Skill 都在实际项目中验证过
- ✅ **开箱即用**：最小化配置，直接调用
- ✅ **可组合使用**：多个 Skills 可以串联完成复杂任务
- ✅ **持续迭代**：根据使用反馈不断优化

## 📦 Skills 总览

### 🏢 企业应用

| Skill | 功能 | 典型场景 |
|-------|------|---------|
| **enterprise-ai-scenario-map** | 企业AI场景地图生成器 | 为企业生成 30+ AI 应用场景规划报告 |
| **proactive-training-ai** | AI 课程设计 | 从0到1设计 AI 培训课程体系 |
| **knowledge-extraction** | 企业知识萃取 | 从文档/访谈中提取结构化知识 |

### 📄 文档处理

| Skill | 功能 | 典型场景 |
|-------|------|---------|
| **md-to-word** | Markdown 转 Word | 快速生成专业文档 |
| **pdf** | PDF 处理 | 提取 PDF 文本和表格 |
| **pptx** | PowerPoint 生成 | 创建演示文稿 |
| **docx** | Word 文档操作 | 创建/编辑 Word 文档 |
| **markitdown** | 通用格式转 Markdown | PDF/Office/图片/音频转 Markdown |

### ✍️ 内容创作

| Skill | 功能 | 典型场景 |
|-------|------|---------|
| **bid-proposal-creator** | 招投标文档生成 | 端到端生成标书 |
| **marketing-huoke-allinone** | 全链路营销文案 | 从定位到执行的一体化文案 |
| **ip-huoke-wenan** | IP 获客文案 | 打造个人 IP 的内容创作 |
| **podcast-transcript-txt** | 播客转录 | 音频转文字并整理 |

### 🔧 工具类

| Skill | 功能 | 典型场景 |
|-------|------|---------|
| **idea-to-prototype** | 创意到原型 | 快速将想法落地为可交互原型 |
| **skill-creator** | Skill 创建工具 | 开发自定义 Skills |
| **html-to-png** | HTML 截图 | 网页转图片 |
| **workspace-personalizer** | 工作空间配置 | OpenClaw 环境初始化 |

### 🌐 协作平台

| Skill | 功能 | 典型场景 |
|-------|------|---------|
| **feishu-lightweight-kb** | 飞书轻量知识库 | 飞书文档检索问答 |
| **tencent-docs-mcp** | 腾讯文档 MCP | 腾讯文档集成 |
| **lark-*** (系列) | 飞书全功能 | 文档/表格/日历/审批等 |

## 🚀 快速开始

### 安装

```bash
npm install
```

### 使用

```bash
npm start
```

### 调用示例

```bash
# 企业应用类
/enterprise-ai-scenario-map "XX公司AI场景地图"
/proactive-training-ai "设计AI培训课程"
/knowledge-extraction "从访谈中萃取知识"

# 文档处理类
/md-to-word "document.md"
/pdf "extract text from file.pdf"
/pptx "create presentation"

# 内容创作类
/bid-proposal-creator "政府采购项目"
/marketing-huoke-allinone "新产品上市推广"
/ip-huoke-wenan "个人品牌定位"
/podcast-transcript-txt "https://podcast.url/episode"

# 工具类
/idea-to-prototype "将创意转为原型"
/skill-creator "创建新技能"

# 协作平台类
/feishu-lightweight-kb "搜索飞书文档"
```

## 🔗 典型工作流

这些 Skills 可以组合使用，形成完整的工作流：

**企业咨询流程：**
```
knowledge-extraction (访谈) → enterprise-ai-scenario-map (规划) →
pptx (汇报) → feishu-lightweight-kb (知识沉淀)
```

**营销内容生产：**
```
ip-huoke-wenan (定位) → marketing-huoke-allinone (文案) →
md-to-word (文档) → lark-doc (发布)
```

**课程开发流程：**
```
proactive-training-ai (大纲) → knowledge-extraction (素材) →
pptx (课件) → md-to-word (手册)
```

## 🛠️ 技术特点

- **语言**: Python + JavaScript
- **集成**: 飞书、腾讯文档、Claude Code
- **输出**: Word、PPT、HTML、Markdown、JSON
- **设计**: 卡片式布局、响应式设计

## 🤝 贡献与交流

这些 Skills 是我在实际工作中开发的工具，欢迎大家：

- ⭐ Star 支持一下
- 🍴 Fork 修改优化
- 💬 提出问题和建议
- 🔧 提交 PR 改进

## 📝 许可证

MIT License

---

**关于李家贵**

AI 顾问，专注企业 AI 应用落地、知识管理、营销自动化。
联系方式：通过 GitHub Issues

**欢迎试用，欢迎反馈！** 🎉
