import json
from pymongo import MongoClient

# Connect MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")

# Create database
db = client["kasparo_db"]

# Collections
faq_collection = db["faqs"]
product_collection = db["products"]
order_collection = db["orders"]

# Load FAQs
with open("faq.json", "r") as f:
    faq_data = json.load(f)

if faq_data:
    faq_collection.insert_many(faq_data)
    print("FAQ data inserted")

# Load Products
with open("products.json", "r") as f:
    product_data = json.load(f)

if product_data:
    product_collection.insert_many(product_data)
    print("Product data inserted")

# Load Orders
with open("orders.json", "r") as f:
    order_data = json.load(f)

if order_data:
    order_collection.insert_many(order_data)
    print("Orders data inserted")

print("All data loaded successfully")