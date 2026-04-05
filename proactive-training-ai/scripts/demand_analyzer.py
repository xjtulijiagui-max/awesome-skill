#!/usr/bin/env python3
"""
需求解析器 - 从客户需求文本中提取关键信息
"""

import json
import os
import re
from typing import Dict, List

class DemandAnalyzer:
    """需求解析器"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.keywords = self._load_keywords()
    
    def _load_keywords(self) -> Dict:
        """加载关键词库"""
        try:
            with open(os.path.join(self.data_dir, "industry_keywords.json"), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载关键词库失败: {e}")
            return {}
    
    def analyze(self, text: str) -> Dict:
        """分析需求文本"""
        text_lower = text.lower()
        
        result = {
            "raw_text": text,
            "industry": self._detect_industry(text),
            "audience": self._detect_audience(text),
            "goal": self._detect_goal(text),
            "duration": self._detect_duration(text),
            "company": self._extract_company(text),
            "location": self._extract_location(text),
            "participants": self._extract_participants(text),
            "time": self._extract_time(text),
            "keywords": self._extract_keywords(text)
        }
        
        return result
    
    def _detect_industry(self, text: str) -> str:
        """检测行业"""
        industries = self.keywords.get("industries", {})
        scores = {}
        
        for industry, data in industries.items():
            score = 0
            keywords = data.get("keywords", [])
            for kw in keywords:
                if kw in text:
                    score += 1
            if score > 0:
                scores[industry] = score
        
        if scores:
            return max(scores, key=scores.get)
        return "general"
    
    def _detect_audience(self, text: str) -> str:
        """检测受众"""
        audiences = self.keywords.get("audience_mapping", {})
        scores = {}
        
        for audience, data in audiences.items():
            score = 0
            keywords = data.get("keywords", [])
            for kw in keywords:
                if kw in text:
                    score += 1
            if score > 0:
                scores[audience] = score
        
        if scores:
            return max(scores, key=scores.get)
        return "general"
    
    def _detect_goal(self, text: str) -> str:
        """检测培训目标"""
        goals = self.keywords.get("goal_mapping", {})
        scores = {}
        
        for goal, data in goals.items():
            score = 0
            keywords = data.get("keywords", [])
            for kw in keywords:
                if kw in text:
                    score += 1
            if score > 0:
                scores[goal] = score
        
        if scores:
            return max(scores, key=scores.get)
        return "general"
    
    def _detect_duration(self, text: str) -> str:
        """检测时长"""
        patterns = [
            r'(\d+)\s*天',
            r'(半|一|二|三|四|五|六|两)\s*天',
            r'(\d+)\s*小时',
            r'(\d+)\s*h'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return "待定"
    
    def _extract_company(self, text: str) -> str:
        """提取公司名称"""
        # 常见公司名称模式
        patterns = [
            r'客户[：:]\s*([^\n，。]+)',
            r'([^\n]{2,10})(?:公司|集团|银行|保险|物业|科技)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return "未知"
    
    def _extract_location(self, text: str) -> str:
        """提取地点"""
        pattern = r'(地点|地址|在|于)[：:]\s*([^\n，。]+)'
        match = re.search(pattern, text)
        if match:
            return match.group(2).strip()
        return "待定"
    
    def _extract_participants(self, text: str) -> str:
        """提取参与人数"""
        patterns = [
            r'(\d+)\s*人',
            r'人数[：:]\s*(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1) + "人"
        return "待定"
    
    def _extract_time(self, text: str) -> str:
        """提取时间"""
        patterns = [
            r'(\d{4}年\d{1,2}月)',
            r'(预计\d{1,2}月)',
            r'时间[：:]\s*([^\n，。]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return "待定"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # AI相关
        ai_keywords = ["AI", "人工智能", "大模型", "AIGC", "智能体", "Agent", "提示词", "Prompt"]
        for kw in ai_keywords:
            if kw in text:
                keywords.append(kw)
        
        # 培训相关
        training_keywords = ["培训", "工作坊", "课程", "赋能", "学习", "研讨"]
        for kw in training_keywords:
            if kw in text:
                keywords.append(kw)
        
        return list(set(keywords))


if __name__ == "__main__":
    # 测试
    analyzer = DemandAnalyzer()
    
    test_text = """
    李老师好，这些内容您看看都可以讲吗？
    AI通识类培训-银行技术人员-一天(2次)
    1.AI时代变化、岗位转型、认知
    2.大模型基础
    3.互联网体系
    4.金融范式
    5.工具(提示词重点讲)
    案例结合银行科技/互联网实际来讲
    """
    
    result = analyzer.analyze(test_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
