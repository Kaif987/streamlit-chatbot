"use client";

import {
  Composer,
  Thread,
  ThreadConfig,
  ThreadWelcome,
} from "@assistant-ui/react";
import { FC } from "react";

export default function Home() {
  return (
    <MyThread
      composer={{
        allowAttachments: true,
      }}
    />
  );
}

const MyThread: FC<ThreadConfig> = (config) => {
  return (
    <Thread.Root config={config}>
      <Thread.Viewport>
        <ThreadWelcome />
        <Thread.Messages />
        <Thread.ViewportFooter>
          <Thread.ScrollToBottom />
          <Composer />
        </Thread.ViewportFooter>
      </Thread.Viewport>
    </Thread.Root>
  );
};
