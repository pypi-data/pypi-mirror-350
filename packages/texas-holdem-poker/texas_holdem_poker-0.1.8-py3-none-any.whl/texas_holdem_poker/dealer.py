from typing import List, Dict, Union

from .poker_card import Deck, Card


class Board:
    SLOT_PUBLIC = "public"

    def __init__(self, player_count: int):
        self.players = [i for i in range(player_count)]
        self.value: Dict[Union[int, str], List[Card]] = {
            **{self.SLOT_PUBLIC: []},
            **{player: [] for player in self.players}
        }

    def assign(self, card: Card, to):
        self.value[to].append(card)

    def get(self, index):
        return self.value.get(index)

    def get_construction(self, player_index: int) -> List[Card]:
        """
            get combination of player cards with the community cards
        """
        return self.value[self.SLOT_PUBLIC] + self.value[player_index]

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)


class Dealer:
    @staticmethod
    def deal(player_count=6, deck=None, public_cards: List[Card] = None) -> Board:
        """
            generate a new board to players
        :param player_count: count of players
        :param deck: deal on an already used deck if assigned
        :param public_cards: assign public cards
        :return: dealt board like {0: ['♣5', '♦2'], ..., 'public': ['♠A', '♣3', '♣6', '♣8', '♦J']}
        """
        # if not assigned, generate a new deck and shuffle
        if not deck:
            new_deck = Deck()
            new_deck.shuffle()
            deck = new_deck

        # deal
        board = Board(player_count)

        for player in range(player_count):
            for i in range(2):
                card = deck.pop()
                board.assign(card, player)

        public_cards = public_cards or []
        for card in public_cards:
            board.assign(card, Board.SLOT_PUBLIC)
        for i in range(5 - len(public_cards)):
            card = deck.pop()
            board.assign(card, Board.SLOT_PUBLIC)

        return board
