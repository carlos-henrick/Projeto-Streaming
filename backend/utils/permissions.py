from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"error": "Acesso negado"}), 403

        return fn(*args, **kwargs)
    return wrapper
