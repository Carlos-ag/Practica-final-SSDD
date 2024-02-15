import eel
import random
from datetime import datetime
import os
from os import getcwd

def create_web_app():
    eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')

    @eel.expose
    def send_tcp_message(message):
        print(f"Sending message: {message}")

    eel.start('html/login.html')