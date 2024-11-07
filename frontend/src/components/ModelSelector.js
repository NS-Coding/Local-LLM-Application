// src/components/ModelSelector.js
import React, { useEffect } from 'react';
import api from '../api';

const ModelSelector = ({ models, selectModel, currentModel }) => {
  useEffect(() => {
    const loadModel = async () => {
      try {
        await api.post('/select_model', { model_key: currentModel });
      } catch (error) {
        console.error('Error loading model:', error);
      }
    };
    loadModel();
  }, [currentModel]);

  return (
    <div className="model-selector">
      <label htmlFor="model-select">Select Model:</label>
      <select id="model-select" value={currentModel} onChange={(e) => selectModel(e.target.value)}>
        {models.map((model) => (
          <option key={model.key} value={model.key}>
            {model.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ModelSelector;
