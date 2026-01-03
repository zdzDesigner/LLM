export const PROMPTS = {
  CONSTITUTION: (userInput) => `
    你是一位资深架构师兼 CTO。
    任务：根据用户的输入，创建一份项目章程。
    
    用户输入：
    "${userInput}"
    
    请生成一份 Markdown 格式的章程，包含以下部分：
    1. PROJECT_NAME: 项目名称
    2. TECH_STACK: 明确的技术栈 (如 React, Node.js, Postgres)
    3. CODING_STANDARDS: 编码规范 (如命名规则、目录结构)
    4. ARCHITECTURAL_PRINCIPLES: 架构原则 (如分层架构、DDD)
    
    输出要简洁明了，不要有多余废话。
  `,

  SPECIFY: (constitution, userInput) => {
    // 如果 Constitution 还没生成，提示 AI 虽然没有章程，但依然要努力编写
    const constitutionContext = constitution.includes("暂无项目章程")
      ? "警告：当前没有项目章程，请根据通用最佳实践编写。"
      : `以下项目章程必须严格遵守：\n---\n${constitution}\n---`;

    return `
    你是一位资深的产品经理。
    
    ${constitutionContext}
    
    根据用户需求，编写一份详细的功能规格说明书。
    
    用户需求：
    "${userInput}"
    
    输出格式要求：
    # [Feature Name] Specification
    ## Background (背景)
    ## User Stories (用户故事)
    ## Functional Requirements (功能需求)
    ## API Endpoints (如果是后端) / UI Components (如果是前端)
    ## Non-Functional Requirements (非功能需求，如性能、安全)
  `;
  },
};
