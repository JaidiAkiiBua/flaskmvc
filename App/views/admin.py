# App/views/admin.py
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request, flash, Blueprint
from flask_admin import Admin
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from App.models import db, User
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

class AdminView(ModelView):
    def is_accessible(self):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user and user.role == 'admin':
                return True
            flash("Admins only!", "danger")
        except Exception:
            flash("Login required", "danger")
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_views.login_page', next=request.url))

def setup_admin(app):
    admin = Admin(app, name='FlaskMVC', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

@admin_views.route('/admin_index')
@jwt_required()
def admin_index():
    return render_template('admin/index.html')