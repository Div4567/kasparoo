import random
import json
faq_topics = [
    "returns", "refunds", "shipping", "payments", "delivery",
    "exchange", "tracking", "cancellation", "warranty", "support"
]

faq_templates = [
    "What is the policy for {topic}?",
    "How can I request {topic}?",
    "Can I get help regarding {topic}?",
    "How long does {topic} take?",
    "Is {topic} available for all products?"
]

faq_answers = [
    "Please check your account dashboard for more details.",
    "Our support team will assist you regarding this issue.",
    "This feature is available for eligible orders.",
    "The request is usually processed within 3-5 business days.",
    "You can contact customer support for assistance."
]

faqs = []

for i in range(1, 101):
    topic = random.choice(faq_topics)
    question = random.choice(faq_templates).format(topic=topic)
    answer = random.choice(faq_answers)

    faqs.append({
        "id": i,
        "question": question,
        "answer": answer
    })

# ------------------------------
# PRODUCT GENERATION
# ------------------------------
# ------------------------------
# PRODUCT GENERATION
# ------------------------------

product_category_map = {
    "Headphones": "Electronics",
    "Earbuds": "Electronics",
    "Keyboard": "Electronics",
    "Mouse": "Electronics",
    "Monitor": "Electronics",
    "Router": "Electronics",
    "Speaker": "Electronics",
    "Watch": "Accessories",
    "Tripod": "Accessories",
    "Backpack": "Accessories",
    "Bottle": "Kitchen",
    "Chair": "Furniture",
    "Shoes": "Footwear",
    "Jacket": "Clothing",
    "Hoodie": "Clothing"
}

product_names = list(product_category_map.keys())

adjectives = [
    "Wireless", "Portable", "Smart", "Premium", "Gaming",
    "Ergonomic", "Lightweight", "Bluetooth", "Fast", "Stylish"
]

products = []

for i in range(1, 101):
    adjective = random.choice(adjectives)
    product = random.choice(product_names)

    category = product_category_map[product]

    products.append({
        "id": i,
        "title": f"{adjective} {product}",
        "category": category,
        "price": random.randint(299, 9999),
        "description": f"{adjective} {product.lower()} suitable for daily usage"
    })
# ------------------------------
# ORDER GENERATION
# ------------------------------
first_names = [
    "Aarav", "Priya", "Rohan", "Neha", "Karan",
    "Ananya", "Rahul", "Sneha", "Ishita", "Aditya"
]

last_names = [
    "Sharma", "Singh", "Das", "Verma", "Mehta",
    "Roy", "Kapoor", "Jain", "Rao", "Patel"
]

statuses = [
    "Processing", "Shipped", "Delivered",
    "Cancelled", "Returned", "Out for Delivery"
]

orders = []

for i in range(1, 101):
    customer = f"{random.choice(first_names)} {random.choice(last_names)}"
    selected_product = random.choice(products)

    orders.append({
        "orderId": f"ORD{i:03}",
        "customer": customer,
        "product": selected_product["title"],
        "status": random.choice(statuses)
    })

# ------------------------------
# SAVE FILES
# ------------------------------
with open("faq.json", "w") as f:
    json.dump(faqs, f, indent=2)

with open("products.json", "w") as f:
    json.dump(products, f, indent=2)

with open("orders.json", "w") as f:
    json.dump(orders, f, indent=2)

print("Datasets generated successfully!")
