# 🃏 Toulouse: The ML-Ready 40-Card Playing Cards Framework

> *Because life’s too short for bad code and incomplete decks.*

**Toulouse** is the open-source Python framework for anyone who needs to play, simulate, analyze, or machine-learn with European 40-card games (Italian, Spanish, Portuguese, etc.).

* 🔄 **Flexible**: Support for multiple card systems (extendable to 52, 32, or custom decks)
* 🌍 **Multilingual**: Display cards in multiple languages (en, fr, it, es, de)
* ⚡ **Machine Learning Ready**: One-hot representations, Numpy arrays, fully deterministic
* 🔧 **Modular**: Clean, extensible, documented, PyPI-ready
* 🧑‍💻 **Dev-friendly**: Well-typed, tested, with clear docstrings and a hint of humor

---

## 🚀 Installation

```bash
pip install toulouse
```

---

## ✨ Quick Start

```python
from toulouse.cards import Card
from toulouse.deck import Deck

# Create a single card (Ace of Coins, Italian deck)
card = Card(value=1, suit=0, card_system_key="italian_40", language="it")
print(card)  # Output: "Asso di Denari"

# Create a full shuffled Italian deck
italian_deck = Deck(new=True, card_system_key="italian_40", sorted_deck=False)
print(italian_deck)  # "Deck of 40 cards (italian_40)"
print(italian_deck.pretty_print())

# Draw some cards, work with your hand
hand = italian_deck.draw(3)
print([str(c) for c in hand])

# Use card one-hot state (for ML)
print(hand[0].state)  # Numpy array (length 40)

# Get the deck state (all present cards = 1)
print(italian_deck.state.sum())  # 37
```

---

## 🌍 Supported Card Systems & Languages

* **italian\_40**: Denari, Coppe, Spade, Bastoni
* **spanish\_40**: Oros, Copas, Espadas, Bastos
* More? Just add your own (see below)!

Languages for value names: English, Italian, French, Spanish, German.
*(Suits are always in the local language; "di" stays as separator for now.)*

---

## 🏗️ Extending: Add Your Own Card System

```python
from toulouse.systems import register_card_system

my_system = {
    "suits": ["Red", "Blue"],
    "values": [1, 2, 3],
    "names": {"en": {1: "One", 2: "Two", 3: "Three"}},
    "deck_size": 6,
}
register_card_system("mini_6", my_system)

from toulouse.deck import Deck
mini_deck = Deck(new=True, card_system_key="mini_6")
print(mini_deck)
```

---

## 🤖 Machine Learning / Reinforcement Learning Usage

All cards and decks provide **one-hot numpy arrays** for fast vectorization.

* `card.state` gives you a binary vector (length = deck size)
* `deck.state` is the sum of all present cards (perfect for RL agent states)

Example:

```python
c = Card(value=3, suit=2)
print(c.state)  # [0 0 ... 1 ... 0]
d = Deck(new=True)
print(d.state.sum())  # should be deck_size
```

---

## 📚 API Overview

### Card

* `Card(value, suit, card_system_key, language)`
* `to_index()`: unique position in the deck
* `state`: one-hot numpy vector
* `__str__`, `__repr__`, equality, hashable, immutable

### Deck

* `Deck(new=True, card_system_key="italian_40")`: new deck
* `.draw(n)`, `.append(card)`, `.remove(card)`, `.reset()`, `.shuffle()`
* `.state`: numpy binary vector for present cards
* `.pretty_print()`: group by suit for humans

### System

* Register custom systems with `register_card_system()`
* Get system config with `get_card_system()`

---

## 🧪 Testing

Toulouse ships with a full test suite using pytest.

To run all tests:

```bash
pytest tests/
```

---

## 💡 Why Toulouse?

* Easy integration in RL/ML projects (Scopa, Briscola, Mus…)
* Multilingual card display for education or international games
* Simple but extensible API (add variants, new games, etc.)
* Designed for clean code, with just enough spice

---

## 👩‍💻 Contributing

1. Fork, branch, code, test, PR!
2. Add systems, features, or fix a typo in a card’s name.
3. For rules/GUI, see other repos or wait for a future module.

---

## 📄 License

MIT — Enjoy, remix, and share under the sign of the Ace!

---

*May your decks always be full, your code never shuffled, and your bugs as rare as a perfect hand.*
