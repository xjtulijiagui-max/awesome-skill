#!/usr/bin/env python3
"""
招投标标书搜索模块
支持多平台并行搜索、相似度计算
"""

import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio

@dataclass
class BidDocument:
    """标书文档数据类"""
    title: str
    publisher: str
    province: str
    budget: str
    publish_date: str
    deadline: str
    url: str
    similarity: float
    platform: str
    category: str
    summary: str = ""
    
class BidSearcher:
    """标书搜索器"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or "/root/.openclaw/workspace/skills/bid-proposal-creator/data"
        self.platforms = self._load_platforms()
        
    def _load_platforms(self) -> Dict:
        """加载平台配置"""
        try:
            with open(f"{self.data_dir}/platforms.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载平台配置失败: {e}")
            return {"eastern_top10": [], "central_enterprises": []}
    
    def search_by_company(
        self, 
        company_name: str, 
        province: Optional[str] = None,
        date_range_days: int = 365,
        top_n: int = 10
    ) -> List[BidDocument]:
        """
        基于公司名称搜索相似标书
        
        Args:
            company_name: 公司名称
            province: 省份限制
            date_range_days: 时间范围（天）
            top_n: 返回结果数量
            
        Returns:
            相似标书列表
        """
        # 提取公司核心业务关键词
        keywords = self._extract_company_keywords(company_name)
        print(f"提取关键词: {keywords}")
        
        # 根据关键词确定行业类型
        industry = self._detect_industry(keywords)
        print(f"检测行业类型: {industry}")
        
        # 搜索各平台
        all_results = []
        platforms_to_search = self._get_search_platforms(province)
        
        for platform in platforms_to_search:
            results = self._search_platform(platform, keywords, industry, date_range_days)
            all_results.extend(results)
        
        # 计算相似度并排序
        scored_results = self._calculate_similarity(all_results, company_name, keywords)
        scored_results.sort(key=lambda x: x.similarity, reverse=True)
        
        return scored_results[:top_n]
    
    def search_by_platform(
        self,
        platform_name: str,
        keywords: List[str],
        date_range_days: int = 365,
        top_n: int = 10
    ) -> List[BidDocument]:
        """
        基于指定平台搜索标书
        
        Args:
            platform_name: 平台名称或URL
            keywords: 搜索关键词
            date_range_days: 时间范围
            top_n: 返回结果数量
            
        Returns:
            标书列表
        """
        # 查找匹配的平台
        platform = self._find_platform(platform_name)
        if not platform:
            print(f"未找到平台: {platform_name}")
            return []
        
        industry = self._detect_industry(keywords)
        results = self._search_platform(platform, keywords, industry, date_range_days)
        
        # 计算相似度
        scored_results = self._calculate_similarity(results, "", keywords)
        scored_results.sort(key=lambda x: x.similarity, reverse=True)
        
        return scored_results[:top_n]
    
    def _extract_company_keywords(self, company_name: str) -> List[str]:
        """从公司名称提取业务关键词"""
        # 常见业务词映射
        business_mapping = {
            "福利": ["福利", "慰问品", "节日", "工会", "员工关怀"],
            "科技": ["科技", "软件", "系统", "技术", "信息化"],
            "咨询": ["咨询", "顾问", "策划", "管理"],
            "广告": ["广告", "营销", "推广", "品牌"],
            "培训": ["培训", "教育", "学习", "课程"],
            "网络": ["网络", "互联网", "电商", "平台"],
        }
        
        keywords = []
        for biz, words in business_mapping.items():
            if biz in company_name:
                keywords.extend(words)
        
        # 如果没有匹配到，返回通用关键词
        if not keywords:
            keywords = ["服务", "采购", "项目"]
        
        return keywords
    
    def _detect_industry(self, keywords: List[str]) -> str:
        """检测行业类型"""
        industry_keywords = self.platforms.get("industry_keywords", {})
        
        max_score = 0
        best_industry = "通用服务"
        
        for industry, words in industry_keywords.items():
            score = sum(1 for k in keywords if any(w in k for w in words))
            if score > max_score:
                max_score = score
                best_industry = industry
        
        return best_industry
    
    def _get_search_platforms(self, province: Optional[str] = None) -> List[Dict]:
        """获取要搜索的平台列表"""
        all_platforms = []
        all_platforms.extend(self.platforms.get("eastern_top10", []))
        all_platforms.extend(self.platforms.get("central_enterprises", []))
        
        if province:
            all_platforms = [p for p in all_platforms if p.get("province") == province]
        
        return all_platforms
    
    def _find_platform(self, platform_name: str) -> Optional[Dict]:
        """查找指定平台"""
        all_platforms = []
        all_platforms.extend(self.platforms.get("eastern_top10", []))
        all_platforms.extend(self.platforms.get("central_enterprises", []))
        
        for p in all_platforms:
            if platform_name in p.get("platform_name", "") or platform_name in p.get("url", ""):
                return p
        
        return None
    
    def _search_platform(
        self, 
        platform: Dict, 
        keywords: List[str],
        industry: str,
        date_range_days: int
    ) -> List[BidDocument]:
        """
        搜索指定平台
        
        注意：实际实现需要接入各平台的API或爬虫
        这里返回模拟数据进行演示
        """
        results = []
        
        # 模拟数据 - 实际应用中需要从平台获取
        mock_data = self._get_mock_data(platform, keywords, industry)
        
        for item in mock_data:
            # 检查时间范围
            try:
                pub_date = datetime.strptime(item["publish_date"], "%Y-%m-%d")
                if (datetime.now() - pub_date).days > date_range_days:
                    continue
            except:
                pass
            
            doc = BidDocument(
                title=item["title"],
                publisher=item["publisher"],
                province=platform.get("province", "全国"),
                budget=item.get("budget", "未公开"),
                publish_date=item["publish_date"],
                deadline=item.get("deadline", ""),
                url=item.get("url", ""),
                similarity=0.0,  # 稍后计算
                platform=platform.get("platform_name", ""),
                category=item.get("category", industry),
                summary=item.get("summary", "")
            )
            results.append(doc)
        
        return results
    
    def _get_mock_data(self, platform: Dict, keywords: List[str], industry: str) -> List[Dict]:
        """获取模拟数据 - 实际应用中会调用真实API"""
        # 使用近期日期避免被过滤
        today = datetime.now()
        
        # 模拟一些福利采购相关的标书
        mock_bids = [
            {
                "title": "2025年度工会会员节日慰问品采购项目",
                "publisher": "广州市总工会",
                "budget": "280万元",
                "publish_date": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
                "deadline": (today + timedelta(days=20)).strftime("%Y-%m-%d"),
                "url": "https://example.com/bid/1",
                "category": "福利采购",
                "summary": "采购春节、端午、中秋等节日慰问品，包括食品、日用品等"
            },
            {
                "title": "职工福利平台服务采购",
                "publisher": "深圳某国有大型企业",
                "budget": "150万元/年",
                "publish_date": (today - timedelta(days=30)).strftime("%Y-%m-%d"),
                "deadline": (today + timedelta(days=15)).strftime("%Y-%m-%d"),
                "url": "https://example.com/bid/2",
                "category": "弹性福利",
                "summary": "建设职工弹性福利平台，提供积分兑换、商品自选等服务"
            },
            {
                "title": "员工生日福利采购项目",
                "publisher": "广东省某事业单位",
                "budget": "45万元",
                "publish_date": (today - timedelta(days=45)).strftime("%Y-%m-%d"),
                "deadline": (today + timedelta(days=10)).strftime("%Y-%m-%d"),
                "url": "https://example.com/bid/3",
                "category": "福利采购",
                "summary": "为员工提供生日蛋糕、礼品等福利"
            },
            {
                "title": "年度员工健康体检服务采购",
                "publisher": "江苏省某国企",
                "budget": "120万元",
                "publish_date": (today - timedelta(days=20)).strftime("%Y-%m-%d"),
                "deadline": (today + timedelta(days=25)).strftime("%Y-%m-%d"),
                "url": "https://example.com/bid/4",
                "category": "福利采购",
                "summary": "为2000名员工提供年度健康体检服务"
            },
            {
                "title": "企业福利商城平台建设项目",
                "publisher": "浙江省某集团",
                "budget": "200万元",
                "publish_date": (today - timedelta(days=15)).strftime("%Y-%m-%d"),
                "deadline": (today + timedelta(days=30)).strftime("%Y-%m-%d"),
                "url": "https://example.com/bid/5",
                "category": "弹性福利",
                "summary": "建设企业专属福利商城，整合供应商资源"
            }
        ]
        
        # 根据关键词筛选
        filtered = []
        for bid in mock_bids:
            title = bid["title"]
            summary = bid.get("summary", "")
            if any(k in title or k in summary for k in keywords):
                filtered.append(bid)
        
        return filtered if filtered else mock_bids[:3]
    
    def _calculate_similarity(
        self, 
        results: List[BidDocument], 
        company_name: str,
        keywords: List[str]
    ) -> List[BidDocument]:
        """计算相似度分数"""
        for doc in results:
            score = 0.0
            
            # 关键词匹配
            title_lower = doc.title.lower()
            for kw in keywords:
                if kw in title_lower:
                    score += 0.2
            
            # 行业匹配
            if doc.category in ["福利采购", "弹性福利"]:
                score += 0.3
            
            # 预算规模（模拟）
            if "万" in doc.budget:
                score += 0.1
            
            # 时间新鲜度
            try:
                pub_date = datetime.strptime(doc.publish_date, "%Y-%m-%d")
                days_ago = (datetime.now() - pub_date).days
                if days_ago < 30:
                    score += 0.2
                elif days_ago < 90:
                    score += 0.1
            except:
                pass
            
            doc.similarity = min(score, 1.0) * 100  # 转换为百分比
        
        return results
    
    def format_results_table(self, results: List[BidDocument]) -> str:
        """格式化搜索结果为表格"""
        if not results:
            return "未找到相关标书"
        
        lines = [
            "| 序号 | 项目名称 | 招标方 | 预算 | 发布时间 | 相似度 |",
            "|-----|---------|--------|------|---------|--------|"
        ]
        
        for i, doc in enumerate(results, 1):
            lines.append(
                f"| {i} | {doc.title[:30]}... | {doc.publisher[:15]} | {doc.budget} | {doc.publish_date} | {doc.similarity:.0f}% |"
            )
        
        return "\n".join(lines)


# 测试代码
if __name__ == "__main__":
    searcher = BidSearcher()
    
    # 测试按公司搜索
    print("=" * 60)
    print("测试：搜索'东方福利网'相关标书")
    print("=" * 60)
    results = searcher.search_by_company("东方福利网", top_n=5)
    print(searcher.format_results_table(results))
    
    print("\n" + "=" * 60)
    print("测试：从广东省平台搜索")
    print("=" * 60)
    results = searcher.search_by_platform("广东省公共资源交易中心", ["福利", "工会"])
    print(searcher.format_results_table(results))
