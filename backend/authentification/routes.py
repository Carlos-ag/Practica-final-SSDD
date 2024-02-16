from flask import request, jsonify, g
import hashlib
from . import get_db
import sqlite3

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def register_routes_authentification(app):
    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM user WHERE username = ?', (data['username'],))
        user = cursor.fetchone()
        if user:
            return jsonify(success=False, message="Username already exists."), 409
        hashed_password = hash_password(data['password'])
        cursor.execute('INSERT INTO user (username, password, name) VALUES (?, ?, ?)',
                       (data['username'], hashed_password, data['name']))
        db.commit()
        return jsonify(success=True), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM user WHERE username = ?', (data['username'],))
        user = cursor.fetchone()
        if not user or not verify_password(user['password'], data['password']):
            return jsonify(success=False, message="Invalid username or password."), 401
        return jsonify(success=True), 200

# Remember to import get_db from your __init__.py or wherever it's defined
