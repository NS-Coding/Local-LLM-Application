// src/components/ChatHistory.js
import React, { useEffect, useState } from 'react';
import api from '../api';

const ChatHistory = ({ currentModel }) => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get('/history', {
          params: { model_key: currentModel },
        });
        setHistory(response.data.history);
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    };
    fetchHistory();
  }, [currentModel]);

  return (
    <div className="chat-history">
      <h2>Chat History ({currentModel})</h2>
      {history.length === 0 ? (
        <p>No chat history available.</p>
      ) : (
        history.map((chat) => (
          <div key={chat.id} className="history-item">
            <p>
              <strong>You:</strong> {chat.user_message}
            </p>
            <p>
              <strong>Bot:</strong> {chat.bot_response}
            </p>
            <hr />
          </div>
        ))
      )}
    </div>
  );
};

export default ChatHistory;
