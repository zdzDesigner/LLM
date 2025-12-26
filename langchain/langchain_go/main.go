package main

import (
	"context"
	"fmt"
	"os"
	// "time"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/openai"
)

func main() {
	key := os.Getenv("OPENAI_API_KEY")
	fmt.Println(key)

	ctx := context.Background()
	// ctx, cancel := context.WithCancel(context.Background())

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

	// go func() {
	// 	time.Sleep(time.Second * 3)
	// 	cancel()
	// }()
	go func() {
		select {
		case <-ctx.Done():
			fmt.Println("OK")
			// default:
			// 	time.Sleep(time.Second * 1)
			// 	fmt.Println("xxxxxxx")
		}
	}()
	// llm.GenerateContent(ctx,messages,func(co *llms.CallOptions) {})
	res, err := llm.GenerateContent(ctx, messages, llms.WithTemperature(0.7))
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(res)
	// for _, cc := range res.Choices {
	// 	fmt.Println(cc)
	// 	// fmt.Println(cc.Content)
	// }
}
