from config import db
from datetime import datetime, date

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(255))
    role_id = db.Column(db.String(100), db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<User {self.username}>'