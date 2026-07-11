from temporalio import activity
from temporalio.exceptions import ApplicationError

from feedspeechback.contracts.evaluation import EvaluationResult, Scenario
from feedspeechback.contracts.speaker import DiarizedTranscript
from feedspeechback.services.evaluation.rubrics import RUBRICS


@activity.defn
async def evaluate_transcript(
    aligned: DiarizedTranscript, scenario: Scenario
) -> EvaluationResult:
    rubric = RUBRICS.get(scenario)
    if rubric is None:
        raise ApplicationError(
            f"No rubric for scenario: {scenario!r}. Known scenarios: {sorted(RUBRICS)}",
            non_retryable=True,
        )

    activity.logger.info(f"Evaluating transcript for scenario={scenario}")

    # TODO: LangGraph / LLM judge scoring using rubric["criteria"]

    return EvaluationResult(scenario=scenario, score=85, feedback="Good structure")
