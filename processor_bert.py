import os
import tempfile
import joblib
from sentence_transformers import SentenceTransformer

# Ensure caches go to a writable directory across OS
_temp_root = tempfile.gettempdir()
_hf_root = os.path.join(_temp_root, "hf")
os.environ.setdefault("HF_HOME", _hf_root)
os.environ.setdefault("HF_HUB_CACHE", os.path.join(_hf_root, "hub"))
os.environ.setdefault("TRANSFORMERS_CACHE", os.path.join(_hf_root, "transformers"))
os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", os.path.join(_hf_root, "sentence-transformers"))

_model_embedding = None
_model_classification = None


def _get_models():
	global _model_embedding, _model_classification
	if _model_embedding is None:
		_model_embedding = SentenceTransformer('all-MiniLM-L6-v2')
	if _model_classification is None:
		_model_classification = joblib.load("models/log_classifier.joblib")
	return _model_embedding, _model_classification


def classify_with_bert(log_message):
	model_embedding, model_classification = _get_models()
	embeddings = model_embedding.encode([log_message])
	probabilities = model_classification.predict_proba(embeddings)[0]
	if max(probabilities) < 0.5:
		return "Unclassified"
	predicted_label = model_classification.predict(embeddings)[0]
	return predicted_label


if __name__ == "__main__":
	logs = [
		"alpha.osapi_compute.wsgi.server - 12.10.11.1 - API returned 404 not found error",
		"GET /v2/3454/servers/detail HTTP/1.1 RCODE   404 len: 1583 time: 0.1878400",
		"System crashed due to drivers errors when restarting the server",
		"Hey bro, chill ya!",
		"Multiple login failures occurred on user 6454 account",
		"Server A790 was restarted unexpectedly during the process of data transfer"
	]
	for log in logs:
		label = classify_with_bert(log)
		print(log, "->", label)
