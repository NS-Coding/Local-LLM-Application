# models.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAMES = {
    'gpt2': 'gpt2',
    'distilgpt2': 'distilgpt2',
    'gpt-neo': 'EleutherAI/gpt-neo-125M'
}

loaded_models = {}

def get_model(model_key):
    if model_key in loaded_models:
        return loaded_models[model_key]
    else:
        model_name = MODEL_NAMES.get(model_key)
        if model_name is None:
            raise ValueError(f"Model {model_key} is not recognized.")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        if torch.cuda.is_available():
            model.to('cuda')
        loaded_models[model_key] = (model, tokenizer)
        return model, tokenizer
