import json
from pathlib import Path
from typing import Any, Dict, List

from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections, utility
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "kasparo_documents"
EMBEDDING_DIM = 384


def load_json(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        # If the JSON is a dictionary instead of a list, return its values if possible.
        if "items" in data and isinstance(data["items"], list):
            return data["items"]
        return [data]

    if not isinstance(data, list):
        raise ValueError(f"Unsupported JSON structure in {path}. Expected object or list.")

    return data


def build_document(item: Dict[str, Any], source: str) -> Dict[str, Any]:
    title = item.get("title") or item.get("name") or item.get("product") or ""
    description = item.get("description", "")
    faq_question = item.get("question", "")
    faq_answer = item.get("answer", "")

    text_parts = [title, description]
    if faq_question:
        text_parts.append(f"FAQ question: {faq_question}")
    if faq_answer:
        text_parts.append(f"FAQ answer: {faq_answer}")

    # Use additional fields for search relevance if present
    for extra in ["category", "status", "price", "customer", "orderId", "id"]:
        if extra in item and item[extra] not in (None, ""):
            text_parts.append(f"{extra}: {item[extra]}")

    document_text = ". ".join([part.strip() for part in text_parts if part])

    document_id = str(item.get("id") or item.get("orderId") or item.get("product") or item.get("name") or item.get("title") or "doc_")
    if source and document_id:
        document_id = f"{source}:{document_id}"

    return {
        "document_id": document_id,
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
        "embedded_text": document_text,
    }


def create_milvus_collection(collection_name: str) -> Collection:
    if utility.has_collection(collection_name):
        print(f"Dropping existing Milvus collection '{collection_name}'...")
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

    schema = CollectionSchema(fields, description="Kasparo product / FAQ embedding collection")
    collection = Collection(name=collection_name, schema=schema)
    print(f"Created collection '{collection_name}' with {len(fields)} fields.")
    return collection


def insert_documents(collection: Collection, documents: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
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
        embeddings,
    ]

    result = collection.insert(entities)
    print(f"Inserted {len(result.primary_keys)} rows into Milvus.")

    index_params = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128},
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    print("Created embedding index in Milvus.")
    collection.load()
    print("Collection loaded and ready for search.")


def embed_texts(texts: List[str], model_name: str = MODEL_NAME) -> List[List[float]]:
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return [embedding.tolist() for embedding in embeddings]


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Load JSON data, generate embeddings, and store them in Milvus.")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input JSON files to process")
    parser.add_argument("--host", default="127.0.0.1", help="Milvus host")
    parser.add_argument("--port", default="19530", help="Milvus port")
    parser.add_argument("--collection", default=COLLECTION_NAME, help="Milvus collection name")
    parser.add_argument("--drop", action="store_true", help="Drop existing Milvus collection before inserting")
    args = parser.parse_args()

    connections.connect(alias="default", host=args.host, port=args.port)
    if args.drop or not utility.has_collection(args.collection):
        collection = create_milvus_collection(args.collection)
    else:
        collection = Collection(args.collection)
        print(f"Using existing collection '{args.collection}'.")

    all_documents: List[Dict[str, Any]] = []
    for input_file in args.inputs:
        path = Path(input_file)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")

        items = load_json(path)
        source_name = path.stem.lower().replace(".json", "")
        for item in items:
            doc = build_document(item, source_name)
            all_documents.append(doc)

    if not all_documents:
        print("No documents found to embed.")
        return

    texts = [doc["embedded_text"] for doc in all_documents]
    embeddings = embed_texts(texts)
    insert_documents(collection, all_documents, embeddings)

    print("Finished embedding and storing JSON documents in Milvus.")


if __name__ == "__main__":
    main()
