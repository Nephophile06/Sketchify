from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.controller.database_collection_controller import getOrderedProductsCollection
from bson.objectid import ObjectId
from flask_mail import Message
from app import mail

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




@order_route.route('/send-invoice/<order_id>')
def send_invoice(order_id):
    user = session.get('user')
    if not user:
        flash("Please log in to send invoices.", "warning")
        return redirect(url_for("user_route.login"))

    orders_collection = getOrderedProductsCollection()
    order = orders_collection.find_one({"_id": ObjectId(order_id)})

    if not order or order.get("user_name") != user.get("username"):
        flash("Invoice not found or access denied.", "danger")
        return redirect(url_for("order_route.orders_by_username"))

    # Render the invoice HTML
    html_body = render_template("Components/Order/invoice.html", order=order)

    # Compose email
    msg = Message(
        subject=f"Your Sketchify Invoice - Order #{str(order['_id'])[:6]}",
        recipients=[user["email"]],
        html=html_body
    )

    # Send email
    try:
        mail.send(msg)
        flash("Invoice sent to your email!", "success")
    except Exception as e:
        print("Mail Error:", e)
        flash("Failed to send email. Please try again later.", "danger")

    return redirect(url_for("order_route.orders_by_username"))
