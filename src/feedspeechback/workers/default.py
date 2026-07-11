from feedspeechback.activities.alignment import align_transcript_diarization
from feedspeechback.activities.evaluation import evaluate_transcript
from feedspeechback.activities.report import generate_report
from feedspeechback.queues import DEFAULT_QUEUE
from feedspeechback.workers._runner import run_worker
from feedspeechback.workflows.interview import InterviewWorkflow
from feedspeechback.workflows.job_meeting import JobMeetingWorkflow

if __name__ == "__main__":
    run_worker(
        DEFAULT_QUEUE,
        activities=[
            align_transcript_diarization,
            evaluate_transcript,
            generate_report,
        ],
        workflows=[InterviewWorkflow, JobMeetingWorkflow],
    )
