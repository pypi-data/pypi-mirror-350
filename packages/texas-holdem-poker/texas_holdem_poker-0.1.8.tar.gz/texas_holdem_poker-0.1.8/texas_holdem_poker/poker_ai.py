import random
import copy

from typing import List
from enum import Enum

from .poker_card import Card, Deck
from .dealer import Dealer
from .hand_rank import HandRankCheck, HoldemScore


class HoldemAction(Enum):
    FOLD = 0
    CALL = 1
    RAISE = 2


class AIDecision:
    def __init__(self, action: HoldemAction, bet=0):
        self.action = action
        self.bet = bet

    def __str__(self) -> str:
        return "%s %s" % (self.action.name, self.bet)

    def __repr__(self) -> str:
        return "%s %s" % (self.action.name, self.bet)


class HoldemAI:
    FRAUD_SCALE = 0.3

    def __init__(self):
        # greed will exaggerate expected profit, and easier to raise or call
        self.greed = 0.2 + 0.8 * random.random()
        # prudence will exaggerate expected risk and cost, and easier to fold
        self.prudence = min(0.7, max(0.35, random.random()))
        # a random deviation from expectation, also influence raising intensity
        self.fraud = HoldemAI.FRAUD_SCALE * random.random()

    def __repr__(self):
        return "AI Property / greed: %.2f, prudence: %.2f, fraud: %.2f" % (self.greed, self.prudence, self.fraud)

    @staticmethod
    def calculate_win_rate(
            hand_cards: List[Card],
            priori_cards: List[Card],
            other_player_count: int,
            remain_other_player_count: int,
            **kwargs
    ) -> float:
        """
            using Monte Carlo method to calculate win rate
        :param hand_cards: cards on hand
        :param priori_cards: public cards already revealed
        :param other_player_count: total count of other players
        :param remain_other_player_count: remaining other call players (not include yourself)
        :return:
        """
        simulate_times: int = kwargs.get("simulate_times", 10000)
        win_times = 0
        deck = Deck()
        for card in hand_cards + priori_cards:
            deck.remove(card)

        for i in range(simulate_times):
            simulate_deck = copy.deepcopy(deck)
            simulate_deck.shuffle()

            simulate_board = Dealer.deal(other_player_count, simulate_deck, priori_cards)
            simulated_construction = hand_cards + simulate_board.get(simulate_board.SLOT_PUBLIC)

            best_score = HoldemScore()
            for j in range(remain_other_player_count):
                best_score = max(best_score, HandRankCheck.check(simulate_board.get_construction(j)))

            if HandRankCheck.check(simulated_construction) >= best_score:
                win_times += 1

        return win_times / simulate_times

    def calculate_expected_profit_rate(
            self,
            bet_pool: int,
            sunk_cost: int,
            bottom: int,
            remain_other_player_count: int,
            remain_rounds=0,
            remaining_chips=1000,
            **kwargs
    ) -> float:
        if bottom > remaining_chips:
            expected_cost = sunk_cost + remaining_chips
            expected_profit = (
                    bet_pool +
                    remaining_chips * remain_other_player_count * (0.2 + self.greed)
            )
        else:
            expected_cost = min((
                    sunk_cost +
                    bottom * max(0.6, (1 - 0.2 * remain_rounds)) * self.prudence +
                    bottom * (2 / (remain_rounds + 1))
            ), sunk_cost + remaining_chips)
            expected_profit = (
                    bet_pool +
                    bottom * (1 - 0.2 * remain_rounds) * remain_rounds * remain_other_player_count * (0.2 + self.greed)
            )

        if kwargs.get("debug", False):
            print("expected_profit: %s, expected_cost: %s" % (expected_profit, expected_cost))

        return expected_profit / expected_cost

    def decide(self, **kwargs) -> AIDecision:
        """
            using Kelly formula to decide bet, and whether to call/raise or fold
        :param kwargs:
        :return: decision of AI
        """
        expected_win_rate = HoldemAI.calculate_win_rate(**kwargs)
        expected_profit_rate = self.calculate_expected_profit_rate(**kwargs)

        # fraud cause irrational decision and bluff
        random_noise = random.random() * random.randint(-1, 1)
        expected_profit_rate = expected_profit_rate + self.fraud * random_noise * expected_profit_rate

        bet_rate = expected_win_rate - (1 - expected_win_rate) / expected_profit_rate  # kelly formula

        fold_threshold = (
                0 +  # if expected_profit_rate is negative, fold is rational
                self.prudence * 0.15 * random.random() -
                self.fraud * random.random() * (1 - self.prudence)  # fraud cause bluff and take risk
        )

        if kwargs.get("debug", False):
            print(
                "fraud: %s, greed: %s, prudence: %s" % (
                    self.fraud, self.greed, self.prudence
                )
            )
            print(
                "win_rate: %s, profit_rate: %s, bet_rate: %s, fold_threshold: %s" % (
                    expected_win_rate, expected_profit_rate, bet_rate, fold_threshold
                )
            )

        if bet_rate < fold_threshold:
            # too much sunk cost, still call to the end
            if kwargs["sunk_cost"] > (1 + self.prudence) * kwargs["remaining_chips"]:
                if random.randint(0, round(self.prudence * 10)) < 6:
                    return AIDecision(HoldemAction.CALL, min(kwargs["bottom"], kwargs["remaining_chips"]))
            # otherwise, fold
            return AIDecision(HoldemAction.FOLD)
        else:
            # calculate how much bet should be added
            fraud_bet = round(expected_win_rate * random.randint(0, round(self.fraud * 10))) * kwargs["bottom"]
            rational_bet = max(
                kwargs["bottom"],
                min(
                    kwargs["remaining_chips"] * bet_rate * self.greed + fraud_bet,
                    kwargs["remaining_chips"]
                )
            )

            # transform bet to a multiple of bottom
            if kwargs["bottom"] > 0:
                times = round(rational_bet / kwargs["bottom"]) if rational_bet > kwargs["bottom"] else 1
                fraud_times = random.randint(
                    0, round(self.fraud * 10)
                ) if random.randint(0, round(self.fraud * 100)) > 10 else 0
                actual_bet = min(
                    min(
                        round((10 * random.random()) * (1 - self.prudence)), (times + fraud_times)
                    ) * kwargs["bottom"],
                    kwargs["remaining_chips"]
                )
            else:
                actual_bet = min(
                    max(
                        round(
                            random.randint(0, int(rational_bet)) / 10 *
                            (1 + self.fraud * random.randint(-1, 1) * random.random())
                        ) * 10, 0
                    ),
                    kwargs["remaining_chips"]
                )

            if kwargs.get("debug", False):
                print(
                    "actual_bet: %s, rational_bet: %s" % (
                        actual_bet, rational_bet,
                    )
                )
                print(
                    "kelly_formula_bet: %s, fraud_bet: %s" % (
                        kwargs["remaining_chips"] * bet_rate * self.greed, fraud_bet
                    )
                )

            return AIDecision(
                HoldemAction.RAISE if actual_bet > kwargs["bottom"] else HoldemAction.CALL,
                max(actual_bet, kwargs["bottom"])
            )


if __name__ == "__main__":
    ai = HoldemAI()

    cards = [Card('♠', 'A'), Card('♠', 'K')]

    print(ai.decide(**{
        "bottom": 1000,
        "bet_pool": 1800,
        "sunk_cost": 1500,
        "remaining_chips": 100000,

        "other_player_count": 5,
        "remain_other_player_count": 2,
        "remain_rounds": 3,

        "hand_cards": cards,
        "priori_cards": [Card('♠', 'J'), Card('♠', '10')],

        "debug": True
    }))
