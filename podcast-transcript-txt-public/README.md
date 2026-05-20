# Podcast Transcript TXT (Public Version)

🎯 **完全自动化播客转录工具** - 公开版本，需要您自己配置 ASR 凭证

## 🔓 为什么需要这个版本？

**隐私安全优先**
- ✅ 不包含任何预配置的 API 密钥或凭证
- ✅ 所有敏感信息通过环境变量配置
- ✅ 完全开源，代码透明可审计
- ✅ 适合公开分享和团队协作

**与原版本的区别**
| 特性 | 原版本 | 公开版本 |
|-----|--------|---------|
| 预配置凭证 | ✅ 包含私人 API 密钥 | ❌ 无任何凭证 |
| 开箱即用 | ✅ 零配置使用 | ⚠️ 需要配置凭证或本地 ASR |
| 隐私安全 | ⚠️ 包含敏感信息 | ✅ 完全安全 |
| 公开分享 | ❌ 不适合分享 | ✅ 可以安全分享 |

## 🚀 三种使用方式

### 方式 1：YouTube 视频（推荐，无需任何配置）

```bash
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public

# YouTube 会自动使用字幕，不需要任何配置
python scripts\podcast_transcript_txt.py \
  --input "https://www.youtube.com/watch?v=n1E9IZfvGMA" \
  --out-dir "./transcripts"
```

### 方式 2：火山引擎 ASR（需要配置，但质量最好）

```bash
# 步骤 1：获取火山引擎凭证
# 访问 https://console.volcengine.com/
# 注册 → 语音技术 → 创建应用 → 获取 APP ID 和 Access Key

# 步骤 2：设置环境变量
# Windows PowerShell
$env:VOLCANO_APP_ID="your_app_id"
$env:VOLCANO_ACCESS_KEY="your_access_key"

# Linux/Mac
export VOLCANO_APP_ID="your_app_id"
export VOLCANO_ACCESS_KEY="your_access_key"

# 步骤 3：运行转录
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public
python scripts\podcast_transcript_txt.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --out-dir "./transcripts"
```

### 方式 3：本地 ASR（无需 API 密钥，完全离线）

```bash
# 步骤 1：安装依赖
pip install faster-whisper yt-dlp

# 步骤 2：运行转录
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public
python scripts\podcast_transcript_txt.py \
  --input "音频链接" \
  --asr-model small \
  --out-dir "./transcripts"

# 可选：使用 medium 模型（更准确）
python scripts\podcast_transcript_txt.py \
  --input "音频链接" \
  --asr-model medium \
  --out-dir "./transcripts"
```

## 📋 快速开始

### 1. 检查系统状态

```bash
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public
python scripts\podcast_transcript_txt.py --doctor
```

**预期输出（未配置时）：**
```
DOCTOR  OK      python      python 3.12.10 detected
DOCTOR  OK      yt-dlp      found at /usr/bin/yt-dlp
DOCTOR  WARN    faster-whisper missing faster-whisper
DOCTOR  WARN    volcano-asr  not configured
FIX     Volcano ASR (optional): export VOLCANO_APP_ID and VOLCANO_ACCESS_KEY
FIX     Local ASR: python3 -m pip install -r requirements.txt
```

**预期输出（配置后）：**
```
DOCTOR  OK      python      python 3.12.10 detected
DOCTOR  OK      yt-dlp      found at /usr/bin/yt-dlp
DOCTOR  OK      faster-whisper faster-whisper ok
DOCTOR  OK      volcano-asr  credentials configured
READY   python3 scripts/podcast_transcript_txt.py --input '<link>' --out-dir '<dir>'
```

### 2. 处理第一个播客

```bash
# YouTube（推荐起点 - 无需配置）
python scripts\podcast_transcript_txt.py \
  --input "https://www.youtube.com/watch?v=n1E9IZfvGMA" \
  --out-dir "./transcripts"

# 小宇宙播客（需要火山引擎或本地 ASR）
python scripts\podcast_transcript_txt.py \
  --input "https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14" \
  --out-dir "./transcripts"

# 批量处理
python scripts\podcast_transcript_txt.py \
  --input "链接1" \
  --input "链接2" \
  --input "标题关键词" \
  --out-dir "./transcripts"
```

## 🎓 配置指南

### 火山引擎 ASR 配置（详细步骤）

**为什么推荐火山引擎？**
- ✅ 中文识别准确率最高
- ✅ 云端处理，不占用本地资源
- ✅ 处理速度快（76分钟约5分钟）
- ✅ 支持多种音频格式

**详细配置步骤：**

