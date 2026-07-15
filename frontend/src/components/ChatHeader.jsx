import "./ChatHeader.css";

function ChatHeader() {
  return (
    <header className="chat-header">
      <div className="logo">🤖</div>

      <div>
        <h2>Retail SQL Assistant</h2>
        <p>Ask me anything about your retail database</p>
      </div>
    </header>
  );
}

export default ChatHeader;