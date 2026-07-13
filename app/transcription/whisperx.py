"""WhisperX transcription + alignment."""

from app import config


def transcribe(audio_path: str) -> dict:
    """Return WhisperX result: aligned segments + detected language."""
    import whisperx

    device = config.device()
    compute_type = "float16" if device == "cuda" else "int8"

    model = whisperx.load_model(
        config.WHISPER_MODEL, device, compute_type=compute_type
    )
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=config.WHISPER_BATCH_SIZE)
    language = result["language"]

    align_model, metadata = whisperx.load_align_model(
        language_code=language, device=device
    )
    result = whisperx.align(result["segments"], align_model, metadata, audio, device)
    result["language"] = language
    return result
