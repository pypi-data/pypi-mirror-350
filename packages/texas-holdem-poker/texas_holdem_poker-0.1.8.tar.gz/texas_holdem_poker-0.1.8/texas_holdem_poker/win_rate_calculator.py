"""
    A realtime command-line-interactive wining rate calculator

    how to use this:
        from texas_holdem_poker import Calculator

        Calculator().run()
"""
from .poker_ai import HoldemAI, Card


class Calculator:
    SUIT_SHORTCUT = {
        "S": "♠",
        "C": "♣",
        "H": "♥",
        "D": "♦",
    }

    def __init__(self, simulate_times=1500):
        self.simulate_times = simulate_times

    def run(self):
        while True:
            try:
                print("Input your hand cards, for examples: \"SJ S10\", S=Spade♠, C=Club♣, H=Heart♥, D=Diamond♦")
                hands = [Card(self.SUIT_SHORTCUT[card_str[0]], card_str[1::]) for card_str in input().upper().split(" ")]
                print("Input community cards, can be empty")
                community_input = input()
                if community_input:
                    community = [
                        Card(self.SUIT_SHORTCUT[card_str[0]], card_str[1::])
                        for card_str in community_input.upper().split(" ")
                    ]
                else:
                    community = []
                print("Input total players and total remaining players(include yourself), for examples:\"6 2\"")
                total_players, remaining_players = input().split(" ")
                print("Win Rate: %s" % HoldemAI.calculate_win_rate(
                    hand_cards=hands,
                    priori_cards=community,
                    other_player_count=int(total_players) - 1,
                    remain_other_player_count=int(remaining_players) - 1,
                    simulate_times=self.simulate_times
                ), "\n")
            except Exception:
                print("Something went wrong, please try again\n")
                pass


if __name__ == "__main__":
    Calculator.run()
