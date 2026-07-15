import { useState } from "react";

function ChatInput({ onSend, disabled }) {
  const [question, setQuestion] = useState("");

  const handleSend = () => {
    if (!question.trim()) return;

    onSend(question);

    setQuestion("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        placeholder="Type your question..."
        value={question}
        disabled={disabled}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
        onKeyDown={handleKeyDown}
      />

      <button
        onClick={handleSend}
        disabled={disabled}
      >
        Send
      </button>
    </div>
  );
}

export default ChatInput;