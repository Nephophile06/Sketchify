from flask import Flask
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

# bcrypt object
bcrypt = Bcrypt()



client = None
Users_first_collection = None

def create_app():
    app = Flask(__name__)
    # Secret Key
    app.secret_key = "$anika202!$#"
    load_dotenv()
    
    bcrypt.init_app(app)

    # Default Routes
    from .routes.default_routes import default_route
    app.register_blueprint(default_route)

    # User Routes
    from .routes.user_routes import user_route
    app.register_blueprint(user_route)

    # Category Routes
    from .routes.category_routes import category_route
    app.register_blueprint(category_route)
    
    # Admin Routes
    from .routes.admin_routes import admin_route
    app.register_blueprint(admin_route)
    
    # Cart Routes
    from .routes.cart_route import cart_route
    app.register_blueprint(cart_route)
    return app
