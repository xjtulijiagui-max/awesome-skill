# Bid Proposal Creator - 招投标文档生成专家

## 功能简介

端到端招投标解决方案，内置东部GDP前10省级公共交易平台，支持：

1. **智能标书搜索** - 输入公司名称或平台，自动搜索相似历史标书
2. **招标文件解析** - 自动提取招标要求、资质条件、评分细则
3. **投标初稿生成** - 一键生成高质量Word格式投标文档

## 安装

将本目录复制到 OpenClaw 的 skills 目录：

```bash
cp -r bid-proposal-creator ~/.openclaw/workspace/skills/
```

## 使用方式

### 1. 列出支持的平台

```bash
python3 scripts/bid_creator.py platforms
```

### 2. 按公司名称搜索标书

```bash
python3 scripts/bid_creator.py search --company "东方福利网" --top 5
```

### 3. 按指定平台搜索标书

```bash
python3 scripts/bid_creator.py search --platform "广东省公共资源交易中心" --keywords "福利,工会" --top 5
```

### 4. 生成投标文档

```bash
# 基于JSON配置文件生成
python3 scripts/bid_creator.py generate --bid-file bid_info.json --company-file company.json --template "福利采购"

# 基于命令行参数生成
python3 scripts/bid_creator.py generate --project-name "2025年工会福利采购" --publisher "广州市总工会" --budget "280万元" --company-name "东方福利网" --template "福利采购"
```

## 支持的模板类型

- `福利采购` - 节日慰问品、生日福利等
- `弹性福利` - 福利平台、积分商城等
- `IT服务` - 系统集成、软件开发等
- `咨询服务` - 管理咨询、培训服务等
- `通用服务` - 通用模板

## 内置数据源

### 东部GDP前10省级交易平台

| 排名 | 省份 | 平台名称 | 网址 |
|------|------|---------|------|
| 1 | 广东 | 广东省公共资源交易中心 | https://www.gdggzy.org.cn |
| 2 | 江苏 | 江苏省公共资源交易中心 | http://jsggzy.jiangsu.gov.cn |
| 3 | 山东 | 山东省公共资源交易中心 | http://ggzy.shandong.gov.cn |
| 4 | 浙江 | 浙江省公共资源交易服务平台 | http://www.zjpubservice.com |
| 5 | 河南 | 河南省公共资源交易中心 | http://www.hnggzy.com |
| 6 | 四川 | 四川省公共资源交易信息网 | http://ggzyjy.sc.gov.cn |
| 7 | 湖北 | 湖北省公共资源交易中心 | http://www.hbggzyfwpt.cn |
| 8 | 福建 | 福建省公共资源交易电子公共服务平台 | https://ggzyfw.fujian.gov.cn |
| 9 | 湖南 | 湖南省公共资源交易中心 | https://ggzy.hunan.gov.cn |
| 10 | 上海 | 上海市公共资源交易中心 | http://ggzyjy.sh.gov.cn |

### 央企/国企采购平台

- 中国招标投标公共服务平台
- 中国政府采购网
- 中国石化、国家电网、中国移动等央企采购平台

## 配置扩展

创建 `EXTEND.md` 添加自定义平台：

```yaml
additional_platforms:
  - name: "XX市政府采购网"
    url: "https://xxx.gov.cn"
    
default_company:
  name: "您的公司名"
  address: "公司地址"
  contact: "联系人"
  phone: "联系电话"
```

## 注意事项

1. 当前版本使用模拟数据演示，实际应用需要接入各平台的真实API或爬虫
2. 生成的投标文档为初稿，实际投标前请根据具体要求进行调整
3. 建议在生成后进行人工审核和完善

## 技术架构

```
bid-proposal-creator/
├── SKILL.md                 # 技能说明文档
├── data/
│   └── platforms.json       # 平台数据库
├── scripts/
│   ├── bid_creator.py       # 主入口脚本
│   ├── search_bid.py        # 标书搜索模块
│   └── generate_proposal.py # 文档生成模块
└── README.md               # 本文件
```

## 开发计划

- [ ] 接入更多省级交易平台API
- [ ] 实现真实平台爬虫
- [ ] 增加标书查重功能
- [ ] 支持电子签章
- [ ] 接入招标信息推送

## License

MIT
