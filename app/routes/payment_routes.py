from flask import Blueprint, session, redirect, url_for, flash
import stripe
import os

payment_route = Blueprint("payment_route", __name__)
stripe.api_key =  os.getenv('stripe_api_key')

@payment_route.route("/payment")
def payment_page():
    cart = session.get('cart')
    if not cart or len(cart) == 0:
        flash("Cart is empty.", "warning")
        return redirect(url_for('cart_route.view_cart'))

    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    # Convert to cents (Stripe expects smallest currency unit)
    amount_in_cents = int(total_price)

    # Create Stripe Checkout Session
    session_stripe = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Sketchify Cart Purchase',
                    },
                    'unit_amount': amount_in_cents,
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=url_for('payment_route.success', _external=True),
        cancel_url=url_for('payment_route.cancel', _external=True),
    )

    return redirect(session_stripe.url)

@payment_route.route("/payment/success")
def success():
    session.pop('cart', None)  # Clear cart after success
    flash("✅ Payment successful! Thank you.", "success")
    return redirect(url_for("default_route.home_page"))

@payment_route.route("/payment/cancel")
def cancel():
    flash("Payment Canceled Try again..", "danger")
    return redirect(url_for("default_route.home_page"))
