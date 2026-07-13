"""Speaker diarization — pyannote via WhisperX's DiarizationPipeline wrapper."""

from app import config


def diarize(audio_path: str, result: dict) -> dict:
    """Tag each transcript segment with a speaker. Needs HF_TOKEN
    (gated model: pyannote/speaker-diarization-3.1)."""
    import whisperx
    from whisperx.diarize import DiarizationPipeline

    diarizer = DiarizationPipeline(token=config.HF_TOKEN, device=config.device())
    return whisperx.assign_word_speakers(diarizer(audio_path), result)
