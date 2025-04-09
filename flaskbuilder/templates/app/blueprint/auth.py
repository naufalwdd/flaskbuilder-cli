from flask import Blueprint, request, redirect, url_for, session, jsonify
from config import db
from werkzeug.security import check_password_hash
from app.models.user import User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

# Superuser hardcoded
SUPERUSER = {
    "username": "admin",
    "password": "superpassword123"
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == SUPERUSER['username'] and password == SUPERUSER['password']:
        return jsonify({"status": "success", "message": "Login sukses"}), 200
        
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return jsonify({
            "status": "success",
            "message": "Login sukses",
            "user": {
                "username": user.username,
                "name": user.name,
                "email": user.email
            }
        }), 200
    return jsonify({"status": "error", "message": "Login gagal. Username atau password salah"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not username or not email or not password:
        return jsonify({"status": "success", "message": "Semua field wajib diisi"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "warning", "message": "Username sudah terdaftar"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"status": "warning", "message": "Email sudah terdaftar"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        name=name
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "Registrasi berhasil"}), 201
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user_id from session
    return redirect(url_for('main.login'))
