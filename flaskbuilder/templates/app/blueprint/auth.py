from flask import Blueprint, request, redirect, url_for, session, jsonify
from config import db
from werkzeug.security import check_password_hash
from app.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

# Superuser hardcoded
SUPERUSER = {
    "username": "admin",
    "password": "admin"
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == SUPERUSER['username'] and password == SUPERUSER['password']:
        access_token = create_access_token(identity=username)
        
        session['token'] = access_token
        session['username'] = username
        session['name'] = 'Super Admin'
        session['role']= 'Admin'
        session['email'] = 'superuser@superuser'
        
        return jsonify({
            "status": "success", 
            "message": "Login sukses", 
            "token": access_token,
            "user": {
                "username": username,
                "name": "Superuser",
                "email": "superuser@superuser"
            }
        }), 200
        
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        
        session['token'] = access_token
        session['username'] = user.username
        session['name'] = user.name
        session['role'] = user.role.name
        session['email'] = user.email
        
        return jsonify({
            "status": "success",
            "message": "Login sukses",
            "token": access_token,
            "user": {
                "username": user.username,
                "name": user.name,
                "email": user.email
            }
        }), 200
    return jsonify({"status": "error", "message": "Login gagal. Username atau password salah"}), 401

@auth_bp.route('/logout')
def logout():
    session.pop("token", None)
    return redirect(url_for('web.login'))
