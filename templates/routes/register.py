from routes.web import web_bp
from app.blueprint.user import user_bp
from app.blueprint.auth import auth_bp

def register_routes(app):
    app.register_blueprint(web_bp)
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')