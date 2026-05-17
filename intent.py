def detect_intent(query: str) -> str:

    query = query.lower()

    # =========================
    # ORDER KEYWORDS
    # =========================

    order_keywords = [
        "order",
        "track",
        "tracking",
        "shipment",
        "shipping status",
        "delivery",
        "package",
        "return",
        "refund",
        "cancel order",
        "my parcel",
        "where is my order",
        "when will my order arrive",
        "status"
    ]

    # =========================
    # PRODUCT KEYWORDS
    # =========================

    product_keywords = [
        "product",
        "price",
        "cost",
        "stock",
        "available",
        "availability",
        "buy",
        "category",
        "specification",
        "feature",
        "details"
    ]

    # =========================
    # CHECK ORDER INTENT
    # =========================

    for word in order_keywords:
        if word in query:
            return "order"

    # =========================
    # CHECK PRODUCT INTENT
    # =========================

    for word in product_keywords:
        if word in query:
            return "product"

    # =========================
    # DEFAULT = FAQ
    # =========================

    return "faq"