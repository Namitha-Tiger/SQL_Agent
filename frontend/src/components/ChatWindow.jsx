import ChatBubble from "./ChatBubble";
import TypingIndicator from "./TypingIndicator";
import { useEffect, useRef } from "react";

function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="chat-window">
      {messages.map((message) => (
        <ChatBubble
          key={message.id}
          sender={message.sender}
          text={message.text}
        />
      ))}

      {loading && <TypingIndicator />}

      <div ref={bottomRef}></div>
    </div>
  );
}

export default ChatWindow;