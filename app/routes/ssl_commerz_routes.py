import requests
import uuid
from flask import Blueprint, session, redirect, url_for, request, flash

sslcommerz_route = Blueprint("sslcommerz_route", __name__)

@sslcommerz_route.route("/pay")
def pay_with_sslcommerz():
    cart = session.get('cart')
    if not cart:
        flash("Cart is empty.", "warning")
        return redirect(url_for("cart_route.view_cart"))

    total_amount = sum(item['price'] * item['quantity'] for item in cart.values())

    data = {
        'store_id': 'tousi682d997d587ca',
        'store_passwd': 'tousi682d997d587ca@ssl',
        'total_amount': str(format(total_amount, '.2f')),
        'currency': 'BDT',
        'tran_id': str(uuid.uuid4()),  # Unique transaction ID
        'success_url': url_for('sslcommerz_route.payment_success', _external=True),
        'fail_url': url_for('sslcommerz_route.payment_failed', _external=True),
        'cancel_url': url_for('sslcommerz_route.payment_canceled', _external=True),
        'emi_option': 0,
        'cus_name': 'Customer Name',
        'cus_email': 'customer@email.com',
        'cus_phone': '01711111111',
        'cus_add1': 'Dhaka',
        'cus_city': 'Dhaka',
        'cus_country': 'Bangladesh',
        'shipping_method': 'NO',
        'product_name': 'Sketchify Cart',
        'product_category': 'mobile',  # ✅ push mobile payment method
        'product_profile': 'physical-goods',  # ✅ required for bKash popup
    }

    try:
        response = requests.post("https://sandbox.sslcommerz.com/gwprocess/v4/api.php", data=data)
        res_data = response.json()
    except Exception as e:
        return f"Error communicating with SSLCommerz: {str(e)}"

    if res_data.get("status") == "SUCCESS":
        return redirect(res_data["GatewayPageURL"])  # ✅ Hosted checkout page
    else:
        return f"❌ Payment init failed: {res_data}"

# Payment status routes
@sslcommerz_route.route("/payment-success", methods=["GET", "POST"])
def payment_success():
    session.pop('cart', None)
    flash("✅ Payment successful via bKash/Nagad!", "success")
    return redirect(url_for("default_route.home_page"))

@sslcommerz_route.route("/payment-failed")
def payment_failed():
    flash("❌ Payment failed. Try again.", "danger")
    return redirect(url_for('payment_route.payment_page'))

@sslcommerz_route.route("/payment-canceled")
def payment_canceled():
    flash("❌ Payment was canceled.", "warning")
    return redirect(url_for('payment_route.payment_page'))
