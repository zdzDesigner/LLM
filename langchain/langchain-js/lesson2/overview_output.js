const v = {
  messages: {
    HumanMessage: {
      id: "79243383-bb25-4108-9076-9c475d6a1d1b",
      content: "What's the weather in Tokyo?",
      additional_kwargs: {},
      response_metadata: {},
    },
    AIMessage: {
      id: "019a9acad22b2f2c12336f2fd1bcc93a",
      content: "",
      name: "model",
      additional_kwargs: {
        tool_calls: [
          {
            id: "019a9acad347f23491fc5d5915688d74",
            type: "function",
            function: "[Object]",
          },
        ],
      },
      response_metadata: {
        tokenUsage: {
          promptTokens: 204,
          completionTokens: 22,
          totalTokens: 226,
        },
        finish_reason: "tool_calls",
        model_provider: "openai",
        model_name: "Qwen/Qwen2.5-7B-Instruct",
      },
      tool_calls: [
        {
          name: "get_weather",
          args: {
            city: "Tokyo",
          },
          type: "tool_call",
          id: "019a9acad347f23491fc5d5915688d74",
        },
      ],
      invalid_tool_calls: [],
      usage_metadata: {
        output_tokens: 22,
        input_tokens: 204,
        total_tokens: 226,
        input_token_details: {},
        output_token_details: {
          reasoning: 0,
        },
      },
    },
    ToolMessage: {
      id: "30a198e1-04eb-48ad-8000-b2347a398336",
      content: "It's always sunny in Tokyo!",
      name: "get_weather",
      additional_kwargs: {},
      response_metadata: {},
      tool_call_id: "019a9acad347f23491fc5d5915688d74",
    },
    AIMessage: {
      id: "019a9acad3c46c8ac7efde80ed8086d3",
      content:
        "It seems there's always sunshine in Tokyo! However, for more detailed weather information, I can provide you with the current temperature, humidity, and other relevant details. Would you like that?",
      name: "model",
      additional_kwargs: {},
      response_metadata: {
        tokenUsage: {
          promptTokens: 250,
          completionTokens: 38,
          totalTokens: 288,
        },
        finish_reason: "stop",
        model_provider: "openai",
        model_name: "Qwen/Qwen2.5-7B-Instruct",
      },
      tool_calls: [],
      invalid_tool_calls: [],
      usage_metadata: {
        output_tokens: 38,
        input_tokens: 250,
        total_tokens: 288,
        input_token_details: {},
        output_token_details: {
          reasoning: 0,
        },
      },
    },
  },
}
