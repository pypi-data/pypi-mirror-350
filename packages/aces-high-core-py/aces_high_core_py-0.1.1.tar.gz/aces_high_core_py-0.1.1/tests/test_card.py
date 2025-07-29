import pytest

from aces_high_core import Card, Rank, Suit


def test_card_has_suit():
    card = Card(Suit.CLUBS, Rank.TWO)
    assert card.suit == Suit.CLUBS


def test_card_has_rank():
    card = Card(Suit.CLUBS, Rank.THREE)
    assert card.rank == Rank.THREE


def test_card_has_repr():
    card = Card(Suit.HEARTS, Rank.KING)
    assert repr(card) == "The King of Hearts"


@pytest.mark.parametrize(
    "rank,expected_value",
    [
        (Rank.ACE, 1),
        (Rank.TWO, 2),
        (Rank.THREE, 3),
        (Rank.FOUR, 4),
        (Rank.FIVE, 5),
        (Rank.SIX, 6),
        (Rank.SEVEN, 7),
        (Rank.EIGHT, 8),
        (Rank.NINE, 9),
        (Rank.TEN, 10),
        (Rank.JACK, 11),
        (Rank.QUEEN, 12),
        (Rank.KING, 13),
    ],
)
def test_card_has_correct_value(rank, expected_value):
    card = Card(Suit.CLUBS, rank)
    assert card.value == expected_value
