# routes/auth.py
from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.is_locked = True
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()
        return jsonify({'error': 'Invalid credentials'}), 401
    if user.is_locked:
        return jsonify({'error': 'Account locked'}), 403

    user.failed_login_attempts = 0
    db.session.commit()

    token = create_access_token(identity={'id': user.id, 'role': user.role, 'email': user.email})
    return jsonify({
        'token': token,
        'user': {'id': user.id, 'role': user.role, 'email': user.email}
    })
