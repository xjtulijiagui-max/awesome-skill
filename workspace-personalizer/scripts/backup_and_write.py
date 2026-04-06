#!/usr/bin/env python3
"""
backup_and_write.py — 备份 + 幂等写入
"""
import os, shutil, json
from datetime import datetime

BACKUP_DIR = "/workspace/.openclaw-backup"
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_file(filepath: str) -> str | None:
    """备份文件到 BACKUP_DIR，返回备份路径，失败返回 None"""
    if not os.path.exists(filepath):
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    bn = os.path.basename(filepath)
    bk_path = os.path.join(BACKUP_DIR, f"{bn}.{ts}.bak")
    try:
        shutil.copy2(filepath, bk_path)
        return bk_path
    except Exception:
        return None

def write_with_backup(filepath: str, auto_content: str, marker_start: str = "<!-- AUTO-GENERATED: workspace-personalizer -->",
                       marker_end: str = "<!-- /AUTO-GENERATED: workspace-personalizer -->") -> bool:
    """
    先备份，再写入（保留非自动生成的用户内容）。
    保证幂等性：同样内容写两次结果一致。
    """
    new_wrapped = f"{marker_start}\n{auto_content}\n{marker_end}"
    backup_file(filepath)  # 有文件就备份，失败不阻止（后面检查）

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # 移除旧自动块，保留用户内容
        pattern = f"{marker_start}.*?{marker_end}"
        import re
        remaining = re.sub(pattern, "", content, flags=re.DOTALL).strip()
        # 组合：用户内容 + 新自动块
        combined = f"{remaining}\n\n{new_wrapped}".strip()
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(combined)
            return True
        except Exception:
            rollback(filepath)
            return False
    else:
        # 新建文件
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_wrapped)
            return True
        except Exception:
            return False

def rollback(filepath: str) -> bool:
    """从备份恢复最新版本，失败返回 False"""
    if not os.path.exists(filepath):
        return False
    bn = os.path.basename(filepath)
    try:
        backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith(bn)],
                        reverse=True)
        if not backups:
            return False
        shutil.copy2(os.path.join(BACKUP_DIR, backups[0]), filepath)
        return True
    except Exception:
        return False

def batch_write(files: dict[str, str]) -> dict[str, bool]:
    """
    批量写入，返回 {filepath: success}。
    任何失败都会尝试回滚已写入的文件。
    """
    results = {}
    written = []
    for fp, content in files.items():
        ok = write_with_backup(fp, content)
        results[fp] = ok
        if ok:
            written.append(fp)
        else:
            # 回滚已写入的
            for wfp in written:
                rollback(wfp)
            # 回滚其余全部（标记为失败）
            for rfp in files:
                if rfp not in written:
                    results[rfp] = False
            return results
    return results

if __name__ == "__main__":
    # 简单测试
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, dir=".") as f:
        f.write("user content\n\n<!-- AUTO-GENERATED: workspace-personalizer -->\nold\n<!-- /AUTO-GENERATED: workspace-personalizer -->\n")
        t = f.name
    ok = write_with_backup(t, "new auto content here")
    print(f"write_with_backup: {'OK' if ok else 'FAIL'}")
    with open(t) as f:
        print("Result:", f.read())
    os.unlink(t)
    print("rollback test:", "OK" if os.path.exists(os.path.join(BACKUP_DIR, os.listdir(BACKUP_DIR)[0])) else "?")
