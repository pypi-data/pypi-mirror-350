"""
    A command-line-interactive texas holdem poker game

    how to play:
        from texas_holdem_poker import HoldemGame

        HoldemGame.run()
"""
import time
import random
import math

from typing import List, Dict

from .poker_ai import HoldemAI, HoldemScore, HandRankCheck, HoldemAction
from .dealer import Dealer


class PlayerProperty:
    def __init__(self, money=1000, ai: HoldemAI = None):
        self.money = money
        self.ai = ai


class HoldemGame:
    BOTTOM = 10
    INITIAL_MONEY = 400
    HUMAN_PLAYER_INDEX = 0

    def __init__(self, player_nums = 6, display_ai_property = False):
        self.player_nums = player_nums
        self.display_ai_property = display_ai_property
        self.properties = {}
        for i in range(self.player_nums):
            self.properties[i] = PlayerProperty(money=self.INITIAL_MONEY, ai=HoldemAI())

        self.total_defeat = 0

    def show_money(self):
        for i in range(self.player_nums):
            if i == self.HUMAN_PLAYER_INDEX:
                print("Your money: %s" % self.properties[i].money)
            else:
                print("Player%s money: %s" % (i, self.properties[i].money))

    @staticmethod
    def input_bet():
        while True:
            bet = input()
            try:
                bet = int(bet.strip())
                break
            except ValueError:
                print("illegal input, please type integer! (tips: negative value like -1 represent fold)")

        if bet < 0:  # fold
            return -1

        if bet == 1:
            bet = 10

        return bet

    def run(self):
        print("""
            Texas Holdem Poker Simulator
        """)
        button, small_blind, big_blind, current_action_player = -1, None, None, None

        while True:  # start a new round
            button = (button + 1) % self.player_nums
            small_blind = (button + 1) % self.player_nums
            big_blind = (button + 2) % self.player_nums

            # property check
            for player in range(self.player_nums):
                if self.properties[player].money <= 0:
                    if player == self.HUMAN_PLAYER_INDEX:
                        print("You lose all your money!")
                        print("Totally defeat %s AIs!" % self.total_defeat)
                        if self.total_defeat > 5:
                            print("Well played!")
                        elif self.total_defeat > 10:
                            print("You are really good at this!")
                        elif self.total_defeat > 20:
                            print("You are pro!")
                        elif self.total_defeat > 50:
                            print("OMG! How did you make it?")

                        if self.display_ai_property:
                            print("\nAI Property:")
                            for player in range(self.player_nums):
                                if player != self.HUMAN_PLAYER_INDEX:
                                    print(self.properties[player].ai)

                        print("try again? Y/N")
                        if input().lower().strip() not in ["y", "1", "yes", "ok", "restart"]:
                            exit()
                        else:
                            print("""
                                Restart game!
                            """)
                            self.__init__(self.player_nums, self.display_ai_property)
                    else:  # other player lose
                        self.total_defeat += 1
                        print("Player%s lost all his money!" % player)
                        time.sleep(1)
                        del self.properties[player].ai
                        print("Player%s is eliminated!" % player)
                        time.sleep(2)
                        self.properties[player].ai = HoldemAI()
                        self.properties[player].money = self.INITIAL_MONEY
                        print("A new AI has come!")
                        print("You have already defeat %s AI!" % self.total_defeat)

            time.sleep(1)
            print("\n")
            self.show_money()

            board = Dealer.deal(self.player_nums)

            pool = 0
            player_bets: dict = {}  # chips player has already bet
            remain_rounds = 4
            remain_players = list(range(self.player_nums))

            community_cards = board.get(board.SLOT_PUBLIC)

            while True:  # every round, pre-flop -> flop -> turn -> river -> showdown
                pool_last_round = pool
                flag_horse_racing = (
                        (len([1 for player in remain_players if self.properties[player].money > 0]) <= 1)
                        and (len(remain_players) > 1) and remain_rounds > 0
                )  # all remaining players bet their all money
                if not flag_horse_racing:
                    print("\nRound: %s" % (4 - remain_rounds))
                else:
                    print("Horse Racing!")
                    if remain_rounds > 1:
                        print("community: %s" % community_cards[0:(6 - remain_rounds)])
                        time.sleep(1)
                    remain_rounds -= 1
                    if remain_rounds != 0:
                        continue

                if (
                        remain_rounds <= 0 or
                        len([1 for player in remain_players if self.properties[player].money > 0]) <= 1
                ):  # game finish
                    # display leaderboard
                    print("community: %s" % community_cards)
                    print("your hands: %s, %s" % (
                        board.get(self.HUMAN_PLAYER_INDEX), HandRankCheck.check(
                            board.get_construction(self.HUMAN_PLAYER_INDEX)
                        )
                    ))
                    for player in remain_players:
                        if player != self.HUMAN_PLAYER_INDEX:
                            print("AI%s hands: %s, %s" % (
                                player, board.get(player), HandRankCheck.check(board.get_construction(player))
                            ))

                    # decide who wins
                    score_status: Dict[HoldemScore, List] = {}

                    for player in remain_players:
                        score = HandRankCheck.check(board.get_construction(player))
                        score_status[score] = score_status.get(score, [])
                        score_status[score].append(player)

                    winner_order: List[List] = [
                        winner_group for score, winner_group in
                        sorted(score_status.items(), key=lambda x: x[0], reverse=True)
                    ]

                    # divide prize pool
                    human_player_earned = -player_bets.get(self.HUMAN_PLAYER_INDEX, 0)
                    for winner_group in winner_order:
                        # announce first winner group
                        if winner_group == winner_order[0]:
                            for winner in winner_group:
                                if winner == self.HUMAN_PLAYER_INDEX:
                                    print("you win!")
                                else:
                                    print("AI%s win!" % winner)

                        # division algorithm
                        winners_by_bet_ascend = sorted(winner_group, key=lambda x: player_bets.get(x))

                        for winner_idx in range(len(winners_by_bet_ascend)):
                            winner = winners_by_bet_ascend[winner_idx]
                            chips_base = player_bets.get(winner)

                            pot = 0
                            for player in player_bets:
                                chips_to_transfer = (
                                    chips_base
                                    if player_bets.get(player, 0) > chips_base else
                                    player_bets.get(player, 0)
                                )
                                player_bets[player] = player_bets.get(player, 0) - chips_to_transfer
                                pot += chips_to_transfer

                            chips_ought_to_win = int(round(pot / len(winners_by_bet_ascend[winner_idx::])))

                            for winner_to_give in winners_by_bet_ascend[winner_idx::]:
                                self.properties[winner_to_give].money += chips_ought_to_win
                                if winner_to_give == self.HUMAN_PLAYER_INDEX:
                                    human_player_earned += chips_ought_to_win

                    # tooltip of earning
                    if human_player_earned > 0:
                        print("you have earned %s!" % human_player_earned)
                        if human_player_earned > 1000 and random.random() > 0.3:
                            print("What a hot 'pot'!")
                    elif human_player_earned < 0:
                        print("you have lost %s!" % abs(human_player_earned))

                    print("continue?")
                    if input().lower().strip() in ["no", "n", "0", "-1", "2"]:
                        exit()
                    print("\n")
                    break

                if remain_rounds != 4:
                    print("community: %s" % community_cards[0:(6 - remain_rounds)])

                bottom = self.BOTTOM if remain_rounds == 4 else 0  # you can check after pre-flop
                first_raise_player = None
                raised_player = None
                chips_on_board = {}
                raising_round = 0  # at most 3 chance to raise
                fold_flag = False

                # first action player: always next to the button
                next_to_button = [player for player in remain_players if player > button]
                current_action_player = next_to_button[0] if next_to_button else remain_players[0]  # if button is end of list
                while True:
                    if first_raise_player == current_action_player:
                        raising_round += 1
                        first_raise_player = None
                    if raised_player == current_action_player:  # end raising
                        break

                    if (self.HUMAN_PLAYER_INDEX == current_action_player):
                        if self.properties[self.HUMAN_PLAYER_INDEX].money <= 0:
                            current_action_player = remain_players[
                                (remain_players.index(current_action_player) + 1) % len(remain_players)
                            ]
                            continue

                        # HUMAN PLAYER ACTION

                        print("now your turn, your cards:", board.get(0))
                        print("pool: %s, current bet: %s" % (pool, bottom))
                        print("remaining money: %s, already bet: %s" % (
                            self.properties[self.HUMAN_PLAYER_INDEX].money, player_bets.get(self.HUMAN_PLAYER_INDEX, 0)
                        ))
                        blind_bet = -1
                        appendix_message = ""
                        if small_blind == self.HUMAN_PLAYER_INDEX and remain_rounds == 4 and raising_round == 0:
                            print("you are small blind, bet %s!" % int(math.floor(self.BOTTOM / 2)))
                            blind_bet = int(math.floor(self.BOTTOM / 2))
                            appendix_message = "(small blind)"
                        elif big_blind == self.HUMAN_PLAYER_INDEX and remain_rounds == 4 and raising_round == 0:
                            print("you are big blind, bet %s!" % self.BOTTOM)
                            blind_bet = self.BOTTOM
                            appendix_message = "(big blind)"
                        else:
                            print("input your bet:")
                        bet = self.input_bet() if blind_bet == -1 else blind_bet
                        if bet < 0:
                            print("you fold.")
                            fold_flag = True
                        else:
                            if bet < bottom and blind_bet == -1:
                                bet = bottom

                            if bet > bottom and raising_round > 3:
                                print("reach the limit of raising (at most 3)!")
                                bet = bottom

                            chips_on_board[self.HUMAN_PLAYER_INDEX] = chips_on_board.get(self.HUMAN_PLAYER_INDEX, [])
                            diff = bet - sum(chips_on_board[self.HUMAN_PLAYER_INDEX])

                            if diff >= self.properties[self.HUMAN_PLAYER_INDEX].money:
                                print("YOU: ALL IN!")
                                diff = self.properties[self.HUMAN_PLAYER_INDEX].money

                            chips_on_board[self.HUMAN_PLAYER_INDEX].append(diff)

                            pool += diff
                            self.properties[self.HUMAN_PLAYER_INDEX].money -= diff
                            player_bets[self.HUMAN_PLAYER_INDEX] = player_bets.get(self.HUMAN_PLAYER_INDEX, 0) + diff

                            chips = sum(chips_on_board.get(self.HUMAN_PLAYER_INDEX, []))

                            if chips > bottom or (blind_bet != -1 and small_blind == self.HUMAN_PLAYER_INDEX):
                                print("you raise bet to %s %s" % (chips, appendix_message))
                                raised_player = self.HUMAN_PLAYER_INDEX
                                first_raise_player = raised_player if first_raise_player is None else first_raise_player
                                bottom = chips
                            else:
                                if raised_player is None:  # First check, None -> 0
                                    raised_player = current_action_player
                                    first_raise_player = raised_player if first_raise_player is None else first_raise_player
                                print("you %s, bet %s" % (("check" if bottom == 0 else "call"), min(chips, bottom)))
                    else:
                        if self.properties[current_action_player].money <= 0:
                            current_action_player = remain_players[
                                (remain_players.index(current_action_player) + 1) % len(remain_players)
                            ]
                            continue

                        time.sleep(max(0.3, 0.7 * random.random()))
                        decision = self.properties[current_action_player].ai.decide(**{
                            "bottom": bottom,
                            "bet_pool": pool_last_round,
                            "sunk_cost": player_bets.get(current_action_player, 0),
                            "remaining_chips": self.properties[current_action_player].money,

                            "other_player_count": self.player_nums - 1,
                            "remain_other_player_count": len(remain_players) - 1,
                            "remain_rounds": remain_rounds,

                            "hand_cards": board.get(current_action_player),
                            "priori_cards": community_cards[0:(6 - remain_rounds)] if remain_rounds != 4 else [],

                            "simulate_times": 1500
                        })

                        appendix_message = ""

                        if small_blind == current_action_player and remain_rounds == 4 and raising_round == 0:
                            decision.bet = int(math.floor(self.BOTTOM / 2))
                            decision.action = HoldemAction.RAISE
                            appendix_message = "(small blind)"
                        if big_blind == current_action_player and remain_rounds == 4 and raising_round == 0:
                            decision.bet = self.BOTTOM
                            decision.action = HoldemAction.RAISE
                            appendix_message = "(big blind)"

                        if decision.action == HoldemAction.FOLD and bottom == 0:
                            decision.action = HoldemAction.CALL

                        if decision.action == HoldemAction.FOLD:
                            print("AI%s fold." % current_action_player)
                            fold_flag = True
                        else:
                            # if reach the limit of raising
                            if decision.action == HoldemAction.RAISE and raising_round > 3:
                                decision.action = HoldemAction.CALL
                                decision.bet = bottom

                            if (decision.bet >= self.properties[current_action_player].money +
                                    sum(chips_on_board.get(current_action_player, []))):
                                print("AI%s: ALL IN!" % current_action_player)

                            if decision.action == HoldemAction.RAISE:
                                print("AI%s raise bet to %s %s" % (current_action_player, decision.bet, appendix_message))
                                raised_player = current_action_player
                                first_raise_player = raised_player if first_raise_player is None else first_raise_player
                                bottom = decision.bet
                            elif decision.action == HoldemAction.CALL:
                                if raised_player is None:  # First check, None -> 0
                                    raised_player = current_action_player
                                    first_raise_player = raised_player if first_raise_player is None else first_raise_player
                                print(
                                    "AI%s %s, bet %s" % (
                                        current_action_player, ("check" if decision.bet == 0 else "call"),
                                        min(
                                            decision.bet,
                                            self.properties[current_action_player].money +
                                            sum(chips_on_board.get(current_action_player, []))
                                        )
                                    )
                                )

                            chips_on_board[current_action_player] = chips_on_board.get(current_action_player, [])

                            diff = bottom - sum(chips_on_board.get(current_action_player, []))
                            if diff > self.properties[current_action_player].money:  # call but have no enough money
                                diff = self.properties[current_action_player].money

                            chips_on_board[current_action_player].append(diff)

                            pool += diff
                            self.properties[current_action_player].money -= diff
                            player_bets[current_action_player] = player_bets.get(current_action_player, 0) + diff

                    next_action_player = remain_players[
                        (remain_players.index(current_action_player) + 1) % len(remain_players)
                    ]

                    if fold_flag:
                        remain_players.remove(current_action_player)
                        fold_flag = False

                    current_action_player = next_action_player

                remain_rounds -= 1


if __name__ == "__main__":
    HoldemGame().run()
