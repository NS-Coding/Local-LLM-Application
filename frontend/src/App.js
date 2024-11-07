// src/App.js
import React, { useState } from 'react';
import ModelSelector from './components/ModelSelector';
import ChatWindow from './components/ChatWindow';
import ChatHistory from './components/ChatHistory';
import './styles/App.css';

function App() {
  const [currentModel, setCurrentModel] = useState('gpt2');

  const models = [
    { key: 'gpt2', name: 'GPT-2' },
    { key: 'distilgpt2', name: 'DistilGPT-2' },
    { key: 'gpt-neo', name: 'GPT-Neo 125M' },
  ];

  const selectModel = (modelKey) => {
    setCurrentModel(modelKey);
  };

  return (
    <div className="app-container">
      <h1>LLM Chat Application</h1>
      <ModelSelector models={models} selectModel={selectModel} currentModel={currentModel} />
      <div className="chat-section">
        <ChatWindow currentModel={currentModel} />
        <ChatHistory currentModel={currentModel} />
      </div>
    </div>
  );
}

export default App;
