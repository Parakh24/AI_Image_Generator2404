"""
Category detection logic for the prompt service. 

Combines two layers to decide which product category a request belongs to: 

Layer 2 (checked_first): looks for category keywords inside the user's own prompt text. 
This is the most specific signal for this particular request. 

Layer 1 (checked only if layer 2 finds nothing) : falls back to the business's stored 
default_category, set once when the business was onboarded. 

If neither layer finds a match, this returns None, and the caller should skip adding any 
category-specific style boost.
"""


from typing import Optional 
from app.feature.image_generation.services.prompt_service.categories import CATEGORY_KEYWORDS 
from app.feature.image_generation.services.prompt_service.schemas import BusinessProfile 

def _match_from_prompt(user_prompt: str) -> Optional[str]:

    """
    Layer 2: scans the prompt text for known category keywords. 
    If keywords from more than one category are found, the category with the highest
    number of matches wins (simple-tie-breaking). Returns None if no keyword from any category 
    is found
    """ 
    lowered_prompt = user_prompt.lower() 

    best_category: Optional[str] = None 
    best_match_count = 0 


    for category, keywords in CATEGORY_KEYWORDS.items(): 
        match_count = sum(1 for keyword in keywords if keyword in lowered_prompt)
        if match_count > best_match_count:
            best_match_count = match_count 
            best_category = category 

    return best_category 


def detect_category(user_prompt: str, business_profile: BusinessProfile) -> Optional[str]: 
    """
    Public entry point. Combines layer 2 and layer 1 in the correct order.

    Order of checks:
    1. Try to match a category from the prompt text itself (layer 2) --
       this is the most specific signal.
    2. If nothing matched, fall back to the business's default_category
       (layer 1).
    3. If neither matched, return None -- the caller keeps the prompt
       generic.
    """
    category_from_prompt = _match_from_prompt(user_prompt)
    if category_from_prompt is not None:
        return category_from_prompt

    return business_profile.default_category
    