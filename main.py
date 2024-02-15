from backend.authentification import create_app
from backend.authentification.routes import register_routes

from frontend import create_web_app

import threading

authentification_app = create_app()
register_routes(authentification_app)

if __name__ == '__main__':
    # create thread to run the app in the port 6789
    t = threading.Thread(target=authentification_app.run, kwargs={'port':6789})
    t.start()

    # run the frontend app
    create_web_app()


    