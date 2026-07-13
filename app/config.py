"""All knobs in one place — read from environment variables."""

import os

WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "large-v2")
WHISPER_BATCH_SIZE = int(os.environ.get("WHISPER_BATCH_SIZE", "16"))

NEBIUS_BASE_URL = os.environ.get("NEBIUS_BASE_URL", "https://api.studio.nebius.com/v1/")
NEBIUS_MODEL = os.environ.get("NEBIUS_MODEL", "meta-llama/Llama-3.3-70B-Instruct")

HF_TOKEN = os.environ.get("HF_TOKEN", "")


def nebius_api_key() -> str:
    return os.environ["NEBIUS_API_KEY"]


def device() -> str:
    import torch

    return "cuda" if torch.cuda.is_available() else "cpu"
