from main import app
from app.models import db, Role

with app.app_context():
    db.create_all()

    roles = ['Admin', 'Teacher', 'Finance', 'Student']
    for role_name in roles:
        existing = Role.query.filter_by(name=role_name).first()
        if not existing:
            db.session.add(Role(name=role_name, id=role_name.lower()))
    
    db.session.commit()
    print("✅ Master roles berhasil diinject.")