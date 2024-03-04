from api import create_app
from api.routes import register_routes_authentification
from api.routes import register_routes_chat

from tcp import create_tcp_app


import threading

def main():
    authentification_app = create_app()
    register_routes_authentification(authentification_app)
    register_routes_chat(authentification_app)

    print("TCP server starting...")
    thread_tcp = threading.Thread(target=create_tcp_app)
    thread_tcp.start()

    print("Authentification server starting...")
    thread_authentification = threading.Thread(target=authentification_app.run, kwargs={'port':6789})
    thread_authentification.start()






if __name__ == '__main__':
    main()
