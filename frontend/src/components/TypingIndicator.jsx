import "./TypingIndicator.css";

function TypingIndicator() {
  return (
    <div className="message-container bot">
      <div className="typing">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
}

export default TypingIndicator;