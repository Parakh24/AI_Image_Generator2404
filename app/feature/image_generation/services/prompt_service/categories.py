"""
Category registry for the prompt service. 
This file stores only DATA -- a lookup table that maps each product category to: 

1. the keywords used to detect it inside a free-text user prompt (layer 2) 
2. the extra style phrase added to the final prompt when that category is detected

To add a new category, this is the only file needs to be touched
"""

from typing import Dict, List 


CATEGORY_KEYWORDS = Dict[str , List[str]] = {
    "smart_watches" : ["watch" , "smartwatch" , "wristwatch" , "wearable"],
    "electronics_repair" : ["repair" , "circuit_board" , "soldering" , "phone_screen"],
}

CATEGORY_STYLE_BOOST: Dict[str , str] = {
    "smart_watches" : "close-up wrist shot , sleek band , digital display",
    "electronics_repair" : "workshop_lighting, tools in frame, technical detail",
                            
}

