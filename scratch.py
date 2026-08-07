"""Small manual example that compiles and prints an enriched prompt."""

from app.feature.image_generation.services.prompt_service import prompt_service, PromptRequest, PromptPreset, BusinessProfile 

request = PromptRequest(
    user_prompt = "Create a social media advertisement for a new product launch,",
    business_profile = BusinessProfile(
        brand_name="ABC",
        primary_color="blue",
        audience_demographics="students",
    ),
    preset = PromptPreset.SOCIAL_MEDIA_AD,
)

final_prompt = prompt_service.compile(request) 
print(final_prompt) 
