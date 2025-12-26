import { ChatOpenAI } from "@langchain/openai"

import { ChatPromptTemplate } from "@langchain/core/prompts"
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio"
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters"

import { OpenAIEmbeddings } from "@langchain/openai"
import { MemoryVectorStore } from "@langchain/classic/vectorstores/memory"
// import { Milvus } from "@langchain/milvus"

import { createAgent } from "langchain"

import * as dotenv from "dotenv"
dotenv.config()

const model_chat = new ChatOpenAI({
  modelName: "Qwen/Qwen2.5-7B-Instruct",
  temperature: 0.9,
  configuration: {
    baseURL: "https://api.siliconflow.cn/v1",
  },
})

const docs = [
  {
    pageContent: `
Gain control with LangGraph to design agents that reliably handle complex tasks

Trusted by companies shaping the future of agents— including Klarna, Replit, Elastic, and more— LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents.
LangGraph is very low-level, and focused entirely on agent orchestration. Before using LangGraph, we recommend you familiarize yourself with some of the components used to build agents, starting with models and tools.
We will commonly use LangChain components throughout the documentation to integrate models and tools, but you don’t need to use LangChain to use LangGraph. If you are just getting started with agents or want a higher-level abstraction, we recommend you use LangChain’s agents that provide pre-built architectures for common LLM and tool-calling loops.
LangGraph is focused on the underlying capabilities important for agent orchestration: durable execution, streaming, human-in-the-loop, and more.`,
    metadata: { source: "example.txt" },
  },
]
// const loader = new CheerioWebBaseLoader(
//   "https://docs.langchain.com/oss/javascript/langchain/overview",
// )
// console.log("加载要向量化文档.......")
// const docs = await loader.load()
// console.log({ docs })

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 100,
  chunkOverlap: 20,
})
const splitDocs = await splitter.splitDocuments(docs)
// const vectorStore = await Milvus.fromDocuments(
//   splitDocs,
//   new OpenAIEmbeddings(),
//   {
//     collectionName: "your_collection",
//     url: "http://localhost:19530", // Milvus 服务地址
//   },
// )
const model_embedding = new OpenAIEmbeddings({
  // modelName: "BAAI/bge-large-zh-v1.5",
  modelName: "BAAI/bge-m3",
  temperature: 0.9,
  configuration: {
    baseURL: "https://api.siliconflow.cn/v1",
  },
})
const vectorstore = await MemoryVectorStore.fromDocuments(
  splitDocs,
  model_embedding,
)
console.log({ vectorstore })
// 打印向量数据
console.log("存储的向量数据:")
console.log(vectorstore.memoryVectors)

// 或者打印更详细的信息
vectorstore.memoryVectors.forEach((item, index) => {
  console.log(`文档 ${index}:`)
  console.log("内容:", item.content)
  console.log("向量:", item.embedding)
  console.log("元数据:", item.metadata)
  console.log("---")
})

const retriever = vectorstore.asRetriever({ k: 2 })

const agent = createAgent({
  model: model_chat,
  systemMessage:
    "Answer the user's question from the following context: {context}",
  middleware: [
    async (state, next) => {
      const docs = await retriever.invoke(
        state.messages[state.messages.length - 1].content,
      )
      state.context = docs.map((doc) => doc.pageContent).join("\n\n")
      console.log({ docs })
      return next(state)
    },
  ],
})

const response = await agent.invoke({
  messages: [{ role: "user", content: "What is LangGraph feature?" }],
})

console.log(response)
