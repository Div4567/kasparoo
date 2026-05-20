# Divya AI Support System 

Get Smth is an intelligent, scalable e-commerce customer support system powered by Generative AI (LLMs) and Retrieval-Augmented Generation (RAG). Divya, the Get Smth AI assistant, handles general inquiries, custom policy retrieval, order tracking, and intelligently escalates complex or highly-sensitive issues to human agents.

## 🏗 Architecture Overview

The system operates across a microservices architecture:

1. **Frontend (React + Tailwind CSS):** A mock e-commerce storefront containing the user's dashboard (Orders, Recommendations) and a persistent floating Chat UI for communicating with the AI.
2. **API Gateway (Node.js + Express + MongoDB):** The backend brain. It receives queries from the frontend, queries business data (MongoDB) like orders or tickets, and acts as an orchestrator to the AI service.
3. **AI Service (Python + FastAPI):** Handles Intent Classification, queries the Vector DB for context (RAG), and prompts the LLM via Ollama using `qwen3:4b` to generate accurate, non-hallucinated responses.
4. **Data Layer:** 
   - **Commerce DB:** MongoDB (stores Orders, Tickets, Users).
   - **Vector DB:** Milvus (stores vectorized FAQs, policies, and documents).

## 🚀 Prerequisites

Ensure you have the following installed on your local machine:
- **Docker & Docker Compose** (for MongoDB and Milvus)
- **Node.js** (v18+)
- **Python** 3.10+
- **Ollama** (with local `qwen3:4b` model downloaded: `ollama run qwen3:4b`)

*Note for Ubuntu/Debian users:* You may need to install `python3-pip` and `python3-venv` via `sudo apt install python3-pip python3.14-venv` to set up the Python environment.

## ⚙️ Run Steps

Follow these steps to run the complete project locally.

### 1. Start the Databases (MongoDB & Milvus)
```bash
# In the root project directory
sudo docker compose up -d

```
*Wait a minute for Milvus and MongoDB to fully initialize.*

### 2. Start the Backend API Gateway
```bash
cd backend
npm install
node index.js
```
*The backend will run on http://localhost:5000*

### 3. Start the AI Service (Python FastAPI)
In a new terminal window:
```bash
cd ai_service
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r req.txt fastapi uvicorn pydantic requests sentence-transformers pymilvus

# (Optional) First time setup: Generate embeddings and populate Milvus
# python src/store_embeddings_from_json.py 

# Start the API
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```
*The AI service will run on http://localhost:8000*

### 4. Start the Frontend (React App)
In another new terminal window:
```bash
cd frontend
npm install
npm start
```
*The frontend React app will run on http://localhost:3000.*

## 🧠 Core Features Implemented
- **Intent Classification & Escalation:** Custom Python logic automatically parses user sentiment and intents. If the LLM lacks context or the user asks for a human/manager, an escalation flag triggers and effectively generates a MongoDB support ticket via the Node backend.
- **RAG Powered Anti-Hallucination:** Divya is strictly prompted to only use information from Milvus semantic retrieval. 
- **Model Switching:** The default Ollama model is `qwen3:4b`. Override it with the `LLM_MODEL` environment variable if you need to switch models.

## 🛠 Contributing
Contributions are welcome! Please branch out from `main` and submit a PR for any new features or bug fixes.
