"""
Card class for Toulouse – strong, elegant, and not afraid of being one-hot.
"""
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo
import numpy as np
from .systems import get_card_system

class Card(BaseModel):
    value: int
    suit: int  # 0-based
    card_system_key: str = "italian_40"
    language: str = "en"

    model_config = {
        "frozen": True  # replaces class Config: frozen = True
    }

    @field_validator("value")
    @classmethod
    def check_value(cls, v, info: ValidationInfo):
        card_system_key = info.data.get("card_system_key", "italian_40")
        system = get_card_system(card_system_key)
        if v not in system["values"]:
            raise ValueError(f"Value {v} not in allowed values for this system: {system['values']}")
        return v

    @field_validator("suit")
    @classmethod
    def check_suit(cls, v, info: ValidationInfo):
        card_system_key = info.data.get("card_system_key", "italian_40")
        system = get_card_system(card_system_key)
        if not (0 <= v < len(system["suits"])):
            raise ValueError(f"Suit {v} out of range for system suits: {system['suits']}")
        return v

    def to_index(self) -> int:
        """Get canonical index of the card (for one-hot)."""
        system = get_card_system(self.card_system_key)
        idx = self.suit * len(system["values"]) + (self.value - min(system["values"]))
        return idx

    @property
    def state(self) -> np.ndarray:
        """One-hot numpy array for ML/RL."""
        system = get_card_system(self.card_system_key)
        arr = np.zeros(system["deck_size"], dtype=np.uint8)
        arr[self.to_index()] = 1
        return arr

    def __str__(self) -> str:
        system = get_card_system(self.card_system_key)
        names = system["names"].get(self.language, system["names"]["en"])
        value_str = names.get(self.value, str(self.value))
        suit_str = system["suits"][self.suit]
        return f"{value_str} of {suit_str}" if self.language == "en" else f"{value_str} di {suit_str}"

    def __repr__(self) -> str:
        return f"Card(value={self.value}, suit={self.suit}, system='{self.card_system_key}', lang='{self.language}')"
