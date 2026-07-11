from temporalio import activity

from feedspeechback.contracts.speaker import Diarization, DiarizedTranscript
from feedspeechback.contracts.transcript import Transcript


@activity.defn
async def align_transcript_diarization(
    transcript: Transcript, diarization: Diarization
) -> DiarizedTranscript:
    activity.logger.info("Aligning transcript with diarization output")

    # TODO: align diarization speaker segments with transcript word-level
    # timestamps to produce a single speaker-labeled transcript.

    return DiarizedTranscript(transcript=transcript, diarization=diarization)
