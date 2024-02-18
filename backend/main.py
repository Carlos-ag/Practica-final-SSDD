from authentification import create_app
from authentification.routes import register_routes_authentification
from chat_storage.routes import register_routes_chat

from tcp import start_server_tcp


import threading

def main():
    authentification_app = create_app()
    register_routes_authentification(authentification_app)
    register_routes_chat(authentification_app)

    # create thread to run the app in the port 6789
    thread_authentification = threading.Thread(target=authentification_app.run, kwargs={'port':6789})
    thread_authentification.start()

    thread_tcp = threading.Thread(target=start_server_tcp)
    thread_tcp.start()





if __name__ == '__main__':
    main()
