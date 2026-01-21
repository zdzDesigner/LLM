# 编程文章写手 v2.0 快速开始指南

## 🚀 5分钟快速上手

### 第1步：基本使用

在 Opencode 中直接说：

```
写一篇关于TypeScript类型安全的文章
```

**结果**：自动生成一篇 medium 长度、casual 风格的中文文章

---

### 第2步：指定文章长度

根据需求选择合适的长度：

```bash
# 短篇介绍（500-800字）
写一篇关于React Hooks的简短介绍

# 中篇标准（800-1200字）
写一篇关于Python异步编程的文章

# 长篇详细（1200-2000字）
写一篇关于Docker容器化部署的详细文章
```

---

### 第3步：选择写作风格

根据读者群体选择风格：

```bash
# 轻松风格 - 适合技术博客
写一篇关于Vue 3新特性的文章，语言轻松一些

# 专业风格 - 适合技术文档
写一篇专业的TypeScript类型系统文章

# 教程风格 - 适合学习指南
写一篇教程：如何使用React Hooks
```

---

### 第4步：多语言支持

支持中文和英文：

```bash
# 中文（默认）
写一篇关于Kubernetes的文章

# 英文
Write an article about Kubernetes best practices
```

---

### 第5步：高级配置

组合使用多个配置：

```bash
# 长篇 + 专业风格 + 英文
Write a detailed professional article about microservices architecture in English

# 长篇 + 教程风格 + 关键词
写一篇关于Python异步编程的详细教程，重点关注asyncio和async/await
```

---

## 📖 使用场景示例

### 场景1：技术博客写作
**需求**：写一篇吸引人的技术博客

```bash
写一篇关于React性能优化的文章，语言轻松幽默，适合中级开发者阅读
```

**预期**：
- 长度：medium (800-1200字)
- 风格：casual
- 语言：zh
- 特点：生动有趣，有代码示例

---

### 场景2：团队培训材料
**需求**：编写团队内部培训文档

```bash
写一篇专业的TypeScript类型系统文章，适合团队内部培训
```

**预期**：
- 长度：long (1200-2000字)
- 风格：professional
- 语言：zh
- 特点：严谨专业，逻辑清晰

---

### 场景3：学习笔记整理
**需求**：整理学习Docker的笔记

```bash
写一篇教程：如何使用Docker容器化部署，一步步掌握核心技巧
```

**预期**：
- 长度：medium (800-1200字)
- 风格：tutorial
- 语言：zh
- 特点：循序渐进，实用性强

---

### 场景4：英文技术文档
**需求**：编写英文技术文档

```bash
Write a detailed tutorial about Kubernetes orchestration in English
```

**预期**：
- 长度：long (1200-2000字)
- 风格：tutorial
- 语言：en
- 特点：英文专业术语，国际标准

---

### 场景5：快速参考指南
**需求**：快速了解某个技术

```bash
写一篇关于Go并发编程的简短介绍
```

**预期**：
- 长度：short (500-800字)
- 风格：casual
- 语言：zh
- 特点：简洁明了，快速上手

---

## 🎯 配置速查表

| 需求 | 推荐配置 | 触发词示例 |
|-----|---------|-----------|
| 快速了解 | short + casual | "简短介绍" |
| 标准博客 | medium + casual | "写一篇关于..." |
| 详细教程 | long + tutorial | "详细教程" |
| 专业文档 | long + professional | "专业的...文章" |
| 英文文档 | 任意 + en | "Write an article..." |
| 带关键词 | 任意 + 关键词 | "重点关注..." |

---

## 💡 使用技巧

### 1. 主题描述要具体
```bash
# ❌ 不好
写一篇Python文章

# ✅ 好
写一篇关于Python异步编程的文章，重点介绍asyncio的用法
```

### 2. 明确目标读者
```bash
# 适合初级开发者
写一篇适合初学者的React入门文章

# 适合有经验的开发者
写一篇深入的TypeScript高级类型文章
```

### 3. 强调重点内容
```bash
# 多举代码示例
写一篇关于React Hooks的文章，多举些代码示例

# 重点讲原理
写一篇关于算法的文章，重点讲原理，少举例
```

### 4. 组合多个要求
```bash
写一篇专业的TypeScript类型系统文章，要求详细深入，适合团队培训
```

### 5. 使用关键词优化搜索
```bash
写一篇关于性能优化的文章，重点关注useMemo、useCallback、memo
```

