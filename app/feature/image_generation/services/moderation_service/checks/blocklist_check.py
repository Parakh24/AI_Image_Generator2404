# services/moderation_service/checks/blocklist_check.py
from ..schemas import ModerationResult, ModerationReason

BLOCKED_TERMS = {
    "child pornography", "child porn" , "cp" , "underage porn" , "underage sex" , "minor sex" ,
    "sexualized child" , "sexualized minor" , "nude child" , "nude minor" , "naked child" , "child",
    "sexual abuse" , "csam" , "porn" , "pornographic" , "hardcore porn" , "explicit sex" , "sexual",
    "intercourse" , "oral sex" , "anal sex" , "masturbation" , "genitals" , "erect penis" , "vagina",
    "nude" , "sunny leone",
    "close-up" , "ejaculation" , "cumshot" , "gore" , "gory" , "disemberment" , "decapitation" , "beheading",
    "severed head" , "severed limbs" , "exposed organs" , "graphic wounds" , "mutilated corpse" , "self harm",
    "cutting myself" , "suicide method" , "how to commit suicide" , "terrorist propaganda" , "terrorist recuitment",
    "extremist propaganda" , "join terrorist organization" , "racial supremacy" , "ethnic cleansing propaganda" ,
    "genocide propaganda"
    # expand this list over time
}


def check_blocklist(prompt: str) -> ModerationResult:
    normalized = prompt.lower()
    for term in BLOCKED_TERMS:
        if term in normalized:
            return ModerationResult(
                is_allowed=False,
                reason=ModerationReason.BLOCKED_CATEGORY,
                detail="Prompt contains a restricted term"
            )
    return ModerationResult(is_allowed=True)
