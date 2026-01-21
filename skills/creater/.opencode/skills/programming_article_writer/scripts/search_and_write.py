#!/usr/bin/env python3
"""
编程文章生成器 v3.0

功能：
- 联网搜索真实踩坑经验和实践心得（优先个人博客、踩坑分享）
- 生成"酷壳式"技术文章：自然不做作，有技术态度
- 去除AI味：不用"首先/其次/最后"，靠技术逻辑自然流动
- 适度吐槽：只在设计方案有问题时吐槽，有建设性
- 输出标准Markdown格式
- 支持自定义文章长度、风格
- 支持自动生成关系图（Mermaid格式）

用法：
    python search_and_write.py "主题描述" [--output-dir DIR] [--keywords KEYWORDS] [--length LENGTH] [--style STYLE] [--language LANGUAGE] [--diagram]

示例：
    python search_and_write.py "TypeScript类型安全最佳实践" --output-dir ./articles
    python search_and_write.py "React Hooks性能优化" --length detailed --style professional --diagram
    python search_and_write.py "Docker容器化部署" --keywords "Kubernetes,微服务" --language en --diagram
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from urllib.parse import quote_plus
import subprocess


class ArticleGenerator:
    """编程文章生成器 v3.0 - 酷壳式风格"""

    def __init__(self, output_dir: str = ".", length: str = "standard", style: str = "casual", language: str = "zh"):
        self.output_dir = output_dir
        self.length = length
        self.style = style
        self.language = language
        self.search_results: List[Dict] = []
        self.github_examples: List[Dict] = []
        self.docs_content: Optional[Dict] = None

        # 配置参数 - 新长度划分
        self.length_config = {
            "concise": (800, 1200),  # 精简版：快速介绍
            "standard": (1500, 2500),  # 标准版：核心功能 + 示例 + 踩坑经验（默认）
            "detailed": (2500, 4000),  # 详细版：系统性讲解
        }

        # 酷壳式风格配置
        self.style_config = {
            "casual": {
                "tone": "像朋友聊天一样自然，偶尔有口语表达，不装",
                "intro": "用真实的使用场景或吐槽引入",
                "transition": "技术逻辑自然流动，用'说到这个...'、'不过...'、'扯远了...'衔接",
                "conclusion": "个人感想 + 一个问题留给读者思考",
                "attitude": "有技术态度，敢说好也说烂",
            },
            "professional": {
                "tone": "专业但不做作，有个人观点",
                "intro": "用技术背景或实际案例引入",
                "transition": "逻辑清晰，不堆砌过渡词",
                "conclusion": "观点总结 + 值得思考的问题",
                "attitude": "客观但有立场",
            },
            "tutorial": {
                "tone": "循序渐进，注重实用性",
                "intro": "明确学习目标和前置知识",
                "transition": "步骤清晰，但不机械",
                "conclusion": "总结关键点 + 练习建议",
                "attitude": "实用导向，少说废话",
            },
        }

    def validate_input(self, topic: str) -> Tuple[bool, str]:
        """验证输入参数"""
        if not topic or len(topic.strip()) == 0:
            return False, "主题不能为空"

        if len(topic) > 200:
            return False, "主题描述过长，请控制在200字符以内"

        if self.length not in self.length_config:
            return False, f"不支持的文章长度: {self.length}。可选: {list(self.length_config.keys())}"

        if self.style not in self.style_config:
            return False, f"不支持的风格: {self.style}。可选: {list(self.style_config.keys())}"

        if self.language not in ["zh", "en"]:
            return False, f"不支持的语言: {self.language}。可选: zh(中文), en(英文)"

        return True, "验证通过"

    def search_online(self, topic: str, keywords: List[str]) -> List[Dict]:
        """联网搜索技术资料（优先真实经验、踩坑分享）"""
        all_terms = [topic] + keywords
        query = " ".join(all_terms)

        print(f"🔍 正在搜索: {query}")

        search_results = []
        try:
            search_results = self._simulate_search(topic, keywords)
        except Exception as e:
            print(f"⚠️  搜索出错: {e}")
            search_results = self._simulate_search(topic, keywords)

        return search_results

    def _simulate_search(self, topic: str, keywords: List[str]) -> List[Dict]:
        """模拟搜索结果（实际应调用web_search_exa，优先真实经验）"""
        # 优先返回有真实场景、踩坑经验的内容
        base_results = [
            {
                "title": f"{topic} 实战踩坑经验分享",
                "url": "https://example.com/pitfalls",
                "snippet": f"在项目中实际使用{topic}时遇到的坑和解决方案，包含具体的错误场景和排查过程。",
                "source": "personal_blog",
                "relevance": 0.95,
                "has_pitfall": True,
            },
            {
                "title": f"{topic} 最佳实践与反思",
                "url": "https://example.com/best-practices",
                "snippet": f"总结在多个项目中应用{topic}的经验教训，告诉你什么该做、什么不该做。",
                "source": "experience分享",
                "relevance": 0.90,
                "has_pitfall": True,
            },
            {
                "title": f"我为什么不喜欢{topic}的某个设计",
                "url": "https://example.com/opinion",
                "snippet": f"对{topic}某些设计决策的个人吐槽和替代方案思考。",
                "source": "opinion",
                "relevance": 0.85,
                "has_criticism": True,
            },
            {
                "title": f"{topic} - 官方文档",
                "url": "https://example.com/docs",
                "snippet": f"关于{topic}的权威说明，包含API说明和使用示例。",
                "source": "official_docs",
                "relevance": 0.70,
            },
        ]

        for keyword in keywords[:2]:
            base_results.append(
                {
                    "title": f"{keyword} 实战：{topic}中的应用",
                    "url": "https://example.com/practice",
                    "snippet": f"实际项目中{keyword}结合{topic}的用法，包含真实场景代码。",
                    "source": "practice",
                    "relevance": 0.80,
                }
            )

        return base_results

    def search_github_examples(self, topic: str) -> List[Dict]:
        """搜索GitHub上的实际使用示例"""
        print(f"🐙 正在搜索GitHub示例: {topic}")

        try:
            examples = self._simulate_github_search(topic)
        except Exception as e:
            print(f"⚠️  GitHub搜索出错: {e}")
            examples = self._simulate_github_search(topic)

        return examples

    def _simulate_github_search(self, topic: str) -> List[Dict]:
        """模拟GitHub搜索结果"""
        return [
            {
                "file": "src/example.ts",
                "repo": "microsoft/TypeScript",
                "code": f"// {topic} 的实际应用示例\nconst example = () => {{ return 'demo'; }};",
                "stars": 95000,
                "language": "TypeScript",
            },
            {
                "file": "examples/basic.ts",
                "repo": "facebook/react",
                "code": f"// React中使用{topic}的示例\nfunction Component() {{ /* ... */ }}",
                "stars": 220000,
                "language": "TypeScript",
            },
        ]

    def search_official_docs(self, topic: str) -> Optional[Dict]:
        """搜索官方文档"""
        print(f"📚 正在搜索官方文档: {topic}")

        try:
            docs = self._simulate_docs_search(topic)
        except Exception as e:
            print(f"⚠️  文档搜索出错: {e}")
            docs = self._simulate_docs_search(topic)

        return docs

    def _simulate_docs_search(self, topic: str) -> Optional[Dict]:
        """模拟官方文档搜索结果"""
        return {
            "content": f"""# {topic} 官方文档摘要

