from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import os
from app.controller.admin_controller import authenticate_admin
admin_route = Blueprint('admin_route', __name__)

# Admin credentials accessing 
admin_name = os.getenv("ADMIN_NAME")
admin_pass = os.getenv("ADMIN_PASS")

@admin_route.route("/admin-authenticate", methods=["POST"])
def admin_authentication():
    username = request.form['username']
    password = request.form['password']
    success, message = authenticate_admin(username, password)
    if success:
        session['admin_logged_in'] = True
        flash(message, "success")
        return redirect(url_for("admin_route.admin_dashboard"))
    else:
        flash(message, "danger")
        return redirect(url_for("admin_route.admin_login"))


@admin_route.route("/admin/dashboard")
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_route.admin_login'))
    
    # Example dummy data
    total_users = 50
    total_products = 20
    total_orders = 12
    
    return render_template(
        "Components/Admin/admin_dashboard.html",
        total_users=total_users,
        total_products=total_products,
        total_orders=total_orders,
    )

@admin_route.route("/admin/login")
def admin_login():
    return render_template('Components/Admin/admin_login.html')