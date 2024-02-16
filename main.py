from backend.authentification import create_app
from backend.authentification.routes import register_routes_authentification

from backend.chat_storage.routes import register_routes_chat

from backend.tcp import start_server_tcp

from frontend import create_web_app


import threading

authentification_app = create_app()
register_routes_authentification(authentification_app)
register_routes_chat(authentification_app)



if __name__ == '__main__':
    # create thread to run the app in the port 6789
    t = threading.Thread(target=authentification_app.run, kwargs={'port':6789})
    t.start()

    t2 = threading.Thread(target=start_server_tcp)
    t2.start()

    # run the frontend app
    create_web_app()


    