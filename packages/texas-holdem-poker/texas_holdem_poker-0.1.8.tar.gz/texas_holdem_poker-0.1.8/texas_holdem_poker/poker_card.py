import random

from typing import List


class Card:
    SUITS = ['♠', '♣', '♥', '♦']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    ILLUSION_RANKS = ['1']
    RANK_MAPPING = {"A": 14, "K": 13, "Q": 12, "J": 11}

    def __init__(self, suit: str, rank: str):
        if suit not in self.SUITS or rank not in self.RANKS + self.ILLUSION_RANKS:
            raise ValueError('illegal suit or rank')
        self.suit: str = suit
        self.rank: int = int(self.RANK_MAPPING.get(rank, rank))
        self.value = suit + rank

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    def __lt__(self, other) -> bool:
        return (self.rank, self.suit) < (other.rank, other.suit)

    def __gt__(self, other) -> bool:
        return (self.rank, self.suit) > (other.rank, other.suit)

    def __eq__(self, other) -> bool:
        return self.value == other.value


class Deck:
    """
        a deck of cards
    """

    def __init__(self, cards=None):
        self.cards: List[Card] = cards or [Card(i, k) for i in Card.SUITS for k in Card.RANKS]

    def pop(self, idx=0) -> Card:
        return self.cards.pop(idx)

    def remove(self, card: Card):
        self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def __deepcopy__(self, memodict={}):
        new_object = Deck(self.cards.copy())
        return new_object
