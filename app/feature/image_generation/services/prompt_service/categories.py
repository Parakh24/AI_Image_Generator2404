"""Electronics repair category keywords and image-style boosts.

Every key in ``CATEGORY_KEYWORDS`` must have a matching entry in
``CATEGORY_STYLE_BOOST`` so the prompt builder can enrich detected categories.
"""

from typing import Dict, List


CATEGORY_KEYWORDS: Dict[str, List[str]] = {


    "mobile_repair_shop":   ["mobile repair","mobile phone repair","phone repair","smartphone repair",
                           "screen replacement","phone screen","battery replacement",
                           "charging port repair",
    ],


    "laptop_repair_center": ["laptop repair","notebook repair","laptop service","laptop screen repair",
                             "laptop motherboard repair","laptop battery replacement",
    ],


    "computer_desktop_repair": ["computer repair","desktop repair","pc repair","computer service",
                                "desktop service","pc troubleshooting","computer hardware repair",  

    ],

    "tv_repair": ["tv repair","television repair","led tv repair","lcd tv repair","smart tv repair",
                   "tv service center","display panel repair",
    ],


    "home_appliance_repair": ["home appliance repair","appliance repair","appliance service",
                              "kitchen appliance repair","multi appliance repair","household appliance repair",
    ],


    "ac_repair_and_service": ["ac repair","ac service","air conditioner repair","air conditioning service",
                              "ac installation","ac maintenance","ac gas refill",
    ],

                              
    "refrigerator_repair": ["refrigerator repair","fridge repair","refrigerator service","fridge service",
                            "freezer repair","refrigerator cooling problem",
    ],


    "washing_machine_repair": ["washing machine repair","washing machine service","washer repair",
                               "laundry machine repair","washing machine installation","washing machine maintenance",
    ],


    "inverter_ups_repair": ["inverter repair","ups repair","inverter service","ups service",
                            "power backup repair","inverter battery service",
    ],


    "electronics_service_center": ["electronics service center","electronic service center",
                                   "multi brand service center","multi-brand service center",
                                   "electronics repair center","electronic device repair",
                                   "electronics repair shop",
    ],


    "cctv_installation_and_repair": ["cctv installation","cctv repair","security camera installation",
                                     "security camera repair","surveillance system repair","cctv service",
                                     "dvr repair","nvr repair",
    ],


    "printer_scanner_repair": ["printer repair","scanner repair","printer service","scanner service",
                               "printer maintenance","laser printer repair","inkjet printer repair",
    ],


    "camera_repair_center": ["camera repair","dslr repair","digital camera repair","camera service center",
                             "camera lens repair","mirrorless camera repair","camera sensor cleaning",
    ],


    "gaming_console_repair": ["gaming console repair","game console repair","playstation repair",
                              "ps4 repair","ps5 repair","xbox repair","nintendo repair",
                              "nintendo switch repair","console controller repair",
    ],


    "smartwatch_wearable_repair": ["smartwatch repair","smart watch repair","wearable device repair",
                                   "fitness tracker repair","apple watch repair",
                                   "smartwatch screen replacement","smartwatch battery replacement",
    ],
}


CATEGORY_STYLE_BOOST: Dict[str, str] = {
    "mobile_repair_shop": "professional mobile repair counter, smartphone diagnostics, precision tools, clean technical lighting",


    "laptop_repair_center": "organized laptop repair bench, open laptop hardware, diagnostic equipment, skilled technician at work",


    "computer_desktop_repair": "professional computer workshop, desktop components, hardware diagnostics, tidy anti-static workspace",


    "tv_repair": "modern television service area, illuminated display panel, careful diagnostics, clean workshop environment",


    "home_appliance_repair": "professional home appliance service scene, experienced technician, practical tools, trustworthy local-service aesthetic",


    "ac_repair_and_service": "air-conditioner service scene, trained HVAC technician, maintenance tools, bright clean residential setting",


    "refrigerator_repair": "refrigerator servicing scene, cooling-system diagnostics, professional technician, clean home environment",


    "washing_machine_repair": "washing-machine service scene, open control panel, repair tools, skilled technician in a bright utility area",


    "inverter_ups_repair": "power-backup repair bench, inverter and UPS components, electrical testing equipment, precise technical detail",


    "electronics_service_center": "modern multi-brand electronics service center, organized repair stations, diagnostic devices, professional customer-service atmosphere",


    "cctv_installation_and_repair": "professional CCTV installation scene, security cameras and cabling, technician at work, crisp surveillance technology detail",


    "printer_scanner_repair": "organized printer service workspace, open printer mechanism, diagnostic tools, clean office-technology aesthetic",


    "camera_repair_center": "precision camera repair bench, DSLR and lens components, delicate tools, premium macro technical photography",


    "gaming_console_repair": "modern gaming-console repair setup, console internals and controllers, neon-accented workshop lighting, detailed electronics work",
    

    "smartwatch_wearable_repair": "close-up wearable-device repair, smartwatch internals, precision micro-tools, crisp screen and component detail",
}
