import sqlite3

DB_NAME = "translator_bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            target_lang TEXT DEFAULT 'en'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_text TEXT,
            translated_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_user_lang(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT target_lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return 'en'

def set_user_lang(user_id, lang_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, target_lang) 
        VALUES(?, ?) 
        ON CONFLICT(user_id) DO UPDATE SET target_lang = ?
    ''', (user_id, lang_code, lang_code))
    conn.commit()
    conn.close()

def add_history(user_id, original, translated):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO history (user_id, original_text, translated_text) 
        VALUES (?, ?, ?)
    ''', (user_id, original, translated))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT original_text, translated_text FROM history 
        WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT 5
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows