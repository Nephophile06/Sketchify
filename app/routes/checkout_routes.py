from flask import render_template, Blueprint, session, redirect, url_for, flash

checkout_route = Blueprint('checkout_route', __name__)

@checkout_route.route("/checkout")
def checkout():
        
# Check if user is logged in
    if 'user' not in session:
        flash("You need to log in to proceed to checkout.","danger") 
        return redirect(url_for('user_route.login')) 

    # If both are OK, go to payment
    return redirect(url_for('payment.payment_page'))
