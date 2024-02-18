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


    

    # init at port 6788
    # import from os where we are executing this, and then inside that folder, go to frontend/web/html/login.html
    # print(f'{os.path.dirname(os.path.realpath(__file__))}/web/html/login.html') 
    # eel.start('/Users/carlos/Documents/SSDD/Practica final SSDD/frontend/python_functions/web/html/login.html', port=6788)
    eel.start('html/login.html')