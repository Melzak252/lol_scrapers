ROLES = {
    "top": "top",
    "jungle": "jungle",
    "jg": "jungle",
    "jng": "jungle",
    "mid": "mid",
    "middle": "mid",
    "adc": "adc",
    "bot": "adc",
    "support": "support",
    "supp": "support",
    "sup": "support",
    "aram": "aram"
}

NOT_FOUND_URLS = [
    "https://eune.op.gg/champion/statistics",
    "https://eune.op.gg/aram/statistics",
]

CHAMPION_URL = "https://eune.op.gg/champion/{}/statistics/{}"
ARAM_URL = "https://eune.op.gg/aram/{}/statistics/{}"
SYNERGY_URL = "https://lolchess.gg/synergies"
ITEMS_URL = "https://lolchess.gg/items"
META_URL = "https://lolchess.gg/decks"


def src2https(src: str):
    """Formats src urls to https type
    """
    return f"https:{src}"
