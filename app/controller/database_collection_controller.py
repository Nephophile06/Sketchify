from pymongo import MongoClient
import os

# Users collection 
def getUsersCollection():
    cluster = MongoClient(os.getenv("MONGO_URI"))
    main_database = cluster['Sketchify']
    users_collection = main_database['Users']
    return users_collection

# Categories Collection
def getCategoriesCollection():
    cluster = MongoClient(os.getenv("MONGO_URI"))
    main_database = cluster['Sketchify']
    categories_collection = main_database['Categories']
    return categories_collection

# Featured Products Collection
def getFeaturedProductsCollection():
    cluster = MongoClient(os.getenv("MONGO_URI"))
    main_database = cluster['Sketchify']
    feattured_collection = main_database['Featured']
    return feattured_collection