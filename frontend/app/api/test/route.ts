import { RemoteRunnable } from "@langchain/core/runnables/remote";
import { Message } from "ai";
import { NextResponse } from "next/server";

export const maxDuration = 30;

export async function POST(req: Request) {
  const msg: Message = await req.json();
  console.log(msg);

  const remoteChain = new RemoteRunnable({
    url: "http://localhost:8000/chain/",
  });

  const response = await remoteChain.invoke("hi");

  return NextResponse.json(response);
}
