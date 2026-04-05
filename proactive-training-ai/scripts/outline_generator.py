#!/usr/bin/env python3
"""
大纲生成器 - 根据需求分析和课程匹配生成完整课程大纲
"""

import json
import os
import re
from typing import Dict, List
from datetime import datetime

class OutlineGenerator:
    """大纲生成器"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.courses = self._load_courses()
        self.cases = self._load_cases()
    
    def _load_courses(self) -> List[Dict]:
        """加载课程库"""
        try:
            with open(os.path.join(self.data_dir, "course_library.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("courses", [])
        except Exception as e:
            print(f"加载课程库失败: {e}")
            return []
    
    def _load_cases(self) -> Dict:
        """加载案例库"""
        try:
            with open(os.path.join(self.data_dir, "case_studies.json"), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {}
    
    def generate(self, demand_text: str, demand_analysis: Dict = None, 
                 course_match: Dict = None, format: str = "markdown") -> str:
        """生成课程大纲"""
        
        # 如果没有传入分析结果，需要重新分析
        if demand_analysis is None:
            from demand_analyzer import DemandAnalyzer
            analyzer = DemandAnalyzer()
            demand_analysis = analyzer.analyze(demand_text)
        
        if course_match is None:
            from course_matcher import CourseMatcher
            matcher = CourseMatcher()
            course_match = matcher.match(
                industry=demand_analysis.get('industry'),
                audience=demand_analysis.get('audience'),
                goal=demand_analysis.get('goal'),
                duration=demand_analysis.get('duration')
            )
        
        # 获取主推荐课程
        main_course_id = course_match.get('recommended_courses', [{}])[0].get('id', 'ai_scenario_innovation')
        main_course = self._get_course_by_id(main_course_id)
        
        if format == "markdown":
            return self._generate_markdown(demand_analysis, main_course, course_match)
        elif format == "json":
            return json.dumps(self._generate_structure(demand_analysis, main_course), ensure_ascii=False, indent=2)
        else:
            return self._generate_markdown(demand_analysis, main_course, course_match)
    
    def _get_course_by_id(self, course_id: str) -> Dict:
        """根据ID获取课程"""
        for course in self.courses:
            if course["id"] == course_id:
                return course
        return self.courses[0] if self.courses else {}
    
    def _generate_markdown(self, demand: Dict, course: Dict, match: Dict) -> str:
        """生成Markdown格式大纲"""
        
        # 提取行业用于案例匹配
        industry = demand.get('industry', 'general')
        industry_name = self._get_industry_name(industry)
        
        # 匹配行业案例
        matched_cases = self._match_cases(industry)
        
        outline = f"""# {course.get('name', 'AI培训课程')}

## 课程基本信息

| 项目 | 内容 |
|------|------|
| **课程名称** | {course.get('name', '待定')} |
| **课程时长** | {demand.get('duration', course.get('duration', ['1天'])[0])} |
| **目标学员** | {demand.get('audience', '企业管理者')} |
| **授课形式** | 讲授 + 案例研讨 + 小组演练 + AI工具实操 |
| **行业定位** | {industry_name} |

---

## 学习目标

完成本课程后，学员将能够：

"""
        
        # 添加学习目标（从课程库获取）
        for i, objective in enumerate(course.get('deliverables', ['掌握AI核心概念', '了解行业应用案例', '实操AI工具']), 1):
            outline += f"{i}. {objective}\n"
        
        outline += f"""
---

## 课程核心框架

```
{course.get('core_framework', '方法论输入 × AI工具加速 × 共创落地')}
```

---

## 课程模块结构

"""
        
        # 添加模块
        for i, module in enumerate(course.get('modules', []), 1):
            outline += f"""### 模块{i}：{module.get('name', f'模块{i}')}

**主要内容：**
"""
            for topic in module.get('topics', []):
                outline += f"- {topic}\n"
            
            outline += "\n"
        
        # 添加行业定制案例
        outline += f"""---

## 行业定制案例（{industry_name}）

"""
        
        for i, case in enumerate(matched_cases[:3], 1):
            outline += f"""**案例{i}：{case.get('company')} - {case.get('scenario')}**
- 成果：{case.get('result')}

"""
        
        # 添加定制建议
        outline += """---

## 定制建议

"""
        
        for suggestion in match.get('customization_suggestions', []):
            outline += f"- {suggestion}\n"
        
        # 添加AI工具清单
        outline += f"""
---

## 配套AI工具

"""
        for tool in course.get('tools', ['DeepSeek', 'Kimi', '通义听悟'])[:5]:
            outline += f"- {tool}\n"
        
        # 添加交付物
        outline += """
---

## 课程交付物

学员将带走：

"""
        for deliverable in course.get('deliverables', ['AI场景清单', '工作模板', '工具使用指南']):
            outline += f"- ✅ {deliverable}\n"
        
        # 添加页脚
        outline += f"""
---

*本大纲由 Proactive Training AI 智能生成*
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*客户需求：{demand.get('raw_text', '')[:50]}...*
"""
        
        return outline
    
    def _generate_structure(self, demand: Dict, course: Dict) -> Dict:
        """生成结构化数据"""
        return {
            "course_name": course.get('name'),
            "duration": demand.get('duration'),
            "audience": demand.get('audience'),
            "industry": demand.get('industry'),
            "modules": course.get('modules'),
            "tools": course.get('tools'),
            "cases": course.get('cases'),
            "deliverables": course.get('deliverables')
        }
    
    def _get_industry_name(self, industry_code: str) -> str:
        """获取行业中文名"""
        mapping = {
            "banking": "银行金融",
            "manufacturing": "制造业",
            "insurance": "保险业",
            "technology": "科技/互联网",
            "design": "设计/创意",
            "property": "物业服务",
            "energy": "能源/公用事业",
            "general": "通用行业"
        }
        return mapping.get(industry_code, "通用行业")
    
    def _match_cases(self, industry: str) -> List[Dict]:
        """匹配行业案例"""
        all_cases = []
        
        # 行业映射到案例类别
        industry_case_map = {
            "banking": ["finance"],
            "insurance": ["finance"],
            "manufacturing": ["manufacturing"],
            "technology": ["technology"],
            "design": ["scenario"],
            "property": ["scenario"],
            "energy": ["energy", "manufacturing"]
        }
        
        case_categories = industry_case_map.get(industry, ["scenario"])
        
        for category in case_categories:
            all_cases.extend(self.cases.get("cases", {}).get(category, []))
        
        # 如果没有匹配到，返回通用场景案例
        if not all_cases:
            all_cases = self.cases.get("cases", {}).get("scenario", [])
        
        return all_cases


if __name__ == "__main__":
    # 测试
    generator = OutlineGenerator()
    
    test_demand = {
        "industry": "banking",
        "audience": "技术人员",
        "duration": "1天",
        "raw_text": "银行技术人员AI通识培训"
    }
    
    test_match = {
        "recommended_courses": [{"id": "ai_organization_change"}],
        "customization_suggestions": ["结合银行科技案例"]
    }
    
    outline = generator.generate("", test_demand, test_match)
    print(outline)
