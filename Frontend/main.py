
from create_app import create_web_app
import threading
from python_functions.multicast import init_multicast_client
from python_functions.global_variables import global_variables_init

def main():
    global_variables_init()
    multicast_thread = threading.Thread(target=init_multicast_client)
    multicast_thread.start()
    create_web_app()
    

if __name__ == '__main__':
    main()