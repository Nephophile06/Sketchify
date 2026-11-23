from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import os
from app.controller.database_collection_controller import getFeaturedProductsCollection, getFeedbackCollection

default_route = Blueprint("default_route", __name__)

@default_route.route("/")
def home_page():
    featured_collection = getFeaturedProductsCollection()
    
    featured_collection_data = featured_collection.find()
    featured_collection_data = list(featured_collection_data)
    
    for featured_products in featured_collection_data:
        featured_products['_id'] = str(featured_products['_id'])
    
    return render_template('homepage.html', featured_products = featured_collection_data)

@default_route.route("/categories")
def categories():
    return redirect(url_for("categories.category", category_name="new-in"))

@default_route.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email", "").strip()
    suggestion = request.form.get("suggestion", "").strip()

    if not email:
        flash("Please provide a valid email address.", "danger")
        return redirect(url_for("default_route.home_page"))

    try:
        feedback_collection = getFeedbackCollection()
        feedback_collection.insert_one({
            "email": email,
            "suggestion": suggestion,
            "created_at": datetime.now()
        })

        # 📨 Send direct email notification to your Gmail
        admin_email = os.getenv("MAIL_USERNAME")
        if admin_email and os.getenv("MAIL_PASSWORD"):
            try:
                from flask_mail import Message
                from app import mail

                font_stack = "'Comic Neue', 'Comic Sans MS', cursive, sans-serif"
                msg = Message(
                    subject=f"💌 New Thought / Feedback from {email}",
                    recipients=[admin_email],
                    reply_to=email,
                    body=f"Someone shared their thoughts on Sketchify!\n\nFrom: {email}\n\nThought / Suggestion:\n{suggestion}\n\n(Tip: Click 'Reply' in your email to respond to them directly!)",
                    html=f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,400;0,700;1,400&display=swap');
        * {{
            font-family: {font_stack} !important;
        }}
    </style>
</head>
<body style="margin: 0; padding: 12px; background-color: #ffffff; font-family: {font_stack};">
    <div style="font-family: {font_stack}; padding: 26px; color: #264653; max-width: 580px; border: 1.5px solid #c2aae3; border-radius: 16px; background-color: #faf8fc; box-shadow: 0 4px 16px rgba(116, 84, 153, 0.08);">
        <h2 style="font-family: {font_stack}; color: #3c7a89; margin-top: 0; font-size: 22px; font-weight: 700;">💌 New Thought on Sketchify</h2>
        <p style="font-family: {font_stack}; margin: 10px 0; font-size: 15px; color: #2c2538;">
            <strong>From (Customer Email):</strong> 
            <a href="mailto:{email}" style="font-family: {font_stack}; color: #3c7a89; text-decoration: underline; font-weight: 700;">{email}</a>
        </p>
        <div style="background-color: #ffffff; padding: 18px 20px; border-radius: 12px; border-left: 4px solid #3c7a89; margin: 18px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.04); border-top: 1px solid #f2ecf7; border-right: 1px solid #f2ecf7; border-bottom: 1px solid #f2ecf7;">
            <p style="font-family: {font_stack}; margin: 0; font-size: 16px; line-height: 1.6; color: #2b4550; white-space: pre-wrap;">{suggestion}</p>
        </div>
        <p style="font-family: {font_stack}; font-size: 13px; color: #7f748f; margin-bottom: 0;">
            💡 Tip: You can click <strong>Reply</strong> to email this customer directly.
        </p>
    </div>
</body>
</html>"""
                )
                mail.send(msg)
            except Exception as mail_err:
                print("Feedback email notification error:", mail_err)

        flash("Thank you for sharing your thoughts and subscribing!", "success")
    except Exception as e:
        print("Feedback error:", e)
        flash("Something went wrong. Please try again.", "danger")

    return redirect(url_for("default_route.home_page"))