"""
queue_client.py

Thin wrapper around the job queue (Redis + RQ).

generation_service calls enqueue_generation_job() here - it never
imports Redis or RQ itself, and it never imports the image provider.
This file's only job is "put this job_id somewhere a worker can find it".
"""

import os
from redis import Redis
from rq import Queue

_redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
_redis_connection = Redis.from_url(_redis_url)

# One shared queue named "generation" - the worker (built in a later
# step) listens on this exact queue name to pick up jobs.
generation_queue = Queue("generation", connection=_redis_connection)


def enqueue_generation_job(job_id: str) -> None:
    """
    Pushes a job_id onto the queue.

    The string below is the import path RQ will use to find the
    function that should run - it points to a function the Worker
    step will implement. RQ only needs to resolve that import when a
    worker actually picks up the job, not when this function runs -
    so this works correctly even though that worker file doesn't
    exist yet.
    """
    generation_queue.enqueue(
        "app.feature.image_generation.worker.generation_worker.tasks.process_generation_job",
        job_id,
    )
