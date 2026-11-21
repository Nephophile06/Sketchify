from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

cluster = MongoClient(os.getenv("MONGO_URI"))
main_database = cluster['Sketchify']

# Users collection 
def getUsersCollection():
    users_collection = main_database['Users']
    return users_collection

# Categories Collection
def getCategoriesCollection():
    categories_collection = main_database['Categories']
    return categories_collection

# Featured Products Collection
def getFeaturedProductsCollection():
    feattured_collection = main_database['Featured']
    return feattured_collection

# Ordered Products Collection
def getOrderedProductsCollection():
    orders_collection = main_database['Orders']
    return orders_collection

# Feedback Collection
def getFeedbackCollection():
    feedback_collection = main_database['Feedback']
    return feedback_collection