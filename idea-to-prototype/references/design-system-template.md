# 设计系统文档模板

> 本文件是 Step 1 的详细模板参考，AI 在生成设计系统时应参照此结构。

---

# 设计系统：[项目名称]

## 1. 设计令牌（Design Tokens）

### 1.1. 颜色（Colors）

```yaml
# 主色阶（Primary）
--color-primary-50:  [基于用户提供的 --primary-100 智能扩展]
--color-primary-100: [用户提供]
--color-primary-200: [用户提供]
--color-primary-300: [用户提供]
--color-primary-400: [...]
--color-primary-500: [...]
--color-primary-600: [...]
--color-primary-700: [...]
--color-primary-800: [...]
--color-primary-900: [...]

# 中性色阶（Neutral/Gray）
--color-gray-50:  #F7F7F7
--color-gray-100: #E5E5E5
--color-gray-200: #CCCCCC
--color-gray-300: #999999
--color-gray-400: #666666
--color-gray-500: #333333
--color-gray-600: #1A1A1A
--color-gray-700: #000000

# 语义色（Semantic）
--color-success: #22C55E
--color-error:   #EF4444
--color-warning: #F59E0B
--color-info:    #3B82F6

# 文本色（Text）
--color-text-primary:   [用户提供 --text-100]
--color-text-secondary: [用户提供 --text-200]
--color-text-disabled:  --color-gray-400

# 背景色（Background）
--color-bg-primary:   [用户提供 --bg-100]
--color-bg-secondary: [用户提供 --bg-200]
--color-bg-tertiary:  [用户提供 --bg-300]
```

### 1.2. 字体（Typography）

```yaml
# 字体族
--font-family-base: 'Inter', 'Noto Sans SC', -apple-system, sans-serif
--font-family-heading: 'Poppins', 'Noto Sans SC', sans-serif

# 字号系统
--font-size-xs:   12px
--font-size-sm:   14px
--font-size-base: 16px
--font-size-lg:   18px
--font-size-xl:   20px
--font-size-2xl:  24px
--font-size-3xl:  30px
--font-size-4xl:  36px

# 字重
--font-weight-regular:  400
--font-weight-medium:   500
--font-weight-semibold: 600
--font-weight-bold:    700

# 行高
--line-height-tight:   1.25
--line-height-normal:  1.5
--line-height-relaxed: 1.75

# 文本样式
--text-heading-1: { fontSize: 36px, fontWeight: 700, lineHeight: 1.25 }
--text-heading-2: { fontSize: 30px, fontWeight: 700, lineHeight: 1.25 }
--text-heading-3: { fontSize: 24px, fontWeight: 600, lineHeight: 1.3 }
--text-heading-4: { fontSize: 20px, fontWeight: 600, lineHeight: 1.4 }
--text-body-lg:   { fontSize: 18px, fontWeight: 400, lineHeight: 1.6 }
--text-body:      { fontSize: 16px, fontWeight: 400, lineHeight: 1.5 }
--text-body-sm:   { fontSize: 14px, fontWeight: 400, lineHeight: 1.5 }
--text-caption:   { fontSize: 12px, fontWeight: 400, lineHeight: 1.4 }
```

### 1.3. 间距（Spacing）

```yaml
--space-1:  4px
--space-2:  8px
--space-3:  12px
--space-4:  16px
--space-5:  20px
--space-6:  24px
--space-8:  32px
--space-10: 40px
--space-12: 48px
--space-16: 64px
--space-20: 80px

# 常用组合
--spacing-section: 48px
--spacing-card-inner: 16px
--spacing-screen-x: 20px
```

### 1.4. 效果（Effects）

```yaml
# 圆角
--radius-sm:   4px
--radius-md:   8px
--radius-lg:   12px
--radius-xl:   16px
--radius-2xl:  24px
--radius-full: 9999px

# 阴影
--shadow-sm:  0 1px 2px rgba(0,0,0,0.06)
--shadow-md:  0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05)
--shadow-lg:  0 10px 15px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.05)
--shadow-xl:  0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04)

# 模糊
--blur-sm: 4px
--blur-md: 8px
--blur-lg: 16px

# 过渡
--transition-fast:   150ms ease
--transition-normal: 250ms ease
--transition-slow:   400ms ease
```

