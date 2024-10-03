"use client";

import { useChat } from "ai/react";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useVercelUseChatRuntime } from "@assistant-ui/react-ai-sdk";

export function MyRuntimeProvider({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const chat = useChat({
    api: "/api/chat",
  });

  const runtime = useVercelUseChatRuntime(chat);
  // const runtime = useEdgeRuntime({
  //   api: "/api/chat",
  //   adapters: {
  //     attachments: new CompositeAttachmentAdapter([
  //       new SimpleTextAttachmentAdapter(),
  //     ]),
  //   },
  // });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      {children}
    </AssistantRuntimeProvider>
  );
}
