# Awesome Claude Skills Collection

这是一个精选的 Claude Code Skills 集合，每个 skill 都经过精心设计和测试。

## 📁 目录结构

```
skills/
├── font-generator/          # 字体风格自适应提示生成器
└── README.md                # 本文件
```

## 🎨 Available Skills

### Font Generator (字体生成器)

- **位置**: `font-generator/skill.md`
- **功能**: 根据用户输入的文字内容，智能分析主题、氛围、文化语境，生成专业的字体设计提示词
- **适用场景**:
  - 品牌字体设计
  - 标题字体创意
  - 海报字体设计
  - 游戏/动漫标题字体
- **支持风格**:
  - 科幻未来类（故障体、数据流、全息）
  - 复古怀旧类（蒸汽波、酸性字体）
  - 传统古风类（瘦金体、碑刻、水墨）
  - 现代简约类（几何、包豪斯）
  - 手写艺术类（刷字、涂鸦、书法）
  - 游戏动漫类（像素风、8-bit）
  - 自然有机类（枯山水、禅意）

#### 使用示例

```bash
# 生成科幻风格字体
/font-generator "数字梦境"

# 生成古风字体
/font-generator "鲁迅的散文诗"

# 生成像素风游戏字体
/font-generator "像素大战"
```

## 🚀 快速开始

### 安装 Skills

1. 克隆本仓库到你的 Claude skills 目录：
```bash
cd ~/.claude/skills
git clone https://github.com/xjtulijiagui-max/awesome-skills.git
```

2. 或者手动复制单个 skill：
```bash
cp -r font-generator ~/.claude/skills/
```

### 使用 Skills

在 Claude Code 中直接调用：

```bash
# 使用字体生成器
/font-generator "你的文字内容"
```

## 📝 Skill 开发规范

每个 skill 应包含：

- ✅ **完整的 frontmatter**（type, name, description）
- ✅ **清晰的功能描述**
- ✅ **详细的使用说明**
- ✅ **丰富的示例**
- ✅ **错误处理说明**
- ✅ **更新日志**

## 🤝 贡献指南

欢迎提交新的 skills！

1. Fork 本仓库
2. 创建新的 skill 目录
3. 编写 skill.md 文件
4. 提交 Pull Request

## 📄 许可证

MIT License

## 👨‍💻 作者

李家贵 (xjtulijiagui-max)

## 🔗 相关链接

- [Claude Code 官方文档](https://github.com/anthropics/claude-code)
- [Skill 开发指南](https://github.com/anthropics/claude-code/blob/main/docs/skills.md)

---

⭐ 如果这个项目对你有帮助，请给个 Star！
