from flask import render_template, request, redirect, url_for
from models import get_available_models, load_model, generate_response
from database import (
    get_conversations,
    create_new_conversation,
    save_message,
    get_messages,
)

def init_routes(app):
    @app.route('/')
    def index():
        models = get_available_models()
        conversations = get_conversations()
        return render_template('index.html', models=models, conversations=conversations)

    @app.route('/new_chat', methods=['POST'])
    def new_chat():
        model_name = request.form['model']
        conversation_id = create_new_conversation(model_name)
        return redirect(url_for('chat', model_name=model_name, conversation_id=conversation_id))

    @app.route('/chat/<model_name>/<int:conversation_id>', methods=['GET', 'POST'])
    def chat(model_name, conversation_id):
        model_tuple = load_model(model_name)
        messages = get_messages(conversation_id)

        if request.method == 'POST':
            user_message = request.form['message']
            save_message(conversation_id, 'User', user_message)

            # Get updated messages after saving the user's message
            conversation_history = get_messages(conversation_id)
            bot_response = generate_response(model_tuple, conversation_history)
            save_message(conversation_id, 'Bot', bot_response)

            return redirect(url_for('chat', model_name=model_name, conversation_id=conversation_id))

        return render_template(
            'chat.html',
            model_name=model_name,
            conversation_id=conversation_id,
            messages=messages,
        )
