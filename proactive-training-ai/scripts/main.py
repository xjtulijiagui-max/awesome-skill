#!/usr/bin/env python3
"""
Proactive Training AI - 主入口
课程设计智能体系统
"""

import argparse
import json
import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from demand_analyzer import DemandAnalyzer
from course_matcher import CourseMatcher
from outline_generator import OutlineGenerator

def main():
    parser = argparse.ArgumentParser(description="Proactive Training AI - 课程设计智能体")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # analyze 命令 - 分析客户需求
    analyze_parser = subparsers.add_parser("analyze", help="分析客户需求")
    analyze_parser.add_argument("--input", "-i", required=True, help="客户需求文本或文件路径")
    
    # match 命令 - 匹配课程产品
    match_parser = subparsers.add_parser("match", help="匹配课程产品")
    match_parser.add_argument("--industry", help="行业")
    match_parser.add_argument("--audience", help="受众")
    match_parser.add_argument("--goal", help="培训目标")
    match_parser.add_argument("--duration", help="时长")
    
    # generate 命令 - 生成课程大纲
    generate_parser = subparsers.add_parser("generate", help="生成课程大纲")
    generate_parser.add_argument("--input", "-i", required=True, help="客户需求文本或文件路径")
    generate_parser.add_argument("--output", "-o", help="输出文件路径")
    generate_parser.add_argument("--format", choices=["markdown", "json", "docx"], default="markdown", help="输出格式")
    
    # complete 命令 - 全流程（分析→匹配→生成）
    complete_parser = subparsers.add_parser("complete", help="完整流程：分析→匹配→生成")
    complete_parser.add_argument("--input", "-i", required=True, help="客户需求文本或文件路径")
    complete_parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        analyze_demand(args)
    elif args.command == "match":
        match_courses(args)
    elif args.command == "generate":
        generate_outline(args)
    elif args.command == "complete":
        complete_workflow(args)
    else:
        parser.print_help()

def analyze_demand(args):
    """分析客户需求"""
    analyzer = DemandAnalyzer()
    
    # 读取输入
    if os.path.isfile(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            demand_text = f.read()
    else:
        demand_text = args.input
    
    print("🔍 正在分析客户需求...\n")
    result = analyzer.analyze(demand_text)
    
    print("=" * 60)
    print("📊 需求分析结果")
    print("=" * 60)
    print(f"🏢 行业：{result.get('industry', '未知')}")
    print(f"👥 受众：{result.get('audience', '未知')}")
    print(f"🎯 目标：{result.get('goal', '未知')}")
    print(f"⏱️ 时长：{result.get('duration', '未知')}")
    print(f"💼 公司：{result.get('company', '未知')}")
    print(f"📍 地点：{result.get('location', '未知')}")
    print(f"🔢 人数：{result.get('participants', '未知')}")
    print(f"📅 时间：{result.get('time', '未知')}")
    print("\n📝 需求关键词：", ", ".join(result.get('keywords', [])))
    print("=" * 60)
    
    return result

def match_courses(args):
    """匹配课程产品"""
    matcher = CourseMatcher()
    
    print("🎯 正在匹配课程产品...\n")
    result = matcher.match(
        industry=args.industry,
        audience=args.audience,
        goal=args.goal,
        duration=args.duration
    )
    
    print("=" * 60)
    print("📚 推荐课程组合")
    print("=" * 60)
    
    for i, course in enumerate(result.get('recommended_courses', []), 1):
        print(f"\n{i}. {course['name']}")
        print(f"   匹配度：{course['match_score']}%")
        print(f"   说明：{course['reason']}")
    
    print("\n" + "=" * 60)
    print("📌 定制建议")
    print("=" * 60)
    for suggestion in result.get('customization_suggestions', []):
        print(f"• {suggestion}")
    
    return result

def generate_outline(args):
    """生成课程大纲"""
    generator = OutlineGenerator()
    
    # 读取输入
    if os.path.isfile(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            demand_text = f.read()
    else:
        demand_text = args.input
    
    print("✍️ 正在生成课程大纲...\n")
    outline = generator.generate(demand_text, format=args.format)
    
    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(outline)
        print(f"✅ 课程大纲已保存至：{args.output}")
    else:
        print(outline)
    
    return outline

def complete_workflow(args):
    """完整流程"""
    print("🚀 启动 Proactive Training AI 完整流程\n")
    print("=" * 60)
    
    # 1. 需求分析
    analyzer = DemandAnalyzer()
    if os.path.isfile(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            demand_text = f.read()
    else:
        demand_text = args.input
    
    demand_result = analyzer.analyze(demand_text)
    
    # 2. 课程匹配
    matcher = CourseMatcher()
    match_result = matcher.match(
        industry=demand_result.get('industry'),
        audience=demand_result.get('audience'),
        goal=demand_result.get('goal'),
        duration=demand_result.get('duration')
    )
    
    # 3. 生成大纲
    generator = OutlineGenerator()
    outline = generator.generate(
        demand_text=demand_text,
        demand_analysis=demand_result,
        course_match=match_result,
        format="markdown"
    )
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(outline)
        print(f"\n✅ 完整课程大纲已保存至：{args.output}")
    else:
        print("\n" + "=" * 60)
        print("📄 生成的课程大纲")
        print("=" * 60)
        print(outline)
    
    print("\n🎉 流程完成！")

if __name__ == "__main__":
    main()
