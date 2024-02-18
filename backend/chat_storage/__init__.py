import sqlite3
import os

# Define the path for the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'databases')
os.makedirs(db_path, exist_ok=True)  # Ensure the databases directory exists

chats_db_path = os.path.join(db_path, 'chats.db')
messages_db_path = os.path.join(db_path, 'messages.db')

# Initialize databases
def init_db():
    # Connect to the chats database and create the table if it doesn't exist
    with sqlite3.connect(chats_db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS chats (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL)''')
    
    # Connect to the messages database and create the table if it doesn't exist
    with sqlite3.connect(messages_db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY,
                        chat_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        message TEXT NOT NULL,
                        FOREIGN KEY (chat_id) REFERENCES chats(id))''')

        id_exists = conn.execute('''SELECT EXISTS(SELECT 1 FROM messages WHERE id=49152)''').fetchone()[0]

        # If the record does not exist, insert it
        if not id_exists:
            conn.execute('''INSERT INTO messages (id, chat_id, user_id, message) VALUES (49152, 1, 1, 'Starting ID')''')

        
        

init_db()  # Initialize the database when the module is imported

# Define the module functions below
def get_chat_information(chat_id):
    with sqlite3.connect(chats_db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM chats WHERE id = ?", (chat_id,))
        return cur.fetchone()

def get_chat_history(chat_id):
    with sqlite3.connect(messages_db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM messages WHERE chat_id = ?", (chat_id,))
        return cur.fetchall()

def create_chat(chat_name):
    with sqlite3.connect(chats_db_path) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO chats (name) VALUES (?)", (chat_name,))
        conn.commit()
        return cur.lastrowid

def save_message_to_db(chat_id, user_id, message):
    with sqlite3.connect(messages_db_path) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (chat_id, user_id, message) VALUES (?, ?, ?)", (chat_id, user_id, message))
        conn.commit()
        return cur.lastrowid
