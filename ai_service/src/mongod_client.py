from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

db = client["kasparo_db"]

faq_collection = db["faqs"]
product_collection = db["products"]
order_collection = db["orders"]