from flask import Blueprint, jsonify
from app.models import User
from utils.decorators import jwt_protected

user_bp = Blueprint('user_api', __name__)

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