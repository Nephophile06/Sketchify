from flask import Flask,flash, Blueprint, render_template, request, redirect, url_for
from app import bcrypt
import os                                       #environment variables access kore
import re
from pymongo import MongoClient
from app.controller.user_controller import register_user_controller, login_user_controller, update_user_controller, delete_user_controller, generate_backup_code, send_backup_code_email
from app.controller.database_collection_controller import getCategoriesCollection, getFeaturedProductsCollection
from flask import session
user_route = Blueprint("user_route", __name__)



@user_route.route("/login")
def login():
    return render_template('Components/login.html')

@user_route.route("/register")
def register():
    return render_template('Components/register.html')

@user_route.route("/user-dashboard")
def user_dashboard():
    return render_template("Components/userDashboard.html")

@user_route.route("/edit-user-profile")
def edit_user_profile():
    return render_template("Components/editUserProfile.html")

@user_route.route("/user_login", methods=["POST"])
def user_login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    success, message = login_user_controller(data)
    flash(message, "success" if success else "danger")

    return redirect(url_for("default_route.home_page" if success else "user_route.login"))

@user_route.route("/user_register", methods=["POST"])
def user_register():
    backup_code = generate_backup_code()
    
    data = {
        'full_name' : request.form['name'],
        'username' : request.form['username'],
        'gender' : request.form['gender'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'backup_code': backup_code
    } 

    # Checking for the password length
    if len(data['password']) <= 6:
        flash("Password must be more than 6 characters.", "danger")
        return redirect(url_for("user_route.register"))
    
    success, message = register_user_controller(data)
    send_backup_code_email(data['email'], backup_code)

    # Flash Message
    flash(message, "success" if success else "danger" )

    #redirect
    return redirect(url_for("user_route.login" if success else "user_route.register"))




@user_route.route("/search")
def search_products():
    query = request.args.get("query", "").strip()
    
    if not query:
        flash("Please enter a search term.", "danger")
        return redirect(url_for("default_route.home_page"))

    products_collection = getCategoriesCollection()
    featured_prodcuts_collection = getFeaturedProductsCollection()
    # Escape special regex characters
    safe_query = re.escape(query)

    # Case-insensitive partial match
    products = list(products_collection.find({
        "name": {"$regex": safe_query, "$options": "i"}
    }))
    
    fproducts = list(featured_prodcuts_collection.find({
        "name" : {"$regex": safe_query, "$options" : "i"}
    }))

    return render_template("Components/Search/search_results.html", products=products, fproducts = fproducts ,query=query)


@user_route.route("/logout")
def logout():
    session.pop('user')
    success = True
    flash("You have been logged out", "success" if success else "danger")
    return redirect(url_for('default_route.home_page'))  


@user_route.route("/updateInfo", methods = ["POST"])
def updateInfo():
    data = {
        'email': request.form['email'],
        'password': request.form['new_password']
    }

    success, message = update_user_controller(data)
    flash(message, "success" if success else "danger")
    return redirect(url_for("user_route.user_dashboard" if success else "user_route.edit_user_profile"))

@user_route.route("/delete-user" , methods = ["POST"])
def deleteUser():
    data = {
        'email' : session['user']['email']
    }

    success, message = delete_user_controller(data)
    flash(message, "success" if success else "danger")
    return redirect(url_for("default_route.home_page" if success else "user_route.edit_user_profile"))