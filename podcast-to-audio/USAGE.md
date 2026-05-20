# 🚀 播客音频提取工具 - 使用指南

## 完全自动化使用（推荐，无需确认）

### 批量提取多个播客

**步骤 1**：创建 `urls.txt` 文件，每行一个链接：

```text
https://www.xiaoyuzhoufm.com/episode/69eb5dfc1d989496e76d373c
https://www.xiaoyuzhoufm.com/episode/69e96b5b1e94ae6921ee3c2b
```

**步骤 2**：运行批量提取脚本：

```bash
python3 batch_extract.py
```

所有链接会自动依次处理，无需任何确认！

### 单链接快速提取

**Windows 用户**（推荐）：
```bash
extract.bat "https://www.xiaoyuzhoufm.com/episode/69eb5dfc1d989496e76d373c"
```

**Mac/Linux 用户**：
```bash
python3 scripts/podcast_to_audio.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69eb5dfc1d989496e76d373c" \
  --out-dir "./audio"
```

### 使用 Slash Command

在 Claude Code 中直接使用：
```
/podcast-to-audio <播客链接>
```

## 📁 输出位置

所有音频文件默认保存到：`./audio/` 目录

每个播客会生成两个文件：
- `标题.m4a` - 音频文件
- `标题.meta.json` - 元数据（包含来源链接、文件大小等信息）

## 💡 提示

1. **批量处理时**：把所有链接放到 `urls.txt`，运行一次即可自动处理全部
2. **断点续传**：如果批量处理中断，只需从 `urls.txt` 中删除已完成的链接，重新运行即可
3. **文件管理**：音频文件会自动使用播客标题命名，方便识别

## 🔧 故障排除

**问题**：中文文件名乱码
- **解决**：已修复 Windows 编码问题，如仍有问题请更新脚本

**问题**：下载速度慢
- **解决**：这是正常的，取决于网络和音频文件大小

**问题**：无法解析音频链接
- **解决**：确认链接是小宇宙 episode 页面，而不是专辑首页
