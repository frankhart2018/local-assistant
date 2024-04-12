import React, { useState } from 'react';
import Markdown from "react-markdown";

const SSEComponent = () => {
  const [messages, setMessages] = useState("");

  const connectToSSE = () => {
    setMessages("");
    const eventSource = new EventSource('http://localhost:8080/stream-assistant?id=0');

    eventSource.onmessage = function(event) {
      if (event.data.trim() === "END") {
        eventSource.close();
        return;
      }
      setMessages((prev) => {
        return `${prev}${event.data.replaceAll("<NEWLINE>", "\n")}`;
      });
    };

    eventSource.onerror = function(error) {
      console.error('EventSource failed:', error);
      eventSource.close();
    };
  };

  return (
    <div>
      <button onClick={connectToSSE}>Connect to SSE</button>
      <Markdown>{messages}</Markdown>
    </div>
  );
};

export default SSEComponent;
