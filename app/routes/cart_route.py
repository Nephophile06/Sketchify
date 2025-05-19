from flask import Blueprint, session, redirect, url_for, request

cart_route = Blueprint('cart_route', __name__)

@cart_route.route("/add-to-cart/<product_id>")
def add_to_cart(product_id):
    cart = session.get('cart', {})

    # Increment quantity or set to 1
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    session['cart'] = cart
    return redirect(request.referrer or url_for('default_route.home_page'))
