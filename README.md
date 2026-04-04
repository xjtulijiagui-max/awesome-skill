# Awesome Skills

各种 AI Agent Skills 集合

## 📚 技能列表

| 技能名称 | 描述 | 来源 |
|---------|------|------|
| **enterprise-ai-scenario-map** | 企业AI场景地图生成器 - 通过深度调研生成30+AI应用场景，支持Word/HTML双格式输出 | [源子AI](https://github.com/MetaInFLow/Enterprise-ai-scenario-map-skill) |
| **idea-to-prototype** | 从创意到原型快速转换 | - |
| **skill-creator** | 技能创建工具 | Anthropic官方 |

---

## 企业AI场景地图生成器 (enterprise-ai-scenario-map)

> 由**源子（深圳）人工智能有限公司（Yuanzi AI）**原创开发

### 功能特性

- 📊 **深度调研**：基于 web-search 的企业信息和行业痛点调研
- 📝 **完整报告**：V2.1 标准模板（6个Part，15-30页）
- 📄 **双格式输出**：自动生成 Word (.docx) + HTML 可视化报告
- 🏭 **行业场景库**：8大行业（建筑、电商、金融、制造、医疗、教育、法律、物流）典型AI场景参考
- ⚖️ **优先级框架**：P0/P1/P2 优先级评估体系
- 🛣️ **实施路径**：分阶段落地计划和关键成功要素

### 使用方式

```
帮我为"XX有限公司"生成一份AI场景地图报告
```

### 目录结构

```
enterprise-ai-scenario-map-skill/
├── SKILL.md                        # 核心 Skill 定义
├── scripts/
│   └── deep_research_wrapper.py    # 调研框架生成脚本
├── references/
│   ├── report-template-v2.1.md     # V2.1 报告模板
│   ├── business-analysis-framework.md
│   ├── typical-ai-scenarios.md     # 8大行业场景库
│   ├── scenario-priority-framework.md
│   └── company-info-config.md      # 源子AI公司信息
└── README.md
```

---

## 安装

\`\`\`bash
npm install
\`\`\`

## 使用

\`\`\`bash
npm start
\`\`\`

## 许可证

MIT
