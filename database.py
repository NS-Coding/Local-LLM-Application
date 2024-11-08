import sqlite3
from datetime import datetime

DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            created_at TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            sender TEXT,
            message TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_conversations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conversations ORDER BY created_at DESC')
    conversations = cursor.fetchall()
    conn.close()
    return conversations

def create_new_conversation(model_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO conversations (model_name, created_at) VALUES (?, ?)',
        (model_name, datetime.now()),
    )
    conn.commit()
    conversation_id = cursor.lastrowid
    conn.close()
    return conversation_id

def save_message(conversation_id, sender, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (conversation_id, sender, message, timestamp) VALUES (?, ?, ?, ?)',
        (conversation_id, sender, message, datetime.now()),
    )
    conn.commit()
    conn.close()

def get_messages(conversation_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT sender, message FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC',
        (conversation_id,),
    )
    messages = cursor.fetchall()
    conn.close()
    return messages
