from huggingface_hub import hf_hub_download
from joblib import load
from sklearn.pipeline import Pipeline

import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"  # Add at top
MODEL_REPO = "adrian7305/email-classifier"
MODEL_FILE = "model.joblib"

def load_model() -> Pipeline:
    model_path = hf_hub_download(
    repo_id=MODEL_REPO,
    filename=MODEL_FILE,
    cache_dir="/tmp/.hf_cache"
)
    return load(model_path)

def classify_email(model: Pipeline, email: str) -> str:
    return str(model.predict([email])[0])