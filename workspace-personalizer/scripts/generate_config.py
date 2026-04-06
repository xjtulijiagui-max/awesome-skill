#!/usr/bin/env python3
"""
generate_config.py — 基于用户输入生成各配置文件内容
"""
import json, os, re
from typing import Optional

# ── 加载 SOUL 预设片段 ──────────────────────────────────────────
_snippets_path = os.path.join(os.path.dirname(__file__), "..", "assets", "default-soul-snippets.json")
_SOUL_SNIPPETS: dict = {}
if os.path.exists(_snippets_path):
    with open(_snippets_path, encoding="utf-8") as f:
        _SOUL_SNIPPETS = json.load(f)

_COLLABORATION_STYLES = {
    "顾问型": {
        "soul_style_desc": "给出思路框架，让用户决策；不直接给最终答案",
        "identity_tone": "引导式、提问式、启发性",
        "principles": [
            ("先理解，再产出", "不急着写，先判断你要的是大纲/方案/还是评审意见"),
            ("结构比堆料更重要", "逻辑顺、顺序对、标题准、重点清"),
            ("追求可直接交付", "能直接复制不只给思路；能直接替换不只提建议"),
        ],
        "judgment": ["能不能直接拿去给客户看", "能不能直接拿去给学员讲", "能不能直接立项/提案"],
    },
    "执行型": {
        "soul_style_desc": "直接产出，用户只做审核；给出可直接交付的版本",
        "identity_tone": "确定式、结论式、高效直接",
        "principles": [
            ("直接输出，不绕弯", "一上来就给可用的版本，边用边调"),
            ("结构清晰", "逻辑顺、顺序对、标题准、重点清"),
            ("追求可直接交付", "能直接复制使用的就不要只给思路"),
        ],
        "judgment": ["能不能直接发给客户", "能不能直接拿去制作", "能不能直接立项"],
    },
    "挑战型": {
        "soul_style_desc": "主动指出逻辑漏洞，挑战假设，推动用户思考更深",
        "identity_tone": "直接、批判性但建设性",
        "principles": [
            ("先质疑，再产出", "指出逻辑漏洞，不接受模糊需求"),
            ("逻辑优先", "结构顺、假设可验证、结论有支撑"),
            ("追求严谨交付", "能经受住评审的方案才是好方案"),
        ],
        "judgment": ["逻辑是否严密", "假设是否可验证", "能否通过专家评审"],
    },
    "创意型": {
        "soul_style_desc": "发散思维，给多个方向选项，帮助突破框架",
        "identity_tone": "开放、鼓励实验、充满热情",
        "principles": [
            ("多方案并行", "先给多个方向，再聚焦最优解"),
            ("打破常规", "鼓励尝试新形式、新方法"),
            ("追求创新交付", "让人眼前一亮的方案才是好方案"),
        ],
        "judgment": ["是否有新意", "是否超出客户预期", "是否具有传播性"],
    },
}

_TOOL_MAP: dict = {
    "培训师": [
        ("minimax-pdf", "生成高质量培训手册 PDF（封面+正文+排版）"),
        ("minimax-docx", "撰写培训方案 Word 文档"),
        ("pptx-generator", "生成/打磨培训 PPT"),
        ("batch_web_search", "搜集行业案例、政策解读"),
        ("batch_text_to_video", "生成培训导入视频素材"),
        ("images_understand", "分析参考图/PPT 截图，提炼风格"),
    ],
    "产品经理": [
        ("batch_web_search", "搜集竞品信息、市场数据"),
        ("minimax-docx", "撰写 PRD、产品方案文档"),
        ("minimax-pdf", "输出产品报告 PDF"),
        ("extract_content_from_websites", "深度读取行业分析文章"),
    ],
    "开发者": [
        ("batch_web_search", "搜索技术文档、解决方案"),
        ("extract_content_from_websites", "读取 API 文档、技术博客"),
    ],
    "内容创作者": [
        ("batch_web_search", "搜集选题资料、热点话题"),
        ("minimax-pdf", "输出电子书、深度报告 PDF"),
        ("batch_text_to_video", "生成短视频脚本/素材"),
    ],
    "HR/人才发展": [
        ("minimax-docx", "撰写人才发展方案、JD"),
        ("minimax-pdf", "生成培训手册、评估报告 PDF"),
        ("pptx-generator", "制作内部培训 PPT"),
        ("batch_web_search", "搜集行业人才趋势报告"),
    ],
    "创业者": [
        ("batch_web_search", "搜集市场情报、竞品动态"),
        ("minimax-docx", "撰写商业计划书、融资材料"),
        ("minimax-pdf", "输出商业计划书 PDF"),
        ("extract_content_from_websites", "读取行业深度报告"),
    ],
    "老师/大学教授": [
        ("minimax-pdf", "生成课程讲义 PDF"),
        ("pptx-generator", "制作课程 PPT"),
        ("batch_web_search", "搜集学科前沿案例"),
        ("minimax-docx", "撰写教学大纲、教案"),
    ],
    "律师": [
        ("batch_web_search", "搜集法律法规、判例"),
        ("extract_content_from_websites", "读取法规原文、判例分析"),
        ("minimax-docx", "撰写法律意见书、合同"),
    ],
    "销售/客户成功": [
        ("batch_web_search", "搜集客户行业情报"),
        ("minimax-docx", "撰写客户方案、提案"),
        ("minimax-pdf", "输出客户演示 PDF"),
    ],
}

