"""Pipeline wiring tests against Temporal's time-skipping test server.

The pipeline routes activities to three task queues, so the test runs three
workers — a single worker on DEFAULT_QUEUE would reproduce the silent-hang
failure mode these queues are documented for. The ML activities are mocked;
the cheap default-queue activities run for real.

First run downloads the Temporal test-server binary (needs network).
"""

import uuid
from contextlib import asynccontextmanager

import pytest
from temporalio import activity
from temporalio.client import Client, WorkflowFailureError
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.exceptions import ActivityError, ApplicationError
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from feedspeechback.activities.alignment import align_transcript_diarization
from feedspeechback.activities.evaluation import evaluate_transcript
from feedspeechback.activities.report import generate_report
from feedspeechback.contracts.evaluation import Scenario
from feedspeechback.contracts.speaker import Diarization, Speaker, SpeakerSegment
from feedspeechback.contracts.submission import Submission
from feedspeechback.contracts.transcript import Transcript
from feedspeechback.queues import DEFAULT_QUEUE, DIARIZATION_QUEUE, TRANSCRIPTION_QUEUE
from feedspeechback.workflows.interview import InterviewWorkflow
from feedspeechback.workflows.job_meeting import JobMeetingWorkflow


@activity.defn(name="transcribe_audio")
async def transcribe_audio_mock(audio_path: str) -> Transcript:
    return Transcript(text="hello world", language="en")


@activity.defn(name="diarize_audio")
async def diarize_audio_mock(audio_path: str) -> Diarization:
    return Diarization(
        speakers=[Speaker(speaker="A", segments=[SpeakerSegment(start=0.0, end=1.0)])]
    )


@asynccontextmanager
async def pipeline_running(client: Client, transcribe=transcribe_audio_mock):
    default_worker = Worker(
        client,
        task_queue=DEFAULT_QUEUE,
        workflows=[InterviewWorkflow, JobMeetingWorkflow],
        activities=[align_transcript_diarization, evaluate_transcript, generate_report],
    )
    transcription_worker = Worker(
        client, task_queue=TRANSCRIPTION_QUEUE, activities=[transcribe]
    )
    diarization_worker = Worker(
        client, task_queue=DIARIZATION_QUEUE, activities=[diarize_audio_mock]
    )
    async with default_worker, transcription_worker, diarization_worker:
        yield


@pytest.mark.parametrize(
    ("workflow_cls", "expected_scenario"),
    [
        (InterviewWorkflow, Scenario.INTERVIEW),
        (JobMeetingWorkflow, Scenario.JOB_MEETING),
    ],
)
async def test_pipeline_produces_scenario_report(workflow_cls, expected_scenario):
    async with await WorkflowEnvironment.start_time_skipping(
        data_converter=pydantic_data_converter
    ) as env:
        async with pipeline_running(env.client):
            report = await env.client.execute_workflow(
                workflow_cls.run,
                Submission(audio_path="meeting.wav"),
                id=f"test-{uuid.uuid4()}",
                task_queue=DEFAULT_QUEUE,
            )

    assert report.evaluation.scenario == expected_scenario
    assert expected_scenario.value in report.html_path
    assert expected_scenario.value in report.pdf_path


async def test_non_retryable_activity_failure_fails_workflow_on_first_attempt():
    attempts = 0

    @activity.defn(name="transcribe_audio")
    async def corrupt_audio_transcribe(audio_path: str) -> Transcript:
        nonlocal attempts
        attempts += 1
        raise ApplicationError("corrupt audio", non_retryable=True)

    async with await WorkflowEnvironment.start_time_skipping(
        data_converter=pydantic_data_converter
    ) as env:
        async with pipeline_running(env.client, transcribe=corrupt_audio_transcribe):
            with pytest.raises(WorkflowFailureError) as exc_info:
                await env.client.execute_workflow(
                    InterviewWorkflow.run,
                    Submission(audio_path="corrupt.wav"),
                    id=f"test-{uuid.uuid4()}",
                    task_queue=DEFAULT_QUEUE,
                )

    assert attempts == 1
    activity_error = exc_info.value.cause
    assert isinstance(activity_error, ActivityError)
    assert isinstance(activity_error.cause, ApplicationError)
    assert "corrupt audio" in str(activity_error.cause)
