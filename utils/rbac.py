# utils/rbac.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def require_role(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = get_jwt_identity()
            if user['role'] != required_role:
                return jsonify({'error': 'Access denied'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
