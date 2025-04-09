from functools import wraps
from flask import redirect, url_for, session, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function

def restricted(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401 # Return Unauthorized response
        return f(*args, **kwargs)
    return decorated_function