# 快速使用指南

## 场景1：我是东方福利网，想找福利采购相关标书

```bash
# 搜索与"东方福利网"业务相关的标书
python3 scripts/bid_creator.py search --company "东方福利网" --top 10

# 结果会显示：
# - 项目名称
# - 招标方
# - 预算金额
# - 发布时间
# - 相似度评分
```

## 场景2：我想从广东省平台找特定类型的标书

```bash
# 从广东省公共资源交易中心搜索福利相关标书
python3 scripts/bid_creator.py search \
  --platform "广东省公共资源交易中心" \
  --keywords "福利,工会,慰问品" \
  --top 5

# 保存结果到文件
python3 scripts/bid_creator.py search \
  --platform "广东省公共资源交易中心" \
  --keywords "福利" \
  --output results.json
```

## 场景3：基于找到的标书生成投标文档

```bash
# 方式1：使用命令行参数快速生成
python3 scripts/bid_creator.py generate \
  --project-name "2025年工会会员福利采购" \
  --publisher "广州市总工会" \
  --budget "280万元" \
  --company-name "东方福利网科技有限公司" \
  --template "福利采购" \
  --output /tmp/我的投标书.docx

# 方式2：使用JSON配置文件（推荐）
# 1. 创建 bid_info.json
# 2. 创建 company_info.json
# 3. 运行生成命令
python3 scripts/bid_creator.py generate \
  --bid-file bid_info.json \
  --company-file company_info.json \
  --template "福利采购"
```

## JSON配置示例

### bid_info.json（招标信息）

```json
{
  "project_name": "2025年度工会会员节日慰问品采购",
  "publisher": "广州市总工会",
  "budget": "280万元",
  "duration": "2年",
  "qualification_requirements": [
    "具有独立法人资格",
    "具有食品经营许可证",
    "近3年有类似项目业绩"
  ],
  "scoring_criteria": {
    "价格": 40,
    "技术": 35,
    "商务": 25
  },
  "deliverables": [
    "春节慰问品",
    "端午慰问品",
    "中秋慰问品"
  ]
}
```

### company_info.json（公司信息）

```json
{
  "name": "东方福利网科技有限公司",
  "address": "广州市天河区XXX路XXX号",
  "contact": "张三",
  "phone": "138-xxxx-xxxx",
  "email": "contact@dongfangfuli.com",
  "qualifications": [
    "营业执照（三证合一）",
    "食品经营许可证",
    "ISO9001质量管理体系认证",
    "ISO22000食品安全管理体系认证"
  ],
  "achievements": [
    {
      "year": "2024",
      "client": "某大型国企",
      "project": "员工福利采购项目",
      "amount": "150万元"
    },
    {
      "year": "2023",
      "client": "某事业单位",
      "project": "节日慰问品采购",
      "amount": "80万元"
    }
  ]
}
```

## 查看支持的平台列表

```bash
python3 scripts/bid_creator.py platforms
```

输出示例：
```
================================================================================
东部GDP前10省级交易平台
================================================================================

1. 广东 (13.0万亿)
   平台: 广东省公共资源交易中心
   网址: https://www.gdggzy.org.cn
   
2. 江苏 (12.0万亿)
   平台: 江苏省公共资源交易中心
   网址: http://jsggzy.jiangsu.gov.cn
   
...
```

## 模板类型说明

| 模板类型 | 适用场景 | 包含内容 |
|---------|---------|---------|
| 福利采购 | 节日慰问品、生日福利 | 产品方案、配送服务、售后保障 |
| 弹性福利 | 福利平台、积分商城 | 平台架构、功能模块、技术方案 |
| IT服务 | 系统集成、软件开发 | 技术架构、实施方案、安全保障 |
| 咨询服务 | 管理咨询、培训服务 | 方法论、项目计划、团队配置 |
| 通用服务 | 其他服务类项目 | 通用模板结构 |

## 完整工作流程

```bash
# Step 1: 搜索相似标书
python3 scripts/bid_creator.py search --company "东方福利网" --output results.json

# Step 2: 查看搜索结果，选择合适的参考标书
# （查看 results.json 内容）

# Step 3: 准备公司信息配置文件 company_info.json

# Step 4: 生成投标文档
python3 scripts/bid_creator.py generate \
  --bid-file results.json \
  --company-file company_info.json \
  --template "福利采购" \
  --output /tmp/投标书_2025.docx

# Step 5: 下载并完善文档
# - 填写具体报价
# - 完善资质文件
# - 调整技术方案细节
```

## 常见问题

### Q: 搜索不到结果？
A: 可能原因：
- 关键词不匹配，尝试使用更通用的关键词
- 时间范围限制，扩大 `--days` 参数
- 平台限制，尝试不指定省份或更换平台

### Q: 生成的文档格式不对？
A: 生成的 `.docx` 文件是简化版本，建议使用专业的Markdown转Word工具（如 pandoc）进行转换：
```bash
pandoc /tmp/投标书.md -o /tmp/投标书.docx --reference-doc=template.docx
```

### Q: 如何添加新的平台？
A: 编辑 `data/platforms.json` 文件，在 `additional_platforms` 部分添加新的平台信息。

### Q: 是否支持真实平台数据？
A: 当前版本使用模拟数据演示，实际部署需要：
1. 接入各平台的官方API
2. 或者实现网页爬虫获取数据
3. 需要处理反爬虫机制和限流策略
