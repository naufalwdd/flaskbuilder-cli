from flask import Blueprint, render_template, jsonify, request
from app.models import User, Teacher, Student
from utils.decorators import jwt_protected
from werkzeug.security import generate_password_hash
from config import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
@jwt_protected
def register():
    data = request.get_json()

    # Data Umum
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    gender = data.get("gender")
    phone_number = data.get("phone_number")
    address = data.get("address")
    role_id = data.get("role_id")  # 'admin', 'teacher', 'student'

    if not all([username, email, password, name, role_id]):
        return jsonify({"status": "error", "message": "Data umum wajib diisi"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "Username sudah digunakan"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"status": "error", "message": "Email sudah digunakan"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        name=name,
        gender=gender,
        phone_number=phone_number,
        address=address,
        role_id=role_id
    )
    db.session.add(new_user)
    db.session.flush()  # Supaya user_id tersedia untuk relasi

    # Role-specific
    if role_id == "teacher":
        nip = data.get("nip")
        if not nip:
            return jsonify({"status": "error", "message": "NIP wajib diisi untuk guru"}), 400

        if Teacher.query.filter_by(nip=nip).first():
            return jsonify({"status": "error", "message": "NIP sudah digunakan"}), 400

        teacher = Teacher(
            user_id=username,
            nip=nip
        )
        db.session.add(teacher)

    elif role_id == "student":
        nis = data.get("nis")
        class_name = data.get("class_name")
        religion = data.get("religion")
        place_of_birth = data.get("place_of_birth")
        date_of_birth = data.get("date_of_birth")
        parent_name = data.get("parent_name")

        if not all([nis, class_name]):
            return jsonify({"status": "error", "message": "NIS dan kelas wajib diisi untuk siswa"}), 400

        if Student.query.filter_by(nis=nis).first():
            return jsonify({"status": "error", "message": "NIS sudah digunakan"}), 400

        student = Student(
            user_id=username,
            nis=nis,
            class_name=class_name,
            religion=religion,
            place_of_birth=place_of_birth,
            date_of_birth=date_of_birth,
            parent_name=parent_name
        )
        db.session.add(student)

    db.session.commit()
    return jsonify({"status": "success", "message": f"Registrasi {role_id} berhasil"}), 201

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