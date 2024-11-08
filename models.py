import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

loaded_models = {}

def get_available_models():
    # Add or remove model names here
    return [
        'nvidia/Nemotron-4-340B-Instruct',
        'deepseak-ai/DeepSeek-Coder-V2-Instruct',  
        'CohereForAI/c4ai-command-r-plus',
        'Qwen/Qwen2-72B-Instruct',
    ]

def load_model(model_name):
    if model_name in loaded_models:
        return loaded_models[model_name]
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        if torch.cuda.is_available():
            model.to('cuda')
        loaded_models[model_name] = (model, tokenizer)
        return loaded_models[model_name]

def generate_response(model_tuple, conversation_history):
    model, tokenizer = model_tuple

    # Prepare the prompt with conversation history
    prompt = ''
    for msg in conversation_history:
        prompt += f"{msg['sender']}: {msg['message']}\n"
    prompt += 'Bot:'

    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    attention_mask = torch.ones_like(input_ids)

    if torch.cuda.is_available():
        input_ids = input_ids.to('cuda')
        attention_mask = attention_mask.to('cuda')

    output_ids = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=input_ids.size(1) + 200,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_p=0.95,
        top_k=60,
    )

    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # Extract the bot's response
    response = output_text[len(prompt):].split('User:')[0].strip()
    return response
