from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.controller.database_collection_controller import getOrderedProductsCollection
from bson.objectid import ObjectId

order_route = Blueprint('order_route', __name__)

@order_route.route("/orders")
def orders_by_username():
    # Check if the user is logged in
    user = session.get('user')
    if not user:
        flash("Please log in to view your orders.", "warning")
        return redirect(url_for("user_route.login"))

    username = user.get("username")  # ✅ Get username from session

    orders_collection = getOrderedProductsCollection()

    # Fetch user's orders using the username from session
    user_orders = list(orders_collection.find({"user_name": username}))

    return render_template('Components/Order/user_order.html', orders=user_orders, username=username)

@order_route.route('/print-invoice/<order_id>')
def print_invoice(order_id):
    user = session.get('user')
    if not user:
        flash("Please log in to view invoices.", "warning")
        return redirect(url_for("user_route.login"))

    orders_collection = getOrderedProductsCollection()

    try:
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
    except:
        flash("Invalid order ID.", "danger")
        return redirect(url_for("order_route.orders_by_username"))

    if not order or order.get("user_name") != user.get("username"):
        flash("Invoice not found or access denied.", "danger")
        return redirect(url_for("order_route.orders_by_username"))

    return render_template("Components/Order/invoice.html", order=order)