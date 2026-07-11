from temporalio import activity

from feedspeechback.contracts.speaker import Diarization, Speaker


@activity.defn
async def diarize_audio(audio_path: str) -> Diarization:
    activity.logger.info(f"Diarizing {audio_path}")

    # TODO: pyannote speaker segmentation

    return Diarization(speakers=[Speaker(speaker="A", segments=[])])
