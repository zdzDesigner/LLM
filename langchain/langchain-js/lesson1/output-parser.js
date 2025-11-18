import { ChatOpenAI } from "@langchain/openai"
import { ChatPromptTemplate } from "@langchain/core/prompts"
import {
  CommaSeparatedListOutputParser,
  StringOutputParser,
  StructuredOutputParser,
} from "@langchain/core/output_parsers"

import { z } from "zod"
// import { StructuredOutputParser } from "@langchain/core/output_parsers"

// Import environment variables
import * as dotenv from "dotenv"
dotenv.config()

// Instantiate the model
const model = new ChatOpenAI({
  modelName: "Qwen/Qwen2.5-7B-Instruct",
  temperature: 0.9,
  // temperature: 0,
  // temperature: 9,
  configuration: {
    baseURL: "https://api.siliconflow.cn/v1",
  },
})

async function callStringOutputParser() {
  const prompt = ChatPromptTemplate.fromTemplate(
    "Tell a joke about {word}. Please answer in Chinese",
  )
  const outputParser = new StringOutputParser()

  // Create the Chain
  const chain = prompt.pipe(model).pipe(outputParser)
  // const chain = prompt.pipe(model)

  return await chain.invoke({ word: "dog" })
}

async function callListOutputParser() {
  const prompt = ChatPromptTemplate.fromMessages([
    [
      "system",
      "Provide 5 synonyms, seperated by commas, for a word that the user will provide. Please answer in Chinese",
    ],
    ["human", "{word}"],
  ])
  const outputParser = new CommaSeparatedListOutputParser() // 逗号分隔

  const chain = prompt.pipe(model).pipe(outputParser)

  return await chain.invoke({
    word: "happy",
  })
}

async function callStructuredParser() {
  const prompt = ChatPromptTemplate.fromTemplate(
    "Extract information from the following phrase.\n{format_instructions}\n{phrase}",
  )

  // 信息提取
  const outputParser = StructuredOutputParser.fromNamesAndDescriptions({
    name: "name of the person",
    age: "age of person",
  })

  const chain = prompt.pipe(model).pipe(outputParser)
  console.log("getFormatInstructions:", outputParser.getFormatInstructions())

  return await chain.invoke({
    phrase: "Max is 30 years old",
    format_instructions: outputParser.getFormatInstructions(),
  })
}

async function callZodStructuredParser() {
  const prompt = ChatPromptTemplate.fromTemplate(
    "Extract information from the following phrase.\n{format_instructions}\n{phrase}",
  )
  const outputParser = StructuredOutputParser.fromZodSchema(
    z.object({
      recipe: z.string().describe("name of recipe"),
      ingredients: z.array(z.string()).describe("ingredients"),
    }),
  )
  console.log("getFormatInstructions:", outputParser.getFormatInstructions())

  // Create the Chain
  const chain = prompt.pipe(model).pipe(outputParser)

  return await chain.invoke({
    phrase:
      "The ingredients for a Spaghetti Bolognese recipe are tomatoes, minced beef, garlic, wine and herbs.",
    format_instructions: outputParser.getFormatInstructions(),
  })
}

// const response = await callStringOutputParser();
// const response = await callListOutputParser();
// const response = await callStructuredParser();
const response = await callZodStructuredParser()
console.log(response)
