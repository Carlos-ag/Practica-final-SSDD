from flask import request, jsonify, g
import hashlib
import sqlite3
from . import get_chat_information, get_chat_history, create_chat, save_message_to_db
from auth import auth


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
        print(raw_chat_history)
        if not raw_chat_history:
            return jsonify(success=False, message="Chat not found."), 404

        # Convert each tuple in the chat history to a dictionary
        chat_history = [
            {
                'message_id': message[0],
                'chat_id': message[1],
                'user_id': message[2],
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
