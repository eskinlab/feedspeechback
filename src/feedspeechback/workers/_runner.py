import asyncio
import logging
from collections.abc import Callable, Sequence

from temporalio.worker import Worker

from feedspeechback.temporal import connect_temporal


def run_worker(
    task_queue: str,
    *,
    activities: Sequence[Callable] = (),
    workflows: Sequence[type] = (),
) -> None:
    logging.basicConfig(level=logging.INFO)

    async def main():
        client = await connect_temporal()

        worker = Worker(
            client,
            task_queue=task_queue,
            activities=list(activities),
            workflows=list(workflows),
        )

        await worker.run()

    asyncio.run(main())
