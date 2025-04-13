from functools import wraps
import traceback
from flask import redirect, url_for, session, jsonify
from flask_jwt_extended import verify_jwt_in_request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('web.login'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function

def restricted(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'message': 'Unauthorized'}), 401 # Return Unauthorized response
        return f(*args, **kwargs)
    return decorated_function

def jwt_protected(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = session.get("token")
        print(token)
        if token:
            try:
                verify_jwt_in_request(token=token)
            except Exception as e:
                return jsonify({"message": "Invalid session token"}), 401
        else:
            try:
                verify_jwt_in_request()
            except Exception:
                return jsonify({"message": "Missing or invalid token"}), 401
        return fn(*args, **kwargs)
    return wrapper