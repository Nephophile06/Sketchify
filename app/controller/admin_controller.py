# controllers/admin_controller.py
import os
from app.controller.database_collection_controller import getUsersCollection, getCategoriesCollection, getOrderedProductsCollection
from pymongo import DESCENDING, ASCENDING
import io
import csv
from flask import request, render_template

admin_name = os.getenv("ADMIN_NAME")
admin_pass = os.getenv("ADMIN_PASS")

def authenticate_admin(username, password):
    if username == admin_name and password == admin_pass:
        return True, "Successfully Logged in!!"
    else:
        return False, "Invalid Username or Password"
def user_list_controller():
    users_collection = getUsersCollection()
    users_data = users_collection.find()
    users_data = list(users_data)
    
    for user in users_data:
        user['_id'] = str(user['_id'])
         
    return users_data

def product_list_controller():
    products_collection = getCategoriesCollection()
    products_data = products_collection.find()
    products_data = list(products_data)
    
    for product in products_data:
        product['_id'] = str(product['_id'])
    return products_data

def orders_list_controller():
    orders_collection = getOrderedProductsCollection()

    # Params
    page = int(request.args.get("page", 1))
    per_page = 10
    search = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "created_at")
    order = request.args.get("order", "desc")

    # Sorting direction
    sort_direction = DESCENDING if order == "desc" else ASCENDING

    # Search filter
    filter_query = {
        "$or": [
            {"user_name": {"$regex": search, "$options": "i"}},
            {"user_email": {"$regex": search, "$options": "i"}},
            {"payment_method": {"$regex": search, "$options": "i"}},
        ]
    } if search else {}

    total_orders = orders_collection.count_documents(filter_query)
    orders_cursor = (
        orders_collection.find(filter_query)
        .sort(sort_by, sort_direction)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )
    orders = list(orders_cursor)

    for order in orders:
        order['_id'] = str(order['_id'])

    return render_template(
        "Components/Admin/orders-list.html",
        orders=orders,
        page=page,
        total_pages=(total_orders + per_page - 1) // per_page,
        search=search,
        sort_by=sort_by,
        order=order
    )
