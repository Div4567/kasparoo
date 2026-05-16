import json
from pathlib import Path
from typing import Any, Dict, List

from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, MilvusException, connections, utility

COLLECTION_NAME = "kasparo_documents"
EMBEDDING_DIM = 384


def load_json(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            return data["items"]
        return [data]

    if not isinstance(data, list):
        raise ValueError(f"Unsupported JSON structure in {path}. Expected object or list.")

    return data


def infer_source(path: Path) -> str:
    stem = path.stem.lower()
    return stem.replace("_embeddings", "")


def build_document(item: Dict[str, Any], source: str) -> Dict[str, Any]:
    title = item.get("title") or item.get("name") or item.get("product") or ""
    description = item.get("description", "")
    faq_question = item.get("question", "")
    faq_answer = item.get("answer", "")

    return {
        "document_id": str(item.get("id") or item.get("orderId") or item.get("product") or item.get("title") or ""),
        "source": source,
        "title": title,
        "description": description,
        "faq_question": faq_question,
        "faq_answer": faq_answer,
        "category": str(item.get("category", "")),
        "price": str(item.get("price", "")),
        "status": str(item.get("status", "")),
        "customer": str(item.get("customer", "")),
        "order_id": str(item.get("orderId", "")),
        "embedded_text": str(item.get("embedded_text", "")),
        "embedding": item.get("embedding", []),
    }


def create_milvus_collection(collection_name: str) -> Collection:
    if utility.has_collection(collection_name):
        print(f"Dropping existing collection '{collection_name}'...")
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="document_id", dtype=DataType.VARCHAR, is_primary=True, max_length=256),
        FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="faq_question", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="faq_answer", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="price", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="status", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="customer", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="order_id", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="embedded_text", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
    ]
    schema = CollectionSchema(fields, description="Kasparo generated JSON embeddings")
    return Collection(name=collection_name, schema=schema)


def insert_documents(collection: Collection, documents: List[Dict[str, Any]]) -> None:
    if not documents:
        print("No documents to insert.")
        return

    entities = [
        [doc["document_id"] for doc in documents],
        [doc["source"] for doc in documents],
        [doc["title"] for doc in documents],
        [doc["description"] for doc in documents],
        [doc["faq_question"] for doc in documents],
        [doc["faq_answer"] for doc in documents],
        [doc["category"] for doc in documents],
        [doc["price"] for doc in documents],
        [doc["status"] for doc in documents],
        [doc["customer"] for doc in documents],
        [doc["order_id"] for doc in documents],
        [doc["embedded_text"][:65534] for doc in documents],
        [doc["embedding"] for doc in documents],
    ]

    result = collection.insert(entities)
    print(f"Inserted {len(result.primary_keys)} rows into Milvus.")
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {"nlist": 128},
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.load()
    print("Collection loaded for search.")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Insert generated JSON embeddings into Milvus.")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input embedding JSON files")
    parser.add_argument("--host", default="127.0.0.1", help="Milvus host")
    parser.add_argument("--port", default="19530", help="Milvus port")
    parser.add_argument("--collection", default=COLLECTION_NAME, help="Milvus collection name")
    parser.add_argument("--drop", action="store_true", help="Drop existing collection before inserting")
    args = parser.parse_args()

    try:
        connections.connect(alias="default", host=args.host, port=args.port)
    except MilvusException as exc:
        raise RuntimeError(
            f"Unable to connect to Milvus at {args.host}:{args.port}. "
            "Please verify that the Milvus server is running and reachable, "
            "or pass the correct host/port."
        ) from exc

    if args.drop or not utility.has_collection(args.collection):
        collection = create_milvus_collection(args.collection)
    else:
        collection = Collection(args.collection)
        print(f"Using existing collection '{args.collection}'.")

    all_docs: List[Dict[str, Any]] = []
    for input_file in args.inputs:
        path = Path(input_file)
        items = load_json(path)
        source = infer_source(path)
        for item in items:
            if "embedding" not in item or not isinstance(item["embedding"], list):
                raise ValueError(f"Missing embedding vector in {path}: {item}")
            doc = build_document(item, source)
            all_docs.append(doc)

    insert_documents(collection, all_docs)
    print("All documents inserted into Milvus.")


if __name__ == "__main__":
    main()
