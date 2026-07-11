from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from temporalio.client import WorkflowExecutionStatus, WorkflowHandle
from temporalio.exceptions import WorkflowAlreadyStartedError
from temporalio.service import RPCError, RPCStatusCode

from feedspeechback.contracts.report import Report
from feedspeechback.contracts.submission import Submission
from feedspeechback.queues import DEFAULT_QUEUE
from feedspeechback.temporal import connect_temporal
from feedspeechback.workflows.interview import InterviewWorkflow
from feedspeechback.workflows.job_meeting import JobMeetingWorkflow


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal = await connect_temporal()
    yield


app = FastAPI(lifespan=lifespan)


class AudioRequest(BaseModel):
    audio_path: str


class SubmissionStatus(BaseModel):
    status: str
    result: Report | None = None


def register_scenario_routes(prefix: str, workflow_cls) -> None:
    @app.post(f"/{prefix}", name=f"create_{prefix}", operation_id=f"create_{prefix}")
    async def create(request: AudioRequest):
        try:
            handle: WorkflowHandle = await app.state.temporal.start_workflow(
                workflow_cls.run,
                Submission(audio_path=request.audio_path),
                id=f"{prefix}-{request.audio_path}",
                task_queue=DEFAULT_QUEUE,
            )
        except WorkflowAlreadyStartedError as exc:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Submission already exists for this audio_path",
                    "workflow_id": exc.workflow_id,
                },
            ) from exc

        return {"workflow_id": handle.id}

    @app.get(
        f"/{prefix}/{{workflow_id}}",
        name=f"get_{prefix}_result",
        operation_id=f"get_{prefix}_result",
    )
    async def get_result(workflow_id: str) -> SubmissionStatus:
        handle = app.state.temporal.get_workflow_handle(workflow_id, result_type=Report)
        try:
            description = await handle.describe()
        except RPCError as exc:
            if exc.status == RPCStatusCode.NOT_FOUND:
                raise HTTPException(
                    status_code=404, detail="Workflow not found"
                ) from exc
            raise

        if description.status == WorkflowExecutionStatus.COMPLETED:
            # Completed: the result is already in history, this returns immediately.
            return SubmissionStatus(status="completed", result=await handle.result())

        if (
            description.status is None
            or description.status == WorkflowExecutionStatus.RUNNING
        ):
            return SubmissionStatus(status="running")

        return SubmissionStatus(status=description.status.name.lower())


register_scenario_routes("interview", InterviewWorkflow)
register_scenario_routes("job-meeting", JobMeetingWorkflow)
