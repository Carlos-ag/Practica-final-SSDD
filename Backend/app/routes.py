from flask import request, jsonify
from .models import db, User
import hashlib

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def register_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        print
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return jsonify(success=False, message="Username already exists."), 409
        hashed_password = hash_password(data['password'])
        new_user = User(username=data['username'], password=hashed_password, name=data['name'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(success=True), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if not user or not verify_password(user.password, data['password']):
            return jsonify(success=False, message="Invalid username or password."), 401
        return jsonify(success=True), 200
