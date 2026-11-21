from flask import Blueprint, render_template, redirect, url_for
from app.controller.database_collection_controller import getCategoriesCollection

# Route Blueprint
category_route = Blueprint('categories', __name__)

# Fetching all the products in the specific category
@category_route.route('/categories/<category_name>')
def category(category_name):
    categories_collection = getCategoriesCollection()
    products = list(categories_collection.find({"category": category_name}))

    for product in products:
        product['_id'] = str(product['_id'])

    return render_template('Components/categories/category.html', category_name=category_name, products=products)
