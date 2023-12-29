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
        return self.worth > other.worth

    def __eq__(self, other):
        return self.worth == other.worth
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

