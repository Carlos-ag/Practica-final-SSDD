from app import create_app
from app.routes import register_routes
import threading

app = create_app()
register_routes(app)

if __name__ == '__main__':
    # create thread to run the app
    t = threading.Thread(target=app.run)
    t.start()
    for i in range(10):
        print(i)


    
