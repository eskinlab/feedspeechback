from temporalio import workflow

from feedspeechback.workflows._speech_feedback_pipeline import generate_feedback

with workflow.unsafe.imports_passed_through():
    from feedspeechback.contracts.evaluation import Scenario
    from feedspeechback.contracts.report import Report
    from feedspeechback.contracts.submission import Submission


@workflow.defn
class InterviewWorkflow:
    @workflow.run
    async def run(self, submission: Submission) -> Report:
        return await generate_feedback(
            submission.audio_path, scenario=Scenario.INTERVIEW
        )
