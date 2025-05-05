from flask_admin.contrib.sqla import ModelView
from flask import redirect, session
from wtforms.fields import SelectField, PasswordField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin, AdminIndexView, expose
from app.models.models import User, Role

# Custom AdminIndexView
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not session.get('username'):
            return redirect('/?login=admin')
        return super().index()

class UserAdmin(ModelView):
    def is_accessible(self):
        return session.get('username')

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/?login=admin')
    
    form_columns = [
        'username', 'password', 'email', 'name',
        'gender', 'phone_number', 'address', 'role_id'
    ]

    form_overrides = dict(
        gender=SelectField,
        password=PasswordField,
        role_id=SelectField
    )

    def _get_role_choices(self):
        from app.models.models import Role  # pastikan import Role di sini
        return [(r.id, r.name) for r in self.session.query(Role).all()]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.gender.choices = [('male', 'Laki-Laki'), ('female', 'Perempuan')]
        form.role_id.choices = self._get_role_choices()
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.gender.choices = [('male', 'Laki-Laki'), ('female', 'Perempuan')]
        form.role_id.choices = self._get_role_choices()
        return form

    def on_model_change(self, form, model, is_created):
        raw_password = form.password.data

        if is_created:
            if raw_password:
                model.password = generate_password_hash(raw_password)
        else:
            user_in_db = self.session.query(self.model).get(model.username)
            if raw_password and not check_password_hash(user_in_db.password, raw_password):
                model.password = generate_password_hash(raw_password)
            else:
                model.password = user_in_db.password
                
class RoleAdmin(ModelView):
    def is_accessible(self):
        return session.get('username')

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/?login=admin')
    
    form_columns = [
        'id', 'name'
    ]
                
def init_app(app, db):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())

    # Tambahkan views
    admin.add_view(UserAdmin(User, db.session, name='Users'))
    admin.add_view(RoleAdmin(Role, db.session, name='Roles'))