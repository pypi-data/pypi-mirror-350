"""
Deck class for Toulouse: manages a pile of cards with discipline and panache.
"""
import random
from typing import List, Optional, Iterator
import numpy as np
from .systems import get_card_system
from .cards import Card

class Deck:
    """
    A deck of playing cards for a specific card system.
    Mutable (draw, shuffle, append), auto-checks system consistency.
    """
    def __init__(self, cards: Optional[List[Card]] = None, new: bool = False,
                 card_system_key: str = "italian_40", language: str = "en", sorted_deck: bool = True):
        self.card_system_key = card_system_key
        self.language = language
        system = get_card_system(card_system_key)
        if cards:
            for card in cards:
                if card.card_system_key != card_system_key:
                    raise ValueError(f"All cards must be of system '{card_system_key}'.")
            self.cards = list(cards)
        elif new:
            # Build full deck
            self.cards = [Card(value=v, suit=s, card_system_key=card_system_key, language=language)
                          for s in range(len(system["suits"]))
                          for v in system["values"]]
            if not sorted_deck:
                self.shuffle()
        else:
            self.cards = []
        self.deck_size = system["deck_size"]

    def __len__(self):
        return len(self.cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

    def __getitem__(self, idx):
        return self.cards[idx]

    def __str__(self):
        return f"Deck of {len(self.cards)} cards ({self.card_system_key})"

    def __repr__(self):
        preview = ", ".join([str(card) for card in self.cards[:4]])
        return f"Deck(cards=[{preview}, ...], system='{self.card_system_key}')"

    def pretty_print(self) -> str:
        system = get_card_system(self.card_system_key)
        lines = []
        for suit_idx, suit in enumerate(system["suits"]):
            suit_cards = [card for card in self.cards if card.suit == suit_idx]
            suit_str = ", ".join(str(card) for card in suit_cards)
            lines.append(f"{suit}: {suit_str}")
        return "\n".join(lines)

    def draw(self, n: int = 1) -> List[Card]:
        """Draw n cards from the top. If not enough, draw all."""
        n = max(0, min(n, len(self.cards)))
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

    def shuffle(self):
        random.shuffle(self.cards)
        # The cards are now less predictable than the outcome of a game of Sueca played by beginners.

    def sort(self):
        self.cards.sort(key=lambda c: c.to_index())

    def append(self, card: Card):
        if card.card_system_key != self.card_system_key:
            raise ValueError(f"Cannot add card from system '{card.card_system_key}' to '{self.card_system_key}' deck.")
        self.cards.append(card)

    def remove(self, card: Card):
        self.cards.remove(card)

    def contains(self, card: Card) -> bool:
        return card in self.cards

    def reset(self):
        # Like caffeine for your deck: brings it back to full force.
        system = get_card_system(self.card_system_key)
        self.cards = [Card(value=v, suit=s, card_system_key=self.card_system_key, language=self.language)
                      for s in range(len(system["suits"]))
                      for v in system["values"]]

    @property
    def state(self) -> np.ndarray:
        # One-hot vector indicating present cards
        arr = np.zeros(self.deck_size, dtype=np.uint8)
        for card in self.cards:
            arr[card.to_index()] = 1
        return arr

    def move_card_to(self, card: Card, other_deck: 'Deck'):
        self.remove(card)
        other_deck.append(card)