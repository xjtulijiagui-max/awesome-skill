---
type: skill
name: vue-element-app
description: 创建 Vue + Element UI 应用原型，包含登录页、数据表格、表单、图表等功能
---

# Vue + Element UI 应用原型生成器

## 功能描述

创建包含完整功能的企业级单页应用原型，使用 Vue 2 + Element UI + ECharts 技术栈，通过 CDN 引入，无需构建工具。

## 适用场景

- 用户要求"企业应用原型"、"管理系统"、"数据看板"
- 需要快速创建管理后台、业务系统原型
- 需要数据表格、表单提交、图表展示等功能

## 技术栈

- **Vue 2.7.14**: https://unpkg.com/vue@2.7.14/dist/vue.js
- **Element UI 2.15.13**: https://unpkg.com/element-ui@2.15.13/lib/theme-chalk/index.css
- **ECharts 5.4.0**: https://unpkg.com/echarts@5.4.0/dist/echarts.min.js
- **Font Awesome 6.0.0**: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css

## 核心功能模块

### 1. 登录页面
```javascript
// 登录状态
isLoggedIn: false,
loginForm: {
    username: '',
    password: ''
}

// 登录方法
handleLogin() {
    if (!this.loginForm.username || !this.loginForm.password) {
        this.$message.warning('请输入用户名和密码');
        return;
    }
    this.isLoggedIn = true;
    this.$message.success('登录成功');
}
```

### 2. 顶部导航栏
- Logo 和系统标题
- 用户信息显示
- 退出登录按钮

### 3. 侧边菜单导航
```javascript
menuItems: [
    { index: 'dashboard', icon: 'el-icon-s-data', title: '数据看板' },
    { index: 'table', icon: 'el-icon-s-grid', title: '数据表格' },
    { index: 'form', icon: 'el-icon-s-order', title: '表单提交' },
    { index: 'chart', icon: 'el-icon-s-marketing', title: '图表分析' },
    { index: 'settings', icon: 'el-icon-s-tools', title: '系统设置' }
]
```

### 4. 数据表格
```javascript
// 表格数据
tableData: [
    { id: 1, name: '张三', department: '技术部', status: '在职', date: '2024-01-15' },
    { id: 2, name: '李四', department: '产品部', status: '在职', date: '2024-01-20' },
    // ...
],

// 分页
pagination: {
    currentPage: 1,
    pageSize: 10,
    total: 100
}
```

### 5. 表单提交
```javascript
form: {
    name: '',
    email: '',
    department: '',
    description: ''
},

rules: {
    name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
    email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }]
}
```

### 6. ECharts 图表
```javascript
// 初始化图表
initChart() {
    const chart = echarts.init(this.$refs.chartContainer);
    const option = {
        title: { text: '数据统计' },
        tooltip: {},
        xAxis: { data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
        yAxis: {},
        series: [{
            name: '销量',
            type: 'bar',
            data: [120, 200, 150, 80, 70, 110]
        }]
    };
    chart.setOption(option);
}
```

