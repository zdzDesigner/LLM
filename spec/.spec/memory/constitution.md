# 项目章程

## PROJECT_NAME
CLI-UI-App

## TECH_STACK
- **Frontend**: React (using Ink library)
- **Backend**: Node.js (if required)
- **Other**: TypeScript (optional)

## CODING_STANDARDS
- **命名规则**: 使用 PascalCase 对组件和类，camelCase 对变量和函数，snake_case 对文件夹和文件名。
- **目录结构**:
  - `src/`: 主源代码目录
    - `components/`: 可复用的 UI 组件
    - `utils/`: 工具函数和辅助代码
    - `cli/`: CLI 具体实现
  - `tests/`: 测试代码目录
- **代码风格**: 遵循 Airbnb JavaScript Style Guide 和 Prettier 格式化规范。

## ARCHITECTURAL_PRINCIPLES
- **分层架构**: 前端采用组件化结构，后端 (如有) 采用分层架构，分离业务逻辑与数据访问层。
- **关注点分离**: CLI 功能模块与 UI 组件明确分离，减少耦合。
- **可扩展性**: 模块化设计，支持未来新增 CLI 功能或 UI 组件。
- **简洁性**: 优先实现核心功能，避免过度设计。