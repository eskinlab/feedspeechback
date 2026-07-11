from pydantic import BaseModel


class Transcript(BaseModel):
    text: str
    language: str
