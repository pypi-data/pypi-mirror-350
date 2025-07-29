from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"


class Rank(Enum):
    ACE = "Ace"
    TWO = "Two"
    THREE = "Three"
    FOUR = "Four"
    FIVE = "Five"
    SIX = "Six"
    SEVEN = "Seven"
    EIGHT = "Eight"
    NINE = "Nine"
    TEN = "Ten"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"


face_values = {
    Rank.ACE: 1,
    Rank.TWO: 2,
    Rank.THREE: 3,
    Rank.FOUR: 4,
    Rank.FIVE: 5,
    Rank.SIX: 6,
    Rank.SEVEN: 7,
    Rank.EIGHT: 8,
    Rank.NINE: 9,
    Rank.TEN: 10,
    Rank.JACK: 11,
    Rank.QUEEN: 12,
    Rank.KING: 13,
}


@dataclass(frozen=True, eq=True)
class Card:
    suit: Suit
    rank: Rank

    @property
    def value(self):
        return face_values[self.rank]

    def __repr__(self):
        return f"The {self.rank.value} of {self.suit.value}"
