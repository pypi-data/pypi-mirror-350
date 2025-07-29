import pytest

from aces_high_core import Card, Rank, StandardDeck, Suit


@pytest.fixture
def standard_deck():
    return StandardDeck()


def test_deck_starts_with_52_cards(standard_deck):
    assert len(standard_deck) == 52


def test_deck_contains_all_clubs(standard_deck):
    for rank in Rank:
        assert Card(Suit.CLUBS, rank) in standard_deck._cards


def test_deck_contains_all_hearts(standard_deck):
    for rank in Rank:
        assert Card(Suit.HEARTS, rank) in standard_deck._cards


def test_deck_contains_all_spades(standard_deck):
    for rank in Rank:
        assert Card(Suit.SPADES, rank) in standard_deck._cards


def test_deck_contains_all_diamonds(standard_deck):
    for rank in Rank:
        assert Card(Suit.DIAMONDS, rank) in standard_deck._cards


def test_deck_shuffles_itself(standard_deck):
    original_deck = [card for card in standard_deck._cards]
    standard_deck.shuffle()
    assert original_deck != standard_deck._cards


# this test ensures that even if some cards are in the same position post-shuffle, not all of them are
def test_shuffle_moves_most_cards(standard_deck):
    original_deck = standard_deck._cards.copy()
    standard_deck.shuffle()
    # Count how many cards remain in the same position
    unchanged = sum(1 for o, s in zip(original_deck, standard_deck._cards) if o == s)
    assert unchanged < len(original_deck)


# this test ensures a shuffled deck still contains all of the same cards
def test_shuffle_preserves_all_cards(standard_deck):
    original_set = set(standard_deck._cards)
    standard_deck.shuffle()
    assert set(standard_deck._cards) == original_set


def test_deal_returns_one_card(standard_deck):
    dealt = standard_deck.deal()
    assert len(dealt) == 1
    assert len(standard_deck) == 51


def test_deal_returns_expected_number_of_cards(standard_deck):
    dealt = standard_deck.deal(5)
    assert len(dealt) == 5
    assert len(standard_deck) == 47


def test_cannot_deal_more_cards_than_deck_has(standard_deck):
    with pytest.raises(ValueError):
        standard_deck.deal(53)


def test_cannot_deal_zero_cards(standard_deck):
    with pytest.raises(ValueError):
        standard_deck.deal(0)


def test_cannot_deal_negative_cards(standard_deck):
    with pytest.raises(ValueError):
        standard_deck.deal(-1)


def test_cannot_deal_from_empty_deck(standard_deck):
    standard_deck.deal(52)
    with pytest.raises(ValueError):
        standard_deck.deal(1)
