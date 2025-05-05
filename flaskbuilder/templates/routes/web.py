from flask import Blueprint, render_template, session
from utils.decorators import protected
import os

template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
web_bp = Blueprint('web', __name__, template_folder=template_path)

@web_bp.route('/admin-login')
def admin_login():
    return render_template('admin/login.html')
    
@web_bp.route('/home')
@protected
def home():
    return render_template('home.html', context={
        'page_title': 'Home',
        'user_data': session
    })

@web_bp.route('/')
def login():
    return render_template('index.html', context={
        'page_title': 'Login'
    })