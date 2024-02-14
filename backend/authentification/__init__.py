from flask import Flask
from .models import db
from flask_cors import CORS

import os



def create_app():
    app = Flask(__name__)
    CORS(app)
    file_path = os.path.abspath(os.getcwd())+"/backend/databases/users.db"


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app
