# 编程文章写手

## 📋 功能概述

**酷壳式**编程技术文章生成工具，追求"像朋友聊天一样自然"的技术写作风格。

- ✅ **去AI味**：不用"首先/其次/最后"，靠技术逻辑自然流动
- ✅ **真实踩坑**：优先搜索真实经验、踩坑分享，不是API文档罗列
- ✅ **适度吐槽**：只在设计方案有问题时吐槽，有建设性
- ✅ **结尾留思考**：用个人感想 + 问题留给读者，代替"综上所述"

**默认长度**：1500-2500字（标准版），支持 800-1200 / 1500-2500 / 2500-4000 字三档

## 🎯 什么是"酷壳式"风格？

参考酷壳（CoolShell）的文章特点：

| 传统AI写法 | 酷壳式写法 |
|-----------|-----------|
| "首先...其次...最后..." | 技术逻辑自然推进 |
| "综上所述，总而言之" | 个人感想 + 留问题给读者 |
| 泛泛而谈的"最佳实践" | 具体踩坑经验和场景 |
| 机械工整的句子 | 长短句交替，偶尔口语化 |
| 不敢表态 | 有技术态度，敢说好也说烂 |

**文章结构**：`场景引入 → 痛点吐槽 → 解决方案 → 代码示例 → 踩坑经验 → 思考问题`

## 🚀 快速开始

### 触发Skill

直接对 Opencode 说：
- "写一篇关于React Hooks的文章"
- "写一篇Python异步编程的经验分享"
- "帮我写一篇Docker踩坑记录"
- "编程文章：TypeScript用下来的感受"

### 示例对话

**User**: 写一篇关于TypeScript类型安全的文章

**Opencode**: [识别到编程文章写手]
1. 正在搜索TypeScript踩坑经验...
2. 搜索GitHub示例...
3. 分析资料并规划酷壳式结构...
4. 生成文章内容...

**Output**: ✅ TypeScript文章已生成
📁 文件路径：`./typescript_article_20260121.md`
📝 字数统计: 1850字
📊 文章长度: standard (1500-2500字)
🎨 文章风格: casual（酷壳式）

---

## 📁 输入/输出

### 输入

- **主题描述**：自然语言描述
- **配置选项**（可选）：

| 配置项 | 选项 | 默认值 | 说明 |
|--------|------|--------|------|
| 文章长度 | concise/standard/detailed | standard | concise: 800-1200, standard: 1500-2500, detailed: 2500-4000 |
| 写作风格 | casual/professional/tutorial | casual | casual: 轻松自然, professional: 专业有态度, tutorial: 教程实用 |
| 输出语言 | zh/en | zh | zh: 中文, en: 英文 |
| 额外关键词 | 逗号分隔 | 无 | 帮助搜索更精准 |

### 输出

- **Markdown文件**：标准Markdown格式
- **文件命名**：`<主题>_article_YYYYMMDD.md`
- **字数范围**：800-4000字（根据配置）
- **结构**：场景→痛点→解决→示例→经验→思考

### 输出格式示例

```markdown
---
title: "TypeScript：我用下来的真实感受"
date: 2026-01-21
tags: [TypeScript, 类型系统]
description: 聊聊TypeScript的实际使用体验、踩坑经验和实用建议
---

记得第一次接触TypeScript的时候，我是一脸懵的...

## 说TypeScript之前，先说说它让人头疼的地方

**坑一：配置复杂...**

## 怎么解决

...解决方案...

## 代码怎么写

```typescript
// 示例代码
```

## 用下来的感受

...踩坑经验...

## 最后说几句

...个人感想 + 问题留给读者...

---
*本文由编程文章写手Skill v3.0生成*
```

---

## 📊 关系图支持

### 自动关系图类型

| 图表类型 | 适用场景 | 触发关键词 |
|---------|---------|-----------|
| **概念图** | 核心概念和关系 | 概念、原理、核心 |
| **流程图** | 处理步骤和工作流程 | 流程、步骤、过程 |
| **架构图** | 系统架构和组件 | 架构、系统、部署、Docker、Kubernetes |
| **类图** | 类和对象结构 | 类、对象、OOP |
| **状态图** | 状态转换和生命周期 | 状态、生命周期 |

### 使用示例

```bash
# 架构类主题（自动添加架构图）
写一篇关于Docker容器化部署的文章

# 流程类主题（自动添加流程图）
写一篇关于数据处理流程的文章

# 概念类主题（自动添加概念图）
写一篇关于TypeScript类型系统的文章
```

---

## 🔧 命令行使用

```bash
# 基础用法（默认 standard 长度，casual 风格）
python scripts/search_and_write.py "TypeScript类型安全"

# 精简版（800-1200字）
python scripts/search_and_write.py "React Hooks" --length concise

# 详细版（2500-4000字）
python scripts/search_and_write.py "Docker容器化" --length detailed

# 专业风格
python scripts/search_and_write.py "TypeScript类型系统" --style professional

# 英文文章
python scripts/search_and_write.py "Kubernetes best practices" --language en

# 带关键词
python scripts/search_and_write.py "React性能优化" --keywords "useMemo,useCallback"

# 指定输出目录
python scripts/search_and_write.py "Python异步编程" --output-dir ./articles
```

---

## 💡 使用技巧

1. **具体化需求**：越具体越好
   - ❌ "写一篇Python的文章"
   - ✅ "写一篇Python异步编程的文章，重点讲asyncio的坑"

2. **指定文章长度**
   - "简短介绍" → concise (800-1200字)
   - "正常讲讲" → standard (1500-2500字，默认)
   - "详细全面" → detailed (2500-4000字)

3. **酷壳式表达**
   - 可以说"我用下来觉得XXX很坑"
   - 可以说"这个设计我不太理解"
   - 可以留问题给读者思考

4. **组合使用**
   ```bash
   python scripts/search_and_write.py "TypeScript类型系统" \
     --length detailed --style professional --language zh
   ```

---

## 🐛 故障排除

### 问题1：生成的文章太短/太长
**解决**：明确指定长度配置

### 问题2：技术内容不够准确
**解决**：Skill优先搜索真实经验，如果不准可以要求补充关键词

### 问题3：风格不像酷壳
**解决**：确保使用casual风格，并在主题描述中说明要"真实感受"、"踩坑经验"

### 问题4：文件保存失败
**解决**：确认目录存在且有写权限

### 问题5：搜索结果不理想
**解决**：添加更具体的关键词，或换角度描述主题

---

## 📝 更新日志

- **v3.0.0 (2026-01-21)**: 重大升级
  - ✨ **全新酷壳式风格**：去AI味、自然不做作
  - ✨ **新文章结构**：场景→痛点→解决→示例→经验→思考
  - ✨ **新长度划分**：concise(800-1200)/standard(1500-2500)/detailed(2500-4000)
  - ✨ **真实踩坑经验**：优先搜索个人博客、踩坑分享
  - ✨ **适度吐槽机制**：设计方案有问题时吐槽
  - ✨ **结尾留思考**：代替"综上所述"
  - ✨ 去除"首先/其次/最后"机械过渡
- v2.1.0: 新增智能关系图
- v2.0.0: 新增长度配置、风格配置、多语言支持
- v1.0.0: 初始版本

---

## 📚 相关文档

- [SKILL.md](SKILL.md) - 技能详细说明
- [scripts/search_and_write.py](scripts/search_and_write.py) - 文章生成脚本（v3.0）
- [templates/article_template.md](templates/article_template.md) - 文章模板
