import eel
import os
from os import getcwd
from python_functions.tcp import send_tcp_message

import os
from python_functions.multicast import change_multicast_listening_port
import threading


def create_web_app():
    eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')


    @eel.expose
    def send_tcp_message_eel(chat_id, user_id, message):
        send_tcp_message(message, chat_id, user_id)
    
    @eel.expose
    def change_multicast_listening_port_eel(port):
        change_multicast_listening_port(port)
    

    
    port_file_name = 'frontend/port_eel.txt'
    with open(port_file_name, 'r') as file:
        port = int(file.read())
    with open(port_file_name, 'w') as file:
        file.write(str(port+1))
    
    eel.start('html/login.html', port=port)