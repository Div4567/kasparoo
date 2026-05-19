def detect_intent(query: str) -> str:
    query = query.lower()
    if any(word in query for word in ["order history", "my orders", "view orders", "order details", "purchase history"]):
        return "order_history"
    if any(word in query for word in ["cancel", "change my order", "modify"]):
        return "order_cancellation"
    if any(word in query for word in ["replace", "alternative", "similar", "instead", "what else"]):
        return "check_replacements"
    if any(word in query for word in ["buy", "order a", "place order", "i want to buy", "add to cart"]):
        return "create_order"
    if any(word in query for word in ["where is", "track", "status", "has shipped"]):
        return "order_tracking"
    if any(word in query for word in ["return", "refund", "broken", "damaged"]):
        return "return_refund"
    if any(word in query for word in ["speak to human", "manager", "agent", "operator", "angry", "terrible", "worst"]):
        return "human_escalation"
    return "general_inquiry"

def check_escalation(query: str, intent: str, ai_reply: str) -> bool:
    if intent == "human_escalation":
        return True
    if intent == "order_history":
        return False
    if "I do not have that specific information" in ai_reply:
        return True
    return False
