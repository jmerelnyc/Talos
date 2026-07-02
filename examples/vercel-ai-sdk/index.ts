// Example: call the Talos gateway with the Vercel AI SDK.
//
// The Talos gateway implements Chat Completions, not the OpenAI Responses
// API, so models are created with `.chat()` rather than the default
// `openai(modelId)` factory.
//
// Install:
//   npm install
//
// Run:
//   export TALOS_API_KEY=talos_YOUR_KEY
//   npx tsx index.ts

import { createOpenAI } from "@ai-sdk/openai";
import { streamText } from "ai";

const apiKey = process.env.TALOS_API_KEY;
if (!apiKey) {
  console.error("TALOS_API_KEY is not set. Create a key on your Talos dashboard and export it.");
  process.exit(1);
}

const talos = createOpenAI({
  apiKey,
  baseURL: process.env.TALOS_BASE_URL || "https://api.talos.ai/v1",
});

async function main() {
  const result = streamText({
    model: talos.chat(process.env.TALOS_MODEL || "talos-auto"),
    prompt: "Say hi in five words or fewer.",
  });

  for await (const chunk of result.textStream) {
    process.stdout.write(chunk);
  }
  process.stdout.write("\n");
}

main();