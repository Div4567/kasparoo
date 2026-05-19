# Architecture

The Get Smth architecture relies on four main pillars:
1. **Frontend:** React + Tailwind CSS
2. **Backend Gateway:** Express.js + MongoDB API
3. **AI Service:** FastAPI, Sentence-Transformers, Milvus, and Ollama integration
4. **Vector Database:** Milvus for RAG indexing

Traffic flows from the User -> React Frontend -> Express API Gateway -> AI Python Service. The AI Service connects to Milvus to fetch RAG context before pinging the LLM (Qwen) for generation.
