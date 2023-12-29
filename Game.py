from Card import CardDeck
from Combinations import Combinations
class Game:
    def __init__(self, blind=25):
        self.bank = 0
        self.deck = CardDeck()
        self.deck.shuffle()
        self.table = []
        self.players = []

    def give_players_cards(self):
        for i in range(2):
            for player in self.players:
                player.add_card(self.deck.get_card())
        for player in self.players:
            player.kicker = max(player.cards, key = lambda x: x.worth)

    def lay_cards_on_table(self):
        for i in range(3):
            self.table.append(self.deck.get_card())

    def start_round(self):
        self.give_players_cards()
        self.lay_cards_on_table()

    def check(self):
        bets = []
        for i in self.players:
            bets.append(i.bet)
        return max(bets)

    def join(self, player):
        if len(self.players) < 6:
            self.players.append(player)
        else:
            return ('Игра заполнена')

    def lay_card(self):
        self.table.append(self.deck.get_card())


    def kick_player(self, player_index):
        self.players.pop(player_index)

    def check_winner(self):
        win_combination  = ""
        winners = []
        for combination in Combinations.get_combinations():
            winner = combination(self.players, self.table)
            if winner:
                return combination.__name__, winner
