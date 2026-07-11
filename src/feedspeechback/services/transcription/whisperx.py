from feedspeechback.contracts.transcript import Transcript


class WhisperXTranscriber:
    async def transcribe(self, audio_path: str) -> Transcript:
        # TODO: WhisperX (CPU or CUDA) — load the model once in __init__,
        # transcribe here, and map the WhisperX segments into Transcript.
        return Transcript(text="transcribed text", language="en")
