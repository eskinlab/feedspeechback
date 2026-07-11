from feedspeechback.contracts.transcript import Transcript


class CloudTranscriber:
    async def transcribe(self, audio_path: str) -> Transcript:
        # TODO: call a hosted transcription API and map its response
        # into Transcript.
        raise NotImplementedError("Cloud transcription is not implemented yet")
