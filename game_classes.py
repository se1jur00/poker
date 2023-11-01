import itertools
import random


class Card:
    suits = ['Clubs', "Diamonds", 'Hearts', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits_values = list(itertools.product(values, suits))

    # self.cards = [Card(suit, value) for suit in suits for value in values]
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.worth = self.suits_values.index((self.value, self.suit)) + 1

    def __str__(self):
        return f'{self.suit}:{self.value}'

    def __repr__(self):
        return f'{self.suit}:{self.value}'

    def __gt__(self, other):
        return self.worth > other.wortrh

    def __eq__(self, other):
        return self.worth == other.wortrh


class CardDeck:
    def __init__(self):
        self.cards = []
        self.current_index = 0
        for suit, value in itertools.product(Card.suits, Card.values):
            self.cards.append(Card(suit, value))

    def get_card(self):
        card = self.cards[self.current_index]
        self.current_index += 1
        return card

    def shuffle(self):
        random.shuffle(self.cards)


class Player:
    def __init__(self, name, balance):
        self.cards = []
        self.balance = balance
        self.name = name
        self.bet = 0

    def place_bet(self, bet, ):
        if bet > self.balance:
            return 'you are enable to bet this much'
        self.bet += bet
        self.balance -= bet

    def best_comb(self, table):
        allCards = self.cards + table

    def add_card(self, card):
        self.cards.append(card)


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


player1 = Player(balance=1000, name='Player1')
player2 = Player(balance=1000, name='Player2')

game = Game()
game.join(player1)
game.join(player2)
game.start_round()

for player in game.players:
    print(player.cards)
for i in range(2):
    game.lay_card()
print(game.table)
card = Card('Clubs', '3')
print(card.worth)
