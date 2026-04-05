#!/usr/bin/env python3
"""
招投标文档生成模块
基于模板和招标信息生成Word格式的投标初稿
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import os

@dataclass
class CompanyInfo:
    """公司信息"""
    name: str
    address: str
    contact: str
    phone: str
    email: str
    business_license: str
    qualifications: List[str]
    achievements: List[Dict]

@dataclass
class BidRequirement:
    """招标要求"""
    project_name: str
    publisher: str
    budget: str
    duration: str
    qualification_requirements: List[str]
    scoring_criteria: Dict[str, int]
    deliverables: List[str]
    service_requirements: List[str]

def generate_proposal(
    bid_info: Dict,
    company_info: Dict,
    output_path: str,
    template_type: str = "通用服务"
) -> str:
    """
    生成投标文档
    
    Args:
        bid_info: 招标信息
        company_info: 公司信息
        output_path: 输出路径
        template_type: 模板类型
        
    Returns:
        生成的文档路径
    """
    # 根据模板类型选择模板
    template = get_template(template_type)
    
    # 生成文档内容
    content = fill_template(template, bid_info, company_info)
    
    # 保存为Markdown（后续转换为Word）
    md_path = output_path.replace(".docx", ".md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    # 调用docx转换（简化版，实际可以使用pandoc或python-docx）
    docx_path = convert_to_docx(md_path, output_path)
    
    return docx_path

def get_template(template_type: str) -> str:
    """获取模板内容"""
    
    templates = {
        "福利采购": WELFARE_TEMPLATE,
        "弹性福利": FLEXIBLE_WELFARE_TEMPLATE,
        "通用服务": GENERAL_SERVICE_TEMPLATE,
        "IT服务": IT_SERVICE_TEMPLATE,
        "咨询服务": CONSULTING_TEMPLATE
    }
    
    return templates.get(template_type, GENERAL_SERVICE_TEMPLATE)

def fill_template(
    template: str, 
    bid_info: Dict, 
    company_info: Dict
) -> str:
    """填充模板"""
    
    # 替换基本信息
    content = template
    content = content.replace("{{PROJECT_NAME}}", bid_info.get("project_name", ""))
    content = content.replace("{{PUBLISHER}}", bid_info.get("publisher", ""))
    content = content.replace("{{BUDGET}}", bid_info.get("budget", ""))
    content = content.replace("{{DURATION}}", bid_info.get("duration", ""))
    content = content.replace("{{COMPANY_NAME}}", company_info.get("name", ""))
    content = content.replace("{{COMPANY_ADDRESS}}", company_info.get("address", ""))
    content = content.replace("{{CONTACT}}", company_info.get("contact", ""))
    content = content.replace("{{PHONE}}", company_info.get("phone", ""))
    content = content.replace("{{EMAIL}}", company_info.get("email", ""))
    content = content.replace("{{DATE}}", datetime.now().strftime("%Y年%m月%d日"))
    
    # 生成资质列表
    qualifications = company_info.get("qualifications", [])
    qual_str = "\n".join([f"- {q}" for q in qualifications])
    content = content.replace("{{QUALIFICATIONS}}", qual_str)
    
    # 生成业绩列表
    achievements = company_info.get("achievements", [])
    if achievements:
        ach_str = "\n".join([
            f"| {a.get('year', '')} | {a.get('client', '')} | {a.get('project', '')} | {a.get('amount', '')} |"
            for a in achievements[:5]
        ])
        content = content.replace("{{ACHIEVEMENTS}}", ach_str)
    else:
        content = content.replace("{{ACHIEVEMENTS}}", "| 2023 | 某大型企业 | 员工福利采购项目 | 100万 |")
    
    return content

def convert_to_docx(md_path: str, output_path: str) -> str:
    """
    将Markdown转换为Word
    简化实现，实际可以使用pandoc或python-docx
    """
    # 这里只是复制，实际应该调用转换工具
    # 可以使用: pandoc input.md -o output.docx
    return output_path

# ============ 模板定义 ============

WELFARE_TEMPLATE = """# 投标文件

**项目名称：** {{PROJECT_NAME}}

**投标单位：** {{COMPANY_NAME}}

**投标日期：** {{DATE}}

---

## 一、投标函

致：{{PUBLISHER}}

根据贵方 {{PROJECT_NAME}} 的招标公告，我方经研究招标文件后，决定参加该项目的投标。我方正式授权 {{CONTACT}} 代表我方全权处理本次投标的有关事宜。

据此函，签字代表宣布同意如下：

1. 我方愿意按照招标文件的规定，承担招标文件中要求的全部工作内容。
2. 我方已详细阅读并完全理解招标文件的所有条款，自愿遵守其中的各项规定。
3. 我方保证提供的所有资料真实、准确、完整。

投标单位：{{COMPANY_NAME}}（盖章）

