from pydantic import BaseModel


class Submission(BaseModel):
    """What a user submits for speech feedback.

    Extend with optional fields (source types, language hint, expected
    speaker count, ...) to stay backward compatible with in-flight
    workflows and old clients.
    """

    audio_path: str
