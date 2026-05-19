import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Get Smth Chat Service")

# Support for model switching, defaulting to Qwen
DEFAULT_MODEL = os.getenv("LLM_MODEL", "qwen:4b")


class ChatRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    history: Optional[List[dict]] = None
    model: Optional[str] = DEFAULT_MODEL


@app.post("/chat")
def handle_chat(req: ChatRequest):
    """
    Lazy-import heavy dependencies at request-time. If imports or downstream
    services are not available, return a graceful fallback reply so the API
    can remain responsive while the full AI infra (Milvus/Ollama/models)
    is brought up.
    """
    try:
        from src.ollama_client import chat, milvus_search, build_context
        from src.intent import detect_intent, check_escalation
        from src.mongo_search import search_order
    except Exception as e:
        return {
            "reply": "The chat backend is not fully available right now.\n"
                     "Please try again later or contact support.",
            "intent": None,
            "escalate": True,
            "model_used": None,
            "context_retrieved": 0,
            "error": str(e)
        }

    try:
        # 1. Retrieve Context from Milvus
        search_results = milvus_search(req.query, top_k=3)
        context_str = build_context(search_results)

        intent = detect_intent(req.query)

        # Enhance context with Order data if intent is tracking or history
        if intent in ["order_tracking", "order_history", "order_cancellation", "return_refund"]:
            order = search_order(req.query)
            if order:
                context_str += f"\n[Order details found in DB]: Order ID: {order.get('order_id', 'Unknown')}, Customer: {order.get('customer_name', 'Unknown')}, Product: {order.get('product_name', 'Unknown')}, Status: {order.get('status', 'Unknown')}."
            else:
                context_str += "\n[Order details]: I could not find a matching order for this query in the database. Please provide a valid order ID."

        # 2. Build Prompt
        system_prompt = (
            "You are Divya, the official customer support assistant for Get Smth, an e-commerce platform.\n"
            "Your tone is polite, professional, and empathetic.\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. You MUST answer the user's question using ONLY the information provided in the Context below.\n"
            "2. If the context does not contain the answer, politely say: 'I apologize, but I do not have that specific information. Let me escalate this to a human agent.'\n"
            "3. Do NOT make up return policies, shipping times, or pricing if it is not in the context.\n"
            "4. If the user asks about an order and it is in the context, clearly explain the status and details.\n"
            "5. Be concise but complete.\n\n"
            f"=== CONTEXT ===\n{context_str}\n================\n"
        )

        # 3. Handle Chat History
        messages = [{"role": "system", "content": system_prompt}]
        if req.history:
            messages.extend(req.history)

        messages.append({"role": "user", "content": req.query})

        # 4. Generate Response using Model
        model_to_use = req.model if req.model else DEFAULT_MODEL
        reply = chat(messages, model=model_to_use)

        # 5. Intent and Escalation
        escalate = check_escalation(req.query, intent, reply)

        return {
            "reply": reply,
            "intent": intent,
            "escalate": escalate,
            "model_used": model_to_use,
            "context_retrieved": len(search_results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
