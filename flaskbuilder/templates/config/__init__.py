import sqlite3
from flask import Flask, g
from config.config import Config
from database.db import close_db
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, static_folder=static_path, static_url_path='/static' )
    app.config.from_object(Config)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    from app.models.user import User
    migrate.init_app(app, db)
    
    
    # Register Blueprints
    from routes.register import register_routes
    register_routes(app)

    # Ensure database is closed after each request
    app.teardown_appcontext(close_db)
    
    return app