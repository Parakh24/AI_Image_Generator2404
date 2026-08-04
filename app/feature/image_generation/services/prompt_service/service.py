from app.feature.image_generation.services.prompt_service.builder import build_final_prompt
from app.feature.image_generation.services.prompt_service.schemas import PromptRequest 

"""
This file is majorly used by the api/routes service, they do not need to enter into 
the details of how the prompt is built, they just need to call this service and get the final prompt.
"""


class PromptService: 
    def compile(self, request: PromptRequest) -> str: 
        return build_final_prompt(
                user_prompt=request.user_prompt,
                business_profile=request.business_profile,
                preset= request.preset,
        )


prompt_service = PromptService() 