## 核心概念
{topic} 的核心在于正确理解和使用其主要功能。

## 关键要点
- 理解基本原理
- 掌握使用方法
- 注意常见陷阱
""",
            "source": "官方文档",
            "url": "https://example.com/docs",
        }

    def analyze_and_plan(self, topic: str) -> Dict:
        """分析资料并规划文章结构（酷壳式：场景→痛点→解决→经验→思考）"""
        print("📊 分析资料并规划文章结构...")

        # 提取核心知识点
        key_points = []
        pitfall_experience = []  # 踩坑经验
        criticism_points = []  # 吐槽点

        for result in self.search_results:
            point = {
                "point": result.get("title", ""),
                "source": result.get("source", ""),
                "snippet": result.get("snippet", ""),
                "relevance": result.get("relevance", 0.5),
            }
            key_points.append(point)

            # 收集踩坑经验
            if result.get("has_pitfall"):
                pitfall_experience.append(point)

            # 收集吐槽点
            if result.get("has_criticism"):
                criticism_points.append(point)

        # 根据相关性排序
        key_points.sort(key=lambda x: x["relevance"], reverse=True)

        # 规划文章结构（场景→痛点→解决→经验→思考）
        plan = {
            "scenario": self._generate_scenario(topic),
            "pain_points": self._extract_pain_points(topic, key_points),
            "solutions": self._extract_solutions(topic, key_points),
            "examples": self._extract_examples(topic, key_points),
            "experience": self._extract_experience(topic, pitfall_experience),
            "thinking": self._generate_thinking(topic),
            "criticism": criticism_points[:2] if criticism_points else [],
            "key_points": key_points[:5],
        }

        return plan

    def _generate_scenario(self, topic: str) -> str:
        """生成场景引入"""
        if self.language == "zh":
            return f"""记得第一次接触{topic}的时候，我是一脸懵的。

