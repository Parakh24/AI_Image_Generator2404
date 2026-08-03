from generation_worker.pipeline import GenerationPipeline 


def process_generation_job(job_id : str):
    pipeline = GenerationPipeline(job_id) 
    pipeline.run() 