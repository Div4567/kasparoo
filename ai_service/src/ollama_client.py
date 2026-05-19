import requests
from typing import Any, Dict, List, Optional

from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer

BASE_URL = "http://localhost:11434"
MILVUS_HOST = "127.0.0.1"
MILVUS_PORT = "19530"
MILVUS_COLLECTION = "kasparo_documents"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def chat(messages: List[Dict[str, str]],
         model: str = "qwen:4b",
         temperature: float = 0.0,
         max_tokens: Optional[int] = None,
         timeout: int = 60) -> str:
    """
    Send chat-style messages to Ollama and return the model reply.
    messages: list of {"role": "system|user|assistant", "content": "..."}
    """
    url = f"{BASE_URL}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    resp = requests.post(url, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    return data["message"]["content"]


def embed_query(text: str, model_name: str = EMBEDDING_MODEL_NAME) -> List[float]:
    """Create a semantic embedding for the user query."""
    model = SentenceTransformer(model_name)
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def milvus_search(query: str,
                  top_k: int = 5,
                  nprobe: int = 16,
                  collection_name: str = MILVUS_COLLECTION,
                  host: str = MILVUS_HOST,
                  port: str = MILVUS_PORT) -> List[Dict[str, Any]]:
    """Search Milvus for the top-k documents relevant to the query."""
    client = MilvusClient(uri=f"http://{host}:{port}")
    if not client.has_collection(collection_name=collection_name):
        raise RuntimeError(f"Milvus collection '{collection_name}' does not exist.")

    client.load_collection(collection_name=collection_name)

    query_embedding = embed_query(query)
    search_params = {
        "metric_type": "COSINE",
        "params": {"nprobe": nprobe},
    }

    results = client.search(
        collection_name=collection_name,
        data=[query_embedding],
        anns_field="embedding",
        search_params=search_params,
        limit=top_k,
        output_fields=["source", "title", "description", "embedded_text", "faq_question", "faq_answer"],
    )

    hits: List[Dict[str, Any]] = []
    for hit in results[0]:
        entity = hit.get("entity", {})
        hits.append({
            "score": hit.get("distance"),
            "source": entity.get("source"),
            "title": entity.get("title"),
            "description": entity.get("description"),
            "embedded_text": entity.get("embedded_text"),
            "faq_question": entity.get("faq_question"),
            "faq_answer": entity.get("faq_answer"),
        })
    return hits


def build_context(results: List[Dict[str, Any]]) -> str:
    """Convert Milvus hits into a single context string for the LLM prompt."""
    context_lines = []
    for idx, hit in enumerate(results, start=1):
        parts = [f"Result {idx}:"
                 ]
        if hit.get("title"):
            parts.append(f"Title: {hit['title']}")
        if hit.get("source"):
            parts.append(f"Source: {hit['source']}")
        if hit.get("description"):
            parts.append(f"Description: {hit['description']}")
        if hit.get("faq_question"):
            parts.append(f"FAQ question: {hit['faq_question']}")
        if hit.get("faq_answer"):
            parts.append(f"FAQ answer: {hit['faq_answer']}")
        if hit.get("embedded_text"):
            parts.append(f"Content: {hit['embedded_text']}")
        parts.append(f"Score: {hit['score']:.6f}")
        context_lines.append("\n".join(parts))
    return "\n\n".join(context_lines)


def search_and_answer(query: str,
                      top_k: int = 5,
                      nprobe: int = 16,
                      model: str = "qwen:4b",
                      temperature: float = 0.0,
                      max_tokens: Optional[int] = None,
                      timeout: int = 60,
                      milvus_host: str = MILVUS_HOST,
                      milvus_port: str = MILVUS_PORT,
                      milvus_collection: str = MILVUS_COLLECTION) -> str:
    """Retrieve top-k context from Milvus, then ask Qwen to answer using that context."""
    results = milvus_search(query,
                            top_k=top_k,
                            nprobe=nprobe,
                            collection_name=milvus_collection,
                            host=milvus_host,
                            port=milvus_port)

    if not results:
        raise RuntimeError("No documents returned from Milvus search.")

    context = build_context(results)
    prompt = (
        "Use only the following retrieved documents to answer the user's question. "
        "If the answer is not contained in the retrieved context, say that you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the provided documents to answer the question accurately."},
        {"role": "user", "content": prompt}
    ]

    return chat(messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout)
if __name__ == "__main__":
    query = input("enter your query here")

    answer = search_and_answer(
        query=query,
        top_k=5,
        model="qwen:4b"
    )

    print("\nANSWER:\n")
    print(answer)