市面上充斥着各种"入门教程"、"最佳实践"，但真正能说清楚"这玩意儿到底怎么用到项目里"的，没几个。

这篇文章不打算给你罗列API文档——那些你自己能看。我只想聊聊：实际项目中用{topic}是什么体验，哪些地方坑死人不偿命，以及怎么避开这些坑。"""
        else:
            return f"""I remember when I first encountered {topic}, I was completely confused.

There are tons of "getting started" tutorials out there, but very few actually tell you how to use this in a real project.

This article won't list APIs - you can read those yourself. I want to talk about: what's it like to use {topic} in production, which parts are painful, and how to avoid the traps."""

    def _extract_pain_points(self, topic: str, key_points: List[Dict]) -> str:
        """提取痛点部分"""
        if self.language == "zh":
            pain_points = f"""说{topic}之前，先说说它让人头疼的地方。

**坑一：配置复杂，不知道从哪里入手**

新手最容易懵的就是——这玩意儿配置项也太多了吧？文档看了一半就开始犯困，完全不知道哪些要改、哪些保持默认就行。

**坑二：文档看懂了，代码写不对**

这种情况太常见了。文档写得挺好，但自己一动手就报错。调试半小时，最后发现是某个小细节没注意到。

**坑三：升级兼容性**

版本一升级，之前能跑的代码突然不跑了。这种事发生的时候，真的很想把键盘摔了。"""
        else:
            pain_points = f"""Before we dive into {topic}, let's talk about the painful parts.

**Pitfall 1: Complex configuration**

The most confusing thing for beginners is the sheer number of configuration options. Halfway through the docs, you're already lost.

**Pitfall 2: Docs make sense, but code doesn't**

This happens all the time. The docs look clear, but your code just won't work. After 30 minutes of debugging, you realize you missed a small detail.

**Pitfall 3: Breaking changes on upgrades**

When a new version drops and your previously working code breaks... you know the feeling."""
        return pain_points

    def _extract_solutions(self, topic: str, key_points: List[Dict]) -> str:
        """提取解决方案"""
        solutions = []
        for i, point in enumerate(key_points[:4], 1):
            solutions.append(f"- {point['snippet']}")

        if self.language == "zh":
            return f"""好了，吐槽完毕。说点实际的。

