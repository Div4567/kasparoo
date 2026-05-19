# API Reference

## Backend API Gateway (Port 5000)

- `GET /health` : Health check.
- `POST /api/chat` : Forward messages to AI Service.
- `GET /api/orders/:userId` : Get user orders.
- `POST /api/tickets` : Create a human escalation ticket.

## AI Service (Port 8000)

- `POST /chat` : Central LLM routing. Body: `{ "query": "str", "user_id": "str", "history": [] }`
