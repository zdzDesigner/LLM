# CODE_EXAMPLE_SEARCHER - 使用示例

## 示例 1：React 异步状态管理

### 背景
用户在一个旧项目中工作，想知道团队目前是如何处理 React 异步请求状态的，以及业界推荐的写法，防止引入新的反模式。

### 输入
User: "关于在 React 中处理异步请求状态的最佳实践是什么？帮我找找例子。"

### 执行过程
1. **分析**: 关键词 "React", "异步状态", "最佳实践"。
2. **并发派发**:
   - `librarian`: 搜索 "React async state management patterns", "swr vs react-query examples", "useEffect fetch anti-patterns".
   - `explore`: 搜索本地 `useEffect`, `useState` 组合，或是否引入了 `react-query`/`swr`。
   - `Direct Tool`: `ast_grep_search(pattern='useEffect(() => { $$$ fetch($$$) $$$ })')`
3. **聚合**: 发现本地混用了 `Redux` 和手写 `useEffect`，外部推荐 `TanStack Query`。
4. **输出**: 生成报告，建议逐步迁移到 React Query，并给出本地重构示例。

### 输出
✅ 报告已生成：best_practices_report.md

## 示例 2：Python 错误重试机制

### 背景
用户想实现一个带指数退避的重试装饰器，但不确定项目里是否已经有了。

### 输入
User: "Python 错误重试机制的最佳实践，看看我们有没有现成的轮子。"

### 执行过程
1. **分析**: 关键词 "Python", "Retry", "Decorator", "Backoff".
2. **并发派发**:
   - `librarian`: 搜索 "tenacity usage examples", "python retry decorator best practice".
   - `explore`: 搜索 `def retry`, `@retry`, `import tenacity`.
3. **聚合**: 发现本地有一个手写的脆弱 `retry` 函数，外部推荐 `tenacity` 库。
4. **输出**: 报告建议引入 `tenacity` 库替代手写实现。
