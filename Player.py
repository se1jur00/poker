class Player:
    def __init__(self, name, balance):
        self.cards = []
        self.balance = balance
        self.name = name
        self.bet = 0
        self.kicker : Card

    def __repr__(self):
        return f'{self.name}:{self.cards}'

    def place_bet(self, bet, ):
        if bet > self.balance:
            return 'you are enable to bet this much'
        self.bet += bet
        self.balance -= bet

    def best_comb(self, table):
        allCards = self.cards + table

    def add_card(self, card):
        self.cards.append(card)
    def fold(self):
        self.cards = []