1. **注册账号**
   ```
   访问：https://console.volcengine.com/
   点击：注册/登录
   验证：手机号或邮箱验证
   ```

2. **创建应用**
   ```
   导航：语音技术 → 语音识别
   点击：创建应用
   填写：应用名称（如：播客转录工具）
   选择：按需付费套餐（新用户有免费额度）
   ```

3. **获取凭证**
   ```
   应用管理 → 应用详情
   复制：APP ID
   复制：Access Key
   ```

4. **设置环境变量**
   
   **Windows（临时）：**
   ```powershell
   $env:VOLCANO_APP_ID="your_app_id"
   $env:VOLCANO_ACCESS_KEY="your_access_key"
   ```
   
   **Windows（永久）：**
   ```powershell
   [System.Environment]::SetEnvironmentVariable('VOLCANO_APP_ID', 'your_app_id', 'User')
   [System.Environment]::SetEnvironmentVariable('VOLCANO_ACCESS_KEY', 'your_access_key', 'User')
   # 重启终端生效
   ```
   
   **Linux/Mac（临时）：**
   ```bash
   export VOLCANO_APP_ID="your_app_id"
   export VOLCANO_ACCESS_KEY="your_access_key"
   ```
   
   **Linux/Mac（永久）：**
   ```bash
   echo 'export VOLCANO_APP_ID="your_app_id"' >> ~/.bashrc
   echo 'export VOLCANO_ACCESS_KEY="your_access_key"' >> ~/.bashrc
   source ~/.bashrc
   ```

5. **验证配置**
   ```bash
   python scripts\podcast_transcript_txt.py --doctor
   # 应该看到：DOCTOR  OK  volcano-asr
   ```

### 本地 ASR 配置（替代方案）

**为什么使用本地 ASR？**
- ✅ 完全免费，无需 API 密钥
- ✅ 完全离线，隐私保护
- ✅ 支持多种模型大小

**配置步骤：**

1. **安装依赖**
   ```bash
   pip install faster-whisper yt-dlp
   ```

2. **预下载模型（可选）**
   ```bash
   python scripts\podcast_transcript_txt.py --bootstrap-models small
   python scripts\podcast_transcript_txt.py --bootstrap-models medium
   ```

3. **使用本地 ASR**
   ```bash
   # small 模型（默认）
   python scripts\podcast_transcript_txt.py \
     --input "音频链接" \
     --out-dir "./transcripts"
   
   # medium 模型（更准确）
   python scripts\podcast_transcript_txt.py \
     --input "音频链接" \
     --asr-model medium \
     --out-dir "./transcripts"
   ```

## 📊 方案对比

| 方案 | 准确率 | 速度 | 成本 | 隐私 | 推荐场景 |
|-----|--------|------|------|------|---------|
| **YouTube 字幕** | ⭐⭐⭐⭐ | ⚡⚡⚡ | 免费 | ✅ | YouTube 视频 |
| **火山引擎 ASR** | ⭐⭐⭐⭐⭐ | ⚡⚡ | 按量付费 | ⚠️ | 中文播客 |
| **本地 ASR (small)** | ⭐⭐⭐ | ⚡ | 免费 | ✅✅ | 快速初稿 |
| **本地 ASR (medium)** | ⭐⭐⭐⭐ | 🐢 | 免费 | ✅✅ | 高质量初稿 |

## 🔧 故障排除

### 问题 1：doctor 检查失败

**症状：**
```
DOCTOR  FAIL    python      need Python 3.9+
```

**解决方案：**
```bash
# 升级 Python
# Windows：从 python.org 下载 Python 3.12+
# Mac：brew install python@3.12
# Linux：sudo apt install python3.12
```

### 问题 2：yt-dlp 不可用

**症状：**
```
DOCTOR  FAIL    yt-dlp      missing yt-dlp
```

**解决方案：**
```bash
pip install yt-dlp
```

### 问题 3：火山引擎 ASR 不可用

**症状：**
```
DOCTOR  WARN    volcano-asr  not configured
```

**解决方案：**
```bash
# 检查环境变量
echo $VOLCANO_APP_ID
echo $VOLCANO_ACCESS_KEY

# 如果为空，选择：
# 1. 配置火山引擎凭证（见上方配置指南）
# 2. 使用本地 ASR（pip install faster-whisper）
# 3. 只处理 YouTube 视频（自动使用字幕）
```

### 问题 4：转录质量不佳

**解决方案：**
1. 查看元数据中的 `resolver` 字段
2. 如果是 `local-asr`，尝试升级到 medium 模型
3. 如果是 `volcano-asr`，检查音频质量
4. 对所有 ASR 输出，建议使用 Claude 校对：

