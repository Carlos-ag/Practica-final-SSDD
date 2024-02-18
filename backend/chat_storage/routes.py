from flask import request, jsonify, g
import hashlib
import sqlite3
from . import get_chat_information, get_chat_history, create_chat, save_message_to_db


def register_routes_chat(app):
    # get chat information, get_chat_information(chat_id) -> chat_info
    # use a post
    @app.route('/get_chat_information', methods=['POST'])
    def get_chat_information_api():
        data = request.json
        chat_info = get_chat_information(data['chat_id'])
        if not chat_info:
            return jsonify(success=False, message="Chat not found."), 404
        return jsonify(success=True, chat_info=chat_info), 200 

    
    # get chat history, get_chat_history(chat_id) -> list of messages

    @app.route('/get_chat_history', methods=['POST'])
    def get_chat_history_api():
        data = request.json
        chat_history = get_chat_history(data['chat_id'])
        if not chat_history:
            return jsonify(success=False, message="Chat not found."), 404
        return jsonify(success=True, chat_history=chat_history), 200

    # create chat, create_chat(chat_name) -> chat_id
    @app.route('/create_chat', methods=['POST'])
    def create_chat_api():
        data = request.json
        chat_id = create_chat(data['chat_name'])
        return jsonify(success=True, chat_id=chat_id), 201
