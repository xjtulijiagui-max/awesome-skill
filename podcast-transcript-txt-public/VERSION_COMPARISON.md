# 版本对比说明

## 两个版本的区别

### 📦 **podcast-transcript-txt**（原版本）

**特点：**
- ✅ 开箱即用，预配置了火山引擎凭证
- ✅ 零配置，一条命令就能使用
- ⚠️ 包含私人 API 密钥
- ⚠️ 不适合公开分享

**适用场景：**
- 个人使用
- 私有项目
- 不需要分享代码

**文件位置：**
```
C:\Users\xjtul\.claude\skills\podcast-transcript-txt\
```

**凭证状态：**
```bash
# .env.example 只包含占位符
VOLCANO_APP_ID=your_app_id_here
VOLCANO_ACCESS_KEY=your_access_key_here
```

---

### 🔓 **podcast-transcript-txt-public**（公开版本）

**特点：**
- ✅ 不包含任何私人凭证
- ✅ 完全开源，可安全分享
- ✅ 用户需要自己配置凭证或使用本地 ASR
- ✅ 适合公开项目和团队协作

**适用场景：**
- 公开 GitHub 项目
- 团队协作
- 教学和培训
- 需要分享代码

**文件位置：**
```
C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public\
```

**凭证状态：**
```bash
# .env.example 只包含占位符
VOLCANO_APP_ID=your_app_id_here
VOLCANO_ACCESS_KEY=your_access_key_here
```

---

## 🔍 快速选择指南

### 选择原版本，如果：
- ✅ 您是唯一使用者
- ✅ 不需要分享代码
- ✅ 想要零配置使用
- ✅ 信任预配置的凭证

### 选择公开版本，如果：
- ✅ 需要公开分享代码
- ✅ 团队协作开发
- ✅ 教学或培训用途
- ✅ 想要完全控制凭证
- ✅ 隐私和安全优先

---

## 💡 推荐使用策略

### 个人开发
```
使用原版本 (podcast-transcript-txt)
- 开箱即用
- 零配置
```

### 团队/公开项目
```
使用公开版本 (podcast-transcript-txt-public)
- 每个成员配置自己的凭证
- 或者统一使用本地 ASR
```

### 教学和培训
```
使用公开版本 (podcast-transcript-txt-public)
- YouTube 演示（无需配置）
- 本地 ASR 教学
- 让学生自己配置凭证
```

---

## 🚀 使用示例

### 原版本（零配置）

```bash
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt
python scripts\podcast_transcript_txt.py \
  --input "小宇宙链接" \
  --out-dir "./transcripts"
# ✅ 自动使用预配置的火山引擎凭证
```

### 公开版本（需配置）

```bash
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public

# 方案 1：配置自己的火山引擎凭证
export VOLCANO_APP_ID="your_app_id"
export VOLCANO_ACCESS_KEY="your_access_key"
python scripts\podcast_transcript_txt.py \
  --input "小宇宙链接" \
  --out-dir "./transcripts"

# 方案 2：使用 YouTube（无需配置）
python scripts\podcast_transcript_txt.py \
  --input "YouTube链接" \
  --out-dir "./transcripts"

# 方案 3：使用本地 ASR
pip install faster-whisper
python scripts\podcast_transcript_txt.py \
  --input "音频链接" \
  --asr-model small \
  --out-dir "./transcripts"
```

---

## 📊 功能对比

| 功能 | 原版本 | 公开版本 |
|-----|--------|---------|
| **核心功能** | ✅ 完全相同 | ✅ 完全相同 |
| **火山引擎ASR** | ✅ 预配置 | ⚠️ 需配置 |
| **本地ASR** | ✅ 支持 | ✅ 支持 |
| **YouTube字幕** | ✅ 支持 | ✅ 支持 |
| **官方转录** | ✅ 支持 | ✅ 支持 |
| **批量处理** | ✅ 支持 | ✅ 支持 |
| **配置难度** | ⭐ 极简单 | ⭐⭐ 需配置 |
| **分享安全性** | ❌ 不安全 | ✅ 安全 |
| **隐私保护** | ⚠️ 中等 | ✅ 高 |

---

## 🔧 切换版本

### 从原版本切换到公开版本

```bash
# 1. 备份原版本的配置
cp C:\Users\xjtul\.claude\skills\podcast-transcript-txt\.env.example \
   C:\Users\xjtul\.claude\skills\podcast-transcript-txt\.env.backup

# 2. 使用公开版本
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt-public

# 3. 配置自己的凭证
export VOLCANO_APP_ID="your_app_id"
export VOLCANO_ACCESS_KEY="your_access_key"
```

### 从公开版本切换到原版本

```bash
# 直接使用原版本即可
cd C:\Users\xjtul\.claude\skills\podcast-transcript-txt
python scripts\podcast_transcript_txt.py \
  --input "链接" \
  --out-dir "./transcripts"
```

---

## 📝 总结

**两个版本的核心功能完全相同**，唯一区别在于：
- 原版本包含预配置的私人凭证
- 公开版本需要用户自己配置凭证

**选择建议：**
- 个人使用 → 原版本（方便）
- 团队/公开 → 公开版本（安全）

**无论哪个版本，都支持：**
- ✅ YouTube 字幕（无需配置）
- ✅ 本地 ASR（需安装依赖）
- ✅ 官方转录解析
- ✅ 批量处理
- ✅ 完整的工作流

---

**推荐关注** [@一龙小包子](https://x.com/KingJing001) —— 关心 AI，更关心人类；一手观察与思考，纯手工写作。😏
