from flask import Blueprint, render_template, jsonify, request
from app.models import User, Teacher, Student
from utils.decorators import jwt_protected
from werkzeug.security import generate_password_hash
from config import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/list', methods=['GET'])
@jwt_protected
def get_users():
    users = User.query.all()
    user_list = [
        {
            **{col.name: getattr(u, col.name) for col in u.__table__.columns},
            "role": u.role.name if u.role else None
        }
        for u in users
    ]
    return jsonify(user_list), 200