import { ChatOpenAI } from "@langchain/openai"
import { ChatPromptTemplate } from "@langchain/core/prompts"

// Import environment variables
import * as dotenv from "dotenv"
dotenv.config()

// Instantiate the model
const model = new ChatOpenAI({
  modelName: "Qwen/Qwen2.5-7B-Instruct",
  temperature: 0.9,
  configuration: {
    baseURL: "https://api.siliconflow.cn/v1",
  },
})

// Create Prompt Template using fromTemplate
const prompt1 = ChatPromptTemplate.fromTemplate("Tell a joke about {word}")

// Create Prompt Template from fromMessages
const prompt2 = ChatPromptTemplate.fromMessages([
  [
    "system",
    "You are a talented chef.  Create a recipe based on a main ingredient provided by the user. Please answer in Chinese",
  ],
  ["human", "{word}"],
])

// const chain = prompt1.pipe(model)
const chain = prompt2.pipe(model)

const response = await chain.invoke({ word: "dog" })

console.log(response)
