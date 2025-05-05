import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecret')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'mysecret')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]
    DATABASE_PATH = os.path.join(os.path.join(f"{str(Path().absolute())}", "database"), 'app.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Appbuilder Configuration
    APP_NAME = "Admin Panel"
    AUTH_TYPE = 1  # 1 means database authentication (login via User model)
    AUTH_ROLE_ADMIN = 'admin'
    AUTH_ROLE_PUBLIC = 'public'