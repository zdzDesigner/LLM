---
name: code_example_searcher
description: Deeply search for best coding practices and examples using parallel agents. Searches local codebase (explore) and external sources (librarian) simultaneously. Use when user asks for "best practice", "find examples", "how to implement", "search pattern", or "关于xxxx的最佳实践".
allowed-tools: Read, Write, Grep, Glob, Bash, ast_grep_search, delegate_task, background_output, background_cancel, websearch_web_search_exa, grep_app_searchGitHub
---

[技能说明]
    针对模糊的编码需求，通过并行调度内部探查（Explore Agent）和外部调研（Librarian Agent），结合AST与正则搜索，输出包含本地现状、行业标准和实施建议的综合报告。具备自动容错和降级机制。**特别强调代码位置的精确性**。

[核心能力]
    - **模糊需求解析**：将"怎么写更好"转化为具体的AST模式和搜索关键词。
    - **饱和式并行搜索**：强制并发执行本地代码深度挖掘与外部开源方案调研。
    - **精准定位**：在报告中必须列出代码的具体文件路径、行号或在线链接，方便用户直接跳转。
    - **智能容错**：当特定 Agent（如 librarian）不可用时，自动降级使用通用搜索工具。

[执行流程]
    第一步：需求分析与策略制定
        - 分析用户模糊需求，提取关键技术点（语言、框架、模式）。
        - 制定搜索策略：
            - **本地策略**：确定 AST Pattern 或关键函数名。
            - **外部策略**：确定 GitHub 搜索关键词和目标仓库。
        - 告知用户："正在并行搜索本地库与外部资源..."

    第二步：并发任务派发（严格遵守参数互斥规则）
        - **任务 A (External)**: 优先尝试调用 Librarian。
          - 调用 `delegate_task(subagent_type="librarian", run_in_background=true, prompt="Find best practices for [需求]. MUST include specific file paths and GitHub URLs in the output.")`
          - **重要**：不要传递 `category` 参数。
          - *降级策略*：如果 Librarian 调用失败，使用 `grep_app_searchGitHub` 和 `websearch_web_search_exa` 直接搜索。
        
        - **任务 B (Internal)**: 调用 Explore Agent。
          - 调用 `delegate_task(subagent_type="explore", run_in_background=true, prompt="Search local codebase for [需求]. MUST provide file paths and line numbers for every match.")`
          - **重要**：不要传递 `category` 参数。
        
        - **任务 C (Direct)**: 立即执行 `ast_grep_search` 或 `Grep` 进行快速摸底。

    第三步：结果回收与合成
        - 使用 `background_output` 回收任务 A 和 B 的结果。
        - 检查任务状态，如果任务失败（Status: error），立即手动执行备选工具补充信息。
        - 读取模板：`Read .opencode/skills/code_example_searcher/templates/search_report.md`

    第四步：生成分析报告
        - 整合所有信息，填写 Markdown 报告。
        - **关键要求**：填写模板时，必须替换 `<位置>` 占位符为实际的文件路径（本地）或 URL（远程）。
        - 重点对比：本地实现 vs 外部标准。
        - 输出文件：`best_practices_report.md` (或用户指定名称)。
        - 返回："✅ 报告已生成：best_practices_report.md"

[注意事项]
    - **位置追踪**：所有引用的代码片段必须附带来源（本地路径+行号 或 远程URL）。
    - **参数互斥**：调用 `delegate_task` 时，严禁同时提供 `category` 和 `subagent_type`。
    - **AST 优先**：搜索代码结构时，优先使用 `ast_grep_search` 而非纯文本 Grep。
    - **超时处理**：如果 Agent 超过 60s 未返回，先使用 Direct Search 的结果生成初步报告。
