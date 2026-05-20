#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch extract podcast audio from a list of URLs."""

import sys
import os
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

from podcast_to_audio import process_episode

def main():
    # Default input file
    input_file = Path(__file__).parent / "urls.txt"
    output_dir = Path(__file__).parent / "audio"

    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])

    if not input_file.exists():
        print(f"错误：找不到文件 {input_file}")
        print(f"请创建一个 urls.txt 文件，每行一个链接")
        return 1

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read URLs from file
    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print(f"错误：{input_file} 中没有找到链接")
        return 1

    print(f"找到 {len(urls)} 个链接")
    print(f"输出目录：{output_dir}\n")

    # Process each URL
    failures = 0
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 处理：{url}")

        try:
            output_path, metadata = process_episode(url, output_dir)
            print(f"[OK] 成功：{Path(output_path).name}\n")
        except Exception as e:
            failures += 1
            print(f"[X] 失败：{e}\n")

    # Summary
    print(f"\n完成！{len(urls) - failures}/{len(urls)} 个成功")
    if failures > 0:
        print(f"失败：{failures} 个")

    return 0 if failures == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
