from flask import Flask, Blueprint, render_template
from app.controller.database_collection_controller import getFeaturedProductsCollection

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