from flask import Blueprint, session, redirect, url_for, flash, render_template
import stripe
import os

payment_route = Blueprint("payment_route", __name__)
stripe.api_key =  os.getenv('stripe_api_key')

@payment_route.route("/payment-card")
def payment_card():
    cart = session.get('cart')
    if not cart or len(cart) == 0:
        flash("Cart is empty.", "warning")
        return redirect(url_for('cart_route.view_cart'))

    # Total price in BDT
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    # Stripe expects amount in the smallest unit, so convert taka → poisha
    amount_in_poisha = int(total_price * 100)

    session_stripe = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'bdt',  
                    'product_data': {
                        'name': 'Sketchify Cart Purchase',
                    },
                    'unit_amount': amount_in_poisha,  
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=url_for('payment_route.success', _external=True),
        cancel_url=url_for('payment_route.cancel', _external=True),
    )

    return redirect(session_stripe.url)

@payment_route.route("/payment-page")
def payment_page():
    cart = session.get('cart')
    user = session.get("user")
    if not user:
        return redirect(url_for("user_route.login"))
    
    if not cart:
        return "Cart is empty"

    return render_template("Components/Payment/payment_page.html", cart=cart, user=user)

    

@payment_route.route("/payment/success")
def success():
    session.pop('cart', None)  # Clear cart after success
    flash("✅ Payment successful! Thank you.", "success")
    return redirect(url_for("default_route.home_page"))

@payment_route.route("/payment/cancel")
def cancel():
    flash("Payment Canceled Try again..", "danger")
    return redirect(url_for("payment_route.payment_page"))