---

## 🔧 命令行使用

如果你需要更多控制，可以直接使用命令行：

```bash
# 基础用法
python scripts/search_and_write.py "TypeScript类型安全"

# 指定长度
python scripts/search_and_write.py "React性能优化" --length long

# 指定风格
python scripts/search_and_write.py "Docker容器化" --style professional

# 指定语言
python scripts/search_and_write.py "Kubernetes basics" --language en

# 组合使用
python scripts/search_and_write.py "Microservices" \
  --length long \
  --style professional \
  --language en

# 指定输出目录
python scripts/search_and_write.py "Python异步编程" --output-dir ./articles

# 添加关键词
python scripts/search_and_write.py "React Hooks" \
  --keywords "useMemo,useCallback,性能优化"
```

---

## 📁 输出文件

### 文件命名
```
<主题>_article_YYYYMMDD.md
```

示例：
- `typescript_type_safety_article_20260120.md`
- `react_hooks_article_20260120.md`

### 文件结构
```markdown
---
title: "文章标题"
date: 2026-01-20
tags: [TypeScript, 类型安全]
description: 文章描述
---

# 文章标题

## 写在前面
...

## 一、问题背景
...

## 二、解决方案
...

## 三、代码示例
...

## 四、效果验证
...

## 五、总结
...

---
*本文由编程文章写手Skill v2.0自动生成*
```

---

## 🐛 常见问题

### Q1：文章字数不符合预期
**A**：在主题描述中明确指定长度
```bash
写一篇关于...的详细文章  # long
写一篇关于...的简短介绍  # short
```

### Q2：文章风格不符合预期
**A**：明确指定风格
```bash
写一篇专业的...文章      # professional
写一篇轻松的...文章      # casual
写一篇教程：如何...      # tutorial
```

### Q3：想要英文文章
**A**：使用英文描述主题
```bash
Write an article about...
```

### Q4：搜索结果不理想
**A**：添加相关关键词
```bash
写一篇关于React性能优化的文章，重点关注useMemo和useCallback
```

### Q5：文件保存在哪里
**A**：默认保存在当前目录，可以指定输出目录
```bash
python scripts/search_and_write.py "主题" --output-dir ./my_articles
```

---

## 📚 进阶使用

### 1. 批量生成文章
```bash
# 创建批量脚本
cat > generate_articles.sh << 'EOF'
#!/bin/bash
python scripts/search_and_write.py "TypeScript类型安全"
python scripts/search_and_write.py "React性能优化"
python scripts/search_and_write.py "Docker容器化"
EOF

chmod +x generate_articles.sh
./generate_articles.sh
```

### 2. 定制输出目录
```bash
# 按日期组织
python scripts/search_and_write.py "主题" --output-dir ./articles/2026-01-20

# 按技术栈组织
python scripts/search_and_write.py "React主题" --output-dir ./articles/frontend
python scripts/search_and_write.py "Go主题" --output-dir ./articles/backend
```

### 3. 结合其他工具
```bash
# 生成后自动打开
python scripts/search_and_write.py "主题" && code .

# 生成后预览
python scripts/search_and_write.py "主题" && cat *.md | head -50
```

---

## 🎓 学习路径

### 初级（1-2周）
1. 使用默认配置生成文章
2. 尝试不同的主题
3. 熟悉输出格式

### 中级（2-4周）
1. 尝试不同长度配置
2. 体验不同写作风格
3. 使用关键词优化搜索

### 高级（1-2月）
1. 组合使用多个配置
2. 批量生成文章
3. 整合到工作流程

---

## 📝 检查清单

使用前确认：
- [ ] 主题描述清晰具体
- [ ] 选择了合适的长度
- [ ] 选择了合适的风格
- [ ] 选择了合适的语言
- [ ] 添加了相关关键词（可选）
- [ ] 指定了输出目录（可选）

---

## 🎉 开始使用

现在你已经掌握了所有使用技巧！

**立即尝试**：
```
写一篇关于你最感兴趣的技术的文章
```

**需要帮助**：
- 查看 [README.md](README.md) - 完整使用说明
- 查看 [SKILL.md](SKILL.md) - 技能详细说明
- 查看 [UPGRADE_v2.0.md](UPGRADE_v2.0.md) - 升级详情

---

**祝你写作愉快！** 🚀

**v2.0.0** - 2026-01-20
