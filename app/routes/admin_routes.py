from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import os
from app.controller.admin_controller import authenticate_admin
from app.controller.database_collection_controller import getUsersCollection, getCategoriesCollection
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
    else:
        # real user count from the database
        users_collection = getUsersCollection()
        total_users = users_collection.find()
        total_users = list(total_users)
        
        count = 0
        for user in total_users:
            count += 1
            user['_id'] = str(user['_id'])
            
            
        # Real categories count from the database
        categories_collection = getCategoriesCollection()
        total_category = categories_collection.find()
        total_category = list(total_category)
        
        countC = 0
        for category in total_category:
            countC += 1
            category['_id'] = str(category['_id'])
        return render_template(
            "Components/Admin/dashboard.html",
            total_users = count,
            total_products = countC,
            total_orders = 0
        )
    

@admin_route.route("/admin/login")
def admin_login():
    return render_template('Components/Admin/admin_login.html')

