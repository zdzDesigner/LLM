import { ChatOpenAI } from "@langchain/openai"
import { createAgent } from "@langchain/classic"

import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio"
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter"

import { OpenAIEmbeddings } from "@langchain/openai"
import { MemoryVectorStore } from "langchain/vectorstores/memory"

import * as dotenv from "dotenv"
dotenv.config()

const model = new ChatOpenAI({
  modelName: "gpt-3.5-turbo",
  temperature: 0.7,
})

const loader = new CheerioWebBaseLoader(
  "https://js.langchain.com/docs/expression_language/",
)
const docs = await loader.load()

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 100,
  chunkOverlap: 20,
})
const splitDocs = await splitter.splitDocuments(docs)

const embeddings = new OpenAIEmbeddings()

const vectorstore = await MemoryVectorStore.fromDocuments(splitDocs, embeddings)

const retriever = vectorstore.asRetriever({ k: 2 })

const agent = createAgent({
  llm: model,
  systemMessage: "Answer the user's question from the following context: {context}",
  middleware: async (state, next) => {
    const docs = await retriever.invoke(state.messages[state.messages.length - 1].content)
    state.context = docs.map(doc => doc.pageContent).join("\n\n")
    return next(state)
  }
})

const response = await agent.invoke({
  messages: [{ role: "user", content: "What is LCEL?" }]
})

console.log(response)