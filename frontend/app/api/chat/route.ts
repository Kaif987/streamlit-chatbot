import { RemoteRunnable } from "@langchain/core/runnables/remote";
import type { RunnableConfig } from "@langchain/core/runnables";
import { LangChainAdapter, type Message } from "ai";
import fs from "node:fs/promises";

export const maxDuration = 30;

export async function POST(req: Request) {
  const formData = await req.formData();
  const file = formData.get("file") as File;
  console.log(file);
  const arrayBuffer = await file.arrayBuffer();
  const buffer = new Uint8Array(arrayBuffer);
  console.log(buffer);
  await fs.writeFile(`./public/uploads/${file.name}`, buffer);

  const { messages }: { messages: Message[] } = await req.json();

  // TODO replace with your own langserve URL
  const remoteChain = new RemoteRunnable<string, string, RunnableConfig>({
    url: "http://localhost:8000/chain/",
  });

  const stream = await remoteChain.stream(
    messages[messages.length - 1].content
  );

  // NextResponse.json(stream);

  return LangChainAdapter.toDataStreamResponse(stream);
}
