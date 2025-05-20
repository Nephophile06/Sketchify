from flask import Blueprint, session, redirect, url_for, request, render_template
from bson.objectid import ObjectId
from app.controller.database_collection_controller import getCategoriesCollection, getFeaturedProductsCollection
cart_route = Blueprint('cart_route', __name__)

@cart_route.route("/add-to-cart/<product_id>")
def add_to_cart(product_id):
    products_collection = getCategoriesCollection()
    featured_collection = getFeaturedProductsCollection()

    # Try to find in products
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    
    # If not found, try in featured products
    if not product:
        product = featured_collection.find_one({"_id": ObjectId(product_id)})
    
    if not product:
        return redirect(request.referrer or url_for('default_route.home_page'))

    cart = session.get('cart', {})
    product_id_str = str(product['_id'])

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'name': product['name'],
            'price': float(product['price']),
            'quantity': 1
        }

    session['cart'] = cart
    return redirect(request.referrer or url_for('default_route.home_page'))



@cart_route.route("/cart")
def view_cart():
    cart = session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template("Components/cart/cart.html", cart=cart, total=total_price)



@cart_route.route("/update-quantity", methods=["POST"])
def update_quantity():
    product_id = request.form.get("product_id")
    action = request.form.get("action")
    cart = session.get("cart", {})

    if product_id in cart:
        if action == "increase":
            cart[product_id]["quantity"] += 1
        elif action == "decrease":
            cart[product_id]["quantity"] -= 1
            if cart[product_id]["quantity"] <= 0:
                del cart[product_id]

    session["cart"] = cart
    return redirect(url_for("cart_route.view_cart"))
