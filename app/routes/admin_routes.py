from flask import Blueprint, render_template

admin_route = Blueprint('admin_route', __name__)

@admin_route.route("/admin/login")
def admin_login():
    return render_template('Components/Admin/admin_login.html')