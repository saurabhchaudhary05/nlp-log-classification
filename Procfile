web: env HF_HOME=/tmp/hf TRANSFORMERS_CACHE=/tmp/hf/transformers SENTENCE_TRANSFORMERS_HOME=/tmp/hf/sentence-transformers HF_HUB_CACHE=/tmp/hf/hub gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT app:app
