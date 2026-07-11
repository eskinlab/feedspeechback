from pydantic import BaseModel

from feedspeechback.contracts.transcript import Transcript


class SpeakerSegment(BaseModel):
    start: float
    end: float


class Speaker(BaseModel):
    speaker: str
    segments: list[SpeakerSegment]


class Diarization(BaseModel):
    speakers: list[Speaker]


class DiarizedTranscript(BaseModel):
    transcript: Transcript
    diarization: Diarization
