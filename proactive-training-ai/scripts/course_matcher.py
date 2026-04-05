#!/usr/bin/env python3
"""
课程匹配器 - 根据需求匹配合适的课程产品
"""

import json
import os
from typing import Dict, List

class CourseMatcher:
    """课程匹配器"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.courses = self._load_courses()
        self.keywords = self._load_keywords()
    
    def _load_courses(self) -> List[Dict]:
        """加载课程库"""
        try:
            with open(os.path.join(self.data_dir, "course_library.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("courses", [])
        except Exception as e:
            print(f"加载课程库失败: {e}")
            return []
    
    def _load_keywords(self) -> Dict:
        """加载关键词"""
        try:
            with open(os.path.join(self.data_dir, "industry_keywords.json"), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {}
    
    def match(self, industry: str = None, audience: str = None, goal: str = None, duration: str = None) -> Dict:
        """匹配课程"""
        recommended = []
        customization = []
        
        # 基于行业匹配
        if industry:
            industry_data = self.keywords.get("industries", {}).get(industry, {})
            industry_courses = industry_data.get("recommended_courses", [])
            customization.extend(industry_data.get("customization_points", []))
            
            for course_id in industry_courses:
                course = self._get_course_by_id(course_id)
                if course:
                    recommended.append({
                        "id": course_id,
                        "name": course["name"],
                        "match_score": 90,
                        "reason": f"基于{industry}行业推荐"
                    })
        
        # 基于受众匹配
        if audience:
            audience_data = self.keywords.get("audience_mapping", {}).get(audience, {})
            audience_courses = audience_data.get("recommended_courses", [])
            
            for course_id in audience_courses:
                existing = next((r for r in recommended if r["id"] == course_id), None)
                if existing:
                    existing["match_score"] = min(100, existing["match_score"] + 5)
                    existing["reason"] += f"，适合{audience}受众"
                else:
                    course = self._get_course_by_id(course_id)
                    if course:
                        recommended.append({
                            "id": course_id,
                            "name": course["name"],
                            "match_score": 85,
                            "reason": f"适合{audience}受众"
                        })
        
        # 基于目标匹配
        if goal:
            goal_data = self.keywords.get("goal_mapping", {}).get(goal, {})
            goal_course = goal_data.get("course")
            
            if goal_course:
                existing = next((r for r in recommended if r["id"] == goal_course), None)
                if existing:
                    existing["match_score"] = min(100, existing["match_score"] + 5)
                    existing["reason"] += f"，匹配{goal}目标"
                else:
                    course = self._get_course_by_id(goal_course)
                    if course:
                        recommended.append({
                            "id": goal_course,
                            "name": course["name"],
                            "match_score": 88,
                            "reason": f"匹配{goal}目标"
                        })
        
        # 去重并排序
        seen = set()
        unique_recommended = []
        for r in recommended:
            if r["id"] not in seen:
                seen.add(r["id"])
                unique_recommended.append(r)
        
        unique_recommended.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "recommended_courses": unique_recommended[:3],
            "customization_suggestions": list(set(customization))
        }
    
    def _get_course_by_id(self, course_id: str) -> Dict:
        """根据ID获取课程"""
        for course in self.courses:
            if course["id"] == course_id:
                return course
        return None
    
    def get_course_details(self, course_id: str) -> Dict:
        """获取课程详细信息"""
        return self._get_course_by_id(course_id)


if __name__ == "__main__":
    # 测试
    matcher = CourseMatcher()
    result = matcher.match(
        industry="banking",
        audience="technical",
        goal="scenario"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
