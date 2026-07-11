import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# These activity imports also run on the default (workflow) worker at
# startup, so activity modules must stay import-light: heavy ML dependencies
# (whisperx, torch, pyannote, ...) belong behind the lazy provider factories
# in services/, never at module level in activities/.
with workflow.unsafe.imports_passed_through():
    from feedspeechback.activities.alignment import align_transcript_diarization
    from feedspeechback.activities.diarization import diarize_audio
    from feedspeechback.activities.evaluation import evaluate_transcript
    from feedspeechback.activities.report import generate_report
    from feedspeechback.activities.transcription import transcribe_audio
    from feedspeechback.contracts.evaluation import Scenario
    from feedspeechback.contracts.report import Report
    from feedspeechback.queues import DIARIZATION_QUEUE, TRANSCRIPTION_QUEUE

# Temporal's default policy retries forever; bounded attempts guarantee the
# workflow reaches a terminal state. Activities signal known-permanent
# failures (corrupt audio, bad credentials) by raising
# ApplicationError(non_retryable=True), which skips remaining attempts.
# Expensive ML activities get fewer attempts than cheap local ones.
_ML_RETRY = RetryPolicy(maximum_attempts=3)
_DEFAULT_RETRY = RetryPolicy(maximum_attempts=5)


async def generate_feedback(audio_path: str, scenario: Scenario) -> Report:
    transcript, diarization = await asyncio.gather(
        workflow.execute_activity(
            transcribe_audio,
            audio_path,
            start_to_close_timeout=timedelta(minutes=30),
            heartbeat_timeout=timedelta(seconds=30),
            task_queue=TRANSCRIPTION_QUEUE,
            retry_policy=_ML_RETRY,
        ),
        workflow.execute_activity(
            diarize_audio,
            audio_path,
            start_to_close_timeout=timedelta(minutes=10),
            task_queue=DIARIZATION_QUEUE,
            retry_policy=_ML_RETRY,
        ),
    )

    # No task_queue: these run on the workflow's own queue (DEFAULT_QUEUE).
    aligned = await workflow.execute_activity(
        align_transcript_diarization,
        args=[transcript, diarization],
        start_to_close_timeout=timedelta(minutes=5),
        retry_policy=_DEFAULT_RETRY,
    )

    evaluation = await workflow.execute_activity(
        evaluate_transcript,
        args=[aligned, scenario],
        start_to_close_timeout=timedelta(minutes=10),
        retry_policy=_DEFAULT_RETRY,
    )

    return await workflow.execute_activity(
        generate_report,
        evaluation,
        start_to_close_timeout=timedelta(minutes=5),
        retry_policy=_DEFAULT_RETRY,
    )
