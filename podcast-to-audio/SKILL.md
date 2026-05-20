---
name: podcast-to-audio
description: 从播客链接自动提取和下载音频文件。支持小宇宙、YouTube等平台，一键获取 m4a/mp3 音频文件。
---

# Podcast to Audio

## Overview
**一键式播客音频提取工具** - 输入播客链接，自动下载音频文件到本地。

### 功能特性
- ✅ **自动提取**：从播客页面自动解析并下载音频文件
- ✅ **多平台支持**：小宇宙、YouTube 等主流播客平台
- ✅ **进度显示**：实时显示下载进度和文件大小
- ✅ **元数据保存**：自动保存 .meta.json 文件记录来源信息
- ✅ **批量处理**：支持一次性处理多个播客链接

**适用场景**：
- 离线收听播客
- 备份播客音频
- 提取音频进行后期处理

## Quick Start

### 基本用法

```bash
# 下载单个播客音频
python3 scripts/podcast_to_audio.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --out-dir "./audio"
```

### 批量下载

```bash
# 下载多个播客
python3 scripts/podcast_to_audio.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --input "https://www.xiaoyuzhoufm.com/episode/69f231defbed7ba941222e98" \
  --out-dir "./audio"
```

## Usage Examples

### 小宇宙播客

```bash
python3 scripts/podcast_to_audio.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --out-dir "./podcasts"
```

**输出示例**：
```
Processing episode: https://www.xiaoyuzhoufm.com/episode/...
Title: 商业访谈录 - 136. 全球大模型季报第9集
Audio URL: https://media.xyzcdn.net/...
Downloading audio from: https://media.xyzcdn.net/...
Progress: 100.0% (52456789/52456789 bytes)
✓ Downloaded to: ./podcasts/商业访谈录 - 136. 全球大模型季报第9集.m4a
✓ Metadata saved to: ./podcasts/商业访谈录 - 136. 全球大模型季报第9集.meta.json
File size: 50.03 MB

✓ SUCCESS: ./podcasts/商业访谈录 - 136. 全球大模型季报第9集.m4a
```

### YouTube 视频

```bash
python3 scripts/podcast_to_audio.py \
  --input "https://www.youtube.com/watch?v=n1E9IZfvGMA" \
  --out-dir "./youtube-audio"
```

## Output Files

对于每个输入的播客链接，工具会生成：

1. **`<title>.m4a`** (或 `.mp3` 等) - 音频文件
2. **`<title>.meta.json`** - 元数据文件，包含：
   - 输入链接
   - 播客标题
   - 音频 URL
   - 输出文件路径
   - 文件大小
   - 处理状态

**元数据示例**：
```json
{
  "input": "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14",
  "status": "ok",
  "title": "商业访谈录 - 136. 全球大模型季报第9集",
  "audio_url": "https://media.xyzcdn.net/...",
  "output_file": "/path/to/audio/商业访谈录 - 136. 全球大模型季报第9集.m4a",
  "file_size": 52456789
}
```

## Supported Platforms

| 平台 | URL 格式 | 支持状态 |
|------|----------|---------|
| **小宇宙** | `https://www.xiaoyuzhoufm.com/episode/...` | ✅ 完全支持 |
| **YouTube** | `https://www.youtube.com/watch?v=...` | ✅ 支持 |
| **其他播客平台** | 包含 `og:audio` 的页面 | ✅ 支持 |

## Troubleshooting

### 下载失败

**问题**：网络连接超时或下载中断

**解决方案**：
```bash
# 检查网络连接
ping www.xiaoyuzhoufm.com

# 重新运行命令
python3 scripts/podcast_to_audio.py --input "URL" --out-dir "./audio"
```

### 无法解析音频 URL

**问题**：页面不包含 `og:audio` 或 `associatedMedia.contentUrl`

**解决方案**：
- 确认链接是播客episode页面（不是专辑首页）
- 尝试使用其他播客平台的链接
- 查看页面源代码确认是否有音频信息

### 文件名问题

**问题**：文件名包含特殊字符导致保存失败

**解决方案**：工具会自动清理文件名，移除非法字符
- `/` `:` `*` `?` `"` `<` `>` `|` 等字符会被替换为空格
- 文件名长度限制为 180 个字符

## Advanced Usage

### 自定义输出目录

```bash
# 保存到指定目录
python3 scripts/podcast_to_audio.py \
  --input "URL" \
  --out-dir "/path/to/custom/dir"
```

### 批量下载脚本

创建 `batch_download.sh`：
```bash
#!/bin/bash
# 批量下载播客列表

urls=(
  "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14"
  "https://www.xiaoyuzhoufm.com/episode/69f231defbed7ba941222e98"
  "https://www.youtube.com/watch?v=n1E9IZfvGMA"
)

for url in "${urls[@]}"; do
  python3 scripts/podcast_to_audio.py \
    --input "$url" \
    --out-dir "./podcasts"
done
```

运行：
```bash
chmod +x batch_download.sh
./batch_download.sh
```

## Technical Details

### 工作原理

1. **页面解析**：获取播客 episode 页面 HTML
2. **元数据提取**：
   - 从 `<meta property="og:audio">` 提取音频 URL
   - 从 JSON-LD `associatedMedia.contentUrl` 提取音频 URL
   - 从 `<meta property="og:title">` 提取标题
3. **文件下载**：使用 urllib 下载音频文件，显示进度
4. **元数据保存**：保存 .meta.json 记录处理信息

### 支持的音频格式

- M4A (默认)
- MP3
- WAV
- FLAC
- AAC
- OGG
- Opus

### 网络配置

如果遇到网络问题，可以设置代理（环境变量）：
```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"

python3 scripts/podcast_to_audio.py --input "URL" --out-dir "./audio"
```

## Notes

- **仅提取音频**：此工具只下载音频文件，不进行转写或内容处理
- **合法使用**：请遵守播客平台的使用条款，下载的内容仅供个人使用
- **网络要求**：需要稳定的网络连接，下载大文件时可能需要较长时间

## Credits

Based on the podcast-transcript-txt skill by [@一龙小包子](https://x.com/KingJing001).

This is a simplified version focused only on audio extraction, without transcription or content processing features.
