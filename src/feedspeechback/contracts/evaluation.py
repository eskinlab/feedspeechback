from enum import StrEnum

from pydantic import BaseModel


class Scenario(StrEnum):
    INTERVIEW = "interview"
    JOB_MEETING = "job_meeting"


class EvaluationResult(BaseModel):
    scenario: Scenario
    score: int
    feedback: str
