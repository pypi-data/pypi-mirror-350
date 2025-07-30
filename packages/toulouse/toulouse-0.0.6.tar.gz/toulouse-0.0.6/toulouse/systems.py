"""
Card systems definitions and registration for Toulouse.
This module is where all supported card systems (Italian 40, Spanish 40, etc.) live.
Feel free to add your own system – no border control, just clean data.
"""
from typing import Dict, Any
from copy import deepcopy

_CARD_SYSTEMS: Dict[str, Dict[str, Any]] = {}

# Predefined systems
_CARD_SYSTEMS["italian_40"] = {
    "suits": ["Denari", "Coppe", "Spade", "Bastoni"],
    "values": list(range(1, 11)),  # 1–10
    "names": {
        "en": {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Jack", 9: "Knight", 10: "King"},
        "it": {1: "Asso", 2: "Due", 3: "Tre", 4: "Quattro", 5: "Cinque", 6: "Sei", 7: "Sette", 8: "Fante", 9: "Cavallo", 10: "Re"},
        "fr": {1: "As", 2: "Deux", 3: "Trois", 4: "Quatre", 5: "Cinq", 6: "Six", 7: "Sept", 8: "Valet", 9: "Cavalier", 10: "Roi"},
        "es": {1: "As", 2: "Dos", 3: "Tres", 4: "Cuatro", 5: "Cinco", 6: "Seis", 7: "Siete", 8: "Sota", 9: "Caballo", 10: "Rey"},
        "de": {1: "Ass", 2: "Zwei", 3: "Drei", 4: "Vier", 5: "Fünf", 6: "Sechs", 7: "Sieben", 8: "Bube", 9: "Reiter", 10: "König"},
    },
    "deck_size": 40,
}

# Spanish 40 cards (same values, different suit names)
_CARD_SYSTEMS["spanish_40"] = {
    "suits": ["Oros", "Copas", "Espadas", "Bastos"],
    "values": list(range(1, 11)),
    "names": deepcopy(_CARD_SYSTEMS["italian_40"]["names"]),
    "deck_size": 40,
}

# Add more systems here as needed (standard_52, french_32, sueca_40...)


def get_card_system(key: str) -> Dict[str, Any]:
    """Retrieve a deep copy of the card system config."""
    if key not in _CARD_SYSTEMS:
        raise KeyError(f"Card system '{key}' is not registered.")
    return deepcopy(_CARD_SYSTEMS[key])


def register_card_system(key: str, config: Dict[str, Any]):
    """Register a new card system.
    Args:
        key (str): Name for your card system.
        config (dict): Dict with keys: suits, values, names, deck_size.
    """
    if key in _CARD_SYSTEMS:
        raise ValueError(f"Card system '{key}' already exists!")
    # Basic checks
    for req in ["suits", "values", "names", "deck_size"]:
        if req not in config:
            raise ValueError(f"Missing '{req}' in card system config.")
    _CARD_SYSTEMS[key] = deepcopy(config)