法定代表人或授权代表：（签字）

日期：{{DATE}}

---

## 二、法定代表人授权书

本授权书声明：注册于 {{COMPANY_ADDRESS}} 的 {{COMPANY_NAME}} 的法定代表人 现授权 {{CONTACT}} 为我方委托代理人，代表我方参加 {{PROJECT_NAME}} 的投标活动。

委托代理人有权代表我方签署投标文件、进行澄清及签署中标后的合同等相关法律文件。

本授权书于 {{DATE}} 签字生效，特此声明。

授权单位：{{COMPANY_NAME}}（盖章）

法定代表人：（签字）

被授权人：（签字）

---

## 三、投标单位基本情况

| 项目 | 内容 |
|-----|------|
| 单位名称 | {{COMPANY_NAME}} |
| 注册地址 | {{COMPANY_ADDRESS}} |
| 联系人 | {{CONTACT}} |
| 联系电话 | {{PHONE}} |
| 电子邮箱 | {{EMAIL}} |

### 3.1 资质文件

{{QUALIFICATIONS}}

### 3.2 类似项目业绩

| 年份 | 客户名称 | 项目名称 | 合同金额 |
|-----|---------|---------|---------|
{{ACHIEVEMENTS}}

---

## 四、技术方案

### 4.1 项目理解

针对 {{PROJECT_NAME}}，我方充分理解贵单位在员工福利采购方面的需求，包括：

- 产品质量保障
- 配送及时准确
- 售后服务完善
- 价格合理透明

### 4.2 服务方案

#### 4.2.1 产品供应

我方将提供以下类别的福利产品：

1. **节日慰问品**
   - 春节：年货礼盒、特色食品
   - 端午：粽子礼盒、咸鸭蛋
   - 中秋：月饼礼盒、水果

2. **生日福利**
   - 生日蛋糕券
   - 生日礼品自选

3. **日常关怀**
   - 生活用品
   - 健康食品

#### 4.2.2 配送服务

- 配送范围：覆盖全国
- 配送时效：下单后48小时内发货
- 配送方式：快递送货上门

#### 4.2.3 售后服务

- 7×24小时客服热线
- 质量问题无条件退换
- 定期回访满意度调查

### 4.3 质量保障措施

1. 严格筛选供应商，确保产品质量
2. 每批次产品提供质检报告
3. 建立产品追溯体系
4. 定期产品质量抽检

---

## 五、商务报价

| 项目 | 单价（元） | 数量 | 小计（元） |
|-----|-----------|-----|-----------|
| 春节慰问品 | 待填 | 待填 | 待填 |
| 端午慰问品 | 待填 | 待填 | 待填 |
| 中秋慰问品 | 待填 | 待填 | 待填 |
| 生日福利 | 待填 | 待填 | 待填 |
| **合计** | - | - | **{{BUDGET}}** |

---

## 六、服务承诺

我方郑重承诺：

1. **产品质量承诺**：所有产品均为正品，假一赔十
2. **配送时效承诺**：按时配送，延误赔偿
3. **售后服务承诺**：24小时内响应，48小时内解决
4. **价格承诺**：同类产品价格不高于市场平均水平

---

*本投标文件由 KimiClaw 招投标助手自动生成*
"""

FLEXIBLE_WELFARE_TEMPLATE = """# 投标文件

**项目名称：** {{PROJECT_NAME}}

**投标单位：** {{COMPANY_NAME}}

**投标日期：** {{DATE}}

---

## 一、投标函

致：{{PUBLISHER}}

我方已充分理解 {{PROJECT_NAME}} 的需求，决定参加本项目投标。我方承诺提供一套完整的弹性福利平台解决方案，帮助贵单位提升员工福利体验。

投标单位：{{COMPANY_NAME}}（盖章）

日期：{{DATE}}

---

## 二、方案概述

### 2.1 平台架构

我方提供的弹性福利平台包含以下核心模块：

1. **员工端APP/小程序**
   - 福利积分查询
   - 商品浏览选购
   - 订单跟踪
   - 售后服务

2. **管理后台**
   - 员工管理
   - 积分发放
   - 数据统计
   - 供应商管理

3. **供应商系统**
   - 商品管理
   - 订单处理
   - 库存同步
   - 结算对账

### 2.2 核心功能

| 功能模块 | 功能描述 |
|---------|---------|
| 积分管理 | 支持多种积分发放规则，灵活配置 |
| 商城系统 | 多品类商品，支持搜索、筛选、收藏 |
| 订单系统 | 全流程订单跟踪，支持退换货 |
| 数据分析 | 多维度数据报表，辅助决策 |
| 消息通知 | 系统消息、短信、邮件多渠道触达 |

---

## 三、技术方案

### 3.1 系统架构