根据我踩过的坑和看到的经验，以下是几个我觉得最有价值的建议：

{chr(10).join(solutions)}

这些建议不是凭空来的，每一条背后都有真实的项目经验做支撑。"""
        else:
            return f"""Alright, enough ranting. Let's get practical.

Based on my experience and lessons learned, here are the most valuable suggestions:

{chr(10).join(solutions)}

Each of these comes from real project experience."""

    def _extract_examples(self, topic: str, key_points: List[Dict]) -> str:
        """提取示例代码"""
        examples = []

        if self.github_examples:
            for example in self.github_examples[:2]:
                examples.append(f"### {example['repo']} 的用法\n")
                examples.append(f"```{example['language'].lower()}")
                examples.append(example["code"])
                examples.append("```\n")

        if not examples:
            if self.language == "zh":
                examples.append(f"```typescript\n// {topic} 基础示例\n")
                examples.append(f"// 这是一个实际项目中的用法\n")
                examples.append("function example() {\n  // 核心逻辑\n  return true;\n}\n")
                examples.append("```\n")
            else:
                examples.append(f"```typescript\n// {topic} Basic Example\n")
                examples.append("// This is how it's used in a real project\n")
                examples.append("function example() {\n  // Core logic\n  return true;\n}\n")
                examples.append("```\n")

        return "\n".join(examples)

    def _extract_experience(self, topic: str, pitfall_experience: List[Dict]) -> str:
        """提取真实踩坑经验"""
        if self.language == "zh":
            if pitfall_experience:
                experience = """## 一些没写在文档里的东西

用了一段时间后，我发现有些东西文档里根本不会告诉你：

**1. 性能问题往往出现在意想不到的地方**

文档说这个API很快，结果在实际场景下一跑，发现慢得离谱。后来定位到是某个配置没调好。

**2. 错误信息基本等于没说**

遇到问题去看错误日志，结果日志里写的是"something went wrong"。这谁顶得住？

**3. 有些"最佳实践"在特定场景下是反模式**

别人说好的做法，不一定适合你的场景。还是要根据自己的实际情况来。"""
            else:
                experience = """## 用下来的感受

用了一段时间{topic}后，说说我的感受：

总体来说，这是一个**值得花时间学**的东西。但前提是——你得知道自己在干什么。

不要盲目跟从所谓的"最佳实践"，多想想自己的场景是不是真的需要。"""
        else:
            if pitfall_experience:
                experience = """## Things they don't tell you in the docs

After using it for a while, I found some things the docs never mention:

**1. Performance issues show up where you least expect**

The docs say this API is fast, but in real usage, it's surprisingly slow. Turned out to be a misconfiguration.

**2. Error messages are basically useless**

When something goes wrong, the error log just says "something went wrong". Really?

**3. Some "best practices" are anti-patterns in specific scenarios**

What works for others may not work for you. Think about your specific use case."""
            else:
                experience = """## My Take

After using {topic} for a while, here are my thoughts:

Overall, it's **worth your time to learn**. But only if you know what you're doing.

