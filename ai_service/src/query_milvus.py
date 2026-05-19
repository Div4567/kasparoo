import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from pymilvus import Collection, connections, utility
from sentence_transformers import SentenceTransformer

DEFAULT_COLLECTION = "kasparo_documents"
EMBEDDING_DIM = 384
MODEL_NAME = "all-MiniLM-L6-v2"


def connect_milvus(host: str, port: str) -> None:
    if not utility.has_collection(DEFAULT_COLLECTION):
        raise RuntimeError(f"Milvus collection '{DEFAULT_COLLECTION}' does not exist.")
    connections.connect(alias="default", host=host, port=port)


def embed_query(query: str, model_name: str = MODEL_NAME) -> List[float]:
    model = SentenceTransformer(model_name)
    embedding = model.encode(query, convert_to_numpy=True)
    return embedding.tolist()


def query_collection(collection_name: str, query_embedding: List[float], top_k: int, nprobe: int) -> List[Dict[str, Any]]:
    collection = Collection(collection_name)

    search_params = {
        "metric_type": "COSINE",
        "params": {"nprobe": nprobe},
    }

    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        expr=None,
        output_fields=[
            "document_id",
            "source",
            "title",
            "description",
            "faq_question",
            "faq_answer",
            "category",
            "price",
            "status",
            "customer",
            "order_id",
            "embedded_text",
        ],
    )

    hits = []
    for hit in results[0]:
        hits.append({
            "document_id": hit.entity.get("document_id"),
            "source": hit.entity.get("source"),
            "title": hit.entity.get("title"),
            "description": hit.entity.get("description"),
            "faq_question": hit.entity.get("faq_question"),
            "faq_answer": hit.entity.get("faq_answer"),
            "category": hit.entity.get("category"),
            "price": hit.entity.get("price"),
            "status": hit.entity.get("status"),
            "customer": hit.entity.get("customer"),
            "order_id": hit.entity.get("order_id"),
            "embedded_text": hit.entity.get("embedded_text"),
            "score": hit.distance,
        })
    return hits


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the Milvus embedding collection.")
    parser.add_argument("--query", required=True, help="Text query to search in Milvus")
    parser.add_argument("--host", default="127.0.0.1", help="Milvus host")
    parser.add_argument("--port", default="19530", help="Milvus gRPC port")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION, help="Milvus collection name")
    parser.add_argument("--topk", type=int, default=5, help="Number of top results to return")
    parser.add_argument("--nprobe", type=int, default=16, help="nprobe parameter for IVF search")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--output", help="Optional output file path for JSON format")
    args = parser.parse_args()

    try:
        connections.connect(alias="default", host=args.host, port=args.port)
    except Exception as exc:
        raise RuntimeError(
            f"Unable to connect to Milvus at {args.host}:{args.port}. Ensure the server is running and reachable."
        ) from exc

    if not utility.has_collection(args.collection):
        raise RuntimeError(f"Milvus collection '{args.collection}' does not exist.")

    query_embedding = embed_query(args.query)
    hits = query_collection(args.collection, query_embedding, args.topk, args.nprobe)

    if args.format == "json":
        output_data = {"query": args.query, "results": hits}
        json_text = json.dumps(output_data, indent=2)
        if args.output:
            Path(args.output).write_text(json_text, encoding="utf-8")
            print(f"Wrote JSON results to {args.output}")
        else:
            print(json_text)
        return

    for index, hit in enumerate(hits, start=1):
        print(f"Result {index}: score={hit['score']:.4f}")
        print(f"  source: {hit['source']}")
        print(f"  document_id: {hit['document_id']}")
        if hit["title"]:
            print(f"  title: {hit['title']}")
        if hit["description"]:
            print(f"  description: {hit['description']}")
        if hit["faq_question"] or hit["faq_answer"]:
            print(f"  faq_question: {hit['faq_question']}")
            print(f"  faq_answer: {hit['faq_answer']}")
        if hit["status"]:
            print(f"  status: {hit['status']}")
        if hit["customer"]:
            print(f"  customer: {hit['customer']}")
        if hit["price"]:
            print(f"  price: {hit['price']}")
        print()


if __name__ == "__main__":
    main()
