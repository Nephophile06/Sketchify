from datetime import datetime
from bson import ObjectId
from app.controller.database_collection_controller import getOrderedProductsCollection
from flask import session, request

def save_order(user, cart, payment_method, transaction_id=None):
    orders_collection = getOrderedProductsCollection()

    order_data = {
        "user_id": ObjectId(user["_id"]),
        "user_name": user.get("username", "Unknown"),
        "user_email": user.get("email", "Unknown"),
        "items": list(cart.values()),
        "total_amount": sum(item['price'] * item['quantity'] for item in cart.values()),
        "status": "Paid",
        "created_at": datetime.today(),
        "payment_method": payment_method,
        "transaction_id": transaction_id,
        "delivery_status": "Processing"
    }

    orders_collection.insert_one(order_data)
