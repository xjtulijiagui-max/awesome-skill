---
name: podcast-transcript-txt-public
description: Public version of podcast transcript tool - requires your own Volcano Engine ASR credentials or local ASR setup. Deterministic workflow to find and export full podcast transcripts as cleaned TXT files from YouTube URLs, episode webpages (including Xiaoyuzhou), Apple Podcasts title search, X/Twitter links, direct audio URLs, or plain episode titles.
---

# Podcast Transcript TXT (Public Version)

🎯 **完全自动化播客转录工具** - 需要您自己配置 ASR 凭证

## ✨ 特性

- ✅ **完全自动化**：支持小宇宙、YouTube、Scripod 等平台
- ✅ **云端ASR支持**：可集成火山引擎ASR，高质量中文识别（需自己配置）
- ✅ **本地ASR备选**：faster-whisper 本地转录（无需API密钥）
- ✅ **智能降级**：官方转录 > 字幕 > 云端ASR > 本地ASR
- ✅ **零预装凭证**：所有敏感信息通过环境变量配置

## 🚀 快速开始

### 选项 1：使用火山引擎 ASR（推荐，需配置）

```bash
# 设置火山引擎凭证
export VOLCANO_APP_ID="your_app_id"
export VOLCANO_ACCESS_KEY="your_access_key"

# 运行转录
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public
python scripts\podcast_transcript_txt.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --out-dir "./transcripts"
```

### 选项 2：使用本地 ASR（无需 API 密钥）

```bash
# 安装依赖
pip install faster-whisper yt-dlp

# 运行转录
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public
python scripts\podcast_transcript_txt.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --out-dir "./transcripts"
```

### 选项 3：优先使用官方转录和字幕（无需任何配置）

```bash
# YouTube 视频会自动使用字幕
python scripts\podcast_transcript_txt.py \
  --input "https://www.youtube.com/watch?v=n1E9IZfvGMA" \
  --out-dir "./transcripts"
```

## 📋 工作流程

```
输入链接
    ↓
自动识别平台
    ↓
尝试官方转录（Priority A）
    ↓ 失败
尝试平台字幕（Priority B）
    ↓ 失败
提取页面文本（Priority C）
    ↓ 失败
火山引擎 ASR（Priority D）- 需要配置凭证 🔑
    ↓ 失败/未配置
本地 faster-whisper ASR（Priority E）
    ↓
输出 TXT + 元数据
```

## ⚙️ 配置说明

### 火山引擎 ASR 配置（可选但推荐）

1. **获取凭证**
   - 访问 https://console.volcengine.com/
   - 注册账号并登录
   - 导航到"语音技术" (Speech Technology)
   - 创建应用，获取 APP ID 和 Access Key

2. **设置环境变量**
   
   **Windows PowerShell:**
   ```powershell
   $env:VOLCANO_APP_ID="your_app_id"
   $env:VOLCANO_ACCESS_KEY="your_access_key"
   ```
   
   **Linux/Mac:**
   ```bash
   export VOLCANO_APP_ID="your_app_id"
   export VOLCANO_ACCESS_KEY="your_access_key"
   ```
   
   **永久设置（添加到配置文件）:**
   
   Windows (PowerShell):
   ```powershell
   [System.Environment]::SetEnvironmentVariable('VOLCANO_APP_ID', 'your_app_id', 'User')
   [System.Environment]::SetEnvironmentVariable('VOLCANO_ACCESS_KEY', 'your_access_key', 'User')
   ```
   
   Linux/Mac:
   ```bash
   echo 'export VOLCANO_APP_ID="your_app_id"' >> ~/.bashrc
   echo 'export VOLCANO_ACCESS_KEY="your_access_key"' >> ~/.bashrc
   source ~/.bashrc
   ```

### 本地 ASR 配置（无需 API 密钥）

```bash
# 安装依赖
pip install faster-whisper yt-dlp

# 可选：预下载模型
python scripts/podcast_transcript_txt.py --bootstrap-models small

# 使用 medium 模型（更准确但更慢）
python scripts/podcast_transcript_txt.py \
  --input "链接" \
  --asr-model medium \
  --out-dir "./transcripts"
```

## 🔍 诊断和测试

```bash
# 检查系统状态
python scripts/podcast_transcript_txt.py --doctor
```

预期输出：
```
DOCTOR  OK      python      python 3.12.10 detected
DOCTOR  OK      yt-dlp      found at /usr/bin/yt-dlp
DOCTOR  WARN    faster-whisper missing faster-whisper
DOCTOR  WARN    volcano-asr  not configured; set VOLCANO_APP_ID and VOLCANO_ACCESS_KEY env vars
FIX     Volcano ASR recommended: export VOLCANO_APP_ID and VOLCANO_ACCESS_KEY
FIX     Fallback: python3 -m pip install -r requirements.txt
```

## 📂 输出文件

每个节目会生成：

1. **`<播客名> - <标题>.txt`** - 清理后的逐字稿
2. **`<播客名> - <标题>.meta.json`** - 完整元数据
   - 来源信息
   - 使用的解析器
   - 质量指标
   - ASR 元数据

