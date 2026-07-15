import { useState } from "react";
import "./App.css";

import ChatHeader from "./components/ChatHeader.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import ChatInput from "./components/ChatInput.jsx";

import { askQuestion } from "./services/api";

interface Message {
  id: number;
  sender: "user" | "bot";
  text: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      sender: "bot",
      text: "Hello! 👋 I'm your Retail SQL Assistant. Ask me anything about your database.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const handleSend = async (question: string) => {
    if (!question.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      // Call FastAPI backend
      const response = await askQuestion(question);

      // Add bot response
      const botMessage: Message = {
        id: Date.now() + 1,
        sender: "bot",
        text: response.answer,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now() + 2,
        sender: "bot",
        text: "Sorry, something went wrong while processing your request.",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <ChatHeader />

      <ChatWindow
        messages={messages}
        loading={loading}
      />

      <ChatInput
        onSend={handleSend}
        disabled={loading}
      />
    </div>
  );
}

export default App;