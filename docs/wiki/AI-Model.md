# AI & Model Configuration

Get Smth uses `qwen2.5:3b` as its default language model served via Ollama. 

## Semantic Search (RAG)
Vector embeddings are generated locally via the `all-MiniLM-L6-v2` transformer and pushed into Milvus. 

## Intent Routing
`ai_service/src/intent.py` performs keyword extraction to bypass the LLM and instantly route "refund" or "angry" sentiments to create a support ticket.
