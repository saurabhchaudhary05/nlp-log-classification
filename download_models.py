#!/usr/bin/env python3
"""
Prepare HF cache directories in the OS temp folder so downloads have permission.
"""
import os
import tempfile
from pathlib import Path

# Use OS-specific temp directory
_temp_root = tempfile.gettempdir()
_hf_root = os.path.join(_temp_root, "hf")
os.environ.setdefault("HF_HOME", _hf_root)
os.environ.setdefault("HF_HUB_CACHE", os.path.join(_hf_root, "hub"))
os.environ.setdefault("TRANSFORMERS_CACHE", os.path.join(_hf_root, "transformers"))
os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", os.path.join(_hf_root, "sentence-transformers"))


def download_model_if_needed():
	# Create cache directories to avoid permission issues
	for env_key in ("HF_HOME", "HF_HUB_CACHE", "TRANSFORMERS_CACHE", "SENTENCE_TRANSFORMERS_HOME"):
		Path(os.environ[env_key]).mkdir(parents=True, exist_ok=True)
	print("HF cache directories prepared:", os.environ.get("HF_HOME"))


if __name__ == "__main__":
	download_model_if_needed()
