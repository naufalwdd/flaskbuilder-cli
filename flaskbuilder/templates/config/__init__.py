from flask import Flask, g, session
from config.config import Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
jwt_blacklist = set()

def create_app():
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, static_folder=static_path, static_url_path='/static' )
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    
    from app.models.models import User, Role, Teacher, Student, Attendance, SPP, TeacherSchedule, StudentReport
    
    migrate.init_app(app, db)
    
    # Register Blueprints
    from routes.register import register_routes
    register_routes(app)

    return app