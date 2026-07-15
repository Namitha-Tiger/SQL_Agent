import "./ChatBubble.css";

function ChatBubble({ sender, text }) {
  return (
    <div
      className={`message-container ${
        sender === "user" ? "user" : "bot"
      }`}
    >
      <div className="message-bubble">
        {text}
      </div>
    </div>
  );
}

export default ChatBubble;