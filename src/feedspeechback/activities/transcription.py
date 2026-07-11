from temporalio import activity

from feedspeechback.contracts.transcript import Transcript
from feedspeechback.services.transcription import get_transcriber


@activity.defn
async def transcribe_audio(audio_path: str) -> Transcript:
    activity.logger.info(f"Transcribing {audio_path}")
    activity.heartbeat("started")

    # TODO: pass a heartbeat callback into the transcriber so long inference
    # calls activity.heartbeat() periodically (e.g. per chunk) and a dead
    # worker is detected within heartbeat_timeout instead of the full
    # start_to_close_timeout.

    return await get_transcriber().transcribe(audio_path)