_HEARTBEAT_TEMPLATES: dict = {
    "培训师": {
        "active_start": "08:00", "active_end": "21:00",
        "silent_start": "21:00", "silent_end": "08:00",
        "checks": ["邮件/未读消息", "日历/未来3天事件", "项目进度更新"],
        "morning_time": "08:30", "afternoon_time": "18:00",
        "look_ahead": "3天", "advance_reminder": "1小时",
    },
    "产品经理": {
        "active_start": "09:00", "active_end": "20:00",
        "silent_start": "20:00", "silent_end": "09:00",
        "checks": ["邮件/未读消息", "日历/未来3天评审", "飞书/企微未读"],
        "morning_time": "09:00", "afternoon_time": "18:30",
        "look_ahead": "3天", "advance_reminder": "2小时",
    },
    "开发者": {
        "active_start": "09:00", "active_end": "22:00",
        "silent_start": "22:00", "silent_end": "09:00",
        "checks": ["GitHub/GitLab 更新", "CI/CD 状态", "日历/会议"],
        "morning_time": "09:30", "afternoon_time": "18:00",
        "look_ahead": "2天", "advance_reminder": "30分钟",
    },
    "default": {
        "active_start": "09:00", "active_end": "20:00",
        "silent_start": "20:00", "silent_end": "09:00",
        "checks": ["邮件/未读消息", "日历/未来3天事件"],
        "morning_time": "09:00", "afternoon_time": "18:00",
        "look_ahead": "3天", "advance_reminder": "1小时",
    },
}


def _infer_industry(occupation: str, service_object: str) -> str:
    if service_object:
        return service_object
    if occupation in ["培训师", "HR/人才发展"]:
        return "企业培训/人力资源"
    if occupation in ["产品经理"]:
        return "互联网/科技"
    if occupation == "律师":
        return "法律服务"
    if occupation in ["销售/客户成功"]:
        return "B2B 销售/客户服务"
    return "通用行业"


def _infer_output_formats(outputs: list) -> str:
    lines = []
    for o in outputs:
        o_lower = o.lower()
        if "ppt" in o_lower or "幻灯片" in o:
            lines.append("- PPT → PPTX（附演讲备注）")
        if "word" in o_lower or "文档" in o or "方案" in o:
            lines.append("- 方案文档 → Word")
        if "pdf" in o_lower or "手册" in o or "报告" in o:
            lines.append("- 报告/手册 → PDF")
        if "大纲" in o or "课纲" in o:
            lines.append("- 课程大纲 → Markdown / Word")
        if "竞品" in o or "分析" in o:
            lines.append("- 分析报告 → Word + 图表")
    if not lines:
        lines.append("- 通用文档 → Markdown")
    return "\n".join(lines)


def _generate_ai_name(user_inputs: dict) -> str:
    if user_inputs.get("ai_name"):
        return user_inputs["ai_name"]
    occupation = user_inputs.get("occupation", "")
    style = user_inputs.get("collaboration_style", "顾问型")
    names = {
        "培训师": "灵渊",
        "产品经理": "探微",
        "开发者": "码渊",
        "内容创作者": "墨语",
        "HR/人才发展": "知行",
        "创业者": "破局",
        "老师/大学教授": "明德",
        "律师": "辩机",
        "销售/客户成功": "赢谋",
    }
    base = names.get(occupation, "灵知")
    return f"{base}-{style[0]}" if style != "顾问型" else base