```
提示词：
"请校对这份播客逐字稿，重点修正：
1. 人名和专有名词
2. 技术术语
3. 标点符号和段落划分

保持原意不变，只做必要的修正。"
```

## 💡 使用技巧

### 1. 创建 PowerShell 别名（Windows）

```powershell
# 添加到 $PROFILE
function transcript {
    python C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public\scripts\podcast_transcript_txt.py @args
}

# 使用
transcript --input "链接" --out-dir "./transcripts"
```

### 2. 批量处理脚本

```bash
# 创建链接列表文件
cat > links.txt << EOF
https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14
https://www.youtube.com/watch?v=n1E9IZfvGMA
商业访谈录
EOF

# 批量处理
cat links.txt | while read link; do
  python scripts\podcast_transcript_txt.py \
    --input "$link" \
    --out-dir "./transcripts"
done
```

### 3. 按日期组织输出

```bash
# Linux/Mac
python scripts\podcast_transcript_txt.py \
  --input "链接" \
  --out-dir "./transcripts/$(date +%Y%m%d)"

# Windows PowerShell
$date = Get-Date -Format "yyyyMMdd"
python scripts\podcast_transcript_txt.py `
  --input "链接" `
  --out-dir ".\transcripts\$date"
```

## 📚 高级用法

### 禁用页面文本降级

```bash
python scripts\podcast_transcript_txt.py \
  --input "链接" \
  --page-text-fallback off \
  --out-dir "./transcripts"
```

### 指定本地 ASR 模型

```bash
# small 模型（默认）
python scripts\podcast_transcript_txt.py \
  --input "链接" \
  --asr-model small \
  --out-dir "./transcripts"

# medium 模型（更准确）
python scripts\podcast_transcript_txt.py \
  --input "链接" \
  --asr-model medium \
  --out-dir "./transcripts"
```

## 🎓 工作原理

```
输入链接
    ↓
自动识别平台
    ↓
┌─────────────────────────────────┐
│  优先级 A: 官方转录              │
│  - Scripod API                   │
│  - TTML 文件                     │
│  - transcription.json            │
└─────────────────────────────────┘
    ↓ 失败
┌─────────────────────────────────┐
│  优先级 B: 平台字幕              │
│  - YouTube 自动字幕              │
│  - 无需任何配置                  │
└─────────────────────────────────┘
    ↓ 失败
┌─────────────────────────────────┐
│  优先级 C: 页面文本              │
│  - 小宇宙 shownotes              │
│  - 节目描述                      │
└─────────────────────────────────┘
    ↓ 失败
┌─────────────────────────────────┐
│  优先级 D: 火山引擎 ASR          │
│  - 需要配置凭证                  │
│  - 高质量中文识别                │
│  - 云端处理                      │
└─────────────────────────────────┘
    ↓ 失败/未配置
┌─────────────────────────────────┐
│  优先级 E: 本地 ASR              │
│  - faster-whisper                │
│  - 完全离线                      │
│  - 无需 API 密钥                 │
└─────────────────────────────────┘
    ↓
输出：TXT + 元数据
```

## 📄 输出文件说明

### 文件 1：`<播客名> - <标题>.txt`
纯文本逐字稿，包含：
- 完整对话内容
- 时间戳（可选）
- 段落分隔

### 文件 2：`<播客名> - <标题>.meta.json`
元数据文件，包含：
- `input`: 输入的链接
- `resolver`: 使用的解析器
- `source`: 最终来源
- `status`: ok/warn
- `quality`: 质量指标
- `asr`: ASR 元数据（如果使用）

## 🔐 隐私说明

**数据流向：**
- ✅ 本地处理：YouTube 字幕、本地 ASR
- ⚠️ 云端处理：火山引擎 ASR（音频上传到字节跳动）

**凭证安全：**
- ✅ 通过环境变量配置
- ✅ 不存储在代码中
- ✅ 不上传到版本控制

**建议：**
- 对于敏感内容，使用本地 ASR
- 对于公开内容，可以使用火山引擎 ASR
- 定期轮换 API 密钥

## 🤝 贡献

欢迎贡献！您可以：
- 报告 bug
- 提出改进建议
- 提交 pull request
- 分享您的使用经验

## 📄 许可证

MIT License - 自由使用、修改和分发

## 👨‍💻 致谢

- **原作者**: [@一龙小包子](https://x.com/KingJing001)
- **火山引擎集成**: 社区贡献
- **公开版本**: 匿名贡献者

---

**推荐关注** [@一龙小包子](https://x.com/KingJing001) —— 关心 AI，更关心人类；一手观察与思考，纯手工写作。😏