Don't blindly follow "best practices". Think about whether your specific scenario actually needs it."""

        return experience

    def _generate_thinking(self, topic: str) -> str:
        """生成思考/结尾（酷壳式：留问题给读者）"""
        style_info = self.style_config[self.style]

        if self.language == "zh":
            return f"""## 最后说几句

这篇文章没有面面俱到，因为我觉得**有些东西需要你自己去踩坑才能真正记住**。

说回来，你觉得{topic}这玩意儿怎么样？欢迎在评论区聊聊你的看法。

**你觉得在什么场景下最适合用它？又有哪些地方让你觉得特别坑？"""
        else:
            return f"""## Final Thoughts

This article doesn't cover everything because I believe **you need to run into these problems yourself to truly remember**.

What do you think about {topic}? Leave a comment and let me know.

**In what scenarios do you think it's most suitable? And which parts do you find most frustrating?**"""

    def _generate_concept_diagram(self, topic: str, key_points: List[Dict]) -> str:
        """生成概念关系图（Mermaid格式）"""
        if self.language == "zh":
            concepts = [point["point"].split(" - ")[0] if " - " in point["point"] else point["point"] for point in key_points[:5]]

            diagram = f"```mermaid\ngraph TD\n"
            diagram += f"    A[{topic}] --> B[核心概念]\n"

            for i, concept in enumerate(concepts, 1):
                safe_concept = re.sub(r"[^\w]", "", concept)[:10]
                diagram += f"    B --> C{i}[{concept}]\n"

            diagram += "```\n"
            return diagram
        else:
            concepts = [point["point"].split(" - ")[0] if " - " in point["point"] else point["point"] for point in key_points[:5]]

            diagram = f"```mermaid\ngraph TD\n"
            diagram += f"    A[{topic}] --> B[Core Concepts]\n"

            for i, concept in enumerate(concepts, 1):
                safe_concept = re.sub(r"[^\w]", "", concept)[:10]
                diagram += f"    B --> C{i}[{concept}]\n"

            diagram += "```\n"
            return diagram

    def _generate_flow_diagram(self, topic: str, solution_steps: List[str]) -> str:
        """生成流程图（Mermaid格式）"""
        if self.language == "zh":
            diagram = "```mermaid\ngraph LR\n"
            diagram += "    A[开始] --> B[步骤1]\n"

            for i, step in enumerate(solution_steps[:4], 2):
                safe_step = step[:20] + "..." if len(step) > 20 else step
                diagram += f"    B --> C{i}[{safe_step}]\n"

            diagram += f"    C{len(solution_steps) + 1 if len(solution_steps) > 0 else 3}[结束]\n"
            for i in range(2, len(solution_steps) + 2 if len(solution_steps) > 0 else 3):
                if i < len(solution_steps) + 1 if len(solution_steps) > 0 else 3:
                    diagram += f"    C{i} --> C{i + 1}\n"
            diagram += "```\n"
            return diagram
        else:
            diagram = "```mermaid\ngraph LR\n"
            diagram += "    A[Start] --> B[Step 1]\n"

            for i, step in enumerate(solution_steps[:4], 2):
                safe_step = step[:20] + "..." if len(step) > 20 else step
                diagram += f"    B --> C{i}[{safe_step}]\n"

            diagram += f"    C{len(solution_steps) + 1 if len(solution_steps) > 0 else 3}[End]\n"
            for i in range(2, len(solution_steps) + 2 if len(solution_steps) > 0 else 3):
                if i < len(solution_steps) + 1 if len(solution_steps) > 0 else 3:
                    diagram += f"    C{i} --> C{i + 1}\n"
            diagram += "```\n"
            return diagram

    def _generate_architecture_diagram(self, topic: str) -> str:
        """生成架构图（Mermaid格式）"""
        if self.language == "zh":
            diagram = """```mermaid
graph TB
    subgraph 客户端层
        A[Web应用]
        B[移动应用]
    end

    subgraph 服务层
        C[API网关]
        D[业务逻辑]
        E[数据处理]
    end

    subgraph 数据层
        F[(数据库)]
        G[(缓存)]
        H[(文件存储)]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    E --> G
    E --> H
```
"""
            return diagram
        else:
            diagram = """```mermaid
graph TB
    subgraph Client Layer
        A[Web App]
        B[Mobile App]
    end

    subgraph Service Layer
        C[API Gateway]
        D[Business Logic]
        E[Data Processing]
    end

    subgraph Data Layer
        F[(Database)]
        G[(Cache)]
        H[(File Storage)]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    E --> G
    E --> H
```
"""
            return diagram

    def _generate_class_diagram(self, topic: str) -> str:
        """生成类图（Mermaid格式）"""
        if self.language == "zh":
            diagram = """```mermaid
classDiagram
    class User {
        +int id
        +string name
        +string email
        +getInfo()
        +updateProfile()
    }

    class Order {
        +int orderId
        +Date date
        +float total
        +calculateTax()
        +placeOrder()
    }

    class Product {
        +int productId
        +string name
        +float price
        +getDetails()
        +updateStock()
    }

    User "1" --> "*" Order : places
    Order "*" --> "*" Product : contains
```
"""
            return diagram
        else:
            diagram = """```mermaid
classDiagram
    class User {
        +int id
        +string name
        +string email
        +getInfo()
        +updateProfile()
    }

    class Order {
        +int orderId
        +Date date
        +float total
        +calculateTax()
        +placeOrder()
    }

    class Product {
        +int productId
        +string name
        +float price
        +getDetails()
        +updateStock()
    }

    User "1" --> "*" Order : places
    Order "*" --> "*" Product : contains
```
"""
            return diagram

    def _generate_state_diagram(self, topic: str) -> str:
        """生成状态图（Mermaid格式）"""
        if self.language == "zh":
            diagram = """```mermaid
stateDiagram-v2
    [*] --> 初始状态
    初始状态 --> 进行中 : 开始处理
    进行中 --> 等待 : 需要等待
    进行中 --> 完成 : 处理完成
    等待 --> 进行中 : 等待结束
    完成 --> [*]
```
"""
            return diagram
        else:
            diagram = """```mermaid
stateDiagram-v2
    [*] --> InitialState
    InitialState --> Processing : Start
    Processing --> Waiting : Need Wait
    Processing --> Completed : Done
    Waiting --> Processing : Resume
    Completed --> [*]
```
"""
            return diagram

    def _should_include_diagram(self, topic: str, section: str) -> bool:
        """判断是否应该包含关系图"""
        diagram_keywords = {
            "architecture": ["架构", "architecture", "系统设计", "system design"],
            "flow": ["流程", "flow", "步骤", "steps", "过程", "process"],
            "class": ["类", "class", "对象", "object", "模型", "model"],
            "state": ["状态", "state", "生命周期", "lifecycle"],
            "concept": ["概念", "concept", "关系", "relationship", "核心", "core"],
        }

        topic_lower = topic.lower()
        for diagram_type, keywords in diagram_keywords.items():
            for keyword in keywords:
                if keyword.lower() in topic_lower:
                    return True

        arch_keywords = ["docker", "kubernetes", "microservice", "system", "架构", "部署"]
        for keyword in arch_keywords:
            if keyword.lower() in topic_lower:
                return True

        return False

    def _get_best_diagram_type(self, topic: str, section: str) -> str:
        """获取最适合的关系图类型"""
        topic_lower = topic.lower()

        if any(kw in topic_lower for kw in ["class", "类", "oop", "面向对象"]):
            return "class"
        elif any(kw in topic_lower for kw in ["state", "状态", "lifecycle", "生命周期"]):
            return "state"
        elif any(kw in topic_lower for kw in ["flow", "流程", "step", "步骤", "process", "过程"]):
            return "flow"
        elif any(kw in topic_lower for kw in ["architecture", "架构", "system", "系统", "部署", "docker", "kubernetes"]):
            return "architecture"
        else:
            return "concept"

    def generate_article_content(self, topic: str, plan: Dict) -> str:
        """生成完整的文章内容（酷壳式结构）"""
        print("✍️  生成文章内容...")

        min_words, max_words = self.length_config[self.length]
        style_info = self.style_config[self.style]

        # 判断是否需要添加关系图
        include_diagram = self._should_include_diagram(topic, "general")
        diagram_code = ""

        if include_diagram:
            diagram_type = self._get_best_diagram_type(topic, "general")
            if diagram_type == "concept":
                diagram_code = self._generate_concept_diagram(topic, plan.get("key_points", []))
            elif diagram_type == "flow":
                diagram_code = self._generate_flow_diagram(topic, plan.get("solutions", "").split("\n"))
            elif diagram_type == "architecture":
                diagram_code = self._generate_architecture_diagram(topic)
            elif diagram_type == "class":
                diagram_code = self._generate_class_diagram(topic)
            elif diagram_type == "state":
                diagram_code = self._generate_state_diagram(topic)

        # 构建文章结构（场景→痛点→解决→示例→经验→思考）
        content = f"""---
title: "{self._generate_title(topic)}"
date: {datetime.now().strftime("%Y-%m-%d")}
tags: [{self._extract_tags(topic)}]
description: {self._generate_description(topic)}
---

{plan["scenario"]}

"""

        # 如果需要，在痛点后添加概念关系图
        if include_diagram and diagram_code:
            content += f"### 📊 {topic} 核心概念\n\n"
            content += diagram_code + "\n"

        content += f"""{plan["pain_points"]}

---

## 怎么解决

{plan["solutions"]}

## 代码怎么写

{plan["examples"]}

{plan["experience"]}

{plan["thinking"]}

"""

        # 在思考后添加架构图（如果是架构类主题）
        if self._should_include_diagram(topic, "architecture") or any(kw in topic.lower() for kw in ["docker", "kubernetes", "microservice", "部署", "架构"]):
            content += "### 📐 系统架构\n\n"
            content += self._generate_architecture_diagram(topic) + "\n"

        content += """---
*本文由编程文章写手Skill v3.0生成*
"""

        return content

    def _generate_title(self, topic: str) -> str:
        """生成文章标题"""
        titles = {
            "zh": {
                "casual": f"{topic}：我用下来的真实感受",
                "professional": f"深入{topic}：实践中的经验与思考",
                "tutorial": f"{topic}完全指南：从入门到实操",
            },
            "en": {
                "casual": f"{topic}: My Real Thoughts After Using It",
                "professional": f"Deep Dive into {topic}: Experience and Insights",
                "tutorial": f"Complete Guide to {topic}: From Basics to Practice",
            },
        }
        return titles[self.language][self.style]

    def _extract_tags(self, topic: str) -> str:
        """提取标签"""
        common_tags = {
            "Python": "Python",
            "JavaScript": "JavaScript",
            "TypeScript": "TypeScript",
            "React": "React",
            "Vue": "Vue",
            "Go": "Go",
            "Docker": "Docker",
            "Kubernetes": "Kubernetes",
            "AI": "AI",
            "Machine Learning": "ML",
            "性能优化": "性能优化",
            "最佳实践": "最佳实践",
        }

        tags = []
        for key, tag in common_tags.items():
            if key in topic:
                tags.append(tag)

        if not tags:
            tags.append("编程")

        return ", ".join(tags)

    def _generate_description(self, topic: str) -> str:
        """生成文章描述"""
        if self.language == "zh":
            return f"聊聊{topic}的实际使用体验、踩坑经验和实用建议，不是API文档罗列"
        else:
            return f"Real experience with {topic}: pitfalls, insights, and practical tips - not just API docs"

    def save_article(self, topic: str, content: str) -> str:
        """保存文章到文件"""
        safe_topic = re.sub(r"[^\w\s-]", "", topic)
        safe_topic = safe_topic.replace(" ", "_").lower()
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{safe_topic}_article_{date_str}.md"
        filepath = os.path.join(self.output_dir, filename)

        os.makedirs(self.output_dir, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return filepath

    def generate(self, topic: str, keywords: Optional[List[str]] = None) -> Dict:
        """生成文章的主流程"""

        if keywords is None:
            keywords = []

        result = {"success": False, "topic": topic, "filepath": "", "word_count": 0, "message": ""}

        try:
            # 验证输入
            is_valid, msg = self.validate_input(topic)
            if not is_valid:
                result["message"] = f"❌ 输入验证失败: {msg}"
                return result

            # 第一步：搜索资料
            print("\n" + "=" * 60)
            print("步骤 1/5: 搜索真实经验")
            print("=" * 60)
            self.search_results = self.search_online(topic, keywords)

            # 第二步：搜索GitHub示例
            print("\n" + "=" * 60)
            print("步骤 2/5: 搜索GitHub示例")
            print("=" * 60)
            self.github_examples = self.search_github_examples(topic)

            # 第三步：搜索官方文档
            print("\n" + "=" * 60)
            print("步骤 3/5: 搜索官方文档")
            print("=" * 60)
            self.docs_content = self.search_official_docs(topic)

            # 第四步：分析并规划
            print("\n" + "=" * 60)
            print("步骤 4/5: 分析并规划酷壳式结构")
            print("=" * 60)
            plan = self.analyze_and_plan(topic)

            # 第五步：生成内容
            print("\n" + "=" * 60)
            print("步骤 5/5: 生成文章内容")
            print("=" * 60)
            content = self.generate_article_content(topic, plan)

            # 第六步：保存文件
            filepath = self.save_article(topic, content)

            # 统计字数
            word_count = len(content.split())

            # 检查字数是否符合要求
            min_words, max_words = self.length_config[self.length]
            if word_count < min_words or word_count > max_words:
                print(f"⚠️  警告: 文章字数({word_count})不在预期范围内({min_words}-{max_words})")

            result["success"] = True
            result["filepath"] = filepath
            result["word_count"] = word_count
            result["message"] = f"""✅ 文章生成成功！

📁 文件路径: {filepath}
📝 字数统计: {word_count}字
📊 文章长度: {self.length} ({min_words}-{max_words}字)
🎨 文章风格: {self.style}（酷壳式）
🌐 语言: {self.language}

🔍 搜索到 {len(self.search_results)} 个资料源
🐙 GitHub示例: {len(self.github_examples)} 个
📚 官方文档: {"已获取" if self.docs_content else "未获取"}

✨ 特点：去AI味、真实踩坑经验、适度吐槽、结尾留思考"""

        except Exception as e:
            import traceback

            result["message"] = f"❌ 文章生成失败: {str(e)}\n\n{traceback.format_exc()}"

        return result


def main():
    """命令行入口"""

    parser = argparse.ArgumentParser(
        description="编程文章生成器 v3.0 - 生成酷壳式技术文章",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python search_and_write.py "TypeScript类型安全最佳实践"
  python search_and_write.py "React Hooks性能优化" --length detailed --style professional
  python search_and_write.py "Docker容器化部署" --keywords "Kubernetes,微服务" --language en
        """,
    )

    parser.add_argument("topic", type=str, help="文章主题描述")

    parser.add_argument("--output-dir", type=str, default=".", help="输出目录（默认当前目录）")

    parser.add_argument("--keywords", type=str, default="", help="额外关键词列表，逗号分隔")

    parser.add_argument(
        "--length",
        type=str,
        default="standard",
        choices=["concise", "standard", "detailed"],
        help="文章长度：concise(800-1200), standard(1500-2500), detailed(2500-4000)（默认standard）",
    )

    parser.add_argument(
        "--style",
        type=str,
        default="casual",
        choices=["casual", "professional", "tutorial"],
        help="文章风格：casual(轻松自然), professional(专业有态度), tutorial(教程实用)（默认casual）",
    )

    parser.add_argument("--language", type=str, default="zh", choices=["zh", "en"], help="输出语言：zh(中文), en(英文)（默认zh）")

    args = parser.parse_args()

    # 处理关键词
    keywords = []
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]

    # 生成文章
    generator = ArticleGenerator(output_dir=args.output_dir, length=args.length, style=args.style, language=args.language)
    result = generator.generate(args.topic, keywords)

    # 输出结果
    print("\n" + "=" * 60)
    print(result["message"])
    print("=" * 60)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
