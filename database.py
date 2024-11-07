# database.py

import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_chat(model_key, user_message, bot_response):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('INSERT INTO chats (model, user_message, bot_response) VALUES (?, ?, ?)',
              (model_key, user_message, bot_response))
    conn.commit()
    conn.close()

def get_chat_history(model_key=None, limit=20, offset=0):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    if model_key:
        c.execute('SELECT * FROM chats WHERE model = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?', 
                  (model_key, limit, offset))
    else:
        c.execute('SELECT * FROM chats ORDER BY timestamp DESC LIMIT ? OFFSET ?', 
                  (limit, offset))
    chats = c.fetchall()
    conn.close()

    chat_history = [{
        'id': chat[0],
        'model': chat[1],
        'user_message': chat[2],
        'bot_response': chat[3],
        'timestamp': chat[4]
    } for chat in chats]

    return chat_history
