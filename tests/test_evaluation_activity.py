"""Unit tests for the evaluation activity — no Temporal server needed."""

import pytest
from temporalio.exceptions import ApplicationError
from temporalio.testing import ActivityEnvironment

from feedspeechback.activities.evaluation import evaluate_transcript
from feedspeechback.contracts.evaluation import Scenario
from feedspeechback.contracts.speaker import Diarization, DiarizedTranscript
from feedspeechback.contracts.transcript import Transcript

ALIGNED = DiarizedTranscript(
    transcript=Transcript(text="hello world", language="en"),
    diarization=Diarization(speakers=[]),
)


# Parametrizing over the enum means adding a Scenario member without a
# rubric fails here, before it fails in production.
@pytest.mark.parametrize("scenario", list(Scenario))
async def test_every_scenario_has_a_rubric(scenario: Scenario) -> None:
    result = await ActivityEnvironment().run(evaluate_transcript, ALIGNED, scenario)
    assert result.scenario == scenario


async def test_unknown_scenario_fails_non_retryable() -> None:
    with pytest.raises(ApplicationError) as exc_info:
        await ActivityEnvironment().run(evaluate_transcript, ALIGNED, "karaoke")
    assert exc_info.value.non_retryable
