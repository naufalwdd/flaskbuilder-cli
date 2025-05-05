from flask import Flask
from config.config import Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_babel import Babel
from werkzeug.security import generate_password_hash
import logging

babel = Babel()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
jwt_blacklist = set()

class FrontendRequestFilter(logging.Filter):
    def filter(self, record):
        # Only allow logs that are NOT for frontend/static files
        msg = record.getMessage()
        frontend_extensions = ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.ttf', '.ico']
        frontend_paths = ['/static/', '/admin/static/']

        return not any(path in msg for path in frontend_paths) and not any(ext in msg for ext in frontend_extensions)

log = logging.getLogger('werkzeug')
log.addFilter(FrontendRequestFilter())

def create_app():
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, static_folder=static_path, static_url_path='/static' )
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    babel.init_app(app)
    
    from app.models.models import User
    
    migrate.init_app(app, db)
    
    from app import admin
    admin.init_app(app, db)
    
    # Register Blueprints
    from routes.register import register_routes
    register_routes(app)
    
    # seed default user
    with app.app_context():
        try:
            create_admin_user()
            
        except:
            print("Database is not ready...")

    return app

def create_admin_user():
    from app.models.models import User
    admin_user = User.query.filter_by(username='admin').first()

    if admin_user is None:
        hashed_password = generate_password_hash('admin')  # Change to a secure password
        new_user = User(
            username='admin',
            email='admin@super.com',
            password=hashed_password,
            name='Super Admin',
            gender='male',
            phone_number='-',
            address='-',
            role_id='admin'
        )
        
        db.session.add(new_user)
        db.session.commit()

        print("Admin user created with username 'admin' and password 'admin_password'")
    else:
        print("Admin user already exists, skipping creation.")