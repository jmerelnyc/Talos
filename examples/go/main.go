// Example: call the Talos gateway with the community go-openai client.
//
// Install:
//   go mod tidy
//
// Run:
//   export TALOS_API_KEY=talos_YOUR_KEY
//   go run main.go
package main

import (
	"context"
	"fmt"
	"os"

	openai "github.com/sashabaranov/go-openai"
)

func main() {
	apiKey := os.Getenv("TALOS_API_KEY")
	if apiKey == "" {
		fmt.Println("TALOS_API_KEY is not set. Create a key on your Talos dashboard and export it.")
		os.Exit(1)
	}

	baseURL := os.Getenv("TALOS_BASE_URL")
	if baseURL == "" {
		baseURL = "https://api.usetalos.xyz/v1"
	}
	model := os.Getenv("TALOS_MODEL")
	if model == "" {
		model = "talos-auto"
	}

	config := openai.DefaultConfig(apiKey)
	config.BaseURL = baseURL
	client := openai.NewClientWithConfig(config)

	stream, err := client.CreateChatCompletionStream(context.Background(), openai.ChatCompletionRequest{
		Model: model,
		Messages: []openai.ChatCompletionMessage{
			{Role: openai.ChatMessageRoleUser, Content: "Say hi in five words or fewer."},
		},
		Stream: true,
	})
	if err != nil {
		fmt.Println("error:", err)
		os.Exit(1)
	}
	defer stream.Close()

	for {
		resp, err := stream.Recv()
		if err != nil {
			break
		}
		fmt.Print(resp.Choices[0].Delta.Content)
	}
	fmt.Println()
}