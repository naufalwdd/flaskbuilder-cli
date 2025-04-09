from config import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'