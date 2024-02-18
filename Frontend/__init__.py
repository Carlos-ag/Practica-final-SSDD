import eel
import os
from os import getcwd
from frontend.my_python_code.tcp import send_tcp_message
from frontend.my_python_code.global_variables import global_variables_init
import os
from frontend.my_python_code.multicast import multicast_client

def create_web_app():
    eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')

    global_variables_init()

    # start the multicast client in a new thread
    t = threading.Thread(target=multicast_client)
    t.start()
    

    @eel.expose
    def send_tcp_message_eel(chat_id, user_id, message):
        send_tcp_message(message, chat_id, user_id)

        
    

    # init at port 6788
    # import from os where we are executing this, and then inside that folder, go to frontend/web/html/login.html
    # print(f'{os.path.dirname(os.path.realpath(__file__))}/web/html/login.html') 
    # eel.start('/Users/carlos/Documents/SSDD/Practica final SSDD/frontend/my_python_code/web/html/login.html', port=6788)
    eel.start('html/login.html')