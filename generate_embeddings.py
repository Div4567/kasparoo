import json
import os
from pathlib import Path

INPUT_DIR = Path(__file__).parent
DATA_FILES = {
    "products": INPUT_DIR / "products.json",
    "orders": INPUT_DIR / "orders.json",
    "faq": INPUT_DIR / "faq.json",
}
OUTPUT_SUFFIX = "_embeddings.json"


def get_text_to_embed(item: dict, source: str) -> str:
    if source == "products":
        return " | ".join(
            str(item.get(field, "")).strip()
            for field in ("title", "category", "description")
        )

    if source == "orders":
        return " | ".join(
            str(item.get(field, "")).strip()
            for field in ("orderId", "customer", "product", "status")
        )

    if source == "faq":
        return " | ".join(
            str(item.get(field, "")).strip()
            for field in ("question", "answer")
        )

    return " | ".join(str(v).strip() for v in item.values())


class EmbeddingGenerator:
    def __init__(self):
        self.provider = None
        self.model_name = None
        self._init_provider()

    def _init_provider(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                import openai

                openai.api_key = api_key
                self.provider = "openai"
                self.model_name = "text-embedding-3-large"
                self._client = openai
                return
            except ImportError as exc:
                raise RuntimeError(
                    "OpenAI API key is set but the openai package is not installed. "
                    "Install it with `pip install openai`."
                ) from exc

        try:
            from sentence_transformers import SentenceTransformer

            self.provider = "local"
            self.model_name = "all-MiniLM-L6-v2"
            self._client = SentenceTransformer(self.model_name)
        except ImportError:
            raise RuntimeError(
                "No embedding provider is available. Set OPENAI_API_KEY and install openai, "
                "or install sentence-transformers with `pip install sentence-transformers`."
            )

    def embed_texts(self, texts):
        if self.provider == "openai":
            response = self._client.Embedding.create(
                model=self.model_name,
                input=texts,
            )
            return [item["embedding"] for item in response["data"]]

        return [emb.tolist() for emb in self._client.encode(texts, show_progress_bar=True, batch_size=32)]


def process_file(source: str, input_path: Path, output_path: Path, embedder: EmbeddingGenerator):
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        items = json.load(f)

    texts = [get_text_to_embed(item, source) for item in items]
    embeddings = embedder.embed_texts(texts)

    for item, embedding in zip(items, embeddings):
        item["embedding"] = embedding

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"Saved {len(items)} records to {output_path}")


if __name__ == "__main__":
    embedder = EmbeddingGenerator()

    for source, input_path in DATA_FILES.items():
        output_path = INPUT_DIR / f"{source}{OUTPUT_SUFFIX}"
        process_file(source, input_path, output_path, embedder)

    print("Embedding generation complete.")