---

## 2. 组件库（Component Library）

### 2.1. Button 按钮

```yaml
props:
  - type: primary | secondary | ghost | danger
  - size: sm (h-32px) | md (h-40px) | lg (h-48px)
  - state: default | hover | active | disabled | loading
  - icon: boolean（左侧图标）
  - fullWidth: boolean

样式规则:
  - 圆角: borderRadius = --radius-full（药丸形）或 --radius-lg
  - 过渡: transition = --transition-fast
  - Hover: opacity 0.9, transform: scale(0.98)
  - Active: transform: scale(0.96)
  - Loading: 显示 Spinner，文字不变，禁用交互
```

### 2.2. Input 输入框

```yaml
props:
  - type: text | password | email | number
  - size: sm | md | lg
  - state: default | focus | error | disabled
  - label: string
  - placeholder: string
  - errorMessage: string
  - prefixIcon / suffixIcon: boolean

样式规则:
  - 边框: 1px solid --color-gray-200
  - Focus: 边框色变为主色，添加 box-shadow
  - Error: 边框变 --color-error
  - 圆角: --radius-md
```

### 2.3. Card 卡片

```yaml
props:
  - padding: sm (12px) | md (16px) | lg (24px)
  - shadow: none | sm | md | lg
  - radius: sm | md | lg | xl
  - clickable: boolean

样式规则:
  - Background: --color-bg-primary 或 --color-bg-secondary
  - Hover (clickable): shadow升级 + transform: translateY(-2px)
  - 圆角: --radius-lg
```

### 2.4. TabBar 底部标签栏

```yaml
props:
  - items: [{ icon, activeIcon, label, path }]
  - activeIndex: number

样式规则:
  - 高度: 56px + safe-area-bottom
  - 背景: --color-bg-primary + 顶部 1px 分割线
  - 激活态: 主色图标 + 主色文字
  - 默认态: --color-gray-400 图标 + --color-gray-500 文字
  - 过渡: 颜色切换 --transition-fast
```

### 2.5. Avatar 头像

```yaml
props:
  - src: string
  - size: xs(24px) | sm(32px) | md(40px) | lg(56px) | xl(80px)
  - shape: circle | square
  - badge: boolean

样式规则:
  - 圆角: --radius-full（圆形）或 --radius-md（方形）
  - 默认占位: 渐变背景 + 姓名首字母
```

### 2.6. Badge / Tag 徽标/标签

```yaml
props:
  - type: filled | outlined
  - color: primary | success | warning | error | gray
  - size: sm | md

样式规则:
  - 圆角: --radius-full
  - 字号: --font-size-xs 或 --font-size-sm
  - 内边距: 2px 8px
```

### 2.7. Modal 模态框

```yaml
props:
  - visible: boolean
  - title: string
  - content: string | slot
  - primaryAction / secondaryAction: Button props

样式规则:
  - 遮罩: rgba(0,0,0,0.5) + blur(4px)
  - 弹窗: --color-bg-primary, --radius-xl, shadow-xl
  - 入场动画: scale(0.95) → scale(1), opacity 0→1
```

### 2.8. NavBar 导航栏

```yaml
props:
  - title: string
  - leftIcon: arrow-back | close | menu
  - rightIcon: string[]
  - transparent: boolean

样式规则:
  - 高度: 44px + safe-area-top
  - 标题: 居中，--font-weight-semibold
  - 返回按钮: 左侧，图标 + 可选文字
```

---

## 3. 页面蓝图示例

> 以下为登录页的组件树示例，实际项目应根据需求调整。

```
Page: 登录页
├── NavBar (transparent, title="")
├── IllustrationSection (欢迎插图区)
│   ├── SVGAbstractShape
│   └── WelcomeTitle ("欢迎使用")
├── FormSection
│   ├── Input (手机号)
│   ├── Input (验证码)
│   └── Button (获取验证码 / 登录)
├── Divider ("其他登录方式")
├── SocialLoginRow [微信, Apple, 短信]
└── TermsRow ("登录即代表同意《用户协议》和《隐私政策》")
```
