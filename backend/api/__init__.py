from flask import Flask, g, current_app
from flask_cors import CORS
import sqlite3
import os
import sqlite3



# Define the path for the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'databases')
os.makedirs(db_path, exist_ok=True)  # Ensure the databases directory exists

chats_db_path = os.path.join(db_path, 'chats.db')
messages_db_path = os.path.join(db_path, 'messages.db')
users_db_path = os.path.join(db_path, 'users.db')


def create_app():
    app = Flask(__name__)
    CORS(app)
    file_path = os.path.abspath(os.getcwd())+"/backend/databases/users.db"
    app.config['DATABASE'] = file_path

    if not os.path.exists('./backend/databases'):
        os.makedirs('./backend/databases')

    init_db()


    @app.teardown_appcontext
    def close_db(error):
        if hasattr(g, 'db'):
            g.db.close()

    return app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Initialize databases
def init_db():
    # Connect to the chats database and create the table if it doesn't exist
    with sqlite3.connect(chats_db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS chats (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL)''')

    with sqlite3.connect(users_db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        name TEXT NOT NULL)''')

    
    # Connect to the messages database and create the table if it doesn't exist
    with sqlite3.connect(messages_db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY,
                        chat_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        message TEXT NOT NULL,
                        FOREIGN KEY (chat_id) REFERENCES chats(id))''')        
        

  # Initialize the database when the module is imported

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
