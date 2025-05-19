# controllers/admin_controller.py
import os
from app.controller.database_collection_controller import getUsersCollection, getCategoriesCollection

admin_name = os.getenv("ADMIN_NAME")
admin_pass = os.getenv("ADMIN_PASS")

def authenticate_admin(username, password):
    if username == admin_name and password == admin_pass:
        return True, "Successfully Logged in!!"
    else:
        return False, "Invalid Username or Password"
def user_list_controller():
    users_collection = getUsersCollection()
    users_data = users_collection.find()
    users_data = list(users_data)
    
    for user in users_data:
        user['_id'] = str(user['_id'])
         
    return users_data