#!/usr/bin/env python3
"""
Bid Proposal Creator - 招投标文档生成专家
主入口脚本
"""

import argparse
import json
import sys
import os
from typing import Optional

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

from search_bid import BidSearcher
from search_bid_browser import BidSearcher as BrowserBidSearcher
from generate_proposal import generate_proposal

def search_command(args):
    """搜索标书命令"""
    
    # 优先使用浏览器自动化模式
    if args.browser:
        print("🌐 使用浏览器自动化模式搜索...")
        searcher = BrowserBidSearcher()
        
        if args.company:
            print(f"🔍 正在搜索与 '{args.company}' 相关的标书...")
            results = searcher.search_by_company_browser(
                company_name=args.company,
                province=args.province,
                date_range_days=args.days,
                top_n=args.top
            )
        elif args.platform:
            print(f"🔍 正在从 '{args.platform}' 搜索标书...")
            keywords = args.keywords.split(",") if args.keywords else ["服务", "采购"]
            results = searcher.search_by_platform_browser(
                platform_name=args.platform,
                keywords=keywords,
                date_range_days=args.days,
                top_n=args.top
            )
        else:
            print("❌ 请提供公司名称(--company)或平台名称(--platform)")
            return
    else:
        # 使用模拟数据模式
        searcher = BidSearcher()
        
        if args.company:
            print(f"🔍 正在搜索与 '{args.company}' 相关的标书...")
            results = searcher.search_by_company(
                company_name=args.company,
                province=args.province,
                date_range_days=args.days,
                top_n=args.top
            )
        elif args.platform:
            print(f"🔍 正在从 '{args.platform}' 搜索标书...")
            keywords = args.keywords.split(",") if args.keywords else ["服务", "采购"]
            results = searcher.search_by_platform(
                platform_name=args.platform,
                keywords=keywords,
                date_range_days=args.days,
                top_n=args.top
            )
        else:
            print("❌ 请提供公司名称(--company)或平台名称(--platform)")
            return
    
    # 显示结果
    print("\n" + "=" * 80)
    print(f"找到 {len(results)} 条相关标书：")
    print("=" * 80)
    print(searcher.format_results_table(results))
    
    # 保存结果
    if args.output:
        output_data = [
            {
                "title": r.title,
                "publisher": r.publisher,
                "province": r.province,
                "budget": r.budget,
                "publish_date": r.publish_date,
                "deadline": r.deadline,
                "url": r.url,
                "similarity": r.similarity,
                "platform": r.platform,
                "category": r.category,
                "summary": r.summary
            }
            for r in results
        ]
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: {args.output}")

def generate_command(args):
    """生成投标书命令"""
    print(f"📝 正在生成投标文档...")
    
    # 加载招标信息
    if args.bid_file:
        with open(args.bid_file, "r", encoding="utf-8") as f:
            bid_info = json.load(f)
    else:
        # 使用命令行参数
        bid_info = {
            "project_name": args.project_name or "未指定项目",
            "publisher": args.publisher or "未指定招标方",
            "budget": args.budget or "未公开",
            "duration": args.duration or "未指定"
        }
    
    # 加载公司信息
    if args.company_file:
        with open(args.company_file, "r", encoding="utf-8") as f:
            company_info = json.load(f)
    else:
        # 使用默认公司信息
        company_info = {
            "name": args.company_name or "您的公司名",
            "address": "请填写公司地址",
            "contact": "请填写联系人",
            "phone": "请填写电话",
            "email": "请填写邮箱",
            "qualifications": ["营业执照", "相关资质证书"],
            "achievements": []
        }
    
    # 生成文档
    output_path = args.output or f"/tmp/投标书_{bid_info['project_name'][:10]}_{bid_info.get('publish_date', '2024')}.docx"
    
    result_path = generate_proposal(
        bid_info=bid_info,
        company_info=company_info,
        output_path=output_path,
        template_type=args.template
    )
    
    print(f"\n✅ 投标文档生成完成！")
    print(f"📄 文档路径: {result_path}")
    print(f"\n提示：")
    print("- 请根据实际情况填写报价信息")
    print("- 请完善公司资质和业绩部分")
    print("- 建议打印前仔细校对")

def list_platforms_command(args):
    """列出支持的平台"""
    searcher = BidSearcher()
    platforms = searcher.platforms
    
    print("\n" + "=" * 80)
    print("东部GDP前10省级交易平台")
    print("=" * 80)
    
    for p in platforms.get("eastern_top10", []):
        print(f"\n{p['rank']}. {p['province']} ({p['gdp_trillion']}万亿)")
        print(f"   平台: {p['platform_name']}")
        print(f"   网址: {p['platform_url']}")
        print(f"   类型: {', '.join(p['categories'])}")
    
    print("\n" + "=" * 80)
    print("央企/国企采购平台")
    print("=" * 80)
    
    for p in platforms.get("central_enterprises", []):
        print(f"\n• {p['name']}")
        print(f"  类型: {p['type']}")
        print(f"  网址: {p['url']}")

def main():
    parser = argparse.ArgumentParser(
        description="招投标文档生成专家 - 内置东部GDP前10省级交易平台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 按公司名称搜索标书
  python bid_creator.py search --company "东方福利网" --top 5
  
  # 从指定平台搜索
  python bid_creator.py search --platform "广东省公共资源交易中心" --keywords "福利,工会"
  
  # 生成投标文档
  python bid_creator.py generate --bid-file bid_info.json --company-file company.json --template "福利采购"
  
  # 列出支持的平台
  python bid_creator.py platforms
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索相似标书")
    search_parser.add_argument("--company", "-c", help="公司名称")
    search_parser.add_argument("--platform", "-p", help="指定平台名称")
    search_parser.add_argument("--province", help="省份限制")
    search_parser.add_argument("--keywords", "-k", help="关键词（逗号分隔）")
    search_parser.add_argument("--days", "-d", type=int, default=365, help="时间范围（天）")
    search_parser.add_argument("--top", "-n", type=int, default=10, help="返回结果数量")
    search_parser.add_argument("--output", "-o", help="输出JSON文件路径")
    search_parser.add_argument("--browser", "-b", action="store_true", help="使用浏览器自动化模式（真实数据）")
    
    # generate 命令
    generate_parser = subparsers.add_parser("generate", help="生成投标文档")
    generate_parser.add_argument("--bid-file", "-b", help="招标信息JSON文件")
    generate_parser.add_argument("--company-file", help="公司信息JSON文件")
    generate_parser.add_argument("--project-name", help="项目名称")
    generate_parser.add_argument("--publisher", help="招标方")
    generate_parser.add_argument("--budget", help="预算金额")
    generate_parser.add_argument("--duration", help="服务期限")
    generate_parser.add_argument("--company-name", help="公司名称")
    generate_parser.add_argument("--template", "-t", default="通用服务", 
                                choices=["福利采购", "弹性福利", "通用服务", "IT服务", "咨询服务"],
                                help="模板类型")
    generate_parser.add_argument("--output", "-o", help="输出文档路径")
    
    # platforms 命令
    subparsers.add_parser("platforms", help="列出支持的交易平台")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "search":
        search_command(args)
    elif args.command == "generate":
        generate_command(args)
    elif args.command == "platforms":
        list_platforms_command(args)

if __name__ == "__main__":
    main()