## 模板代码结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[应用名称]</title>
    <!-- Element UI CSS -->
    <link rel="stylesheet" href="https://unpkg.com/element-ui@2.15.13/lib/theme-chalk/index.css">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* 全局样式 */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
            background-color: #f5f7fa;
            color: #303133;
        }
        .app-container { min-height: 100vh; display: flex; flex-direction: column; }
        .app-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0 20px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        .main-container {
            display: flex;
            flex: 1;
            margin-top: 60px;
        }
        .sidebar {
            width: 200px;
            background: white;
            border-right: 1px solid #e4e7ed;
            overflow-y: auto;
        }
        .content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        .page-container {
            background: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        }
        /* 登录页面 */
        .login-container {
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-card {
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            width: 100%;
            max-width: 400px;
        }
    </style>
</head>
<body>
    <div id="app">
        <!-- 登录页面 -->
        <div v-if="!isLoggedIn" class="login-container">
            <div class="login-card">
                <div style="text-align: center; margin-bottom: 30px;">
                    <i class="fas fa-cube" style="font-size: 48px; color: #667eea;"></i>
                    <h2 style="margin-top: 20px; color: #303133;">[系统名称]</h2>
                    <p style="color: #909399; margin-top: 8px;">请登录访问系统</p>
                </div>
                <el-form :model="loginForm">
                    <el-form-item>
                        <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="el-icon-lock"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" style="width: 100%;" @click="handleLogin">登录</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>

        <!-- 主应用 -->
        <div v-else class="app-container">
            <!-- 顶部导航 -->
            <header class="app-header">
                <div class="header-title" style="font-size: 20px; font-weight: 600;">
                    <i class="fas fa-cube" style="margin-right: 10px;"></i>
                    [系统名称]
                </div>
                <div class="header-nav">
                    <span>{{ currentUser }}</span>
                    <el-button type="text" style="color: white;" @click="handleLogout">
                        <i class="fas fa-sign-out-alt"></i> 退出
                    </el-button>
                </div>
            </header>

            <!-- 主体区域 -->
            <div class="main-container">
                <!-- 侧边栏 -->
                <aside class="sidebar">
                    <el-menu :default-active="activeMenu" @select="handleMenuSelect">
                        <el-menu-item v-for="item in menuItems" :key="item.index" :index="item.index">
                            <i :class="item.icon"></i>
                            <span>{{ item.title }}</span>
                        </el-menu-item>
                    </el-menu>
                </aside>

                <!-- 内容区 -->
                <main class="content">
                    <div class="page-container">
                        <!-- 数据看板 -->
                        <div v-if="activeMenu === 'dashboard'">
                            <h2>数据看板</h2>
                            <div style="margin-top: 20px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
                                <el-card v-for="stat in statistics" :key="stat.title">
                                    <div style="text-align: center;">
                                        <div style="font-size: 32px; font-weight: bold; color: #667eea;">{{ stat.value }}</div>
                                        <div style="color: #909399; margin-top: 8px;">{{ stat.title }}</div>
                                    </div>
                                </el-card>
                            </div>
                        </div>

                        <!-- 数据表格 -->
                        <div v-if="activeMenu === 'table'">
                            <h2>数据表格</h2>
                            <el-table :data="tableData" style="width: 100%; margin-top: 20px;">
                                <el-table-column prop="id" label="ID"></el-table-column>
                                <el-table-column prop="name" label="姓名"></el-table-column>
                                <el-table-column prop="department" label="部门"></el-table-column>
                                <el-table-column prop="status" label="状态"></el-table-column>
                                <el-table-column label="操作">
                                    <template slot-scope="scope">
                                        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                                        <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                            <el-pagination
                                style="margin-top: 20px; text-align: right;"
                                :current-page="pagination.currentPage"
                                :page-size="pagination.pageSize"
                                :total="pagination.total"
                                layout="prev, pager, next">
                            </el-pagination>
                        </div>

                        <!-- 更多页面... -->
                    </div>
                </main>
            </div>
        </div>
    </div>

    <!-- Vue 2 -->
    <script src="https://unpkg.com/vue@2.7.14/dist/vue.js"></script>
    <!-- Element UI JS -->
    <script src="https://unpkg.com/element-ui@2.15.13/lib/index.js"></script>
    <!-- ECharts -->
    <script src="https://unpkg.com/echarts@5.4.0/dist/echarts.min.js"></script>

    <script>
        new Vue({
            el: '#app',
            data() {
                return {
                    isLoggedIn: false,
                    currentUser: '管理员',
                    loginForm: {
                        username: '',
                        password: ''
                    },
                    activeMenu: 'dashboard',
                    menuItems: [
                        { index: 'dashboard', icon: 'el-icon-s-data', title: '数据看板' },
                        { index: 'table', icon: 'el-icon-s-grid', title: '数据表格' },
                        { index: 'form', icon: 'el-icon-s-order', title: '表单提交' },
                        { index: 'chart', icon: 'el-icon-s-marketing', title: '图表分析' }
                    ],
                    statistics: [
                        { title: '总用户数', value: '1,234' },
                        { title: '今日访问', value: '567' },
                        { title: '数据总量', value: '8,901' },
                        { title: '系统状态', value: '正常' }
                    ],
                    tableData: [
                        { id: 1, name: '张三', department: '技术部', status: '在职', date: '2024-01-15' },
                        { id: 2, name: '李四', department: '产品部', status: '在职', date: '2024-01-20' }
                    ],
                    pagination: {
                        currentPage: 1,
                        pageSize: 10,
                        total: 100
                    }
                };
            },
            methods: {
                handleLogin() {
                    if (!this.loginForm.username || !this.loginForm.password) {
                        this.$message.warning('请输入用户名和密码');
                        return;
                    }
                    this.isLoggedIn = true;
                    this.$message.success('登录成功');
                },
                handleLogout() {
                    this.isLoggedIn = false;
                    this.$message.success('已退出登录');
                },
                handleMenuSelect(index) {
                    this.activeMenu = index;
                },
                handleEdit(row) {
                    this.$message.info('编辑：' + row.name);
                },
                handleDelete(row) {
                    this.$confirm('确认删除该记录吗？', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    }).then(() => {
                        this.$message.success('删除成功');
                    });
                }
            }
        });
    </script>
</body>
</html>
```

## 输出结果

```
✅ Vue + Element UI 应用原型已创建完成！

📁 文件位置：[目录]/[文件名].html

🎨 技术栈：
- Vue 2.7.14
- Element UI 2.15.13
- ECharts 5.4.0
- Font Awesome 6.0.0

📋 功能模块：
✓ 登录页面（用户名/密码验证）
✓ 顶部导航栏（Logo + 用户信息）
✓ 侧边菜单导航（可配置）
✓ 数据看板（统计卡片）
✓ 数据表格（分页、操作）
✓ 表单提交（验证）
✓ 图表分析（ECharts）

🚀 使用方法：
1. 双击打开 HTML 文件
2. 输入任意用户名和密码登录
3. 通过左侧菜单切换不同功能模块
```

## 常用 Element UI 组件

### 按钮
- `<el-button>` - 基础按钮
- `<el-button type="primary">` - 主要按钮
- `<el-button type="success">` - 成功按钮
- `<el-button type="danger">` - 危险按钮

### 表单
- `<el-form>` - 表单容器
- `<el-form-item>` - 表单项
- `<el-input>` - 输入框
- `<el-select>` - 下拉选择
- `<el-date-picker>` - 日期选择

### 数据展示
- `<el-table>` - 表格
- `<el-pagination>` - 分页
- `<el-card>` - 卡片
- `<el-tag>` - 标签

### 反馈
- `this.$message.success('成功')` - 消息提示
- `this.$confirm('确认？', '提示')` - 确认对话框
- `this.$notify({ title: '通知' })` - 通知

## 注意事项

1. 所有资源通过 CDN 引入，需要网络连接
2. 默认用户名/密码可以是任意值（演示用途）
3. 数据存储在内存中，刷新页面会丢失
4. 可根据需求自定义配色方案和布局
