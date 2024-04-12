from flask import request, jsonify, g
import hashlib
from . import get_db
import sqlite3


from . import get_chat_information, get_chat_history, create_chat, save_message_to_db


from flask_httpauth import HTTPBasicAuth
from . import get_db
import hashlib
from flask import g


auth = HTTPBasicAuth()


def check_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def get_username_from_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
    user = cursor.fetchone()
  
    return user['name']

@auth.verify_password
def verify_password(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user and check_password(user['password'], password):
        g.user = user
        return True


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def register_routes_authentification(app):
    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM user WHERE username = ?', (data['username'],))
        user = cursor.fetchone()
        if user:
            return jsonify(success=False, message="Username already exists."), 409
        hashed_password = hash_password(data['password'])
        cursor.execute('INSERT INTO user (username, password, name) VALUES (?, ?, ?)',
                    (data['username'], hashed_password, data['name']))
        db.commit()
        user_id = cursor.lastrowid  # Get the last inserted id
        return jsonify(success=True, user_id=user_id), 201


    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM user WHERE username = ?', (data['username'],))
        user = cursor.fetchone()
        if not user or not verify_password(user['password'], data['password']):
            return jsonify(success=False, message="Invalid username or password."), 401
        # Assuming 'id' is the column name for the user identifier in your database
        user_id = user['id']  # Adjust this line based on how your user dictionary is structured
        return jsonify(success=True, user_id=user_id), 200

    # api endpoint to exchange the user_id for the username: get_username_from_id(user_id)
    @app.route('/api/get_username_from_id/<user_id>', methods=['GET'])
    def get_username_from_id_api(user_id):
        username = get_username_from_id(user_id)
        return jsonify(success=True, username=username), 200








# _________________________________________________________________________________________


def register_routes_chat(app):
    # get chat information, get_chat_information(chat_id) -> chat_info
    # use a post
    @auth.login_required
    @app.route('/api/get_chat_information', methods=['POST'])
    def get_chat_information_api():
        data = request.json
        chat_info = get_chat_information(data['chat_id'])
        if not chat_info:
            return jsonify(success=False, message="Chat not found."), 404
        return jsonify(success=True, chat_info=chat_info), 200 

    
    # get chat history, get_chat_history(chat_id) -> list of messages

    @auth.login_required
    @app.route('/api/get_chat_history', methods=['POST'])
    def get_chat_history_api():
        data = request.json
        raw_chat_history = get_chat_history(data['chat_id'])
        if not raw_chat_history:
            return jsonify(success=False, message="Chat not found."), 404

        # Convert each tuple in the chat history to a dictionary
        chat_history = [
            {
                'message_id': message[0],
                'chat_id': message[1],
                'user_id': message[2],
                'username': get_username_from_id(message[2]),
                'content': message[3]
            } for message in raw_chat_history
        ]

        return jsonify(success=True, chat_history=chat_history), 200

    # create chat, create_chat(chat_name) -> chat_id
    @auth.login_required
    @app.route('/api/create_chat', methods=['POST'])
    def create_chat_api():
        data = request.json
        chat_id = create_chat(data['chat_name'])
        return jsonify(success=True, chat_id=chat_id), 201
