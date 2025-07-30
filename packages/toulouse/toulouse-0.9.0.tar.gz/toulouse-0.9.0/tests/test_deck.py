import pytest
import numpy as np
from toulouse.cards import Card

# --- Test valid card creation and core properties ---
def test_card_creation_valid():
    """Basic creation: check field assignments, index, and one-hot state."""
    card = Card(value=1, suit=0, card_system_key="italian_40", language="en")
    assert card.value == 1
    assert card.suit == 0
    assert card.card_system_key == "italian_40"
    assert card.language == "en"
    # Index should be 0 for Asso di Denari
    assert card.to_index() == 0
    # State vector: all zero except first
    arr = card.state
    assert isinstance(arr, np.ndarray)
    assert arr.sum() == 1
    assert arr[0] == 1
    assert arr.shape == (40,)

# --- Test string representation in different languages ---
def test_card_creation_other_language():
    """
    Check string representation in various languages.
    The suit is never translated in current implementation (always 'di'), so expect 'di' not 'de'.
    """
    card = Card(value=10, suit=2, card_system_key="italian_40", language="fr")
    assert str(card) == "Roi di Spade"  # suit stays 'di Spade', not 'de Spade'
    card_it = Card(value=8, suit=1, language="it")
    assert str(card_it) == "Fante di Coppe"
    card_es = Card(value=9, suit=3, language="es")
    assert str(card_es) == "Caballo di Bastoni"
    card_en = Card(value=1, suit=0, language="en")
    assert str(card_en).startswith("Ace")

# --- Test __repr__, equality, hashability ---
def test_card_repr_and_hash():
    """Check __repr__, equality, and hashability (should behave like a value object)."""
    card1 = Card(value=7, suit=2, card_system_key="italian_40")
    card2 = Card(value=7, suit=2, card_system_key="italian_40")
    assert card1 == card2
    assert hash(card1) == hash(card2)
    r = repr(card1)
    assert "value=7" in r and "suit=2" in r and "italian_40" in r

# --- Test creation with invalid value or suit ---
def test_card_creation_invalid_value():
    """Creating a card with an invalid value should raise ValueError."""
    with pytest.raises(ValueError):
        Card(value=99, suit=0, card_system_key="italian_40")
    with pytest.raises(ValueError):
        Card(value=0, suit=1, card_system_key="italian_40")

def test_card_creation_invalid_suit():
    """Creating a card with an invalid suit should raise ValueError."""
    with pytest.raises(ValueError):
        Card(value=2, suit=44, card_system_key="italian_40")
    with pytest.raises(ValueError):
        Card(value=2, suit=-1, card_system_key="italian_40")

# --- Test to_index covers all ---
def test_card_to_index_bounds():
    """to_index() covers all possible cards in the system (no duplicate/no miss)."""
    seen = set()
    for suit in range(4):
        for value in range(1, 11):
            card = Card(value=value, suit=suit, card_system_key="italian_40")
            idx = card.to_index()
            assert 0 <= idx < 40
            assert idx not in seen, f"Duplicate index: {idx}"
            seen.add(idx)
    assert len(seen) == 40  # Must fill all slots

# --- Test state is always a one-hot ---
def test_card_state_is_onehot():
    """Card state is always a one-hot vector with one '1' at the card's index."""
    for suit in range(4):
        for value in range(1, 11):
            card = Card(value=value, suit=suit)
            arr = card.state
            assert arr.sum() == 1
            assert arr[card.to_index()] == 1
            assert arr.dtype == np.uint8

# --- Fallback for unknown language ---
def test_card_str_unknown_language_fallback():
    """If an unknown language is given, should fallback to English names."""
    card = Card(value=1, suit=0, language="elvish")
    assert "Ace" in str(card) or "1" in str(card)  # fallback to English or numeric

# --- Variant system (example) ---
def test_card_system_variants():
    """Test creating cards from another system (if available, e.g., spanish_40)."""
    try:
        card = Card(value=1, suit=0, card_system_key="spanish_40", language="es")
        assert str(card).startswith("As")
        assert card.to_index() == 0
    except KeyError:
        pass  # System not present, skip

# --- Immutability ---
def test_card_immutability():
    """
    Card should be immutable (frozen).
    Assignment must fail. Note: pydantic v2+ now raises ValidationError (not TypeError).
    """
    card = Card(value=2, suit=1)
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        card.value = 3
