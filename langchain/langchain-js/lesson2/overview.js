import * as z from "zod"
// npm install @langchain/anthropic to call the model
import { createAgent } from "langchain"
import { tool } from "@langchain/core/tools"
import { ChatOpenAI } from "@langchain/openai"

const model = new ChatOpenAI({
  modelName: "Qwen/Qwen2.5-7B-Instruct",
  temperature: 0.7,
  configuration: {
    baseURL: "https://api.siliconflow.cn/v1",
  },
})

// tool_calls: [
//   {
//     name: "get_weather",
//     args: {
//       city: "Tokyo",
//     },
//     type: "tool_call",
//     id: "019a9acad347f23491fc5d5915688d74",
//   },
// ],

const getWeather = tool(({ city }) => `It's always sunny in ${city}!`, {
  name: "get_weather",
  description: "Get the weather for a given city",
  schema: z.object({
    city: z.string(),
  }),
})

const agent = createAgent({
  model,
  tools: [getWeather],
})

console.log(
  await agent.invoke({
    // messages: [{ role: "user", content: "What's the weather in Tokyo?" }],
    // messages: [{ role: "human", content: "What's the weather in Tokyo?" }],
    messages: [
      { role: "human", content: "What's the weather in China SuZhou?" },
    ],
  }),
)

//  human => AI => tools => AI
