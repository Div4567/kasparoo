from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

db = client["kasparo_db"]

order_collection = db["orders"]

product_collection = db["products"]


def search_order(query: str):

    query = query.lower()

    orders = list(order_collection.find())

    for order in orders:

        order_id = str(order.get("order_id", "")).lower()

        customer = str(order.get("customer_name", "")).lower()

        product = str(order.get("product_name", "")).lower()

        if (
            order_id in query
            or customer in query
            or product in query
        ):
            return order

    return None


def search_product(query: str):

    query = query.lower()

    products = list(product_collection.find())

    for product in products:

        name = str(product.get("name", "")).lower()

        category = str(product.get("category", "")).lower()

        if name in query or category in query:
            return product

    return None