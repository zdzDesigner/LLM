import OpenAI from "openai";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

const openai_api_key = process.env.OPENAI_API_KEY;
const openai_base_url = process.env.OPENAI_BASE_URL;
const openai_model = process.env.OPENAI_MODEL;

// 兼容 ESM 模式下的 __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 加载 .env (尽量在入口处加载，但这里加载也能保证运行)
dotenv.config({ path: path.resolve(process.cwd(), ".env") });

const client = new OpenAI({
  apiKey: openai_api_key || "dummy-key", // 防止未配置 key 导致直接报错
  baseURL: openai_base_url,
});

export async function callLLM(systemPrompt, userPrompt) {
  // 简单的校验
  if (!openai_api_key || openai_api_key === "dummy-key") {
    throw new Error("❌ 错误：未在 .env 文件中配置 OPENAI_API_KEY");
  }

  try {
    console.log("🤖 正在请求 AI 模型...");
    const response = await client.chat.completions.create({
      model: openai_model, // 建议先用便宜的模型测试，如 gpt-3.5-turbo 或 gpt-4o-mini
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
      temperature: 0.7,
    });
    return response.choices[0].message.content;
  } catch (error) {
    console.error("❌ LLM API 调用失败:", error.message);
    if (error.status === 401) console.error("提示：请检查 API Key 是否正确。");
    throw error;
  }
}
