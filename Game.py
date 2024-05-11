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
        self.BB = None
        self.next_player = None
        self.max_bet = 0

    def give_players_cards(self):
        for i in range(2):
            for player in self.players.values():
                player.add_card(self.deck.get_card())
        for player in self.players.values():
            player.kicker = max(player.cards, key = lambda x: x.worth)

    def lay_cards_on_table(self):
        for i in range(3):
            self.table.append(self.deck.get_card())
        for _id in self.players:
            self.players[_id].reset_bet()
        self.max_bet = 0


    def start_round(self):
        self.give_players_cards()
        self.SB = list(self.players.values())[len(self.players) - 2]
        self.SB.place_bet(25)
        self.bank += 25
        self.BB = list(self.players.values())[len(self.players)-1]
        self.BB.place_bet(50)
        self.bank += 50
        self.max_bet = 50
        if len(self.players) > 2:
            self.next_player = {"player_id": list(self.players.keys())[0], "player_index": 0, 'object' : list(self.players.values())[0]}


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
        if bet > self.max_bet:
            self.max_bet = bet

    def get_next_player_id(self):
        if self.next_player["player_index"] + 1 == len(self.players):
            self.next_player['player_index'] = 0
            self.next_player['player_id'] = list(self.players.keys())[0]
            self.next_player['object'] = self.players[self.next_player['player_id']]
            return
        self.next_player['player_index'] = self.next_player["player_index"] + 1
        self.next_player['player_id'] =list(self.players.keys())[ self.next_player['player_index']]
        self.next_player['object'] = self.players[self.next_player['player_id']]
        return self.next_player['player_id']

    def check(self, id):
        if id == self.next_player['player_id']:
            if len(self.table) == 0 and self.BB.id == id and self.max_bet == self.BB.bet:
                self.get_next_player_id()
                return 'OK BB'
            elif len(self.table) != 0 and self.next_player['player_index'] == 0:
                self.get_next_player_id()
                return 'OK'
            elif len(self.table) != 0 and list(self.players.keys())[-1] == id:
                if len(self.table) < 5:
                    self.get_next_player_id()
                    self.lay_card()
                    return 'END'
                else:
                    return self.check_winner()

            elif len(self.table) != 0 and list(self.players.values())[self.next_player['player_index']-1].bet == 0:
                self.get_next_player_id()
                return 'OK'
        return  'NOT'


    def call(self, id):
        max_bet = self.max_bet
        player_bet = self.players[id].bet
        player_balance = self.players[id].balance
        dif = max_bet - player_bet
        if player_balance < dif:
            self.bank += player_balance
            self.players[id].bet = max_bet
            self.players[id].balance = 0
        else:
            self.bank += dif
            self.players[id].bet += dif
            self.players[id].balance -= dif
        self.get_next_player_id()
        return self.next_player['object'].name, self.next_player['player_index']
