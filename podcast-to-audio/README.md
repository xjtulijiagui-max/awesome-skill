# Podcast to Audio

从播客链接自动提取和下载音频文件的简化工具。

## 功能特点

- ✅ **简单易用**：一个命令下载音频
- ✅ **自动解析**：从播客页面自动提取音频链接
- ✅ **进度显示**：实时显示下载进度
- ✅ **元数据保存**：自动保存来源信息
- ✅ **批量处理**：支持同时下载多个播客

## 快速开始

### 基本用法

```bash
python3 scripts/podcast_to_audio.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --out-dir "./audio"
```

### Slash Command

```
/podcast-to-audio <url>
```

## 输出

- **音频文件**：`<标题>.m4a`（或 mp3 等格式）
- **元数据文件**：`<标题>.meta.json`

## 支持平台

- 小宇宙（Xiaoyuzhou）
- YouTube
- 其他支持 og:audio 的播客平台

## 技术细节

### 工作流程

1. 获取播客页面 HTML
2. 从 `og:audio` 或 JSON-LD 提取音频 URL
3. 下载音频文件到本地
4. 保存元数据 JSON

### 音频格式

支持 M4A、MP3、WAV、FLAC、AAC、OGG、Opus 等格式。

## 注意事项

- 仅用于个人学习和备份
- 请遵守播客平台的使用条款
- 需要稳定的网络连接

## Credits

基于 [podcast-transcript-txt](https://github.com/anthropics/anthropic-quickstarts/tree/main/podcast-transcript-txt) 简化而来，仅保留音频提取功能。

原工具由 [@一龙小包子](https://x.com/KingJing001) 开发。
