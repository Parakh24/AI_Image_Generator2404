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
"""RQ worker entry point for image-generation jobs."""

import logging
import os
import socket

from redis import Redis
from rq import Queue
from rq.worker import SpawnWorker


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379",
)

QUEUE_NAME = os.getenv(
    "GENERATION_QUEUE_NAME",
    "generation",
)


def start_worker() -> None:
    """Start a Windows-compatible RQ image-generation worker."""

    redis_conn = Redis.from_url(REDIS_URL)

    queue = Queue(
        name=QUEUE_NAME,
        connection=redis_conn,
    )

    worker = SpawnWorker(
        queues=[queue],
        connection=redis_conn,
        name=(
            f"generation-worker-"
            f"{socket.gethostname()}-"
            f"{os.getpid()}"
        ),
    )

    worker.work(with_scheduler=True)


if __name__ == "__main__":
    start_worker()