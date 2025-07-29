

# Aces High: Core Python Library

A Python library for modeling playing cards, decks, and core logic for traditional card games. Built with clean, testable design principles and designed to serve as the foundation for more complex gameplay logic.

> 🧠 Built to teach — this library powers the examples in the companion eBook:  
> [**Building Systems Like a Senior Engineer**](https://github.com/asmitty92/aces-high-ebook)

---

## Features

- 🎴 Card and Deck modeling using Pythonic, enum-safe data structures
- 🔁 Standard shuffling, dealing, and deck state management
- 🧪 Fully tested with `pytest`, using a test-first design process
- 🧹 Enforced code quality via `black` and `ruff`
- 📦 Easy-to-install package, published to [PyPI](https://pypi.org/project/aces-high-core/)

---

## Installation

```bash
pip install aces-high-core-py
```

---

## Usage

```python
from aces_high import StandardDeck

deck = StandardDeck()
deck.shuffle()

hand = deck.deal(5)
for card in hand:
    print(card)
```

---

## Development

Clone the repo and install dependencies with [uv](https://github.com/astral-sh/uv):

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Format and lint:

```bash
black src/ tests/
ruff check src/ tests/
```

---

## Publishing

We use `uv publish` and `workflow_dispatch` in GitHub Actions for controlled PyPI deploys. See the `Publish to PyPI` workflow for more.

---

## License

MIT License © Aaron Smith

---

## See Also

📘 [**Aces High eBook**](https://github.com/asmitty92/aces-high-ebook) — Learn how this library was designed and built from scratch, with a focus on practical system design and senior engineering practices.