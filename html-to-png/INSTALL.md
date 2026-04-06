# HTML to PNG Skill - 完整创建总结

## Skill 已成功创建！

根据 Skill Creator 标准流程，以下是完整的 Skill 文件结构：

## 📁 文件结构

```
html-to-png/
├── SKILL.md                  # 核心 Skill 指令（必需）
├── README.md                 # Skill 说明文档
├── INSTALL.md                # 本文件
├── evals/
│   └── evals.json            # 测试用例
└── scripts/
    └── image-to-base64.js    # 辅助脚本：图片转 base64
```

## 🎯 Skill 描述

**Name**: html-to-png

**Description**: Automatically add "Save as PNG" screenshot functionality to HTML files. Use this skill whenever the user mentions: adding screenshot functionality to HTML, converting HTML to images, saving web pages as pictures, creating downloadable screenshots from HTML, adding export-to-image buttons, generating PNG from HTML content, or when they need to capture long scrolling HTML pages as complete images.

## 📋 核心功能

1. **一键截图功能** - 在 HTML 文件中添加悬浮按钮，点击即可保存为高清 PNG
2. **全页面捕获** - 支持超长页面完整截图，无高度限制
3. **高分辨率输出** - 2x 缩放，确保在所有设备上清晰显示
4. **智能配置** - 自动处理背景色、字体加载、按钮隐藏等

## 🔧 技术实现

- **核心库**: html2canvas v1.4.1（CDN 引入）
- **输出格式**: PNG（2x 分辨率）
- **固定宽度**: 1200px（确保截图一致性）
- **按钮样式**: 固定定位右下角，截图时自动隐藏

## ⚠️ 重要限制

**图片必须是 base64 格式！**

由于浏览器 CORS 限制，html2canvas 无法捕获外部链接的图片（https://...）。
所有 `<img>` 标签的 `src` 属性必须是 data:image/...;base64,... 格式。

## 📦 安装方法

### 方法 1：手动复制（推荐）

1. 将整个 `html-to-png/` 文件夹复制到：
   ```
   C:\Users\xjtul\.claude\skills\
   ```

2. 重启 Claude Code

3. Skill 将自动可用

### 方法 2：创建 .skill 包

如果需要创建 .skill 安装包，需要安装 Node.js 依赖：

```bash
npm install archiver
node create-skill-package.js C:\Users\xjtul\.claude\skills\html-to-png
```

这将生成 `html-to-png.skill` 文件，可直接拖拽安装。

## 🧪 测试用例

Skill 包含 3 个测试用例：

1. **现有 HTML 文件** - 测试添加截图功能到已有 HTML
2. **从零创建** - 测试从头创建带截图功能的 HTML
3. **外部图片处理** - 测试 CORS 警告和错误处理

运行测试（需要 Python 环境）：
```bash
cd C:\Users\xjtul\.claude\skills\skill-creator
python -m scripts.run_tests ../html-to-png
```

## 💡 使用示例

### 示例 1：添加到现有文件
```
你：帮我在这个 HTML 文件中添加截图功能：./course-brochure.html

Claude：[使用 html-to-png skill 修改文件]
```

### 示例 2：创建新文件
```
你：创建一个可以导出为图片的课程大纲页面

Claude：[使用 html-to-png skill 创建完整 HTML]
```

### 示例 3：处理外部图片
```
你：这个 HTML 有外部图片，能加截图功能吗？

Claude：[使用 html-to-png skill，并警告 CORS 限制]
```

## 🔍 核心代码片段

### html2canvas 引入（必须）
```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
```

### 固定宽度 CSS
```css
body {
    width: 1200px;
    margin: 0 auto;
    overflow-x: hidden;
}
```

### 截图按钮
```html
<div id="screenshot-btn" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
    <button onclick="captureScreenshot()">📸 保存为图片</button>
</div>
```

### 捕获函数（简化版）
```javascript
async function captureScreenshot() {
    const btn = document.getElementById('screenshot-btn');
    btn.style.display = 'none';

    const canvas = await html2canvas(document.body, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: window.getComputedStyle(document.body).backgroundColor
    });

    canvas.toBlob(blob => {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'screenshot.png';
        a.click();
        btn.style.display = '';
    }, 'image/png');
}
```

## 🛠️ 辅助工具

### 图片转 base64 脚本
```bash
node scripts/image-to-base64.js ./photo.png
```

输出可直接用于 HTML 的 data URL。

## 📚 参考资源

- **原始文档**: C:\Users\xjtul\Downloads\html-to-png-SKILL.md
- **示例文件**: C:\Users\xjtul\Desktop\2026\3月项目\openclaw素材\招生简章_完整截图版_新版_base64.html
- **html2canvas 官方文档**: https://html2canvas.hertzen.com/

## ✅ 验证清单

安装后，请验证：
- [ ] Skill 出现在 Claude Code 的技能列表中
- [ ] 触发词能正确激活 Skill
- [ ] 测试用例能通过
- [ ] 生成的 HTML 能在浏览器中正常显示
- [ ] 点击按钮能成功下载 PNG
- [ ] 截图包含所有内容（无截断）
- [ ] 图片渲染正确（无空白）

## 🎓 Skill Creator 流程遵循

本 Skill 严格按照 Skill Creator 标准流程创建：

1. ✅ **Capture Intent** - 明确用户意图
2. ✅ **Interview and Research** - 研究边缘情况
3. ✅ **Write SKILL.md** - 编写核心指令
4. ✅ **Create Test Cases** - 创建测试用例
5. ✅ **Bundled Resources** - 包含辅助脚本
6. ⏭️ **Package and Present** - 打包并呈现（本步骤）

## 📞 支持

如有问题，请检查：
1. Python 环境是否正确配置
2. Node.js 是否可用
3. 文件路径是否正确
4. SKILL.md 格式是否正确（YAML frontmatter）

---

**创建日期**: 2026-04-06
**版本**: 1.0.0
**状态**: ✅ 完成
