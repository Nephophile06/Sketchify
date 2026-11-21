from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from app.controller.database_collection_controller import getFeaturedProductsCollection, getFeedbackCollection

default_route = Blueprint("default_route", __name__)

@default_route.route("/")
def home_page():
    featured_collection = getFeaturedProductsCollection()
    
    featured_collection_data = featured_collection.find()
    featured_collection_data = list(featured_collection_data)
    
    for featured_products in featured_collection_data:
        featured_products['_id'] = str(featured_products['_id'])
    
    return render_template('homepage.html', featured_products = featured_collection_data)

@default_route.route("/categories")
def categories():
    return render_template("categories.html")

@default_route.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email", "").strip()
    suggestion = request.form.get("suggestion", "").strip()

    if not email:
        flash("Please provide a valid email address.", "danger")
        return redirect(url_for("default_route.home_page"))

    try:
        feedback_collection = getFeedbackCollection()
        feedback_collection.insert_one({
            "email": email,
            "suggestion": suggestion,
            "created_at": datetime.now()
        })
        flash("Thank you for sharing your thoughts and subscribing!", "success")
    except Exception as e:
        print("Feedback error:", e)
        flash("Something went wrong. Please try again.", "danger")

    return redirect(url_for("default_route.home_page"))