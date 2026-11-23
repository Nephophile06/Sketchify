from flask_mail import Message
import os                                       #environment variables access kore
from pymongo import MongoClient
from app import bcrypt
from flask import session, flash, redirect, url_for
from app import mail
import random
# Database Setup
def userCollectionDatabase():
    client = MongoClient(os.getenv("MONGO_URI"))
    Users_database = client['Sketchify']
    Users_first_collection = Users_database['Users']

    return Users_first_collection


# Register Controller
def register_user_controller(data):
    userCollection = userCollectionDatabase()

    # Checking for an existing user

    if userCollection.find_one({'username': data['username']}):
        return False, "User already exists with this username"    

    if userCollection.find_one({'email': data['email']}):
        return False, "User already exists with this email"
    

    # Hashing
    data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    userCollection.insert_one(data)
    
    # Success Message
    return True, "User Successfully Registered. A 8 digit backup code has been sent to your email."

# Login User Controller
def login_user_controller(data):
    
    userCollection = userCollectionDatabase()

    # UserEmail
    user_email = data["email"]

    user = userCollection.find_one({'email': user_email})

    # 1st Condition ( user ache ki na ) eita bujho ki na dekho arekbar milao
    if user:
        # 2nd Condition ( password match kortese ki na)
        if bcrypt.check_password_hash(user['password'], data['password']):

            # Session Define korbo 
            session['user'] = {
                "_id": str(user['_id']),
                "username": user['username'],
                "email": user['email']
            }           
            return True, "Login Successful"
        else:
            return False, "Password do not match"
    else:
        return False, 'User Not Found'

#updating the user info
def update_user_controller(data):
    new_email = data['email']
    new_password = data['password']

    userCollection = userCollectionDatabase()

    if 'user' not in session:
        return False, "Please login first."

    current_email = session['user']['email']
    users_data = userCollection.find_one({'email': current_email})

    if not users_data:
        return False, "User not found."

    update_user_data = {}

    # Password update logic
    if new_password.strip():
        if len(new_password) <= 6:
            return False, "Password must be greater than 6 characters"
        elif bcrypt.check_password_hash(users_data['password'], new_password):
            return False, "You have entered an old password. Enter a new one"
        update_user_data['password'] = bcrypt.generate_password_hash(new_password).decode('utf-8')

    # Email update logic
    if new_email != current_email:
        existing_user = userCollection.find_one({'email': new_email})
        if existing_user:
            return False, "This email is already in use by another account."
        update_user_data['email'] = new_email

    # If anything changed, update DB
    if update_user_data:
        userCollection.update_one({'email': current_email}, {"$set": update_user_data})
        if 'email' in update_user_data:
            session['user']['email'] = update_user_data['email']

    return True, "Profile Updated Successfully"



# Delete user controller
def delete_user_controller(data):
    user = userCollectionDatabase()
    user_data = user.find_one({'email': data['email']})

    if not user_data:
        return False, "User Not Found"

    user.delete_one({'email': data['email']})
    session.pop('user', None)
    return True, "User Deleted"


def login_with_backup_controller(data):
    email = data['email'].strip()
    code = data['backup_code'].strip()
    
    users_collection = userCollectionDatabase()
    user = users_collection.find_one({'email': email, 'backup_code': code})
    
    if not user:
        return False, "Invalid email or backup code."
    
    session["user"] = {
        "_id": str(user['_id']),
        "username": user["username"],
        "email": user["email"]
    }
    return True, "Logged in with the 8 digit backup code"

def generate_backup_code():
    return str(random.randint(10000000, 99999999))  # 8-digit code

def send_backup_code_email(email, code):
    subject = "Your Sketchify Backup Login Code"
    body = f"""
        Hi there,

        Here is your 8-digit backup login code: {code}

        Please keep this code safe. It can be used to log in if you forget your password.

        - Sketchify Team
    """
    font_stack = "'Comic Neue', 'Comic Sans MS', cursive, sans-serif"
    html = f"""<!DOCTYPE html>
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
    <div style="font-family: {font_stack}; padding: 26px; color: #264653; max-width: 540px; border: 1.5px solid #c2aae3; border-radius: 16px; background-color: #faf8fc; box-shadow: 0 4px 16px rgba(116, 84, 153, 0.08);">
        <h2 style="font-family: {font_stack}; color: #3c7a89; margin-top: 0; font-size: 22px; font-weight: 700;">🔐 Sketchify Backup Login Code</h2>
        <p style="font-family: {font_stack}; font-size: 15px; color: #2c2538; margin: 10px 0;">Hi there,</p>
        <p style="font-family: {font_stack}; font-size: 15px; color: #2c2538; margin: 10px 0;">Here is your 8-digit backup login code for accessing your Sketchify account:</p>
        <div style="background-color: #ffffff; padding: 16px 24px; border-radius: 12px; border: 2px dashed #745499; margin: 20px 0; text-align: center; display: inline-block;">
            <span style="font-family: {font_stack}; font-size: 26px; font-weight: 700; letter-spacing: 4px; color: #745499;">{code}</span>
        </div>
        <p style="font-family: {font_stack}; font-size: 14px; color: #5a5068; line-height: 1.5; margin: 10px 0;">
            Please keep this code in a safe place. You can use it anytime to log in if you forget your password.
        </p>
        <hr style="border: none; border-top: 1px solid #ede7f3; margin: 20px 0;">
        <p style="font-family: {font_stack}; font-size: 13px; color: #887d99; margin: 0;">
            Warm regards,<br>
            <strong style="color: #3c7a89;">The Sketchify Team</strong>
        </p>
    </div>
</body>
</html>"""
    try:
        msg = Message(subject, recipients=[email], body=body, html=html)
        mail.send(msg)
        return True
    except Exception as e:
        print("Mail sending error:", e)
        return False
