// src/components/ChatWindow.js
import React, { useState } from 'react';
import api from '../api';

const ChatWindow = ({ currentModel }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = input;
    setInput('');
    setMessages([...messages, { sender: 'user', text: userMessage }]);
    setLoading(true);

    try {
      const response = await api.post('/chat', {
        model_key: currentModel,
        message: userMessage,
      });
      setMessages((msgs) => [...msgs, { sender: 'bot', text: response.data.response }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((msgs) => [...msgs, { sender: 'bot', text: 'Error: ' + error.message }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="chat-window">
      <h2>Chat with {currentModel}</h2>
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
          </div>
        ))}
        {loading && <p>Loading...</p>}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          placeholder="Type your message..."
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