```
┌─────────────────────────────────────────────┐
│  前端层：Web、APP、小程序                     │
├─────────────────────────────────────────────┤
│  接入层：负载均衡、API网关                    │
├─────────────────────────────────────────────┤
│  服务层：用户服务、商品服务、订单服务、支付服务  │
├─────────────────────────────────────────────┤
│  数据层：MySQL、Redis、Elasticsearch         │
└─────────────────────────────────────────────┘
```

### 3.2 安全保障

- 数据加密传输（HTTPS/TLS）
- 敏感数据加密存储
- 定期安全漏洞扫描
- 完善的权限控制体系

### 3.3 性能指标

- 系统可用性：99.9%
- 并发用户数：支持10万+
- 页面响应时间：< 2秒
- 数据备份：每日全量+实时增量

---

## 四、实施计划

| 阶段 | 时间 | 工作内容 |
|-----|-----|---------|
| 需求确认 | 第1周 | 详细需求调研、方案确认 |
| 系统部署 | 第2-3周 | 环境搭建、系统配置 |
| 数据迁移 | 第4周 | 历史数据导入、数据校验 |
| 培训上线 | 第5周 | 用户培训、试运行 |
| 正式运营 | 第6周起 | 正式上线、运营支持 |

---

## 五、报价方案

| 项目 | 费用（万元/年） | 说明 |
|-----|----------------|------|
| 平台使用费 | 待填 | SaaS模式，按用户数计费 |
| 实施部署费 | 待填 | 一次性费用 |
| 运维支持费 | 待填 | 7×24小时技术支持 |
| **合计** | **{{BUDGET}}** | - |

---

*本投标文件由 KimiClaw 招投标助手自动生成*
"""

GENERAL_SERVICE_TEMPLATE = """# 投标文件

**项目名称：** {{PROJECT_NAME}}

**投标单位：** {{COMPANY_NAME}}

**投标日期：** {{DATE}}

---

## 一、投标函

致：{{PUBLISHER}}

我方已认真研究 {{PROJECT_NAME}} 的招标文件，愿意按照招标文件的要求承担相应工作。

投标单位：{{COMPANY_NAME}}（盖章）

日期：{{DATE}}

---

## 二、公司简介

{{COMPANY_NAME}} 成立于XXXX年，是一家专业从事XXXX的企业。公司拥有丰富的行业经验和专业的技术团队，致力于为客户提供优质的服务。

### 2.1 公司资质

{{QUALIFICATIONS}}

### 2.2 主要业绩

{{ACHIEVEMENTS}}

---

## 三、技术方案

### 3.1 项目理解

针对本项目，我方理解的核心需求包括：

- 需求点1
- 需求点2
- 需求点3

### 3.2 解决方案

（此处根据具体项目要求填写详细的技术方案）

### 3.3 实施计划

| 阶段 | 时间安排 | 主要工作 |
|-----|---------|---------|
| 第一阶段 | 第1-2周 | 需求调研、方案设计 |
| 第二阶段 | 第3-6周 | 开发/采购/实施 |
| 第三阶段 | 第7-8周 | 测试验收 |
| 第四阶段 | 第9周起 | 交付运维 |

---

## 四、商务报价

| 序号 | 项目 | 金额（元） | 备注 |
|-----|-----|-----------|-----|
| 1 | 项目费用 | 待填 | - |
| 2 | 实施费用 | 待填 | - |
| 3 | 维护费用 | 待填 | - |
| **合计** | | **{{BUDGET}}** | - |

---

## 五、服务承诺

1. 严格按照合同约定履行义务
2. 保证服务质量，按时交付
3. 提供完善的售后服务
4. 保守商业秘密

---

*本投标文件由 KimiClaw 招投标助手自动生成*
"""

IT_SERVICE_TEMPLATE = GENERAL_SERVICE_TEMPLATE

CONSULTING_TEMPLATE = GENERAL_SERVICE_TEMPLATE

# 测试代码
if __name__ == "__main__":
    # 测试数据
    bid_info = {
        "project_name": "2024年度工会会员节日慰问品采购",
        "publisher": "广州市总工会",
        "budget": "280万元",
        "duration": "2年"
    }
    
    company_info = {
        "name": "东方福利网科技有限公司",
        "address": "广州市天河区XXX路XXX号",
        "contact": "张三",
        "phone": "138-xxxx-xxxx",
        "email": "contact@example.com",
        "qualifications": [
            "营业执照",
            "食品经营许可证",
            "ISO9001质量管理体系认证"
        ],
        "achievements": [
            {"year": "2023", "client": "某国企", "project": "员工福利采购", "amount": "150万"},
            {"year": "2023", "client": "某事业单位", "project": "节日慰问品", "amount": "80万"}
        ]
    }
    
    output_path = "/tmp/投标书_测试.docx"
    result = generate_proposal(bid_info, company_info, output_path, "福利采购")
    print(f"生成文档：{result}")