## 🎯 支持的输入类型

| 平台 | 示例 | 解析方式 | 需要凭证 |
|-----|------|---------|---------|
| **小宇宙** | `xiaoyuzhoufm.com/episode/...` | 页面文本 → 火山ASR | 可选 |
| **YouTube** | `youtube.com/watch?v=...` | 字幕 → 本地ASR | 否 |
| **Scripod** | `scripod.com/episode/...` | 官方转录 | 否 |
| **音频URL** | `https://.../audio.m4a` | 火山ASR → 本地ASR | 可选 |
| **标题搜索** | `商业访谈录` | Scripod → YouTube → Apple | 否 |

## 💡 使用场景

### 场景 1：YouTube 视频（推荐，无需配置）

```bash
# 自动使用 YouTube 字幕
python scripts\podcast_transcript_txt.py \
  --input "https://www.youtube.com/watch?v=n1E9IZfvGMA" \
  --out-dir "./transcripts"
```

### 场景 2：小宇宙播客（需要配置）

```bash
# 配置火山引擎后自动使用
python scripts\podcast_transcript_txt.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --out-dir "./transcripts"
```

### 场景 3：批量处理

```bash
python scripts\podcast_transcript_txt.py \
  --input "链接1" \
  --input "链接2" \
  --input "标题关键词" \
  --out-dir "./transcripts"
```

### 场景 4：纯本地模式（离线使用）

```bash
# 安装本地依赖
pip install faster-whisper yt-dlp

# 处理音频文件（会自动下载 faster-whisper 模型）
python scripts\podcast_transcript_txt.py \
  --input "音频链接" \
  --asr-model small \
  --out-dir "./transcripts"
```

## 📊 性能对比

| 方法 | 准确率 | 速度 | 成本 | 需要凭证 |
|-----|--------|------|------|---------|
| **官方转录** | ⭐⭐⭐⭐⭐ | ⚡ | 免费 | ❌ |
| **平台字幕** | ⭐⭐⭐⭐ | ⚡ | 免费 | ❌ |
| **火山引擎ASR** | ⭐⭐⭐⭐ | 🔥 | 按量付费 | ✅ |
| **本地ASR** | ⭐⭐⭐ | 🐢 | 免费 | ❌ |

## 🔧 故障排除

### 问题 1：火山引擎 ASR 不可用

**症状：**
```
DOCTOR  WARN    volcano-asr  not configured
```

**解决方案：**
```bash
# 检查环境变量
echo $VOLCANO_APP_ID
echo $VOLCANO_ACCESS_KEY

# 如果为空，需要配置凭证或使用本地 ASR
```

### 问题 2：本地 ASR 依赖缺失

**症状：**
```
DOCTOR  WARN    faster-whisper missing faster-whisper
```

**解决方案：**
```bash
pip install faster-whisper
```

### 问题 3：质量不佳

**解决方案：**
1. 查看元数据中的 `resolver` 字段
2. 如果使用的是本地 ASR，尝试升级到 medium 模型
3. 对火山引擎 ASR 输出，建议使用 Claude 进行校对

## 📚 高级用法

### 指定本地 ASR 模型

```bash
python scripts\podcast_transcript_txt.py \
  --input "链接" \
  --asr-model medium \
  --out-dir "./transcripts"
```

### 禁用页面文本降级

```bash
python scripts\podcast_transcript_txt.py \
  --input "链接" \
  --page-text-fallback off \
  --out-dir "./transcripts"
```

## 🎓 质量优化建议

对于所有 ASR 生成的逐字稿，强烈建议使用 Claude 进行校对：

```
提示词模板：
"请校对这份播客逐字稿，重点修正：
1. 人名和专有名词（如：Anthropic、OpenAI、豆包等）
2. 技术术语（如：AGI、Coding、Agent等）
3. 标点符号和段落划分

保持原意不变，只做必要的修正。"
```

## 🔐 隐私和安全

- ✅ **不收集数据**：所有处理在本地完成
- ✅ **凭证保护**：API 密钥通过环境变量配置，不存储在代码中
- ✅ **开源透明**：所有代码公开可审计
- ⚠️ **云端ASR**：使用火山引擎时，音频会上传到字节跳动服务器

## 📝 与原版本的区别

| 特性 | 原版本 | 公开版本 |
|-----|--------|---------|
| 预配置凭证 | ✅ | ❌ |
| 开箱即用 | ✅ | ❌（需配置） |
| 隐私安全 | ⚠️ | ✅ |
| 可定制性 | ⚠️ | ✅ |
| 公开分享 | ❌ | ✅ |

## 🤝 贡献

这是一个公开版本，欢迎：
- 报告 bug
- 提出改进建议
- 提交 pull request
- 分享您的使用经验

## 📄 许可证

MIT License - 自由使用、修改和分发

## 👨‍💻 原作者

- **Skill作者**: [@一龙小包子](https://x.com/KingJing001)
- **火山引擎集成**: 用户贡献
- **公开版本**: 匿名贡献者

---

**推荐关注** [@一龙小包子](https://x.com/KingJing001) —— 关心 AI，更关心人类；一手观察与思考，纯手工写作。😏
