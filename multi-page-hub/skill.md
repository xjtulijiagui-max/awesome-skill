---
type: skill
name: multi-page-hub
description: 创建多页面导航入口，整合多个独立 HTML 文件为统一的导航中心
---

# 多页面导航入口生成器

## 功能描述

根据现有 HTML 文件自动创建导航入口页面，将多个独立的 HTML 文件整合为一个统一的导航中心。

## 适用场景

- 用户要求"整合多个HTML"、"创建导航入口"、"统一入口"
- 需要将多个相关页面整合为一个导航系统
- 创建课程中心、文档中心、工具箱等导航页面

## 执行步骤

### 1. 分析需求并收集页面信息

首先询问用户或从上下文中获取：
- 需要整合的 HTML 文件列表
- 导航入口的标题/名称
- 菜单项的名称和对应的目标文件

如果用户提供了目录，使用 Glob 工具查找该目录下的所有 HTML 文件。

### 2. 读取已有页面，提取设计风格

读取 1-2 个已有的 HTML 文件，提取：
- 主色调（主要颜色变量）
- 字体样式
- 背景风格（渐变、纯色等）

### 3. 创建导航入口页面

创建 `index.html` 文件，包含：

#### HTML 结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[导航入口标题]</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        /* CSS 样式 */
    </style>
</head>
<body>
    <div class="container">
        <!-- 左侧导航 -->
        <nav class="sidebar">
            <div class="logo">
                <i class="[logo图标]"></i>
                <span>[标题]</span>
            </div>
            <ul class="nav-menu" id="navMenu">
                <!-- 菜单项将由 JS 生成 -->
            </ul>
        </nav>

        <!-- 右侧内容区 -->
        <main class="main-content">
            <iframe id="contentFrame" src="[第一个页面]"></iframe>
        </main>
    </div>

    <script>
        // JavaScript 逻辑
    </script>
</body>
</html>
```

#### CSS 样式（参考模板）
```css
:root {
    --primary-color: [提取的主色调];
    --sidebar-width: 260px;
    --header-height: 60px;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
    background: #f5f7fa;
    overflow: hidden;
}

.container {
    display: flex;
    height: 100vh;
}

/* 左侧导航栏 */
.sidebar {
    width: var(--sidebar-width);
    background: linear-gradient(180deg, var(--primary-color), [深色变体]);
    color: white;
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.logo {
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 18px;
    font-weight: 600;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo i {
    font-size: 24px;
}

.nav-menu {
    list-style: none;
    padding: 10px 0;
    flex: 1;
    overflow-y: auto;
}

.nav-item {
    padding: 12px 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.3s ease;
    border-left: 3px solid transparent;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
    background: rgba(255, 255, 255, 0.15);
    border-left-color: white;
    font-weight: 600;
}

.nav-item .number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    font-size: 12px;
    font-weight: 600;
}

/* 右侧内容区 */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
}

#contentFrame {
    width: 100%;
    height: 100vh;
    border: none;
    background: white;
}
```

#### JavaScript 逻辑
```javascript
// 菜单配置
const menuItems = [
    { number: '01', icon: 'fas fa-home', name: '[菜单名称1]', url: '[页面1.html]' },
    { number: '02', icon: 'fas fa-file-alt', name: '[菜单名称2]', url: '[页面2.html]' },
    // ... 更多菜单项
];

const navMenu = document.getElementById('navMenu');
const contentFrame = document.getElementById('contentFrame');

// 生成菜单
menuItems.forEach((item, index) => {
    const li = document.createElement('li');
    li.className = 'nav-item' + (index === 0 ? ' active' : '');
    li.innerHTML = `
        <span class="number">${item.number}</span>
        <i class="${item.icon}"></i>
        <span>${item.name}</span>
    `;
    li.addEventListener('click', () => loadPage(item.url, li));
    navMenu.appendChild(li);
});

// 加载页面
function loadPage(url, element) {
    contentFrame.src = url;
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    element.classList.add('active');
}
```

### 4. 输出结果

完成后向用户展示：

```
✅ 多页面导航入口已创建完成！

📁 文件位置：[目录]/index.html

📋 菜单项与跳转目标对照表：
┌──────┬─────────────────────┬──────────────────────┐
│ 编号 │ 菜单名称            │ 目标文件             │
├──────┼─────────────────────┼──────────────────────┤
│ 01   │ [菜单名称1]         │ [页面1.html]         │
│ 02   │ [菜单名称2]         │ [页面2.html]         │
└──────┴─────────────────────┴──────────────────────┘

🚀 使用方法：
直接用浏览器打开 index.html 即可使用。
```

## 图标参考

常用图标（Font Awesome）：
- `fas fa-home` - 首页
- `fas fa-file-alt` - 文档
- `fas fa-book` - 教程/课程
- `fas fa-tools` - 工具
- `fas fa-chart-bar` - 图表/数据
- `fas fa-cog` - 设置
- `fas fa-user` - 用户
- `fas fa-graduation-cap` - 教育/培训
- `fas fa-lightbulb` - 创意/场景
- `fas fa-rocket` - 战略/启动

## 注意事项

1. 确保所有 HTML 文件在同一目录下或使用相对路径正确引用
2. 如果页面之间有跨域限制，iframe 可能无法加载
3. 菜单项数量建议不超过 15 个，超过则考虑分组
4. 保持视觉风格与已有页面一致
