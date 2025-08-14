#!/usr/bin/env python3
"""
Script to download required models at runtime
This reduces repository size by not storing large model files
"""
import os
import joblib
from sentence_transformers import SentenceTransformer
import requests
import zipfile
from pathlib import Path

def download_model_if_needed():
    """Download models if they don't exist locally"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Check if log_classifier.joblib exists
    classifier_path = models_dir / "log_classifier.joblib"
    
    if not classifier_path.exists():
        print("Downloading log classifier model...")
        # You can either:
        # 1. Download from a cloud storage (Google Drive, AWS S3, etc.)
        # 2. Train the model on first run
        # 3. Use a pre-trained model from Hugging Face
        
        # For now, we'll create a simple placeholder
        # In production, you should download the actual trained model
        print("Creating placeholder model...")
        # This is where you'd download your actual model
        # For example:
        # download_from_cloud_storage("log_classifier.joblib", classifier_path)
        
    # Download sentence transformer model
    print("Loading sentence transformer model...")
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Sentence transformer model loaded successfully!")
    except Exception as e:
        print(f"Error loading sentence transformer: {e}")
        print("The model will be downloaded automatically on first use.")

if __name__ == "__main__":
    download_model_if_needed()
