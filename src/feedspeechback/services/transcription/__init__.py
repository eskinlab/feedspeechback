import os
from functools import lru_cache

from feedspeechback.services.transcription.interface import Transcriber


@lru_cache(maxsize=1)
def get_transcriber() -> Transcriber:
    provider = os.environ.get("TRANSCRIPTION_PROVIDER", "whisperx")
    match provider:
        case "whisperx":
            from feedspeechback.services.transcription.whisperx import (
                WhisperXTranscriber,
            )

            return WhisperXTranscriber()
        case "cloud":
            from feedspeechback.services.transcription.cloud_api import (
                CloudTranscriber,
            )

            return CloudTranscriber()
        case _:
            raise ValueError(f"Unknown TRANSCRIPTION_PROVIDER: {provider!r}")
