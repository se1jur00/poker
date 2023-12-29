class Combinations:
    combs = ['royal flush', 'straight flush', 'four of kind', 'full house', 'flush', 'straight', 'set', 'two pairs',
             'pairs', 'kicker']

    @staticmethod
    def get_suit_statistics( cards):
        suit_dict = {}
        for card in cards:
            if card.suit in suit_dict:
                suit_dict[card.suit] += 1
            else:
                suit_dict[card.suit] = 1
        return suit_dict

    @staticmethod
    def get_value_statistics(cards):
        value_dict = {}
        for card in cards:
            if card.value in value_dict:
                value_dict[card.value] += 1
            else:
                value_dict[card.value] = 1
        return value_dict

    @staticmethod
    def get_combinations():
        return [Combinations.four_of_a_kind, Combinations.flush, Combinations.set, Combinations.two_pairs,  Combinations.pairs,]

    @staticmethod
    def flush(players, table):
        winners = []
        for player in players:
            suit_dict = Combinations.get_suit_statistics(cards=player.cards +table)
            for suit in suit_dict:
                if suit_dict[suit] >= 5:
                    winners.append(player)
        if len(winners) == 1:
            return winners[0]
        elif len(winners) == 0:
            return
        else:
            kicker_dict = {winner : winner.kicker for winner in winners}
            winner = max(kicker_dict, key = kicker_dict.get)
            return winner


    @staticmethod
    def pairs(players, table):
        winners = []
        for player in players:
            value_dict = Combinations.get_value_statistics(cards=player.cards +table)
            for value in value_dict:
                if value_dict[value] == 2 and value in [card.value for card in player.cards]:
                    winners.append(player)
                    break
        if len(winners) == 1:
            return winners[0]
        elif len(winners) == 0:
            return
        else:
            win_dict = {winner : Combinations.sort_cards(winner.cards+table) for winner in winners}
            win_dict = {winner: hand[0] if hand[0] in winner.cards else hand[1] for winner, hand in win_dict.items()}
            winner = max(win_dict, key = win_dict.get)
            return winner

    def set(players, table):
        winners = []
        for player in players:
            value_dict = Combinations.get_value_statistics(cards=player.cards + table)
            for value in value_dict:
                if value_dict[value] == 3  and value in [card.value for card in player.cards]:
                    winners.append(player)
                    break
        if len(winners) == 1:
            return winners[0]
        elif len(winners) == 0:
            return
        else:
            win_dict = {winner: Combinations.sort_cards(winner.cards + table) for winner in winners}
            win_dict = {winner: hand[0] if hand[0] in winner.cards else hand[1] if hand[1] in winner.cards else hand[2] for winner, hand in win_dict.items()}
            winner = max(win_dict, key=win_dict.get)
            return winner, winners

    def four_of_a_kind(players, table):
        winners = []
        for player in players:
            value_dict = Combinations.get_value_statistics(cards=player.cards + table)
            for value in value_dict:
                if value_dict[value] == 4 and value in [card.value for card in player.cards]:
                    winners.append(player)
                    break
        if len(winners) == 1:
            return winners[0]
        elif len(winners) == 0:
            return
        else:
            win_dict = {winner: Combinations.sort_cards(winner.cards + table) for winner in winners}
            win_dict = {winner: hand[0] if hand[0] in winner.cards
                        else hand[1] if hand[1] in winner.cards
                        else hand[2] if hand[2] in winner.cards
                        else hand[3] for winner, hand in win_dict.items()}
            winner = max(win_dict, key=win_dict.get)
            return winner, winners

    def two_pairs(players, table):
        winners = []
        for player in players:
            sorted_cards = Combinations.sort_cards(player.cards + table)
            print(sorted_cards)
            if sorted_cards[0].value == sorted_cards[1].value and sorted_cards[2].value == sorted_cards[3].value and sorted_cards[0].value != sorted_cards[2].value:
                    winners.append(player)
                    break
        print(winners)
        if len(winners) == 1:
            return winners[0]
        elif len(winners) == 0:
            return
        else:
            win_dict = {winner: Combinations.sort_cards(winner.cards + table) for winner in winners}
            win_dict = {winner: hand[0] if hand[0] in winner.cards
            else hand[1] if hand[1] in winner.cards
            else hand[2] if hand[2] in winner.cards
            else hand[3] for winner, hand in win_dict.items()}
            winner = max(win_dict, key=win_dict.get)
            return winner, winners


    @staticmethod
    def sort_cards(cards):
        value_dict = Combinations.get_value_statistics(cards= cards)
        sort_cards = sorted(cards, key = lambda x: x.worth, reverse = True)
        sort_cards = sorted(sort_cards, key = lambda x: value_dict.get(x.value), reverse = True)
        return sort_cards
