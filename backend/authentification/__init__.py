from flask import Flask, g, current_app
from flask_cors import CORS
import sqlite3
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    file_path = os.path.abspath(os.getcwd())+"/backend/databases/users.db"
    app.config['DATABASE'] = file_path

    if not os.path.exists('./backend/databases'):
        os.makedirs('./backend/databases')

    with app.app_context():
        db_exists = os.path.isfile(file_path)
        db = get_db()

        if not db_exists:
            # The database file does not exist. Apply the schema.
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    @app.teardown_appcontext
    def close_db(error):
        if hasattr(g, 'db'):
            g.db.close()

    return app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Make sure to register close_db with the app to ensure it's called when cleaning up after a request
# Inside create_app(), add the line: app.teardown_appcontext(close_db)
