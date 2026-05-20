import os


DEFAULT_MODEL = os.getenv("LLM_MODEL", "qwen3:4b")
MODEL_FALLBACKS = {
	"qwen3:4b": ["qwen:4b"],
}


def get_model_attempts(model: str | None = None) -> list[str]:
	primary_model = model or DEFAULT_MODEL
	attempts = [primary_model]

	for fallback_model in MODEL_FALLBACKS.get(primary_model, []):
		if fallback_model not in attempts:
			attempts.append(fallback_model)

	return attempts