from flask import Blueprint, render_template, jsonify
from database.db import get_db, map_data
from utils.decorators import restricted

user_bp = Blueprint('user', __name__)

@user_bp.route('/get')
@restricted
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, username, email FROM users')
    users = cursor.fetchall()
    
    user_data = map_data(users)
    
    cursor.close()
    
    return jsonify(user_data)