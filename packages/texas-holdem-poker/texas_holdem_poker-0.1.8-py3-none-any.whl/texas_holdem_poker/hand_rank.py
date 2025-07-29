from enum import Enum
from typing import List, Tuple, Iterable, Dict
from collections import Counter

from .poker_card import Card


class HandRank(Enum):
    ROYAL_FLUSH = 9
    STRAIGHT_FLUSH = 8
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 6
    FLUSH = 5
    STRAIGHT = 4
    THREE_OF_A_KIND = 3
    TWO_PAIRS = 2
    ONE_PAIR = 1
    HIGH_CARD = 0
    NONE = -1


class HoldemScore:
    def __init__(self,
                 hand_rank: HandRank = HandRank.NONE,
                 top_rank: Iterable[int] = (1,),
                 kicker: Iterable[int] = (1,)):
        self.hand_rank: HandRank = hand_rank
        self.top_rank: Iterable[int] = top_rank
        self.kicker: Iterable[int] = kicker
        self.value: Iterable[int] = (self.hand_rank.value, *self.top_rank, *self.kicker)

    def __lt__(self, other) -> bool:
        if self.hand_rank == other.hand_rank:
            return self.value < other.value
        else:
            return self.hand_rank.value < other.hand_rank.value

    def __le__(self, other) -> bool:
        if self.hand_rank == other.hand_rank:
            return self.value <= other.value
        else:
            return self.hand_rank.value <= other.hand_rank.value

    def __gt__(self, other) -> bool:
        if self.hand_rank == other.hand_rank:
            return self.value > other.value
        else:
            return self.hand_rank.value > other.hand_rank.value

    def __ge__(self, other) -> bool:
        if self.hand_rank == other.hand_rank:
            return self.value >= other.value
        else:
            return self.hand_rank.value >= other.hand_rank.value

    def __eq__(self, other) -> bool:
        return self.value == other.value if type(self) == type(other) else False

    def __repr__(self) -> str:
        return self.hand_rank.name + str(self.value)

    def __str__(self) -> str:
        return self.hand_rank.name + str(self.value)

    def __hash__(self) -> int:
        return hash(self.hand_rank.name + str(self.value))


class HandRankCheck:
    @classmethod
    def check_straight(cls, cards: List[Card]) -> HoldemScore:
        illusion_cards = []
        for card in cards:
            if card.rank == 14:  # Ace represent both 1 and 14
                illusion_cards.append(Card(card.suit, '1'))
        cards = cards + illusion_cards

        cards = sorted(cards, reverse=True)

        # save suits of ranks, buffer is like {8: ['♦'], 7: ['♦'], 6: ['♦', '♥', '♣'], 5: ['♦'], 4: ['♦']}
        buffer: Dict[str, List[str]] = {}
        for card in cards:
            buffer[card.rank] = buffer.get(card.rank, [])
            buffer[card.rank].append(card.suit)

        best_score = HoldemScore()
        for i in range(len(buffer)):
            ranks = list(buffer.keys())[i:i+5]
            if len(ranks) != 5:
                continue
            is_continuous = all([(ranks[_] - ranks[_ + 1]) == 1 for _ in range(0, 4)])  # whether ranks is continuous
            # each suit of a specific rank can only appear at most once
            suits = sum([list(set(rank_suits)) for rank_suits in list(buffer.values())[i:i+5]], [])  # all suits
            is_same_suits = any([suits_count == 5 for suits_count in Counter(suits).values()])
            top_rank = list(buffer.keys())[i]
            if is_continuous:
                if is_same_suits:
                    if top_rank == 14:
                        return HoldemScore(HandRank.ROYAL_FLUSH)
                    return HoldemScore(HandRank.STRAIGHT_FLUSH, (top_rank,))
                else:
                    best_score = max(best_score, HoldemScore(HandRank.STRAIGHT, (top_rank,)))

        return best_score

    @classmethod
    def check_flush(cls, cards: List[Card]) -> HoldemScore:
        suits: List[str] = [card.suit for card in cards]
        counter: List[Tuple[str, int]] = sorted(Counter(suits).items(), key=lambda x: x[1], reverse=True)
        suit_at_most = counter[0]

        top_suit_ranks = tuple(sorted([card.rank for card in cards if card.suit in suit_at_most[0]], reverse=True)[0:5])

        return HoldemScore(
            HandRank.FLUSH,
            (top_suit_ranks[0], ),
            top_suit_ranks[1:]
        ) if suit_at_most[1] >= 5 else HoldemScore()

    @classmethod
    def check_pairs(cls, cards: List[Card]) -> HoldemScore:
        ranks: List[int] = [card.rank for card in cards]
        counter: List[Tuple[int, int]] = sorted(Counter(ranks).items(), key=lambda x: (x[1], x[0]), reverse=True)
        ranks_order = sorted(set(ranks), reverse=True)

        rank_at_most, rank_at_second_most = counter[0], counter[1]
        kickers_1 = [rank for rank in ranks_order if rank != rank_at_most[0]]
        kickers_2 = [rank for rank in ranks_order if rank != rank_at_most[0] and rank != rank_at_second_most[0]]

        if rank_at_most[1] == 4:
            return HoldemScore(HandRank.FOUR_OF_A_KIND, (rank_at_most[0],), (max(kickers_1),))
        elif rank_at_most[1] == 3:
            if rank_at_second_most[1] == 2:
                return HoldemScore(HandRank.FULL_HOUSE, (rank_at_most[0], rank_at_second_most[0]))
            elif rank_at_second_most[1] == 3:
                return HoldemScore(HandRank.FULL_HOUSE, (
                    max(rank_at_most[0], rank_at_second_most[0]),
                    min(rank_at_most[0], rank_at_second_most[0])
                ))
            else:
                return HoldemScore(HandRank.THREE_OF_A_KIND, (rank_at_most[0],), kickers_1[0:2])
        elif rank_at_most[1] == 2:
            if rank_at_second_most[1] == 2:
                return HoldemScore(HandRank.TWO_PAIRS, (rank_at_most[0], rank_at_second_most[0]), (max(kickers_2),))
            else:
                return HoldemScore(HandRank.ONE_PAIR, (rank_at_most[0],), kickers_1[0:3])
        else:
            return HoldemScore(HandRank.HIGH_CARD, (rank_at_most[0],), kickers_1[0:4])

    @classmethod
    def check(cls, cards: List[Card]) -> HoldemScore:
        return max([
            cls.check_straight(cards),
            cls.check_flush(cards),
            cls.check_pairs(cards)
        ])
