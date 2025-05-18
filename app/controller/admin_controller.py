# controllers/admin_controller.py
import os

admin_name = os.getenv("ADMIN_NAME")
admin_pass = os.getenv("ADMIN_PASS")

def authenticate_admin(username, password):
    if username == admin_name and password == admin_pass:
        return True, "Successfully Logged in!!"
    else:
        return False, "Invalid Username or Password"
