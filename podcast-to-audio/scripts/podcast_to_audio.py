#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract podcast audio from Xiaoyuzhou and other platforms."""

import argparse
import html
import json
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)

AUDIO_EXTS = (".m4a", ".mp3", ".wav", ".flac", ".aac", ".ogg", ".opus")


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:180] if len(name) > 180 else name


def compact_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def http_get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def extract_og_content(page_html: str, prop: str) -> Optional[str]:
    p = re.escape(prop)
    patterns = [
        rf'<meta[^>]+property=["\']{p}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']{p}["\']',
        rf'<meta[^>]+name=["\']{p}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']{p}["\']',
    ]
    for pattern in patterns:
        m = re.search(pattern, page_html, flags=re.I)
        if m:
            return html.unescape(m.group(1).strip())
    return None


def title_from_page_html(page_html: str) -> str:
    title = extract_og_content(page_html, "og:title")
    if title:
        return compact_ws(title)
    m = re.search(r"<title>(.*?)</title>", page_html, flags=re.I | re.S)
    return compact_ws(html.unescape(m.group(1))) if m else "podcast episode"


def extract_audio_from_episode_page(url: str, page_html: Optional[str] = None) -> Tuple[str, str]:
    """Extract audio URL and title from podcast episode page."""
    page = page_html if page_html is not None else http_get(url, timeout=30)

    # Try og:audio first
    audio = extract_og_content(page, "og:audio")

    # Fallback to JSON-LD
    if not audio:
        ld = re.findall(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            page,
            flags=re.I | re.S,
        )
        for block in ld:
            try:
                data = json.loads(block)
            except Exception:
                continue
            if isinstance(data, dict):
                media = data.get("associatedMedia") or {}
                if isinstance(media, dict):
                    v = media.get("contentUrl")
                    if isinstance(v, str) and v.startswith("http"):
                        audio = v
                        break

    if not audio:
        raise RuntimeError("Episode page has no og:audio or associatedMedia.contentUrl")

    return title_from_page_html(page), compact_ws(audio)


def download_audio_file(audio_url: str, dest: Path) -> None:
    """Download audio file to destination."""
    print(f"Downloading audio from: {audio_url}")
    req = urllib.request.Request(audio_url, headers={"User-Agent": UA})

    try:
        with urllib.request.urlopen(req, timeout=90) as resp, open(dest, "wb") as f:
            # Download with progress indication
            total_size = resp.getheader("Content-Length")
            if total_size:
                total_size = int(total_size)
                downloaded = 0
                chunk_size = 1024 * 1024  # 1MB chunks

                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end="")
                print()  # New line after progress
            else:
                shutil.copyfileobj(resp, f, length=1 << 20)

        print(f"[OK] Downloaded to: {dest}")
    except Exception as e:
        # Clean up partial download
        if dest.exists():
            dest.unlink()
        raise RuntimeError(f"Failed to download audio: {e}") from e


def process_episode(url: str, out_dir: Path) -> Tuple[Path, dict]:
    """Extract and download audio from a podcast episode."""
    metadata = {
        "input": url,
        "status": "pending",
        "title": None,
        "audio_url": None,
        "output_file": None,
        "file_size": None,
    }

    try:
        # Extract audio URL and title
        print(f"Processing episode: {url}")
        title, audio_url = extract_audio_from_episode_page(url)

        metadata["title"] = title
        metadata["audio_url"] = audio_url

        print(f"Title: {title}")
        print(f"Audio URL: {audio_url}")

        # Determine output filename
        filename = sanitize_filename(title)
        # Try to preserve original extension from URL
        audio_url_path = urllib.parse.urlparse(audio_url).path
        ext = Path(audio_url_path).suffix.lower()
        if ext not in AUDIO_EXTS:
            ext = ".m4a"  # Default to m4a

        output_path = out_dir / f"{filename}{ext}"

        # Download audio
        download_audio_file(audio_url, output_path)

        # Get file size
        file_size = output_path.stat().st_size
        metadata["output_file"] = str(output_path)
        metadata["file_size"] = file_size
        metadata["status"] = "ok"

        # Save metadata
        meta_path = out_dir / f"{filename}.meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"[OK] Metadata saved to: {meta_path}")
        print(f"File size: {file_size / (1024*1024):.2f} MB")

        return output_path, metadata

    except Exception as e:
        metadata["status"] = "failed"
        metadata["error"] = str(e)
        raise RuntimeError(f"Failed to process episode: {e}") from e


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract podcast audio from episode pages. Supports Xiaoyuzhou, YouTube, and other platforms."
    )
    parser.add_argument("--input", action="append", help="Podcast episode URL(s)")
    parser.add_argument("--out-dir", default="./audio", help="Output directory for audio files")
    args = parser.parse_args()

    if not args.input:
        parser.error("At least one --input is required")

    # Create output directory
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Output directory: {out_dir}")
    print(f"Processing {len(args.input)} episode(s)...\n")

    failures = 0
    for url in args.input:
        try:
            output_path, metadata = process_episode(url, out_dir)
            print(f"\n[OK] SUCCESS: {output_path}\n")
        except Exception as e:
            failures += 1
            print(f"\n[X] FAILED: {url}", file=sys.stderr)
            print(f"  Error: {e}\n", file=sys.stderr)

    if failures > 0:
        print(f"\n{failures} out of {len(args.input)} episode(s) failed", file=sys.stderr)
        return 1

    print(f"\n[OK] All {len(args.input)} episode(s) processed successfully!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
