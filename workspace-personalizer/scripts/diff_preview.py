#!/usr/bin/env python3
"""
diff_preview.py — 生成变更预览
"""
import re, os
from typing import TypedDict

class DiffResult(TypedDict):
    status: str
    current_blocks: str
    new_blocks: str
    summary: str

AUTO_START = "<!-- AUTO-GENERATED: workspace-personalizer -->"
AUTO_END   = "<!-- /AUTO-GENERATED: workspace-personalizer -->"

def extract_auto_blocks(content: str) -> str:
    pattern = re.compile(re.escape(AUTO_START) + r"(.*?)" + re.escape(AUTO_END), re.DOTALL)
    blocks = pattern.findall(content)
    return "\n\n".join(blocks).strip()

def remove_auto_blocks(content: str) -> str:
    pattern = re.compile(re.escape(AUTO_START) + r".*?" + re.escape(AUTO_END), re.DOTALL)
    return pattern.sub("", content).strip()

def diff_preview(filepath: str, new_auto_content: str) -> DiffResult:
    new_wrapped = f"{AUTO_START}\n{new_auto_content}\n{AUTO_END}"
    if not os.path.exists(filepath):
        return DiffResult(status="new", current_blocks="", new_blocks=new_wrapped,
                         summary=f"📄 新建 `{os.path.basename(filepath)}`")
    with open(filepath, "r", encoding="utf-8") as f:
        current_content = f.read()
    current_auto = extract_auto_blocks(current_content)
    if current_auto.strip() == new_auto_content.strip():
        return DiffResult(status="unchanged", current_blocks=current_auto, new_blocks=new_wrapped,
                         summary=f"✅ `{os.path.basename(filepath)}` 无需更新（内容一致）")
    return DiffResult(status="update", current_blocks=current_auto or "(无自动生成块)",
                      new_blocks=new_wrapped,
                      summary=f"🔄 更新 `{os.path.basename(filepath)}`")

def render_preview(diff_result: DiffResult, filename: str) -> str:
    s = diff_result["status"]
    if s == "new":
        return (f"━━━ 新建 | {filename} ━━━\n{diff_result['new_blocks']}\n\n{diff_result['summary']}")
    elif s == "update":
        return (f"━━━ 更新 | {filename} ━━━\n【当前】\n{diff_result['current_blocks']}\n\n【新内容】\n{diff_result['new_blocks']}\n\n{diff_result['summary']}")
    return f"✅ {filename} — 无需更新"

def render_all_previews(results: dict) -> str:
    nc = sum(1 for r in results.values() if r["status"]=="new")
    uc = sum(1 for r in results.values() if r["status"]=="update")
    cc = sum(1 for r in results.values() if r["status"]=="unchanged")
    lines = [f"━━━ 配置变更预览 ━━━\n新增 {nc} | 更新 {uc} | 无变更 {cc}\n"]
    for fn, res in results.items():
        lines.append(render_preview(res, fn))
        lines.append("")
    lines.append("回复【确认写入】执行备份写入。回复【取消】放弃。\n━━━")
    return "\n".join(lines)

if __name__ == "__main__":
    import tempfile, os as _os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(f"# Test\n{AUTO_START}\nold\n{AUTO_END}\n")
        t = f.name
    print(render_preview(diff_preview(t, "new"), "test.md"))
    _os.unlink(t)
    print(render_preview(diff_preview("/nope/file.md", "new"), "brandnew.md"))
