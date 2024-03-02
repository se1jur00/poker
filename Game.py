from Card import CardDeck
from Combinations import Combinations
import random
class Game:
    def __init__(self, blind=25):
        self.bank = 0
        self.deck = CardDeck()
        self.deck.shuffle()
        self.table = []
        self.players = {}
        self.SB = ''
        self.BB = ''
        self.next_player = None

    def give_players_cards(self):
        for i in range(2):
            for player in self.players.values():
                player.add_card(self.deck.get_card())
        for player in self.players.values():
            player.kicker = max(player.cards, key = lambda x: x.worth)

    def lay_cards_on_table(self):
        for i in range(3):
            self.table.append(self.deck.get_card())

    def start_round(self):
        self.give_players_cards()
        self.SB = list(self.players.values())[0]
        self.SB.place_bet(25)
        self.bank += 25
        self.BB = list(self.players.values())[1]
        self.BB.place_bet(50)
        self.bank += 50
        if len(self.players) > 2:
            self.next_player = list(self.players.keys())[2]



    def check(self):
        bets = []
        for i in self.players.values():
            bets.append(i.bet)
        return max(bets)

    def join(self, player):
        if len(self.players) < 6:
            self.players[player.id]=player
        else:
            return ('Игра заполнена')

    def lay_card(self):
        self.table.append(self.deck.get_card())


    def kick_player(self, player_id):
        del self.players[player_id]

    def check_winner(self):
        win_combination  = ""
        winners = []
        for combination in Combinations.get_combinations():
            winner = combination(self.players.values(), self.table)
            if winner:
                return combination.__name__, winner

    def place_bet(self, player, bet):
        player.place_bet(bet)
        self.bank += bet

    def get_next_player_id(self):
        self.next_player = list(self.players.values())[list(self.players.keys()).index(self.next_player)+1]
        return self.next_player
