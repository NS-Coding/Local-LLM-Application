# routes.py

from flask import Blueprint, request, jsonify
from models import get_model, MODEL_NAMES
from database import save_chat, get_chat_history
import torch

routes = Blueprint('routes', __name__)

@routes.route('/select_model', methods=['POST'])
def select_model():
    data = request.get_json()
    model_key = data.get('model_key')
    if model_key in MODEL_NAMES:
        # Load the model (this will download if not already)
        get_model(model_key)
        return jsonify({'status': f'Model {model_key} loaded'}), 200
    else:
        return jsonify({'error': 'Model not found'}), 404

@routes.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    model_key = data.get('model_key')
    user_message = data.get('message')

    if model_key not in MODEL_NAMES:
        return jsonify({'error': 'Model not found'}), 404

    try:
        model, tokenizer = get_model(model_key)
        inputs = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')
        if torch.cuda.is_available():
            inputs = inputs.to('cuda')
        outputs = model.generate(inputs, max_length=500, pad_token_id=tokenizer.eos_token_id)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Save to database
        save_chat(model_key, user_message, response_text)

        return jsonify({'response': response_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/history', methods=['GET'])
def get_history():
    model_key = request.args.get('model_key')
    limit = int(request.args.get('limit', 20))  # Default to 20 records
    offset = int(request.args.get('offset', 0))

    chat_history = get_chat_history(model_key, limit, offset)

    return jsonify({'history': chat_history}), 200

# Error handler for the routes
@routes.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': str(e)}), 500
