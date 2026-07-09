import { useState, useEffect, useRef } from "react";
import "./ChatAssistant.css";
import { FaRobot, FaPaperPlane } from "react-icons/fa";
import { sendMessage } from "../services/api";

const ChatAssistant = ({ setAiFormData }) => {

  const [input, setInput] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text:
        "👋 Hello! I can help you log HCP interactions.\n\nTry asking:\n\n• Log meeting with Dr Sharma today\n• Dr Sharma gave positive feedback\n• Is Dr Sharma available tomorrow?\n• Edit previous interaction outcome\n• Show previous interactions",
    },
  ]);

  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const handleSend = async () => {

    if (!input.trim()) return;

    const userMessage = {
      sender: "user",
      text: input,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {

      const data = await sendMessage(input);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: data.response,
        },
      ]);
      if(data.form_data){
    setAiFormData(data.form_data);
  }

    } catch (err) {

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "❌ Backend not responding.",
        },
      ]);

      console.log(err);

    }

    setLoading(false);

    setInput("");

  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="chat-container">

      <div className="chat-header">

        <div className="chat-title">

          <FaRobot className="robot-icon" />

          <div>

            <h2>AI Assistant</h2>

            <p>Log interactions using natural language</p>

          </div>

        </div>

      </div>

      <div className="chat-body">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={msg.sender === "user" ? "user-message" : "ai-message"}
          >
            {msg.text}
          </div>

        ))}

        {loading && (
          <div className="ai-message">
            Thinking...
          </div>
        )}
        <div ref={messagesEndRef}></div>

      </div>
      
      <div className="chat-input">

        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSend();
            }
          }}
          placeholder="Ask AI anything..."
        />

        <button onClick={handleSend}>
          <FaPaperPlane />
        </button>

      </div>

    </div>
  );
};

export default ChatAssistant;