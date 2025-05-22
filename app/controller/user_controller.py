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
    return True, "User Successfully Registered"

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
    user_data = user.find_one({'email' : data['email']})

    if data['email'] == user_data['email']:
        user.delete_one({'email' : data['email']})
        session.pop('user')
        return True, "User Deleted"
    else:
        return False, "User Not Found"


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
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)
