from typing import Protocol

from feedspeechback.contracts.transcript import Transcript


class Transcriber(Protocol):
    async def transcribe(self, audio_path: str) -> Transcript: ...
