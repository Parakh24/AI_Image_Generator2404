"""Category keywords and image-style boosts used by the prompt service.

Add a category to both mappings below. The prompt builder detects keywords in
the user's text and appends the corresponding style boost to the final prompt.


1. the keywords used to detect it inside a free-text user prompt 
2. the extra style phrase added to the final prompt when that category is detected 

To add a new category, this is the ONLY file you should need to touch. 
"""

from typing import Dict, List


CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "smart_watches": ["watch", "smartwatch", "smart watch", "wristwatch", "wearable"],
    "electronics_repair": ["electronics repair", "device repair", "phone repair", "screen repair", "phone screen", "circuit board", "soldering", "repair shop"],
    "consumer_electronics": ["smartphone", "phone", "laptop", "tablet", "headphones", "earbuds", "speaker", "camera", "gadget", "electronics"],
    "fashion": ["fashion", "clothing", "apparel", "dress", "shirt", "jacket", "jeans", "outfit", "streetwear"],
    "footwear": ["shoes", "shoe", "sneakers", "sneaker", "boots", "sandals", "footwear"],
    "jewelry": ["jewelry", "jewellery", "necklace", "ring", "bracelet", "earrings", "pendant", "gemstone"],
    "beauty_and_skincare": ["beauty", "skincare", "skin care", "cosmetics", "makeup", "serum", "moisturizer", "lipstick", "foundation"],
    "food_and_beverage": ["food", "restaurant", "cafe", "coffee", "drink", "beverage", "meal", "dish", "dessert", "bakery", "snack"],
    "health_and_fitness": ["fitness", "gym", "workout", "exercise", "wellness", "yoga", "sports", "health supplement", "protein powder"],
    "home_and_furniture": ["furniture", "sofa", "chair", "table", "bed", "home decor", "interior", "lamp", "kitchenware"],
    "automotive": ["automotive", "car", "vehicle", "motorcycle", "bike", "tyre", "tire", "auto parts", "car service"],
    "real_estate": ["real estate", "property", "apartment", "house", "villa", "office space", "home listing"],
    "travel_and_hospitality": ["travel", "tourism", "hotel", "resort", "vacation", "holiday", "flight", "tour package", "destination"],
    "education": ["education", "school", "college", "university", "course", "classroom", "online learning", "training program"],
    "financial_services": ["finance", "banking", "insurance", "investment", "loan", "credit card", "fintech", "savings"],
    "software_and_saas": ["software", "saas", "app", "platform", "dashboard", "cloud service", "cybersecurity", "automation"],
    "professional_services": ["consulting", "agency", "legal services", "law firm", "accounting", "business services", "professional services"],
    "pets": ["pet", "pets", "dog", "cat", "pet food", "pet care", "veterinary"],
    "baby_and_kids": ["baby", "kids", "children", "toy", "toys", "stroller", "nursery", "children's clothing"],
    "books_and_stationery": ["book", "books", "stationery", "notebook", "journal", "pen", "planner", "office supplies"],
}


CATEGORY_STYLE_BOOST: Dict[str, str] = {
    "smart_watches": "close-up wrist shot, sleek band, crisp digital display, premium wearable photography",
    "electronics_repair": "clean workshop lighting, precision tools in frame, intricate technical detail",
    "consumer_electronics": "sleek product lighting, reflective surfaces, modern technology aesthetic, crisp details",
    "fashion": "editorial fashion photography, confident styling, premium fabric texture, dynamic pose",
    "footwear": "low-angle product shot, detailed materials, clean backdrop, premium commercial lighting",
    "jewelry": "luxury macro photography, elegant highlights, refined reflections, exquisite craftsmanship",
    "beauty_and_skincare": "soft beauty lighting, luminous skin tones, clean vanity aesthetic, premium packaging",
    "food_and_beverage": "appetizing food photography, fresh ingredients, rich texture, warm natural lighting",
    "health_and_fitness": "energetic composition, athletic movement, motivational atmosphere, high-contrast lighting",
    "home_and_furniture": "inviting interior styling, balanced composition, natural light, tactile materials",
    "automotive": "dramatic automotive photography, sculpted reflections, dynamic angle, cinematic lighting",
    "real_estate": "wide-angle architectural photography, bright natural light, spacious composition, polished interiors",
    "travel_and_hospitality": "aspirational travel photography, scenic depth, warm sunlight, welcoming atmosphere",
    "education": "bright learning environment, approachable people, clear educational context, optimistic mood",
    "financial_services": "trustworthy corporate aesthetic, clean composition, subtle financial motifs, polished lighting",
    "software_and_saas": "modern digital workspace, clean interface presentation, subtle technology motifs, crisp lighting",
    "professional_services": "professional corporate photography, confident composition, refined office setting, credible tone",
    "pets": "warm lifestyle photography, expressive animal subject, playful energy, soft natural light",
    "baby_and_kids": "bright playful setting, gentle pastel accents, joyful expression, soft diffused lighting",
    "books_and_stationery": "thoughtful flat-lay composition, tactile paper detail, organized desk styling, soft natural light",
}
