from flask import Blueprint, render_template, redirect, url_for
from pymongo import MongoClient
import os

# Route Blueprint
category_route = Blueprint('categories', __name__)


# database configuration
def categoryCollection():
    client = MongoClient(os.getenv("MONGO_URI"))
    main_database = client['Sketchify']
    catgories_collection = main_database['Categories']

    return catgories_collection

# Fetching all the products in the specific category
@category_route.route('/categories/<category_name>')
def category(category_name):

    # Fetching all the products in the specific category
    categories_collection = categoryCollection()


    products = categories_collection.find({"category": category_name})
    products = list(products)

    for product in products:
        product['_id'] = str(product['_id'])

    return render_template('Components/categories/category.html',category_name=category_name, products=products)