def _generate_name_meaning(ai_name: str) -> str:
    meanings = {
        "灵渊": "灵感有源，帮助知识找到最容易被吸收的路径",
        "探微": "洞察细节，探微知著",
        "码渊": "代码的深度与广度",
        "墨语": "笔墨之间，尽显思想",
        "知行": "知行合一，人才发展之道",
        "破局": "突破困境，开创新局",
        "明德": "明德新民，止于至善",
        "辩机": "辨析法理，把握关键",
        "赢谋": "洞察客户，赢得信任",
    }
    for k, v in meanings.items():
        if k in ai_name:
            return v
    return f"智慧同行，助你高效工作"


class ConfigGenerator:
    def __init__(self, user_inputs: dict):
        self.inputs = user_inputs
        self.occupation = user_inputs.get("occupation", "通用")
        self.outputs = user_inputs.get("outputs", [])
        self.service_object = user_inputs.get("service_object", "")
        self.collaboration_style = user_inputs.get("collaboration_style", "顾问型")
        self.ai_name = _generate_ai_name(user_inputs)
        self.industry = _infer_industry(self.occupation, self.service_object)
        self.timezone = user_inputs.get("timezone", "Asia/Shanghai")
        self.reporting_style = user_inputs.get("reporting_style", "结论先行，适合领导层阅读")
        self.heartbeat = _HEARTBEAT_TEMPLATES.get(self.occupation, _HEARTBEAT_TEMPLATES["default"])

    # ── USER.md ─────────────────────────────────────────────────
    def generate_USER_md(self) -> str:
        outputs_str = "、".join(self.outputs) if self.outputs else "通用工作产出"
        tools = _TOOL_MAP.get(self.occupation, [])
        tool_names = "、".join([t[0] for t in tools[:3]]) if tools else "通用工具"
        output_formats = _infer_output_formats(self.outputs)

        return (
            f"- **职业：** {self.occupation}\n"
            f"- **主要输出：** {outputs_str}\n"
            f"- **时区：** {self.timezone}\n"
            f"\n## 业务背景\n"
            f"- **行业/领域：** {self.industry}\n"
            f"- **主要客户/场景：** {self.service_object or '通用业务场景'}\n"
            f"- **当前项目：** [进行中的项目可随时补充]\n"
            f"\n## 协作偏好\n"
            f"- **AI搭档风格：** {self.collaboration_style}——"
            f"{_COLLABORATION_STYLES.get(self.collaboration_style, {}).get('soul_style_desc', '')}\n"
            f"- **汇报风格：** {self.reporting_style}\n"
            f"- **案例偏好：** {self.industry}行业案例\n"
            f"- **输出格式：**\n{output_formats}\n"
            f"\n## 常用工具\n"
            f"- 已有：OpenClaw（AI协作平台）\n"
            f"- 常用AI工具：{tool_names}\n"
            f"- 偏好：能直接产出的就不要只给思路"
        )

    # ── SOUL.md ─────────────────────────────────────────────────
    def generate_SOUL_md(self) -> str:
        style_info = _COLLABORATION_STYLES.get(self.collaboration_style, _COLLABORATION_STYLES["顾问型"])
        principles = style_info["principles"]
        judgment = style_info["judgment"]

        # 从预设片段中查找
        snippet_key = next((k for k in _SOUL_SNIPPETS if k in self.occupation), None)
        if snippet_key:
            preset = _SOUL_SNIPPETS[snippet_key]
        else:
            preset = _SOUL_SNIPPETS.get("培训师", {})

        capable_items = preset.get("capable_items", [
            ("核心能力1", "描述1"),
            ("核心能力2", "描述2"),
            ("核心能力3", "描述3"),
            ("核心能力4", "描述4"),
            ("核心能力5", "描述5"),
        ])

        capable_lines = []
        for i, (title, desc) in enumerate(capable_items[:5], 1):
            capable_lines.append(f"{i}. **{title}**\n   {desc}")

        principle_lines = []
        for title, content in principles:
            principle_lines.append(f'1. **{title}** — {content}')

        judgment_lines = [f"- {j}" for j in judgment]

        examples = preset.get("example_phrases", [
            f'"帮我做一个{self.occupation}相关的输出"',
            '"看看这个内容有没有问题"',
        ])

        return (
            f"{{{self.ai_name}_}}是您的AI{self.occupation}搭档。不是写字机器，"
            f"是能把\"模糊需求\"变成\"可直接交付成果\"的{self.collaboration_style}。_\n"
            f"\n## 核心定位\n"
            f"我是一名**AI{self.occupation}搭档**，专注于帮助{self.occupation}高效完成工作。\n"
            f"\n我最擅长的事情包括：\n\n"
            + "\n\n".join(capable_lines) + "\n"
            f"\n---\n"
            f"\n## 我帮你搞定\n"
            + "\n".join([f"- {preset.get('solve_items', ['搞定事项1', '搞定事项2', '搞定事项3'])[i] if i < len(preset.get('solve_items', [])) else f'搞定事项{i+1}'}" for i in range(5)]) + "\n"
            f"\n---\n"
            f"\n## 我的工作原则\n\n"
            + "\n".join(principle_lines) + "\n"
            f"\n---\n"
            f"\n## 我的判断标准\n"
            f"\n一份输出是否合格，看：\n"
            + "\n".join(judgment_lines) + "\n"
            f"\n---\n"
            f"\n## 对我说话的方式\n"
            f"\n直接告诉我你的需求，越具体越好，比如：\n\n"
            + "\n".join([f"> {e}" for e in examples]) + "\n\n"
            f"我会判断你要的类型，然后直接输出对应的成果。"
        )

    # ── IDENTITY.md ─────────────────────────────────────────────
    def generate_IDENTITY_md(self) -> str:
        style_info = _COLLABORATION_STYLES.get(self.collaboration_style, {})
        tone = style_info.get("identity_tone", "专业、沉稳、有结构感")
        meaning = _generate_name_meaning(self.ai_name)

        return (
            f"- **名字：** {self.ai_name}\n"
            f"- **角色：** AI{self.occupation}搭档\n"
            f"- **风格：** {tone}\n"
            f"- **签名 emoji：** 🧠\n"
            f"- **头像：** [待设置，建议用深蓝色系专业头像]\n"
            f"\n---\n"
            f"{{{self.ai_name}_}}是我的名字。寓意\"{meaning}\"。_"
        )

    # ── HEARTBEAT.md ────────────────────────────────────────────
    def generate_HEARTBEAT_md(self) -> str:
        hb = self.heartbeat
        checks_str = "\n".join([f"- [ ] {c}" for c in hb["checks"]])

        return (
            f"## 推送时段\n"
            f"- **活跃时段：** {hb['active_start']} - {hb['active_end']}\n"
            f"- **静默时段：** {hb['silent_start']} - {hb['silent_end']}（除非紧急，否则不主动推送）\n"
            f"- **时区：** {self.timezone}\n"
            f"\n## 推送频率\n"
            f"- 日常：1-2 次/工作日\n"
            f"- 周末：根据项目需要，不主动打扰\n"
            f"\n## 推送内容类型\n"
            f"根据工作节奏轮转推送以下内容：\n\n"
            f"1. **每日开始**（{hb['morning_time']}）\n"
            f"   - 当日任务预览\n"
            f"   - 重要截止日期提醒\n\n"
            f"2. **每日结束**（{hb['afternoon_time']}）\n"
            f"   - 当日完成情况汇总\n"
            f"   - 次日优先事项提示\n\n"
            f"3. **每周五**\n"
            f"   - 本周工作摘要\n"
            f"   - 下周重点预告\n\n"
            f"4. **按需**\n"
            f"   - 重要邮件/消息提醒\n"
            f"   - 日历事件提前 {hb['advance_reminder']} 通知\n"
            f"\n## 心跳检查清单\n"
            f"每次心跳轮转检查（不超过 3 项）：\n\n{checks_str}\n"
            f"\n## 静默规则\n"
            f"- 晚间 {hb['silent_start']} 后不主动推送\n"
            f"- 周末除非紧急，否则静默\n"
            f"- 连续 3 天无互动后降低推送频率"
        )

    # ── TOOLS.md ───────────────────────────────────────────────
    def generate_TOOLS_md(self) -> str:
        tools = _TOOL_MAP.get(self.occupation, [])
        output_formats = _infer_output_formats(self.outputs)

        if not tools:
            return (
                f"## 核心工具\n\n"
                f"| 工具 | 用途 |\n"
                f"|------|------|\n"
                f"| batch_web_search | 搜集资料、信息检索 |\n\n"
                f"## 输出格式规范\n\n{output_formats}\n\n"
                f"## 快捷指令\n\n"
                f"- \"帮我搜索\" → 启动信息搜集\n"
                f"- \"生成内容\" → 启动内容创作"
            )

        tool_rows = "\n".join([f"| `{t[0]}` | {t[1]} |" for t in tools])

        return (
            f"## 已接入的核心工具\n\n"
            f"| 工具 | 用途 |\n"
            f"|------|------|\n"
            f"{tool_rows}\n"
            f"\n---\n"
            f"\n## 输出格式规范\n\n{output_formats}\n"
            f"\n---\n"
            f"\n## 工作流惯例\n\n"
            f"1. 收到任务 → 确认目标 → 输出结构 → 用户确认 → 产出细节\n"
            f"2. 重要输出 → 先出大纲 → 用户确认 → 再出完整内容\n"
            f"3. 方案评审 → 先整体读一遍 → 给修改建议 → 出优化版本\n"
            f"\n---\n"
            f"\n## 快捷指令\n\n"
            f"- \"帮我设计一个课\" → 启动课程设计流程\n"
            f"- \"做个方案\" → 启动方案撰写\n"
            f"- \"打磨PPT\" → 启动PPT评审与优化\n"
            f"- \"搜一些案例\" → 按当前主题搜集行业案例\n"
            f"- \"帮我看看这个大纲\" → 启动评审模式"
        )

    # ── AGENTS.md（空实现，默认不生成）─────────────────────────
    def generate_AGENTS_md(self) -> str:
        return ""

    # ── MEMORY.md ──────────────────────────────────────────────
    def generate_MEMORY_md(self) -> str:
        from datetime import date
        today = date.today().isoformat()
        return (
            f"## 用户背景\n\n"
            f"- 职业：{self.occupation}\n"
            f"- 主要工作：{', '.join(self.outputs) if self.outputs else '通用工作'}\n"
            f"- 协作风格：{self.collaboration_style}\n"
            f"- 服务对象：{self.service_object or '通用'}\n"
            f"\n## 已知偏好\n\n"
            f"- 输出格式偏好：见 USER.md\n"
            f"- AI搭档风格：{self.collaboration_style}\n"
            f"\n## 重要上下文\n\n"
            f"- 行业：{self.industry}\n"
            f"- 时区：{self.timezone}\n"
            f"\n## 更新记录\n\n"
            f"- {today}：初始化配置"
        )

    # ── BOOTSTRAP.md ───────────────────────────────────────────
    def generate_BOOTSTRAP_md(self) -> str:
        return (
            f"这是你的 OpenClaw 首次配置。\n\n"
            f"你已经通过 workspace-personalizer 完成了初始化配置：\n"
            f"- IDENTITY.md ✅\n"
            f"- SOUL.md ✅\n"
            f"- USER.md ✅\n"
            f"- TOOLS.md ✅\n"
            f"- HEARTBEAT.md ✅\n"
            f"- MEMORY.md ✅\n\n"
            f"配置完成后，请删除此文件。你不需要再看到它。\n\n"
            f"——你的 AI 搭档 {self.ai_name}"
        )

    # ── 全量生成 ──────────────────────────────────────────────
    def generate_all(self) -> dict:
        files = {
            "USER.md": self.generate_USER_md(),
            "SOUL.md": self.generate_SOUL_md(),
            "IDENTITY.md": self.generate_IDENTITY_md(),
            "HEARTBEAT.md": self.generate_HEARTBEAT_md(),
            "TOOLS.md": self.generate_TOOLS_md(),
            "MEMORY.md": self.generate_MEMORY_md(),
            "BOOTSTRAP.md": self.generate_BOOTSTRAP_md(),
        }
        # AGENTS.md 默认不生成（空字符串过滤掉）
        return {k: v for k, v in files.items() if v}


if __name__ == "__main__":
    test_inputs = {
        "occupation": "产品经理",
        "outputs": ["PRD", "竞品分析报告"],
        "service_object": "企业管理层",
        "collaboration_style": "顾问型",
        "timezone": "Asia/Shanghai",
    }
    gen = ConfigGenerator(test_inputs)
    all_files = gen.generate_all()
    print("Generated files:", list(all_files.keys()))
    print("\nSOUL.md preview:")
    print(all_files["SOUL.md"][:300])
    print("\nIDENTITY.md:")
    print(all_files["IDENTITY.md"])
