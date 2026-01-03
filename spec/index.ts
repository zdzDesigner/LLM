import inquirer from "inquirer";
import chalk from "chalk";
import { callLLM } from "./core/llm.js";
import {
  loadConstitution,
  saveSpec,
  saveConstitution,
} from "./core/context.js";
import { PROMPTS } from "./core/prompts.js";

async function main() {
  try {
    console.log(chalk.cyan.bold("\n🚀 Welcome to Mini Spec Kit v1.0"));

    // 检查环境变量
    if (!process.env.OPENAI_API_KEY) {
      console.log(chalk.red("❌ 未检测到 OPENAI_API_KEY。"));
      console.log(
        chalk.yellow("请确保在项目根目录下有 .env 文件并配置了 Key。\n")
      );
      process.exit(1);
    }

    const { action } = await inquirer.prompt([
      {
        type: "list",
        name: "action",
        message: "请选择操作:",
        choices: [
          { name: "1. 初始化/更新章程", value: "constitution" },
          { name: "2. 创建功能 Spec", value: "spec" },
          { name: "3. 退出", value: "exit" },
        ],
      },
    ]);

    if (action === "constitution") {
      await handleConstitution();
    } else if (action === "spec") {
      await handleSpecify();
    } else {
      console.log(chalk.gray("👋 再见！"));
      process.exit(0);
    }
  } catch (error) {
    console.error(chalk.red("\n❌ 程序发生错误:"), error.message);
    // 调试用：打印完整堆栈
    // console.error(error);
  }
}

// --- 逻辑流 1: Constitution ---
async function handleConstitution() {
  const { userInput } = await inquirer.prompt([
    {
      type: "input",
      name: "userInput",
      message: "描述一下你的项目构想 (技术栈、目标等):",
    },
  ]);

  console.log(chalk.yellow("🧠 AI 正在思考项目章程..."));

  const systemPrompt = "你是一个 expert CTO，擅长制定技术标准和架构规范。";
  const userPrompt = PROMPTS.CONSTITUTION(userInput);

  const constitutionContent = await callLLM(systemPrompt, userPrompt);

  const savedPath = await saveConstitution(constitutionContent);

  console.log(chalk.green(`✅ 章程已生成/更新: ${savedPath}`));

  // 询问是否继续创建 Spec
  const { continueNext } = await inquirer.prompt([
    {
      type: "confirm",
      name: "continueNext",
      message: "是否现在创建第一个功能 Spec?",
      default: true,
    },
  ]);

  if (continueNext) {
    await handleSpecify();
  } else {
    process.exit(0);
  }
}

// --- 逻辑流 2: Specify ---
async function handleSpecify() {
  const constitution = await loadConstitution();

  if (constitution.includes("暂无项目章程")) {
    console.log(
      chalk.yellow(
        "⚠️  警告：当前没有有效的项目章程，AI 将基于通用常识生成 Spec。建议先运行 '初始化章程'。\n"
      )
    );
  }

  const { featureName, userInput } = await inquirer.prompt([
    {
      type: "input",
      name: "featureName",
      message: "功能名称 (例如: user-login):",
    },
    { type: "input", name: "userInput", message: "描述这个功能的需求:" },
  ]);

  console.log(
    chalk.yellow(`🧠 AI 正在基于章程编写 [${featureName}] 的规格文档...`)
  );

  const systemPrompt =
    "你是一个资深产品经理，擅长编写技术规格说明书，并且严格遵守给定的约束条件。";
  const userPrompt = PROMPTS.SPECIFY(constitution, userInput);

  const specContent = await callLLM(systemPrompt, userPrompt);

  const savedPath = await saveSpec(featureName, specContent);

  console.log(chalk.green(`✅ 规格文档已生成: ${savedPath}/spec.md`));
}

// 启动程序
main();
