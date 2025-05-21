from flask import Blueprint, session, redirect, url_for, flash, render_template, request
import stripe
import os
from app.controller.order_controller import save_order

payment_route = Blueprint("payment_route", __name__)
stripe.api_key = os.getenv('stripe_api_key')

@payment_route.route("/payment-card")
def payment_card():
    cart = session.get('cart')
    user = session.get('user')
    
    if not user:
        flash("Please log in to proceed with payment.", "warning")
        return redirect(url_for("user_route.login"))

    if not cart or len(cart) == 0:
        flash("Cart is empty.", "warning")
        return redirect(url_for('cart_route.view_cart'))

    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    amount_in_poisha = int(total_price * 100)  # Stripe needs the amount in the smallest currency unit

    # Create a Stripe Checkout session
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
        success_url=url_for('payment_route.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('payment_route.cancel', _external=True),
        client_reference_id=user.get('_id'),  # Optional: track user
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
    cart = session.get('cart')
    user = session.get('user')
    session_id = request.args.get("session_id")  # ✅ Capture session_id from URL

    if not cart or not user or not session_id:
        flash("Session expired or cart missing.", "danger")
        return redirect(url_for("default_route.home_page"))

    try:
        # Retrieve the Stripe session
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        transaction_id = checkout_session.payment_intent  # ✅ Actual Stripe Payment Intent ID
    except Exception as e:
        flash(f"Failed to verify payment: {str(e)}", "danger")
        return redirect(url_for("default_route.home_page"))

    # Save the order to DB
    save_order(user, cart, payment_method="Stripe", transaction_id=transaction_id)

    # Clear cart after successful order
    session.pop('cart', None)
    flash("✅ Payment successful! Thank you.", "success")
    return redirect(url_for("default_route.home_page"))


@payment_route.route("/payment/cancel")
def cancel():
    flash("❌ Payment was canceled. Try again.", "danger")
    return redirect(url_for("payment_route.payment_page"))
