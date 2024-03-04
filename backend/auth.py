from flask_httpauth import HTTPBasicAuth
from authentification import get_db
import hashlib
from flask import g


auth = HTTPBasicAuth()

def check_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

@auth.verify_password
def verify_password(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user and check_password(user['password'], password):
        g.user = user
        return True