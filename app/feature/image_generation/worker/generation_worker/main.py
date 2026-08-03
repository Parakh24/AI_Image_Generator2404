"""RQ worker entry point for image-generation jobs.

This module configures and starts a single RQ worker that listens to the
image-generation queue stored in Redis.

Environment variables:
    REDIS_URL:
        Redis connection URL.
        Defaults to ``redis://localhost:6379``.

    GENERATION_QUEUE_NAME:
        Name of the RQ queue consumed by this worker.
        Defaults to ``generation``.

The worker is intentionally configured as a single process so that GPU-bound
generation jobs execute sequentially. This helps prevent multiple jobs from
using the same limited GPU resources at the same time.
"""

import logging
import os

from redis import Redis
from rq import Queue, Worker


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
QUEUE_NAME = os.getenv("GENERATION_QUEUE_NAME", "generation")


def start_worker() -> None:
    """Create and start the image-generation RQ worker.

    The function performs the following steps:

    1. Connects to Redis using ``REDIS_URL``.
    2. Creates or references the configured generation queue.
    3. Creates a named RQ worker for that queue.
    4. Starts the worker with scheduler support enabled.

    Scheduler support is required for delayed retries, such as retry intervals
    configured through ``rq.Retry``.

    This call is blocking and keeps running until the worker is stopped.
    """
    redis_conn = Redis.from_url(REDIS_URL)

    queue = Queue(
        name=QUEUE_NAME,
        connection=redis_conn,
    )

    worker = Worker(
        queues=[queue],
        connection=redis_conn,
        name="generation-worker-1",
    )

    worker.work(with_scheduler=True)


if __name__ == "__main__":
    start_worker()