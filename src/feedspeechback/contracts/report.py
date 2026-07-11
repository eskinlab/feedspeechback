from pydantic import BaseModel

from feedspeechback.contracts.evaluation import EvaluationResult


class Report(BaseModel):
    evaluation: EvaluationResult
    html_path: str
    pdf_path: str
