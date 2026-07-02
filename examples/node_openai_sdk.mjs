// Example: call the Talos gateway with the official OpenAI Node.js SDK.
//
// Install:
//   npm install openai
//
// Run:
//   export TALOS_API_KEY=talos_YOUR_KEY
//   node node_openai_sdk.mjs

import OpenAI from "openai";

const baseURL = process.env.TALOS_BASE_URL || "https://api.talos.ai/v1";
const model = process.env.TALOS_MODEL || "talos-auto";

async function main() {
  const apiKey = process.env.TALOS_API_KEY;
  if (!apiKey) {
    console.error("TALOS_API_KEY is not set. Create a key on your Talos dashboard and export it.");
    process.exit(1);
  }

  const client = new OpenAI({ apiKey, baseURL });

  const stream = await client.chat.completions.create({
    model,
    messages: [{ role: "user", content: "Say hi in five words or fewer." }],
    stream: true,
  });

  for await (const chunk of stream) {
    const delta = chunk.choices[0]?.delta?.content || "";
    process.stdout.write(delta);
  }
  process.stdout.write("\n");
}

main();