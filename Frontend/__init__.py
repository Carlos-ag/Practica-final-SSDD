import eel
import os
from os import getcwd
from backend.chat_storage import get_chat_information, get_chat_history, create_chat, add_message_to_chat

def create_web_app():
    eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')

    @eel.expose
    def create_chat_in_database(chat_name):
        chat_id = create_chat(chat_name)
        return chat_id

    @eel.expose
    def get_chat_info(chat_id):
        chat_info = get_chat_information(chat_id)
        return chat_info

    @eel.expose
    def get_chat_history_from_database(chat_id):
        chat_history = get_chat_history(chat_id)
        return chat_history


    eel.start('html/login.html')