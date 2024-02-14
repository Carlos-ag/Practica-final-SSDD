from backend.authentification import create_app
from backend.authentification.routes import register_routes
import threading

authentification_app = create_app()
register_routes(authentification_app)

if __name__ == '__main__':
    # create thread to run the app
    t = threading.Thread(target=authentification_app.run)
    t.start()

    