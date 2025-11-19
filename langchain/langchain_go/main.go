package main

import (
	"context"
	"fmt"
	"os"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/openai"
)

func main() {
	key := os.Getenv("OPENAI_API_KEY")
	fmt.Println(key)

	ctx := context.Background()

	llm, err := openai.New(
		openai.WithToken(key),
		openai.WithModel("Qwen/Qwen2.5-7B-Instruct"),
		openai.WithBaseURL("https://api.siliconflow.cn/v1"),
	)
	if err != nil {
		return
	}

	messages := []llms.MessageContent{
		llms.TextParts(llms.ChatMessageTypeSystem, "你是一个golang语言专家"),
		llms.TextParts(llms.ChatMessageTypeHuman, "帮我介绍下interface类型"),
	}

	// llm.GenerateContent(ctx,messages,func(co *llms.CallOptions) {})
	res, err := llm.GenerateContent(ctx, messages, llms.WithTemperature(0.7))
	for _, cc := range res.Choices {
		fmt.Println(cc.Content)
	}
}
